import random
import pandas as pd

random.seed(42)  # same fake data every time you run it

# ---- Match these to your real headers exactly ----
ITEM_COL = 'Description'
BRAND_COL = 'Brand'
COST_COL = 'Bought'
SALE_COL = 'Sold'
# ---------------------------------------------------

brands = [
    'Northwind', 'Alder & Oak', 'Vantora', 'Brightway', 'Kestrel', 'Moonlark',
    'Ridgeline', 'Copperfield', 'Solstice', 'Halcyon', 'Ironwood', 'Pinecrest',
    'Zephyrix', 'Marlowe', 'Tidewater', 'Saffron Co', 'Bluebell', 'Granite Peak',
    'Lumen', 'Orchard Lane', 'Quillon', 'Redfern', 'Thistle', 'Umber', 'Wrenfield',
    'Ashgrove', 'Birchwood', 'Cinder', 'Driftwood', 'Elmstead',
]
item_types = ['Jacket', 'Shoes', 'Bag', 'Watch', 'Hoodie', 'Jeans', 'Hat', 'Belt', 'Boots', 'Sweater']

rows = []
for i in range(1, 601):
    cost = round(random.uniform(5, 80), 2)
    brand = random.choice(brands) if random.random() > 0.08 else None   # ~8% have no brand
    sold = random.random() > 0.15                                        # ~15% not sold yet
    sale = round(cost * random.uniform(0.8, 3.0), 2) if sold else None
    rows.append({
        ITEM_COL: f'{random.choice(item_types)} #{i}',
        BRAND_COL: brand,
        COST_COL: cost,
        SALE_COL: sale,
    })

df = pd.DataFrame(rows)
df.to_excel('sample_sales.xlsx', index=False, engine='openpyxl')
print('Created sample_sales.xlsx with', len(df), 'rows')