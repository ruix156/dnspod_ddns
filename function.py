import requests
import urllib3
import inspect
import re
import json
from config import node_info, domain, max_offline_times, SCKEY, bark_api
from config import APIID, APITOKEN, record_id, domain_id, sub_domain


def get_variable_name(variable):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is variable]


def get_status_code(ip, domain):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        res = requests.get('http://' + ip, headers={'Host': domain}, verify=False, timeout=5)
        print("IP：" + str(ip) + '｜' + str(res.status_code))
        return res.status_code
    except Exception as e:
        print(e)
        # print('Timeout')
        print('502')
        return 502


def get_node_status(ip, domain):
    status_code = get_status_code(ip, domain)
    if status_code >= 500:
        return 'offline'
    else:
        return 'online'


def get_node_list(node_info):
    node_list = []
    node_dic = locals()
    I = 0
    for node_ip in node_info:
        node_dic['node_' + str(I)] = {}
        node_dic['node_' + str(I)].update(id=I, ip=node_ip, status='online', offline_quota=0)
        # print(node_dic['node_' + str(I)])
        # print(type(node_dic['node_' + str(I)]))
        node_list.append(node_dic['node_' + str(I)])
        # print(node_list)
        # exec('print(node_{}, end=" ")'.format(I))
        # print(type(('node_' + str(I))))
        # ('node_' + str(I)).update(ip=node_ip)
        # print(('node_' + str(I)).ip)
        I += 1
    # print(node_list)
    return node_list


def change_dns(address):
    print('节点变动，即将切换解析节点为：' + str(address))
    post_data = {}
    post_data.update(
        login_token=APIID + "," + APITOKEN, format='json',
        domain_id=domain_id, record_id=record_id, sub_domain=sub_domain,
        value=address, record_line='默认', ttl=600
    )
    POST_URL = 'https://dnsapi.cn/Record.Modify'
    rst = re.match(r'[a-zA-Z]', address)
    if rst is None:
        print('该解析类型为AAAA，即将POST DnsPod API，更改IP地址')
        post_data.update(record_type='A')
        # print(post_data)
        rst = requests.post(POST_URL, data=post_data)
        ret_data = json.loads(rst.text)
        # print(ret_data)
        if '操作已经成功完成' in str(ret_data):
            print('API返回数据：操作成功')
            print('-----------------------------------------')
        else:
            print('API返回数据：操作失败')
            print(ret_data)
            print('-----------------------------------------')
    else:
        print('该解析类型为CNAME，即将POST DnsPod API，更改CNAME地址')
        post_data.update(record_type='CNAME')
        print(post_data)
        rst = requests.post(POST_URL, data=post_data)
        ret_data = json.loads(rst.text)
        # print(ret_data)
        if '操作已经成功完成' in str(ret_data):
            print('API返回数据：操作成功')
        else:
            print('API返回数据：操作失败')
            print(ret_data)


def wechat_push(pattern, now_ip, change_ip):
    POST_URL = 'https://sc.ftqq.com/{}.send'.format(SCKEY)
    if pattern == 1:
        post_data = {'text': '节点故障，解析已自动切换', 'desp': '当前节点: {} 故障，已经切换解析至: {}'.format(now_ip, change_ip)}
    elif pattern == 2:
        post_data = {'text': '节点恢复，解析已自动切换', 'desp': '优先级较高的节点: {} 已恢复，已由{} 切回 '.format(change_ip, now_ip)}
    rst = requests.post(POST_URL, data=post_data)
    # print(rst.text)
    if 'success' in str(rst.text):
        print('微信推送成功')
    else:
        print('微信推送失败')
        print(rst.text)


def bark_push(pattern, now_ip, change_ip):
    if pattern == 1:
        get_url = bark_api + '节点故障，解析已自动切换' + '/' + '当前节点: {} 故障，已经切换解析至: {}'.format(now_ip, change_ip)
    elif pattern == 2:
        get_url = bark_api + '节点恢复，解析已自动切换' + '/' + '优先级较高的节点: {} 已恢复，已由{} 切回 '.format(change_ip, now_ip)
    rst = requests.get(get_url)
    # print(rst.text)
    if '200' in str(rst.text):
        print('IOS推送成功')
    else:
        print('IOS推送失败')
        print(rst.text)



# bark_push(2, '133.333.333.333', '123.cn')


def check_set(node_info, node_list):
    tasks = []
    for i in range(0, len(node_info)):
        # print(node_list[i])
        ip = node_list[i]['ip']
        node_status = get_node_status(ip, domain)
        # print(node_list[i]['offline_quota'])
        # print(node_status)
        # print(node_list[i]['status'])
        # print(node_list[i])
        if node_status == 'offline':
            node_list[i]['offline_quota'] += 1
        else:
            node_list[i]['offline_quota'] -= 1
        if node_list[i]['offline_quota'] < 0:
            node_list[i]['status'] = 'online'
            node_list[i]['offline_quota'] = 0
        if node_list[i]['offline_quota'] > max_offline_times:
            node_list[i]['status'] = 'offline'
            node_list[i]['offline_quota'] = max_offline_times
        # print(node_list[i])
    print('---------------------------')
