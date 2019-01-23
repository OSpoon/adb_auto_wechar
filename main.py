import random
import sys
import time

import xmltodict
from common import common

def adb_click(x, y):
    command = 'shell input tap ' + str(x) + ' ' + str(y)
    print('点击：' + command)
    print(adb.run(command))
    time.sleep(random.uniform(1, 2))


def adb_swipe(x1, y1, x2 ,y2):
    command = 'shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2)
    print('滑动：' + command)
    print(adb.run(command))
    time.sleep(random.uniform(1, 2))


def adb_input(text):
    command = 'shell input text ' + text
    print('输入：' + command)
    print(adb.run(command))
    time.sleep(random.uniform(1, 5))


def adb_dump():
    print('获取布局')
    print(adb.run('shell uiautomator dump'))
    print(adb.run('pull /sdcard/window_dump.xml'))


def adb_key(key):
    command = 'shell input keyevent ' + key
    print('按键：' + command)
    print(adb.run(command))


def analysis(obj):
    if isinstance(obj, dict):

        if obj['@text'] == '添加为熟朋友':
            x1 = float(obj['@bounds'].split('][')[0][1:].split(',')[0])
            y1 = float(obj['@bounds'].split('][')[0][1:].split(',')[1])
            x2 = float(obj['@bounds'].split('][')[1][:-1].split(',')[0])
            y2 = float(obj['@bounds'].split('][')[1][:-1].split(',')[1])

            print('添加为熟朋友')
            adb_click(int(random.uniform(x1, x2)), int(random.uniform(y1, y2)))

            print('确认')
            adb_click(int(random.uniform(558, 966)), int(random.uniform(757, 889)))

            print('返回')
            adb_click(int(random.uniform(0, 150)), int(random.uniform(72, 216)))


        if obj['@text'] == '添加到通讯录':

            x1 = float(obj['@bounds'].split('][')[0][1:].split(',')[0])
            y1 = float(obj['@bounds'].split('][')[0][1:].split(',')[1])
            x2 = float(obj['@bounds'].split('][')[1][:-1].split(',')[0])
            y2 = float(obj['@bounds'].split('][')[1][:-1].split(',')[1])

            print('添加到通讯录')
            adb_click(int(random.uniform(x1, x2)), int(random.uniform(y1, y2)))

            adb_dump()

            with open('window_dump.xml', 'r', encoding='utf-8') as rf:
                window_dump = rf.read()
                if '验证申请' in window_dump:
                    # 解析布局中的申请内容节点
                    analysis(xmltodict.parse(window_dump)['hierarchy']['node'])
                else:
                    print('返回')
                    adb_click(int(random.uniform(26, 98)), int(random.uniform(68, 212)))
                    adb_click(int(random.uniform(26, 98)), int(random.uniform(68, 212)))

        if obj.__contains__('@resource-id'):
            if obj['@resource-id'] == 'com.tencent.mm:id/dx6':
                for item in range(len(obj['@text'])):
                    print('删除字符')
                    adb_key(str(67))

                print('填写申请')
                adb_input('hello')

                print('发送')
                adb_click(int(random.uniform(855, 1035)), int(random.uniform(100, 190)))

                print('返回')
                adb_click(int(random.uniform(26, 98)), int(random.uniform(68, 212)))
                adb_click(int(random.uniform(26, 98)), int(random.uniform(68, 212)))

        if obj.__contains__('node'):
            analysis(obj['node'])

    elif isinstance(obj, list):
        for item in obj:
            analysis(item)


def add_wechar():
    list_phone = ['qq1825203636', 'qq1825203637', '15545825361']

    for item in list_phone:

        phone = item
        print('添加好友：' + phone)

        # 定焦输入框
        print('定焦输入框')
        adb_click(int(random.uniform(50, 1035)), int(random.uniform(280, 370)))

        # 填写微信号
        print('填写微信号')
        adb_input(phone)

        # 搜索好友
        print('搜索好友')
        adb_click(int(random.uniform(55, 190)), int(random.uniform(240, 380)))

        # 获取布局
        adb_dump()

        with open('window_dump.xml', 'r', encoding='utf-8') as rf:
            window_dump = rf.read()
            if '添加到通讯录' in window_dump:
                node_obj = xmltodict.parse(window_dump)['hierarchy']['node']
                analysis(node_obj)
            elif '发消息' in window_dump:
                print('已经是好友了，返回上一页')
                adb_click(int(random.uniform(26, 98)), int(random.uniform(68, 212)))
                print('返回上一页')
                adb_click(int(random.uniform(26, 98)), int(random.uniform(68, 212)))
            elif '该用户不存在' in window_dump:
                print('用户不存在，返回上一页')
                adb_click(int(random.uniform(26, 98)), int(random.uniform(68, 212)))


if sys.version_info.major != 3:
    print('请使用Python3')
    exit(1)
try:
    from common.auto_adb import auto_adb
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)
adb = auto_adb()

VERSION = "0.0.1"

adb.test_device()


def add_ltb():
    adb_swipe(30, 749, 30, 417)
    # 获取布局
    adb_dump()
    with open('window_dump.xml', 'r', encoding='utf-8') as rf:
        window_dump = rf.read()
        if '添加为熟朋友' in window_dump:
            node_obj = xmltodict.parse(window_dump)['hierarchy']['node']
            analysis(node_obj)
        elif '发送消息' in window_dump:
            print('已经是好友了，返回上一页')
            adb_click(int(random.uniform(0, 150)), int(random.uniform(72, 216)))


def add_ltb_main():
    count = 480 / 5

    print(int(count))

    for item in range(int(count)):
        adb_click(int(random.uniform(30, 234)), int(random.uniform(417, 649)))

        add_ltb()

        adb_click(int(random.uniform(234, 438)), int(random.uniform(417, 649)))

        add_ltb()

        adb_click(int(random.uniform(438, 642)), int(random.uniform(417, 649)))

        add_ltb()

        adb_click(int(random.uniform(642, 846)), int(random.uniform(417, 649)))

        add_ltb()

        adb_click(int(random.uniform(846, 1050)), int(random.uniform(417, 649)))

        add_ltb()

        adb_swipe(30, 649, 30, 417)


def news():
    while 1:

        # adb_swipe(24, 375, 24, 1047)
        adb_swipe(24, 1047, 24, 175)

        adb_click(int(random.uniform(24, 1056)), int(random.uniform(375, 475)))# 1047

        adb_swipe(24, 1047, 24, 175)
        adb_swipe(24, 1047, 24, 175)
        adb_swipe(24, 1047, 24, 175)
        adb_swipe(24, 1047, 24, 175)
        adb_swipe(24, 1047, 24, 175)

        adb_dump()
        with open('window_dump.xml', 'r', encoding='utf-8') as rf:
            window_dump = rf.read()
            if 'com.bullet.messenger:id/news_share_outside_btn' in window_dump:
                adb_click(int(random.uniform(0, 150)), int(random.uniform(72, 216)))


def while_send():
    while 1:
        adb_click(int(random.uniform(838, 1030)), int(random.uniform(1155, 1347)))

if __name__ == '__main__':
    # add_ltb_main()
    # while_send()
    common.activation_hei_yu(adb)
