from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設定你的Line Bot的Channel Access Token與Channel Secret
line_bot_api = LineBotApi('kwZ6RMTHwbtWUgP/pBUlDI8RJYgidnH1Zjj6EQllHDSz3yY4CUBboNpv9e4JjyojM047SNVapVg1utpll2vut6rdREiJvGGcHnGXrVNSPIji51UHILc2rUOXmlNCJEg7Sm8/2/8xzQOlBB0eWJFQ6gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('405c12ebd48d02117433cde09f727044')

# Webhook路由
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 接收與回覆訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="你剛剛輸入了：" + message))

if __name__ == "__main__":
    app.run()