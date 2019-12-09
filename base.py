import sqlite3
con = sqlite3.connect('data/products.db') # Warning: This file is created in the current directory
con.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name char(100) NOT NULL, price float NOT NULL, stock INTEGER NOT NULL)")
con.execute("INSERT INTO products (name,price,stock) VALUES ('Guitarra Fender',3550,5)")
con.execute("INSERT INTO products (name,price,stock) VALUES ('Guitarra Cort',2600,3)")
con.execute("INSERT INTO products (name,price,stock) VALUES ('Guitarra ESP Star',5450,6)")
con.execute("INSERT INTO products (name,price,stock) VALUES ('Guitarra Ibanez',3600,2)")
con.commit()