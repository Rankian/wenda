from PIL import ImageGrab,Image
from aip import AipOcr
import webbrowser,time,os,requests,urllib.parse,configparser,msvcrt

def start():
    # 电脑截屏
    # pic=ImageGrab.grab()
    # pic.save('pic.png')

    # Win+Android执行adb命令截屏
    os.system('adb shell /system/bin/screencap -p /sdcard/screenshot.png')
    os.system('adb pull /sdcard/screenshot.png pic.png')

    # Mac+ios截屏
    # wda.Client().screenshot('pic.png')

    # 打开本地图片
    open_img=Image.open('pic.png')

    # 读取配置
    config=configparser.ConfigParser()
    pixels=''
    with open('config.conf','r') as cfgfile:
        config.readfp(cfgfile)
        left=config.get('pixels','left')
        top=config.get('pixels','top')
        right=config.get('pixels','right')
        bottom=config.get('pixels','bottom')

    # 开始截取问题区域图片
    question_img=open_img.crop((int(left),int(top),int(right),int(bottom)))

    # 保存问题区域图片
    question_img.save('question.png')

    # 百度ORC APPID,AK,SK
    APP_ID='10665196'
    API_KEY='Vzts1FQORkGMydqNyWieFdX6'
    SECRET_KEY ='43k9OGgOcj5RZOQe0KXmdmKeeKTUXonT'
    clicent=AipOcr(APP_ID,API_KEY,SECRET_KEY)

    #读取图片
    def get_img_content(filePath):
        with open(filePath,'rb') as fp:
            return fp.read()

    # 读取问题区域图片
    question_image=get_img_content('question.png')

    # 调用通用文字识别, 图片参数为本地图片
    qusetion_image_text=clicent.basicGeneral(question_image)

    # 提取问题
    question=''
    for i in qusetion_image_text['words_result']:
        question += i['words']

    # 过滤字符
    # 查找第一个字符‘.’，返回键值s
    dot_num=question.find('.')
    if dot_num>-1:
        question=question[dot_num+1:]

    print(question)
    result=urllib.parse.quote(question)

    # 百度搜索
    webbrowser.open('https://www.baidu.com/s?wd={}'.format(result))

def next_question():
    while (True):
        print(u"\nENTER 下一题 ,ESC 退出:")
        key=msvcrt.getch()
        os.system('cls')
        if ord(key) == 27:  # Esc
            print('答题结束')
            break
        elif ord(key) == 13:  # enter
            start()

next_question()