from database.database import connection
from datetime import datetime, timedelta

def assign_subscription(customer_id, plan_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        # Fetch Plan Duration
        cursor.execute(
            "SELECT duration FROM plans WHERE plan_id = ?",
            (plan_id,)
        )
        duration_data = cursor.fetchone()

        if duration_data is None:
            conn.close()
            return False, "Invalid Plan ID!"

        duration = duration_data[0]

        # Calculate Dates
        start_date = datetime.today()
        expiry_date = start_date + timedelta(days=duration)

        start_date_str = start_date.strftime("%Y-%m-%d")
        expiry_date_str = expiry_date.strftime("%Y-%m-%d")

        status = "Active"

        # Insert Subscription
        cursor.execute(
            """
            INSERT INTO subscriptions
            (customer_id, plan_id, start_date, expiry_date, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (customer_id, plan_id, start_date_str, expiry_date_str, status)
        )

        conn.commit()
        conn.close()
        return True, "Subscription Assigned Successfully!"

    except Exception as e:
        return False, f"Error assigning subscription: {e}"


def view_subscriptions():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM subscriptions")
        subs = cursor.fetchall()
        
        conn.close()
        return True, subs
    except Exception as e:
        return False, f"Error fetching subscriptions: {e}"


def update_subscription(subscription_id, choice, new_value):
    try:
        conn = connection()
        cursor = conn.cursor()

        if choice == 1:
            # Update Plan
            cursor.execute(
                "UPDATE subscriptions SET plan_id = ? WHERE subscription_id = ?",
                (int(new_value), subscription_id)
            )
            message = "Plan Updated Successfully!"
            
        elif choice == 2:
            # Update Status
            cursor.execute(
                "UPDATE subscriptions SET status = ? WHERE subscription_id = ?",
                (new_value, subscription_id)
            )
            message = "Status Updated Successfully!"
            
        else:
            conn.close()
            return False, "Invalid Choice"

        conn.commit()
        conn.close()
        return True, message

    except Exception as e:
        return False, f"Error updating subscription: {e}"


def cancel_subscription(subscription_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE subscriptions
            SET status = 'Cancelled'
            WHERE subscription_id = ?
            """,
            (subscription_id,)
        )

        conn.commit()
        conn.close()
        return True, "Subscription Cancelled Successfully!"

    except Exception as e:
        return False, f"Error cancelling subscription: {e}"


def check_expired_subscriptions():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE subscriptions
            SET status = 'Expired'
            WHERE expiry_date < DATE('now')
            AND status != 'Cancelled'
            """
        )

        conn.commit()
        conn.close()
        return True, "Expired subscriptions updated successfully!"

    except Exception as e:
        return False, f"Error updating expired subscriptions: {e}"


def renew_subscription(subscription_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT s.expiry_date, p.duration
            FROM subscriptions s
            JOIN plans p
            ON s.plan_id = p.plan_id
            WHERE s.subscription_id = ?
            """,
            (subscription_id,)
        )

        data = cursor.fetchone()

        if data is None:
            conn.close()
            return False, "Subscription not found!"

        expiry_date = datetime.strptime(data[0], "%Y-%m-%d")
        duration = data[1]

        new_expiry = expiry_date + timedelta(days=duration)
        new_expiry_str = new_expiry.strftime("%Y-%m-%d")

        cursor.execute(
            """
            UPDATE subscriptions
            SET expiry_date = ?,
                status = 'Active'
            WHERE subscription_id = ?
            """,
            (new_expiry_str, subscription_id)
        )

        conn.commit()
        conn.close()
        return True, "Subscription Renewed Successfully!"

    except Exception as e:
        return False, f"Error renewing subscription: {e}"