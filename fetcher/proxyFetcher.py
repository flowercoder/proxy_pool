# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'

import json
import re
import time
from time import sleep

import requests
from lxml import etree
from fake_useragent import UserAgent

from util.webRequest import WebRequest
from pyquery import PyQuery
import lxml.html


class ProxyFetcher(object):
    # """
    # proxy getter
    # """

    @staticmethod
    def freeProxy01():
        """
        米扑代理 https://proxy.mimvp.com/
        :return:
        """
        url_list = [
            'https://proxy.mimvp.com/freeopen?proxy=in_hp',
            'https://proxy.mimvp.com/freeopen?proxy=out_hp'
        ]
        port_img_map = {'DMxMjg': '3128', 'Dgw': '80', 'DgwODA': '8080',
                        'DgwOA': '808', 'DgwMDA': '8000', 'Dg4ODg': '8888',
                        'DgwODE': '8081', 'Dk5OTk': '9999'}
        for url in url_list:
            html_tree = WebRequest().get(url).tree
            for tr in html_tree.xpath(".//table[@class='mimvp-tbl free-proxylist-tbl']/tbody/tr"):
                try:
                    ip = ''.join(tr.xpath('./td[2]/text()'))
                    port_img = ''.join(tr.xpath('./td[3]/img/@src')).split("port=")[-1]
                    port = port_img_map.get(port_img[14:].replace('O0O', ''))
                    if port:
                        yield '%s:%s' % (ip, port)
                except Exception as e:
                    print(e)

    @staticmethod
    def freeProxy02():
        BASE_URL = 'http://www.66ip.cn/{page}.html'
        MAX_PAGE = 5
        """
        daili66 crawler, http://www.66ip.cn/1.html
        """
        urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]
        for url in urls:
            doc = PyQuery(url)
            trs = doc('.containerbox table tr:gt(0)').items()
            for tr in trs:
                host = tr.find('td:nth-child(1)').text()
                port = int(tr.find('td:nth-child(2)').text())
                yield f"{host}:{port}"


    @staticmethod
    def freeProxy03():
        """ 开心代理 """
        target_urls = ["http://www.kxdaili.com/dailiip.html", "http://www.kxdaili.com/dailiip/2/1.html"]
        for url in target_urls:
            tree = WebRequest().get(url).tree
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                yield "%s:%s" % (ip, port)

    # @staticmethod
    # def freeProxy04():
    #     """ 蝶鸟IP """
    #     url = "https://www.dieniao.com/FreeProxy.html"
    #     tree = WebRequest().get(url, verify=False).tree
    #     for li in tree.xpath("//div[@class='free-main col-lg-12 col-md-12 col-sm-12 col-xs-12']/ul/li")[1:]:
    #         ip = "".join(li.xpath('./span[1]/text()')).strip()
    #         port = "".join(li.xpath('./span[2]/text()')).strip()
    #         yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy05(page_count=1):
        """ 快代理 https://www.kuaidaili.com """
        url_pattern = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]
        url_list = []
        for page_index in range(1, page_count + 1):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    # @staticmethod
    # def freeProxy06():
    #     """ PROXY11 https://proxy11.com """
    #     url = "https://proxy11.com/api/demoweb/proxy.json?country=hk&speed=2000"
    #     try:
    #         resp_json = WebRequest().get(url).json
    #         for each in resp_json.get("data", []):
    #             yield "%s:%s" % (each.get("ip", ""), each.get("port", ""))
    #     except Exception as e:
    #         print(e)

    @staticmethod
    def freeProxy07():
        """ 云代理 """
        urls = ['http://www.ip3366.net/free/?stype=1&page=1', "http://www.ip3366.net/free/?stype=1&page=2"]
        for url in urls:
            r = WebRequest().get(url, timeout=3)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy08():
        """ 小幻代理 """
        url = 'https://ip.ihuan.me/address/5Lit5Zu9.html'
        urls =[url]
        html = WebRequest().get(url, timeout=3)
        tree = lxml.html.fromstring(html.text)
        for i in range(3, 7):
            title = tree.cssselect(f'nav >ul>li:nth-child({i}) > a')[0].get('href')
            newurl = f'{url}/{title}'
            urls.append(newurl)
            # yield title
        for url in urls:
            r = WebRequest().get(url, timeout=3)
            sleep(5)
            proxies = re.findall(r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

        # urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
        # for url in urls:
        #     r = WebRequest().get(url, timeout=3)
        #     proxies = re.findall(r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>', r.text)
        #     for proxy in proxies:
        #         yield ":".join(proxy)


    # @staticmethod
    # def freeProxy09(page_count=1):
    #     """ 免费代理库 """
    #     for i in range(1, page_count + 1):
    #         url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(i)
    #         html_tree = WebRequest().get(url).tree
    #         for index, tr in enumerate(html_tree.xpath("//table//tr")):
    #             if index == 0:
    #                 continue
    #             yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    # @staticmethod
    # def freeProxy10():
    #     """ 89免费代理 """
    #     urls = ['https://www.89ip.cn/index_1.html', "https://www.89ip.cn/index_2.html", "https://www.89ip.cn/index_3.html", "https://www.89ip.cn/index_4.html", "https://www.89ip.cn/index_5.html"]
    #     for url in urls:
    #         r = WebRequest().get(url, timeout=3)
    #         proxies = re.findall(
    #             r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
    #             r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    # @staticmethod
    # def wallProxy01():
    #     """
    #     PzzQz https://pzzqz.com/
    #     """
    #     from requests import Session
    #     from lxml import etree
    #     session = Session()
    #     try:
    #         index_resp = session.get("https://pzzqz.com/", timeout=20, verify=False).text
    #         x_csrf_token = re.findall('X-CSRFToken": "(.*?)"', index_resp)
    #         if x_csrf_token:
    #             data = {"http": "on", "ping": "3000", "country": "cn", "ports": ""}
    #             proxy_resp = session.post("https://pzzqz.com/", verify=False,
    #                                       headers={"X-CSRFToken": x_csrf_token[0]}, json=data).json()
    #             tree = etree.HTML(proxy_resp["proxy_html"])
    #             for tr in tree.xpath("//tr"):
    #                 ip = "".join(tr.xpath("./td[1]/text()"))
    #                 port = "".join(tr.xpath("./td[2]/text()"))
    #                 yield "%s:%s" % (ip, port)
    #     except Exception as e:
    #         print(e)

    # @staticmethod
    # def freeProxy10():
    #     """
    #     墙外网站 cn-proxy
    #     :return:
    #     """
    #     urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=3)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    # @staticmethod
    # def freeProxy12():
    #     urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=3)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    @staticmethod
    def freeProxy13():

        ua = UserAgent(verify_ssl=False)
        headers = {
            'User-agent': ua.random
        }
        payload = {}
        urls = ['https://www.beesproxy.com/free/page/1', "https://www.beesproxy.com/free/page/2", "https://www.beesproxy.com/free/page/3", "https://www.beesproxy.com/free/page/4"]
        for url in urls:
            response = requests.request("GET", url, headers=headers, data=payload, timeout=2000)
            page = etree.HTML(response.text)

            for i in range(1, 20):
                j = str(i)
                ip = page.xpath(
                    '/html/body/div[2]/section[1]/div/div/div/div[1]/div/article/div[2]/div/figure/table/tbody/tr[' + j + ']/td[1]/text()')
                port = page.xpath(
                    '/html/body/div[2]/section[1]/div/div/div/div[1]/div/article/div[2]/div/figure/table/tbody/tr[' + j + ']/td[2]/text()')
                res = f"{ip[0]}:{port[0]}"
                yield res

    # @staticmethod
    # def freeProxy14():
    #     url = "https://www.beesproxy.com/free/page/1"
    #
    #     ua = UserAgent(verify_ssl=False)
    #     headers = {
    #         'User-agent': ua.random
    #     }
    #     payload = {}
    #     response = requests.request("GET", url, headers=headers, data=payload, timeout=2000)
    #     page = etree.HTML(response.text)
    #
    #     for i in range(1, 20):
    #         j = str(i)
    #         ip = page.xpath(
    #             '/html/body/div[2]/section[1]/div/div/div/div[1]/div/article/div[2]/div/figure/table/tbody/tr[' + j + ']/td[1]/text()')
    #         port = page.xpath(
    #             '/html/body/div[2]/section[1]/div/div/div/div[1]/div/article/div[2]/div/figure/table/tbody/tr[' + j + ']/td[2]/text()')
    #         res = f"{ip[0]}:{port[0]}"
    #         yield res

    @staticmethod
    def freeProxy15():
        """ 云代理 """
        urls = ["https://proxypool.scrape.center/all"]
        for url in urls:
            respone = WebRequest().get(url, timeout=3)
            lines = re.split('\r',str(respone.text))
            # lines = json(respone.text)
            for line in lines:
                yield ":".join(lines)

    # @staticmethod
    # def abroadProxy11():
    #     """
    #     https://proxy-list.org/english/index.php
    #     :return:
    #     """
    #     urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 5)]
    #     request = WebRequest()
    #     import base64
    #     for url in urls:
    #         r = request.get(url, timeout=3)
    #         proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
    #         for proxy in proxies:
    #             yield base64.b64decode(proxy).decode()

    # @staticmethod
    # def freeProxy15():
    #     """ 云代理 """
    #     urls = ["http://127.0.0.1:5555/all"]
    #     for url in urls:
    #         respone = WebRequest().get(url, timeout=3)
    #         lines = re.split('\r',str(respone.text))
    #
    #         # lines = json(respone.text)
    #         for line in lines:
    #             yield ":".join(lines)

    @staticmethod
    def freeProxy16():
        """
        Fatezero crawler,http://proxylist.fatezero.org
        """
        BASE_URL = 'http://proxylist.fatezero.org/proxy.list'
        request = WebRequest().get(BASE_URL, timeout=8)
        hosts_ports = request.text.split('\n')
        for addr in hosts_ports:
            if (addr):
                ip_address = json.loads(addr)
                host = ip_address['host']
                port = ip_address['port']
                yield f"{host}:{port}"

    # @staticmethod
    # def freeProxy17():
    #     BASE_URL = 'http://www.goubanjia.com/'
    #     MAX_PAGE = 1
    #     """
    #     ip  Goubanjia crawler, http://www.goubanjia.com/
    #     """
    #     urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]
    #     for url in urls:
    #         print(url)
    #         doc = PyQuery(url)('.ip').items()
    #         # ''.join([*filter(lambda x: x != '',re.compile('\>([\d:\.]*)\<').findall(td.html()))])
    #         for td in doc:
    #             trs = td.children()
    #             ip_str = ''
    #             for tr in trs:
    #                 attrib = tr.attrib
    #                 if 'style' in attrib and 'none' in tr.attrib['style']:
    #                     continue
    #                 ip_str += '' if not tr.text else tr.text
    #             addr_split = ip_str.split(':')
    #             if (len(addr_split) == 2):
    #                 host = addr_split[0]
    #                 port = addr_split[1]
    #                 yield f"{host}:{port}"
    #             else:
    #                 port = trs[-1].text
    #                 host = ip_str.replace(port, '')
    #                 yield f"{host}:{port}"

    @staticmethod
    def freeProxy18():
        BASE_URL = 'https://ip.ihuan.me/today/{path}.html'
        """
        ip  ihuan crawler, https://ip.ihuan.me
        """
        path = time.strftime("%Y/%m/%d/%H", time.localtime())
        url = BASE_URL.format(path=path)
        ignore = False
        request = WebRequest().get(url, timeout=3)
            # doc = PyQuery(url)('.text-left')
        ip_address = re.compile('([\d:\.]*).*?<br>')
        hosts_ports = ip_address.findall(request.text)
        for addr in hosts_ports:
            addr_split = addr.split(':')
            if (len(addr_split) == 2):
                host = addr_split[0]
                port = addr_split[1]
                yield f"{host}:{port}"

    @staticmethod
    def freeProxy19():
        """
        seo方法 crawler, https://proxy.seofangfa.com/
        """
        url = "https://proxy.seofangfa.com/"
        requests = WebRequest().get(url, timeout=5)
        doc = PyQuery(requests.text)
        trs = doc('.table tr:gt(0)').items()
        for tr in trs:
            host = tr.find('td:nth-child(1)').text()
            port = int(tr.find('td:nth-child(2)').text())
            yield f"{host}:{port}"

    @staticmethod
    def freeProxy20():
        BaseUrl = 'http://www.taiyanghttp.com/free/page{num}'
        MAX_PAGE = 3
        """
        taiyangdaili crawler, http://www.taiyanghttp.com/free/
        """
        urls = [BaseUrl.format(num=i) for i in range(1, 6)]
        for url in urls:
            doc = PyQuery(url)
            trs = doc('#ip_list .tr.ip_tr').items()
            for tr in trs:
                host = tr.find('div:nth-child(1)').text()
                port = tr.find('div:nth-child(2)').text()
                yield f"{host}:{port}"

    # @staticmethod
    # def freeProxy21():
    #     PAGE_BASE_URL = "https://www.xsdaili.cn/index.php"
    #     """
    #     小舒代理 crawler, http://www.xsdaili.cn/
    #     """
    #     html = WebRequest().get(PAGE_BASE_URL, timeout=3)
    #     tree = lxml.html.fromstring(html.text)
    #     title = tree.cssselect('div.title > a')[0].get('href')
    #
    #     print(title)
    #     values = re.findall(r"\d+", title)
    #     value = values[0]
    #     print(value)
    #     website = 'https://www.xsdaili.cn/dayProxy/ip/'
    #     yield website
    #     for i in range(int(value),int(value)+2):
    #         yield i
    #         page = f"{website}{i}.html"
    #         yield page
    #         html = WebRequest().get(page, timeout=3)
    #         tree = lxml.html.fromstring(html.text)
    #         yield tree.text_content()

    # @staticmethod
    # def freeProxy21():
    #     url = 'https://www.zdaye.com/dayProxy/1.html'
    #     """
    #     zhandaye crawler, https://www.zdaye.com/dayProxy/
    #     """
    #     html = WebRequest().get(url, timeout=3)
    #     print(html.text)
    #     tree = lxml.html.fromstring(html.text)
    #     # print(tree.text_content())
    #     title = tree.cssselect('div > h3 > a')[0].get('href')
    #     values = re.findall(r"\d+", title)
    #     value = values[0]
    #     print(value)
    #     webhtml ='https://www.zdaye.com/dayProxy/ip/'
    #     for i in range(int(value)-2,int(value)+1):
    #         yield i
    #         page = f"{webhtml}{i}.html"
    #         yield page
    #         html = WebRequest().get(page, timeout=3).tree
    #         print("==========================")
    #         print(html.text)
    #         # ips = html.xpath('/html/body/div[3]/div/div[2]/div/div[5]/table/tbody/tr[1]/td[1]')
    #         # ports = html.xpath('/html/body/div[3]/div/div[2]/div/div[5]/table/tbody/tr[1]/td[2]')
    #
    #         # tree = lxml.html.fromstring(html.text)
    #         # yield f'{ips}:{ports}'

    @staticmethod
    def freeProxy22():
        url = 'https://gh.api.99988866.xyz/https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt'
        """
        https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt
        """
        html = WebRequest().get(url, timeout=3)
        for line in html.text.splitlines():
            yield line



if __name__ == '__main__':
    p = ProxyFetcher()
    # p.freeProxy15()
    # p.freeProxy21()
    for _ in p.freeProxy22():
        print(_)



# http://nntime.com/proxy-list-01.htm