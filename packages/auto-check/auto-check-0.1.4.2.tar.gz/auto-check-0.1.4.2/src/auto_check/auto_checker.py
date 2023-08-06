# -*- coding: UTF-8 -*-
import enum
import json

import requests
import time
import datetime
import random

try:
    from .notice import send, get_log
    from .cuslog import main_msg_list
except ImportError:
    from notice import send, get_log
    from cuslog import main_msg_list

msg_list = []
class WaitType(enum.Enum):
    # 前面为方法名，后面为最大等待时间(单位：min)
    CHECK_IN = 'checkin', 11, '签到'
    CHECK_OUT = 'checkout', 50, '签退'
    LOGIN = '', 0.5, '登录'


def wait(check_type, delay, delay_min=0):
    topic = '{0}暂停'.format(check_type.value[2])
    if delay_min == 0:
        delay_min = check_type.value[1]

    # 最少要延迟20s
    t = random.randint(10, delay_min * 60)
    if check_type == WaitType.LOGIN or delay:
        #print('\n\twill be waiting for ' + str(t) + ' seconds!\n')
        msg_list.append(get_log(topic, '暂停' + str(t) + '秒!'))
        time.sleep(t)
    else:
        msg_list.append(get_log(topic, '跳过暂停'))


class AutoChecker:
    __check_headers = {
        'User-Agent': 'E-MobileE-Mobile 6.5.64 (iPhone; iOS 12.1; zh_CN)',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive',
    }

    def __init__(self, config, test, delay, force):
        self.__udid = config.get_property('udid')
        self.__username = config.get_property('username')
        self.__password = config.get_property('password')
        self.__latlng = config.get_property('latlng')
        self.__addr = config.get_property('addr')
        self.__server = config.get_property('server')
        self.__notice = config.get_property('notification')

        try:
            self.__client_agent = config.get_property('agent')
            self.__client_type = config.get_property('client_type')
            self.__client_os = config.get_property('client_os')
        except Exception:
            self.__client_agent = 'E-MobileE-Mobile 6.5.64 (iPhone; iOS 12.1; zh_CN)'
            self.__client_type = 'iPhone'
            self.__client_os = 'iOs'



        self.__test = test
        self.__delay = delay
        self.__off_delay = config.get_property('check_delay')
        self.__force= force
        self.sessionkey = ''

    def __get_cio_cookie(self, user_key='', session_id='', user_id='1'):
        return dict([('ClientCountry', 'CN'), ('ClientLanguage', 'zh-Hans'), ('ClientMobile', ''), ('ClientToken', ''),
                     ('ClientType', self.__client_type), ('ClientUDID', self.__udid), ('ClientVer', '6.5.64'),
                     ('JSESSIONID', session_id),
                     ('Pad', 'false'), ('setClientOS', self.__client_os), ('setClientOSVer', '12.1'), ('userKey', user_key),
                     ('userid', user_id)])

    def __check_inout(self, check_type):
        # 先等待，营造随机效果
        # 如果需要延时
        wait(check_type, self.__delay, self.__off_delay)

        # 登录获取cookie
        args = self.__login()
        topic = check_type.value[2]
        url = 'https://' + self.__server + '/client.do?method=checkin&type=' + check_type.value[0] + '&latlng=' + self.__latlng + '&addr=' + self.__addr + '&sessionkey=' + self.__sessionkey
        query_url = 'https://' + self.__server + '/client.do?method=checkin&type=getStatus&sessionkey=' + self.__sessionkey

        try:
            # 登录后等待一段时间
            wait(WaitType.LOGIN, self.__delay)
            checked = False
            if check_type == WaitType.CHECK_IN:
                # 签到，进行检查，如果已签到过，则不再进行签到
                try:
                    resp = requests.get(query_url, headers=self.__check_headers, cookies=self.__get_cio_cookie(args['user_key'], args['session_id'], args['user_id']))
                    resp.encoding = 'utf-8'
                    rj = resp.json()
                    if rj['signbtns'][0]['sign']:
                        checked = True
                        msg_list.append(get_log(topic, '检测到已{0}，即将退出'.format(check_type.value[2])))
                    else:
                        msg_list.append(get_log(topic,'未{0}，马上{1}'.format(check_type.value[2], check_type.value[2])))
                except Exception as err:
                    msg_list.append(get_log(topic, '获取签到信息失败, 失败原因为：\n' + err.__str__()))
            if not self.__test and not checked:
                r = requests.get(url, headers=self.__check_headers, cookies=self.__get_cio_cookie(args['user_key'], args['session_id'], args['user_id']))
                msg_list.append(get_log(topic, '【{0}】，结果为：\n{1}'.format(check_type.value[2], r.text)))
            elif self.__test:
                msg_list.append(get_log(topic, '{0}测试 -> 测试URL为：{1}'.format(check_type.value[2], url)))
        except Exception as e:
            msg_list.append(get_log(topic, '【{0}失败】，原因为：\n\t{1}'.format(check_type.value[2], e)))
        finally:
            if self.__notice is not None and self.__notice != '':
                send(self.__username, self.__notice, "".join(msg_list), check_type.value[2])
            main_msg_list.extend(msg_list.__iter__())
            print("".join(msg_list))
            msg_list.clear()


    # 登录获取最新cookie
    def __login(self):
        topic = '登录'
        headers = {
            'Host': self.__server,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Proxy-Connection': 'close',
            'Timezone': 'GMT+8',
            'User-Agent': self.__client_agent,
            'Content-Length': '25',
            'Accept-Encoding': 'gzip',
            'Connection': 'close'
        }
        url = 'https://' + self.__server + '/client.do?method=login&udid=' + \
              self.__udid + \
              '&token=&language=zh-Hans&country=CN&isneedmoulds=1&clienttype=' + \
              self.__client_type +\
              '&clientver=6.5.64&clientos=' + \
              self.__client_os + ''
        data = {
            'loginid': self.__username,
            'password': self.__password
        }
        r = requests.post(url, data=data, headers=headers, cookies=self.__get_cio_cookie(), timeout=2)
        try:
            cookies = dict([('user_key', r.cookies['userKey']), ('session_id', r.cookies['JSESSIONID']),
                     ('user_id', r.cookies['userid'])])
            self.__sessionkey = r.json()['sessionkey']
            # print(self.__username + ' -- ' + str(cookies))
            msg_list.append(get_log(topic, '登录成功'))
            return cookies
        except Exception as e:
            msg_list.append(get_log(topic, '【' + self.__username + '】' + '登录失败，原因为：\n' + r.text))
            raise Exception('登录失败, 原因为：\n{0}\n{1}'.format(e, r.text))

    # 延时等待
    def check(self):
        # 获取当前时间
        current_time = int((datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%H'))
        # 根据时间进行判断进行签到、签退
        if 8 <= current_time <= 9:
            print('签到({}):'.format(self.__username))
            self.__check_inout(WaitType.CHECK_IN)
        elif 18 <= current_time <= 20:
            print('签退({}):'.format(self.__username))
            self.__check_inout(WaitType.CHECK_OUT)
        elif self.__test:
            print('\n--\tTest({}):\t--\n'.format(self.__username))
            self.__check_inout(WaitType.CHECK_IN)
            self.__check_inout(WaitType.CHECK_OUT)
        elif self.__force and current_time >= 18:
            print('强制签退:({})'.format(self.__username))
            self.__check_inout(WaitType.CHECK_OUT)
        else:
            print('\n\t{}--不在正常时间内，不建议进行签到/退操作。\n'.format(self.__username))
            
