import os
from telethon.sync import TelegramClient

# Load API credentials from environment variables (NEVER hardcode them!)
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE')

# Session file name
SESSION_NAME = 'telegram_session'

def main():
    """Main function to connect to Telegram and read messages."""
    
    if not all([API_ID, API_HASH, PHONE_NUMBER]):
        print("Error: Please set TELEGRAM_API_ID, TELEGRAM_API_HASH, and TELEGRAM_PHONE environment variables.")
        return

    with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        client.start(phone=PHONE_NUMBER)
        
        if not client.is_user_authorized():
            client.send_code_request(PHONE_NUMBER)
            code = input('Enter the verification code: ')
            client.sign_in(PHONE_NUMBER, code)
        
        print("✅ Signed in successfully!\n")
        
        dialogs = client.get_dialogs()
        
        for dialog in dialogs:
            if dialog.is_user:
                entity = dialog.entity
                messages = client.get_messages(entity, limit=1)
                print(f"📩 Messages from: {entity.first_name}\n")
                for message in messages:
                    print(f"   {message.text}")
                print("-" * 40 + "\n")

if __name__ == "__main__":
    main()