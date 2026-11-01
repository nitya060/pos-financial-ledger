"""Project: Retail POS & Financial Ledger
Description: Python script to automate retail billing, inventory tracking, expense management, and end-of-day financial P&L reporting to CSV.
Author: Nitya Gupta"""
import csv
daily_sales_log=[]
daily_expenses = []

def calculate_and_print_pnl(opening_inv, closing_inv, total_revenue):
"""Computes Cost of Goods Sold (COGS), Gross Profit, Operating Expenses, and Net Profit/Loss, then displays the formatted statement in the console."""
    opening_value = sum(data["stock"] * data["cost_price"] for data in opening_inv.values())
    closing_value = sum(data["stock"] * data["cost_price"] for data in closing_inv.values())
    cogs = opening_value - closing_value
    gross_profit = total_revenue - cogs
    margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0.0
    total_operating_expenses = sum(item['amount'] for item in daily_expenses)
    net_profit = gross_profit - total_operating_expenses
    net_profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0.0
    print("\n" + "=" * 45)
    print("-----AUTOMATED PROFIT & LOSS STATEMENT-----")
    print("=" * 45)
    print(f"  Opening Inventory Valuation : ₹{opening_value:.2f}")
    print(f"  Closing Inventory Valuation : ₹{closing_value:.2f}")
    print("-" * 45)
    print(f"  Cost of Goods Sold (COGS)   : ₹{cogs:.2f}")
    print(f"  Total Sales Revenue         : ₹{total_revenue:.2f}")
    print("-" * 45)
    if gross_profit >= 0:
        print(f"  Gross Profit            : ₹{gross_profit:.2f}")
        print(f"  Gross Profit Margin     : {margin:.2f}%")
    else:
        print(f"  Gross Loss              : ₹{abs(gross_profit):.2f}")
        print(f"  Gross Loss Margin       : {abs(margin):.2f}%")
    print("-" * 45)
    print(f"  Total Operating Expenses    : ₹{total_operating_expenses:.2f}")
    if net_profit >= 0:
        print(f"  Net Profit                  : ₹{net_profit:.2f}")
        print(f"  Net Profit Margin           : {net_profit_margin:.2f}%")
    else:
        print(f"  Net Loss                    : ₹{abs(net_profit):.2f}")
        print(f"  Net Loss Margin             : {abs(net_profit_margin):.2f}%")
    print("=" * 45)
financial_config = {         
    "discount_code": "FESTIVE5",
    "discount_pct": 5.0        
}
def financial_manager_portal(inventory):
"""Secure management portal to configure store-wide promotional discounts, audit profit margins, and update selling prices for inventory items."""
    global financial_config
    print("\n" + "=" * 45)
    print("      FINANCIAL MANAGER PORTAL - PRICING       ")
    print("=" * 45)
    pin = input("Enter Financial Manager PIN (Enter '1234'): ")
    if pin != "1234":
        print("[ERROR] Incorrect PIN. Access Denied.")
        return
    while True:
        print("\n--- FINANCIAL MANAGER SETTINGS ---")
        print("1. Update GST Tax Rate")
        print("2. Set Active Store Discount / Promo Code")
        print("3. View Current Rates & Rules")
        print("4. Return to Main Menu")
        choice = input("Select an option (1-4): ").strip()
        if choice == '1':
            new_gst = float(input("Enter new GST Tax Rate (%): "))
            financial_config["gst_rate"] = new_gst
            print(f"✓ Global GST Rate updated to {new_gst}%") 
        elif choice == '2':
            code = input("Enter Promo Code Name (e.g., FESTIVE5 or NONE): ").strip().upper()
            if code == "NONE":
                financial_config["discount_code"] = None
                financial_config["discount_pct"] = 0.0
                print("✓ All active promo codes disabled.")
            else:
                pct = float(input(f"Enter discount percentage for '{code}' (%): "))
                financial_config["discount_code"] = code
                financial_config["discount_pct"] = pct
                print(f"✓ Promo code '{code}' set to {pct}% discount.")  
        elif choice == '3':
            print(f"\n--- ACTIVE FINANCIAL RULES ---")
            print(f"GST Rate: Slabs are now item-specific (configured per product during setup)")
            if financial_config["discount_code"]:
                print(f"Active Promo Code: {financial_config['discount_code']} ({financial_config['discount_pct']}% OFF)")
            else:
                print("Active Promo Code: None")         
        elif choice == '4':
            print("Returning to Main Menu...")
            break
        else:
            print("[ERROR] Invalid choice. Please select between 1 and 4.")
   
    while True:
        print("\nCurrent Inventory & Prices:")
        for item_name, data in inventory.items():
            print(f" - {item_name}: Cost Price = ₹{data['cost_price']} | Selling Price = ₹{data['price']}")  
        target_item = input("\nEnter product name to set/update Selling Price (or type 'done' to finish): ").strip().lower()
        if target_item == 'done':
            break          
        if target_item in inventory:
            try:
                new_sp = float(input(f"Enter Selling Price (SP) for {target_item}: ₹"))
                if new_sp <= inventory[target_item]['cost_price']:
                    print("⚠️ [WARNING] Selling price is less than or equal to Cost Price! (Risk of Loss)")
                inventory[target_item]["price"] = new_sp
                print(f"[SUCCESS] Selling Price for {target_item} set to ₹{new_sp:.2f}\n")
            except ValueError:
                print("Invalid input. Please enter a valid number for price.")
        else:
            print("[ERROR] Item not found in inventory.")
