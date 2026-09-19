from customers import customers_menu
from orders import orders_menu
from services import services_menu

# MAIN MENU
def main_menu():

    while True:

        print("\n" + "=" * 40)
        print("          SWEET PIXELS STUDIO")
        print("=" * 40)

        print("\n1. Customers")
        print("2. Orders")
        print("3. Services")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            customers_menu()

        elif choice == "2":
            orders_menu()

        elif choice == "3":
            services_menu()

        elif choice == "4":
            print("\nThank you for using Sweet Pixels Studio!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
