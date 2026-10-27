import csv
daily_sales_log=[]
customer_id = 1
from datetime import datetime
store_name = input("ENTER STORE NAME:")
location = input ("ENTER LOCATION:")
while True:
   try:
    contact_no = int(input("ENTER CONTACT NUMBER:"))
    break
   except ValueError:
      print ("INVALID INPUT, PLEASE ENTER A WHOLE NUMBER")

total_customers_today = 0
total_revenue_today = 0.0
total_tax_today = 0.0
total_discount_today = 0.0
total_cash_received_today = 0.0
return_amount = 0.0
balance_due = 0.0
total_cash_received_online = 0.0
total_cash_received_offline = 0.0
def generate_receipt():
   print("\n----NEW CUSTOMER----")
   print ("***HELLO CUSTOMER, WELCOME TO THE SHOPPING STORE***")
   return_amount = 0.0
   balance_due = 0.0
   now = datetime.now()
   formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
   name = input("ENTER CUSTOMER NAME:")
   while True:
    try:
     n= int(input("ENTER TYPES OF ITEMS:"))
     break
    except ValueError:
        print ("INVALID INPUT,PLEASE ENTER A WHOLE NUMBER.")
   total=0
   item_name=0
   cart_items=[]
   for i in range (0,n):
     item_name = input ("ENTER ITEM NAME:")
     while True:
      try:
       amount = float(input("ENTER AMOUNT:"))
       break
      except ValueError:
        print ("INVALID INPUT,PLEASE ENTER A WHOLE NUMBER OR DECIMAL VALUE")
     unit = input ("ENTER UNIT (EG. KG,LITRE,GRAM,PIECES,DOZENS)")
     while True:
      try:
       quantity = float(input("ENTER QUANTITY:"))
       break
      except ValueError:
        print ("INVALID INPUT,PLEASE ENTER A WHOLE NUMBER OR DECIMAL VALUE")
     item_subtotal = amount * quantity
     total += item_subtotal
     cart_items.append({
      "name": item_name,
      "amount": amount,
      "unit": unit,
      "quantity": quantity,
      "subtotal": item_subtotal
       })
     discount_rate = 0.10
     discount_amount = (total*discount_rate)
     total_after_discount = total - discount_amount
     tax_rate = 0.05
     tax_amount = (total*tax_rate)
     grand_total = tax_amount + total_after_discount
     
   print(f"DATE & TIME:{formatted_date}")
   print(f"CUSTOMER NAME:{name}")
   print(f"TOTAL:{total}")
   print(f"TAX AMOUNT:{tax_amount}")
   print(f"DISCOUNT:{discount_amount}")
   print(f"GRAND TOTAL:",grand_total)
   print("\n-----PAYMENT MODE:-----")
   print("1. Offline (Cash)")
   print("2. Online (UPI / Card)")
   while True:
        try:
            payment_mode_str = int(input("Enter payment mode (1 or 2): "))
            if payment_mode_str == 1 or payment_mode_str == 2:
                break
            else:
                print("Please enter 1 for Offline or 2 for Online.")
        except ValueError:
            print("INVALID INPUT. Please enter a whole number (1 or 2).")
   return_amount = 0.0
   balance_due = 0.0
   online_amount = 0.0
   offline_amount = 0.0
   if payment_mode_str == 1:
        cash_paid = float(input("Enter cash received from customer: "))
        if cash_paid > grand_total:
            return_amount = cash_paid - grand_total
            print(f"RETURN AMOUNT (Change): {return_amount:.2f}")
        elif cash_paid == grand_total:
            print("Zero balance. Exact amount paid.")
        else:
            balance_due = grand_total - cash_paid
            print(f"BALANCE DUE: {balance_due:.2f}")
        offline_amount = cash_paid-return_amount
   else:
        online_amount = grand_total
        cash_paid = grand_total
        print(f"Online payment of {grand_total:.2f} processed successfully. Exact amount paid.")
   
   print("\n--- ITEMIZED BILL ---")
   print (f"STORE NAME: {store_name}")
   print (f"LOCATION: {location}")
   print (f"CONTACT NUMBER: {contact_no}")
   print(f"CUSTOMER NAME: {name}")
   print(f"{'ITEM NAME':<15} {'QTY':<8} {'PRICE':<10} {'SUBTOTAL'}")
   print("-" * 45)
   for item in cart_items:
     print(f"{item['name']:<15} {item['quantity']:<8} {item['amount']:<10.2f} {item['subtotal']:.2f}")
     print("-" * 45)
   print ("THANKYOU FOR SHOPPING")
   return formatted_date, grand_total, tax_amount, discount_amount, cash_paid, return_amount, balance_due, online_amount, offline_amount, cart_items, payment_mode_str, name

