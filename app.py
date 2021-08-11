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

# 建立log的客戶端
client = google.cloud.logging.Client()

# 建立line event log，用來記錄line event
bot_event_handler = CloudLoggingHandler(client,name="diving_line_bot_event")
bot_event_logger=logging.getLogger('diving_line_bot_event')
bot_event_logger.setLevel(logging.INFO)
bot_event_logger.addHandler(bot_event_handler)

# 準備app
app = Flask(__name__)
# 專門跟line溝通
line_bot_api = LineBotApi('請輸入token')
# 收消息用的
handler = WebhookHandler('Channel secret')

# http的入口,給line傳消息用的
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    # 消息整個交給bot_event_logger 請他傳回GCP
    bot_event_logger.info(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

### '''烏鴉學舌'''   可新增回應
# # handler收到文字消息的時候,回應用戶講過的話
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     # 請line_bot_api 回傳消息
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))

from google.cloud import storage
from google.cloud import firestore

'''關注時取個資'''
from functions.user_info import handle_follow_event, handle_unfollow_event 
@handler.add(FollowEvent)
def handle_line_follow(event):
    return handle_follow_event(event)

@handler.add(UnfollowEvent)
def handle_line_unfollow(event):
    return handle_unfollow_event(event)


'''
按鍵範本
Button篇
    設定模板消息，指定其參數細節。

alt_text: Line簡覽視窗所出現的說明文字
template: 所使用的模板
ButtonsTemplate: 按鍵模板
    thumbnail_image_url: 展示圖片
    title: 標題
    text: 說明文字
    actions: 模板行為所使用的行為
    data: 觸發postback後用戶回傳值，可以對其做商業邏輯處理
'''

'''準備QuickReply的Button'''
textQRB_wait = QuickReplyButton(
    action=MessageAction(
    label="哀  等吧", 
    text="等吧"
    ))
textQRB_notwait = QuickReplyButton(
    action=MessageAction(
    label = "不等啦 不等啦", 
    text = '''Mnnn...管他的!! 不等啦 
    昨天加班不睡就是為了這!!!
    '''
    ))

textQRB_sand = QuickReplyButton(
    action=MessageAction(
    label="沙地", 
    text="往沙地游過去吧!"
    ))   
textQRB_reef = QuickReplyButton(
    action=MessageAction(
    label = "礁岩區", 
    text = '往礁岩游過去吧'))

textQRB_stay = QuickReplyButton(
    action=MessageAction(
    label="再多待一會兒", 
    text='''沉迷於小可愛們的你, 
    又待了許久才緩緩回程
    '''))
textQRB_leave = QuickReplyButton(
    action=MessageAction(
    label = "回程", 
    text = '''發現的不只是陌生, 還有那強勁的海流!
    於是決定馬上回程'''))

textQRB_lookleft = QuickReplyButton(
    action=MessageAction(
    label = "往左看看", 
    text = '讓我看看!!'))
textQRB_lookright = QuickReplyButton(
    action=MessageAction(
    label="向右瞧瞧", 
    text='好像沒有東西~ 讓我去另一邊看看好了!'))
    
textQRB_lookback = QuickReplyButton(
    action=MessageAction(
    label = "回頭", 
    text = '回頭一望'))
textQRB_moveforward = QuickReplyButton(
    action=MessageAction(
    label ="逃跑", 
    text = '往前加速逃離'))

textQRB_original = QuickReplyButton(
    action=MessageAction(
    label = "原路", 
    text = '由原路回去吧'))
textQRB_aroundreef = QuickReplyButton(
    action=MessageAction(
    label = "繞一圈礁石區再回去", 
    text = '繞一圈礁石區再回去吧!'))

textQRB_closeship = QuickReplyButton(
    action=MessageAction(
    label = "進去看看", 
    text = '來進去沉船裡, 看看有什麼好東西好了!'))
textQRB_leaveship = QuickReplyButton(
    action=MessageAction(
    label = "下次再來", 
    text = '還是先回去吧! 沉船下次再來吧'))

textQRB_directly = QuickReplyButton(
    action=MessageAction(
    label = "游直線", 
    text = '選擇頂著逆流繼續游'))
