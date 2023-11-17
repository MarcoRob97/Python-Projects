# VIN Data Processing

This script processes VIN data from a CSV file, querying a public API to gather additional information about each VIN. The results are then filtered and analyzed to generate meaningful insights.

## Overview

The VIN Data Processing script performs the following steps:

1. **Read from CSV:**
   - Reads VIN data from the specified CSV file.

2. **API Query:**
   - Utilizes the NHTSA API to retrieve detailed information about each VIN.

3. **Data Processing:**
   - Extracts relevant information from the API response.
   - Filters results based on 'Make' and 'Model' criteria.
   - Converts the 'Year' column to integers.

4. **Analysis:**
   - Groups data by 'BodyClass' and generates counts.
   - Produces a DataFrame with the final processed results.

## Usage

1. Ensure you have Python installed on your system.
2. Run the script using a Python interpreter:

   ```bash
   python your_script_name.py