while True:
    formatted_date, g_total, t_amount, d_amount, c_paid, r_amount, b_due, online_amount, offline_amount, cart_items, payment_mode_str, name = generate_receipt()
    for index, item in enumerate(cart_items):
        if index == 0:
            row_timestamp = formatted_date
            row_customer_name = name
            row_contact_no = contact_no
            row_tax_amount = t_amount
            row_discount_amount = d_amount
            row_grand_total = g_total
            row_amount_paid = c_paid
            row_balance_due = b_due
            row_return_amount = r_amount
            row_payment_mode = payment_mode_str
        else:
            row_timestamp = ""
            row_customer_name = ""
            row_contact_no = ""
            row_tax_amount = ""
            row_discount_amount = ""
            row_grand_total = ""
            row_amount_paid = ""
            row_balance_due = ""
            row_return_amount = ""
            row_payment_mode = ""

        daily_sales_log.append({
            "timestamp": row_timestamp,
            "customer_id": customer_id,
            "customer_name": name,
            "customer_contact_no": contact_no,
            "name": item["name"],
            "quantity": item["quantity"],
            "amount": item["amount"],
            "subtotal": item["subtotal"],
            "tax_amount": row_tax_amount,
            "discount_amount": row_discount_amount,
            "grand_total": row_grand_total,
            "payment_mode": row_payment_mode,
            "amount_paid": row_amount_paid,
            "balance_due": row_balance_due,
            "return_amount": row_return_amount
        })
    total_customers_today += 1
    customer_id += 1
    total_revenue_today += g_total
    total_tax_today += t_amount
    total_discount_today += d_amount
    total_cash_received_today += (c_paid-r_amount)
    total_cash_received_online += online_amount
    total_cash_received_offline += offline_amount
    return_amount += r_amount
    balance_due += b_due
    cont = input("\nServe another customer? (yes/no): ")
    if cont.lower() == 'yes':
       continue
    else:
       print("\n" + "-" * 40)
       print("  END OF DAY SALES REPORT  ")
       print("-" * 40)
       print(f"Total Customers Served: {total_customers_today}")
       print(f"Total Revenue (Sales): {total_revenue_today:.2f}")#.2f is used to put the decimal upto 2 places
       print(f"Total Tax Collected: {total_tax_today:.2f}")
       print(f"Total Discounts Given: {total_discount_today:.2f}")
       print(f"Total Amount Received Online: {online_amount:.2f}")
       print(f"Total Amount Received Offline: {total_cash_received_offline:.2f}")
       print(f"Total Amount Received: {total_cash_received_today:.2f}")
       print(f"Total Cash Returned: {return_amount:.2f}")
       print(f"Total Balance Due to Receive: {balance_due:.2f}")
       print("-" * 40)
       print ("  STORE IS NOW CLOSED. GOODBYE!  ")
       break
      
with open("pos_sales_report.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Customer ID", "Customer Name", "Contact No", "Time Stamp", "Item Name", "Quantity", "Unit Price", "Subtotal", "Tax Amount", "Discount Amount","Grand Total", "Payment Mode", "Amount Paid", "Balance Due", "Return amount"])
    
    
    for sale in daily_sales_log:
        writer.writerow([
            sale["customer_id"],
            sale["customer_name"],
            sale["customer_contact_no"],
            sale["timestamp"],
            sale["name"],
            sale["quantity"],
            sale["amount"],
            sale["subtotal"],
            sale["tax_amount"],
            sale["discount_amount"],
            sale["grand_total"],
            sale["payment_mode"],
            sale["amount_paid"],
            sale["balance_due"],
            sale["return_amount"]
        ])

print("[INFO] Success! All daily transactions exported to 'pos_sales_report.csv'.")
