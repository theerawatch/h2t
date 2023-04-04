import image2text as i2t
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage as send_text, FlexSendMessage, ImageMessage
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot import (
    LineBotApi, WebhookHandler
)
from flask import Flask, request, abort
import json
import cv2
import os
import dotenv

dotenv.load_dotenv()


line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

app = Flask(__name__)


@app.route("/detect", methods=['POST'])
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    # print(user_id)
    line_bot_api.push_message(user_id, send_text(f'{user_id}'))


@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    message_id = event.message.id
    user_id = event.source.user_id
    line_bot_api.push_message(user_id, send_text(
        f"We already get your image, pls wait..."))
    messageContent = line_bot_api.get_message_content(message_id)
    fileName = f'img_{message_id}.jpg'
    with open(fileName, 'wb') as fd:
        for chunk in messageContent.iter_content():
            fd.write(chunk)
    img = cv2.imread(fileName)
    os.remove(fileName)
    result_dict = i2t.text_recognition(img)
    result = json.dumps(result_dict)
    line_bot_api.push_message(user_id, send_text(result))


if __name__ == "__main__":
    app.run(port=5000)
