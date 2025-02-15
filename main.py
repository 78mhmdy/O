from telethon import TelegramClient, events
import asyncio

# بيانات تسجيل الدخول إلى Telegram
API_ID = 25140031
API_HASH = 'a9308e99598c9eee9889a1badf2ddd2f'
PHONE_NUMBER = '+971569803058'

# قنوات المصدر والهدف (يمكنك إضافة أكثر من واحدة)
CHANNEL_MAP = {
    'mhmd2704': 'mahmood2794',  # بدون @
    'cointelegraph': 'crypto_N4',
    # أضف المزيد حسب الحاجة
}

# الكلمة المطلوب حذفها من الرسائل
WORD_TO_REMOVE = "@cointelegraph"  # قم بتغييرها حسب الحاجة

# تهيئة العميل
client = TelegramClient('session_name', API_ID, API_HASH)

async def send_code():
    """ إرسال كود التحقق عند تسجيل الدخول لأول مرة """
    try:
        print("Sending code...")
        await client.send_code_request(PHONE_NUMBER)
        code = input('Enter the code you received: ')
        await client.sign_in(PHONE_NUMBER, code)
    except Exception as e:
        print(f"Error during login: {e}")

@client.on(events.NewMessage(chats=list(CHANNEL_MAP.keys())))
async def send_message(event):
    """ معالجة الرسائل الجديدة وإعادة توجيهها بعد التعديل """
    try:
        source = event.chat.username or event.chat.id  # اسم القناة المصدر أو ID
        target = CHANNEL_MAP.get(source)  # البحث عن القناة الهدف

        if target:
            modified_message = event.message.text.replace(WORD_TO_REMOVE, "") if event.message.text else event.message.text
            await client.send_message(target, modified_message)
            print(f"Sent message from {source} to {target}: {modified_message[:50]}...")
        else:
            print(f"Source channel {source} not found in map.")

    except Exception as e:
        print(f"Error sending message: {e}")

async def main():
    """ تشغيل البوت """
    await client.start(PHONE_NUMBER)

    if not await client.is_user_authorized():
        await send_code()

    print("Bot is running...")
    await client.run_until_disconnected()

# تشغيل البوت
with client:
    client.loop.run_until_complete(main())