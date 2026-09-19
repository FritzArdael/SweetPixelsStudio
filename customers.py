# GET DATA FROM MYSQL
from database import get_connection




# VIEW CUSTOMERS
def view_customers():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            CUST_ID,
            FIRST_NAME,
            LAST_NAME,
            CONTACT_NUMBER,
            EMAIL,
            STREET,
            CITY,
            POSTAL_CODE,
            DATE_CREATED
        FROM CUSTOMER
        ORDER BY CUST_ID
    """

    cursor.execute(query)

    customers = cursor.fetchall()

    print("\n" + "=" * 80)
    print("CUSTOMERS")
    print("=" * 80)

    for customer in customers:

        print(
            f"ID: {customer[0]} | "
            f"{customer[1]} {customer[2]} | "
            f"{customer[3]} | "
            f"{customer[4]} | "
            f"{customer[6]}"
        )

    cursor.close()
    connection.close()





# CREATE CUSTOMERS
def create_customer():

    print("\n--- CREATE CUSTOMER ---")

    first_name = input("First name: ")
    last_name = input("Last name: ")
    contact_number = input("Contact number: ")
    email = input("Email: ")
    street = input("Street: ")
    city = input("City: ")
    postal_code = input("Postal code: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO CUSTOMER
        (
            FIRST_NAME,
            LAST_NAME,
            CONTACT_NUMBER,
            EMAIL,
            STREET,
            CITY,
            POSTAL_CODE
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        first_name,
        last_name,
        contact_number,
        email,
        street,
        city,
        postal_code
    )

    cursor.execute(query, values)

    connection.commit()

    print("\nCustomer created successfully.")
    print("Customer ID:", cursor.lastrowid)

    cursor.close()
    connection.close()




# MODIFY CUSTOMERS
def modify_customer():

    view_customers()

    cust_id = input("\nEnter Customer ID to modify: ")

    print("\nEnter new information.")

    first_name = input("First name: ")
    last_name = input("Last name: ")
    contact_number = input("Contact number: ")
    email = input("Email: ")
    street = input("Street: ")
    city = input("City: ")
    postal_code = input("Postal code: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE CUSTOMER
        SET
            FIRST_NAME = %s,
            LAST_NAME = %s,
            CONTACT_NUMBER = %s,
            EMAIL = %s,
            STREET = %s,
            CITY = %s,
            POSTAL_CODE = %s
        WHERE CUST_ID = %s
    """

    values = (
        first_name,
        last_name,
        contact_number,
        email,
        street,
        city,
        postal_code,
        cust_id
    )

    cursor.execute(query, values)

    connection.commit()

    print("\nCustomer modified successfully.")

    cursor.close()
    connection.close()




# DELETE CUSTOMER
def delete_customer():

    view_customers()

    cust_id = input("\nEnter Customer ID to delete: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        DELETE FROM CUSTOMER
        WHERE CUST_ID = %s
    """

    cursor.execute(query, (cust_id,))

    connection.commit()

    if cursor.rowcount == 1:
        print("\nCustomer deleted successfully.")
    else:
        print("\nCustomer ID not found.")

    cursor.close()
    connection.close()





# CUSTOMERS MENU
def customers_menu():

    while True:

        print("\n" + "=" * 40)
        print("CUSTOMERS")
        print("=" * 40)

        print("1. View")
        print("2. Create")
        print("3. Modify")
        print("4. Delete")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_customers()

        elif choice == "2":
            create_customer()

        elif choice == "3":
            modify_customer()

        elif choice == "4":
            delete_customer()

        elif choice == "5":
            break

        else:
            print("\nInvalid choice.")
