import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort

app = Flask(__name__)

# 使用環境變數取得Channel access token和Channel secret
channel_access_token = 'kwZ6RMTHwbtWUgP/pBUlDI8RJYgidnH1Zjj6EQllHDSz3yY4CUBboNpv9e4JjyojM047SNVapVg1utpll2vut6rdREiJvGGcHnGXrVNSPIji51UHILc2rUOXmlNCJEg7Sm8/2/8xzQOlBB0eWJFQ6gdB04t89/1O/w1cDnyilFU='
channel_secret = '405c12ebd48d02117433cde09f727044'

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    app.run()
