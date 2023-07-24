import sqlite3
from twilio.rest import Client

# Replace with your Twilio account details
TWILIO_ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = 'YOUR_TWILIO_PHONE_NUMBER'

def create_contacts_table():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            status TEXT DEFAULT 'New'
        )
    ''')

    conn.commit()
    conn.close()

def add_contact(name, phone_number):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO contacts (name, phone_number) VALUES (?, ?)', (name, phone_number))
    conn.commit()
    conn.close()

def send_message(phone_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=message
    )

def move_through_sales_funnel():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()

    # Fetch contacts with 'New' status
    cursor.execute('SELECT * FROM contacts WHERE status = "New"')
    new_contacts = cursor.fetchall()

    for contact in new_contacts:
        name, phone_number, _ = contact
        # Move the contact to the next stage in the funnel (e.g., 'Contacted', 'Qualified', 'Closed')
        # Update the status in the database
        cursor.execute('UPDATE contacts SET status = "Contacted" WHERE phone_number = ?', (phone_number,))
        conn.commit()

        # Send a message to the contact
        message = f"Hello {name}, thank you for your interest! We'll be in touch soon."
        send_message(phone_number, message)

    conn.close()

if __name__ == "__main__":
    create_contacts_table()

    # Example usage - add contacts to the database
    add_contact('John Doe', '+1234567890')
    add_contact('Jane Smith', '+9876543210')

    # Move contacts through the sales funnel and send messages
    move_through_sales_funnel()
