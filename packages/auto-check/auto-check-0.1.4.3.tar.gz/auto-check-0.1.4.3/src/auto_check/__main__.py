# -*- coding: UTF-8 -*-
import hashlib
import json
import threading
import time

import requests
try:
    from .auto_checker import AutoChecker
    from .property import Property
    from .parse_params import parse
    from .notice import send, get_log
    from .cuslog import main_msg_list
except ImportError:
    from auto_checker import AutoChecker
    from property import Property
    from parse_params import parse
    from notice import send, get_log
    from cuslog import main_msg_list

thread_list = []

def is_holiday():
    topic = '查询节假日'
    try:
        url = 'http://api.goseek.cn/Tools/holiday?date=' + time.strftime('%Y%m%d', time.localtime())
        resp = requests.get(url).json()
        main_msg_list.append(get_log(topic, resp))
    except Exception as err:
        # 请求接口失败，调用本地日历，进行基本判断
        main_msg_list.append(get_log(topic, '查询API失败，失败原因为：\n' + str(err) + '\n---> 调用本地日历，判断是否为周末'))
        return 5 <= time.localtime()[6] <= 6
    else:
        return resp['data'] == 1 or resp['data'] == 3


def get_check_conf(url):
    topic = '获取配置信息'
    try:
        conf = requests.get(url).json()
    except Exception as err:
        main_msg_list.append(get_log(topic, '获取配置信息失败, 失败原因为:\n' + str(err)))
    else:
        return conf


def main(**kwargs):
    topic = '主流程'
    # 解析参数
    params = parse()
    if params.url == '' and params.config_dir == '':
        main_msg_list.append(get_log(topic, 'No conf info defined, please check again or use -h'))
        return
    # 工作日判定
    main_msg_list.append(get_log(topic,'即将检查是否为节假日'))
    if is_holiday():
        main_msg_list.append(get_log(topic, '节假日, 马上退出'))
        return
    main_msg_list.append(get_log(topic, '工作日'))
    # 优先从网络获取配置参数
    timestr = time.strftime('%Y.%m.%d', time.localtime(time.time())) + 'yysasurai'
    m = hashlib.md5()
    m.update(timestr.encode('utf-8'))
    header = {
        'auth': m.hexdigest()
    }
    if params.url != '':
        try:
            resp = requests.get(params.url, headers=header)
            resp.encoding = 'utf-8'
            configs = json.loads(resp.text)
            print(configs)
            main_msg_list.append(get_log(topic, '获取配置成功, 总数为：' + str(len(configs))))
        except Exception as err:
            main_msg_list.append(get_log(topic, '请求配置数据异常，原因为：\n' + err.__str__()))

        for conf in configs:
            # 若已设置过滤，
            if params.suffix != '':
                if not conf['username'].__contains__(params.suffix):
                    pass
                else:
                    t = threading.Thread(target=AutoChecker(Property(conf), params.test, not params.immediately, params.force).check,
                                         name=conf['username'])
                    t.start()
                    thread_list.append(t)
                    print('matched for %s' % params.suffix)
                    break
            else:
                t = threading.Thread(target=AutoChecker(Property(conf), params.test, not params.immediately, params.force).check,
                                     name=conf['username'])
                t.start()
                thread_list.append(t)
    # 再从本地获取
    elif params.config_dir != '':
        print('local config not supported any more')
        return
        # configs = os.listdir(params.config_dir)
        # os.chdir(params.config_dir)
        #
        # cnt = 0
        # for config_name in configs:
        #     if config_name.__contains__('config_' + params.suffix):
        #         print(config_name)
        #         t = threading.Thread(
        #             target=AutoChecker(Property(config_name), params.test, not (params.immediately)).check,
        #             name=config_name)
        #         t.start()
        #         cnt += 1
        # print('There are ' + str(cnt) + ' configuration file(s) satisfied. ')
    else:
        print('No conf info defined, please check again or use -h')
        return


if __name__ == '__main__':
    main()
    for t in thread_list:
        t.join()
    send('管理员', '932100862@qq.com', ''.join(main_msg_list), '整体打卡')
    print(''.join(main_msg_list))