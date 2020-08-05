from aip import AipImageClassify
import json,random
baidu_appid = '16492165'
baidu_apikey = '5LMnk9yA0VHSR7SFZFGWHpGa'
baidu_secretkey = 'SlZosh8CVxpknFVkuTzQzLgtDKOwk5PK'


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


class BaiduDetector(object):
    def __init__(self,image_path):
        self.image_path = image_path
        self.image = get_file_content(image_path)
        self.client = AipImageClassify(baidu_appid, baidu_apikey, baidu_secretkey)
        self.object_class = ''
        self.object_classkeyword = ''
        self.result_string = ''
        self.cls_string = ''
        self.object_keyword = ''
        self.baike_des = ''
        self.ignore_reply = 0

    def config_result(self,result):
        print('二级识别')
        print(result)
        result_arr = result['result']
        self.object_keyword = '按照'+self.cls_string+'属性进行二级识别：'
        for obj in result_arr:
            probability = 0
            if 'probability' in obj.keys():
                probability = float(obj['probability'])
            elif 'score' in obj.keys():
                probability = float(obj['score'])
            percent = probability * 100.0

            if percent == 0:
                self.object_keyword = self.object_keyword + '\n' + '可能是：' + obj['name']
            else:
                self.object_keyword = self.object_keyword + '\n' + str(round(percent, 0)) + '%的可能是：' + obj['name']


        # result_best = result_arr[0]
        # self.object_keyword = result_best['name']
        # baike_info = result_best['baike_info']
        # self.baike_des = baike_info['description']


    def label_detect(self, label,general_result):

        result_arr = general_result['result']
        result_best = result_arr[0]


        if '车' in label:
            print('车')
            self.cls_string = '汽车'
            result = self.client.carDetect(self.image)
            self.config_result(result)
        elif '食物' in label:
            print('食物')
            self.cls_string = '食物'
            result = self.client.dishDetect(self.image)
            self.config_result(result)
        elif 'Logo' in label:
            print('Logo')
            self.cls_string = 'Logo'
            result = self.client.logoSearch(self.image)
            self.config_result(result)
        elif '动物' in label:
            print('动物')
            self.cls_string = '动物'
            result = self.client.animalDetect(self.image)
            self.config_result(result)
        elif '植物' in label:
            print('植物')
            self.cls_string = '植物'
            result = self.client.plantDetect(self.image)
            self.config_result(result)
        elif '地标' in label or '建筑' in label:
            print('地标')
            self.cls_string = '地标'
            result = self.client.landmark(self.image)
            print('二级属性')
            print(result)
            self.object_keyword = ''

            result_obj = result['result']
            if (result_obj is list):
                for obj in result_obj:
                    self.object_keyword = self.object_keyword + obj['landmark'] + '?'
            elif (result_obj is dict):
                self.object_keyword = self.object_keyword + result_obj['landmark'] + '?'

        elif '人物' in label:
            print('人物')
            self.cls_string = '人物'
            self.object_keyword = result_best['keyword']
        else:
            self.object_keyword = result_best['keyword']

    def womengrade(self):
        f = open("./react_words.json", encoding='utf-8')
        map = json.load(f)
        womengrade = map['womengrade']
        index = random.randint(0, len(womengrade) - 1)
        return womengrade[index]


    def general_detect(self):
        result = self.client.advancedGeneral(self.image)
        print('通用识别')
        print(result)
        result_arr = result['result']
        result_best = result_arr[0]

        # baike_info = result_best['baike_info']
        # self.baike_des = baike_info['description']

        label_str = ''
        result_str = '图像识别大类：'
        self.ignore_reply = 0;
        for obj in result_arr:
 #如果大于20%的几率是文字图，屏幕截图，不回答
            score = float(obj['score'])
            percent = score * 100.0
            keyword = obj['keyword']
            if percent > 20 and ('屏幕截图' in keyword or '文字图' in keyword):
                self.ignore_reply = 1
            result_str = result_str + '\n' + str(round(percent, 0)) + '%的可能是：'+ keyword + '(' + obj['root']+')'
            label_str = label_str + obj['root']+'?'+obj['keyword']+'?'


        print('label = '+label_str)

        if self.ignore_reply == 0:
            self.result_string = result_str
            self.object_class = result_best['root']
            self.object_classkeyword = result_best['keyword']
            self.label_detect(label_str, result)
        else:
            print('要忽略显示')


    def answer(self):

        if self.ignore_reply == 1:
            return ''

        cls_arr = self.object_class.split('-')

        # 二级属性
        second_att = ''
        if self.object_keyword != '':
            second_att = '\n'+self.object_keyword
        # answer = '这是'+ self.object_classkeyword +'吧，一种' + cls_arr[len(cls_arr)-1] + second_att
        answer = self.result_string + second_att

        if '女人' in answer or '美女' in answer:
            return self.womengrade()
        else:
            return answer


# if __name__ == '__main__':
#     dectector = BaiduDetector('./car.jpeg')
#     dectector.general_detect()
#     print(dectector.object_class)
#     print(dectector.object_classkeyword)
#     print(dectector.object_keyword)
#     print(dectector.baike_des)