customer_id = 1
from datetime import datetime

def inventory_manager_portal(inventory, opening_inventory):
"""Initializes product catalogs, stock levels, cost prices, restock thresholds,and item-specific tax slabs before establishing opening inventory balances."""
    print("\n--- INVENTORY INITIALIZATION ---")
    print("Add your products one by one. Type 'done' when finished.\n")
    while True:
        item_name = input("Enter product name (or type 'done' to finish): ").strip().lower()
        if item_name.lower() == 'done':
            break
        if not item_name:
            print("Product name cannot be blank. Please try again.")
            continue
        try:
            stock_qty = int(input(f"Enter initial stock available for {item_name}: "))
            cost_price = float(input(f"Enter Cost Price (CP) for {item_name}: "))
            min_stock = int(input(f"Enter Minimum Stock Alert Threshold for {item_name}: "))
            gst_rate = float(input(f"Enter GST Rate (%) for {item_name} (e.g., 5, 12, 18): "))
        except ValueError:
            print("Invalid number entered. Please try again.")
            continue
        inventory[item_name] = {
            "stock": stock_qty,
            "cost_price": cost_price,
            "price": 0.0,
            "min_stock": min_stock,
            "gst_rate": gst_rate
        }
        print(f"-> Added {item_name} successfully! (CP: ₹{cost_price:.2f} | Min Alert: {min_stock})\n")
    print("\n--- Inventory Setup Complete! Store is Open. ---")
    for item, data in inventory.items():
        opening_inventory[item] = {
         "stock": data["stock"], 
         "cost_price": data["cost_price"], 
         "price": data["price"], 
         "min_stock": data["min_stock"]
        }
total_customers_today = 0
total_revenue_today = 0.0
total_tax_today = 0.0
total_discount_today = 0.0
total_cash_received_today = 0.0
total_cash_returned_today = 0.0
return_amount = 0.0
balance_due = 0.0
total_cash_received_online = 0.0
total_cash_received_offline = 0.0

