import pandas as pd

def load_data():
    orders = pd.read_csv("datasets/olist_orders_dataset.csv", dtype=str)
    order_items = pd.read_csv("datasets/olist_order_items_dataset.csv", dtype=str)
    customers = pd.read_csv("datasets/olist_customers_dataset.csv", dtype=str)
    reviews = pd.read_csv("datasets/olist_order_reviews_dataset.csv", dtype=str)
    return orders, order_items, customers, reviews

def preprocess_data(orders, order_items, customers, reviews):
    # Create return flag
    orders["return_flag"] = orders["order_status"].apply(lambda x: 1 if x == "canceled" else 0)
    orders = orders.merge(reviews[["order_id", "review_score"]], on="order_id", how="left")
    orders["return_flag"] = orders.apply(
        lambda row: 1 if row["return_flag"] == 1 or (row["review_score"] in ["1", "2"]) else 0, axis=1
    )

    # Merge customer information
    orders = orders.merge(customers[["customer_id", "customer_city", "customer_state"]], on="customer_id", how="left")

    # Convert timestamps
    orders["order_date"] = pd.to_datetime(orders["order_purchase_timestamp"], errors="coerce")
    orders["delivery_date"] = pd.to_datetime(orders["order_delivered_customer_date"], errors="coerce")

    # Delivery time feature
    orders["delivery_time"] = (orders["delivery_date"] - orders["order_date"]).dt.days

    # Merge order items
    data = orders.merge(order_items[["order_id", "product_id", "price", "freight_value"]], on="order_id", how="left")

    # Price and freight value cleanup
    data["price"] = pd.to_numeric(data["price"], errors="coerce")
    data["freight_value"] = pd.to_numeric(data["freight_value"], errors="coerce")

    # Feature: low price
    data["low_price"] = (data["price"] <= 50).astype(int)

    # Feature: high density city
    high_density_cities = {"São Paulo", "Rio de Janeiro", "Belo Horizonte"}
    data["high_density_city"] = data["customer_city"].apply(lambda x: 1 if x in high_density_cities else 0)

    # Fill missing values
    data.fillna(-99, inplace=True)

    return data

def save_clean_data(data):
    selected_columns = [
        "order_id", "product_id", "price", "freight_value",
        "customer_city", "customer_state", "delivery_time",
        "low_price", "high_density_city", "review_score",
        "return_flag", "order_status", "order_date", "delivery_date"
    ]
    clean_data = data[selected_columns]
    clean_data.to_csv("cleaned_data.csv", index=False)

def main():
    orders, order_items, customers, reviews = load_data()
    data = preprocess_data(orders, order_items, customers, reviews)
    save_clean_data(data)
    print("Data preparation complete. 'cleaned_data.csv' has been saved.")

if __name__ == "__main__":
    main()