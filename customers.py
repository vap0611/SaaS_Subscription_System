from database.database import connection
import re

def add_customer(name, email, phone, company):
    try:
        # Validations
        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(email_pattern, email):
            return False, "Invalid Email Format!"
            
        if not str(phone).isdigit() or len(str(phone)) != 10:
            return False, "Invalid phone number! It must be exactly 10 digits."

        conn = connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO customers (name, email, phone, company, registration_date) VALUES (?, ?, ?, ?, DATE('now'))",
            (name, email, phone, company)
        )
        
        conn.commit()
        conn.close()
        return True, "Customer added successfully!!"
        
    except Exception as e:
        return False, f"Error adding customer: {e}"


def view_customers():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        
        conn.close()
        return True, customers
    except Exception as e:
        return False, f"Error fetching customers: {e}"


def update_customer(customer_id, choice, new_value):
    try:
        conn = connection()
        cursor = conn.cursor()
        
        if choice == 1:
            cursor.execute("UPDATE customers SET name = ? WHERE customer_id = ?", (new_value, customer_id))
            
        elif choice == 2:
            email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
            if not re.match(email_pattern, new_value):
                conn.close()
                return False, "Invalid Email Format! Cannot be updated."
            cursor.execute("UPDATE customers SET email = ? WHERE customer_id = ?", (new_value, customer_id))
            
        elif choice == 3:
            if not str(new_value).isdigit() or len(str(new_value)) != 10:
                conn.close()
                return False, "Invalid phone number! Must be 10 digits."
            cursor.execute("UPDATE customers SET phone = ? WHERE customer_id = ?", (new_value, customer_id))
            
        elif choice == 4:
            cursor.execute("UPDATE customers SET company = ? WHERE customer_id = ?", (new_value, customer_id))
            
        else:
            conn.close()
            return False, "Invalid Choice!"

        conn.commit()
        conn.close()
        return True, "Customer Updated Successfully!!"
        
    except Exception as e:
        return False, f"Error updating customer: {e}"


def delete_customer(customer_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
        
        conn.commit()
        conn.close()
        return True, "Customer Deleted Successfully!!"
        
    except Exception as e:
        return False, f"Error deleting customer: {e}"