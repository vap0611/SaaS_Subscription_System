from database.database import connection
from datetime import date
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Spacer,
    Paragraph
)
import os

def add_payment(subscription_id, amount, payment_status):
    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be greater than 0!"

        conn = connection()
        cursor = conn.cursor()

        invoice_no = f"INV{subscription_id}"
        payment_date = date.today().strftime("%Y-%m-%d")

        cursor.execute(
            """
            INSERT INTO payments
            (subscription_id, amount, payment_date, payment_status, invoice_no)
            VALUES (?, ?, ?, ?, ?)
            """,
            (subscription_id, amount, payment_date, payment_status, invoice_no)
        )

        conn.commit()
        conn.close()
        return True, "Payment Added Successfully!"

    except Exception as e:
        return False, f"Error adding payment: {e}"


def view_payments():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                pay.payment_id,
                c.name,
                p.plan_name,
                pay.amount,
                pay.payment_date,
                pay.payment_status,
                pay.invoice_no
            FROM payments pay
            JOIN subscriptions s ON pay.subscription_id = s.subscription_id
            JOIN customers c ON s.customer_id = c.customer_id
            JOIN plans p ON s.plan_id = p.plan_id
        """)

        payments = cursor.fetchall()
        conn.close()
        return True, payments
    except Exception as e:
        return False, f"Error fetching payments: {e}"


def update_payment(payment_id, choice, new_value):
    try:
        conn = connection()
        cursor = conn.cursor()

        if choice == 1:
            amount = float(new_value)
            cursor.execute("UPDATE payments SET amount = ? WHERE payment_id = ?", (amount, payment_id))
        elif choice == 2:
            cursor.execute("UPDATE payments SET payment_status = ? WHERE payment_id = ?", (new_value, payment_id))
        else:
            conn.close()
            return False, "Invalid Choice"

        conn.commit()
        conn.close()
        return True, "Payment Updated Successfully!"

    except Exception as e:
        return False, f"Error updating payment: {e}"


def generate_invoice(payment_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                pay.payment_id,
                pay.invoice_no,
                pay.amount,
                pay.payment_date,
                pay.payment_status,
                c.name,
                p.plan_name
            FROM payments pay
            JOIN subscriptions s ON pay.subscription_id = s.subscription_id
            JOIN customers c ON s.customer_id = c.customer_id
            JOIN plans p ON s.plan_id = p.plan_id
            WHERE pay.payment_id = ?
        """, (payment_id,))

        data = cursor.fetchone()
        conn.close()

        if not data:
            return False, "Payment not found!"

        payment_id = data[0]
        invoice_no = data[1]
        amount = data[2]
        payment_date = data[3]
        payment_status = data[4]
        customer_name = data[5]
        plan_name = data[6]

        if not os.path.exists("invoices"):
            os.makedirs("invoices")

        pdf_file = f"invoices/{invoice_no}.pdf"
        doc = SimpleDocTemplate(pdf_file)
        styles = getSampleStyleSheet()
        elements = []

        # HEADER
        header = Table([
            ["Webvanta Innovations"],
            ["SaaS Subscription & Billing Management"]
        ], colWidths=[500])
        header.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#2196F3")),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 18),
            ('FONTSIZE', (0,1), (-1,1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12)
        ]))
        elements.append(header)
        elements.append(Spacer(1,20))

        # INVOICE INFO
        invoice_info = Table([
            [f"Invoice No : {invoice_no}", f"Date : {payment_date}"],
            [f"Status : {payment_status}", f"Payment ID : {payment_id}"]
        ], colWidths=[250,250])
        invoice_info.setStyle(TableStyle([
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BACKGROUND',(0,0),(-1,-1),colors.whitesmoke),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold')
        ]))
        elements.append(invoice_info)
        elements.append(Spacer(1,20))

        # CUSTOMER DETAILS
        customer_details = Table([
            ["Customer Details"],
            [f"Customer Name : {customer_name}"],
            [f"Plan Name : {plan_name}"]
        ], colWidths=[500])
        customer_details.setStyle(TableStyle([
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold')
        ]))
        elements.append(customer_details)
        elements.append(Spacer(1,20))

        # PAYMENT DETAILS
        payment_table = Table([
            ["Description", "Qty", "Rate", "Total"],
            [f"{plan_name} Subscription", "1", f"₹ {amount}", f"₹ {amount}"]
        ], colWidths=[250,60,90,100])
        payment_table.setStyle(TableStyle([
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold')
        ]))
        elements.append(payment_table)
        elements.append(Spacer(1,20))

        # TOTAL SUMMARY
        gst = round(amount * 0.18, 2)
        grand_total = round(amount + gst, 2)
        summary = Table([
            ["Subscription Fee", f"₹ {amount}"],
            ["GST (18%)", f"₹ {gst}"],
            ["Grand Total", f"₹ {grand_total}"]
        ], colWidths=[350,150])
        summary.setStyle(TableStyle([
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BACKGROUND',(0,2),(-1,2),colors.lightgreen),
            ('FONTNAME',(0,2),(-1,2),'Helvetica-Bold')
        ]))
        elements.append(summary)
        elements.append(Spacer(1,30))

        # STATUS BOX
        if payment_status.lower() == "paid":
            color = colors.green
        elif payment_status.lower() == "pending":
            color = colors.orange
        else:
            color = colors.red

        status_box = Paragraph(
            f"<font color='{color.hexval()}'><b>{payment_status.upper()}</b></font>",
            styles['Heading2']
        )
        elements.append(status_box)
        elements.append(Spacer(1,40))

        # FOOTER
        elements.append(Paragraph("<b>Authorized Signature</b>", styles['Normal']))
        elements.append(Spacer(1,20))
        elements.append(Paragraph("Webvanta Innovations", styles['Normal']))
        elements.append(Spacer(1,40))
        footer_style = styles['Normal']
        footer_style.alignment = TA_CENTER
        elements.append(Paragraph("Thank you for choosing Webvanta Innovations", footer_style))
        elements.append(Paragraph("This is a computer-generated invoice.", footer_style))

        doc.build(elements)
        return True, pdf_file 
    except Exception as e:
        return False, f"Error generating invoice: {e}"