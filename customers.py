from database.database import connection
import re 

def add_customer():
    conn = connection()
    cursor = conn.cursor()
    name = input("Enter customer name")
    email = input("Enter E-mail")  
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.match(pattern, email):
        print("Invalid Email Format!")
        return
    phone = input("Enter phone number")
    if not phone.isdigit() or len(phone) != 10:
            print("Invalid phone number ") 
            return 
    company = input("Enter name of the company")
    cursor.execute("INSERT INTO customers (name, email, phone, company, registration_date) VALUES (?, ?, ?, ?, DATE('now'))",(name, email, phone, company))
    conn.commit()
    conn.close()




def view_customers():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("Select * from customers")
    customers=cursor.fetchall()
    for customer in customers:
        print(customer)
    conn.commit()
    conn.close()
    print("That's it ")

def update_customers():
    conn = connection()
    cursor = conn.cursor()
    id = int(input("Enter plan_id to be updated"))
    #print("What do you want to update ??")
    ch = int(input("Enter your choice: \n 1. Name\n"
                   "2. Email\n"
                   "3. Phone\n"
                   "4. Company\n"))
    if ch == 1:
        new_name = input("Enter new name")
        cursor.execute("Update customers set name = ? where customer_id = ?",(new_name, id))
    if ch == 2:
        new_email = int(input("Enter new email"))
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, new_email):
            print("Invalid Email Format! cannot be updates")
            return
        else:
            cursor.execute("Update cutomers set email = ? where customer_id = ?",(new_email, id))
    if ch == 3:
        new_phone = input("Enter updated phone number")
        if not new_phone.isdigit() or len(new_phone) != 10:
            print("Invalid phone number ") 
            return 
        else:
            cursor.execute("Update customers set phone = ? where customer_id = ?",(new_phone, id))
    if ch == 4:
        new_company = input("Enter updated features of plan")
        cursor.execute("Update customers set company = ? where customer_id = ?",(new_company, id))    

    conn.commit()
    conn.close()

    print("Updated Successfully !!")

def delete_customer():
    conn = connection()
    cursor = conn.cursor()

    id = int(input("Enter the customer ID to be deleted"))
    ch = input("Are you sure you want to delete ? Confirm with (Y/n)")
    if ch == 'Y':
        cursor.execute("Delete from customers where customer_id = ?",(id,))
    elif ch == 'n':
        print("Deletion Aborted")
    
    conn.commit()
    conn.close()
    print("Operation Successful")