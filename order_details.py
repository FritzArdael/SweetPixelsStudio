# GET DATA FROM MYSQL
from database import get_connection




# ADD ORDER DETAILS
def add_order_detail(connection, order_id, service_type, service_id, quantity):

    cursor = connection.cursor()

    query = """
        INSERT INTO ORDER_DETAILS
        (
            ORDER_ID,
            SERVICE_TYPE,
            SERVICE_ID,
            QNT
        )
        VALUES (%s, %s, %s, %s)
    """

    values = (
        order_id,
        service_type,
        service_id,
        quantity
    )

    cursor.execute(query, values)

    cursor.close()





# VIEW ORDER_DETAILS
def view_order_details(order_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            ORDER_ID,
            SERVICE_TYPE,
            SERVICE_ID,
            QNT
        FROM ORDER_DETAILS
        WHERE ORDER_ID = %s
    """

    cursor.execute(query, (order_id,))

    rows = cursor.fetchall()

    print("\nORDER_DETAILS")
    print("-" * 50)

    print(
        f"{'ORDER_ID':<10}"
        f"{'TYPE':<15}"
        f"{'SERVICE_ID':<15}"
        f"{'QNT':<10}"
    )

    for row in rows:

        print(
            f"{row[0]:<10}"
            f"{row[1]:<15}"
            f"{row[2]:<15}"
            f"{row[3]:<10}"
        )

    cursor.close()
    connection.close()
