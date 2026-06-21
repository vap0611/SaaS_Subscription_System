import streamlit as st
import pandas as pd
import sqlite3
import os
import time 

from plans import add_plan, view_plans, update_plan
from customers import add_customer, view_customers, update_customer
from subscriptions import assign_subscription, view_subscriptions, update_subscription, cancel_subscription, renew_subscription
from payments import add_payment, view_payments, update_payment, generate_invoice

st.set_page_config(page_title="SaaS Subscription System", page_icon="🏢", layout="wide")

DB_PATH =  "database/saas.db"

def get_dataframe(query):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None

def login_page():
    st.markdown("<h1 style='text-align: center;'>SaaS Subscription System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>Webvanta Innovations</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_btn = st.form_submit_button("Login", use_container_width=True)

            if submit_btn:
                if username == "admin123" and password == "admin@123":
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = 'Admin'
                    st.rerun()
                elif username == "staff123" and password == "staff@123":
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = 'Staff'
                    st.rerun()
                else:
                    st.error("Invalid Username or Password!")

def main_app():
    st.sidebar.title(f"👤 Role: {st.session_state['role']}")
    st.sidebar.markdown("---")
    
    if st.session_state['role'] == 'Admin':
        menu = ["Dashboard", "Plans", "Customers", "Subscriptions", "Payments", "Reports"]
    else:
        menu = ["Dashboard", "Customers", "Subscriptions", "Payments", "Reports"]
        
    choice = st.sidebar.radio("Navigate", menu)
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state['logged_in'] = False
        st.session_state['role'] = None
        st.rerun()

    st.title(f"{choice} Module")
    st.markdown("---")

    if choice == "Dashboard":
        col1, col2, col3 = st.columns(3)
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM customers")
            tot_cust = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM subscriptions WHERE status='Active'")
            act_sub = cur.fetchone()[0]
            cur.execute("SELECT SUM(amount) FROM payments WHERE payment_status='Paid'")
            rev = cur.fetchone()[0] or 0
            conn.close()
            
            col1.metric("Total Customers", tot_cust)
            col2.metric("Active Subscriptions", act_sub)
            col3.metric("Total Revenue", f"₹ {rev}")
        except Exception:
            st.warning("Database not fully setup yet.")


    elif choice == "Plans":
        tab1, tab2, tab3 = st.tabs(["📋 View Plans", "➕ Add Plan", "✏️ Update Plan"])
        with tab1:
            df = get_dataframe("SELECT * FROM plans")
            if not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
            else: st.info("No plans available.")
            
        with tab2:
            with st.form("add_plan"):
                name = st.text_input("Plan Name")
                price = st.number_input("Price (₹)", min_value=0.0)
                duration = st.number_input("Duration (Days)", min_value=1)
                features = st.text_area("Features")
                status = st.selectbox("Status", ["Active", "Inactive"])
                if st.form_submit_button("Add Plan"):
                    success, msg = add_plan(name, price, duration, features, status)
                    if success: 
                        st.success(msg)
                        time.sleep(1)
                        st.rerun()
                    else: st.error(msg)
                    
        with tab3:
            plan_df = get_dataframe("SELECT plan_id, plan_name FROM plans")
            if not plan_df.empty:
                plan_dict = dict(zip(plan_df.plan_name, plan_df.plan_id))
                sel_plan = st.selectbox("Select Plan to Update", plan_dict.keys())
                
                choice_map = {"Name": 1, "Price": 2, "Duration": 3, "Features": 4, "Status": 5}
                update_field = st.selectbox("What to update?", list(choice_map.keys()))
                new_val = st.text_input(f"Enter New {update_field}")
                
                if st.button("Update Plan"):
                    success, msg = update_plan(plan_dict[sel_plan], choice_map[update_field], new_val)
                    if success: 
                        st.success(msg)
                        time.sleep(1)
                        st.rerun()
                    else: st.error(msg)

    elif choice == "Customers":
        tab1, tab2, tab3 = st.tabs(["📋 View Customers", "➕ Add Customer", "✏️ Update Customer"])
        with tab1:
            df = get_dataframe("SELECT * FROM customers")
            if not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
            else: st.info("No customers found.")
            
        with tab2:
            with st.form("add_cust"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone (10 Digits)")
                company = st.text_input("Company Name")
                if st.form_submit_button("Add Customer"):
                    success, msg = add_customer(name, email, phone, company)
                    if success: 
                        st.success(msg)
                        time.sleep(1)
                        st.rerun()
                    else: st.error(msg)
                    
        with tab3:
            cust_df = get_dataframe("SELECT customer_id, name FROM customers")
            if not cust_df.empty:
                cust_dict = dict(zip(cust_df.name, cust_df.customer_id))
                sel_cust = st.selectbox("Select Customer", cust_dict.keys())
                
                choice_map = {"Name": 1, "Email": 2, "Phone": 3, "Company": 4}
                update_field = st.selectbox("What to update?", list(choice_map.keys()))
                new_val = st.text_input(f"Enter New {update_field}")
                
                if st.button("Update Customer"):
                    success, msg = update_customer(cust_dict[sel_cust], choice_map[update_field], new_val)
                    if success: 
                        st.success(msg)
                        time.sleep(1)
                        st.rerun()
                    else: st.error(msg)

    
    elif choice == "Subscriptions":
        tab1, tab2, tab3 = st.tabs(["📋 View Subscriptions", "➕ Assign New", "⚙️ Manage & Update"])
        with tab1:
            df = get_dataframe("""
                SELECT s.subscription_id, c.name, p.plan_name, s.start_date, s.expiry_date, s.status 
                FROM subscriptions s 
                JOIN customers c ON s.customer_id = c.customer_id 
                JOIN plans p ON s.plan_id = p.plan_id
            """)
            if not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
            else: st.info("No subscriptions found.")
            
        with tab2:
            cust_df = get_dataframe("SELECT customer_id, name FROM customers")
            plan_df = get_dataframe("SELECT plan_id, plan_name FROM plans WHERE status='Active'")
            
            with st.form("assign_sub"):
                if not cust_df.empty and not plan_df.empty:
                    cust_dict = dict(zip(cust_df.name, cust_df.customer_id))
                    plan_dict = dict(zip(plan_df.plan_name, plan_df.plan_id))
                    
                    sel_cust = st.selectbox("Select Customer", cust_dict.keys())
                    sel_plan = st.selectbox("Select Plan", plan_dict.keys())
                    
                    if st.form_submit_button("Assign Subscription"):
                        success, msg = assign_subscription(cust_dict[sel_cust], plan_dict[sel_plan])
                        if success: 
                            st.success(msg)
                            time.sleep(1)
                            st.rerun()
                        else: st.error(msg)
                else:
                    st.warning("Please add Customers and Active Plans first.")
                    
        with tab3:
            sub_df = get_dataframe("SELECT subscription_id FROM subscriptions")
            if not sub_df.empty:
                sub_id = st.selectbox("Select Subscription ID", sub_df['subscription_id'])
                action = st.radio("Choose Action", ["Update Detail", "Renew Subscription", "Cancel Subscription"])
                
                if action == "Update Detail":
                    choice_map = {"Plan ID": 1, "Status": 2}
                    update_field = st.selectbox("Update Field", list(choice_map.keys()))
                    new_val = st.text_input(f"Enter New {update_field}")
                    if st.button("Update"):
                        success, msg = update_subscription(sub_id, choice_map[update_field], new_val)
                        if success: 
                            st.success(msg)
                            time.sleep(1)
                            st.rerun()
                        else: st.error(msg)
                        
                elif action == "Renew Subscription":
                    st.info("This will calculate the new expiry date based on the plan duration.")
                    if st.button("Renew Now"):
                        success, msg = renew_subscription(sub_id)
                        if success: 
                            st.success(msg)
                            time.sleep(1)
                            st.rerun()
                        else: st.error(msg)
                        
                elif action == "Cancel Subscription":
                    st.warning("This will immediately mark the subscription as Cancelled.")
                    if st.button("Cancel Sub"):
                        success, msg = cancel_subscription(sub_id)
                        if success: 
                            st.success(msg)
                            time.sleep(1)
                            st.rerun()
                        else: st.error(msg)


    elif choice == "Payments":
        tab1, tab2, tab3, tab4 = st.tabs(["📋 View Payments", "➕ Add Payment", "✏️ Update Payment", "📄 Generate Invoice"])
        with tab1:
            df = get_dataframe("""
                SELECT pay.payment_id, pay.invoice_no, c.name, pay.amount, pay.payment_date, pay.payment_status 
                FROM payments pay 
                JOIN subscriptions s ON pay.subscription_id = s.subscription_id 
                JOIN customers c ON s.customer_id = c.customer_id
            """)
            if not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
            else: st.info("No payments recorded.")
            
        with tab2:
            sub_df = get_dataframe("SELECT subscription_id FROM subscriptions")
            with st.form("add_pay"):
                if not sub_df.empty:
                    sub_id = st.selectbox("Select Subscription ID", sub_df['subscription_id'])
                    amount = st.number_input("Amount (₹)", min_value=1.0)
                    status = st.selectbox("Payment Status", ["Paid", "Pending", "Failed"])
                    
                    if st.form_submit_button("Record Payment"):
                        success, msg = add_payment(sub_id, amount, status)
                        if success: 
                            st.success(msg)
                            time.sleep(1)
                            st.rerun()
                        else: st.error(msg)
                else:
                    st.warning("No active subscriptions found.")
                    
        with tab3:
            pay_df = get_dataframe("SELECT payment_id FROM payments")
            if not pay_df.empty:
                pay_id = st.selectbox("Select Payment ID to Update", pay_df['payment_id'])
                choice_map = {"Amount": 1, "Status": 2}
                update_field = st.selectbox("What to update?", list(choice_map.keys()))
                new_val = st.text_input(f"Enter New {update_field}")
                
                if st.button("Update Payment"):
                    success, msg = update_payment(pay_id, choice_map[update_field], new_val)
                    if success: 
                        st.success(msg)
                        time.sleep(1)
                        st.rerun()
                    else: st.error(msg)
                    
        with tab4:
            st.write("Generate and download PDF invoice for any recorded payment.")
            pay_df = get_dataframe("SELECT payment_id, invoice_no FROM payments WHERE payment_status='Paid'")
            if not pay_df.empty:
                pay_dict = dict(zip(pay_df.invoice_no, pay_df.payment_id))
                sel_inv = st.selectbox("Select Invoice Number", pay_dict.keys())
                
                if st.button("Generate PDF"):
                    success, result = generate_invoice(pay_dict[sel_inv])
                    if success:
                        st.success("Invoice generated successfully!")
                        with open(result, "rb") as pdf_file:
                            st.download_button(
                                label="⬇️ Download Invoice PDF",
                                data=pdf_file,
                                file_name=f"{sel_inv}.pdf",
                                mime="application/pdf"
                            )
                    else:
                        st.error(result)
            else:
                st.info("No successful payments found to generate invoices.")
    # ==============================
    # REPORTS EXPORT MODULE
    # ==============================
    elif choice == "Reports":
        st.subheader("📊 Data & Revenue Reports")
        st.write("Generate and export system reports in CSV format.")
        
        report_type = st.selectbox("Select Report Type", ["Customers Report", "Subscriptions Report", "Payments & Revenue Report"])
        
        if report_type == "Customers Report":
            df = get_dataframe("SELECT * FROM customers")
            file_name = "customers_report.csv"
            
        elif report_type == "Subscriptions Report":
            df = get_dataframe("""
                SELECT s.subscription_id, c.name as Customer, p.plan_name as Plan, 
                       s.start_date, s.expiry_date, s.status 
                FROM subscriptions s 
                JOIN customers c ON s.customer_id = c.customer_id 
                JOIN plans p ON s.plan_id = p.plan_id
            """)
            file_name = "subscriptions_report.csv"
            
        elif report_type == "Payments & Revenue Report":
            df = get_dataframe("""
                SELECT pay.payment_id, pay.invoice_no, c.name as Customer, 
                       pay.amount, pay.payment_date, pay.payment_status 
                FROM payments pay 
                JOIN subscriptions s ON pay.subscription_id = s.subscription_id 
                JOIN customers c ON s.customer_id = c.customer_id
            """)
            file_name = "payments_revenue_report.csv"

        # Show Table and Download Button
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Convert DataFrame to CSV
            csv = df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label=f"⬇️ Download {report_type} (CSV)",
                data=csv,
                file_name=file_name,
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No data available to export for this report.")

if not st.session_state['logged_in']:
    login_page()
else:
    main_app()