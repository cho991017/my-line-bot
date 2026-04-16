import os
import re
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# Render 환경변수에서 읽어오기
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# 화이트리스트 (여기에 본인 ID 추가)
white_list = ["U1234567890abcdef..."]

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_msg = event.message.text
    reply_token = event.reply_token

    # 욕설 패턴 감지
    bad_pattern = r"ㅅ[\s\d\W]*ㅂ|시[\s\d\W]*발"
    
    if re.search(bad_pattern, user_msg) and user_id not in white_list:
        line_bot_api.reply_message(
            reply_token,
            [
                TextSendMessage(text="↑ 욕 설 꾹 눌 러 서 보 내 기 취 소 ↑"),
                TextSendMessage(text="❗ 공 창 내 욕 설 금 지 ❗")
            ]
        )
    elif "/뚝증정식" in user_msg:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="진리채움 뚝증정식 배달 완료! 🍜"))

if __name__ == "__main__":
    # Render가 지정하는 포트를 사용하도록 설정
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
