import os

import shutil

import tempfile



import pandas as pd

import plotly.express as px

from dash import Dash, dcc, html, Input, Output, no_update



# ---- EDIT THESE 5 LINES TO MATCH YOUR FILE ----

FILE_PATH = 'sample_sales.xlsx'      # or your full OneDrive path: r'C:\...\sales.xlsx'

ITEM_COL = 'Description'

COST_COL = 'Bought'

SALE_COL = 'Sold'

DATE_COL = None   

BRAND_COL = 'Brand'            # e.g. 'Date' if you have one, otherwise leave None

# ------------------------------------------------





def load_data():

    tmp = os.path.join(tempfile.gettempdir(), 'sales_copy.xlsx')

    shutil.copy(FILE_PATH, tmp)

    df = pd.read_excel(tmp, engine='openpyxl')



    # Remove the totals row and any blank rows

    df = df[~df[ITEM_COL].astype(str).str.contains('total', case=False, na=False)]

    df[COST_COL] = pd.to_numeric(df[COST_COL], errors='coerce')
    df[SALE_COL] = pd.to_numeric(df[SALE_COL], errors='coerce').fillna(0)
    df = df.dropna(subset=[COST_COL])



    df['Profit'] = df[SALE_COL] - df[COST_COL]

    if DATE_COL:

        df[DATE_COL] = pd.to_datetime(df[DATE_COL])

        df = df.sort_values(DATE_COL)

        df['x'] = df[DATE_COL]

    else:

        df = df.reset_index(drop=True)

        df['x'] = df.index + 1

    df['Cumulative Profit'] = df['Profit'].cumsum()

    return df





app = Dash(__name__)



app.layout = html.Div(

    style={'maxWidth': '1000px', 'margin': 'auto', 'fontFamily': 'Arial'},

    children=[

        html.H2('Sales Dashboard'),

        html.Div(id='kpis', style={'display': 'flex', 'gap': '24px', 'fontSize': '20px'}),

        dcc.Graph(id='profit-line'),

        dcc.Graph(id='brand-bar'),

        dcc.Interval(id='refresh', interval=5000),  # every 5 seconds

    ],

)





@app.callback(

    Output('kpis', 'children'),

    Output('profit-line', 'figure'),

    Output('brand-bar', 'figure'),

    Input('refresh', 'n_intervals'),

)

def update(_):

    try:

        df = load_data()

    except Exception as e:

        print('Could not read file:', e)

        return no_update, no_update, no_update



    kpis = [

        html.Div(f"Total Cost: ${df[COST_COL].sum():,.2f}"),

        html.Div(f"Total Revenue: ${df[SALE_COL].sum():,.2f}"),

        html.Div(f"Total Profit: ${df['Profit'].sum():,.2f}"),

    ]
    line = px.line(df, x='x', y='Cumulative Profit', title='Cumulative Profit')

    brand_clean = df[BRAND_COL].astype(str).str.strip()
    brand_df = df[df[BRAND_COL].notna() & ~brand_clean.str.lower().isin(['none', 'nan', ''])]

    brand_totals = (
        brand_df.assign(**{BRAND_COL: brand_clean[brand_df.index]})
                .groupby(BRAND_COL, as_index=False)[SALE_COL].sum()
                .nlargest(25, SALE_COL)
                .sort_values(SALE_COL, ascending=True)
    )
    brand_fig = px.bar(
        brand_totals, x=BRAND_COL, y=SALE_COL,
        title='Top 25 Brands by Sold Price',
        labels={SALE_COL: 'Total Sold ($)'},
    )
    brand_fig.update_layout(yaxis_tickprefix='$', yaxis_tickformat=',.0f')

    return kpis, line, brand_fig





if __name__ == '__main__':

    app.run(debug=True)