textQRB_obliquely = QuickReplyButton(
    action=MessageAction(
    label = "側切", 
    text = '選擇順著海流朝向岸邊游'))

''' 設計QuickReplyButton的List'''
quickReplyList = QuickReply(
    items = [textQRB_wait, textQRB_notwait, ]
)
wait_QRB_List = QuickReply(
    items = [textQRB_wait, textQRB_notwait]
)
sandreef_QRB_List = QuickReply(
    items = [textQRB_sand, textQRB_reef]
)
stayleave_QRB_List = QuickReply(
    items = [textQRB_stay, textQRB_leave]
)
look_QRB_List = QuickReply(
    items = [textQRB_lookleft, textQRB_lookright]
)
eelevent_QRB_List = QuickReply(
    items = [textQRB_lookback, textQRB_moveforward]
)
ending_QRB_List = QuickReply(
    items = [textQRB_original, textQRB_aroundreef]
)
shipwreck_QRB_List = QuickReply(
    items = [textQRB_closeship, textQRB_leaveship]
)
swimchoose_QRB_List = QuickReply(
    items = [textQRB_directly, textQRB_obliquely]
)


'''物件化quickreply訊息發送'''
wait_QR_text_send_message = TextSendMessage(
    text='要下水嗎??', quick_reply = wait_QRB_List)
sandreef_QR_text_send_message = TextSendMessage(
    text='要往哪邊去呢~?', quick_reply = sandreef_QRB_List)
stayleave_QR_text_send_message = TextSendMessage(
    text='你是怎麼想的呢?', quick_reply = stayleave_QRB_List)
look_QR_text_send_message = TextSendMessage(
    text='怎摩辦!?!?', quick_reply = look_QRB_List)
eelevent_QR_text_send_message = TextSendMessage(
    text='在哪裡呢?', quick_reply = eelevent_QRB_List)
ending_QR_text_send_message = TextSendMessage(
    text='如何回去呢?', quick_reply = ending_QRB_List)
shipwreck_QR_text_send_message = TextSendMessage(
    text='要靠近探險嗎?', quick_reply = shipwreck_QRB_List)
swimchoose_QR_text_send_message = TextSendMessage(
    text='應該如何!!??', quick_reply = swimchoose_QRB_List)


'''根據Richmenu菜單的圖，設定相對應的功能 '''
template_message_dict = {
  "@新雞入水":"咕咕咕",
  "@老手":"咕嚕咕嚕",
  "@聯絡作者":"Here am I!"
}


story_template_message_dict = {
  "@reply": wait_QR_text_send_message,
  "撲通":sandreef_QR_text_send_message,
  "一片陌生":stayleave_QR_text_send_message,
  "海扇好像":look_QR_text_send_message,
  "盯著我":eelevent_QR_text_send_message,
  "死而無憾":ending_QR_text_send_message,
  "年代感的沉船":shipwreck_QR_text_send_message,
  "粗心未察而被帶遠":swimchoose_QR_text_send_message,
}