def cashier_pos_terminal(inventory):
"""Handles customer billing cycles, cart additions, inventory stock deduction,itemized GST and promo discount calculations, payment processing, and transaction logging."""
    global customer_id, total_customers_today, total_revenue_today, total_tax_today, total_discount_today, total_cash_received_today, total_cash_returned_today, total_cash_received_online, total_cash_received_offline, return_amount, balance_due
    
    print("\n----NEW CUSTOMER----")
    print("***HELLO CUSTOMER, WELCOME TO THE SHOPPING STORE***")
    return_amount = 0.0
    balance_due = 0.0
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    name = input("ENTER CUSTOMER NAME: ")
    while True:
        try:
            n = int(input("ENTER TYPES OF ITEMS: "))
            break
        except ValueError:
            print("INVALID INPUT, PLEASE ENTER A WHOLE NUMBER.")
            
    total = 0
    cart_items = []
    for i in range(0, n):
        while True:
            in_stock_items = [item for item, data in inventory.items() if data["stock"] > 0]
            if not in_stock_items:
                print("\nALERT: Store is completely SOLD OUT of all items!")
                break
            print(f"Available items: {in_stock_items}")
            item_name = input(f"ENTER ITEM {i+1} NAME (or type 'done' to finish): ").strip().lower()
            if item_name.lower() == 'done':
                break  
            if item_name not in inventory:
                print(f"Error: '{item_name}' is not in store inventory.")
                continue 
            available_stock = inventory[item_name]["stock"]
            if available_stock <= 0:
                print(f"Sorry, '{item_name}' is completely OUT OF STOCK!")
                continue  
            break
        if 'item_name' in locals() and item_name.lower() == 'done':
            break
        
        while True:
            try:
                quantity = float(input(f"Enter quantity for {item_name} (Available: {available_stock}): "))
                if quantity <= 0:
                    print("Quantity must be greater than 0.")
                    continue
                if quantity > available_stock:
                    print(f"Insufficient stock! You asked for {quantity}, but only {available_stock} are left.")
                    continue
                break 
            except ValueError:
                print("INVALID INPUT, PLEASE ENTER A NUMBER.")
        
        inventory[item_name]["stock"] -= quantity
        amount = inventory[item_name]["price"]
        unit = "units"
        item_subtotal = amount * quantity
        item_gst_rate = inventory[item_name]["gst_rate"] 
        item_tax = item_subtotal * (item_gst_rate / 100)  
        total += item_subtotal
        cart_items.append({
           "name": item_name,
           "amount": amount,
           "unit": unit,
           "quantity": quantity,
           "subtotal": item_subtotal,
           "gst_rate": item_gst_rate, 
           "tax_amount": item_tax
        })
    discount_amount = 0.0
    if financial_config.get("discount_code"):
        apply_promo = input(f"Apply manager promo code '{financial_config['discount_code']}' ({financial_config['discount_pct']}% OFF)? (y/n): ").strip().lower()
        if apply_promo == 'y':
            discount_amount = total * (financial_config["discount_pct"] / 100)
            print(f"✓ Promo Code Applied: -₹{discount_amount:.2f}")

    total_after_discount = total - discount_amount
    tax_amount = sum(item["tax_amount"] for item in cart_items) 
    grand_total = total_after_discount + tax_amount
    print(f"DATE & TIME: {formatted_date}")
    print(f"CUSTOMER NAME: {name}")
    print(f"TOTAL: {total}")
    print(f"TAX AMOUNT: {tax_amount}")
    print(f"DISCOUNT: {discount_amount}")
    print(f"GRAND TOTAL: {grand_total}")
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

    cash_paid = 0.0
    online_amount = 0.0
    offline_amount = 0.0
    if payment_mode_str == 1:
        cash_paid = float(input("Enter cash received from customer: "))
        if cash_paid > grand_total:
            return_amount = cash_paid - grand_total
            print(f"RETURN AMOUNT (Change): {return_amount:.2f}")
            offline_amount = grand_total
        elif cash_paid == grand_total:
            print("Zero balance. Exact amount paid.")
            offline_amount = grand_total
        else:
            balance_due = grand_total - cash_paid
            print(f"BALANCE DUE: {balance_due:.2f}")
            offline_amount = cash_paid
    else:
        online_amount = grand_total
        cash_paid = grand_total
        print(f"Online payment of {grand_total:.2f} processed successfully. Exact amount paid.")
   
    print("\n--- ITEMIZED BILL ---")
    print(f"STORE NAME: {store_name}")
    print(f"LOCATION: {location}")
    print("-" * 45)
    print(f"CONTACT NUMBER: {contact_no}")
    print(f"CUSTOMER NAME: {name}")
    print("_" * 45)
    print(f"{'ITEM NAME':<15} {'QTY':<8} {'PRICE':<10} {'SUBTOTAL'}")
    print("-" * 45)
    for item in cart_items:
        print(f"{item['name']:<15} {item['quantity']:<8} ₹{item['amount']:<9} ₹{item['subtotal']}")
    print("-" * 45)
    print(f"Subtotal: ₹{total}")
    print(f"Discount: -₹{discount_amount}")
    print(f"Total GST (Itemized): ₹{tax_amount}")
    print("=" * 45)
    print(f"GRAND TOTAL: ₹{grand_total}")
    print("=" * 45)
    print(f"BALANCE DUE TO PAY: ₹{balance_due}")
    print(f"RETURN AMOUNT: ₹{return_amount}")
    print("-" * 45)
    print("THANKYOU FOR SHOPPING")
    
    total_customers_today += 1
    total_revenue_today += grand_total
    total_tax_today += tax_amount
    total_discount_today += discount_amount
    total_cash_received_today += cash_paid
    total_cash_received_online += online_amount
    total_cash_received_offline += offline_amount
    total_cash_received_today += (online_amount + offline_amount)
    total_cash_returned_today += return_amount  
    for index, item in enumerate(cart_items):
        if index == 0:
            row_timestamp = formatted_date
            row_customer_name = name
            row_tax_amount = tax_amount
            row_discount_amount = discount_amount
            row_grand_total = grand_total
            row_amount_paid = cash_paid
            row_balance_due = balance_due
            row_return_amount = return_amount
            row_payment_mode = "Offline" if payment_mode_str == 1 else "Online"
        else:
            row_timestamp = ""
            row_customer_name = ""
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
            "customer_name": row_customer_name,
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
    customer_id += 1

