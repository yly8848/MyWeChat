import itchat
import time
import threading
import city_dict
import Tip
import os


class MyCommand:
    """自定义命令类"""

    def run(itchat, msg, config, TLRobot):
        '''命令入口'''
        if msg['Type'] == 'Text':
            text = msg['Text']

            if text == '帮助':
                helps = '1.自动回复\n2.关闭自动回复\n3.add 好友名 城市名\n4.del 好友名\n5.time xx:xx\n6.show user\n7.天气 城市名\n8.char xxx\n9.shell xxx'
                MyCommand.send(helps)
            elif text == u'自动回复':  # 开启自动回复

                config['isAutoRequest'] = True
                MyCommand.send('>>已开启自动回复')

            elif text == u'关闭自动回复':  # 关闭自动回复

                config['isAutoRequest'] = False
                MyCommand.send('>>已关闭自动回复')

            elif text.find('add ') == 0:  # 添加每日播报用户

                MyCommand.send(MyCommand.addUser(
                    itchat, text, config['userlist']))

            elif text.find('del ') == 0:  # 删除每日播报用户

                if len(text) <= 4:
                    MyCommand.send(">>命令错误,格式: del 用户名")
                    return

                name = text.split(' ')[1]
                MyCommand.send(MyCommand.delUser(
                    itchat, name, config['userlist']))

            elif text.find('time ') == 0:  # 设置每日播报时间

                t = text.split(' ')[1]
                flag = MyCommand.getStartTime(t)

                if flag is False:
                    MyCommand.send('>>发生错误!格式错误,例: 10:00')
                else:
                    config['time'] = t
                    config['timer'].cancel()
                    config['timer'] = threading.Timer(flag, config['timefun'])
                    config['timer'].start()
                    MyCommand.send('>>设置每天 %s 发送信息成功!' % t)

            elif text.find('show user') == 0:  # 显示每日播报用户列表

                names = f">>时间: {config['time']}\n"

                if len(config['userlist']) <= 0:

                    names += "用户列表为空"

                else:
                    for x in config['userlist']:
                        names += x + '\n'

                MyCommand.send(names)

            elif text.find('天气 ') == 0:  # 查询天气

                city = text.split(" ")[1]
                city_code = city_dict.city_dict.get(city)

                if city_code is None:
                    MyCommand.send(">>不存在 %s 这个城市" % city)
                else:
                    weather = Tip.get_weather(city_code)
                    MyCommand.send(weather)

            elif text.find('chat ') == 0:  # 与图灵机器人聊天

                data = text.split(' ')[1]
                MyCommand.send(">>%s" % TLRobot.send(data))

            elif text.find('shell ') == 0:  # 执行shell命令

                cmd = text.split(' ')[1]
                data = os.popen(cmd).read()
                MyCommand.send(data)

        else:
            MyCommand.send(">>未知命令")

    def send(msg):
        '''发送信息给文件助手'''
        itchat.send(msg, toUserName='filehelper')

    def search(itchat, name):
        """搜索好友"""
        user = itchat.search_friends(name=name)
        if not user:
            return False
        else:
            return user[0]['UserName']

    def addUser(itchat, text, userlist):
        """添加某个每日播报用户"""
        lists = text.split(" ")

        if len(lists) <= 2:
            return ">>命令错误,格式: add 好友名 城市名"

        name = lists[1]
        username = MyCommand.search(itchat, name)
        citycode = city_dict.city_dict.get(lists[2])

        if username is False:

            return '>>添加 %s 失败,并没有找到这个人' % name

        elif citycode is None:

            return '>>添加城市 %s 失败,并没有找到城市的代码' % lists[2]

        else:
            userlist[name] = [username, citycode]
            return '>>添加 %s %s 成功' % (name, lists[2])

    def delUser(itchat, name, userlist):
        """删除某个每日播报用户"""

        if name in userlist:

            userlist.pop(name)
            return '>>删除 %s 成功' % name

        else:
            return '>>删除 %s 失败,Ta不在列表里' % name

    def getStartTime(tstr):
        '''计算发送时间'''
        try:
            oh = int(tstr.split(':')[0])
            om = int(tstr.split(':')[1])

            # 获取当前的时间
            now = time.strftime("%H:%M", time.localtime())
            h = int(now.split(':')[0])
            m = int(now.split(':')[1])

            t1 = oh - h
            t2 = om - m

            count = 0
            if t1 < 0:
                if t2 < 0:
                    count = (24 + t1) * 60 * 60 + (60 + t2) * 60
                else:
                    count = (24 + t1) * 60 * 60 + t2 * 60
            elif t1 == 0:
                if t2 < 0:
                    count = 23 * 60 * 60 + (60 + t2) * 60
                elif t2 == 0:
                    count = 60 * 60 * 24
                else:
                    count = t2 * 60
            else:
                if t2 < 0:
                    count = t1 * 60 * 60 + (60 + t2) * 60
                else:
                    count = t1 * 60 * 60 + t2 * 60
            return count

        except Exception as e:
            print(e)
            return False
