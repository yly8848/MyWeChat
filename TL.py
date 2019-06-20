import requests
import json
import time
import re


class Robot:
    """图灵机器人接口"""

    def __init__(self):

        # 头信息
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
            "Cookie": "UM_distinctid=16b45de44ea67a-03c8e23878003-4d045769-1fa400-16b45de44eb716; gr_session_id_a879f15d23a9b5f0=3597bd1f-45cc-407c-9767-e55cf31c843d; gr_session_id_a879f15d23a9b5f0_3597bd1f-45cc-407c-9767-e55cf31c843d=true; gr_user_id=0f3e3c46-0fec-4571-b9a6-6381b9f1f42f; CNZZDATA1000214860=994853796-1560245320-null%7C1560772001; login-token=BfVxWx-DeYRLEsCOVF8U1UJaq3LOgWlOuBOj9y01mPpyN42z5d-gdzxzl4ve6Uj1_JXmqDUuGSXRy7lO14_-uSJcYSLFfqW3x49yr6auSTqW4W0UjNC-LcYK_u46UjYt777Vnao9TJ1TV0flmtQ8s-kRBiN5AEBZ8hXCEHc29jSDct8WDxUPX4bBZKs97m6FqH_OrdhWKAmVXDfEAZRfVQ7Cn7brkLAclB2c95v2UBQHRgAYbQOSSvDE0o2wRB70kn-GUx6Y30RdCn-_rIVZ8mNNv3nB7nfJFDBRK4i7O5f5aoJ9szqDluFIKZH7TRxcOlQxK67_NE-GTjZRmGxgwdwNheCKvjxFgGhrFa6dx6U6tMiG4B_sERTPlRZylz7gkrp8xDDtOB7esNHzbDhLrGzabY2rprj93NbgRR-DvKe0PPw.; JSESSIONID=E0E7E2CD64AC8C73AC76754CCAA2C989",
            'Referer': 'http://www.tuling123.com/member/robot/1788547/center/frame.jhtml?page=1&child=0',
            'DNT': '1',
        }

        self.session = self.getSession()

    def getSession(self):
        session = requests.Session()
        session.headers.update(self.headers)
        return session

    def init(self):
        """通过访问连接获取一次请求次数"""
        self.session.get(
            "http://www.tuling123.com/member/robot/1788547/kb/list?page=1&child=0")

    def send(self, msg):
        """向接口发送信息并返回内容"""
        send = {
            "perception": {
                "inputText": {"text": msg}
            },
            "userInfo": {
                "userId": "demo"
            }
        }
        # 初始化获取次数
        self.init()

        url = "http://www.tuling123.com/robot-chat/robot/chat/534427/vDMM?geetest_challenge=&geetest_validate=&geetest_seccode="
        data = self.session.post(url, data=json.dumps(send)).json()
        text = data['data']['results'][0]['values']['text']

        if text == '请求次数超限制!':  # 让爱客服去挺着
            return akf(msg)

        return text


def akf(msg):  # 爱客服接口
    t = time.time()
    t = str(int(round(t * 1000)))
    url = "http://www.aikf.com/ask/getAnswer.htm?&reqtype=1&tenantId=78837bf4eb9a4e068c678eb31b3da4c2&ques=" + msg + "&_=" + t
    r = requests.get(url).json()
    answer = r['text']['content']
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', answer)
    return dd


def char():
    rbt = Robot()
    while True:
        msg = input('>>')
        print('图灵:', rbt.send(msg))


def test():
    rbt = Robot()
    msg = rbt.send("你好")
    print("图灵:", msg)
    while True:
        msg = akf(msg)
        print("爱客服:", msg)
        msg = rbt.send(msg)
        print("图灵:", msg)


if __name__ == '__main__':
    # 聊天
    char()
    # 爱客服 & 图灵 对聊
    # test()
