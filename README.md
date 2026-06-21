# 🚀 SaaS Subscription Management System

A complete SaaS Subscription Management System developed using **Python, SQLite, Streamlit, Pandas, and ReportLab**. The system helps organizations manage subscription plans, customers, subscriptions, payments, invoices, and reports through an interactive web dashboard.

---

# 📌 Project Overview

This project was developed as part of the internship assignment to automate subscription management processes.

The system allows administrators and staff members to:

* Manage subscription plans
* Manage customer records
* Assign plans to customers
* Track active, expired, cancelled, and renewed subscriptions
* Record customer payments
* Generate professional PDF invoices
* View business reports and analytics
* Export reports in CSV format
* Access the system through role-based authentication

---

# 🛠️ Technologies Used

| Technology   | Purpose                     |
| ------------ | --------------------------- |
| Python       | Backend Logic               |
| SQLite       | Database Management         |
| Streamlit    | Frontend Dashboard          |
| Pandas       | Data Processing & Reporting |
| ReportLab    | PDF Invoice Generation      |
| Git & GitHub | Version Control             |

---

# 📂 Project Structure

```text
SaaS_Subscription_System
│
├── app.py
├── database.py
├── plans.py
├── customers.py
├── subscriptions.py
├── payments.py
├── reports.py
│
├── database/
│   └── saas.db
│
├── invoices/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---
# 🔐 User Roles

## 👨‍💼 Admin

Admin has access to:

* Dashboard
* Plans Module
* Customers Module
* Subscriptions Module
* Payments Module
* Reports Module

### Admin Credentials

```text
Username: admin123
Password: admin@123
```

---
## 👨‍💻 Staff

Staff can access:

* Dashboard
* Customers Module
* Subscriptions Module
* Payments Module

### Staff Credentials

```text
Username: staff123
Password: staff@123
```

---
# 📦 Database Modules

## 1️⃣ Plans Module

This module manages subscription plans.

### Features

* Add New Plan
* View Plans
* Update Existing Plans
* Activate / Deactivate Plans

### Plan Information

* Plan ID
* Plan Name
* Price
* Duration
* Features
* Status

---
## 2️⃣ Customers Module

This module manages customer information.

### Features

* Add Customer
* View Customers
* Update Customer Details

### Customer Information

* Customer ID
* Name
* Email
* Phone Number
* Company Name
* Registration Date

### Validations

* Phone number must contain only digits
* Phone number must be exactly 10 digits
* Email must follow valid format

---
## 3️⃣ Subscription Module

This module connects customers with plans.

### Features

* Assign Subscription
* View Subscriptions
* Update Subscription
* Renew Subscription
* Cancel Subscription

### Subscription Information

* Subscription ID
* Customer ID
* Plan ID
* Start Date
* Expiry Date
* Status

### Status Types

* Active
* Expired
* Cancelled

### Automatic Features

* Expiry Date Calculation
* Subscription Renewal
* Subscription Status Tracking

---
## 4️⃣ Payment Module

This module records payment transactions.

### Features

* Add Payment
* View Payments
* Update Payment Details

### Payment Information

* Payment ID
* Subscription ID
* Amount
* Payment Date
* Payment Status
* Invoice Number

### Payment Status

* Paid
* Pending
* Failed

---
## 5️⃣ Invoice Generation Module

Professional PDF invoices are generated after successful payments.

### Invoice Contains

* Invoice Number
* Customer Name
* Plan Name
* Payment Date
* Amount Paid
* Payment Status

### Features

* PDF Invoice Generation
* Download Invoice
* Professional Layout

---
## 6️⃣ Reports Module

Provides business analytics and reporting.

### Features

* Total Customers
* Active Subscriptions
* Expired Subscriptions
* Total Revenue
* Payment Status Analysis
* Upcoming Expiry Tracking

---
# 📊 CSV Export

The system allows exporting reports in CSV format.

### Available Exports

* Customers Report
* Subscription Report
* Payment Report

---
# 🗄️ Database Schema
## Plans Table

```text
plan_id
plan_name
price
duration
features
status
```

## Customers Table
```text
customer_id
name
email
phone
company_name
registration_date
```
## Subscriptions Table

```text
subscription_id
customer_id
plan_id
start_date
expiry_date
status
```
## Payments Table
```text
payment_id
subscription_id
amount
payment_date
payment_status
invoice_no
``

# ▶️ Installation Guide

## Step 1: Clone Repository

```bash
git clone https://github.com/vap0611/SaaS_Subscription_System.git
```

## Step 2: Open Project Folder

```bash
cd SaaS_Subscription_System
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```
## Step 4: Create Database

```bash
python database.py
```
## Step 5: Run Streamlit Application

```bash
streamlit run app.py

# 🎯 Key Features Implemented
✅ Role-Based Login
✅ Plan Management
✅ Customer Management
✅ Subscription Assignment
✅ Automatic Expiry Calculation
✅ Subscription Renewal
✅ Subscription Cancellation
✅ Payment Management
✅ Invoice Generation
✅ CSV Export
✅ Business Reports
✅ Streamlit Dashboard
✅ SQLite Database Integration
✅ Professional UI

# 📈 Future Enhancements

* Email Reminder System
* SMS Notifications
* Password Encryption
* Cloud Database Integration
* Online Payment Gateway
* Advanced Analytics Dashboard

---

# 👩‍💻 Developed By

**Vidhi Patel**

Computer Engineering Student

Internship Project – SaaS Subscription Management System

Webvanta Innovations

---

# 📄 License

This project is developed for educational and internship purposes.

