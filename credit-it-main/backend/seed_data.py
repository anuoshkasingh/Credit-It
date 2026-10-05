import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "credit_it.db")

def create_tables(conn):
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        pan TEXT,
        dob TEXT
    );
    """)
    
    # Transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        transaction_date TEXT NOT NULL,
        merchant_name TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        merchant_type TEXT NOT NULL,
        frequency_type TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    );
    """)
    
    # Credit cards table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credit_cards (
        card_id TEXT PRIMARY KEY,
        card_name TEXT NOT NULL,
        bank_name TEXT NOT NULL,
        card_network TEXT NOT NULL,
        card_type TEXT NOT NULL,
        image_path TEXT NOT NULL,
        apply_url TEXT NOT NULL,
        
        -- Fees
        joining_fee REAL DEFAULT 0,
        annual_fee REAL DEFAULT 0,
        annual_fee_waiver_spend REAL DEFAULT 0,
        
        -- Eligibility
        minimum_income REAL DEFAULT 0,
        minimum_credit_score INTEGER DEFAULT 600,
        eligibility_notes TEXT,
        
        -- Reward rules
        reward_type TEXT NOT NULL,
        reward_rate REAL DEFAULT 0,
        reward_value REAL DEFAULT 1.0,
        reward_cap REAL DEFAULT 0,
        minimum_spend_for_rewards REAL DEFAULT 0,
        reward_expiry TEXT,
        excluded_categories TEXT,
        
        -- Category Rewards (Percentage return)
        food_reward REAL DEFAULT 0,
        shopping_reward REAL DEFAULT 0,
        travel_reward REAL DEFAULT 0,
        fuel_reward REAL DEFAULT 0,
        grocery_reward REAL DEFAULT 0,
        utility_reward REAL DEFAULT 0,
        online_reward REAL DEFAULT 0,
        offline_reward REAL DEFAULT 0,
        international_reward REAL DEFAULT 0,
        
        -- Benefits
        welcome_benefit TEXT,
        welcome_spend_requirement REAL DEFAULT 0,
        milestone_benefit TEXT,
        milestone_spend REAL DEFAULT 0,
        lounge_access TEXT,
        lounge_spend_requirement REAL DEFAULT 0,
        fuel_surcharge_waiver TEXT,
        dining_benefit TEXT,
        movie_benefit TEXT,
        travel_benefit TEXT,
        hotel_benefit TEXT,
        shopping_benefit TEXT,
        grocery_benefit TEXT,
        insurance_benefit TEXT,
        
        -- Charges
        forex_markup REAL DEFAULT 3.5,
        cash_withdrawal_fee REAL DEFAULT 500,
        late_payment_fee REAL DEFAULT 750,
        interest_rate REAL DEFAULT 3.5,
        overlimit_fee REAL DEFAULT 500,
        card_replacement_fee REAL DEFAULT 100
    );
    """)
    
    conn.commit()

def seed_users(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users;")
    
    users_data = [
        ("001", "Rohan Sharma", "rohan.s@gmail.com", "+91 98765 43210", "ABCDE1234F", "15/08/1995"),
        ("002", "Anuoshka Singh", "anuoshka.s@gmail.com", "+91 98123 45678", "BKWPS5678G", "22/11/1998"),
        ("003", "Aarya Janghel", "aarya.j@gmail.com", "+91 97531 24680", "CPZTR9012H", "05/03/2003")
    ]
    
    cursor.executemany("""
    INSERT INTO users (user_id, name, email, phone, pan, dob)
    VALUES (?, ?, ?, ?, ?, ?);
    """, users_data)
    
    conn.commit()

def seed_transactions(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions;")
    
    random.seed(42)
    start_date = datetime.now() - timedelta(days=270)
    
    user1_merchants = [
        ("MakeMyTrip Flights", "Travel", "Flights", 18000, 38000, "Credit Card", "Online", "One-time"),
        ("Taj Hotels & Resorts", "Travel", "Hotels", 15000, 32000, "Credit Card", "Online", "One-time"),
        ("Vistara Airlines", "Travel", "Flights", 12000, 28000, "Credit Card", "Online", "One-time"),
        ("Uber Premier", "Travel", "Cab", 800, 2500, "UPI", "Online", "One-time"),
        ("Zara Luxe", "Shopping", "Apparel", 6000, 18000, "Credit Card", "Offline", "One-time"),
        ("Apple Premium Reseller", "Shopping", "Electronics", 15000, 45000, "Credit Card", "Offline", "One-time"),
        ("Tata CLiQ Luxury", "Shopping", "Luxury Goods", 8000, 25000, "Credit Card", "Online", "One-time"),
        ("Myntra Luxe", "Shopping", "Fashion", 4000, 12000, "Credit Card", "Online", "One-time"),
        ("Olive Bar & Kitchen", "Dining", "Restaurants", 3500, 8500, "Credit Card", "Offline", "One-time"),
        ("Bespoke Fine Dining", "Dining", "Restaurants", 4000, 9500, "Credit Card", "Offline", "One-time"),
        ("Swiggy Gourmet", "Food", "Food Delivery", 1200, 3500, "UPI", "Online", "One-time"),
        ("Shell Select Fuel Station", "Fuel", "Fuel", 3000, 5500, "Debit Card", "Offline", "Recurring"),
        ("Adani Electricity", "Utilities", "Electricity", 4500, 8000, "UPI", "Online", "Recurring"),
        ("Airtel Postpaid Family", "Utilities", "Telecom", 1999, 2999, "Credit Card", "Online", "Recurring"),
        ("Netflix Premium 4K", "Entertainment", "Streaming", 649, 649, "Credit Card", "Online", "Recurring"),
    ]
    
    user1_txs = []
    tx_count = 1
    for i in range(100):
        m_info = random.choice(user1_merchants)
        tx_id = f"TXN_USER1_{tx_count:03d}"
        tx_date = (start_date + timedelta(days=random.randint(1, 265), hours=random.randint(8, 22))).strftime("%Y-%m-%d %H:%M:%S")
        merchant, cat, subcat, min_a, max_a, p_method, m_type, f_type = m_info
        amount = round(random.uniform(min_a, max_a), 2)
        user1_txs.append((tx_id, "001", tx_date, merchant, cat, subcat, amount, p_method, m_type, f_type))
        tx_count += 1

    anuoshka_merchants = [
        ("D-Mart Supermarket", "Groceries", "Supermarket", 1500, 3800, "UPI", "Offline", "Recurring"),
        ("BigBasket Grocery", "Groceries", "Grocery", 1200, 2900, "UPI", "Online", "Recurring"),
        ("Zomato Delivery", "Food", "Food Delivery", 350, 950, "UPI", "Online", "One-time"),
        ("Local Cafe & Bakery", "Food", "Restaurants", 450, 1200, "UPI", "Offline", "One-time"),
        ("Myntra Fashion", "Shopping", "Apparel", 1200, 3500, "Credit Card", "Online", "One-time"),
        ("Amazon India", "Shopping", "General Shopping", 800, 2800, "Credit Card", "Online", "One-time"),
        ("IRCTC Train Booking", "Travel", "Train", 650, 1800, "UPI", "Online", "One-time"),
        ("Uber Go", "Travel", "Cab", 220, 650, "UPI", "Online", "One-time"),
        ("HPCL Fuel Pump", "Fuel", "Fuel", 1500, 2500, "Debit Card", "Offline", "Recurring"),
        ("Electricity Board Bill", "Utilities", "Electricity", 1200, 2400, "UPI", "Online", "Recurring"),
        ("Jio Postpaid", "Utilities", "Telecom", 499, 799, "UPI", "Online", "Recurring"),
        ("BookMyShow Movies", "Entertainment", "Movies", 400, 900, "UPI", "Online", "One-time"),
    ]
    
    anuoshka_txs = []
    for i in range(100):
        m_info = random.choice(anuoshka_merchants)
        tx_id = f"TXN_ANUOSHKA_{tx_count:03d}"
        tx_date = (start_date + timedelta(days=random.randint(1, 265), hours=random.randint(9, 21))).strftime("%Y-%m-%d %H:%M:%S")
        merchant, cat, subcat, min_a, max_a, p_method, m_type, f_type = m_info
        amount = round(random.uniform(min_a, max_a), 2)
        anuoshka_txs.append((tx_id, "002", tx_date, merchant, cat, subcat, amount, p_method, m_type, f_type))
        tx_count += 1

    aarya_merchants = [
        ("Campus Canteen", "Food", "Fast Food", 60, 220, "UPI", "Offline", "One-time"),
        ("Chai Point", "Food", "Beverages", 40, 150, "UPI", "Offline", "One-time"),
        ("Swiggy Snacks", "Food", "Food Delivery", 120, 380, "UPI", "Online", "One-time"),
        ("Zepto Quick Delivery", "Groceries", "Grocery", 90, 350, "UPI", "Online", "One-time"),
        ("Metro Rail Recharge", "Transport", "Metro", 100, 500, "UPI", "Online", "One-time"),
        ("Uber Auto", "Transport", "Cab", 50, 180, "UPI", "Online", "One-time"),
        ("PVR Cinemas", "Entertainment", "Movies", 250, 550, "UPI", "Offline", "One-time"),
        ("Spotify Student Premium", "Entertainment", "Streaming", 59, 59, "UPI", "Online", "Recurring"),
        ("Amazon Student Buy", "Shopping", "Stationery & Electronics", 300, 1500, "UPI", "Online", "One-time"),
        ("Trendy Youth Fashion", "Shopping", "Apparel", 450, 1200, "UPI", "Offline", "One-time"),
        ("Airtel Prepaid Mobile", "Utilities", "Recharge", 299, 479, "UPI", "Online", "One-time"),
    ]
    
    aarya_txs = []
    for i in range(100):
        m_info = random.choice(aarya_merchants)
        tx_id = f"TXN_AARYA_{tx_count:03d}"
        tx_date = (start_date + timedelta(days=random.randint(1, 265), hours=random.randint(10, 23))).strftime("%Y-%m-%d %H:%M:%S")
        merchant, cat, subcat, min_a, max_a, p_method, m_type, f_type = m_info
        amount = round(random.uniform(min_a, max_a), 2)
        aarya_txs.append((tx_id, "003", tx_date, merchant, cat, subcat, amount, p_method, m_type, f_type))
        tx_count += 1

    all_txs = user1_txs + anuoshka_txs + aarya_txs
    cursor.executemany("""
    INSERT INTO transactions (transaction_id, user_id, transaction_date, merchant_name, category, subcategory, amount, payment_method, merchant_type, frequency_type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, all_txs)
    
    conn.commit()

