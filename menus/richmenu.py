from google.cloud import storage
from google.cloud import firestore
from flask import Request
from linebot import (
    LineBotApi, WebhookHandler
)
from flask import Flask, request, abort
import urllib.request
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, 
    TextSendMessage, PostbackEvent
)

line_bot_api = LineBotApi('DrKBizvbfKriwD55+lOR9uu/5mPEt+4Ty4gwp2pRlv9LDlPvpsl/nTUUPvpfvPo3INHx3VjDCEJPRa7l+kAtm1WwBuuow/7S0yRTMv2xw4t+65R2IU9p3y1urDuDc1l3vl8cAJsKmfEw7OjjHErIEQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ffed9c02546d9c25478cea4e006a41a8')

'''
用戶菜單功能介紹
    用戶能透過點擊菜單，進行我方希冀之業務功能。
流程
    準備菜單的圖面設定檔
    讀取安全設定檔上的參數
    將菜單設定檔傳給Line
    對Line上傳菜單照片
    檢視現有的菜單
    將菜單與用戶做綁定
    將菜單與用戶解除綁定
    刪除菜單
'''
'''
菜單設定檔

    設定圖面大小、按鍵名與功能
    
'''

# 下方json檔 來自於line bot 圖文選單
menuRawData="""
{
  "size": {
    "width": 2500,
    "height": 843
  },
  "selected": true,
  "name": "我是誰",
  "chatBarText": "我是誰~",
  "areas": [
    {
      "bounds": {
        "x": 0,
        "y": 2,
        "width": 835,
        "height": 841
      },
      "action": {
        "type": "postback",
        "text": "@新雞入水",
        "data": "資料 1"
      }
    },
    {
      "bounds": {
        "x": 831,
        "y": 0,
        "width": 834,
        "height": 842
      },
      "action": {
        "type": "postback",
        "text": "@老手",
        "data": "資料 2"
      }
    },
    {
      "bounds": {
        "x": 1667,
        "y": 4,
        "width": 831,
        "height": 839
      },
      "action": {
        "type": "postback",
        "text": "@聯絡作者",
        "data": "資料 3"
      }
    }
  ]
}
"""

'''
建圖文選單
  json
  圖片
  圖文選單id正式運作
把用戶跟圖文選單綁釘在一起
解除綁定
瀏覽目前有多少張圖文選單
'''
'''
載入前面的圖文選單設定，
並要求line_bot_api將圖文選單上傳至Line
'''
from linebot.models import RichMenu
import requests
import json, os
# 讀取圖文選單設定檔
menuJson=json.loads(menuRawData)
# 用line_bot_api的 create_rich_menu方法創造圖文選單id
# rich_menu :　RichMenu
# new_from_json_dict  可以從json裡生成RichMenu物件
lineRichMenuId = line_bot_api.create_rich_menu(rich_menu=RichMenu.new_from_json_dict(menuJson))
print(lineRichMenuId)

'''
將先前準備的菜單照片，以Post消息寄發給Line
    載入照片
    要求line_bot_api，將圖片傳到先前的圖文選單id
圖文選單id 要好好保存，通常會存到資料庫中
richmenu-9c87b4194d18802e1234296e5ea0c8d2
'''
# 開啟圖檔
uploadImageFile = open("/home/will830222/cloudshell_open/diving_line_bot_will/menus/richmenu.jpg", 'rb')

# GET https://api.line.me/v2/bot/richmenu/{richmenu-9ad99ad2c4ad04f381b76885e17d0acb}

# 讓line_bot_api上傳照片，把那生成的id跟圖文選單的照片綁在一起
setImageResponse = line_bot_api.set_rich_menu_image(lineRichMenuId, 'image/jpeg', uploadImageFile)

print(setImageResponse)

'''
將選單綁定到特定用戶身上
    取出上面得到的菜單Id及用戶id
    要求line_bot_api告知Line，將用戶與圖文選單做綁定
'''
# https://api.line.me/v2/bot/user/{userId}/richmenu/{richMenuId}

# 讓line_bot_api 告知line 把圖文選單給指定的user
# 以後也可以自行偵測user_id  => event.source.uesr_id
# linkResult = line_bot_api.link_rich_menu_to_user("Uff25b58196920cabc1ad651c0d0afba2", lineRichMenuId)
# linkResult = line_bot_api.link_rich_menu_to_user("Uff25b58196920cabc1ad651c0d0afba2", 'richmenu-9c87b4194d18802e1234296e5ea0c8d2')
def linkResult(event):
    return line_bot_api.link_rich_menu_to_user(event.source.uesr_id, 'richmenu-9c87b4194d18802e1234296e5ea0c8d2')
# print(linkResult)

'''

檢視用戶目前所綁定的菜單
    取出用戶id，並告知line_bot_api，
    line_bot_api傳回用戶所綁定的菜單
    印出

'''
#  https://api.line.me/v2/bot/user/{userId}/richmenu
# 查詢特定用戶 所使用的圖文選單
rich_menu_id = line_bot_api.get_rich_menu_id_of_user("Uff25b58196920cabc1ad651c0d0afba2")
# print(rich_menu_id)