def expense_manager():
"""Tracks and records daily overhead operating costs (such as rent, electricity, and packaging) to calculate into net profit."""
    while True:
        print("\n=============================================")
        print("           EXPENSE MANAGER PORTAL            ")
        print("=============================================")
        print("1. Add Store Expense")
        print("2. View Today's Recorded Expenses")
        print("3. Return to Main Menu")
        print("=============================================")

        choice = input("Select an option (1-3): ").strip()

        if choice == '1':
            category = input("Enter expense category (e.g., Rent, Electricity, Packaging): ").strip()
            try:
                amount = float(input(f"Enter amount for '{category}': ₹"))
                if amount > 0:
                    daily_expenses.append({'category': category, 'amount': amount})
                    print(f"[SUCCESS] Recorded expense: {category} - ₹{amount:.2f}")
                else:
                    print("[ERROR] Expense amount must be greater than 0.")
            except ValueError:
                print("[ERROR] Invalid input. Please enter a valid numerical amount.")

        elif choice == '2':
            print("\n--- TODAY'S RECORDED EXPENSES ---")
            if not daily_expenses:
                print("No expenses recorded for today.")
            else:
                total_exp = 0.0
                for idx, item in enumerate(daily_expenses, 1):
                    print(f"{idx}. {item['category']}: ₹{item['amount']:.2f}")
                    total_exp += item['amount']
                print("---------------------------------------------")
                print(f"Total Logged Expenses: ₹{total_exp:.2f}")

        elif choice == '3':
            print("Returning to Main Menu...")
            break
        else:
            print("[ERROR] Invalid choice. Please enter 1, 2, or 3.")

