import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def execute_query(query, values=(), fetch=False):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, values)

        if fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = None

        return result

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# GET DATA
# ============================================================

def get_customers():
    return execute_query("""
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
    """, fetch=True)


def get_orders():
    return execute_query("""
        SELECT
            O.ORDER_ID,
            O.CUST_ID,
            CONCAT(C.FIRST_NAME, ' ', C.LAST_NAME),
            O.ORDER_DATE,
            O.BOOKING_DATE
        FROM ORDERS O
        JOIN CUSTOMER C
            ON O.CUST_ID = C.CUST_ID
        ORDER BY O.ORDER_ID
    """, fetch=True)


def get_order_details():
    return execute_query("""
        SELECT
            ORDER_DETAIL_ID,
            ORDER_ID,
            SERVICE_TYPE,
            SERVICE_ID,
            QNT
        FROM ORDER_DETAILS
        ORDER BY ORDER_ID, ORDER_DETAIL_ID
    """, fetch=True)


def get_services():
    return execute_query("""
        SELECT
            SERVICE_TYPE,
            SERVICE_NAME
        FROM SERVICES
        ORDER BY SERVICE_TYPE
    """, fetch=True)


def get_photography():
    return execute_query("""
        SELECT
            SERVICE_NUMBER,
            SERVICE_ID,
            CATEGORY,
            NAME,
            DESCRIPTION,
            MIN_HOURS,
            MAX_HOURS,
            MIN_PHOTO,
            MAX_PHOTO,
            BASE_PRICE,
            ADD_ON,
            SERVICE_TYPE,
            DATE_CREATED
        FROM PHOTOGRAPHY
        ORDER BY SERVICE_NUMBER
    """, fetch=True)


def get_custom_products():
    return execute_query("""
        SELECT
            SERVICE_NUMBER,
            SERVICE_ID,
            CATEGORY,
            NAME,
            DESCRIPTION,
            BASE_PRICE,
            SERVICE_TYPE,
            DATE_CREATED
        FROM CUSTOM_PRODUCTS
        ORDER BY SERVICE_NUMBER
    """, fetch=True)


# ============================================================
# TABLE DISPLAY
# ============================================================

current_table = ""


def clear_table():
    for item in tree.get_children():
        tree.delete(item)


def set_columns(columns):
    tree["columns"] = columns

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=130, anchor="center")


def show_data(data):
    clear_table()

    for row in data:
        tree.insert("", tk.END, values=row)


def show_customers():
    global current_table

    current_table = "CUSTOMER"

    columns = (
        "CUST_ID",
        "FIRST_NAME",
        "LAST_NAME",
        "CONTACT_NUMBER",
        "EMAIL",
        "STREET",
        "CITY",
        "POSTAL_CODE",
        "DATE_CREATED"
    )

    set_columns(columns)
    show_data(get_customers())

    title_label.config(text="CUSTOMERS")


def show_orders():
    global current_table

    current_table = "ORDERS"

    columns = (
        "ORDER_ID",
        "CUST_ID",
        "CUSTOMER",
        "ORDER_DATE",
        "BOOKING_DATE"
    )

    set_columns(columns)
    show_data(get_orders())

    title_label.config(text="ORDERS")


def show_order_details():
    global current_table

    current_table = "ORDER_DETAILS"

    columns = (
        "ORDER_DETAIL_ID",
        "ORDER_ID",
        "SERVICE_TYPE",
        "SERVICE_ID",
        "QNT"
    )

    set_columns(columns)
    show_data(get_order_details())

    title_label.config(text="ORDER DETAILS")


def show_services():
    global current_table

    current_table = "SERVICES"

    columns = (
        "SERVICE_TYPE",
        "SERVICE_NAME"
    )

    set_columns(columns)
    show_data(get_services())

    title_label.config(text="SERVICES")


def show_photography():
    global current_table

    current_table = "PHOTOGRAPHY"

    columns = (
        "SERVICE_NUMBER",
        "SERVICE_ID",
        "CATEGORY",
        "NAME",
        "DESCRIPTION",
        "MIN_HOURS",
        "MAX_HOURS",
        "MIN_PHOTO",
        "MAX_PHOTO",
        "BASE_PRICE",
        "ADD_ON",
        "SERVICE_TYPE",
        "DATE_CREATED"
    )

    set_columns(columns)
    show_data(get_photography())

    title_label.config(text="PHOTOGRAPHY")