''' 用戶文字消息的處理方式'''
from  fordummies.fordummies import for_dummies
from  forexperienced.forexperienced import for_experienced


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if (event.message.text.find("@新雞入水") != -1):
        print("Image Carousel")       
        story_or_pass_template = TemplateSendMessage(
        alt_text = 'Image Carousel template',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/startdiving.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '來場海底冒險吧!',
                    text = '聽說附近有一個秘境海域，大片的海葵如同秋實垂穗，滿滿的整片礁岩都是小丑魚和他們ㄉ小孩 \ >皿< /，而據說   就在這草叢後面的海域!',
                    data = 'action=story'
                )
            ),
            ImageCarouselColumn(
                image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/skipbird.jpg?raw=true',
                action=PostbackTemplateAction(
                    label='先來去下回合',
                    text='skip to @新手懶人包',
                    data='action=skip'))
        ]))
        line_bot_api.reply_message(event.reply_token, story_or_pass_template)


    elif (event.message.text.find("秘境海域") != -1):
        story_start_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 0',
        template=ButtonsTemplate(
        title='故事intro',
        text='今天你約好了要跟水水姑娘一起去個秘境探險，為了這次的date，你熬了個全夜...',
        actions=[
            MessageEvent(
                label='欸~ 起風了? ',
                text='風似乎有些些大',
            ),
            MessageEvent(
                label = '靜態table-友站連結<VD Fd>',
                uri = 'https://www.vdfreediving.com/archives/4009'
            ),
            MessageAction(
                label = '返回 上一層',
                text = '@老手'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, story_start_buttons_template_message)
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text=
        # ''' ... 水水又遲到 = =  \n
        #             (sigh...)
        #                     .
        #                     .
        #                     .
        #                     .
        #     诶~? 
        # 話說這... 今天的風好像有些些大''',

        # 要等她再下水嗎, 一個人會不會有點~

        # 你覺得應該如何呢? (請輸入@reply)   '
        # ))
        
        time.sleep(2)

    elif (event.message.text.find("@reply") != -1):
        line_bot_api.reply_message(
        event.reply_token,
        story_template_message_dict.get("@reply")
        )


    elif (event.message.text.find("等吧") != -1):     
        wait_stack_template = TemplateSendMessage(
        alt_text = 'Image Carousel template1',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/beachwaiting.jpg?raw=true',
                action = MessageTemplateAction(
                    label = '疊個石塔吧~',
                    text = 'Alright, lets stack rocks ...'
            ))
        ]))
        line_bot_api.reply_message(event.reply_token, wait_stack_template)

    elif (event.message.text.find("stack rocks") != -1):     
        stack_tide_template = TemplateSendMessage(
        alt_text = 'Image Carousel template2',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/tide01.jpg?raw=true',
                action = MessageTemplateAction(
                    label = '孤身, 看海, 疊塔',
                    text = 
            ''' 好久...
                石塔疊的老高, 那人還是不來

                Mnn  !?
                浪變大哩!, 似乎是漲潮了
                                    .
                                    .
                                    .
                哀...
                下水應該很危險, 還是回家吧...'''
            ))
        ]))
        line_bot_api.reply_message(event.reply_token, stack_tide_template)

    # elif (event.message.text.find("回家吧") != -1):
    #     tide_home_template = TemplateSendMessage(
    #     alt_text = 'Image Carousel template2',
    #     template = ImageCarouselTemplate(
    #     columns = [
    #         ImageCarouselColumn(
    #             image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/gohome.jpg?raw=true',
    #             action = PostbackTemplateAction(
    #                 label = '開車',
    #                 text = '''下次再找其他人一起來吧~
    #                                             .
    #                                             .
    #                                             .
    #                                             .
    #                    請輸入 @新手懶人包 取得更多資訊  
    #         或是點選下方 我是誰 的menu重新來一次吧!''',
    #                 data = 'go home'))
    #     ]))
    #     line_bot_api.reply_message(event.reply_token, tide_home_template)

    elif (event.message.text.find("不等啦") != -1):     
        bush_push_template = TemplateSendMessage(
        alt_text = 'Image Carousel template3',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/beachbush.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '撥開草叢',
                    text = '''
        是海是海是海!!! 好興奮好興奮RRRR 

        先衝啦RRR    \ >w< /''',
                    data = 'action=run&risk=2&strength=-1'))
        ]))
        line_bot_api.reply_message(event.reply_token, bush_push_template)  

    elif (event.message.text.find("先衝啦R") != -1):     
        jump_into_sea_template = TemplateSendMessage(
        alt_text = 'Image Carousel template4',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/jumpintosea01.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = 'Lets jump!',
                    text = '撲通!!!',
                    data = 'action=dive&risk=4&strength=-1'))
        ]))
        line_bot_api.reply_message(event.reply_token, jump_into_sea_template) 

    elif (event.message.text.find("撲通") != -1):
        line_bot_api.reply_message(
        event.reply_token,
        story_template_message_dict.get("撲通")
        )

    elif (event.message.text.find("往沙地游過去吧") != -1):     
        sand_chosen_template = TemplateSendMessage(
        alt_text = 'Image Carousel template5',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/sand1.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '平坦淺淺的沙地',
                    text = '''軟呼呼的沙看來很欠躺><
                    來去試躺一下好了>////<''',
                    data = 'action=dive&risk=1&strength=-1')),
        ]))
        line_bot_api.reply_message(event.reply_token, sand_chosen_template) 

    elif (event.message.text.find("欠躺") != -1):     
        sleep_on_sand_template = TemplateSendMessage(
        alt_text = 'Image Carousel template7',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/sleepsand.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '躺著休息一下',
                    text = 
            '''                     .
                                    .
                                    .
                                    .
                                    .
                                    .
                                !!!!!
            有個奇妙的身影從旁掠過''',
                    data = 'action=dive&risk=1&strength=-2')),
        ]))
        line_bot_api.reply_message(event.reply_token, sleep_on_sand_template)     

    elif (event.message.text.find("奇妙的身影") != -1):     
        seaturtle_template = TemplateSendMessage(
        alt_text = 'Image Carousel template8',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/seaturtle_sand1.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '龜兄是你!',
                    text = 
            '''     上上下下觀察龜兄一番後，
                    海面上小作休憩的你，
                    命運的海流帶你來到處處皆是奇怪海草的地方!?''',
                    data = 'action=float&risk=1&strength=1')),
        ]))
        line_bot_api.reply_message(event.reply_token, seaturtle_template)  

    elif (event.message.text.find("奇怪海草") != -1):     
        garden_eels_template = TemplateSendMessage(
        alt_text = 'Image Carousel template9',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/garden%20eels.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '這啥!',
                    text = '這啥!??  好奇的你游向他們',
                    data = 'action=dive&risk=1&strength=-1')),
        ]))
        line_bot_api.reply_message(event.reply_token, garden_eels_template)  

    elif (event.message.text.find("這啥") != -1):     
        garden_eel_template = TemplateSendMessage(
        alt_text = 'Image Carousel template10',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/Garden%20eel.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '我是花園鰻!',
                    text = '''成功讓這些小可愛嚇得縮回沙裡的你, 
                    瞥見四周, 發現一片陌生...''',
                    data = 'action=dive&risk=1&strength=-1')),
        ]))
        line_bot_api.reply_message(event.reply_token, garden_eel_template)  

    elif (event.message.text.find('一片陌生') != -1):
        line_bot_api.reply_message(
        event.reply_token,
        story_template_message_dict.get("一片陌生")
        )        

    elif (event.message.text.find("馬上回程") != -1):     
        swimback_immediately_template = TemplateSendMessage(
        alt_text = 'Image Carousel template11',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/swimback.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '使勁地游!游!游!',
                    text = '''強流讓你略感疲倦且害怕, 
                    於是決定回家吧!''',
                    data = 'action=swim&risk=1&strength=-3')),
        ]))
        line_bot_api.reply_message(event.reply_token, swimback_immediately_template)  

    elif (event.message.text.find("緩緩回程") != -1):     
        swimback_late_template = TemplateSendMessage(
        alt_text = 'Image Carousel template12',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/swimback.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '費勁地游!游!游!游!',
                    text = '''強流讓你精疲力竭且耽驚受怕, 
                    決定回家吧...''',
                    data = 'action=swim&risk=2&strength=-4')),
        ]))
        line_bot_api.reply_message(event.reply_token, swimback_late_template)


    elif (event.message.text.find("往礁岩游過去吧") != -1):     
        reef_chosen_template = TemplateSendMessage(
        alt_text = 'Image Carousel template6',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/reef.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '好多礁岩 好多魚><',
                    text = '小丑魚島的家想必在這方向, 往前看看好了!',
                    data = 'action=swim&risk=2&strength=-1'))
        ]))
        line_bot_api.reply_message(event.reply_token, reef_chosen_template) 

    elif (event.message.text.find("想必在這") != -1):     
        soft_corals_template = TemplateSendMessage(
        alt_text = 'Image Carousel template13',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/soft_corals.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '巨大的海扇',
                    text = '诶  總感覺這海扇好像哪裡有點奇怪...',
                    data = 'action=dive&risk=1&strength=-1'))
        ]))
        line_bot_api.reply_message(event.reply_token, soft_corals_template) 

    elif (event.message.text.find("海扇好像") != -1):
        line_bot_api.reply_message(
        event.reply_token,
        story_template_message_dict.get("海扇好像")
        )

    elif (event.message.text.find("讓我去另一邊") != -1) or (event.message.text.find("讓我看看") != -1):     
        sea_horse_template = TemplateSendMessage(
        alt_text = 'Image Carousel template14',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/seahorse.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '豆丁海馬 <3 ',
                    text = '''好可愛的小東西呀>///<
                    海扇旁邊好像還有什麼的樣子...?''',
                    data = 'action=dive&risk=1&strength=-1'))
        ]))
        line_bot_api.reply_message(event.reply_token, sea_horse_template) 

    elif (event.message.text.find("海扇旁邊") != -1):     
        sea_slug_template = TemplateSendMessage(
        alt_text = 'Image Carousel template15',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/seaslug.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '海蛞蝓 >< ',
                    text = '''      好亮麗的小東西呀>///<
                        可惡可惡, 我快受不了啦!!!
                                                 .
                                                 .
            (等等... 是不是.. 有什麼東西在盯著我)
                                  ..o((⊙﹏⊙))o...
                    ''',
                    data = 'action=dive&risk=1&strength=-1'))
        ]))
        line_bot_api.reply_message(event.reply_token, sea_slug_template) 

    elif (event.message.text.find("盯著我") != -1):
        line_bot_api.reply_message(
        event.reply_token,
        story_template_message_dict.get("盯著我")
        )

    elif (event.message.text.find("回頭一望") != -1):     
        eel_template = TemplateSendMessage(
        alt_text = 'Image Carousel template16',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/eel.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '錢鰻 兄',
                    text = '''......
                    不就一隻鰻魚, 瞪屁
          回頭上岸立馬大吃鰻魚飯 壓壓驚
                可惡... 趕緊往前加速吧!
                    ''',
                    data = 'action=dive&risk=0&strength=-1'))
        ]))
        line_bot_api.reply_message(event.reply_token, eel_template) 

    elif (event.message.text.find("往前加速") != -1):     
        clownfish_island_template = TemplateSendMessage(
        alt_text = 'Image Carousel template17',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/clownfish_island.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '小丑魚們溫暖的家 <3',
                    text = '''我的天!! 也太多了吧
                    等等  那個小家庭是怎麼回事, 游近點好了!
                    ''',
                    data = 'action=dive&risk=1&strength=-1'))
        ]))
        line_bot_api.reply_message(event.reply_token, clownfish_island_template) 

    elif (event.message.text.find("小家庭") != -1):     
        clownfish_template = TemplateSendMessage(
        alt_text = 'Image Carousel template18',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/clownfish.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '小丑魚ㄉ小家庭',
                    text = '''    .....

                        能親眼看到這畫面
                    我的人生死而無憾了!!!

         此時, 興奮至極的你在, 在目標達成後
                感到相當疲倦, 於是決定回程
                    ''',
                    data = 'action=dive&risk=1&strength=-1'))
        ]))
        line_bot_api.reply_message(event.reply_token, clownfish_template) 


    elif (event.message.text.find("死而無憾") != -1):
        line_bot_api.reply_message(
        event.reply_token,
        story_template_message_dict.get("死而無憾")
        )

    elif (event.message.text.find("原路回去") != -1):     
        swimback_original_immediately_template = TemplateSendMessage(
        alt_text = 'Image Carousel template19',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/swimback.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '費勁地游!游!游!游!',
                    text = '''強流讓你精疲力竭且耽驚受怕, 
                    決定回家吧!''',
                    data = 'action=swim&risk=2&strength=-3')),
        ]))
        line_bot_api.reply_message(event.reply_token, swimback_original_immediately_template) 

    elif (event.message.text.find("繞一圈礁石區") != -1):     
        shipwreck_template = TemplateSendMessage(
        alt_text = 'Image Carousel template20',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/shipwreck.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '沈船',
                    text = '''是一艘充滿年代感的沉船!  許多小魚在一旁游逸, 
            仔細一看, 還有些神秘的艙室半掩!
                    ''',
                    data = 'action=dive&risk=3&strength=-1'))
        ]))
        line_bot_api.reply_message(event.reply_token, shipwreck_template) 

    elif (event.message.text.find("年代感的沉船") != -1):
        line_bot_api.reply_message(
        event.reply_token,
        story_template_message_dict.get("年代感的沉船")
        )

    elif (event.message.text.find("沉船下次再來") != -1):     
        swimback_current_template = TemplateSendMessage(
        alt_text = 'Image Carousel template21',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/swimback.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '費勁地游!游!游!游!',
                    text = '''粗心未察而被帶遠的你, 突然發現, 海流是如此的強勁 
                    ...''',
                    data = 'action=swim&risk=1&strength=-2')),
        ]))
        line_bot_api.reply_message(event.reply_token, swimback_current_template)

    elif (event.message.text.find("粗心未察而被帶遠") != -1):
        line_bot_api.reply_message(
        event.reply_token,
        story_template_message_dict.get("粗心未察而被帶遠")
        )

    elif (event.message.text.find("順著海流") != -1):     
        swimback_obliquely_template = TemplateSendMessage(
        alt_text = 'Image Carousel template22',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/wave_beach.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '癱倒在不知名的海灘',
                    text = '''僥倖游回岸邊的你, 失去所有餘力''',
                    data = 'action=swim&risk=3&strength=-4')),
        ]))
        line_bot_api.reply_message(event.reply_token, swimback_obliquely_template)

    elif (event.message.text.find("頂著逆流") != -1):     
        swimback_directly_template = TemplateSendMessage(
        alt_text = 'Image Carousel template23',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/sunset.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '泡沫餘暉',
                    text = '''
            過度好奇的你, 陸地已失去了你的形跡
            但  遠望泡沫餘暉, 你的身影仍若影若現

            大概, 你已徹底溶入了這個片海吧
                    ...''',
                    data = 'action=swim&risk=5&strength=-5')),
        ]))
        line_bot_api.reply_message(event.reply_token, swimback_directly_template)

    elif (event.message.text.find("進去沉船") != -1):     
        bubble_sunset_template = TemplateSendMessage(
        alt_text = 'Image Carousel template23',
        template = ImageCarouselTemplate(
        columns = [
            ImageCarouselColumn(
                image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/sunset.jpg?raw=true',
                action = PostbackTemplateAction(
                    label = '泡沫餘暉',
                    text = '''
            船沉的理由, 沉了探索沈船的你
                    ...''',
                    data = 'action=swim&risk=5&strength=-2')),
        ]))
        line_bot_api.reply_message(event.reply_token, bubble_sunset_template)


    elif (event.message.text.find("回家吧") != -1):     
        Best_Ending_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template0',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/gohome.jpg?raw=true',
        title='Best Ending   # 下次再來吧',
        text='下次再找其他人一起來吧~                  記得找些\"其他人\"',
        actions=[
            MessageAction(
                label='再玩一次!',
                text='@新雞入水',
            ),
            MessageAction(
                label='新手懶人包',
                text='@新手懶人包'
            ),
            URIAction(
                label = '找些朋友吧!',
                uri = 'https://www.eatgether.com/'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, Best_Ending_buttons_template_message)
  
    elif (event.message.text.find("略感疲倦且害怕") != -1):     
        Lucky_Ending1_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template1',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/gohome.jpg?raw=true',
        title = 'Lucky Ending   # 人還在 只是累',
        text = 'To 略感疲倦且害怕的你               今天運氣最好!  買張樂透吧!',
        actions = [
            MessageAction(
                label = '再玩一次!',
                text = '@新雞入水',
            ),
            MessageAction(
                label = '新手懶人包',
                text = '@新手懶人包'
            ),
            URIAction(
                label = '不如買張樂透吧',
                uri = 'https://www.taiwanlottery.com.tw/Superlotto638/index.asp'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, Lucky_Ending1_buttons_template_message)
  
    elif (event.message.text.find("精疲力竭且耽驚受怕") != -1):     
        Lucky_Ending2_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template2',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/gohome.jpg?raw=true',
        title = 'Lucky Ending   # 人還在 只是累得像狗',
        text = ' To  精疲力竭且耽驚受怕的你     .今天運氣不錯!    來去買張刮刮樂吧!',
        actions = [
            MessageAction(
                label = '再玩一次!',
                text = '@新雞入水',
            ),
            MessageAction(
                label = '新手懶人包',
                text = '@新手懶人包'
            ),
            URIAction(
                label = '你值得一張刮刮樂',
                uri = 'https://www.taiwanlottery.com.tw/instant/index.asp'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, Lucky_Ending2_buttons_template_message)
  
    elif (event.message.text.find("失去所有餘力") != -1):     
        Normal_Ending_buttons_template_message = TemplateSendMessage(
        alt_text = 'Buttons template3',
        template = ButtonsTemplate(
        thumbnail_image_url = 'https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/wave_beach.jpg?raw=true',
        title = 'Normal Ending   # 人還在 心不在',
        text = ' 癱倒在不知名的海灘上, 等待遙遙無期的體力回復...',
        actions = [
            MessageAction(
                label = '再玩一次!',
                text = '@新雞入水',
            ),
            MessageAction(
                label = '新手懶人包',
                text = '@新手懶人包'
            ),
            URIAction(
                label = '你需要這個',
                uri = 'https://www.ht.org.tw/religion29.htm'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, Normal_Ending_buttons_template_message)

    elif (event.message.text.find("沉了探索沈船的你") != -1):     
        Worst_Ending_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template4',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/sunset.jpg?raw=true',
        title='Worst Ending     # 泡沫餘暉',
        text='過度好奇, 陸地已失去你的形跡  但  遠望泡沫餘暉, 你的身影仍若影若現,    大概   你已徹底 溶入了這片海吧',
        actions=[
            MessageAction(
                label='再玩一次!',
                text='@新雞入水',
            ),
            MessageAction(
                label='新手懶人包',
                text='@新手懶人包'
            ),
            URIAction(
                label = '你需要這個',
                uri = 'https://www.gold-kirin.com.tw/knowledge/detail/%E7%92%B0%E4%BF%9D%E8%91%AC/%E5%B0%8D%E5%A4%A7%E5%9C%B0%E5%8F%8B%E5%96%84%E7%9A%84%E6%9C%80%E5%BE%8C%E9%81%93%E5%88%A5%EF%BC%8C%E6%B5%B7%E8%91%AC%E4%B8%8D%E6%98%AF%E4%BB%80%E9%BA%BC%E5%9C%B0%E6%96%B9%E9%83%BD%E5%8F%AF%E4%BB%A5%EF%BC%8C%E5%9C%B0%E9%BB%9E%E3%80%81%E5%AE%B9%E5%99%A8%E9%83%BD%E6%9C%89%E8%A6%8F%E5%AE%9A'
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, Worst_Ending_buttons_template_message)

    elif (event.message.text.find("@新手懶人包") != -1) or (event.message.text.find("#") != -1):     
        for_dummies(event)
    
    elif (event.message.text.find("@老手") != -1) or (event.message.text.find("*") != -1):     
        for_experienced(event)

    elif (event.message.text.find("@聯絡作者") != -1):     
        Worst_Ending_buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template 3-0',
        template=ButtonsTemplate(
        thumbnail_image_url='https://github.com/williampwhuang/diving_line_bot_project/blob/first-one/image/chick&egg.jpg?raw=true',
        title='作者資訊',
        text='嗨嗨你好，本linebot內容參照各方公開資訊編寫，如有冒犯智財，或是哪需要改進，還請不吝指教!',
        actions=[
            MessageAction(
                label='about me',
                text='我是coding及diving上的小菜鳥，請多指教',
            ),
            MessageAction(
                label='contact me',
                text='will830222@gmail.com',
            ),
            MessageAction(
                label = 'Favorite dive site',
                text = 'training:東北角_潮境, 恆春_出海口, target:蘭嶼_八代灣! '
            ),
        ]))
        line_bot_api.reply_message(event.reply_token, Worst_Ending_buttons_template_message)
 




# ''' PostbackEvent  '''
# @handler.add(PostbackEvent)
# def handle_post_message(event):
#     if (event.postback.data.find('story_or_pass_template')== 0):
#         # return story_or_pass_template
#         return print('test')

#     elif (event.postback.data.find('experienced01') == 0):
#         return ""

#     elif (event.postback.data.find('author01') == 0):
#         return ""

#     elif (event.postback.data.find('uts01') == 0):
#         return ""

#     elif (event.postback.data.find('skip01') == 0):
#         return ""




# 運行伺服器,運行在 8080 port,port那段是為了可以部屬到cloud run而增設的
if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    app.run()

