#!/usr/bin/env python3

import asyncio
from telegram import Bot, error
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, time

# Configuration
BOT_TOKEN = "BOT_TOKEN"

async def send_content(bot, chat_id, message=None, photo_path=None):
    """Send message/photo with comprehensive error handling"""
    try:
        if photo_path:
            with open(photo_path, 'rb') as photo_file:
                if message:
                    await bot.send_photo(
                        chat_id=chat_id,
                        photo=photo_file,
                        caption=message
                    )
                else:
                    await bot.send_photo(
                        chat_id=chat_id,
                        photo=photo_file
                    )
        elif message:
            await bot.send_message(
                chat_id=chat_id,
                text=message
            )
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n✅ Successfully sent to {chat_id} at {timestamp}")
        return True
        
    except error.Unauthorized:
        print("\n❌ Error: Bot was blocked or chat doesn't exist")
    except error.BadRequest as e:
        print(f"\n❌ Telegram error: {e.message}")
    except FileNotFoundError:
        print(f"\n❌ Error: Photo file not found at '{photo_path}'")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    return False

def get_valid_input(prompt, input_type=str, optional=False):
    """Advanced input validation"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and not optional:
                raise ValueError("This field cannot be empty")
            
            if input_type == bool:
                return user_input.lower() in ('y', 'yes')
            elif input_type == time:
                hour, minute = map(int, user_input.split(':'))
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    raise ValueError
                return time(hour, minute)
            return input_type(user_input) if user_input else None
            
        except ValueError:
            print(f"⚠️ Invalid input. Please try again.")

async def main():
    """Main execution flow"""
    print("\n" + "="*50)
    print(" TELEGRAM CONTENT SCHEDULER ".center(50, "☆"))
    print("="*50)
    
    # Initialize components
    bot = Bot(token=BOT_TOKEN)
    scheduler = AsyncIOScheduler()
    
    # Get user inputs
    print("\n" + "-"*50)
    chat_id = get_valid_input("Recipient's Chat ID: ")
    message = get_valid_input("Message (optional, press Enter to skip): ", str, optional=True)
    
    send_photo = get_valid_input("Include photo? (y/n): ", bool)
    photo_path = None
    if send_photo:
        photo_path = get_valid_input("Full photo path (e.g., C:\\pics\\image.jpg): ")
    
    scheduled_time = get_valid_input("Send time (HH:MM 24h format or 'now'): ", time)
    
    # Schedule the content
    if scheduled_time == "now":
        print("\n⚡ Attempting to send now...")
        await send_content(bot, chat_id, message, photo_path)
    else:
        scheduler.add_job(
            send_content,
            'cron',
            args=[bot, chat_id],
            kwargs={'message': message, 'photo_path': photo_path},
            hour=scheduled_time.hour,
            minute=scheduled_time.minute
        )
        scheduler.start()
        
        print("\n" + "-"*50)
        print(f"⏰ Content scheduled for {scheduled_time.strftime('%I:%M %p')}")
        if photo_path:
            print(f"📷 Attached photo: {photo_path}")
        print("-"*50 + "\n")
        
        print("Note: Keep this window running for scheduled messages")
        print("Press Ctrl+C to exit\n")
        
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            scheduler.shutdown()
            print("\n🛑 Scheduler stopped gracefully")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n🔥 Critical error: {str(e)}")
        print("Please check your configuration and try again.")