def show_custom_products():
    global current_table

    current_table = "CUSTOM_PRODUCTS"

    columns = (
        "SERVICE_NUMBER",
        "SERVICE_ID",
        "CATEGORY",
        "NAME",
        "DESCRIPTION",
        "BASE_PRICE",
        "SERVICE_TYPE",
        "DATE_CREATED"
    )

    set_columns(columns)
    show_data(get_custom_products())

    title_label.config(text="CUSTOM PRODUCTS")


# ============================================================
# CUSTOMER - CREATE
# ============================================================

def create_customer():

    window = tk.Toplevel(root)
    window.title("Create Customer")
    window.geometry("450x500")

    labels = [
        "First Name",
        "Last Name",
        "Contact Number",
        "Email",
        "Street",
        "City",
        "Postal Code"
    ]

    entries = []

    for i, label in enumerate(labels):

        tk.Label(
            window,
            text=label
        ).grid(row=i, column=0, padx=10, pady=8, sticky="w")

        entry = tk.Entry(window, width=35)
        entry.grid(row=i, column=1, padx=10, pady=8)

        entries.append(entry)

    def save_customer():

        values = [entry.get().strip() for entry in entries]

        if values[0] == "" or values[1] == "":
            messagebox.showwarning(
                "Missing Information",
                "First Name and Last Name are required."
            )
            return

        execute_query("""
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
        """, values)

        messagebox.showinfo(
            "Success",
            "Customer created successfully."
        )

        window.destroy()
        show_customers()

    tk.Button(
        window,
        text="SAVE",
        width=15,
        command=save_customer
    ).grid(row=8, column=1, pady=20)


# ============================================================
# CUSTOMER - MODIFY
# ============================================================

def modify_customer():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Select Customer",
            "Please select a customer first."
        )
        return

    values = tree.item(selected[0])["values"]

    cust_id = values[0]

    window = tk.Toplevel(root)
    window.title("Modify Customer")
    window.geometry("450x500")

    labels = [
        "First Name",
        "Last Name",
        "Contact Number",
        "Email",
        "Street",
        "City",
        "Postal Code"
    ]

    entries = []

    for i, label in enumerate(labels):

        tk.Label(
            window,
            text=label
        ).grid(row=i, column=0, padx=10, pady=8, sticky="w")

        entry = tk.Entry(window, width=35)
        entry.grid(row=i, column=1, padx=10, pady=8)

        entry.insert(0, values[i + 1])

        entries.append(entry)

    def update_customer():

        new_values = [
            entry.get().strip()
            for entry in entries
        ]

        execute_query("""
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
        """, new_values + [cust_id])

        messagebox.showinfo(
            "Success",
            "Customer updated successfully."
        )

        window.destroy()
        show_customers()

    tk.Button(
        window,
        text="SAVE CHANGES",
        width=15,
        command=update_customer
    ).grid(row=8, column=1, pady=20)


# ============================================================
# CUSTOMER - DELETE
# ============================================================

def delete_customer():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Select Customer",
            "Please select a customer first."
        )
        return

    values = tree.item(selected[0])["values"]

    cust_id = values[0]

    confirm = messagebox.askyesno(
        "Delete Customer",
        f"Delete customer {values[1]} {values[2]}?"
    )

    if not confirm:
        return

    try:

        execute_query(
            "DELETE FROM CUSTOMER WHERE CUST_ID = %s",
            (cust_id,)
        )

        messagebox.showinfo(
            "Success",
            "Customer deleted successfully."
        )

        show_customers()

    except Exception as error:

        messagebox.showerror(
            "Cannot Delete",
            "This customer may have existing orders.\n\n"
            "Delete or reassign the customer's orders first.\n\n"
            f"{error}"
        )


# ============================================================
# ORDER - CREATE
# ============================================================

