import psycopg2
import csv
from connect import connect

conn = connect()
cur = conn.cursor()



# 1. Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        phone VARCHAR(100) UNIQUE NOT NULL
    );
""")




# 2. Insert from CSV
with open('contacts.csv', 'r',encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cur.execute(
            "INSERT INTO contacts (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
            (row['first_name'], row['phone'])
        )
conn.commit()



# 3. Insert from console
name = input("Enter name: ")
phone = input("Enter phone: ")

cur.execute(
    "INSERT INTO contacts(first_name, phone) VALUES (%s, %s)",
    (name, phone)
)
conn.commit()




# 4. Update
ask = input("What do you want to change (Name/Number): ")

if ask == "Name":
    old_phone = input("Enter old phone: ")
    new_name = input("Enter new name: ")

    cur.execute(
        "UPDATE contacts SET first_name = %s WHERE phone = %s",
        (new_name, old_phone)
    )
elif ask == "Number":
    name = input("Enter name: ")
    new_phone = input("Enter new phone: ")

    cur.execute(
        "UPDATE contacts SET phone = %s WHERE first_name = %s",
        (new_phone, name)
    )

conn.commit()




# 5. Query
filter_choice = input("Filter by (Name/Prefix): ")

if filter_choice == "Name":
    name = input("Enter name: ")
    cur.execute(
        "SELECT * FROM contacts WHERE first_name LIKE %s",
        ('%' + name + '%',)
    )
    print(cur.fetchall())

elif filter_choice == "Prefix":
    prefix = input("Enter prefix: ")
    cur.execute(
        "SELECT * FROM contacts WHERE phone LIKE %s",
        (prefix + '%',)
    )
    print(cur.fetchall())




# 6. Delete
delete = input("Delete by (Name/Number): ")

if delete == "Name":
    name = input("Enter name: ")
    cur.execute(
        "DELETE FROM contacts WHERE first_name = %s",
        (name,)
    )

elif delete == "Number":
    phone = input("Enter phone: ")
    cur.execute(
        "DELETE FROM contacts WHERE phone = %s",
        (phone,)
    )

conn.commit()

cur.close()
conn.close()