import pandas as pd
import stripe
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Place your Stripe key
myStripeKey = 'your_stripe_api'

stripe.api_key = myStripeKey
print('connection made')

# Define database connection URL for Microsoft SQL Server
DB_URL = "mssql+pyodbc://username:password@host:port/database"

# Create SQLAlchemy engine and session
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize empty lists to store extracted data and subscription IDs
extracted_data = []

print("the extraction has started")

# Loop until all subscriptions are retrieved (Stripe by default just give you a limit number)
has_more = True
starting_after = None

while has_more:
    # Get the next page of subscriptions
    subscriptions = stripe.Subscription.list(limit=100, starting_after=starting_after)

    # Extract data for each subscription
    for subscription in subscriptions.data:
        status = subscription["status"]
        id_c = subscription["id"]
        customer_id = subscription["customer"]
        current_period_start = pd.to_datetime(subscription["current_period_start"], unit="s")
        current_period_end = pd.to_datetime(subscription["current_period_end"], unit="s")
        amount = subscription["items"]["data"][0]["plan"]["amount"] / 100

        # Append extracted data as a dictionary to the list
        extracted_data.append({
            "subscription_id": id_c,
            "customer_id": customer_id,
            "current_period_start": current_period_start,
            "current_period_end": current_period_end,
            "amount": amount,
            "status": status
        })

    # Check for more pages
    has_more = subscriptions.has_more
    if has_more:
        # Update starting_after for the next request
        starting_after = subscriptions.data[-1].id

print("the extraction has finished successfully")

# Create a session and insert data into the database
session = SessionLocal()
try:
    # Truncate the table before inserting new data
    session.execute("TRUNCATE TABLE IF EXISTS temp_table")
    session.flush()

    # Loop through extracted data and insert each record
    for data in extracted_data:
        session.execute("""
            INSERT INTO temp_table (subscription_id, customer_id, current_period_start, current_period_end, amount, status)
            VALUES (:subscription_id, :customer_id, :current_period_start, :current_period_end, :amount, :status)
        """, data)

    session.commit()
except Exception as e:
    print(f"Error occurred during database insertion: {e}")

finally:
    session.close()

print("the import was successfully made")