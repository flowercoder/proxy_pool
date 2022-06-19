import csv
import json
import os
import random

import requests
from fake_useragent import UserAgent

curpath = os.path.dirname(os.path.realpath(__file__))


# check proxy by https://httpbin.org/get

def checkhttpsproxy(iport):
    try:
        ip = iport[:iport.find(":")]
        proxy = {
            'http': f'http://{iport}',
            'https': f'https://{iport}'
        }
        # print(proxy)
        ua = UserAgent(verify_ssl=False)
        head = {'User-Agent': ua.random,
                'Connection': 'keep-alive'}
        # https://httpbin.org/get会返回当前的IP地址
        # res = requests.get('https://httpbin.org/get', headers=head, timeout=5)
        res = requests.get('https://httpbin.org/get', headers=head, proxies=proxy, verify=False, timeout=5)
        # print(res.text)
        result = json.loads(res.text)
        response = result['origin']
        # print(f"ip:{ip}-response{response}")
        test = ip == response
        if test == True:
            print(f"proxy:[{iport}],checkresult:[{test}]")
            return iport
        else:
            print(f"proxy:[{iport}],checkresult:[{test}]")
    except:
        print(f"proxy:[{iport}],this proxy does not work!!!")


def operatewrite(ips):
    with open(f"{curpath}/data.csv", 'w') as csvfile:
        fieldnames = ['id', 'address']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 写表头
        # writer.writeheader()
        lines = ips.splitlines()
        for num, line in enumerate(lines, 1):
            print(num, line)
            writer.writerow({'id': num, 'address': line})


def operatereadone():
    total = sum(1 for line in open(f"{curpath}/data.csv"))
    with open('data.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        nnn = random.randint(1, total -1)
        for row in reader:
            if row['id'] == str(nnn):
                return row['address']


if __name__ == '__main__':
    # save_address_into_csv
#     operatewrite("""157.100.12.138:999
# 257.100.12.138:999""")

    # check_address_from_csv
#     checkhttpsproxy("119.76.142.220:8080")

    # check https proxy and save into csv
    # url = 'http://127.0.0.1:5555/allhttps'
    # """
    # https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt
    # """
    # html = requests.get(url, timeout=3)
    # data =""
    # for line in html.text.splitlines():
    #     if checkhttpsproxy(line) != None:
    #         data += line + "\n"
    # print(data)
    # operatewrite(data)

    # get_random_one_https_proxy
    print(operatereadone())
