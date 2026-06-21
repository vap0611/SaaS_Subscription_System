from database.database import connection

def add_plan(name, price, duration, features, status):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO plans (plan_name, price, duration, features, status) VALUES (?, ?, ?, ?, ?)",
            (name, float(price), int(duration), features, status)
        )

        conn.commit()
        conn.close()
        return True, "Plan added successfully!!"
    except Exception as e:
        return False, f"Error adding plan: {e}"

def view_plans():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM plans")
        plans = cursor.fetchall()
        
        conn.close()
        return True, plans  # Returning the fetched data to show in Streamlit dataframe
    except Exception as e:
        return False, f"Error fetching plans: {e}"

def update_plan(plan_id, choice, new_value):
    try:
        conn = connection()
        cursor = conn.cursor()
        
        if choice == 1:
            cursor.execute("UPDATE plans SET plan_name = ? WHERE plan_id = ?", (new_value, plan_id))
        elif choice == 2:
            new_price = float(new_value)
            if new_price < 0:
                conn.close()
                return False, "Price cannot be updated as it was negative!!"
            cursor.execute("UPDATE plans SET price = ? WHERE plan_id = ?", (new_price, plan_id))
        elif choice == 3:
            cursor.execute("UPDATE plans SET duration = ? WHERE plan_id = ?", (int(new_value), plan_id))
        elif choice == 4:
            cursor.execute("UPDATE plans SET features = ? WHERE plan_id = ?", (new_value, plan_id))
        elif choice == 5:
            cursor.execute("UPDATE plans SET status = ? WHERE plan_id = ?", (new_value, plan_id))

        conn.commit()
        conn.close()
        return True, "Plan Updated Successfully!!"
    except Exception as e:
        return False, f"Error updating plan: {e}"

def delete_plan(plan_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM plans WHERE plan_id = ?", (plan_id,))
        
        conn.commit()
        conn.close()
        return True, "Plan Deleted Successfully!!"
    except Exception as e:
        return False, f"Error deleting plan: {e}"