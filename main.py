# Standard library imports
import time
from datetime import datetime
from urllib import request

# Third party imports
from bs4 import BeautifulSoup
from twilio.rest import Client

# User-defined constants
recipient_contact_number = "<your phone number>"  # Recipient's phone number for notifications
tickets_date = "2025-05-03"  # Desired date for ticket notifications, format "YYYY-MM-DD"
num_of_messages_to_send = 10  # Number of notification messages to send once tickets are available
interval_between_messages = 60  # Seconds between each notification message

# Twilio account details for sending SMS
account_sid = '<accountId>'  # Twilio account SID
auth_token = '<acountSecret>'  # Twilio auth token
client = Client(account_sid, auth_token)  # Twilio client initialization
twilio_contact_number = "<twillio phone number>"  # Twilio phone number used for sending SMS

# RCB tickets booking page URL
rcb_tickets_page_url = "https://shop.royalchallengers.com/ticket"

# Script execution control variables
tickets_available = False  # Flag to track ticket availability status
sent_messages_count = 0  # Counter for messages sent
fetch_status_delay = 300  # Delay in seconds for script re-execution if tickets are not available

# Email notification configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "<sender-gmail>"  # Replace with your Gmail address
sender_password = "<passwrd>"  # Replace with your Gmail app password
recipient_email = "<your-email>"  # Replace with the recipient's email address

def send_email_notification(subject: str, body: str):
    """
    Sends an email notification using Gmail's SMTP server.

    Parameters:
    - subject (str): The subject of the email.
    - body (str): The body content of the email.
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Email sent successfully.")
    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Failed to send email: {e}")

def getPage(url: str) -> request:
    """
    Fetches and returns the content of a webpage at a given URL.

    This function sends a GET request to the specified URL and returns the
    response object. It sets a custom User-Agent and other headers to simulate a
    browser request.

    Parameters:
    - url (str): The URL of the webpage to fetch.

    Returns:
    - request: A `urllib.request.urlopen` object containing the response from the
      webpage.
    """
    req = request.Request(
        url,
        headers={
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
    )
    return request.urlopen(req)


def get_dates_of_available_tickets(tickets_bsobj: BeautifulSoup) -> list:
    """
    Extracts and returns a list of dates when tickets are available from the parsed
    HTML content of the RCB tickets page.

    This function searches for <p> elements with a specific class attribute that
    contain the dates of available tickets, extracts the text content of these
    elements, and returns a list of these dates.

    Parameters:
    - tickets_bsobj (BeautifulSoup): A BeautifulSoup object parsed from the HTML content of the RCB
      tickets booking page. This object is used to navigate and search the HTML for
      elements that match specific criteria.

    Returns:
    - list: A list of strings, each representing a date when tickets are available.
    """
    dates = list()
    for p in tickets_bsobj.find_all("p", {"class": "css-1nm99ps"}):
        dates.append(p.text)
    return dates


while not tickets_available:
    tickets_page = getPage(rcb_tickets_page_url)
    tickets_bsobj = BeautifulSoup(tickets_page, features="html.parser")
    available_tickets_dates = get_dates_of_available_tickets(tickets_bsobj)

    for available_ticket_date in available_tickets_dates:
        date_obj = datetime.strptime(available_ticket_date, "%A, %b %d, %Y %I:%M %p")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        if formatted_date == tickets_date:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Tickets available. Sending notifications...")
            tickets_available = True

            # Send SMS notifications
            for message_num in range(num_of_messages_to_send):
                message = client.messages.create(
                    from_=twilio_contact_number,
                    body=f'The match tickets for {tickets_date} are available. Login to {rcb_tickets_page_url} to book the tickets immediately.',
                    to=recipient_contact_number
                )
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Message sent successfully - {message_num + 1} time(s)")
                sent_messages_count += 1

                if sent_messages_count == num_of_messages_to_send:
                    break

                time.sleep(interval_between_messages)

            # Send email notification
            email_subject = f"RCB Tickets Available for {tickets_date}"
            email_body = f"The match tickets for {tickets_date} are available. Login to {rcb_tickets_page_url} to book the tickets immediately."
            send_email_notification(email_subject, email_body)

    if not tickets_available:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Tickets not available. Retrying in {fetch_status_delay} seconds...")
        time.sleep(fetch_status_delay)
