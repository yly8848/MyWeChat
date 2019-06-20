import itchat
from itchat.content import *
import time
import TL
from MyCommand import MyCommand
import Tip
import threading


TLRobot = TL.Robot()
# 配置项
config = {}


def init():
    '''初始化配置内容'''
    global config
    # 机器人自动回复
    config['isAutoRequest'] = False
    # 每日播报用户列表
    config['userlist'] = {}
    # 每日播报时间
    config['time'] = "7:00"
    # 距离下一次发送信息的
    config['start_time'] = MyCommand.getStartTime(config['time'])
    # 定时任务函数
    config['timefun'] = setTimeout
    # 定时器
    config['timer'] = threading.Timer(config['start_time'], config['timefun'])
    config['timer'].start()


def run():
    '''主程序入口'''
    flag = itchat.auto_login(enableCmdQR=2, hotReload=True)
    print(flag)
    init()
    time.sleep(5)
    itchat.run()


@itchat.msg_register([TEXT, PICTURE, RECORDING])
def get_msg(msg):

    global config
    print(msg)

    if msg['ToUserName'] == 'filehelper':
        MyCommand.run(itchat, msg, config, TLRobot)
    elif config['isAutoRequest']:
        if msg['Type'] == 'Picture':
            return '😒'
        elif msg['Type'] == 'Recording':
            return '别发语言~,我现在不方便听...'
        else:
            return TLRobot.send(msg['Text'])


def setTimeout():
    '''定时任务'''
    global config
    ciba = Tip.get_ciba()

    for i in config['userlist']:
        weather = Tip.get_weather(config['userlist'][i][1])
        msg = f"{weather}\n{ciba}"
        itchat.send(msg, toUserName=config['userlist'][i][0])

    # 重置定时器
    t = 60 * 60 * 24
    config['timer'] = threading.Timer(t, config['timefun'])
    config['timer'].start()


if __name__ == '__main__':
    run()
