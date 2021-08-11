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
        #下水注意1'''
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

    elif (event.message.text.find("#下水注意1") != -1):     
        notice1_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 1-1_1',
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
                label = '返回 新手懶人包',
                text = '@新手懶人包'
            ),
            MessageAction(
                label = '下一頁',
                text = '#下水注意2'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, notice1_buttons_template_message)
    elif (event.message.text.find("#下水注意2") != -1):     
        notice2_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 1-1_2',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/notice.jpg?raw=true',
        title='故事內容小檢討',
        text='玩過故事後, 來檢查哪裡出了錯吧!',
        actions=[
            MessageAction(
                label = '礁岩區',
                text = '#礁岩區'
            ),
            MessageAction(
                label = '返程及其他',
                text = '#返程及其他'
            ),
            MessageAction(
                label = '返回上一頁',
                text = '#下水注意1'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, notice2_buttons_template_message)

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
                text='#Never_Dive_Alone'
            ),
            MessageAction(
                label = '下一頁',
                text = '#下海前2'
            ),
            MessageAction(
                label = '返回 下水注意',
                text = '#下水注意1'
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
                label = '海象',
                text = '#海象'
            ),
            MessageAction(
                label = '返回 上一頁',
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
                label='返回 下海前',
                text='#下海前1',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, time_buttons_template_message)
    elif (event.message.text.find("#Never_Dive_Alone") != -1):     
        nvda_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template-1-1-1-2',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/tide.jpg?raw=true',
        title='絕不可獨自潛水',
        text='在適當潛伴看護下，可將危險降到最低(如獨潛,意外的昏迷極可能溺水死亡,如有 Buddy,僅需簡單救援步驟即可喚醒）',
        actions=[
            MessageAction(
                label='返回 下海前',
                text='#下海前1',
            )
        ]))
        line_bot_api.reply_message(event.reply_token, nvda_buttons_template_message)
    elif (event.message.text.find("#海象") != -1):     
        weather_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template-1-1-1-3',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/tide.jpg?raw=true',
        title='海象注意',
        text='潛水前評估天氣狀況，請掌握該地的海浪、海流、水溫及能見度四大指標，以策安全',
        actions=[
            URIAction(
                label = '海象app推薦, 同時有強大的手機app功能',
                uri = 'https://www.windy.com/?0.659,105.469,4',
            ),
            MessageAction(
                label='返回 下海前',
                text='#下海前1',
            ),

        ]))
        line_bot_api.reply_message(event.reply_token, weather_buttons_template_message)
    elif (event.message.text.find("#身體狀況") != -1):     
        body_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template-1-1-1-4',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/startdiving.jpg?raw=true',
        title = '身體狀況檢視',
        text = '睡眠不足、身體不適、生理期或是個人疾病如心血管疾病等，導致潛水風險急遽增高，下水前作好準備及評估',
        actions = [
            MessageAction(
                label='返回 下海前',
                text='#下海前1',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, body_buttons_template_message)

    elif (event.message.text.find("#沙地區") != -1):     
        sand_area_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template-1-1-2',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/sand1.jpg?raw=true',
        title='沙地區',
        text='通常因無礁岩, 較無暗流, 也導致魚群種類較少, 點選看看吧!',
        actions=[
            MessageAction(
                label='海流',
                text='#海流',
            ),
            MessageAction(
                label = '返回下水注意',
                text = '#下水注意1'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, sand_area_buttons_template_message)

    elif (event.message.text.find("#海流") != -1):     
        sand_area_current_template_message = TemplateSendMessage(
        alt_text='Buttons template-1-1-2-1',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/sand1.jpg?raw=true',
        title = '海流',
        text = '由於沙地區景觀較一致, 海流導致位移時較難發現, 請務必注意',
        actions = [
            MessageAction(
                label='返回 下水注意',
                text='#下水注意1',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, sand_area_current_template_message)

    elif (event.message.text.find("#礁岩區") != -1):     
        reef_area_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-3',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/reef.jpg?raw=true',
        title = '礁岩區',
        text = '通常因礁岩, 暗流較強, 也導致魚群種類繁多, 點選看看吧!',
        actions = [
            MessageAction(
                label = '暗流',
                text ='#暗流',
            ),
            MessageAction(
                label = '生物',
                text = '#生物',
            ),
            MessageAction(
                label = '小科普',
                text = '#小科普',
            ),
            MessageAction(
                label = '返回 下水注意',
                text = '#下水注意1'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, reef_area_buttons_template_message)

    elif (event.message.text.find("#暗流") != -1):     
        reef_area_underflow_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-3-1',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/reef.jpg?raw=true',
        title = '暗流',
        text = '礁岩區的暗流通常較多, 在不熟悉當地的情況下建議別輕易嘗試, 無論該地方有多美',
        actions = [
            MessageAction(
                label='返回 礁岩區',
                text='#礁岩區',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, reef_area_underflow_buttons_template_message)
    elif (event.message.text.find("#生物") != -1):     
        reef_area_creature_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-3-2',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/clownfish_island.jpg?raw=true',
        title = '海中生物',
        text = '海中生物傷害 常見的有水母 珊瑚 海葵 海膽 海綿等 請務必養成避免觸碰的好習慣!',
        actions = [
            MessageAction(
                label='返回 礁岩區',
                text='#礁岩區',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, reef_area_creature_buttons_template_message)
    elif (event.message.text.find("#小科普") != -1):     
        reef_area_knowledge_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-3-3',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/reef.jpg?raw=true',
        title = '生物小科普',
        text = '點選看看吧!',
        actions = [
            MessageAction(
                label='豆丁海馬',
                text='#豆丁兄',
            ),            
            MessageAction(
                label='海蛞蝓',
                text='#海蛞蝓兄',
            ),
            MessageAction(
                label='錢鰻',
                text='#好吃',
            ),
            MessageAction(
                label='返回 礁岩區',
                text='#礁岩區',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, reef_area_knowledge_buttons_template_message)

    elif (event.message.text.find("#豆丁兄") != -1):     
        reef_area_seahorse_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-3-3-1',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/seahorse.jpg?raw=true',
        title = '豆丁海馬',
        text = '常藏於海扇枝節間的小精靈, 屬於魚綱 成熟體長2～3公分, 會找其他的雌海馬收卵，直到他的育兒袋放滿了卵為止!',
        actions = [
            MessageAction(
                label='返回 小科普',
                text='#小科普',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, reef_area_seahorse_buttons_template_message)
    elif (event.message.text.find("#海蛞蝓兄") != -1):     
        reef_area_seaslug_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-3-3-2',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/seaslug.jpg?raw=true',
        title = '海蛞蝓 俗稱海麒麟 海牛',
        text = '以珊瑚、水母、海葵為食, 海蛞蝓吃掉他們並將毒素轉移到身體表面, 同時披著色彩鮮艷的外表, 以警告掠食者',
        actions = [
            MessageAction(
                label='返回 小科普',
                text='#小科普',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, reef_area_seaslug_buttons_template_message)
    elif (event.message.text.find("#好吃") != -1):     
        reef_area_eel_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-3-3-3',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/seahorse.jpg?raw=true',
        title = '錢鰻 亦稱薯鰻、海鱔等',
        text = '白天躲藏珊瑚礁縫隙只露出顆頭，對人疵牙裂嘴，實際上他們僅嗅聽覺靈敏，根本看不清前面，是大近視仔',
        actions = [
            MessageAction(
                label='返回 小科普',
                text='#小科普',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, reef_area_eel_buttons_template_message)

    elif (event.message.text.find("#返程及其他") != -1):     
        notice_others_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-4',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/swimback.jpg?raw=true',
        title = '返程及其他',
        text = '返程時如若體力已下滑，請避免從事極限挑戰，點選看看吧!',
        actions = [
            MessageAction(
                label = '頂流',
                text ='#頂流',
            ),
            MessageAction(
                label = '上下岸',
                text = '#上下岸',
            ),
            MessageAction(
                label = '返回 下水注意',
                text = '#下水注意1'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, notice_others_buttons_template_message)

    elif (event.message.text.find("#頂流") != -1):     
        notice_others_current_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-4-1',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/swimback.jpg?raw=true',
        title = '頂流時應注意?',
        text = '強流途中大石頭兩側流速更快，盡量避開，此外若流是南北向請斜向踢動，以減少阻力',
        actions = [
            MessageAction(
                label='返回 返程及其他',
                text='#返程及其他',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, notice_others_current_buttons_template_message)
    elif (event.message.text.find("#上下岸") != -1):     
        notice_others_ashore_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-4-1',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/ashore.jpg?raw=true',
        title = '上下岸注意',
        text = '台灣適合潛水處大都為珊瑚礁岩地形，岩石極為鋒利，反而才是潛水受傷的主因。點選看看吧!',
        actions = [
            MessageAction(
                label='離岸入水',
                text='#離岸入水',
            ),
            MessageAction(
                label='上岸',
                text='#上岸',
            ),
            MessageAction(
                label='返回 返程及其他',
                text='#返程及其他',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, notice_others_ashore_buttons_template_message)
    
    elif (event.message.text.find("#離岸入水") != -1):     
        notice_others_not_ashore_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-4-1-1',
        template = ButtonsTemplate(
        title = '離岸入水',
        text = '先戴好面鏡再下水，並利用水流脫離浪區，再穿蛙鞋。',
        actions = [
            MessageAction(
                label='返回 上下岸',
                text='#上下岸',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, notice_others_not_ashore_buttons_template_message)
    elif (event.message.text.find("#上岸") != -1):     
        notice_others_go_ashore_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template-1-1-4-1-2',
        template = ButtonsTemplate(
        title = '上岸',
        text = '勿在浪區穿脫蛙鞋；計算大浪週期，大浪上岸平浪離開，如浪中不穩，別硬抓，隨水流脫離，避免受傷優先',
        actions = [
            MessageAction(
                label='返回 上下岸',
                text='#上下岸',
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, notice_others_go_ashore_buttons_template_message)
    

    elif (event.message.text.find("#用品介紹") != -1):     
        equips_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 1-2',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/dive_equips.jpg?raw=true',
        title='用品介紹',
        text='裝備方面以網頁較為明確，附上準備完整的友站連接以供參考',
        actions=[
            URIAction(
                label = '陳子名的海上生活-<新手入坑基本裝備>',
                uri = 'https://mindiving.tw/freediving_02/',
            ),
            MessageAction(
                label = '返回 新手懶人包',
                text = '@新手懶人包'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, equips_buttons_template_message)
        
    elif (event.message.text.find("#diving_system_intro") != -1):     
        system_intro_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 1-3',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/dive_equips.jpg?raw=true',
        title='潛水系統介紹',
        text='系統介紹以網頁較為明確，附上優秀的友站連接以供參考',
        actions=[
            URIAction(
                label = '陳子名的海上生活-<自潛初階課程比較>',
                uri = 'https://mindiving.tw/freediving_08/',
            ),
            MessageAction(
                label = '返回 新手懶人包',
                text = '@新手懶人包'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, system_intro_buttons_template_message)
