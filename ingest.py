import psycopg2

# Database connection parameters
host = "localhost"
port = "5433"
dbname = "mydatabase"
user = "myuser"
password = "mypassword"

# Connect to the database
conn_string = f"host={host} port={port} dbname={dbname} user={user} password={password}"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

# Empty the products table
cursor.execute("DROP TABLE IF EXISTS products;")

# Empty the langchain_pg_embedding table
cursor.execute("DROP TABLE IF EXISTS langchain_pg_embedding;")

# Commit the deletion
conn.commit()

# Create the Products table
create_table_query = """
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    price DECIMAL(10, 2),
    category VARCHAR(100)
);
"""
cursor.execute(create_table_query)

# List of products to insert
products_to_insert = [
    ('Pappardelle al Cinghiale', 19.50, 'Main Course'),
    ('Risotto alla Fiorentina', 18.00, 'Main Course'),
    ('Tiramisu della Nonna', 8.50, 'Dessert'),
    ('Bruschetta', 5.00, 'Starter'),
    ('Caprese Salad', 6.50, 'Starter'),
    ('Gnocchi al Pesto', 16.50, 'Main Course'),
    ('Lasagna', 17.00, 'Main Course'),
    ('Panna Cotta', 7.50, 'Dessert'),
    ('Cannoli', 6.00, 'Dessert'),
    ('Minestrone Soup', 7.00, 'Starter')
]

# Insert product data, checking if it already exists
for product in products_to_insert:
    insert_query = """
    INSERT INTO products (name, price, category)
    SELECT %s, %s, %s
    WHERE
    NOT EXISTS (
        SELECT 1 FROM products WHERE name = %s
    );
    """
    cursor.execute(insert_query, (product[0], product[1], product[2], product[0]))

# Commit the transaction
conn.commit()

# Query the products
query = "SELECT * FROM products;"
cursor.execute(query)

# Fetch and print the results
products = cursor.fetchall()
for product in products:
    print(product)

# Close the cursor and connection
cursor.close()
conn.close()
