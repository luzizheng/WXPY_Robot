
import baidu_utils



if __name__ == '__main__':
    dectector = baidu_utils.BaiduDetector('./timg.jpeg')
    dectector.general_detect()
    print(dectector.object_class)
    print(dectector.object_classkeyword)
    print(dectector.object_keyword)
    print(dectector.baike_des)
