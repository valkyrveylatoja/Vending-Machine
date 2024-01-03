import sqlite3
     
   
def show_category_table(category):
    conn = sqlite3.connect('vending_machine.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM {category}")
        products = cursor.fetchall()
        print(f"\nProducts in the '{category}' category:")
        print("ID | Name               | Price | Stock")
        print("--------------------------------------")
        for product in products:
            print(f"{product[0]:2d} | {product[1]:<18} | ${product[2]:.2f} | {product[3]:2d}")

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        conn.close()

def make_transaction(product_id, category, amount_paid):
    conn = sqlite3.connect('vending_machine.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM {category} WHERE id = ?", (product_id,))
        product = cursor.fetchone()

        if product:
            if product[3] > 0:
                change = amount_paid - product[2]
                if change >= 0:
                    cursor.execute("INSERT INTO transactions (product_id, category, amount_paid, change) VALUES (?, ?, ?, ?)",
                                   (product_id, category, amount_paid, change))
                    cursor.execute(f"UPDATE {category} SET stock = stock - 1 WHERE id = ?", (product_id,))
                    print("\nTransaction successful!")
                    print(f"Item: {product[1]}, Price: ${product[2]:.2f}, Change: ${change:.2f}")
                else:
                    print("Insufficient funds. Transaction canceled.")
            else:
                print("Out of stock. Transaction canceled.")
        else:
            print("Invalid product ID. Transaction canceled.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        conn.commit()
        conn.close()

def show_transactions():
    conn = sqlite3.connect('vending_machine.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.id, p.name, t.category, t.date_time, t.amount_paid, t.change
            FROM transactions t
            JOIN sweets p ON t.product_id = p.id AND t.category = 'sweets'
            UNION
            SELECT t.id, p.name, t.category, t.date_time, t.amount_paid, t.change
            FROM transactions t
            JOIN healthy p ON t.product_id = p.id AND t.category = 'healthy'
            UNION
            SELECT t.id, p.name, t.category, t.date_time, t.amount_paid, t.change
            FROM transactions t
            JOIN snacks p ON t.product_id = p.id AND t.category = 'snacks'
        """)
        transactions = cursor.fetchall()
        print("\nAll Transactions:")
        print("ID | Product Name        | Category | Date Time               | Amount Paid | Change")
        print("---------------------------------------------------------------------------------")
        for transaction in transactions:
            print(f"{transaction[0]:2d} | {transaction[1]:<20} | {transaction[2]:<8} | {transaction[3]} | ${transaction[4]:.2f} | ${transaction[5]:.2f}")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        
while True:
    print("\nSelect a category:")
    print("1. Sweets")
    print("2. Healthy")
    print("3. Snacks")
    print("4. Purchase Log")
    print("0. Exit")
    choice = input("Enter your choice (0-4): ")
    if choice == '0':
        print("Exiting the program. Goodbye!")
        break
    elif choice in ('1', '2', '3'):
        categories = ['sweets', 'healthy', 'snacks']
        selected_category = categories[int(choice) - 1]
        show_category_table(selected_category)
        try:
            product_id = int(input("Enter the ID of the product you want to purchase: "))
            amount_paid = float(input("Enter the amount of money you are inserting: "))
            make_transaction(product_id, selected_category, amount_paid)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    elif choice=="4":
        show_transactions()
        
    else:
        print("Invalid choice. Please enter a number between 0 and .")
