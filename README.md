# MyWeChat
Python+itchat, 一个简单的微信机器人脚本

## 参考工程
Github: [https://github.com/likaixiang/EverydayWechat](https://github.com/likaixiang/EverydayWechat)。
去除了yam配置文件,以及定时任务
定时任务使用 threading.Timer 来实现

## 功能简介

+ 每天定时发送天气信息给好友
+ 图灵机器人自动回复
+ 执行简单的shell命令

## API接口

天气来源: [SOJSON](https://www.sojson.com/blog/305.html)

每日一句: [金山词霸](http://open.iciba.com/?c=api)

AI聊天 : [图灵机器人](http://www.turingapi.com/)

## 目录结构

- `Main.py` : 程序主主入口
- `MyCommand.py` : 自定义的命令
- `Tip.py` : 每日自动播报信息接口,(天气,每日一句)
- `TL.py` : 图灵机器人接口
- `city_dict.py` : 城市代码,用于获取天气信息


## 相关命令
在文件助手里进行输入

+ `帮助` : 获取命令帮助
+ `add 好友名 城市名` : 添加每日播报好友到列表
+ `del 好友名` : 把好友从队列里删除
+ `time xx:xx` : 设置每日播报时间
+ `show user`: 显示每日播报用户列表
+ `shell xxx`: 执行简单的shell命令

## 环境依赖

+ python3.6+
+ itchat
+ requests