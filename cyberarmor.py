from flask import Flask
import whois
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN environment variable not set!")
    exit(1)

app = Flask(__name__)
@app.route("/")
def health_check():
    return "Bot is running!", 200  # Health check response

# Command: /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to Cyber Armor 🛡️ - Your Cyber Investigation Assistant!\n\n"
                              "I’m here to help you with cybersecurity checks and investigations. As your trusted assistant, I can perform the following tasks:\n\n"
                              "✅ Government Website Check: Ensure if a website is a legitimate government site (check for `.gov.in` or `.nic.in` domains).\n"
                              "🔍 WHOIS Lookup: Retrieve WHOIS information of any domain to know its registration details, including creation and expiration dates.\n\n"
                              "Commands you can use:\n"
                              "/start - Get an introduction to the bot.\n"
                              "/govcheck <URL> - Check if a website is a valid government site.\n"
                              "/whois <domain> - Fetch WHOIS information of a domain.\n\n"
                              "Feel free to try out any of the commands above! I’m here to assist you anytime. 🚀")

# Function to check if a website is a government site
def check_gov_website(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("❌ Please provide a URL: /govcheck example.com")
        return
    
    url = context.args[0]
    if url.endswith(".gov.in") or url.endswith(".nic.in"):
        update.message.reply_text(f"✅ {url} appears to be a genuine government website.")
    else:
        update.message.reply_text(f"⚠️ {url} does NOT seem to be a government website.")

# Function to perform WHOIS lookup
def whois_lookup(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("❌ Please provide a domain: /whois example.com")
        return
    
    domain = context.args[0]
    try:
        domain_info = whois.whois(domain)
        result = f"🔍 WHOIS Info for {domain}:\n"
        result += f"📅 Created: {domain_info.creation_date}\n" if domain_info.creation_date else ""
        result += f"⏳ Expiry: {domain_info.expiration_date}\n" if domain_info.expiration_date else ""
        result += f"🔗 Registrar: {domain_info.registrar}\n" if domain_info.registrar else ""
        update.message.reply_text(result)
    except Exception as e:
        update.message.reply_text(f"❌ Error fetching WHOIS info: {str(e)}")

# Main function to start the bot
def main():
    # Create an Updater instance
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("govcheck", check_gov_website))
    dp.add_handler(CommandHandler("whois", whois_lookup))

    # Start polling for updates
    updater.start_polling()

    # Run the bot until you stop it
    updater.idle()

# Run the bot
if __name__ == "__main__":
    from threading import Thread
    Thread(target=run_bot).start()  # Start bot in a separate thread
    app.run(host="0.0.0.0", port=8080)  # Start Flask app
