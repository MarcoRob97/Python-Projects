import pandas as pd
import stripe
import pyodbc

# Place your Stripe key
myStripeKey = 'your_stripe_api'

stripe.api_key = myStripeKey
print('connection made')

# Initialize empty lists to store extracted data and subscription IDs
extracted_data = []

print("the extraction has started")

# Loop until all subscriptions are retrieved (Stripe by default just give you a limit number)
has_more = True
starting_after = None

while has_more: # thats why i use the loop
    # Get the next page of subscriptions
    subscriptions = stripe.Subscription.list(limit=100, starting_after=starting_after)

    # Extract data for each subscription
    for subscription in subscriptions.data:
        status = subscription["status"]
        id_c = subscription["id"]
        customer_id = subscription["customer"]
        current_period_start = subscription["current_period_start"]
        current_period_end = subscription["current_period_end"]
        amount = subscription["items"]["data"][0]["plan"]["amount"]

        # Store extracted data in a dictionary
        myDict_of_data = {    
            "subscription_id": id_c,
            "customer_id": customer_id,
            "current_period_start": current_period_start,
            "current_period_end": current_period_end,
            "amount": amount,
            "status": status
        }
        extracted_data.append(myDict_of_data)

    # Check for more pages
    has_more = subscriptions.has_more
    if has_more:
        # Update starting_after for the next request
        starting_after = subscriptions.data[-1].id

print("the extraction has finished succesfully")


# Create a DataFrame
df = pd.DataFrame(extracted_data)
subscription_data = df.query("status in ('active','past_due')")
print(f"the size of the extraction was {subscription_data.shape}")

# lets normalize the data for better understanding
# subscription_data["current_period_start"] = pd.to_datetime(subscription_data["current_period_start"], unit="s")
# subscription_data["current_period_end"] = pd.to_datetime(subscription_data["current_period_end"], unit="s")

# Divide the amount by 100 to account for showing in a correct way your decimals
subscription_data["amount"] = subscription_data["amount"] / 100


# LETS CREATE THE CONNECTION TO THE DB

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=yourserver;'
                      'Database=yourdb;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
print('Connection succesfully created')



# now lets initialize the list to the onest that could error out
failed_rows = []

# lets start the looping
try:
    # First lets Truncate the table
    cursor.execute("TRUNCATE TABLE temp_table")
    print("table has been truncated")
    print("the insertion of record has started")
    # Loop through subscription data and insert
    for row in subscription_data.itertuples():
        cursor.execute('''
            INSERT INTO temp_table (subscription_id, customer_id, current_period_start, current_period_end, amount, status)
            VALUES (?,?,?,?,?,?)
        ''',
            row.subscription_id, 
            row.customer_id,
            row.current_period_start,
            row.current_period_end, 
            row.amount,
            row.status            
        )
        conn.commit()

except Exception as e:
    failed_rows.append({'row_number':row,'error':e})
        # print(f"Error inserting row: {e}")
        # print(f"Failed row data: {row}")

conn.close()
print("the import was succesfully made it")