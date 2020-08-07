import json, os, io, sys, re, random, easyquotation, requests, time, base64, optparse
import webbrowser, urllib.request
import sys
sys.path.append('../SDK')
import wx_ai_api_utils,baidu_utils
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from datetime import datetime
from wxpy import *

# jq认证
# jqdatasdk.auth('15902048306', 'jiaojiaodewo')
# all_block_df = jqdatasdk.get_all_securities(types=[], date=None)
robot_running = True
bot = Bot()

# group_1 = bot.groups().search('学习强国')[0]
# group_2 = bot.groups().search('股票小作手')[0]
# group_3 = bot.groups().search('广东云世艺金融中心')[0]
# group_4 = bot.groups().search('Family')[0]
# group_4 = bot.groups().search('Family')[0]
# group_5 = bot.groups().search('佛山')[0]
# group_test = bot.groups().search('AI测试')[0]
# 不用艾特也可以接受消息的群组
# group_free = [group_1,group_2,group_3,group_4,group_test]

# foshan_group = bot.groups().search('图灵测试')
# boss = foshan_group.search(u'Luzz')[0]

group_free = bot.groups()

tuling = Tuling(api_key='14140652801d4be19664ad1c314e50c0')

akey = '3rnZkBSzg5XtyihO'
aid = '2116900501'


def loadReactKeywords():
    f = open("./react_words.json", encoding='utf-8')
    map = json.load(f)
    return map['un_at_word']

def loadprofanity_reply():
    f = open("./react_words.json", encoding='utf-8')
    map = json.load(f)
    return map['profanity_reply']




un_at_react_keyword = loadReactKeywords()
profanity_reply = loadprofanity_reply()

ChinaStockIndexList = [
    "000001",  # sh000001 上证指数
    "399001",  # sz399001 深证成指
    "000300",  # sh000300 沪深300
    "399005",  # sz399005 中小板指
    "399006",  # sz399006 创业板指
    "000003",  # sh000003 B股指数
]

period_All_List = [
    "min",  # 分时线
    "daily",  # 日K线
    "weekly",  # 周K线
    "monthly"  # 月K线
]
period_min = period_All_List[0]
period_daily = period_All_List[1]


