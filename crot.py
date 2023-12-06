from flask import Flask, render_template, request, jsonify
import telebot
import requests
import os
from user_agents import parse  
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if TELEGRAM_TOKEN is None or TELEGRAM_CHAT_ID is None:
    raise ValueError("Please set TELEGRAM_TOKEN and TELEGRAM_CHAT_ID in your .env file.")

def huhusad_asw(message):
    user_details = ngelog_tele()
    log_message = f"""
Interaction details:
*User details:*
- *User Agent:* {user_details['user_agent']}
- *Browser:* {user_details['browser']}
- *OS:* {user_details['os']} {user_details['os_version']}
- *Device:* {user_details['device']}
- *IP Address:* {user_details['ip_address']}
- *Country:* {user_details['country']}
- *Time Use:* {user_details['timestamp']}
*Interaction in Website:* {message}
"""
    bot.send_message(TELEGRAM_CHAT_ID, log_message.strip(), parse_mode='Markdown') 

def ngelog_tele():
    user_agent_string = request.headers.get('User-Agent', '')
    user_agent = parse(user_agent_string)
    ip_address = request.remote_addr
    country = request.headers.get('CF-IPCountry', '')  
    return {
        'user_agent': user_agent_string,
        'browser': user_agent.browser.family,
        'browser_version': user_agent.browser.version_string,
        'os': user_agent.os.family,
        'os_version': user_agent.os.version_string,
        'device': user_agent.device.family,
        'ip_address': ip_address,
        'country': country,
        'timestamp': str(datetime.now())  
    }

@app.route("/")
def index():
    huhusad_asw("User accessed the home page.")
    return render_template("index.html")

@app.route("/api/bank", methods=["GET"])
def khintil():
    huhusad_asw("User accessed the bank API.")
    try:
        response = requests.get("https://api-rekening.lfourr.com/listBank")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"message": "Error fetching bank data", "error": str(e)}), 500

@app.route("/api/ewallet", methods=["GET"])
def asu_1():
    huhusad_asw("User accessed the e-Wallet API.")
    try:
        response = requests.get("https://api-rekening.lfourr.com/listEwallet")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"message": "Error fetching e-Wallet data", "error": str(e)}), 500

@app.route("/checkAccount", methods=["POST"])
def jemboed():
    huhusad_asw("User submitted a request to check an account.")
    data = request.get_json()
    layanan = data.get("layanan")
    bank_code = data.get("bankCode")
    account_number = data.get("accountNumber")

    api_url = (
        f"https://api-rekening.lfourr.com/getBankAccount?bankCode={bank_code}&accountNumber={account_number}"
        if layanan == "bank"
        else f"https://api-rekening.lfourr.com/getEwalletAccount?bankCode={bank_code}&accountNumber={account_number}"
    )
    try:
        response = requests.get(api_url)
        huhusad_asw(f"Account check response: {response.json()}")
        return jsonify(response.json())
    except Exception as e:
        huhusad_asw(f"Error checking account: {str(e)}")
        return jsonify({"message": "Error fetching account data", "error": str(e)}), 500

@bot.message_handler(func=lambda message: True)
def asukabeh(message):
    huhusad_asw(f"Received a message: {message.text}")
    pass

if __name__ == "__main__":
    import threading
    threading.Thread(target=app.run(host="0.0.0.0", debug=True, port=5000)).start()
    bot.polling()
