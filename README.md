# Ticket Automator

## Overview
The Ticket Automator is a Python script designed to monitor the availability of tickets for a specific event and notify the user via SMS and email when tickets become available. The script continuously checks the ticket booking page and sends notifications once the desired tickets are found.

## Features
- Monitors ticket availability for a specified date.
- Sends SMS notifications using Twilio.
- Sends email notifications using Gmail's SMTP server.
- Configurable notification settings, including the number of messages and delay intervals.

## Prerequisites
- Python 3.6 or higher
- Required Python packages (listed in `requirements.txt`):
  - `beautifulsoup4`
  - `twilio`
- A Twilio account with a valid phone number.
- A Gmail account with app password enabled.

## Configuration
Before running the script, update the following constants in `main.py`:

1. **Recipient Contact Information**
   - `recipient_contact_number`: Replace `<your phone number>` with the recipient's phone number.
   - `recipient_email`: Replace `<your-email>` with the recipient's email address.

2. **Ticket Date**
   - `tickets_date`: Set the desired date for ticket notifications in the format `YYYY-MM-DD`.

3. **Twilio Account Details**
   - `account_sid`: Replace `<accountId>` with your Twilio Account SID.
   - `auth_token`: Replace `<acountSecret>` with your Twilio Auth Token.
   - `twilio_contact_number`: Replace with your Twilio phone number.

4. **Email Configuration**
   - `sender_email`: Replace `<sender-gmail>` with your Gmail address.
   - `sender_password`: Replace `<passwrd>` with your Gmail app password.

5. **Notification Settings**
   - `num_of_messages_to_send`: Set the number of SMS notifications to send.
   - `interval_between_messages`: Set the delay (in seconds) between each SMS notification.
   - `fetch_status_delay`: Set the delay (in seconds) for rechecking ticket availability.

## How to Run
1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the script:
   ```bash
   python main.py
   ```

## How It Works
1. The script fetches the ticket booking page using the `getPage` function.
2. It parses the HTML content using BeautifulSoup to extract available ticket dates.
3. If tickets for the specified date are found:
   - Sends SMS notifications using Twilio.
   - Sends an email notification.
4. If tickets are not available, the script waits for the specified delay and retries.

## Notes
- Ensure that the Twilio account and Gmail account are properly configured before running the script.
- The script uses a hardcoded URL for the ticket booking page. Update the `rcb_tickets_page_url` constant if the URL changes.

## Disclaimer
This script is provided as-is without any guarantees. Use it responsibly and ensure compliance with the terms of service of the ticket booking website and notification services.