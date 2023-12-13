# This project outlines a **Python script** for extracting **active subscriptions** from the **Stripe API** and importing them into a **Microsoft SQL Server** database. This pipeline can be deployed on cloud platforms like **AWS** or **Azure** for automated daily data ingestion, enabling you to build dashboards and reports based on up-to-date subscription information.

## Libraries Used
- **pandas**: For data manipulation and analysis.
- **stripe**: Python library for interacting with the **Stripe API**.
- **sqlalchemy**: For connecting to and interacting with the **Microsoft SQL Server** database.
- **pyodbc**: Python driver for connecting to **Microsoft SQL Server** (optional if using a different database connector).

## Usage Instructions
1. **Install dependencies**: Install the required libraries using `pip install pandas stripe sqlalchemy pyodbc` (substitute pyodbc with your preferred database connector if not using **Microsoft SQL Server**).
2. **Configure settings**: Replace the placeholder values in the script with your actual details:
   - `myStripeKey`: Your **Stripe API key**.
   - `DB_URL`: Connection URL for your **Microsoft SQL Server** database (or modify for your database).
   - `temp_table`: Name of the temporary table in your database to store extracted data.
3. **Run the script**: Execute the script to initiate the extraction and database import process.

## Pipeline Workflow
1. **Extraction**: The script utilizes the **Stripe API** to retrieve **active subscriptions** in batches of 100. It iterates through pages until all subscriptions are collected.
2. **Data Processing**: Each subscription record is parsed, and relevant information like ID, customer ID, period start/end, amount, and status is extracted.
3. **Database Import**: The extracted data is inserted in batches into a temporary table in your database.
4. **Data Validation and Processing (Optional)**: You can add additional steps to validate and process the data further before integrating it into your desired dashboards or reports.

## Deployment on Cloud Platforms
This script can be easily deployed on cloud platforms like **AWS** or **Azure** using services like **AWS Lambda** or **Azure Functions**. These services allow you to schedule the script to run automatically on a daily basis, ensuring your database is consistently updated with the latest subscription information.

## Benefits of this Pipeline
- **Automated data ingestion**: Provides a convenient way to regularly update your database with **active subscription data**.
- **Scalability and flexibility**: Cloud deployment options like **AWS** or **Azure** offer scalability and flexibility for handling large datasets and future growth.
- **Data-driven insights**: Enables you to build insightful dashboards and reports based on accurate subscription data, informing business decisions and strategies.
