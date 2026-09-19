# GET DATA FROM MYSQL
from database import get_connection



# SERVICE CLASSES - In this section, I have asked AI to help me
# build the codes for classes and not get any errors during the process
class Service:
    """
    Base class for services offered by Sweet Pixels Studio.
    """

    def __init__(self, service_id, name, category, base_price):
        self.service_id = service_id
        self.name = name
        self.category = category
        self.base_price = base_price

    def display_basic_info(self):
        print(
            f"{self.service_id} | "
            f"{self.category} | "
            f"{self.name} | "
            f"${self.base_price}"
        )


class Photography(Service):
    """Represents a photography service.
    Inherits basic service information from Service.
    """

    def __init__(
        self,
        service_id,
        name,
        category,
        description,
        min_hours,
        max_hours,
        min_photo,
        max_photo,
        base_price,
        add_on
    ):

        super().__init__(
            service_id,
            name,
            category,
            base_price
        )

        self.description = description
        self.min_hours = min_hours
        self.max_hours = max_hours
        self.min_photo = min_photo
        self.max_photo = max_photo
        self.add_on = add_on

    def display(self):
        print(
            f"{self.service_id} | "
            f"{self.category} | "
            f"{self.name} | "
            f"${self.base_price}"
        )


class CustomProduct(Service):
    """
    Represents a custom product.
    Inherits basic service information from Service.
    """

    def __init__(
        self,
        service_id,
        name,
        category,
        description,
        base_price
    ):

        super().__init__(
            service_id,
            name,
            category,
            base_price
        )

        self.description = description

    def display(self):
        print(
            f"{self.service_id} | "
            f"{self.category} | "
            f"{self.name} | "
            f"{self.description} | "
            f"${self.base_price}"
        )





# VIEW SERVICES
def view_photography():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
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
            ADD_ON
        FROM PHOTOGRAPHY
        ORDER BY SERVICE_NUMBER
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    print("\n" + "=" * 90)
    print("PHOTOGRAPHY")
    print("=" * 90)

    for row in rows:

        photography = Photography(
            service_id=row[1],
            name=row[3],
            category=row[2],
            description=row[4],
            min_hours=row[5],
            max_hours=row[6],
            min_photo=row[7],
            max_photo=row[8],
            base_price=row[9],
            add_on=row[10]
        )

        photography.display()

    cursor.close()
    connection.close()





# VIEW CUSTOM PRODUCTS
def view_custom_products():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            SERVICE_NUMBER,
            SERVICE_ID,
            CATEGORY,
            NAME,
            DESCRIPTION,
            BASE_PRICE
        FROM CUSTOM_PRODUCTS
        ORDER BY SERVICE_NUMBER
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    print("\n" + "=" * 80)
    print("CUSTOM PRODUCTS")
    print("=" * 80)

    for row in rows:

        custom_product = CustomProduct(
            service_id=row[1],
            name=row[3],
            category=row[2],
            description=row[4],
            base_price=row[5]
        )

        custom_product.display()

    cursor.close()
    connection.close()





# PHOTOGRAPHY MENU
def photography_menu():

    while True:

        print("\n--- PHOTOGRAPHY ---")

        print("1. View")
        print("2. Create")
        print("3. Modify")
        print("4. Delete")
        print("5. Back to Services")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_photography()

        elif choice == "2":
            print("\nSorry, CREATE option is not yet available. Coming soon.")

        elif choice == "3":
            print("\nSorry, MODIFY option is not yet available. Coming soon.")

        elif choice == "4":
            print("\nSorry, DELETE option is not yet available. Coming soon.")

        elif choice == "5":
            break

        else:
            print("\nInvalid choice.")





# CUSTOM PRODUCTS MENU
def custom_products_menu():

    while True:

        print("\n--- CUSTOM PRODUCTS ---")

        print("1. View")
        print("2. Create")
        print("3. Modify")
        print("4. Delete")
        print("5. Back to Services")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_custom_products()

        elif choice == "2":
            print("\nSorry, CREATE option is not yet available. Coming soon.")

        elif choice == "3":
            print("\nSorry, MODIFY option is not yet available. Coming soon.")

        elif choice == "4":
            print("\nSorry, DELETE option is not yet available. Coming soon.")

        elif choice == "5":
            break

        else:
            print("\nInvalid choice.")





# SERVICES MENU
def services_menu():

    while True:

        print("\n" + "=" * 40)
        print("SERVICES")
        print("=" * 40)

        print("1. Photography")
        print("2. Custom Products")
        print("3. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            photography_menu()

        elif choice == "2":
            custom_products_menu()

        elif choice == "3":
            break

        else:
            print("\nInvalid choice.")
