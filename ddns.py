from function import get_node_list, change_dns, check_set, wechat_push, bark_push
from config import node_info, sleep_time
import time

print("Nodes Amount: " + str(len(node_info)))

node_list = get_node_list(node_info)

Now_Node = 0

while True:
    try:
        check_set(node_info, node_list)
        # print(node_list)
        # print(node_list[Now_Node]['status'])
        if node_list[Now_Node]['status'] == 'offline':
            for i in range(0, len(node_info)):
                if node_list[i]['status'] == 'online':
                    wechat_push(1, node_list[Now_Node]['ip'], node_list[i]['ip'])
                    bark_push(1, node_list[Now_Node]['ip'], node_list[i]['ip'])
                    print("Already Change DNS From {} To {}，Now IP：{}".format(Now_Node, i, node_list[i]['ip']))
                    Now_Node = i
                    change_dns(node_list[i]['ip'])
                    break
        if node_list[Now_Node]['status'] == 'online':
            for i in range(0, Now_Node):
                if node_list[i]['status'] == 'online':
                    if i < Now_Node:
                        wechat_push(2, node_list[Now_Node]['ip'], node_list[i]['ip'])
                        bark_push(2, node_list[Now_Node]['ip'], node_list[i]['ip'])
                        print("Already Change DNS From {} To {}，Now IP：{}".format(Now_Node, i, node_list[i]['ip']))
                        Now_Node = i
                        change_dns(node_list[i]['ip'])
                        break
    except Exception as e:
        print(e)
    time.sleep(sleep_time)
    # print(f"finished at {time.strftime('%X')}")
