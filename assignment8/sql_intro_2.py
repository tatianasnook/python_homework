import pandas as pd
import sqlite3

# Task 5: Read Data into a DataFrame
# Read data into a DataFrame, as described in the lesson. The SQL statement should retrieve the line_item_id,
# quantity, product_id, product_name, and price from a JOIN of the line_items table and the product table. 
# Hint: Your ON statement would be ON line_items.product_id = products.product_id.
#Print the first 5 lines of the resulting DataFrame. Run the program to make sure this much works.
with sqlite3.connect("../db/lesson.db") as conn:
    sql_statement = """SELECT l.line_item_id, l.quantity, l.product_id, p.product_name, p.price
    FROM line_items l JOIN products p
    ON l.product_id = p.product_id"""

    df = pd.read_sql_query(sql_statement, conn)
    print(df.head())

    # Add a column to the DataFrame called "total". This is the quantity times the price. 
    # (This is easy: df['total'] = df['quantity'] * df['price'].) 
    # Print out the first 5 lines of the DataFrame to make sure this works.
    df['total'] = df['quantity'] * df['price']
    print(df.head())

    # Add groupby() code to group by the product_id. Use an agg() method that specifies 
    # 'count' for the line_item_id column, 'sum' for the total column, and 'first' for the 'product_name'. 
    # Print out the first 5 lines of the resulting DataFrame. Run the program to see if it is correct so far.
    grouped = df.groupby('product_id').agg({
        'line_item_id': 'count',
        'total': 'sum',
        'product_name': 'first'
    })
    print(grouped.head())

    # Sort the DataFrame by the product_name column.
    grouped.sort_values(by='product_name', ascending=True, inplace=True)
    
    # Add code to write this DataFrame to a file order_summary.csv, which should be written in 
    # the assignment8 directory. Verify that this file is correct.
    grouped.to_csv("order_summary.csv")
