import pandas as pd
import random

# Load the customers dataset
customers = pd.read_csv("datasets/olist_customers_dataset.csv")

# Find the top 10 cities by customer frequency
top_cities = (
    customers.groupby(["customer_city", "customer_state"])
    .size()
    .reset_index(name="count")
    .sort_values(by="count", ascending=False)
    .head(10)
)

# Generate warehouse data for each of the top cities
warehouses = []

for i, row in top_cities.iterrows():
    city = row["customer_city"]
    state = row["customer_state"]
    max_capacity = random.randint(500, 2000)
    current_load = random.randint(0, max_capacity)
    warehouse = {
        "warehouse_id": f"WH{i+1:03}",
        "warehouse_name": f"{city.title()} Central",
        "city": city,
        "state": state,
        "latitude": round(random.uniform(-25.0, -15.0), 4),   # Simulated location
        "longitude": round(random.uniform(-50.0, -38.0), 4),
        "max_capacity": max_capacity,
        "current_load": current_load,
        "load_percentage": round((current_load / max_capacity) * 100, 2),
        "specialization": random.choice(["electronics", "clothing", "home", "mixed"]),
        "is_active": 1
    }
    warehouses.append(warehouse)

# Convert to DataFrame and save
df = pd.DataFrame(warehouses)
df.to_csv("datasets/warehouses.csv", index=False)

print("warehouses.csv with top 10 hubs created successfully.")