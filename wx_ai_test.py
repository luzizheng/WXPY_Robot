import sys
sys.path.append('../SDK')
import optparse
import time
import wx_ai_api_utils
import json


app_key = '3rnZkBSzg5XtyihO'
app_id = '2116900501'


if __name__ == '__main__':
    str_text = '你是谁'
    type = 0
    ai_obj = wx_ai_api_utils.AiPlat(app_id, app_key)

    rsp = ai_obj.get_image_answer('./tmp_image','10000')

    print(str(rsp))




