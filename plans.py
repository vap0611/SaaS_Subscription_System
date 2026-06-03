from database.database import connection

def add_plan():
    conn = connection()
    cursor = conn.cursor()

    name = input("Enter plan name: ")
    price = float(input("Enter price of the plan: "))
    duration = int(input("Enter duration: "))
    features = input('Enter Features: ')
    status = input("Enter current status of the price(Active/Inactive): ")
    cursor.execute("Insert into plans (plan_name, price, duration, features, status) values (?, ?, ?, ?, ?)",(name, price, duration ,features, status))

    conn.commit()
    conn.close()

    print("Plan added successfully !!")


def view_plans():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("Select * from plans")
    plans=cursor.fetchall()
    for plan in plans:
        print(plan)
    conn.commit()
    conn.close()
    print("That's it ")

def update_plans():
    conn = connection()
    cursor = conn.cursor()
    id = int(input("Enter plan_id to be updated"))
    #print("What do you want to update ??")
    ch = int(input("Enter your choice: \n 1. Name\n"
                   "2. Price\n"
                   "3. Duration\n"
                   "4. Features\n"
                   "5. Status\n"))
    if ch == 1:
        new_name = input("Enter new name")
        cursor.execute("Update plans set plan_name = ? where plan_id = ?",(new_name, id))
    if ch == 2:
        new_price = int(input("Enter new price"))
        if new_price < 0:
            print("Price name cannot be updated as it was negative  !!")
        else:
            cursor.execute("Update plans set price = ? where plan_id = ?",(new_price, id))
    if ch == 3:
        new_duration = input("Enter updated duration of plan")
        cursor.execute("Update plans set duration = ? where plan_id = ?",(new_duration, id))
    if ch == 4:
        new_features = input("Enter updated features of plan")
        cursor.execute("Update plans set features = ? where plan_id = ?",(new_features, id))
    if ch == 5:
        new_status = input("Enter updated status of plan")
        cursor.execute("Update plans set  status= ? where plan_id = ?",(new_status, id))    

    conn.commit()
    conn.close()

    print("Updated Successfully !!")
    


def delete_plan():
    conn = connection()
    cursor = conn.cursor()

    id = int(input("Enter the plan ID to be deleted"))
    ch = input("Are you sure you want to delete ? Confirm with (Y/n)")
    if ch == 'Y':
        cursor.execute("Delete from plans where plan_id = ?",(id,))
    elif ch == 'n':
        print("Deletion Aborted")
    
    conn.commit()
    conn.close()
    print("Operation Successful")