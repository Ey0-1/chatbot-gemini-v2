import streamlit as st
import requests

# آدرس API و کلید
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
API_KEY = "YOUR API KEY"  # این کلید را محرمانه نگه دارید!

# رابط کاربری Streamlit
st.title("چت‌بات Gemini V2")
st.write("این یک رابط ساده برای چت‌بات با استفاده از مدل Gemini V2 است.")

# ذخیره‌ی تاریخچه‌ی گفتگو
if "chat" not in st.session_state:
    st.session_state.chat = []

# نمایش پیام‌های قبلی
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ورودی کاربر
user_text = st.chat_input("پیام خود را وارد کنید...")

# اگر کاربر پیامی وارد کرده باشد
if user_text:
    st.session_state.chat.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # آماده‌سازی درخواست به API
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY
    }

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": "تو یه چت‌بات عصبی و بی‌ادب هستی که فارسی حرف می‌زنه.\n" + user_text
                    }
                ]
            }
        ]
    }

    # ارسال درخواست و دریافت پاسخ
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        bot_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        bot_text = f"خطا در دریافت پاسخ از مدل: {e}"
        st.error(bot_text)

    # نمایش پاسخ چت‌بات
    st.session_state.chat.append({"role": "assistant", "content": bot_text})
    with st.chat_message("assistant"):
        st.markdown(bot_text)
