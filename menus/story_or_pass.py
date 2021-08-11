from google.cloud import storage
from google.cloud import firestore
from flask import Request
from linebot import (
    LineBotApi, WebhookHandler
)
from flask import Flask, request, abort
import urllib.request
from linebot.models import (
    FollowEvent, UnfollowEvent, MessageEvent, TextMessage, ImageMessage, 
    AudioMessage, VideoMessage,TextSendMessage, TemplateSendMessage , PostbackEvent
)

#引入按鍵模板
from linebot.models.template import(
    ButtonsTemplate
)

line_bot_api = LineBotApi('DrKBizvbfKriwD55+lOR9uu/5mPEt+4Ty4gwp2pRlv9LDlPvpsl/nTUUPvpfvPo3INHx3VjDCEJPRa7l+kAtm1WwBuuow/7S0yRTMv2xw4t+65R2IU9p3y1urDuDc1l3vl8cAJsKmfEw7OjjHErIEQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ffed9c02546d9c25478cea4e006a41a8')

'''
alt_text: Line簡覽視窗所出現的說明文字
template: 所使用的模板
ButtonsTemplate: 按鍵模板
    thumbnail_image_url: 展示圖片
    title: 標題
    text: 說明文字
    actions: 模板行為所使用的行為
    data: 觸發postback後用戶回傳值，可以對其做商業邏輯處理
'''