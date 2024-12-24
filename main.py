from flask import Flask, request, jsonify
from twilio.rest import Client
import random

app = Flask(__name__)

# إعدادات Twilio
TWILIO_ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = 'YOUR_TWILIO_PHONE_NUMBER'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# قاعدة بيانات بسيطة لتخزين الرموز
otp_database = {}

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    phone_number = data.get("phone_number")

    if not phone_number:
        return jsonify({"error": "رقم الهاتف مطلوب"}), 400

    # إنشاء رمز تحقق عشوائي
    otp = random.randint(1000, 9999)
    otp_database[phone_number] = otp

    # إرسال الرمز عبر SMS
    try:
        message = client.messages.create(
            body=f"رمز التحقق الخاص بك هو: {otp}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return jsonify({"message": "تم إرسال رمز التحقق"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json
    phone_number = data.get("phone_number")
    otp = data.get("otp")

    if not phone_number or not otp:
        return jsonify({"error": "رقم الهاتف ورمز التحقق مطلوبان"}), 400

    # التحقق من صحة الرمز
    if otp_database.get(phone_number) == int(otp):
        return jsonify({"message": "تم التحقق بنجاح. مرحبًا بك!"}), 200
    else:
        return jsonify({"error": "رمز التحقق غير صحيح"}), 400

if __name__ == '__main__':
    app.run(debug=True)
