# 引用套件
from flask import Flask, request, abort
# 引用line套件
from linebot import (
    LineBotApi, WebhookHandler
)
# 引用驗證消息用的套件
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, UnfollowEvent, MessageEvent, TextMessage, ImageMessage, 
    AudioMessage, VideoMessage,TextSendMessage, TemplateSendMessage , PostbackEvent
)
from linebot.models import (
    MessageAction, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    QuickReply, QuickReplyButton
)
from linebot.models import *
from linebot.models.template import(ButtonsTemplate)
# 時間停頓用
import time
# 圖片下載與上傳專用
import urllib.request
import os
# 建立日誌紀錄設定檔
# https://googleapis.dev/python/logging/latest/stdlib-usage.html
import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

line_bot_api = LineBotApi('請輸入token')


def for_dummies(event):
    if (event.message.text.find("@新手懶人包") != -1):     
        fro_dummies_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 1',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/babyseaturtle.jpg?raw=true',
        title='新手懶人包',
        text='以下資訊提供剛入門的你, 做為參考!',
        actions=[
            MessageAction(
                label='故事內容小檢討',
                text='''故事內容小檢討  
        #下水注意'''
            ),
            MessageAction(
                label='用品介紹!',
                text='#用品介紹',
            ),
            MessageAction(
                label = '各大潛水系統介紹',
                text = '#diving_system_intro'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, fro_dummies_buttons_template_message)

    elif (event.message.text.find("#下水注意") != -1):     
        notice_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 1-1',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/notice.jpg?raw=true',
        title='故事內容小檢討',
        text='玩過故事後, 來檢查哪裡出了錯吧!',
        actions=[
            MessageAction(
                label='下海前',
                text='#下海前1',
            ),
            MessageAction(
                label='沙地區',
                text='#沙地區'
            ),
            MessageAction(
                label = '礁岩區',
                text = '#礁岩區'
            ),
            MessageAction(
                label = '返程',
                text = '#返程'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, notice_buttons_template_message)

    elif (event.message.text.find("#下海前1") != -1):     
        before_sea1_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template-1-1-1_1',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/beachbush.jpg?raw=true',
        title='下海前',
        text='點選看看吧!',
        actions=[
            MessageAction(
                label='守時',
                text='#守時',
            ),
            MessageAction(
                label='絕不可獨自潛水',
                text='#Never Dive Alone'
            ),
            MessageAction(
                label = '下一頁',
                text = '#下海前2'
            ),
            MessageAction(
                label = '返回下水注意',
                text = '#下水注意'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, before_sea1_buttons_template_message)

    elif (event.message.text.find("#下海前2") != -1):     
        before_sea2_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template-1-1-1_2',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/beachbush.jpg?raw=true',
        title='下海前',
        text='點選看看吧!',
        actions=[
            MessageAction(
                label = '身體狀況',
                text = '#身體狀況'
            ),
            MessageAction(
                label = '返回下海前1',
                text = '#下海前1'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, before_sea2_buttons_template_message)

    elif (event.message.text.find("#守時") != -1):     
        time_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template-1-1-1-1',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/beachwaiting.jpg?raw=true',
        title='守時',
        text='潛水是團體活動, 不準時 除了浪費大家時間外, 還常因錯過了正確的下水時間導致危險增加、海況變差等!!',
        actions=[
            MessageAction(
                label='返回下海前',
                text='#下海前',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, time_buttons_template_message)

    elif (event.message.text.find("#Never Dive Alone") != -1):     
        nvda_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template-1-1-1-2',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/tide.jpg?raw=true',
        title='絕不可獨自潛水',
        text='在有適當潛伴的看護下，可將危險降到最低。（從來沒有人, 可以完全洞悉身體的大小毛病, 如果獨潛，任意的昏迷極可能溺水死亡，如果有 Buddy，只需要簡單的救援步驟就可以喚醒）',
        actions=[
            MessageAction(
                label='返回下海前',
                text='#下海前',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, nvda_buttons_template_message)

    elif (event.message.text.find("#海象") != -1):     
        weather_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template-1-1-1-3',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/tide.jpg?raw=true',
        title='海象注意',
        text='潛水之前評估天氣狀況，讓你的潛水之旅更盡興、心理準備，相同的天氣下，不同的海域會有不同的海象，請掌握該地的海浪、海流、水溫及能見度四大指標，以策安全）',
        actions=[
            MessageAction(
                label='返回下海前',
                text='#下海前',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, weather_buttons_template_message)LineBotApi

    elif (event.message.text.find("#身體狀況") != -1):     
        body_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template-1-1-1-4',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/startdiving.jpg?raw=true',
        title = '身體狀況檢視',
        text = '''睡眠不足、感到身體不適、女性生理期及個人疾病如癲癇、心血管疾病等等，皆將導致潛水的風險急遽增高，下水前請務必作好準備及評估''',
        actions = [
            MessageAction(
                label='返回下海前',
                text='#下海前',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, body_buttons_template_message)


    # elif (event.message.text.find("#用品介紹") != -1):     
    #     notice_buttons_template_message = TemplateSendMessage(
    #     alt_text='Buttons template-0',
    #     template=ButtonsTemplate(
    #     thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/sunset.jpg?raw=true',
    #     title='新手懶人包',
    #     text='以下資訊提供剛入門的你, 做為參考!',
    #     actions=[
    #         MessageAction(
    #             label='下水注意',
    #             text='''故事內容小檢討  
    #     #下水注意'''
    #         ),
    #         MessageAction(
    #             label='用品介紹!',
    #             text='#用品介紹',
    #         ),
    #         MessageAction(
    #             label = '各大潛水系統介紹',
    #             text = '#diving_system_intro'
    #         ),
    #     ]))
    #     line_bot_api.reply_message(event.reply_token, notice_buttons_template_message)

    # elif (event.message.text.find("#diving_system_intro") != -1):     
    #     notice_buttons_template_message = TemplateSendMessage(
    #     alt_text='Buttons template-0',
    #     template=ButtonsTemplate(
    #     thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/sunset.jpg?raw=true',
    #     title='新手懶人包',
    #     text='以下資訊提供剛入門的你, 做為參考!',
    #     actions=[
    #         MessageAction(
    #             label='用品介紹!',
    #             text='#用品介紹',
    #         ),
    #         MessageAction(
    #             label='下水注意',
    #             text='''故事內容小檢討  
    #     #下水注意'''
    #         ),
    #         MessageAction(
    #             label = '各大潛水系統介紹',
    #             text = '#diving_system_intro'
    #         ),
    #     ]))
    #     line_bot_api.reply_message(event.reply_token, notice_buttons_template_message)            