def seed_credit_cards(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM credit_cards;")
    
    # Official issuer URLs mapped to each of the 97 cards
    raw_cards = [
        # AMEX
        ("american-express-gold-charge-credit-card", "American Express Gold Charge Card", "American Express", "Amex", "Charge", "https://www.americanexpress.com/in/credit-cards/gold-card/", 1000, 4500, 0, 600000, 720, "Membership Rewards on all spends", "Reward Points", 2.5, 0.5, 0, 0, "No expiry", "", 3.0, 3.0, 4.0, 1.0, 2.0, 2.0, 4.0, 2.0, 4.0, "4,000 Bonus Points", 10000, "1,000 Bonus Points", 4000, "N/A", 0, "1% Waiver at HPCL", "Fine Dining Privileges", "N/A", "Travel Vouchers", "Hotel Upgrades", "Shopping Vouchers", "N/A", "Travel Insurance"),
        ("american-express-membership-rewards-credit-card", "Amex Membership Rewards Credit Card", "American Express", "Amex", "Rewards", "https://www.americanexpress.com/in/credit-cards/membership-rewards-card/", 1000, 4500, 150000, 350000, 680, "1,000 Bonus points monthly", "Reward Points", 2.0, 0.4, 0, 0, "No expiry", "", 2.0, 3.5, 2.5, 1.0, 2.0, 1.5, 3.5, 1.5, 3.0, "4,000 Bonus Points", 15000, "1,000 bonus points", 6000, "N/A", 0, "1% Waiver at HPCL", "Dining Discounts", "N/A", "Bonus Travel Points", "N/A", "E-Vouchers", "N/A", "Purchase Protection"),
        ("american-express-platinum-travel-credit-card", "Amex Platinum Travel Credit Card", "American Express", "Amex", "Travel", "https://www.americanexpress.com/in/credit-cards/platinum-travel-card/", 3500, 5000, 400000, 500000, 700, "Milestone Taj Vouchers", "Air Miles / Vouchers", 3.0, 0.5, 0, 0, "3 Years", "", 2.0, 3.0, 5.0, 1.0, 2.0, 1.0, 4.0, 1.5, 4.0, "10,000 Bonus Points", 15000, "Taj Voucher", 400000, "8 Lounge Visits/yr", 0, "1% Waiver at HPCL", "Dining Discounts", "N/A", "Bonus Miles", "Taj Gift Card", "Shopping Vouchers", "N/A", "Air Insurance"),
        ("american-express-smartearn-credit-card", "Amex SmartEarn Credit Card", "American Express", "Amex", "Entry-level Rewards", "https://www.americanexpress.com/in/credit-cards/smartearn-card/", 495, 495, 40000, 150000, 650, "10X Points on Flipkart, Amazon & Uber", "Reward Points", 1.5, 0.25, 0, 0, "No expiry", "", 3.0, 4.0, 3.0, 1.0, 1.0, 1.0, 4.5, 1.0, 2.0, "₹500 Cashback", 10000, "Fee waiver on ₹40k spend", 40000, "N/A", 0, "1% Waiver at HPCL", "Dining Offers", "N/A", "Uber vouchers", "N/A", "Amazon/Flipkart Cashback", "N/A", "Zero Liability"),
        
        # AU Small Finance Bank
        ("au-vetta-credit-card", "AU Vetta Credit Card", "AU Small Finance Bank", "Visa", "Premium Lifestyle", "https://www.aubank.in/personal-banking/credit-cards/vetta-credit-card", 2999, 2999, 150000, 350000, 680, "10 Reward Points per ₹100 on Utility & Grocery", "Reward Points", 2.5, 0.25, 0, 0, "2 Years", "", 3.0, 4.0, 3.0, 2.0, 4.0, 4.0, 3.5, 2.0, 3.0, "Welcome vouchers worth ₹2,000", 10000, "₹1,000 Voucher", 100000, "1 Lounge Visit/Qtr", 0, "1% Fuel Waiver", "Dining discounts", "Movie BOGO offer", "Flight discounts", "Hotel booking perks", "Shopping Rewards", "Grocery Discounts", "Travel Insurance"),
        ("au-zenith-credit-card", "AU Zenith Credit Card", "AU Small Finance Bank", "Visa", "Super Premium", "https://www.aubank.in/personal-banking/credit-cards/zenith-credit-card", 7999, 7999, 500000, 800000, 740, "20 Reward Points per ₹100 on International", "Reward Points", 4.0, 0.25, 0, 0, "2 Years", "", 5.0, 4.0, 5.0, 2.0, 3.0, 3.0, 4.0, 3.0, 5.0, "Welcome vouchers worth ₹5,000", 25000, "10,000 Bonus Points", 200000, "4 Lounge Visits/Qtr", 0, "1% Fuel Waiver", "Fine dining privileges", "2 Free Movie Tickets", "Airport Meet & Greet", "Luxury Hotel Stays", "Global Luxuries", "N/A", "Medical Cover"),

        # AXIS BANK
        ("axis-ace-credit-card", "Axis Bank ACE Credit Card", "Axis Bank", "Visa", "Cashback", "https://www.axisbank.com/retail/cards/credit-card/ace-credit-card", 499, 499, 200000, 150000, 650, "5% Unlimited Cashback on Google Pay Bill Payments", "Cashback", 2.0, 1.0, 0, 0, "No expiry", "", 2.0, 2.0, 2.0, 2.0, 2.0, 5.0, 2.0, 2.0, 2.0, "500 Cashback", 500, "Fee waiver on ₹2 Lakhs spend", 200000, "4 Lounge Visits/yr", 0, "1% Fuel Waiver", "Dining Delights", "N/A", "N/A", "N/A", "Unlimited Cashback", "5% GPay Bill Cashback", "Personal Accident Cover"),
        ("axis-airtel-credit-card", "Axis Bank Airtel Credit Card", "Axis Bank", "Visa", "Co-Branded Cashback", "https://www.axisbank.com/retail/cards/credit-card/airtel-axis-bank-credit-card", 500, 500, 200000, 150000, 650, "25% Cashback on Airtel Bills; 10% on Swiggy & Zomato", "Cashback", 10.0, 1.0, 300, 0, "No expiry", "", 10.0, 2.0, 2.0, 1.0, 10.0, 25.0, 10.0, 1.0, 1.0, "Amazon Voucher ₹500", 500, "Fee waiver on ₹2 Lakhs spend", 200000, "4 Lounge Visits/yr", 0, "1% Fuel Waiver", "10% Cashback on Swiggy/Zomato", "N/A", "N/A", "N/A", "10% Cashback on BigBasket", "10% BigBasket Cashback", "N/A"),
        ("axis-atlas-credit-card", "Axis Bank Atlas Credit Card", "Axis Bank", "Visa", "Travel", "https://www.axisbank.com/retail/cards/credit-card/atlas-credit-card", 5000, 5000, 1500000, 600000, 720, "5 EDGE Miles per ₹100 on Airlines & Hotels", "Air Miles", 5.0, 1.0, 0, 0, "3 Years", "", 2.0, 2.0, 10.0, 1.0, 1.0, 1.0, 5.0, 2.0, 5.0, "5,000 EDGE Miles", 5000, "10,000 Bonus Miles", 300000, "12 Lounge Visits/yr", 0, "1% Fuel Waiver", "Dining Delights", "N/A", "Air Miles Transfer", "Hotel Discounts", "N/A", "N/A", "Air Accident Insurance"),
        ("axis-flipkart-credit-card", "Flipkart Axis Bank Credit Card", "Axis Bank", "Mastercard", "Cashback", "https://www.axisbank.com/retail/cards/credit-card/flipkart-axisbank-credit-card", 500, 500, 350000, 150000, 650, "5% Unlimited Cashback on Flipkart & Myntra", "Cashback", 1.5, 1.0, 0, 0, "No expiry", "", 1.5, 5.0, 1.5, 1.5, 1.5, 1.5, 5.0, 1.5, 1.5, "₹500 Flipkart Voucher", 500, "Fee waiver on ₹3.5 Lakhs spend", 350000, "4 Lounge Visits/yr", 0, "1% Fuel Waiver", "Dining Delights", "N/A", "Cleartrip discounts", "Cleartrip cashback", "5% Myntra Cashback", "N/A", "N/A"),
        ("axis-magnus-credit-card", "Axis Bank Magnus Credit Card", "Axis Bank", "Visa", "Super Premium", "https://www.axisbank.com/retail/cards/credit-card/magnus-card", 12500, 12500, 2500000, 1200000, 760, "35 EDGE Reward Points per ₹200", "Reward Points", 7.0, 0.2, 0, 0, "3 Years", "", 6.0, 6.0, 12.0, 1.0, 2.0, 2.0, 8.0, 4.0, 8.0, "Flight Voucher worth ₹12,500", 12500, "25,000 Bonus Points", 150000, "Unlimited Airport Lounge Access", 0, "1% Fuel Waiver", "Fine Dining 30% off", "BOGO Movie Ticket", "VIP Concierge", "Luxury Hotel Collection", "Premium Shopping Vouchers", "N/A", "Overseas Medical Cover"),
        ("axis-my-zone-credit-card", "Axis Bank MY ZONE Credit Card", "Axis Bank", "Visa", "Entertainment & Lifestyle", "https://www.axisbank.com/retail/cards/credit-card/my-zone-credit-card", 500, 500, 200000, 120000, 640, "Buy 1 Get 1 Free Movie Ticket on Paytm Movies", "Reward Points / Discounts", 1.0, 0.2, 0, 0, "2 Years", "", 4.0, 2.0, 1.0, 1.0, 1.0, 1.0, 3.0, 1.0, 1.0, "SonyLIV Subscription", 500, "Fee waived on ₹2 Lakhs spend", 200000, "4 Lounge Visits/yr", 0, "1% Fuel Waiver", "Flat ₹120 off Swiggy", "BOGO Movie Ticket on Paytm", "N/A", "N/A", "AJIO discount coupons", "N/A", "N/A"),
        ("axis-privilege-credit-card", "Axis Bank Privilege Credit Card", "Axis Bank", "Visa", "Lifestyle", "https://www.axisbank.com/retail/cards/credit-card/privilege-credit-card", 1500, 1500, 600000, 350000, 680, "10 EDGE Points per ₹200", "Reward Points", 2.5, 0.2, 0, 0, "2 Years", "", 2.5, 5.0, 3.0, 1.0, 2.0, 2.0, 4.0, 2.0, 5.0, "Shopping Vouchers ₹5,000", 1500, "Fee waiver on ₹2.5 Lakhs spend", 250000, "2 Lounge Visits/Qtr", 0, "1% Fuel Waiver", "Dining Delights", "N/A", "Travel Vouchers", "N/A", "Retail Shopping Rewards", "N/A", "Air Accident Cover"),
        ("axis-reserve-credit-card", "Axis Bank Reserve Credit Card", "Axis Bank", "Mastercard", "Ultra Luxury", "https://www.axisbank.com/retail/cards/credit-card/axis-bank-reserve-credit-card", 50000, 50000, 5000000, 1500000, 780, "50 EDGE Points per ₹200 on International", "Reward Points", 12.0, 0.2, 0, 0, "No expiry", "", 10.0, 10.0, 15.0, 1.0, 4.0, 4.0, 12.0, 8.0, 15.0, "50,000 EDGE Points + ITC Voucher", 50000, "Fee waiver on ₹35 Lakhs spend", 3500000, "Unlimited Lounge Access", 0, "1% Fuel Waiver", "50% off Reserve Dining", "BOGO Movies & Events", "VIP Airport Transfer", "Luxury Hotel Stays", "Personal Shopper & Golf", "N/A", "Comprehensive Global Cover"),
        ("axis-select-credit-card", "Axis Bank Select Credit Card", "Axis Bank", "Visa", "Premium Lifestyle", "https://www.axisbank.com/retail/cards/credit-card/select-credit-card", 3000, 3000, 900000, 450000, 700, "10,000 EDGE Points on 1st txn", "Reward Points", 3.0, 0.2, 0, 0, "2 Years", "", 3.0, 6.0, 3.0, 1.0, 4.0, 2.0, 5.0, 2.0, 4.0, "Amazon Voucher ₹2,000", 3000, "Fee waived on ₹6 Lakhs spend", 600000, "2 Lounge Visits/Qtr", 0, "1% Fuel Waiver", "20% off BigBasket & Swiggy", "BOGO Movie Ticket", "Priority Pass", "Marriott Dining Discount", "Retail Shopping Rewards", "20% off BigBasket", "Air Cover"),
        ("axis-vistara-credit-card", "Axis Bank Vistara Credit Card", "Axis Bank", "Visa", "Air Travel", "https://www.axisbank.com/retail/cards/credit-card/axis-bank-vistara-credit-card", 1500, 1500, 500000, 250000, 660, "1 Free Economy Ticket on Joining", "Air Miles", 2.0, 1.0, 0, 0, "3 Years", "", 1.0, 1.0, 6.0, 1.0, 1.0, 1.0, 3.0, 1.0, 4.0, "1 Free Economy Air Ticket", 1500, "Milestone Flight Tickets", 150000, "2 Lounge Visits/Qtr", 0, "1% Fuel Waiver", "Dining discounts", "N/A", "Free Vistara Flight Tickets", "N/A", "N/A", "N/A", "Travel Insurance"),
        ("axis-vistara-infinite-credit-card", "Axis Bank Vistara Infinite Credit Card", "Axis Bank", "Visa", "Luxury Travel", "https://www.axisbank.com/retail/cards/credit-card/axis-bank-vistara-infinite-credit-card", 10000, 10000, 2000000, 1000000, 750, "1 Free Business Class Ticket on Joining", "Air Miles", 6.0, 1.0, 0, 0, "3 Years", "", 2.0, 2.0, 12.0, 1.0, 1.0, 1.0, 6.0, 2.0, 8.0, "1 Free Business Flight Ticket", 10000, "4 Business Class Tickets", 250000, "Unlimited Lounge Access", 0, "1% Fuel Waiver", "Fine Dining 25% off", "N/A", "Free Business Class Tickets", "Luxury Hotel Perks", "N/A", "N/A", "Baggage Delay Cover"),
        ("axis-vistara-signature-credit-card", "Axis Bank Vistara Signature Credit Card", "Axis Bank", "Visa", "Premium Travel", "https://www.axisbank.com/retail/cards/credit-card/axis-bank-vistara-signature-credit-card", 3000, 3000, 900000, 450000, 700, "1 Free Premium Economy Ticket on Joining", "Air Miles", 4.0, 1.0, 0, 0, "3 Years", "", 1.5, 1.5, 8.0, 1.0, 1.0, 1.0, 4.0, 1.5, 5.0, "1 Premium Economy Flight Ticket", 3000, "Milestone Premium Economy Tickets", 150000, "2 Lounge Visits/Qtr", 0, "1% Fuel Waiver", "Dining Delights 20% off", "N/A", "Free Flight Tickets", "N/A", "N/A", "N/A", "Travel Insurance"),

        # BANK OF BARODA (BOB)
        ("bob-easy-credit-card", "BOB Easy Credit Card", "Bank of Baroda", "Visa", "Entry-level Cashback", "https://www.bobcard.co.in/easy", 500, 500, 50000, 100000, 620, "5X Reward Points on Grocery & Movies", "Reward Points", 1.25, 0.25, 0, 0, "2 Years", "", 2.0, 2.0, 1.0, 1.0, 5.0, 2.0, 2.5, 1.0, 1.0, "1,000 Bonus Points", 5000, "Fee waived on ₹50k spend", 50000, "N/A", 0, "1% Fuel Waiver", "N/A", "5X Points on Movies", "N/A", "N/A", "N/A", "5X Points on Groceries", "Zero Liability Cover"),
        ("bob-energie-credit-card", "BOB ENERGIE Credit Card", "Bank of Baroda", "Rupay", "Fuel & Utility", "https://www.bobcard.co.in/energie", 499, 499, 50000, 120000, 630, "4% Savings on Fuel purchases at HPCL", "Fuel Rewards", 4.0, 0.25, 1000, 0, "2 Years", "", 1.0, 1.0, 1.0, 4.0, 1.0, 3.0, 2.0, 1.0, 1.0, "2,000 Bonus Points", 2000, "Fee waived on ₹50k spend", 50000, "N/A", 0, "1% Fuel Waiver", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "Accidental Insurance"),
        ("bob-eterna-credit-card", "BOB Eterna Credit Card", "Bank of Baroda", "Mastercard", "Premium Lifestyle", "https://www.bobcard.co.in/eterna", 2499, 2499, 1200000, 400000, 700, "3.75% Reward Rate on Travel, Dining & Online", "Reward Points", 3.75, 0.25, 0, 0, "2 Years", "", 3.75, 3.75, 3.75, 1.0, 1.0, 1.0, 3.75, 1.0, 3.75, "FitPass Pro Membership", 2500, "Fee waived on ₹2.5 Lakhs spend", 250000, "Unlimited Domestic Lounge", 0, "1% Fuel Waiver", "BOGO Movie Ticket on Paytm", "BOGO Movie Tickets", "3.75% Reward on Travel", "Hotel Booking Perks", "N/A", "N/A", "Air Accident Insurance"),
        ("bob-premier-credit-card", "BOB Premier Credit Card", "Bank of Baroda", "Visa", "Rewards & Lifestyle", "https://www.bobcard.co.in/premier", 1000, 1000, 400000, 250000, 660, "10 Reward Points per ₹100 on Travel & Dining", "Reward Points", 2.5, 0.25, 0, 0, "2 Years", "", 2.5, 2.5, 2.5, 1.0, 1.0, 1.0, 2.5, 1.0, 2.5, "2,000 Bonus Points", 1000, "Fee waived on ₹1.2 Lakhs spend", 120000, "1 Lounge Access/Qtr", 0, "1% Fuel Waiver", "Dining Perks", "Movie Discounts", "10 Points on Travel", "N/A", "Shopping Offers", "N/A", "Accident Insurance"),
        ("bob-select-credit-card", "BOB Select Credit Card", "Bank of Baroda", "Visa", "Shopping & Everyday", "https://www.bobcard.co.in/select", 750, 750, 300000, 150000, 640, "5X Points on Dining, Shopping & Utility", "Reward Points", 2.0, 0.25, 0, 0, "2 Years", "", 3.0, 3.0, 1.0, 1.0, 2.0, 3.0, 2.5, 1.0, 1.0, "1,000 Bonus Points", 750, "Fee waived on ₹75k spend", 75000, "N/A", 0, "1% Fuel Waiver", "5X Points on Fine Dining", "Movie Perks", "N/A", "N/A", "5X Points on Online Shopping", "N/A", "Zero Liability Cover"),

        # CITIBANK / AXIS CITI
        ("citi-cash-back-credit-card", "Citi Cash Back Credit Card", "Citi / Axis", "Visa", "Cashback", "https://www.axisbank.com/retail/cards/credit-card", 500, 500, 200000, 150000, 650, "5% Cashback on Movie Tickets & Utility Bills", "Cashback", 5.0, 1.0, 500, 0, "No expiry", "", 1.0, 1.0, 1.0, 1.0, 1.0, 5.0, 5.0, 0.5, 0.5, "₹500 Statement Credit", 500, "Fee waived on ₹30k spend", 30000, "N/A", 0, "N/A", "N/A", "5% Movie Cashback", "N/A", "N/A", "N/A", "N/A", "Lost Card Liability"),
        ("citi-indianoil-credit-card", "Citi IndianOil Credit Card", "Citi / Axis", "Mastercard", "Fuel", "https://www.axisbank.com/retail/cards/credit-card", 1000, 1000, 200000, 150000, 650, "4 Turbo Points per ₹150 at IndianOil", "Fuel Points", 2.67, 1.0, 0, 0, "No expiry", "", 0.5, 0.5, 0.5, 4.0, 0.5, 0.5, 1.0, 0.5, 0.5, "250 Turbo Points", 500, "Fee waived on ₹30k spend", 30000, "N/A", 0, "Fuel Surcharge Waiver at IOCL", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"),
        ("citi-premier-miles-credit-card", "Citi PremierMiles Credit Card", "Citi / Axis", "Visa", "Travel", "https://www.axisbank.com/retail/cards/credit-card", 3000, 3000, 800000, 400000, 700, "10 Miles per ₹100 on Airlines & Hotels", "Air Miles", 4.0, 0.4, 0, 0, "Never expire", "", 1.6, 1.6, 4.0, 0.5, 1.0, 1.0, 3.0, 1.6, 4.0, "10,000 PremierMiles", 3000, "3,000 Bonus Miles", 3000, "6 Lounge Visits/yr", 0, "1% Fuel Waiver", "Dining privileges", "N/A", "10 Miles on Air Bookings", "Hotel Booking Miles", "N/A", "N/A", "Air Accident Insurance"),
        ("citi-rewards-credit-card", "Citi Rewards Credit Card", "Citi / Axis", "Mastercard", "Rewards", "https://www.axisbank.com/retail/cards/credit-card", 1000, 1000, 300000, 150000, 650, "10 Reward Points per ₹125 at Department Stores", "Reward Points", 2.0, 0.25, 0, 0, "Never expire", "", 1.0, 4.0, 1.0, 1.0, 1.0, 1.0, 3.0, 1.0, 1.0, "1,500 Reward Points", 1000, "Fee waived on ₹30k spend", 30000, "N/A", 0, "1% Fuel Waiver", "Dining Rewards", "N/A", "N/A", "N/A", "10X Points on Fashion", "N/A", "Zero Lost Card Liability"),

        # FEDERAL BANK
        ("federal-celesta-credit-card", "Federal Bank Celesta Credit Card", "Federal Bank", "Visa", "Super Premium", "https://www.federalbank.co.in/celesta-credit-card", 5000, 5000, 1500000, 600000, 720, "2X Points on Travel; 3X on Dining & Electronics", "Reward Points", 3.0, 0.25, 0, 0, "3 Years", "", 4.0, 3.5, 4.0, 1.0, 2.0, 2.0, 3.5, 2.0, 4.5, "Amazon Voucher ₹3,000", 5000, "Fee waived on ₹3 Lakhs spend", 300000, "4 Lounge Visits/Qtr", 0, "1% Fuel Waiver", "BOGO Movie Ticket on BookMyShow", "BOGO Movie Tickets", "2X Points on Travel", "Hotel Privileges", "3X Points on Shopping", "N/A", "Travel Cover"),
        ("federal-signet-credit-card", "Federal Bank Signet Credit Card", "Federal Bank", "Visa", "Lifestyle", "https://www.federalbank.co.in/signet-credit-card", 750, 750, 300000, 150000, 650, "3X Points on Electronics & Apparel", "Reward Points", 1.8, 0.25, 0, 0, "2 Years", "", 2.0, 3.0, 1.5, 1.0, 1.5, 1.5, 2.5, 1.0, 1.5, "Amazon Voucher ₹500", 750, "Fee waived on ₹75k spend", 75000, "2 Lounge Visits/Qtr", 0, "1% Fuel Waiver", "Dining privileges", "BOGO Movie Ticket", "N/A", "N/A", "3X Points on Apparel", "N/A", "Zero Lost Card Cover"),

        # HDFC BANK
        ("hdfc-business-regalia-credit-card", "HDFC Business Regalia Credit Card", "HDFC Bank", "Visa", "Business Premium", "https://www.hdfcbank.com/personal/pay/cards/credit-cards", 2500, 2500, 1200000, 500000, 700, "4 Reward Points per ₹150 on Business spends & Utilities", "Reward Points", 2.67, 0.5, 0, 0, "2 Years", "", 2.5, 2.5, 4.0, 1.0, 1.0, 4.0, 3.0, 2.0, 3.0, "2,500 Reward Points", 2500, "10,000 Bonus Points", 500000, "12 Domestic Lounge Visits", 0, "1% Fuel Waiver", "Good Food Trail Dining", "N/A", "Business Travel Vouchers", "Commercial Hotel Perks", "Tax Spend Rewards", "N/A", "Air Cover"),
        ("hdfc-diners-club-black-credit-card", "HDFC Diners Club Black Credit Card", "HDFC Bank", "Diners Club", "Super Premium", "https://www.hdfcbank.com/personal/pay/cards/credit-cards/diners-black", 10000, 10000, 2500000, 1200000, 760, "5 Reward Points per ₹150; Up to 10X on SmartBuy", "Reward Points", 3.33, 1.0, 0, 0, "3 Years", "", 5.0, 10.0, 10.0, 1.0, 3.0, 3.0, 10.0, 3.33, 5.0, "Club Marriott & Club Vistara Gold", 10000, "10,000 Bonus Points", 400000, "Unlimited Worldwide Lounge Access", 0, "1% Fuel Waiver", "1+1 Fine Dining", "BOGO Movie Ticket on BookMyShow", "10X SmartBuy Flights & Hotels", "Luxury Hotel Collection", "10X SmartBuy Shopping", "N/A", "Medical Emergency Cover"),
        ("hdfc-diners-club-miles-credit-card", "HDFC Diners Club Miles Credit Card", "HDFC Bank", "Diners Club", "Travel", "https://www.hdfcbank.com/personal/pay/cards/credit-cards", 1000, 1000, 500000, 250000, 660, "4 Reward Points per ₹150; 1:1 air miles transfer", "Air Miles", 2.67, 1.0, 0, 0, "2 Years", "", 1.5, 1.5, 5.0, 1.0, 1.0, 1.0, 3.0, 1.5, 4.0, "1,000 Reward Points", 1000, "Fee waived on ₹1 Lakh spend", 100000, "6 Worldwide Lounge Visits", 0, "1% Fuel Waiver", "Good Food Trail", "N/A", "1:1 Air Miles Conversion", "Hotel Discounts", "N/A", "N/A", "Travel Insurance"),
        ("hdfc-diners-club-privilege-credit-card", "HDFC Diners Club Privilege Credit Card", "HDFC Bank", "Diners Club", "Premium Lifestyle", "https://www.hdfcbank.com/personal/pay/cards/credit-cards", 2500, 2500, 900000, 450000, 700, "4 Reward Points per ₹150; 5X Points on Swiggy & Zomato", "Reward Points", 2.67, 0.5, 0, 0, "2 Years", "", 5.0, 4.0, 4.0, 1.0, 2.0, 2.0, 5.0, 2.0, 3.0, "Swiggy One & Times Prime", 2500, "Fee waived on ₹3 Lakhs spend", 300000, "12 Lounge Visits/yr", 0, "1% Fuel Waiver", "5X Points on Swiggy", "BOGO Movie Ticket on BookMyShow", "SmartBuy Flight Discounts", "Hotel Savings", "Shopping Vouchers", "N/A", "Air Cover"),
        ("hdfc-indianoil-credit-card", "HDFC IndianOil Credit Card", "HDFC Bank", "Rupay", "Fuel & Grocery", "https://www.hdfcbank.com/personal/pay/cards/credit-cards", 500, 500, 150000, 100000, 620, "5% Fuel Points at IndianOil; 5% on Grocery & Bills", "Fuel Points", 5.0, 0.96, 250, 0, "2 Years", "", 1.0, 1.0, 1.0, 5.0, 5.0, 5.0, 2.0, 1.0, 1.0, "500 Fuel Points", 500, "Fee waived on ₹50k spend", 50000, "N/A", 0, "Fuel Waiver at IndianOil", "N/A", "N/A", "N/A", "N/A", "N/A", "5% Grocery Cashback", "Zero Liability Cover"),
        ("hdfc-indigo-ka-ching-6e-rewards-credit-card", "HDFC 6E Rewards - IndiGo Credit Card", "HDFC Bank", "Visa", "Air Travel", "https://www.hdfcbank.com/personal/pay/cards/credit-cards", 700, 700, 300000, 150000, 640, "2.5% 6E Rewards on IndiGo Ticket Bookings", "Air Miles", 2.5, 1.0, 0, 0, "2 Years", "", 1.5, 1.0, 2.5, 1.0, 1.5, 1.0, 2.0, 1.0, 2.0, "1 Free Flight Voucher ₹1,500", 700, "Fee waived on ₹1 Lakh spend", 100000, "N/A", 0, "1% Fuel Waiver", "1.5% Rewards on Dining", "N/A", "Free IndiGo Voucher + Priority Check-in", "N/A", "N/A", "N/A", "N/A"),
        ("hdfc-indigo-ka-ching-6e-xl-credit-card", "HDFC 6E Rewards XL - IndiGo Credit Card", "HDFC Bank", "Visa", "Premium Air Travel", "https://www.hdfcbank.com/personal/pay/cards/credit-cards", 2500, 2500, 800000, 350000, 680, "5% 6E Rewards on IndiGo Ticket Bookings", "Air Miles", 5.0, 1.0, 0, 0, "2 Years", "", 3.0, 2.0, 5.0, 1.0, 3.0, 2.0, 3.0, 2.0, 4.0, "1 Free Flight Voucher ₹3,000", 2500, "Fee waived on ₹2.5 Lakhs spend", 250000, "8 Lounge Visits/yr", 0, "1% Fuel Waiver", "3% Rewards on Dining", "3% Rewards on Entertainment", "Free Flight Voucher & Seat Selection", "N/A", "N/A", "3% Rewards on Groceries", "Air Cover"),
        ("hdfc-infinia-credit-card", "HDFC Infinia Credit Card Metal Edition", "HDFC Bank", "Visa", "Super Premium Metal", "https://www.hdfcbank.com/personal/pay/cards/credit-cards/infinia-credit-card", 12500, 12500, 4500000, 1500000, 780, "5 Reward Points per ₹150 (3.3% base); Up to 10X on SmartBuy", "Reward Points", 3.33, 1.0, 0, 0, "3 Years", "", 5.0, 10.0, 10.0, 1.0, 3.33, 3.33, 10.0, 3.33, 5.0, "12,500 Reward Points + Club Marriott", 12500, "Fee waived on ₹10 Lakhs spend", 1000000, "Unlimited Priority Pass Worldwide", 0, "1% Fuel Waiver", "1+1 Buffet at Luxury Hotels", "1+1 Movies on BookMyShow", "10X SmartBuy Flights & Hotels", "ITC Complimentary Night", "10X Apple & Shopping", "N/A", "Medical Cover & Air Cover"),
        ("hdfc-irctc-credit-card", "HDFC IRCTC Credit Card", "HDFC Bank", "Rupay", "Train Travel", "https://www.hdfcbank.com/personal/pay/cards/credit-cards/irctc-credit-card", 500, 500, 150000, 100000, 620, "5 Reward Points per ₹100 on IRCTC Ticketing", "Reward Points", 5.0, 0.25, 0, 0, "2 Years", "", 1.0, 1.0, 5.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, "₹500 IRCTC Ticket Voucher", 500, "Fee waived on ₹1 Lakh spend", 100000, "4 Railway Lounge Access", 0, "1% Fuel Waiver", "N/A", "N/A", "5% Points on IRCTC Train Bookings", "N/A", "N/A", "N/A", "Accidental Death Insurance"),
        ("hdfc-millennia-credit-card", "HDFC Millennia Credit Card", "HDFC Bank", "Visa", "Cashback", "https://www.hdfcbank.com/personal/pay/cards/credit-cards/millennia-credit-card", 1000, 1000, 300000, 150000, 660, "5% CashBack on Amazon, Flipkart, Swiggy, Zomato, BookMyShow, Myntra, Uber", "Cashback", 5.0, 1.0, 1000, 0, "1 Year", "", 5.0, 5.0, 5.0, 1.0, 1.0, 1.0, 5.0, 1.0, 1.0, "1,000 CashPoints", 1000, "Fee waived on ₹1 Lakh spend", 100000, "4 Lounge Visits/yr", 0, "1% Fuel Waiver", "5% Cashback on Swiggy & Zomato", "5% Cashback on BookMyShow", "5% Cashback on Uber cab rides", "N/A", "5% Cashback on Amazon & Flipkart", "1% Cashback on offline", "Accidental Cover"),
        ("hdfc-moneyback-credit-card", "HDFC MoneyBack Credit Card", "HDFC Bank", "Visa", "Entry-level Rewards", "https://www.hdfcbank.com/personal/pay/cards/credit-cards", 500, 500, 150000, 100000, 620, "2 Reward Points per ₹150; 2X points online", "Reward Points", 1.33, 0.2, 0, 0, "2 Years", "", 1.33, 2.66, 1.33, 1.0, 1.33, 1.33, 2.66, 1.33, 1.33, "500 Reward Points", 500, "Fee waived on ₹50k spend", 50000, "N/A", 0, "1% Fuel Waiver", "Dining discounts", "N/A", "N/A", "N/A", "Double reward points online", "N/A", "Zero Liability Cover"),
        ("hdfc-moneyback-plus-credit-card", "HDFC MoneyBack+ Credit Card", "HDFC Bank", "Visa", "Rewards", "https://www.hdfcbank.com/personal/pay/cards/credit-cards", 500, 500, 200000, 120000, 630, "10X CashPoints on Amazon, Flipkart, Swiggy, BigBasket", "Cashback", 3.3, 0.25, 500, 0, "2 Years", "", 3.3, 3.3, 1.0, 1.0, 3.3, 1.0, 3.3, 1.0, 1.0, "500 CashPoints", 500, "Fee waived on ₹50k spend", 50000, "N/A", 0, "1% Fuel Waiver", "10X CashPoints on Swiggy", "N/A", "N/A", "N/A", "10X CashPoints on Amazon & Flipkart", "10X CashPoints on BigBasket", "Zero Liability Cover"),
        ("hdfc-regalia-credit-card", "HDFC Regalia Credit Card", "HDFC Bank", "Visa", "Premium Lifestyle", "https://www.hdfcbank.com/personal/pay/cards/credit-cards/regalia-gold-credit-card", 2500, 2500, 1200000, 450000, 700, "4 Reward Points per ₹150 spent; 10X points on SmartBuy", "Reward Points", 2.67, 0.5, 0, 0, "2 Years", "", 3.0, 5.0, 6.0, 1.0, 2.0, 2.0, 5.0, 2.67, 4.0, "2,500 Reward Points", 2500, "10,000 Bonus Points", 500000, "12 Lounge Visits/yr", 0, "1% Fuel Waiver", "Good Food Trail Privileges", "N/A", "SmartBuy Flight Savings", "Hotel Booking Perks", "SmartBuy Shopping Rewards", "N/A", "Air Accident Insurance"),
        ("hdfc-regalia-first-credit-card", "HDFC Regalia First Credit Card", "HDFC Bank", "Visa", "Mid-level Premium", "https://www.hdfcbank.com/personal/pay/cards/credit-cards", 1000, 1000, 600000, 250000, 660, "4 Reward Points per ₹150; Double points on Dining", "Reward Points", 2.67, 0.3, 0, 0, "2 Years", "", 4.0, 2.67, 3.0, 1.0, 1.0, 1.0, 3.5, 2.67, 4.0, "1,000 Reward Points", 1000, "Fee waived on ₹1 Lakh spend", 100000, "8 Lounge Access/yr", 0, "1% Fuel Waiver", "Double points on dining", "N/A", "Travel Vouchers", "N/A", "Shopping Points", "N/A", "Air Cover"),

        # ICICI BANK
        ("icici-amazon-pay-credit-card", "Amazon Pay ICICI Bank Credit Card", "ICICI Bank", "Visa", "Cashback", "https://www.icicibank.com/personal-banking/cards/credit-card/amazon-pay-credit-card", 0, 0, 0, 0, 600, "5% Unlimited Cashback on Amazon; 2% on Amazon Pay partners; Lifetime Free", "Cashback", 5.0, 1.0, 0, 0, "No expiry", "", 2.0, 5.0, 2.0, 2.0, 2.0, 2.0, 5.0, 1.0, 1.0, "₹1,500 Welcome Rewards", 0, "Lifetime Free Card", 0, "N/A", 0, "1% Fuel Waiver at all gas stations", "15% off Culinary Treats", "N/A", "Flight Cashback on Amazon Travel", "Hotel Cashback on Amazon", "5% Unlimited Shopping Cashback", "N/A", "Zero Liability Cover"),
        ("icici-coral-credit-card", "ICICI Bank Coral Credit Card", "ICICI Bank", "Visa", "Entry-level Lifestyle", "https://www.icicibank.com/personal-banking/cards/credit-card/coral-credit-card", 500, 500, 200000, 100000, 620, "2 Payback Points per ₹100; 25% off on BookMyShow and Inox", "Reward Points", 1.0, 0.25, 0, 0, "2 Years", "", 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.0, 1.0, "500 Payback Points", 500, "Fee waived on ₹1.5 Lakhs spend", 150000, "1 Lounge Visit/Qtr", 0, "1% Fuel Waiver at HPCL", "15% off Culinary Treats", "25% off BookMyShow & Inox", "N/A", "N/A", "N/A", "N/A", "Personal Accident Cover"),
        ("icici-emeralde-credit-card", "ICICI Bank Emeralde Credit Card", "ICICI Bank", "Mastercard", "Super Premium", "https://www.icicibank.com/personal-banking/cards/credit-card/emeralde-credit-card", 12000, 12000, 3000000, 1200000, 760, "4 Payback Points per ₹100; Unlimited Airport Lounge & Spa", "Reward Points", 4.0, 0.25, 0, 0, "2 Years", "", 4.0, 4.0, 6.0, 1.0, 2.0, 2.0, 5.0, 2.0, 6.0, "12,000 Payback Points", 12000, "Fee waived on ₹15 Lakhs spend", 1500000, "Unlimited Lounge & Spa Access", 0, "1% Fuel Waiver", "Gourmet Dining", "BOGO Movie Ticket on BookMyShow", "Unlimited Lounge & Spa", "Luxury Hotel Discounts", "Exclusive Vouchers", "N/A", "Air Cover"),
        ("icici-emirates-skywards-sapphiro-credit-card", "ICICI Emirates Skywards Sapphiro Credit Card", "ICICI Bank", "Visa", "Air Travel Premium", "https://www.icicibank.com/personal-banking/cards/credit-card/emirates-skywards-sapphiro-credit-card", 10000, 10000, 2500000, 1000000, 750, "2.5 Skywards Miles per ₹100; Emirates Silver Tier", "Air Miles", 2.5, 1.0, 0, 0, "3 Years", "", 2.0, 2.0, 8.0, 1.0, 1.0, 1.0, 4.0, 2.0, 8.0, "10,000 Skywards Bonus Miles", 10000, "10,000 Bonus Miles", 1000000, "2 Intl & 4 Dom Lounge Visits/Qtr", 0, "1% Fuel Waiver", "Gourmet Dining", "BOGO Movie Ticket", "Free Emirates Flights", "Luxury Hotel Stays", "N/A", "N/A", "Overseas Medical Cover"),
        ("icici-hpcl-coral-credit-card", "ICICI Bank HPCL Coral Credit Card", "ICICI Bank", "Visa", "Fuel", "https://www.icicibank.com/personal-banking/cards/credit-card/hpcl-coral-credit-card", 199, 199, 50000, 100000, 620, "4% Cashback as Payback Points at HPCL pumps", "Fuel Points", 4.0, 0.25, 200, 0, "2 Years", "", 0.5, 0.5, 0.5, 4.0, 0.5, 0.5, 0.5, 0.5, 0.5, "₹200 Cashback on fuel", 200, "Fee waived on ₹50k spend", 50000, "N/A", 0, "2.5% Fuel Waiver at HPCL", "N/A", "25% off BookMyShow", "N/A", "N/A", "N/A", "N/A", "N/A"),
        ("icici-makemytrip-signature-credit-card", "ICICI MakeMyTrip Signature Credit Card", "ICICI Bank", "Visa", "Co-Branded Travel", "https://www.icicibank.com/personal-banking/cards/credit-card/makemytrip-signature-credit-card", 2500, 0, 0, 150000, 640, "₹1,500 My Cash + ₹2,500 MMT Voucher on Joining; 4 My Cash per ₹200", "Travel Cash", 3.0, 1.0, 0, 0, "1 Year", "", 2.0, 2.0, 5.0, 1.0, 1.0, 1.0, 3.0, 1.0, 3.0, "₹1,500 MMT My Cash + ₹2,500 Voucher", 2500, "Lifetime Free Card", 0, "2 Dom Lounge + 1 Railway Lounge/Qtr", 0, "1% Fuel Waiver", "15% off Culinary Treats", "BOGO Movie Ticket on BookMyShow", "MMT Flight Discounts", "MMT Hotel Cashbacks", "N/A", "N/A", "Accident Insurance"),
        ("icici-rubyx-credit-card", "ICICI Bank Rubyx Credit Card", "ICICI Bank", "Visa", "Dual Card Lifestyle", "https://www.icicibank.com/personal-banking/cards/credit-card/rubyx-credit-card", 3000, 2000, 600000, 350000, 680, "Dual Card (Visa + Amex) - 4 Payback Points per ₹100", "Reward Points", 2.0, 0.25, 0, 0, "2 Years", "", 2.0, 3.0, 3.0, 1.0, 1.5, 1.5, 4.0, 1.5, 3.0, "Vouchers worth ₹5,000", 3000, "Fee waived on ₹3 Lakhs spend", 300000, "2 Lounge Visits/Qtr", 0, "1% Fuel Waiver", "15% off Culinary Treats", "2 Free Movie Tickets on BookMyShow", "Golf Rounds 2/mo", "N/A", "Shopping Brand Vouchers", "N/A", "Air Cover"),
        ("icici-sapphiro-credit-card", "ICICI Bank Sapphiro Credit Card", "ICICI Bank", "Visa", "Premium Dual Card", "https://www.icicibank.com/personal-banking/cards/credit-card/sapphiro-credit-card", 6500, 3500, 1500000, 600000, 720, "Dual Card Advantage; 4 Payback Points on International", "Reward Points", 3.0, 0.25, 0, 0, "2 Years", "", 3.0, 5.0, 5.0, 1.0, 2.0, 2.0, 4.0, 2.0, 6.0, "Welcome Vouchers ₹10,000", 6500, "Fee waived on ₹6 Lakhs spend", 600000, "4 Dom & 2 Intl Lounge Visits/Qtr", 0, "1% Fuel Waiver", "15% off Culinary Treats", "BOGO Movie Ticket up to ₹500", "4 Golf Rounds/mo", "Luxury Hotel Vouchers", "Shopping Vouchers", "N/A", "Air Cover"),

        # IDFC FIRST BANK
        ("idfc-first-classic-credit-card", "IDFC FIRST Classic Credit Card", "IDFC FIRST Bank", "Visa", "Lifetime Free Rewards", "https://www.idfcfirstbank.com/credit-card/classic", 0, 0, 0, 0, 600, "10X Reward Points on spends above ₹20k/mo; 6X online; Lifetime Free", "Reward Points", 2.5, 0.25, 0, 0, "Never expire", "", 1.5, 4.0, 1.5, 1.0, 1.5, 1.5, 4.0, 1.5, 1.5, "Welcome Voucher ₹500", 0, "Lifetime Free Card", 0, "4 Railway Lounge/Qtr", 0, "1% Fuel Waiver", "20% off dining", "25% off movie tickets", "N/A", "N/A", "6X Points on Online Shopping", "N/A", "Personal Accident Insurance"),
        ("idfc-first-millennia-credit-card", "IDFC FIRST Millennia Credit Card", "IDFC FIRST Bank", "Visa", "Youth Lifetime Free", "https://www.idfcfirstbank.com/credit-card/millennia", 0, 0, 0, 0, 600, "10X Reward Points on spends > ₹20k/mo; 6X on Online spends; Lifetime Free", "Reward Points", 2.5, 0.25, 0, 0, "Never expire", "", 2.0, 4.5, 1.5, 1.0, 1.5, 1.5, 4.5, 1.5, 1.5, "Gift Voucher ₹500", 0, "Lifetime Free Card", 0, "4 Railway Lounge Visits/Qtr", 0, "1% Fuel Waiver", "20% off dining", "25% off movie tickets", "N/A", "N/A", "6X Points on E-commerce", "N/A", "Personal Accident Insurance"),
        ("idfc-first-private-credit-card", "IDFC FIRST Private Credit Card", "IDFC FIRST Bank", "Mastercard", "Ultra Premium Metal", "https://www.idfcfirstbank.com/credit-card/first-private", 50000, 50000, 5000000, 1500000, 780, "10X Reward Points on all spends; Zero forex markup", "Reward Points", 5.0, 0.25, 0, 0, "Never expire", "", 5.0, 5.0, 5.0, 2.0, 3.0, 3.0, 5.0, 3.0, 5.0, "200,000 Points + Taj Epicure", 50000, "Fee waived on ₹25 Lakhs spend", 2500000, "Unlimited Worldwide Lounge Access", 0, "1% Fuel Waiver", "50% off Fine Dining", "BOGO Movie Tickets on BookMyShow", "VIP Airport Fast Track", "Taj Luxury Hotel Privileges", "Unlimited Rewards", "N/A", "Comprehensive Overseas Cover"),
        ("idfc-first-select-credit-card", "IDFC FIRST Select Credit Card", "IDFC FIRST Bank", "Visa", "Premium Lifetime Free", "https://www.idfcfirstbank.com/credit-card/select", 0, 0, 0, 150000, 650, "10X Reward Points on spends > ₹20k/mo; 4 Domestic Lounge visits/Qtr; Lifetime Free", "Reward Points", 2.5, 0.25, 0, 0, "Never expire", "", 2.5, 4.0, 3.0, 1.0, 2.0, 2.0, 4.0, 2.0, 2.5, "Welcome Gift Voucher ₹500", 0, "Lifetime Free Card", 0, "4 Airport Lounge Access/Qtr", 0, "1% Fuel Waiver", "20% off dining", "BOGO Movie Ticket on Paytm", "Roadside Assistance Cover", "N/A", "6X Points on E-commerce", "N/A", "Personal Accident Insurance"),
        ("idfc-first-wealth-credit-card", "IDFC FIRST Wealth Credit Card", "IDFC FIRST Bank", "Visa", "Super Premium Lifetime Free", "https://www.idfcfirstbank.com/credit-card/wealth", 0, 0, 0, 350000, 680, "10X Reward Points on spends > ₹20k/mo; 1.5% Forex Fee; Lifetime Free", "Reward Points", 3.0, 0.25, 0, 0, "Never expire", "", 3.0, 4.0, 4.0, 1.0, 2.0, 2.0, 4.0, 2.0, 4.0, "Welcome Voucher ₹500 + Spa", 0, "Lifetime Free Card", 0, "4 Dom & 4 Intl Lounge Visits/Qtr", 0, "1% Fuel Waiver", "20% off dining", "BOGO Movie Tickets on Paytm", "Spa Sessions 2/Qtr", "Luxury Hotel Discounts", "10X Reward Points", "N/A", "Air Cover & Cancellation"),
        ("idfc-first-wow-credit-card", "IDFC FIRST WOW Credit Card", "IDFC FIRST Bank", "Visa", "FD Backed / Credit Builder", "https://www.idfcfirstbank.com/credit-card/wow", 0, 0, 0, 0, 300, "100% Guaranteed approval against FD; 4X Reward Points; 0% Forex Fee", "Reward Points", 1.0, 0.25, 0, 0, "Never expire", "", 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, "Welcome Cashback Perks", 0, "Lifetime Free Card", 0, "N/A", 0, "1% Fuel Waiver", "20% off dining", "Movie Discounts", "N/A", "N/A", "N/A", "N/A", "Zero Lost Card Liability"),

        # INDUSIND BANK
        ("indusind-aura-edge-credit-card", "IndusInd Bank Aura Edge Credit Card", "IndusInd Bank", "Mastercard", "Customized Rewards", "https://www.indusind.com/in/en/personal/cards/credit-cards/aura-edge-credit-card.html", 500, 500, 200000, 120000, 630, "Select customized reward plans: Party, Shopping, Home or Travel", "Reward Points", 2.0, 0.5, 0, 0, "2 Years", "", 4.0, 4.0, 4.0, 1.0, 2.0, 2.0, 3.0, 1.0, 1.0, "Welcome vouchers Bata, Pantaloons", 500, "Fee waived on ₹50k spend", 50000, "N/A", 0, "1% Fuel Waiver", "Customized Party Dining", "BookMyShow Movie Voucher", "Customized Travel Rewards", "N/A", "4X Points on Shopping Plan", "N/A", "Travel Insurance"),
        ("indusind-crest-credit-card", "IndusInd Bank Crest Credit Card", "IndusInd Bank", "Visa", "Ultra Luxury", "https://www.indusind.com/in/en/personal/cards/credit-cards/crest-credit-card.html", 50000, 10000, 3000000, 1200000, 760, "2.5 Reward Points per ₹100 on all spends", "Reward Points", 2.5, 1.0, 0, 0, "2 Years", "", 3.0, 3.0, 5.0, 1.0, 2.0, 2.0, 4.0, 2.5, 4.0, "Luxe Vouchers worth ₹50,000", 50000, "Fee waived on ₹20 Lakhs spend", 2000000, "Unlimited Lounge Access", 0, "1% Fuel Waiver", "Fine Dining 25% off", "BOGO Movie Tickets on BookMyShow", "Airport VIP Fast Track", "Oberoi / ITC Hotel Privileges", "N/A", "N/A", "Air Cover"),
        ("indusind-eazydiner-credit-card", "IndusInd Eazydiner Credit Card", "IndusInd Bank", "Visa", "Dining Co-Branded", "https://www.indusind.com/in/en/personal/cards/credit-cards/eazydiner-credit-card.html", 1999, 1999, 400000, 150000, 640, "25% Extra Discount on Eazydiner Pay + 10 Points per ₹100", "Dining Rewards", 6.0, 1.0, 0, 0, "2 Years", "", 10.0, 2.0, 2.0, 1.0, 1.0, 1.0, 4.0, 1.0, 2.0, "Eazydiner Prime Membership", 1999, "Fee waived on ₹2 Lakhs spend", 200000, "2 Lounge Access/Qtr", 0, "1% Fuel Waiver", "Guaranteed 25% to 50% off top restaurants", "BOGO Movie Ticket on BookMyShow", "N/A", "N/A", "N/A", "N/A", "Zero Liability Cover"),
        ("indusind-indulge-credit-card", "IndusInd Bank Indulge Credit Card", "IndusInd Bank", "Visa", "22K Gold Inlaid Luxury", "https://www.indusind.com/in/en/personal/cards/credit-cards/indulge-credit-card.html", 200000, 10000, 5000000, 1500000, 780, "Pure 22K Gold Inlaid Card; Private Jet & Yacht Access", "Reward Points", 3.0, 1.0, 0, 0, "No expiry", "", 4.0, 4.0, 6.0, 1.0, 2.0, 2.0, 5.0, 3.0, 6.0, "22K Gold Card + Luxe Vouchers ₹2 Lakhs", 200000, "Fee waived on ₹30 Lakhs spend", 3000000, "Unlimited Worldwide Lounge Access", 0, "1% Fuel Waiver", "Chef's Special Dining Experience", "BOGO Movie Ticket up to ₹1,000", "Private Jet Charter Discounts", "Luxury Hotels", "Personal Stylist", "N/A", "Global Insurance"),
        ("indusind-legend-credit-card", "IndusInd Bank Legend Credit Card", "IndusInd Bank", "Visa", "Premium Lifestyle", "https://www.indusind.com/in/en/personal/cards/credit-cards/legend-credit-card.html", 9999, 0, 0, 350000, 680, "1 Point weekday; 2 Points weekend; 4,000 Bonus Points", "Reward Points", 2.0, 1.0, 0, 0, "2 Years", "", 2.0, 3.0, 2.0, 1.0, 1.0, 1.0, 3.0, 1.0, 2.0, "Oberoi Hotel Voucher ₹10,000", 9999, "Lifetime Free (Only Joining Fee)", 0, "2 Lounge Access/Qtr", 0, "1% Fuel Waiver", "15% off dining", "BOGO Movie Ticket on BookMyShow", "Golf Rounds 1/Qtr", "Oberoi Hotel Vouchers", "N/A", "N/A", "Air Accident Insurance"),
        ("indusind-pinnacle-credit-card", "IndusInd Bank Pinnacle Credit Card", "IndusInd Bank", "Mastercard", "Super Premium", "https://www.indusind.com/in/en/personal/cards/credit-cards/pinnacle-credit-card.html", 12999, 0, 0, 500000, 720, "2.5 Reward Points per ₹100 on E-commerce & Travel; 1 Point = ₹1 Cash", "Reward Points", 2.5, 1.0, 0, 0, "2 Years", "", 2.0, 2.5, 2.5, 1.0, 1.0, 1.0, 2.5, 1.0, 2.5, "Welcome Vouchers Luxe, Postcard Hotels", 12999, "Lifetime Free (Only 1-time fee)", 0, "2 Lounge Visits/Qtr + Priority Pass", 0, "1% Fuel Waiver", "BOGO Dining offers", "BOGO Movie Tickets up to ₹500", "1 Golf Game/mo", "Postcard Hotel Vouchers", "2.5% Cash Return on E-commerce", "N/A", "Air Cover"),
        ("indusind-pioneer-heritage-metal-credit-card", "IndusInd Pioneer Heritage Metal Credit Card", "IndusInd Bank", "Mastercard", "Ultra Premium Metal", "https://www.indusind.com/in/en/personal/cards/credit-cards/pioneer-heritage-credit-card.html", 90000, 25000, 5000000, 1500000, 780, "2.5 Reward Points on International & 1.5 on Domestic; 0% Forex Fee", "Reward Points", 3.5, 1.0, 0, 0, "No expiry", "", 4.0, 4.0, 6.0, 1.0, 2.0, 2.0, 4.0, 2.0, 6.0, "Luxe Vouchers worth ₹90,000", 90000, "Fee waived on ₹25 Lakhs spend", 2500000, "Unlimited Lounge Access + 4 Guest Visits", 0, "1% Fuel Waiver", "Unlimited Fine Dining", "BOGO Movie Ticket up to ₹1,000", "Unlimited Golf Games & VIP Airport", "Oberoi Hotel Benefits", "Exclusive Shopping Vouchers", "N/A", "Air Cover"),

        # KOTAK MAHINDRA BANK
        ("kotak-811-credit-card", "Kotak 811 #DreamDifferent Credit Card", "Kotak Mahindra Bank", "Visa", "FD Backed / Beginner", "https://www.kotak.com/en/personal-banking/cards/credit-cards/811-dream-different-credit-card.html", 0, 0, 0, 0, 300, "2X Reward Points on online spends; Lifetime Free", "Reward Points", 1.0, 0.25, 0, 0, "2 Years", "", 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, "500 Welcome Points", 0, "Lifetime Free Card", 0, "N/A", 0, "1% Fuel Waiver", "N/A", "N/A", "N/A", "N/A", "2X Points on Online Purchases", "N/A", "Zero Lost Card Liability"),
        ("kotak-indigo-ka-ching-6e-rewards-credit-card", "Kotak 6E Rewards IndiGo Credit Card", "Kotak Mahindra Bank", "Visa", "Air Travel", "https://www.kotak.com/en/personal-banking/cards/credit-cards/indigo-6e-rewards-credit-card.html", 700, 700, 300000, 150000, 640, "2.5% 6E Rewards on IndiGo Ticket Bookings", "Air Miles", 2.5, 1.0, 0, 0, "2 Years", "", 1.5, 1.0, 2.5, 1.0, 1.5, 1.0, 2.0, 1.0, 2.0, "Free Flight Ticket Voucher ₹1,500", 700, "Fee waived on ₹1 Lakh spend", 100000, "N/A", 0, "1% Fuel Waiver", "1.5% Rewards on Dining", "N/A", "Free Flight Voucher & Priority Check-in", "N/A", "N/A", "N/A", "N/A"),
        ("kotak-indigo-ka-ching-6e-xl-credit-card", "Kotak 6E Rewards XL IndiGo Credit Card", "Kotak Mahindra Bank", "Visa", "Premium Air Travel", "https://www.kotak.com/en/personal-banking/cards/credit-cards/indigo-6e-rewards-xl-credit-card.html", 2500, 2500, 800000, 350000, 680, "5% 6E Rewards on IndiGo Ticket Bookings", "Air Miles", 5.0, 1.0, 0, 0, "2 Years", "", 3.0, 2.0, 5.0, 1.0, 3.0, 2.0, 3.0, 2.0, 4.0, "Free Flight Ticket Voucher ₹3,000", 2500, "Fee waived on ₹2.5 Lakhs spend", 250000, "8 Lounge Access/yr", 0, "1% Fuel Waiver", "3% Rewards on Dining", "3% Rewards on Entertainment", "Free Flight Voucher & Seat Selection", "N/A", "N/A", "3% Rewards on Groceries", "Air Cover"),
        ("kotak-mojo-credit-card", "Kotak Mojo Platinum Credit Card", "Kotak Mahindra Bank", "Visa", "Everyday Rewards", "https://www.kotak.com/en/personal-banking/cards/credit-cards/mojo-platinum-credit-card.html", 799, 799, 300000, 150000, 640, "2.5 Mojo Points per ₹100 on Online spends", "Reward Points", 2.5, 0.4, 0, 0, "2 Years", "", 1.0, 2.5, 1.0, 1.0, 1.0, 1.0, 2.5, 1.0, 1.0, "2,500 Mojo Points", 799, "Fee waived on ₹1 Lakh spend", 100000, "8 Lounge Access/yr", 0, "1% Fuel Waiver", "Dining discounts", "N/A", "N/A", "N/A", "2.5 Mojo Points on Online", "N/A", "Personal Accident Cover"),
        ("kotak-privy-league-signature-credit-card", "Kotak Privy League Signature Credit Card", "Kotak Mahindra Bank", "Visa", "Premium Wealth", "https://www.kotak.com/en/personal-banking/cards/credit-cards/privy-league-signature-credit-card.html", 2500, 2500, 1500000, 450000, 700, "5 Reward Points per ₹100; 4 Free PVR Tickets/Qtr", "Reward Points", 2.5, 0.25, 0, 0, "2 Years", "", 3.0, 3.0, 3.0, 1.0, 2.0, 2.0, 4.0, 2.0, 3.0, "Welcome Vouchers ₹2,500", 2500, "Fee waived on ₹5 Lakhs spend", 500000, "4 Lounge Access/Qtr", 0, "1% Fuel Waiver", "20% off fine dining", "4 Free PVR Movie Tickets/Qtr", "Travel Privileges", "Hotel Vouchers", "Shopping Vouchers", "N/A", "Air Cover"),
        ("kotak-pvr-gold-credit-card", "Kotak PVR Gold Credit Card", "Kotak Mahindra Bank", "Visa", "Entertainment", "https://www.kotak.com/en/personal-banking/cards/credit-cards/pvr-gold-credit-card.html", 499, 499, 200000, 120000, 630, "1 Free PVR Movie Ticket every month on spending ₹10k", "Movie Vouchers", 4.0, 1.0, 0, 0, "1 Year", "", 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, "PVR Movie Voucher ₹500", 499, "15% off PVR F&B", 0, "N/A", 0, "1% Fuel Waiver", "15% off PVR F&B", "Up to 24 Free PVR Movie Tickets/yr", "N/A", "N/A", "N/A", "N/A", "Zero Liability Cover"),
        ("kotak-pvr-platinum-credit-card", "Kotak PVR Platinum Credit Card", "Kotak Mahindra Bank", "Visa", "Entertainment Premium", "https://www.kotak.com/en/personal-banking/cards/credit-cards/pvr-platinum-credit-card.html", 999, 999, 400000, 150000, 640, "2 Free PVR Movie Tickets every month on spending ₹10k", "Movie Vouchers", 6.0, 1.0, 0, 0, "1 Year", "", 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, "2 Free PVR Movie Tickets", 999, "15% off PVR F&B", 0, "N/A", 0, "1% Fuel Waiver", "15% off PVR F&B", "Up to 24 Free PVR Platinum Tickets/yr", "N/A", "N/A", "N/A", "N/A", "Zero Liability Cover"),
        ("kotak-pvr-signature-credit-card", "Kotak PVR Signature Credit Card", "Kotak Mahindra Bank", "Visa", "Super Entertainment", "https://www.kotak.com/en/personal-banking/cards/credit-cards/pvr-signature-credit-card.html", 1499, 1499, 600000, 250000, 660, "2 Free PVR Movie Tickets every month on ₹10k spend", "Movie Vouchers", 8.0, 1.0, 0, 0, "1 Year", "", 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, "PVR Gift Voucher ₹1,500", 1499, "Fee waived on ₹1.5 Lakhs spend", 150000, "N/A", 0, "1% Fuel Waiver", "20% off PVR F&B", "24 Free PVR Signature Tickets/yr", "N/A", "N/A", "N/A", "N/A", "Zero Liability Cover"),
        ("kotak-royale-signature-credit-card", "Kotak Royale Signature Credit Card", "Kotak Mahindra Bank", "Visa", "Rewards & Travel", "https://www.kotak.com/en/personal-banking/cards/credit-cards/royale-signature-credit-card.html", 999, 999, 400000, 180000, 650, "4X Reward Points on Travel, Dining, International", "Reward Points", 2.0, 0.25, 0, 0, "2 Years", "", 4.0, 2.0, 4.0, 1.0, 1.0, 1.0, 2.0, 1.0, 4.0, "Welcome Voucher ₹1,000", 999, "Fee waived on ₹1 Lakh spend", 100000, "2 Lounge Access/Qtr", 0, "1% Fuel Waiver", "4X Points on Fine Dining", "Movie Perks", "4X Points on Flights & Hotels", "N/A", "Shopping Offers", "N/A", "Air Cover"),
        ("kotak-zen-signature-credit-card", "Kotak Zen Signature Credit Card", "Kotak Mahindra Bank", "Visa", "Shopping & Lifestyle", "https://www.kotak.com/en/personal-banking/cards/credit-cards/zen-signature-credit-card.html", 1500, 1500, 600000, 250000, 660, "10 Zen Points per ₹150 on Apparel, Jewellery, Malls", "Reward Points", 3.0, 0.25, 0, 0, "2 Years", "", 2.0, 6.0, 2.0, 1.0, 2.0, 2.0, 5.0, 2.0, 2.0, "1,500 Zen Points", 1500, "Fee waived on ₹1.5 Lakhs spend", 150000, "8 Lounge Access/yr", 0, "1% Fuel Waiver", "Dining Delights", "N/A", "N/A", "N/A", "10 Zen Points on Fashion & Malls", "N/A", "Accidental Death Cover"),

        # ONECARD
        ("onecard", "OneCard Credit Card (Metal)", "FPL / SBM / Federal", "Visa", "Metal Lifetime Free", "https://www.getonecard.app/", 0, 0, 0, 0, 600, "5X Rewards on top 2 spend categories every month; Lifetime Free Metal Card", "Reward Points", 2.0, 0.1, 0, 0, "Never expire", "", 5.0, 5.0, 5.0, 2.0, 2.0, 2.0, 5.0, 2.0, 2.0, "Welcome Bonus Points", 0, "Metal Card free for life", 0, "N/A", 0, "1% Fuel Waiver", "5X Rewards on Dining", "Movie Discounts", "5X Rewards on Travel", "N/A", "5X Rewards on E-Commerce", "N/A", "Zero Liability Cover"),

        # PUNJAB NATIONAL BANK (PNB)
        ("pnb-rupay-platinum-credit-card", "PNB RuPay Platinum Credit Card", "Punjab National Bank", "Rupay", "Government / Everyday", "https://www.pnbcard.in/rupay-platinum.html", 0, 0, 0, 0, 600, "300+ Welcome Points; RuPay UPI Linkage; Lifetime Free", "Reward Points", 1.0, 0.25, 0, 0, "2 Years", "", 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.5, 1.0, 1.0, "300 Reward Points", 0, "Lifetime Free Card", 0, "2 Railway Lounge Visits/Qtr", 0, "1% Fuel Waiver", "Dining Offers", "N/A", "N/A", "N/A", "RuPay UPI Payments Cashback", "N/A", "Accidental Insurance Cover"),

        # RBL BANK
        ("rbl-world-safari-credit-card", "RBL World Safari Credit Card", "RBL Bank", "Mastercard", "0% Forex Travel", "https://www.rblbank.com/product/credit-cards/world-safari-credit-card", 3000, 3000, 1000000, 350000, 680, "0% International Forex Markup Fee; 5 Travel Points per ₹100", "Travel Points", 4.0, 0.25, 0, 0, "2 Years", "", 2.0, 2.0, 5.0, 1.0, 1.0, 1.0, 3.0, 1.0, 5.0, "MakeMyTrip Voucher ₹3,000", 3000, "10,000 Bonus Travel Points", 250000, "2 Intl & 2 Dom Lounge Visits/Qtr", 0, "1% Fuel Waiver", "Dining privileges", "N/A", "0% Forex Markup Fee", "Hotel Vouchers", "N/A", "N/A", "Personal Travel Cover"),
        ("rbl-zomato-edition-black-credit-card", "RBL Zomato Edition Black Credit Card", "RBL Bank", "Mastercard", "Food Co-Branded", "https://www.rblbank.com/product/credit-cards/zomato-edition-black-credit-card", 1499, 1499, 400000, 180000, 650, "10% Edition Cash on Zomato & Blinkit; 5% on Dining", "Food Cash", 10.0, 1.0, 1500, 0, "1 Year", "", 10.0, 2.0, 2.0, 1.0, 2.0, 2.0, 3.0, 5.0, 2.0, "Zomato Gold Membership + ₹1,500 Cash", 1499, "Fee waived on ₹2.5 Lakhs spend", 250000, "2 Lounge Visits/Qtr", 0, "1% Fuel Waiver", "10% Edition Cash on Zomato & 5% Dining Out", "Birthday Special 10% Cash", "N/A", "N/A", "N/A", "N/A", "Zero Lost Card Cover"),
        ("rbl-zomato-edition-classic-credit-card", "RBL Zomato Edition Classic Credit Card", "RBL Bank", "Mastercard", "Food Co-Branded Entry", "https://www.rblbank.com/product/credit-cards/zomato-edition-classic-credit-card", 500, 500, 200000, 100000, 620, "5% Edition Cash on Zomato & Blinkit; 5% on Dining", "Food Cash", 5.0, 1.0, 750, 0, "1 Year", "", 5.0, 1.5, 1.5, 1.0, 1.5, 1.5, 2.0, 5.0, 1.5, "Zomato Gold Membership + ₹500 Cash", 500, "Fee waived on ₹1 Lakh spend", 100000, "N/A", 0, "1% Fuel Waiver", "5% Cash back on Zomato & Dining Out", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"),

        # SBI CARD
        ("sbi-aurum-credit-card", "SBI AURUM Credit Card", "SBI Card", "Visa", "Ultra Luxury", "https://www.sbicard.com/en/personal/credit-cards/lifestyle/aurum.page", 10000, 10000, 3000000, 1200000, 760, "4 Reward Points per ₹100; ₹1,500 Movie Vouchers monthly", "Reward Points", 4.0, 0.25, 0, 0, "3 Years", "", 4.0, 4.0, 6.0, 1.0, 2.0, 2.0, 5.0, 2.0, 5.0, "40,000 Reward Points (value ₹10,000)", 10000, "Luxury Brand Voucher ₹10,000", 500000, "Unlimited Lounge Access", 0, "1% Fuel Waiver", "Exclusive Fine Dining", "4 Free Movie Tickets every month", "Unlimited Airport Lounge & Flight Vouchers", "Taj & Marriott Upgrades", "Luxury Shopping Vouchers", "N/A", "Air Cover"),
        ("sbi-bpcl-octane-credit-card", "BPCL SBI Card Octane", "SBI Card", "Visa", "Fuel Super Premium", "https://www.sbicard.com/en/personal/credit-cards/fuel/bpcl-sbi-card-octane.page", 1499, 1499, 300000, 150000, 650, "7.25% Value Back (25 Reward Points per ₹100) on BPCL Fuel", "Fuel Rewards", 7.25, 0.25, 2500, 0, "2 Years", "", 1.0, 1.0, 1.0, 7.25, 1.0, 1.0, 2.0, 1.0, 1.0, "6,000 Reward Points (value ₹1,500)", 1499, "Fee waived on ₹2 Lakhs spend", 200000, "4 Lounge Access/yr", 0, "Fuel Surcharge Waiver at BPCL", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "Fraud Liability Cover"),
        ("sbi-cashback-credit-card", "CASHBACK SBI Card", "SBI Card", "Visa", "Pure Cashback", "https://www.sbicard.com/en/personal/credit-cards/cashback/cashback-sbi-card.page", 999, 999, 300000, 150000, 650, "5% Auto-Credited Cashback on ALL online shopping without merchant restrictions", "Cashback", 5.0, 1.0, 5000, 0, "No expiry", "Utilities, Fuel", 1.0, 5.0, 1.0, 1.0, 1.0, 1.0, 5.0, 1.0, 1.0, "₹999 Statement Credit", 999, "Fee waived on ₹2 Lakhs spend", 200000, "4 Lounge Access/yr", 0, "1% Fuel Waiver", "N/A", "N/A", "N/A", "N/A", "5% Unlimited Online Shopping Cashback", "1% Offline Cashback", "Zero Liability Cover"),
        ("sbi-elite-credit-card", "SBI Card ELITE", "SBI Card", "Visa", "Premium Lifestyle", "https://www.sbicard.com/en/personal/credit-cards/lifestyle/sbi-card-elite.page", 4999, 4999, 1500000, 450000, 700, "5X Reward Points on Dining & Department Stores; Free Movies ₹6,000/yr", "Reward Points", 2.5, 0.25, 0, 0, "2 Years", "", 5.0, 5.0, 3.0, 1.0, 5.0, 2.0, 4.0, 2.0, 5.0, "Welcome e-Voucher ₹5,000", 4999, "10,000 Bonus Points", 300000, "6 Intl & 8 Dom Lounge Visits/yr", 0, "1% Fuel Waiver", "5X Points on Dining", "Free Movie Tickets ₹500 every month", "Trident Hotel & Club Vistara", "Hotel Vouchers", "5X Points on Department Stores", "N/A", "Air Cover"),
        ("sbi-prime-credit-card", "SBI Card PRIME", "SBI Card", "Visa", "Lifestyle Rewards", "https://www.sbicard.com/en/personal/credit-cards/lifestyle/sbi-card-prime.page", 2999, 2999, 900000, 300000, 670, "20 Reward Points per ₹100 on Utility Bills; 10 Points on Dining, Grocery & Movies", "Reward Points", 3.0, 0.25, 0, 0, "2 Years", "", 4.0, 3.0, 3.0, 1.0, 4.0, 5.0, 4.0, 2.0, 3.0, "Welcome e-Voucher ₹3,000", 2999, "Pizza Hut Voucher ₹1,000", 50000, "4 Intl & 8 Dom Lounge Visits/yr", 0, "1% Fuel Waiver", "10 Points on Dining", "10 Points on Movie Tickets", "Club Vistara Silver Tier", "Trident Privilege Red", "Gift Vouchers ₹3,000", "10 Points on Groceries", "Air Cover"),
        ("sbi-simplyclick-credit-card", "SimplyCLICK SBI Card", "SBI Card", "Visa", "Online Shopping", "https://www.sbicard.com/en/personal/credit-cards/shopping/simplyclick-sbi-card.page", 499, 499, 200000, 100000, 620, "10X Reward Points on Apollo 24x7, BookMyShow, Cleartrip, Domino's, Myntra, Swiggy", "Reward Points", 2.5, 0.25, 0, 0, "2 Years", "", 2.5, 5.0, 5.0, 1.0, 1.0, 1.0, 5.0, 1.0, 1.0, "Amazon Gift Card ₹500", 499, "Cleartrip Voucher ₹2,000", 100000, "N/A", 0, "1% Fuel Waiver", "10X Points on Swiggy & Domino's", "10X Points on BookMyShow", "10X Points on Cleartrip Flights", "N/A", "10X Points on Myntra Shopping", "N/A", "Zero Liability Cover"),
        ("sbi-simplysave-credit-card", "SimplySAVE SBI Card", "SBI Card", "Visa", "Everyday Savings", "https://www.sbicard.com/en/personal/credit-cards/shopping/simplysave-sbi-card.page", 499, 499, 150000, 100000, 620, "10X Reward Points on Dining, Movies, Departmental Stores & Groceries", "Reward Points", 1.66, 0.25, 0, 0, "2 Years", "", 4.0, 4.0, 1.0, 1.0, 4.0, 1.0, 2.0, 1.0, 1.0, "2,000 Bonus Reward Points", 499, "Fee waived on ₹1 Lakh spend", 100000, "N/A", 0, "1% Fuel Waiver", "10X Points on Dining", "10X Points on Movies", "N/A", "N/A", "10X Points on Departmental Stores", "10X Points on Groceries", "Zero Liability Cover"),
        ("sbi-vistara-credit-card", "Club Vistara SBI Card", "SBI Card", "Visa", "Air Travel", "https://www.sbicard.com/en/personal/credit-cards/travel/club-vistara-sbi-card.page", 1499, 1499, 400000, 250000, 660, "1 Free Economy Flight Ticket on Joining", "Air Miles", 3.0, 1.0, 0, 0, "3 Years", "", 1.0, 1.0, 6.0, 1.0, 1.0, 1.0, 3.0, 1.0, 4.0, "1 Free Economy Air Ticket", 1499, "Milestone Flight Tickets", 125000, "4 Lounge Visits/yr", 0, "1% Fuel Waiver", "Dining Privileges", "N/A", "Free Vistara Flight Tickets", "N/A", "N/A", "N/A", "Air Cover"),
        ("sbi-vistara-prime-credit-card", "Club Vistara SBI Card PRIME", "SBI Card", "Visa", "Premium Air Travel", "https://www.sbicard.com/en/personal/credit-cards/travel/club-vistara-sbi-card-prime.page", 2999, 2999, 900000, 350000, 680, "1 Free Premium Economy Flight Ticket on Joining", "Air Miles", 4.0, 1.0, 0, 0, "3 Years", "", 1.5, 1.5, 8.0, 1.0, 1.0, 1.0, 4.0, 1.5, 5.0, "1 Premium Economy Flight Ticket", 2999, "Milestone Premium Economy Tickets", 150000, "8 Dom & 4 Intl Lounge Visits/yr", 0, "1% Fuel Waiver", "Dining Privileges", "N/A", "Free Premium Economy Tickets", "Hotel Discount Vouchers", "N/A", "N/A", "Air Cover"),

        # STANDARD CHARTERED
        ("standard-chartered-digismart-credit-card", "Standard Chartered DigiSmart Credit Card", "Standard Chartered", "Visa", "Digital Subscriptions", "https://www.sc.com/in/credit-cards/digismart-card/", 59, 59, 100000, 100000, 620, "20% off Myntra; 10% off Blinkit; 10% off Zomato; 20% off Yatra", "Discounts", 5.0, 1.0, 0, 0, "1 Month", "", 10.0, 20.0, 20.0, 1.0, 10.0, 5.0, 15.0, 2.0, 2.0, "Instant discount activation", 0, "Fee waived on ₹5k monthly spend", 5000, "N/A", 0, "1% Fuel Waiver", "10% off Zomato", "N/A", "20% off Yatra Flights & Hotels", "Hotel Discounts", "20% off Myntra fashion", "10% off Blinkit Grocery", "Zero Liability Cover"),
        ("standard-chartered-easemytrip-credit-card", "Standard Chartered EaseMyTrip Credit Card", "Standard Chartered", "Visa", "Co-Branded Travel", "https://www.sc.com/in/credit-cards/easemytrip-card/", 350, 350, 200000, 100000, 620, "20% flat discount on Hotels & 10% on Flights on EaseMyTrip", "Travel Discounts", 6.0, 1.0, 0, 0, "2 Years", "", 1.0, 1.0, 10.0, 1.0, 1.0, 1.0, 3.0, 1.0, 4.0, "₹350 Instant Discount", 350, "Fee waived on ₹50k spend", 50000, "2 Lounge Access/yr", 0, "1% Fuel Waiver", "Dining Perks", "N/A", "20% off Hotels & 10% off Flights on EaseMyTrip", "20% off Hotel Bookings", "N/A", "N/A", "Medical Cover"),
        ("standard-chartered-manhattan-credit-card", "Standard Chartered Manhattan Credit Card", "Standard Chartered", "Mastercard", "Supermarket Rewards", "https://www.sc.com/in/credit-cards/manhattan-platinum-card/", 999, 999, 400000, 180000, 650, "5% Cashback on Supermarket & Departmental Store purchases", "Cashback & Points", 5.0, 1.0, 500, 0, "2 Years", "", 1.0, 3.0, 1.0, 1.0, 5.0, 1.0, 3.0, 1.0, 1.0, "BookMyShow Vouchers ₹2,000", 999, "Fee waived on ₹1.2 Lakhs spend", 120000, "N/A", 0, "1% Fuel Waiver", "Dining privileges", "BookMyShow vouchers", "N/A", "N/A", "3X Points on Shopping", "5% Supermarket Cashback", "Zero Liability Cover"),
        ("standard-chartered-smart-credit-card", "Standard Chartered Smart Credit Card", "Standard Chartered", "Visa", "Cashback", "https://www.sc.com/in/credit-cards/smart-credit-card/", 499, 499, 200000, 100000, 620, "2% Cashback on all online spends; 1% on offline spends", "Cashback", 2.0, 1.0, 1000, 0, "No expiry", "", 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, "₹500 Cashback", 499, "Fee waived on ₹1 Lakh spend", 100000, "N/A", 0, "1% Fuel Waiver", "N/A", "N/A", "N/A", "N/A", "2% Cashback on Online Shopping", "1% Offline Cashback", "N/A"),
        ("standard-chartered-super-value-titanium-credit-card", "Standard Chartered Super Value Titanium", "Standard Chartered", "Mastercard", "Fuel & Utility", "https://www.sc.com/in/credit-cards/super-value-titanium-card/", 750, 750, 200000, 120000, 630, "5% Cashback on Fuel, Telecom & Utility bill payments", "Cashback", 5.0, 1.0, 500, 0, "2 Years", "", 1.0, 1.0, 1.0, 5.0, 1.0, 5.0, 1.0, 1.0, 1.0, "1,000 Reward Points", 750, "Fee waived on ₹90k spend", 90000, "N/A", 0, "1% Fuel Waiver at all gas stations", "N/A", "N/A", "N/A", "N/A", "N/A", "5% Utility Cashback", "Zero Liability Cover"),
        ("standard-chartered-ultimate-credit-card", "Standard Chartered Ultimate Credit Card", "Standard Chartered", "Mastercard", "Super Premium Rewards", "https://www.sc.com/in/credit-cards/ultimate-card/", 5000, 5000, 2400000, 600000, 720, "Flat 3.3% Reward Rate (5 Points per ₹150; 1 Point = ₹1 Cash)", "Reward Points", 3.33, 1.0, 0, 0, "3 Years", "", 3.33, 3.33, 5.0, 1.0, 2.0, 2.0, 3.33, 3.33, 5.0, "5,000 Reward Points (value ₹5,000)", 5000, "Fee waived on ₹6 Lakhs spend", 600000, "4 Dom & 4 Intl Lounge Visits/Qtr", 0, "1% Fuel Waiver", "Good Life Dining 25% off", "N/A", "Duty Free 5% Cashback", "Hotel Discounts", "3.33% Return on All Shopping", "N/A", "Air Cover"),

        # YES BANK
        ("yes-first-exclusive-credit-card", "YES FIRST Exclusive Credit Card", "YES Bank", "Mastercard", "Super Premium", "https://www.yesbank.in/personal-banking/yes-first/yes-first-exclusive-credit-card", 9999, 9999, 2400000, 800000, 740, "30 Reward Points per ₹200 on Subscription & Travel", "Reward Points", 3.75, 0.25, 0, 0, "3 Years", "", 3.75, 3.75, 6.0, 1.0, 2.0, 2.0, 5.0, 2.0, 5.0, "40,000 Reward Points", 9999, "Fee waived on ₹6 Lakhs spend", 600000, "Unlimited Lounge Access", 0, "1% Fuel Waiver", "1+1 Dining", "BOGO Movie Ticket up to ₹500", "Unlimited Lounge Access", "Luxury Hotel Discounts", "Shopping Vouchers", "N/A", "Air Cover"),
        ("yes-first-preferred-credit-card", "YES FIRST Preferred Credit Card", "YES Bank", "Mastercard", "Premium Lifestyle", "https://www.yesbank.in/personal-banking/yes-first/yes-first-preferred-credit-card", 2499, 2499, 1200000, 350000, 680, "16 Reward Points per ₹200; 2X Points on Travel & Dining", "Reward Points", 2.0, 0.25, 0, 0, "2 Years", "", 3.0, 2.0, 4.0, 1.0, 1.5, 1.5, 3.0, 1.5, 3.0, "10,000 Reward Points", 2499, "Fee waived on ₹2.5 Lakhs spend", 250000, "4 Dom & 4 Intl Lounge Visits/yr", 0, "1% Fuel Waiver", "2X Points on Dining", "BOGO Movie Ticket on Paytm", "2X Points on Travel", "Hotel Perks", "Shopping Points", "N/A", "Air Cover"),
        ("yes-private-credit-card", "YES Private Credit Card", "YES Bank", "Mastercard", "By-Invitation Ultra Luxury", "https://www.yesbank.in/personal-banking/yes-first/yes-private-prime-credit-card", 50000, 50000, 5000000, 1500000, 780, "By-Invitation Metal Card; 200,000 Welcome Points", "Reward Points", 5.0, 0.25, 0, 0, "No expiry", "", 5.0, 5.0, 8.0, 1.0, 3.0, 3.0, 6.0, 3.0, 8.0, "200,000 Points + Taj Epicure", 50000, "Fee waived on ₹25 Lakhs spend", 2500000, "Unlimited Lounge Access", 0, "1% Fuel Waiver", "Fine Dining & Chef Table", "BOGO Movie Tickets up to ₹1,000", "VIP Limousine Service", "Taj & Oberoi Ultra Luxe Perks", "Shopping Concierge", "N/A", "Air Cover")
    ]
    
    card_rows = []
    for c in raw_cards:
        img_filename = c[0] + ".png"
        img_path = f"assets/cards/{img_filename}"
        
        (cid, cname, bank, net, ctype, app_url, j_fee, a_fee, a_waiver, min_inc, min_cs, elig_notes,
         r_type, r_rate, r_val, r_cap, min_sp_r, r_exp, excl_cat,
         f_rew, s_rew, t_rew, fu_rew, g_rew, u_rew, on_rew, off_rew, int_rew,
         w_ben, w_sp, m_ben, m_sp, l_acc, l_sp, f_waiv, d_ben, mov_ben, tr_ben, hot_ben, shop_ben, groc_ben, ins_ben) = c
        
        card_rows.append((
            cid, cname, bank, net, ctype, img_path, app_url,
            j_fee, a_fee, a_waiver,
            min_inc, min_cs, elig_notes,
            r_type, r_rate, r_val, r_cap, min_sp_r, r_exp, excl_cat,
            f_rew, s_rew, t_rew, fu_rew, g_rew, u_rew, on_rew, off_rew, int_rew,
            w_ben, w_sp, m_ben, m_sp, l_acc, l_sp, f_waiv, d_ben, mov_ben, tr_ben, hot_ben, shop_ben, groc_ben, ins_ben,
            3.5, 500.0, 750.0, 3.5, 500.0, 100.0
        ))
        
    cursor.executemany("""
    INSERT INTO credit_cards (
        card_id, card_name, bank_name, card_network, card_type, image_path, apply_url,
        joining_fee, annual_fee, annual_fee_waiver_spend,
        minimum_income, minimum_credit_score, eligibility_notes,
        reward_type, reward_rate, reward_value, reward_cap, minimum_spend_for_rewards, reward_expiry, excluded_categories,
        food_reward, shopping_reward, travel_reward, fuel_reward, grocery_reward, utility_reward, online_reward, offline_reward, international_reward,
        welcome_benefit, welcome_spend_requirement, milestone_benefit, milestone_spend, lounge_access, lounge_spend_requirement, fuel_surcharge_waiver, dining_benefit, movie_benefit, travel_benefit, hotel_benefit, shopping_benefit, grocery_benefit, insurance_benefit,
        forex_markup, cash_withdrawal_fee, late_payment_fee, interest_rate, overlimit_fee, card_replacement_fee
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?,
        ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?
    );
    """, card_rows)
    
    conn.commit()

def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    seed_users(conn)
    seed_transactions(conn)
    seed_credit_cards(conn)
    conn.close()
    print("Database seeded with official issuer links for all 97 cards.")

if __name__ == "__main__":
    main()
