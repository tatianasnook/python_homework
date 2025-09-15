import sqlite3
import pandas as pd

conn = sqlite3.connect("../db/lesson.db")
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()

# Task 1: Complex JOINs with Aggregation
# Find the total price of each of the first 5 orders.  There are several steps.
# You need to join the orders table with the line_items table and the products table. 
# You need to GROUP_BY the order_id.  
# You need to select the order_id and the SUM of the product price times the line_item quantity. 
# Then, you ORDER BY order_id and LIMIT 5.  You don't need a subquery. 
# Print out the order_id and the total price for each of the rows returned.

cursor.execute("""
    SELECT o.order_id, SUM(p.price * li.quantity) AS total_price
    FROM orders AS o
    JOIN line_items AS li ON o.order_id = li.order_id
    JOIN products AS p ON li.product_id = p.product_id
    GROUP BY o.order_id 
    ORDER BY o.order_id
    LIMIT 5;
""")

# Print result's table:
result = cursor.fetchall()
for row in result:
    print(row)


# Task 2: Understanding Subqueries
# For each customer, find the average price of their orders.  This can be done with a subquery.
# You compute the price of each order as in part 1, but you return the customer_id and the total_price.
# That's the subquery. You need to return the total price using AS total_price, 
# and you need to return the customer_id with AS customer_id_b, for reasons that will be clear in a moment.  
# In your main statement, you left join the customer table with the results of the subquery, 
# using ON customer_id = customer_id_b.  You aliased the customer_id column in the subquery 
# so that the column names wouldn't collide.  Then group by customer_id - - this GROUP BY comes after the subquery - - 
# and get the average of the total price of the customer orders.  Return the customer name and the average_total_price.

cursor.execute("""
    SELECT c.customer_name, AVG(sub.total_price) AS average_total_price
    FROM customers AS c
    LEFT JOIN (
        SELECT o.customer_id AS customer_id_b, 
            SUM(p.price * li.quantity) AS total_price
        FROM orders AS o
        JOIN line_items AS li ON o.order_id = li.order_id
        JOIN products AS p ON li.product_id = p.product_id
        GROUP BY o.order_id 
    ) AS sub
    ON c.customer_id = sub.customer_id_b
    GROUP BY c.customer_id, c.customer_name;
""")

# Print result's table:
result = cursor.fetchall()
for row in result:
    print(row)


# Task 3: An Insert Transaction Based on Data
# You want to create a new order for the customer named Perez and Sons. 
# The employee creating the order is Miranda Harris.  The customer wants 10 of each of the 5 least expensive products.
# You first need to do a SELECT statement to retrieve the customer_id,
# another to retrieve the product_ids of the 5 least expensive products, and another to retrieve the employee_id.
# Then, you create the order record and the 5 line_item records comprising the order.  
# You have to use the customer_id, employee_id, and product_id values you obtained from the SELECT statements.
# You have to use the order_id for the order record you created in the line_items records.
# The inserts must occur within the scope of one transaction.
# Then, using a SELECT with a JOIN, 
# print out the list of line_item_ids for the order along with the quantity and product name for each.

try:
    # Get customer_id
    cursor.execute(
        "SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'")
    customer_id = cursor.fetchone()[0]

    # Get employee_id
    cursor.execute(
        "SELECT employee_id FROM employees WHERE (first_name || ' ' || last_name) = 'Miranda Harris'")
    employee_id = cursor.fetchone()[0]

    # Get product_ids of the 5 least expensive products
    cursor.execute(
        "SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
    product_ids = [row[0] for row in cursor.fetchall()]

    # Insert order
    cursor.execute("""
        INSERT INTO orders (customer_id, employee_id, date)
        VALUES (?, ?, DATE('now'))
        RETURNING order_id
    """, (customer_id, employee_id))
    order_id = cursor.fetchone()[0]

    # Insert line items
    for pid in product_ids:
        cursor.execute("""
            INSERT INTO line_items (order_id, product_id, quantity)
            VALUES (?, ?, ?)
        """, (order_id, pid, 10))

    # Commit if all succeeds
    conn.commit()

    # Print the inserted records
    cursor.execute("""
        SELECT li.line_item_id, li.quantity, p.product_name
        FROM line_items AS li
        JOIN products AS p ON li.product_id = p.product_id
        WHERE li.order_id = ?
    """, (order_id,))
    for row in cursor.fetchall():
        print(row)

except Exception as e:
    print("Error occurred:", e)
    conn.rollback()


# Task 4: Aggregation with HAVING
# Find all employees associated with more than 5 orders.
# You want the first_name, the last_name, and the count of orders.
# You need to do a JOIN on the employees and orders tables, and then use GROUP BY, COUNT, and HAVING.

cursor.execute("""
    SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) AS order_count
    FROM employees AS e
    JOIN orders AS o ON e.employee_id = o.employee_id
    GROUP BY e.employee_id, e.first_name, e.last_name
    HAVING COUNT(o.order_id) > 5;
""")

rows = cursor.fetchall()
for row in rows:
    print(row)
    
conn.close()