def create_order():

    window = tk.Toplevel(root)
    window.title("Create Order")
    window.geometry("750x600")

    # --------------------------------------------------------
    # Customer
    # --------------------------------------------------------

    tk.Label(
        window,
        text="Customer ID:"
    ).pack(pady=(15, 5))

    customer_combo = ttk.Combobox(
        window,
        width=40,
        state="readonly"
    )

    customers = get_customers()

    customer_values = []

    for customer in customers:

        customer_values.append(
            f"{customer[0]} - {customer[1]} {customer[2]}"
        )

    customer_combo["values"] = customer_values
    customer_combo.pack()

    # --------------------------------------------------------
    # Booking Date
    # --------------------------------------------------------

    tk.Label(
        window,
        text="Booking Date (YYYY-MM-DD):"
    ).pack(pady=(15, 5))

    booking_entry = tk.Entry(
        window,
        width=30
    )

    booking_entry.pack()

    # --------------------------------------------------------
    # Order Details
    # --------------------------------------------------------

    tk.Label(
        window,
        text="ORDER DETAILS",
        font=("Arial", 12, "bold")
    ).pack(pady=15)

    detail_frame = tk.Frame(window)
    detail_frame.pack()

    tk.Label(
        detail_frame,
        text="Service Type"
    ).grid(row=0, column=0, padx=5)

    tk.Label(
        detail_frame,
        text="Service ID"
    ).grid(row=0, column=1, padx=5)

    tk.Label(
        detail_frame,
        text="Quantity"
    ).grid(row=0, column=2, padx=5)

    details = []

    def add_detail():

        row = len(details) + 1

        service_type = ttk.Combobox(
            detail_frame,
            values=("PH", "CP"),
            width=12,
            state="readonly"
        )

        service_type.grid(
            row=row,
            column=0,
            padx=5,
            pady=5
        )

        service_id = ttk.Combobox(
            detail_frame,
            width=30,
            state="readonly"
        )

        service_id.grid(
            row=row,
            column=1,
            padx=5,
            pady=5
        )

        quantity = tk.Entry(
            detail_frame,
            width=10
        )

        quantity.grid(
            row=row,
            column=2,
            padx=5,
            pady=5
        )

        # ----------------------------------------------------
        # LOAD SERVICES WHEN SERVICE TYPE CHANGES
        # ----------------------------------------------------

        def load_services(event=None):

            service_type_value = service_type.get()

            connection = get_connection()
            cursor = connection.cursor()

            if service_type_value == "PH":

                cursor.execute("""
                    SELECT SERVICE_ID, NAME, BASE_PRICE
                    FROM PHOTOGRAPHY
                    ORDER BY SERVICE_NUMBER
                """)

            elif service_type_value == "CP":

                cursor.execute("""
                    SELECT SERVICE_ID, NAME, BASE_PRICE
                    FROM CUSTOM_PRODUCTS
                    ORDER BY SERVICE_NUMBER
                """)

            rows = cursor.fetchall()

            cursor.close()
            connection.close()

            service_values = []

            for row_data in rows:

                service_values.append(
                    f"{row_data[0]} - {row_data[1]} - ${row_data[2]}"
                )

            service_id["values"] = service_values

            if service_values:
                service_id.current(0)

        service_type.bind(
            "<<ComboboxSelected>>",
            load_services
        )

        details.append(
            (service_type, service_id, quantity)
        )

    # --------------------------------------------------------
    # SAVE ORDER
    # --------------------------------------------------------

    def save_order():

        if not customer_combo.get():

            messagebox.showwarning(
                "Customer Required",
                "Please select a customer."
            )
            return

        if not booking_entry.get():

            messagebox.showwarning(
                "Booking Date Required",
                "Please enter a booking date."
            )
            return

        try:

            customer_id = int(
                customer_combo.get().split(" - ")[0]
            )

            booking_date = booking_entry.get()

            # -----------------------------------------------
            # Create ORDER
            # -----------------------------------------------

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO ORDERS
                (
                    BOOKING_DATE,
                    CUST_ID
                )
                VALUES (%s, %s)
            """, (
                booking_date,
                customer_id
            ))

            order_id = cursor.lastrowid

            # -----------------------------------------------
            # Create ORDER DETAILS
            # -----------------------------------------------

            for service_type, service_id, quantity in details:

                service_type_value = service_type.get()
                service_id_value = service_id.get().split(" - ")[0]
                quantity_value = quantity.get().strip()

                if not service_type_value:
                    raise ValueError(
                        "Every order detail needs a service type."
                    )

                if not service_id_value:
                    raise ValueError(
                        "Every order detail needs a service ID."
                    )

                if not quantity_value:
                    raise ValueError(
                        "Every order detail needs a quantity."
                    )

                cursor.execute("""
                    INSERT INTO ORDER_DETAILS
                    (
                        ORDER_ID,
                        SERVICE_TYPE,
                        SERVICE_ID,
                        QNT
                    )
                    VALUES (%s, %s, %s, %s)
                """, (
                    order_id,
                    service_type_value,
                    service_id_value,
                    int(quantity_value)
                ))

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                f"Order #{order_id} created successfully."
            )

            window.destroy()
            show_orders()

        except Exception as error:

            try:
                connection.rollback()
                cursor.close()
                connection.close()
            except:
                pass

            messagebox.showerror(
                "Error",
                f"Could not create order.\n\n{error}"
            )

    tk.Button(
        window,
        text="CREATE ORDER",
        width=20,
        command=save_order
    ).pack(pady=20)


# ============================================================
# ORDER - MODIFY
# ============================================================

def modify_order():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Select Order",
            "Please select an order first."
        )
        return

    values = tree.item(selected[0])["values"]

    order_id = values[0]
    cust_id = values[1]
    booking_date = values[4]

    window = tk.Toplevel(root)
    window.title("Modify Order")
    window.geometry("450x300")

    tk.Label(
        window,
        text=f"Order #{order_id}",
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    tk.Label(
        window,
        text="Customer ID:"
    ).pack()

    customer_entry = tk.Entry(
        window,
        width=30
    )

    customer_entry.insert(
        0,
        cust_id
    )

    customer_entry.pack(pady=5)

    tk.Label(
        window,
        text="Booking Date:"
    ).pack()

    booking_entry = tk.Entry(
        window,
        width=30
    )

    booking_entry.insert(
        0,
        booking_date
    )

    booking_entry.pack(pady=5)

    def save_changes():

        execute_query("""
            UPDATE ORDERS
            SET
                CUST_ID = %s,
                BOOKING_DATE = %s
            WHERE ORDER_ID = %s
        """, (
            customer_entry.get(),
            booking_entry.get(),
            order_id
        ))

        messagebox.showinfo(
            "Success",
            "Order updated successfully."
        )

        window.destroy()
        show_orders()

    tk.Button(
        window,
        text="SAVE CHANGES",
        width=20,
        command=save_changes
    ).pack(pady=20)


# ============================================================
# ORDER - DELETE
# ============================================================

def delete_order():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Select Order",
            "Please select an order first."
        )
        return

    values = tree.item(selected[0])["values"]

    order_id = values[0]

    confirm = messagebox.askyesno(
        "Delete Order",
        f"Delete Order #{order_id} and all of its details?"
    )

    if not confirm:
        return

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # Delete order details first
        cursor.execute("""
            DELETE FROM ORDER_DETAILS
            WHERE ORDER_ID = %s
        """, (order_id,))

        # Then delete order
        cursor.execute("""
            DELETE FROM ORDERS
            WHERE ORDER_ID = %s
        """, (order_id,))

        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Order deleted successfully."
        )

        show_orders()

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"Could not delete order.\n\n{error}"
        )


# ============================================================
# ORDER DETAILS - DELETE
# ============================================================

def delete_order_detail():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Select Order Detail",
            "Please select an order detail first."
        )
        return

    values = tree.item(selected[0])["values"]

    detail_id = values[0]

    confirm = messagebox.askyesno(
        "Delete Order Detail",
        f"Delete Order Detail #{detail_id}?"
    )

    if not confirm:
        return

    execute_query("""
        DELETE FROM ORDER_DETAILS
        WHERE ORDER_DETAIL_ID = %s
    """, (detail_id,))

    messagebox.showinfo(
        "Success",
        "Order detail deleted."
    )

    show_order_details()


# ============================================================
# CREATE / MODIFY / DELETE BUTTON LOGIC
# ============================================================

def create_current():

    if current_table == "CUSTOMER":
        create_customer()

    elif current_table == "ORDERS":
        create_order()

    else:
        messagebox.showinfo(
            "Coming Next",
            "Create functionality for this section will be added next."
        )


def modify_current():

    if current_table == "CUSTOMER":
        modify_customer()

    elif current_table == "ORDERS":
        modify_order()

    else:
        messagebox.showinfo(
            "Coming Next",
            "Modify functionality for this section will be added next."
        )


def delete_current():

    if current_table == "CUSTOMER":
        delete_customer()

    elif current_table == "ORDERS":
        delete_order()

    elif current_table == "ORDER_DETAILS":
        delete_order_detail()

    else:
        messagebox.showinfo(
            "Coming Next",
            "Delete functionality for this section will be added next."
        )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Sweet Pixels Studio - Business Manager"
)

root.geometry("1400x750")

root.minsize(1000, 600)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(root)

header.pack(
    fill="x",
    padx=10,
    pady=10
)

tk.Label(
    header,
    text="SWEET PIXELS STUDIO",
    font=("Arial", 22, "bold")
).pack()

tk.Label(
    header,
    text="Business Manager",
    font=("Arial", 11)
).pack()


# ============================================================
# MAIN MENU
# ============================================================

menu_frame = tk.Frame(root)

menu_frame.pack(
    fill="x",
    padx=10,
    pady=5
)


tk.Button(
    menu_frame,
    text="CUSTOMERS",
    width=16,
    command=show_customers
).pack(
    side="left",
    padx=5
)


tk.Button(
    menu_frame,
    text="ORDERS",
    width=16,
    command=show_orders
).pack(
    side="left",
    padx=5
)


tk.Button(
    menu_frame,
    text="ORDER DETAILS",
    width=16,
    command=show_order_details
).pack(
    side="left",
    padx=5
)


tk.Button(
    menu_frame,
    text="SERVICES",
    width=16,
    command=show_services
).pack(
    side="left",
    padx=5
)


tk.Button(
    menu_frame,
    text="PHOTOGRAPHY",
    width=16,
    command=show_photography
).pack(
    side="left",
    padx=5
)


tk.Button(
    menu_frame,
    text="CUSTOM PRODUCTS",
    width=18,
    command=show_custom_products
).pack(
    side="left",
    padx=5
)


# ============================================================
# TABLE TITLE
# ============================================================

title_label = tk.Label(
    root,
    text="Select a table",
    font=("Arial", 15, "bold")
)

title_label.pack(
    pady=10
)


# ============================================================
# CRUD BUTTONS
# ============================================================

crud_frame = tk.Frame(root)

crud_frame.pack(
    pady=5
)


tk.Button(
    crud_frame,
    text="CREATE",
    width=15,
    command=create_current
).pack(
    side="left",
    padx=5
)


tk.Button(
    crud_frame,
    text="MODIFY",
    width=15,
    command=modify_current
).pack(
    side="left",
    padx=5
)


tk.Button(
    crud_frame,
    text="DELETE",
    width=15,
    command=delete_current
).pack(
    side="left",
    padx=5
)


# ============================================================
# TABLE
# ============================================================

table_frame = tk.Frame(root)

table_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


vertical_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical"
)

vertical_scrollbar.pack(
    side="right",
    fill="y"
)


horizontal_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="horizontal"
)

horizontal_scrollbar.pack(
    side="bottom",
    fill="x"
)


tree = ttk.Treeview(
    table_frame,
    show="headings",
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)

tree.pack(
    side="left",
    fill="both",
    expand=True
)


vertical_scrollbar.config(
    command=tree.yview
)

horizontal_scrollbar.config(
    command=tree.xview
)


# ============================================================
# ORDER DETAILS - WINDOW
# ============================================================

def show_order_details_window(order_id):

    window = tk.Toplevel(root)
    window.title(f"Order Details - Order #{order_id}")
    window.geometry("600x450")

    tk.Label(
        window,
        text=f"ORDER DETAILS — ORDER #{order_id}",
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    columns = (
        "ORDER_ID",
        "SERVICE_TYPE",
        "SERVICE_ID",
        "QNT"
    )

    details_tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for column in columns:

        details_tree.heading(
            column,
            text=column
        )

        details_tree.column(
            column,
            width=130,
            anchor="center"
        )

    details_tree.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    # --------------------------------------------------------
    # REFRESH ORDER DETAILS
    # --------------------------------------------------------

    def refresh_details():

        for item in details_tree.get_children():
            details_tree.delete(item)

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                ORDER_DETAIL_ID,
                ORDER_ID,
                SERVICE_TYPE,
                SERVICE_ID,
                QNT
            FROM ORDER_DETAILS
            WHERE ORDER_ID = %s
            ORDER BY ORDER_DETAIL_ID
        """

        cursor.execute(
            query,
            (order_id,)
        )

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        for row in rows:

            # row[0] = ORDER_DETAIL_ID
            # row[1] = ORDER_ID
            # row[2] = SERVICE_TYPE
            # row[3] = SERVICE_ID
            # row[4] = QNT

            details_tree.insert(
                "",
                tk.END,
                iid=str(row[0]),
                values=(
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )
            )

    # --------------------------------------------------------
    # ADD SERVICE
    # --------------------------------------------------------

    def add_service():

        add_window = tk.Toplevel(window)
        add_window.title("Add Service")
        add_window.geometry("350x250")

        tk.Label(
            add_window,
            text="SERVICE TYPE"
        ).pack(pady=(15, 5))

        service_type = ttk.Combobox(
            add_window,
            values=("PH", "CP"),
            state="readonly",
            width=20
        )

        service_type.pack()

        tk.Label(
            add_window,
            text="SERVICE ID"
        ).pack(pady=(10, 5))

        service_id = ttk.Combobox(
            add_window,
            width=20,
            state="readonly"
        )

        service_id.pack()

        def load_service_ids(event=None):

            service_type_value = service_type.get()

            if service_type_value == "PH":

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    SELECT SERVICE_ID
                    FROM PHOTOGRAPHY
                    ORDER BY SERVICE_ID
                """)

                rows = cursor.fetchall()

                cursor.close()
                connection.close()

                service_id["values"] = [
                    row[0] for row in rows
                ]

            elif service_type_value == "CP":

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    SELECT SERVICE_ID
                    FROM CUSTOM_PRODUCTS
                    ORDER BY SERVICE_ID
                """)

                rows = cursor.fetchall()

                cursor.close()
                connection.close()

                service_id["values"] = [
                    row[0] for row in rows
                ]

            else:

                service_id["values"] = ()

            service_id.set("")

            service_type.bind(
                "<<ComboboxSelected>>",
                load_service_ids
            )

        tk.Label(
            add_window,
            text="QUANTITY"
        ).pack(pady=(10, 5))

        quantity = tk.Entry(
            add_window,
            width=23
        )

        quantity.pack()

        def save_service():

            service_type_value = service_type.get()
            service_id_value = service_id.get().strip()
            quantity_value = quantity.get().strip()

            if not service_type_value:
                messagebox.showwarning(
                    "Missing Information",
                    "Please select a service type."
                )
                return

            if not service_id_value:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter a service ID."
                )
                return

            try:
                quantity_number = int(quantity_value)

                if quantity_number <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Invalid Quantity",
                    "Quantity must be a positive whole number."
                )
                return

            connection = get_connection()
            cursor = connection.cursor()

            try:

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

                cursor.execute(
                    query,
                    (
                        order_id,
                        service_type_value,
                        service_id_value,
                        quantity_number
                    )
                )

                connection.commit()

                messagebox.showinfo(
                    "Success",
                    "Service added successfully."
                )

                add_window.destroy()

                refresh_details()

            except mysql.connector.Error as error:

                connection.rollback()

                messagebox.showerror(
                    "Error",
                    f"Could not add service.\n\n{error}"
                )

            finally:

                cursor.close()
                connection.close()

        tk.Button(
            add_window,
            text="SAVE SERVICE",
            width=18,
            command=save_service
        ).pack(pady=20)

    # --------------------------------------------------------
    # MODIFY SERVICE
    # --------------------------------------------------------

    def modify_service():

        selected = details_tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Service",
                "Please select a service to modify."
            )
            return

        order_detail_id = selected[0]

        values = details_tree.item(
            selected[0],
            "values"
        )

        current_type = values[1]
        current_service_id = values[2]
        current_quantity = values[3]

        modify_window = tk.Toplevel(window)
        modify_window.title("Modify Service")
        modify_window.geometry("350x250")

        tk.Label(
            modify_window,
            text="SERVICE TYPE"
        ).pack(pady=(15, 5))

        service_type = ttk.Combobox(
            modify_window,
            values=("PH", "CP"),
            state="readonly",
            width=20
        )

        service_type.set(current_type)
        service_type.pack()

        tk.Label(
            modify_window,
            text="SERVICE ID"
        ).pack(pady=(10, 5))

        service_id = tk.Entry(
            modify_window,
            width=23
        )

        service_id.insert(0, current_service_id)
        service_id.pack()

        tk.Label(
            modify_window,
            text="QUANTITY"
        ).pack(pady=(10, 5))

        quantity = tk.Entry(
            modify_window,
            width=23
        )

        quantity.insert(0, current_quantity)
        quantity.pack()

        def save_changes():

            service_type_value = service_type.get()
            service_id_value = service_id.get().split(" - ")[0]
            quantity_value = quantity.get().strip()

            if not service_type_value:
                messagebox.showwarning(
                    "Missing Information",
                    "Please select a service type."
                )
                return

            if not service_id_value:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter a service ID."
                )
                return

            try:
                quantity_number = int(quantity_value)

                if quantity_number <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Invalid Quantity",
                    "Quantity must be a positive whole number."
                )
                return

            connection = get_connection()
            cursor = connection.cursor()

            try:

                query = """
                    UPDATE ORDER_DETAILS
                    SET
                        SERVICE_TYPE = %s,
                        SERVICE_ID = %s,
                        QNT = %s
                    WHERE ORDER_DETAIL_ID = %s
                """

                cursor.execute(
                    query,
                    (
                        service_type_value,
                        service_id_value,
                        quantity_number,
                        order_detail_id
                    )
                )

                connection.commit()

                messagebox.showinfo(
                    "Success",
                    "Service modified successfully."
                )

                modify_window.destroy()

                refresh_details()

            except mysql.connector.Error as error:

                connection.rollback()

                messagebox.showerror(
                    "Error",
                    f"Could not modify service.\n\n{error}"
                )

            finally:

                cursor.close()
                connection.close()

        tk.Button(
            modify_window,
            text="SAVE CHANGES",
            width=18,
            command=save_changes
        ).pack(pady=20)

    # --------------------------------------------------------
    # DELETE SERVICE
    # --------------------------------------------------------

    def delete_service():

        selected = details_tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Service",
                "Please select a service to delete."
            )
            return

        order_detail_id = selected[0]

        values = details_tree.item(
            selected[0],
            "values"
        )

        service_id_value = values[2]

        confirm = messagebox.askyesno(
            "Delete Service",
            f"Delete service '{service_id_value}' from Order #{order_id}?"
        )

        if not confirm:
            return

        connection = get_connection()
        cursor = connection.cursor()

        try:

            query = """
                DELETE FROM ORDER_DETAILS
                WHERE ORDER_DETAIL_ID = %s
            """

            cursor.execute(
                query,
                (order_detail_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Service deleted successfully."
            )

            refresh_details()

        except mysql.connector.Error as error:

            connection.rollback()

            messagebox.showerror(
                "Error",
                f"Could not delete service.\n\n{error}"
            )

        finally:

            cursor.close()
            connection.close()

    # --------------------------------------------------------
    # BUTTONS
    # --------------------------------------------------------

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="+ ADD SERVICE",
        width=15,
        command=add_service
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="MODIFY SERVICE",
        width=15,
        command=modify_service
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="DELETE SERVICE",
        width=15,
        command=delete_service
    ).grid(row=0, column=2, padx=5)

    # --------------------------------------------------------
    # LOAD DETAILS
    # --------------------------------------------------------

    refresh_details()

    
# ============================================================
# ORDER - DOUBLE CLICK
# ============================================================

def order_double_click(event):

    # Only work when viewing ORDERS
    if current_table != "ORDERS":
        return

    selected = tree.selection()

    if not selected:
        return

    values = tree.item(selected[0], "values")

    order_id = values[0]

    show_order_details_window(order_id)

# ============================================================
# DOUBLE CLICK ORDER
# ============================================================

tree.bind("<Double-1>", order_double_click)

# ============================================================
# START
# ============================================================

show_customers()

root.mainloop()
