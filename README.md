#Financhi
Your Personal Financial AI

1. Call quandlhelper.get_pivot_data with start_date (n+2 days ago) and today's_date
2. Populate Stock class with data from Step 1
3. Iterate through each of the days and get following data:
    - three day pivots
    - daily pivots
    - Support, Resistance
4. Generate a CSV file for data generated in Step 3
5. Plot the following charts:
    - Chart 1
        - Price vs. Date(s)
        - Horizontal lines for Support, Resistance,Pivots
    - Chart 2
        - Price, Pivots vs. Date(s)