def getChinaStockIndexInfo(stockCode, period):
    try:
        exchange = "sz" if (int(stockCode) // 100000 == 3) else "sh"
        # http://hq.sinajs.cn/list=s_sh000001
        dataUrl = "http://hq.sinajs.cn/list=s_" + exchange + stockCode
        stdout = urllib.request.urlopen(dataUrl)
        stdoutInfo = stdout.read().decode('gb2312')
        tempData = re.search('''(")(.+)(")''', stdoutInfo).group(2)
        stockInfo = tempData.split(",")
        # stockCode = stockCode,
        stockName = stockInfo[0]
        stockEnd = stockInfo[1]  # 当前价，15点后为收盘价
        stockZD = stockInfo[2]  # 涨跌
        stockLastEnd = str(float(stockEnd) - float(stockZD))  # 开盘价
        stockFD = stockInfo[3]  # 幅度
        stockZS = stockInfo[4]  # 总手
        stockZS_W = str(int(stockZS) / 100)
        stockJE = stockInfo[5]  # 金额
        stockJE_Y = str(int(stockJE) / 10000)
        content = "#" + stockName + "#" + "(" + str(stockCode) + ")" + " 收盘：" \
                  + stockEnd + "，涨跌：" + stockZD + "，幅度：" + stockFD + "%" \
                  + "，总手：" + stockZS_W + "万" + "，金额：" + stockJE_Y + "亿" + "  "

        imgPath = "http://image.sinajs.cn/newchart/" + period + "/n/" + exchange + str(stockCode) + ".gif"
        twitter = {'message': content, 'image': imgPath}

    except Exception as e:
        print(">>>>>> Exception: " + str(e))
    else:
        return twitter
    finally:
        None


def test_china_index_data():
    for stockCode in ChinaStockIndexList:
        twitter = getChinaStockIndexInfo(stockCode, period_daily)
        print(twitter['message'] + twitter['image'])


def getChinaStockIndexInfo(stockCode, period):
    try:
        exchange = "sz" if (int(stockCode) // 100000 == 3) else "sh"
        # http://hq.sinajs.cn/list=s_sh000001
        dataUrl = "http://hq.sinajs.cn/list=s_" + exchange + stockCode
        stdout = urllib.request.urlopen(dataUrl)
        stdoutInfo = stdout.read().decode('gb2312')
        tempData = re.search('''(")(.+)(")''', stdoutInfo).group(2)
        stockInfo = tempData.split(",")
        # stockCode = stockCode,
        stockName = stockInfo[0]
        stockEnd = stockInfo[1]  # 当前价，15点后为收盘价
        stockZD = stockInfo[2]  # 涨跌
        stockLastEnd = str(float(stockEnd) - float(stockZD))  # 开盘价
        stockFD = stockInfo[3]  # 幅度
        stockZS = stockInfo[4]  # 总手
        stockZS_W = str(int(stockZS) / 100)
        stockJE = stockInfo[5]  # 金额
        stockJE_Y = str(int(stockJE) / 10000)
        content = "#" + stockName + "#" + "(" + str(stockCode) + ")" + " 收盘：" \
                  + stockEnd + "，涨跌：" + stockZD + "，幅度：" + stockFD + "%" \
                  + "，总手：" + stockZS_W + "万" + "，金额：" + stockJE_Y + "亿" + "  "

        imgPath = "http://image.sinajs.cn/newchart/" + period + "/n/" + exchange + str(stockCode) + ".gif"
        twitter = {'message': content, 'image': imgPath}

    except Exception as e:
        print(">>>>>> Exception: " + str(e))
    else:
        return twitter
    finally:
        None


# 获取所有股票信息

def get_global_block_by_msg(msg):
    result = ''
    quotation = easyquotation.use('sina')
    blocks_dict = quotation.market_snapshot(prefix=True)
    global_block = ['sh000001', 'sz399001', 'sh000300', 'sz399005', 'sz399006', 'sh000003']


all_blocknames = []
all_blockcodes = []


def get_allBlockNamesAndCode():
    quotation = easyquotation.use('sina')
    blocks_dict = quotation.market_snapshot(prefix=True)
    flag_a = True if len(all_blocknames) < 1 else False
    flag_b = True if len(all_blockcodes) < 1 else False
    for i in blocks_dict:
        this = blocks_dict[i]
        if flag_a == True:
            name = this['name']
            all_blocknames.append(name)
        if flag_b == True:
            # block_code = re.sub('sh', '', i)
            block_code = i.replace('sh', '')
            block_code = block_code.replace('sz', '')
            all_blockcodes.append(block_code)
    # print(all_blockcodes)

def checkBlockAllNamesAndCodes():
    if len(all_blocknames) == 0 or len(all_blockcodes) == 0:
        get_allBlockNamesAndCode()


def get_blocksInfoByMsg(msg):
    checkBlockAllNamesAndCodes()
    result = ''
    # print(len(all_blocknames))
    for i in range(len(all_blocknames) - 1):
        name = all_blocknames[i]
        code = all_blockcodes[i]
        if name in msg or code in msg:
            result = get_blocks_info_by_msg(msg)
            break
    return result


def get_blocks_info_by_msg(msg):
    result = ''
    quotation = easyquotation.use('sina')
    blocks_dict = quotation.market_snapshot(prefix=True)
    for i in blocks_dict:
        this = blocks_dict[i]
        name = this['name']
        block_code = i.replace('sh', '')
        block_code = block_code.replace('sz', '')
        if name in msg or block_code in msg:
            close = this['close']
            now = this['now']
            status = ''

            volume = float(this['volume']) / 10000000.0

            if now > close:
                up = float('%.2f' % (now - close))
                percent = float('%.2f' % ((up / close) * 100))
                status = '⬆+' + str(round(up, 2)) + '(+' + str(round(percent, 2)) + '%)'
            else:
                down = close - now
                percent = (down / close) * 100
                status = '⬇️-' + str(round(down, 2)) + '(-' + str(round(percent, 2)) + '%)'

            result = name + '(' + i + ')' + '：\n' + '现价:' + str(this['now']) + '，' + status + '，\n昨日收盘价：' + str(
                this['close']) + '，\n开盘价：' + str(
                this['open']) + '，\n今日最高价:' + str(this['high']) + '，\n今日最低价' + str(this['low']) + '，\n交易股数：' + str(
                this['turnover']) + '，\n交易金额：' + str(round(volume, 2)) + '千万'
            return result
            break
    return result


def get_selfie_image_path():
    dir_path = './resource'
    image_names = os.listdir(dir_path)
    index = random.randint(0, len(image_names) - 1)
    return dir_path + '/' + image_names[index]


def get_oneword_everyday():
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content, note


def ask_wx_ai(msg):
    ai_obj = wx_ai_api_utils.AiPlat(aid, akey)
    wxai_sesson_id = '10000'
    msg_string = msg.replace('?', '')
    msg_string = msg_string.replace('@Jarvis ', '')
    msg_string = msg_string.replace('@Jarvis\u2005', '')
    msg_string = msg_string.replace('@星期五 ', '')
    msg_string = msg_string.replace('@星期五\u2005', '')
    msg_string = msg_string.replace('\u2005', '')
    msg_string = msg_string.replace('？', '')
    msg_string = msg_string.replace('!', '')
    msg_string = msg_string.replace('！', '')
    msg_string = msg_string.strip()
    # arr = msg_string.split(' ')
    # msg_string = arr[len(arr)-1]
    # arr_b = msg_string.split('\u2005')
    # msg_string = arr_b[len(arr_b)-1]

    if msg_string == '':
        msg_string = '你好'

    rsp = ai_obj.get_talk_answer(msg_string, wxai_sesson_id)
    if rsp['ret'] == 0:
        return rsp['data']['answer']
    else:
        index = random.randint(0, len(profanity_reply) - 1)
        return profanity_reply[index]

def ask_wx_image(image_path):
    ai_obj = wx_ai_api_utils.AiPlat(aid, akey)
    wxai_sesson_id = '10000'
    rsp = ai_obj.get_image_answer(image_path,wxai_sesson_id)
    return rsp['data']['text']


switch_dict = {}

# def reread_switcharrfromfile():
#     global switch_dict
#     with open('./switch_on.json', 'r') as load_f:
#         tmp = json.load(load_f)
#         if len(tmp)>0:
#             if (type(tmp).__name__ == 'dict'):
#                 switch_dict = tmp


def switch_config(group_name,on):
    # reread_switcharrfromfile()
    global switch_dict
    switch_dict[group_name] = on
    # with open('./switch_on.json', 'w') as f:
    #     json.dump(switch_dict, f)


def check_switch(group_name):
    global switch_dict
    if group_name in switch_dict.keys():
        return switch_dict[group_name]
    else:
        return 1



@bot.register(group_free, msg_types=None)

def auto_reply(msg):
    print(msg)

    if msg.type == TEXT:
        if 'start up' in msg.text or 'startup' in msg.text:
            switch_config(msg.chat.name, 1)
            msg.reply('我回来了~(关闭命令:shutdown)')
            return

    if check_switch(msg.chat.name) == 0:
        return

    if msg.type == TEXT:
        if 'shut down' in msg.text or 'shutdown' in msg.text:
            if check_switch(msg.chat.name) == 1:
                switch_config(msg.chat.name, 0)
                msg.reply('再见~(唤醒命令:startup)')
            return
        elif 'start up' in msg.text or 'startup' in msg.text:
            switch_config(msg.chat.name, 1)
            msg.reply('我又回来了~(关闭命令:shutdown)')
            return
        auto_reply_text(msg)


    else:
        image_dir = './tmp_image/'
        image_path = image_dir + msg.file_name
        print('储存照片路径' + image_path)
        msg.get_file(save_path=image_path)
        detector = baidu_utils.BaiduDetector(image_path)
        detector.general_detect()
        answer = detector.answer()
        if answer != '':
            msg.reply(answer)



def auto_reply_text(msg):
    if isinstance(msg.chat, Group):


        if msg.is_at:
            if '今日鸡汤' in msg.text or '鸡汤' in msg.text:
                msg.reply(get_oneword_everyday())
            if '大盘' in msg.text or '上证' in msg.text or 'a股' in msg.text or 'A股' in msg.text:
                # for stockCode in ChinaStockIndexList:
                #     twitter = getChinaStockIndexInfo(stockCode, period_daily)
                #     msg.reply(twitter['message'] + twitter['image'])
                twitter = getChinaStockIndexInfo('000001', 'daily')
                msg.reply(twitter['message'])
                img_url = twitter['image']
                file_path = '.'
                file_name = 'tmp_image'
                file_suffix = os.path.splitext(img_url)[1]
                print(file_suffix)
                # 拼接图片名（包含路径）
                filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
                print(filename)
                # 下载图片，并保存到文件夹中
                urllib.request.urlretrieve(img_url, filename=filename)
                msg.reply_image(file_path + '/' + file_name, media_id=None)




            else:
                block_reply = get_blocksInfoByMsg(msg.text)
                if block_reply.strip() == '':
                    # tuling.do_reply(msg, False)
                    msg.reply(ask_wx_ai(msg.text))
                else:
                    msg.reply(block_reply)
        else:

            block_reply = get_blocksInfoByMsg(msg.text)
            if block_reply.strip() != '':
                msg.reply(block_reply)

            if '今日鸡汤' in msg.text or '鸡汤' in msg.text:
                msg.reply(get_oneword_everyday())
            elif '发个自拍' in msg.text or '发个照片' in msg.text or '爆照' in msg.text:
                msg.reply_image(get_selfie_image_path(), media_id=None)
            else:
                flag = False
                for keyword in un_at_react_keyword:
                    if keyword in msg.text:
                        flag = True
                        break
                if flag:
                    # tuling.do_reply(msg, False)
                    msg.reply(ask_wx_ai(msg.text))
    else:

        return


embed()

bot.join()
