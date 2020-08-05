import hashlib
import urllib.request
# import urllib2
import base64
import json
import time

url_preffix='https://api.ai.qq.com/fcgi-bin/'
app_key = '3rnZkBSzg5XtyihO'
app_id = '2116900501'

def set_params(array, key, value):
    array[key] = value

def gen_sign_string(parser):
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, urllib.parse.quote(str(parser[key]), safe = ''))
    sign_str = uri_str + 'app_key=' + parser['app_key']
    hash_md5 = hashlib.md5(sign_str.encode('utf-8'))
    return hash_md5.hexdigest().upper()


class AiPlat(object):
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.data = {}
        # self.url_data = {}
        # self.url = ''

    def invoke(self, params):

        # self.url_data = urllib.parse.urlencode(params)
        data = urllib.parse.urlencode(params).encode("utf-8")
        print(self.url)
        print('params = ' + str(self.data))
        req = urllib.request.Request(self.url, data)
        rsp = urllib.request.urlopen(req)
        str_rsp = rsp.read()
        dict_rsp = json.loads(str_rsp)
        return dict_rsp

    def get_talk_answer(self, text, sesson_id):
        self.url = url_preffix + 'nlp/nlp_textchat'
        set_params(self.data, 'app_id', app_id)
        set_params(self.data, 'app_key', app_key)
        set_params(self.data, 'time_stamp', int(time.time()))
        set_params(self.data, 'nonce_str', int(time.time()))
        if sesson_id == '':
            set_params(self.data, 'session', '10000')
        else:
            set_params(self.data, 'session', sesson_id)
        set_params(self.data, 'question', text)
        sign_str = gen_sign_string(self.data)
        set_params(self.data, 'sign', sign_str)

        return self.invoke(self.data)

    def get_image_answer(self,image_path,sesson_id):

        # encodestr = ''
        # with open(image_path,'rb') as f:
        #     data = f.read()
        #     encodestr = base64.b64encode(data).decode("utf-8")
        #
        f = open(image_path,'rb')
        base64_data = base64.b64encode(f.read()).decode('utf-8')


        self.url = 'https://api.ai.qq.com/fcgi-bin/vision/vision_imgtotext'
        set_params(self.data,'app_id',app_id)
        set_params(self.data, 'app_key', app_key)
        set_params(self.data, 'time_stamp', int(time.time()))
        set_params(self.data, 'nonce_str', int(time.time()))
        if sesson_id == '':
            set_params(self.data, 'session_id', '10000')
        else:
            set_params(self.data, 'session_id', sesson_id)
        set_params(self.data,'image',base64_data)
        # set_params(self.data,'scene','word')
        # set_params(self.data,'source','en')
        # set_params(self.data,'target','zh')

        sign_str = gen_sign_string(self.data)
        set_params(self.data, 'sign', sign_str)
        return self.invoke(self.data)