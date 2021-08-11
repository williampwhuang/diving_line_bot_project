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
# from linebot.models import (
#     FollowEvent, UnfollowEvent, MessageEvent, TextMessage, ImageMessage, 
#     AudioMessage, VideoMessage,TextSendMessage, TemplateSendMessage , PostbackEvent
# )
# from linebot.models import (
#     MessageAction, URIAction,
#     PostbackAction, DatetimePickerAction,
#     CameraAction, CameraRollAction, LocationAction,
#     QuickReply, QuickReplyButton
# )
from linebot.models import *
# from linebot.models.template import(ButtonsTemplate)
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

def for_experienced(event):
    if (event.message.text.find("@老手") != -1):
        print("Image Carousel")       
        for_experienced_template = TemplateSendMessage(
        alt_text = 'Image Carousel template ex01',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/weather.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '關於海象!',
                    text = 'About *advanced_weather1',
                    data = 'action=weather'
                )),
            ImageCarouselColumn(
                image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/secretbay.jpg?raw=true',
                action=PostbackTemplateAction(
                    label = '潛點分享',
                    text = 'About *secret_sharing',
                    data = 'action=share'
                )),
            ImageCarouselColumn(
                image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/meditation.jpg?raw=true',
                action=PostbackTemplateAction(
                    label = '關於訓練!',
                    text = 'About *training',
                    data = 'action=train'
                ))
        ]))
        line_bot_api.reply_message(event.reply_token, for_experienced_template)

    elif (event.message.text.find("*advanced_weather1") != -1):     
        advanced_weather1_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 2-1_1',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/weather.jpg?raw=true',
        title='海象與天氣',
        text='潛水之前如果能夠先評估天氣狀況，會讓你的潛水之旅更盡興，也更有心理準備，相同的天氣下，不同的海域會有不同的海象',
        actions=[
            MessageAction(
                label='海浪',
                text='*海浪',
            ),
            MessageAction(
                label='海流',
                text='*海流'
            ),
            MessageAction(
                label = '返回 上一層',
                text = '@老手'
            ),
            MessageAction(
                label = '下一頁',
                text = '*advanced_weather2'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, advanced_weather1_buttons_template_message)
    elif (event.message.text.find("*advanced_weather2") != -1):     
        advanced_weather2_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 2-1_2',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/weather.jpg?raw=true',
        title='海象與天氣',
        text='相同的天氣下，不同的海域會有不同的海象 (更多內容可至下方連結取得)',
        actions=[
            MessageAction(
                label='水溫',
                text='*水溫',
            ),
            MessageAction(
                label='能見度',
                text='*能見度'
            ),
            URIAction(
                label = '友站連結',
                uri = 'https://sites.google.com/site/freedivergroup/system/app/pages/sitemap/hierarchy'
            ),
            MessageAction(
                label = '返回 上一頁',
                text = '*advanced_weather1'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, advanced_weather2_buttons_template_message)

    elif (event.message.text.find("*海浪") != -1):     
        advanced_weather_wave_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 2-1-1',
        template=ButtonsTemplate(
        title='海浪',
        text='建議一開始選擇內凹式地形，如龍洞灣。如想在風勢下保有較佳的潛水體驗，盡量選擇風向與開口方向不同的海域，離島則選擇背風面',
        actions=[
            MessageAction(
                label = '返回 海象與天氣',
                text = '*advanced_weather1'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, advanced_weather_wave_buttons_template_message)
    elif (event.message.text.find("*海流") != -1):     
        advanced_weather_current_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 2-1-2',
        template=ButtonsTemplate(
        title='海流',
        text='除突出地形外，風平浪靜的海面於風向變動時仍未見波紋，很可能有湧升流或水平方向較強海流經過)',
        actions=[
            MessageAction(
                label = '返回 上一頁',
                text = '*advanced_weather1'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, advanced_weather_current_buttons_template_message)
    elif (event.message.text.find("*水溫") != -1):     
        advanced_weather_temp_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 2-1-3',
        template=ButtonsTemplate(
        title='水溫',
        text='失溫風險:人於海水中散熱速度為空氣的二十五倍，且水溫亦隨深度而劇烈變化，無防寒衣情況下要格外注意。另外，水溫突然變化亦可能為海流變化',
        actions=[
            MessageAction(
                label = '返回 上一頁',
                text = '*advanced_weather1'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, advanced_weather_temp_buttons_template_message)
    elif (event.message.text.find("*能見度") != -1):     
        advanced_weather_clear_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 2-1-4',
        template=ButtonsTemplate(
        title='能見度',
        text='深受浪況、潮汐、微生物等影響，於二樓高處判斷效果較佳，另外能見度大變常意味著海流劇變',
        actions=[
            MessageAction(
                label = '返回 上一頁',
                text = '*advanced_weather1'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, advanced_weather_clear_buttons_template_message)

    elif (event.message.text.find("*secret_sharing") != -1):     
        advanced_weather_clear_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 2-2',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/weather.jpg?raw=true',
        title='潛點分享',
        text='每處海域都是截然不同的環境，期待有天能嘗試所有的潛點，下附上推薦的潛點網站與個人經驗分享',
        actions=[
            URIAction(
                label = '友站連結-<海洋控>',
                uri = 'https://missmermaid.tw/diving-location-in-taiwan/',
            ),
            URIAction(
                label = '友站連結-<女子的海>',
                uri = 'https://msocean.com.tw/archives/category/freedive/divingspots'
            ),
            MessageAction(
                label = '望海點分享-日華親善の丘',
                text = '*shareview1'
            ),
            MessageAction(
                label = '返回 上一頁',
                text = '*advanced_weather1'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, advanced_weather_clear_buttons_template_message)

    elif (event.message.text.find("*shareview1") != -1):     
        advanced_weather_shareview_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 2-2-1',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/cliffview01.jpg?raw=true',
        title='望海點分享-日華親善の丘',
        text='恆春，可於google地圖上找到',
        actions=[
            MessageAction(
                label = '返回 上一頁',
                text = '*secret_sharing'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, advanced_weather_shareview_buttons_template_message)

    elif (event.message.text.find("*training") != -1):     
        training_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 2-3',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/badaiwan.jpg?raw=true',
        title='訓練',
        text='下提供常用訓練方式。持續訓練，期望一天能如阿古，跪坐八代灣沈船，眺望魚群',
        actions=[
            URIAction(
                label='呼吸拉伸-友站連結<VD Fd>',
                uri='https://www.youtube.com/watch?v=VUgIYCOlXTE&list=PLHv2dAiNOXYlrzR7tvDWEmK0rgcTk034E&index=5&ab_channel=VDFreedivingVDFreediving',
            ),
            URIAction(
                label = '靜態table-友站連結<VD Fd>',
                uri = 'https://www.vdfreediving.com/archives/4009'
            ),
            MessageAction(
                label = '返回 上一層',
                text = '@老手'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, training_buttons_template_message)