def generate_eod_report(opening_inventory, inventory):
"""Compiles end-of-day operational summaries, triggers P&L statements,and writes multi-table structured datasets to 'pos_sales_report.csv'."""
    print("\n" + "="*45)
    print("      END OF DAY SALES REPORT        ")
    print("="*45)
    print(f"Total Customers Served: {total_customers_today}")
    print(f"Total Revenue (Sales): ₹{total_revenue_today:.2f}")
    print(f"Total Tax Collected: ₹{total_tax_today:.2f}")
    print(f"Total Discounts Given: ₹{total_discount_today:.2f}")
    print(f"Total Amount Received Online: ₹{total_cash_received_online:.2f}")
    print(f"Total Amount Received Offline: ₹{total_cash_received_offline:.2f}")
    print(f"Total Amount Received: ₹{total_cash_received_today:.2f}")
    print(f"Total Cash Returned: ₹{total_cash_returned_today:.2f}")
    print(f"Total Balance Due to Receive: ₹{balance_due:.2f}")
    print("\n--- Remaining Inventory Stock & Restock Alerts ---")
    for item_name, data in inventory.items():
        if data["stock"] <= data["min_stock"]:
            print("!!![LOW STOCK - REORDER RECOMMENDED]!!!")
        print(f" - {item_name}: {data['stock']} units left (CP: ₹{data['cost_price']} | SP: ₹{data['price']})")
    print("-" * 45)
    calculate_and_print_pnl(opening_inventory, inventory, total_revenue_today)
    with open("pos_sales_report.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Table 1: Morning Opening Inventory Valuation
        writer.writerow(["-----------TABLE 1: MORNING OPENING INVENTORY-----------"])
        writer.writerow(["Item Name", "Initial Stock", "Cost Price (INR)", "Total Value (INR)"])
        for item_name, data in opening_inventory.items():
            total_val = data["stock"] * data["cost_price"]
            writer.writerow([item_name, data["stock"], data["cost_price"], total_val])
        writer.writerow([])
        writer.writerow([])
        # Table 2: Daily Customer Transaction Journal
        writer.writerow(["-----------TABLE 2: DAILY CUSTOMER SALES JOURNAL-----------"])
        writer.writerow([
            "Customer ID", "Customer Name", "Time Stamp", "Item Name", 
            "Quantity", "Unit Price", "Subtotal", "Tax Amount", "Discount Amount", 
            "Grand Total", "Payment Mode", "Amount Paid", "Balance Due", "Return Amount"
        ])
        for sale in daily_sales_log:
            writer.writerow([
                sale["customer_id"], sale["customer_name"],
                sale["timestamp"], sale["name"], sale["quantity"], sale["amount"],
                sale["subtotal"], sale["tax_amount"], sale["discount_amount"],
                sale["grand_total"], sale["payment_mode"], sale["amount_paid"],
                sale["balance_due"], sale["return_amount"]
            ])
        writer.writerow([])
        writer.writerow([])

        # Table 3: Closing Left-Out Stock Audit
        writer.writerow(["-----------TABLE 3: CLOSING / LEFT-OUT STOCK-----------"])
        writer.writerow(["Item Name", "Closing Stock", "Cost Price (INR)", "Total Value (INR)"])
        for item_name, data in inventory.items():
            total_val = data["stock"] * data["cost_price"]
            writer.writerow([item_name.title(), data["stock"], data["cost_price"], total_val])
        writer.writerow([])
        writer.writerow([])

        # Table 4: Automated P&L Summary Block
        writer.writerow(["-----------TABLE 4: PROFIT & LOSS SUMMARY-----------"])
        opening_value = sum(data["stock"] * data["cost_price"] for data in opening_inventory.values())
        closing_value = sum(data["stock"] * data["cost_price"] for data in inventory.values())
        cogs = opening_value - closing_value
        gross_profit = total_revenue_today - cogs
        margin = (gross_profit / total_revenue_today * 100) if total_revenue_today > 0 else 0.0
        total_operating_expenses = sum(item['amount'] for item in daily_expenses)
        net_profit = gross_profit - total_operating_expenses
        net_profit_margin = (net_profit / total_revenue_today * 100) if total_revenue_today > 0 else 0.0

        writer.writerow(["Total Operating Expenses", f"{total_operating_expenses:.2f}"])
        writer.writerow(["Opening Inventory Valuation", f"{opening_value:.2f}"])
        writer.writerow(["Closing Inventory Valuation", f"{closing_value:.2f}"])
        writer.writerow(["Cost of Goods Sold (COGS)", f"{cogs:.2f}"])
        writer.writerow(["Total Sales Revenue", f"{total_revenue_today:.2f}"])
        writer.writerow(["Gross Profit / Loss", f"{gross_profit:.2f}"])
        writer.writerow(["Gross Profit Margin (%)", f"{margin:.2f}%"])
        writer.writerow(["Net Profit / Loss", f"{net_profit:.2f}"])
        writer.writerow(["Net Profit Margin (%)", f"{net_profit_margin:.2f}%"])
    print("[SUCCESS] End-of-Day Sales Report exported to 'pos_sales_report.csv'.")
    print(" STORE IS NOW CLOSED. GOODBYE! ")

if __name__ == "__main__":
    # Application Entry Point & Interactive Main Menu Loop
    store_name = input("ENTER STORE NAME: ")
    location = input("ENTER LOCATION: ")
    while True:
        try:
            contact_no = int(input("ENTER CONTACT NUMBER: "))
            break
        except ValueError:
            print("INVALID INPUT, PLEASE ENTER A WHOLE NUMBER")
    inventory = {}
    opening_inventory = {}
    while True:
        print("\n" + "=" * 45)
        print("         STORE MANAGEMENT MAIN MENU         ")
        print("=" * 45)
        print("1. Inventory Manager Portal (Setup / Restock)")
        print("2. Financial Manager Portal (Pricing / Audit)")
        print("3. Cashier POS Terminal (Billing)")
        print("4. Expense Manager Portal (Daily Costs)")       
        print("5. End-of-Day (EOD) P&L Report & Exit")
        print("=" * 45)
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            inventory_manager_portal(inventory, opening_inventory)
        elif choice == '2':
            financial_manager_portal(inventory)
        elif choice == '3':
            if not inventory:
                print("\n[ERROR] Inventory is empty! Please run Option 1 (Inventory Manager Portal) first.")
            else:
                cashier_pos_terminal(inventory)
        elif choice == '4':
           expense_manager()
        elif choice == '5':
            generate_eod_report(opening_inventory, inventory)
            break
        else:
            print("[ERROR] Invalid selection. Please choose between 1 and 5.")
        
