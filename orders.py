import mysql.connector
# GET DATA FROM MYSQL
from database import get_connection
# IMPORT ORDER_DETAILS
from order_details import add_order_detail, view_order_details
# IMPORT CUSTOMERS
from customers import view_customers




# VIEW ORDERS
def view_orders():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            O.ORDER_ID,
            O.CUST_ID,
            C.FIRST_NAME,
            C.LAST_NAME,
            O.ORDER_DATE,
            O.BOOKING_DATE
        FROM ORDERS O
        JOIN CUSTOMER C
            ON O.CUST_ID = C.CUST_ID
        ORDER BY O.ORDER_ID
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    print("\n" + "=" * 90)
    print("ORDERS")
    print("=" * 90)

    for row in rows:

        print(
            f"Order ID: {row[0]} | "
            f"Customer: {row[1]} - {row[2]} {row[3]} | "
            f"Order Date: {row[4]} | "
            f"Booking Date: {row[5]}"
        )

    cursor.close()
    connection.close()





#CREATE ORDERS
def create_order():

    print("\n" + "=" * 50)
    print("CREATE ORDER")
    print("=" * 50)

    # Show customers
    view_customers()

    cust_id = input("\nEnter Customer ID: ")

    booking_date = input(
        "Enter booking date (YYYY-MM-DD): "
    )

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # CREATE ORDER
        query = """
            INSERT INTO ORDERS
            (
                BOOKING_DATE,
                CUST_ID
            )
            VALUES (%s, %s)
        """

        values = (
            booking_date,
            cust_id
        )

        cursor.execute(query, values)

        order_id = cursor.lastrowid

        print("\nOrder created!")
        print("ORDER_ID:", order_id)


        # ADD ORDER DETAIL
        print("\n--- ADD ORDER ITEM ---")

        service_type = input(
            "Service Type (PH/CP): "
        )

        service_id = input(
            "Service ID: "
        )

        quantity = input(
            "Quantity: "
        )

        add_order_detail(
            connection,
            order_id,
            service_type,
            service_id,
            quantity
        )



        # EVERYTHING WORKED
        connection.commit()

        print("\nOrder and order detail saved successfully.")


    # SOMETHING FAILED
    except mysql.connector.Error as error:

        connection.rollback()

        print("\nOrder could not be created.")
        print("No changes were saved.")
        print("Please make sure to enter the following:")
        print("\t- Existing Customer Date")
        print("\t- Correct date format")
        print("\t- Existing Service Type")
        print("\t- Existing Service ID")
        print("\t- Correct quantity value")


    finally:

        cursor.close()
        connection.close()


# MODIFY ORDER
def modify_order():

    print("\nModify Order")

    view_orders()

    order_id = input(
        "\nEnter Order ID to modify: "
    )

    booking_date = input(
        "Enter new booking date (YYYY-MM-DD): "
    )

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE ORDERS
        SET BOOKING_DATE = %s
        WHERE ORDER_ID = %s
    """


    try:
        cursor.execute(
            query,
            (booking_date, order_id)
        )


        if cursor.rowcount == 0:
            print("\nOrder ID does not exist.")
        else:
            connection.commit()
            print("\nOrder modified successfully.")

    except mysql.connector.Error:
        print("\nInvalid date. Please use YYYY-MM-DD.")

        cursor.close()
        connection.close()




# DELETE ORDER
def delete_order():

    view_orders()

    order_id = input(
        "\nEnter Order ID to delete: "
    )

    connection = get_connection()
    cursor = connection.cursor()

    # Delete order details first
    cursor.execute(
        """
        DELETE FROM ORDER_DETAILS
        WHERE ORDER_ID = %s
        """,
        (order_id,)
    )

    # Delete order
    cursor.execute(
        """
        DELETE FROM ORDERS
        WHERE ORDER_ID = %s
        """,
        (order_id,)
    )

    connection.commit()

    if cursor.rowcount == 1:
        print("\nOrder deleted successfully.")
    else:
        print("\nOrder ID not found.")

    cursor.close()
    connection.close()






# ORDERS MENU
def orders_menu():

    while True:

        print("\n" + "=" * 40)
        print("ORDERS")
        print("=" * 40)

        print("1. View")
        print("2. Create")
        print("3. Modify")
        print("4. Delete")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_orders()

        elif choice == "2":
            create_order()

        elif choice == "3":
            modify_order()

        elif choice == "4":
            delete_order()

        elif choice == "5":
            break

        else:
            print("\nInvalid choice.")
