import random
import time
import requests
from fake_useragent import UserAgent
import re
import asyncio
import aiohttp
#

UA = UserAgent()



async def foo(num=2):
    await asyncio.sleep(num)
    print('fool')

async def validate_ip(proxy):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://www.trackip.net/ip', headers={'User-Agent': random.choice(UA.random)},proxy=proxy,timeout=8) as response:
                ip_result = await response.text()
                # print(ip_result, proxy)
                if ip_result.strip() in proxy:
                    return proxy
    except Exception as e:

        return False


def get_ip_proxy():
    start = time.time()
    proxy_temp = []

    while len(proxy_temp) < 10:
        ip_addr = ['https://www.kuaidaili.com/free/inha/%s/' % random.randint(1, 10),
                   'http://www.xicidaili.com/nt/%s' % random.randint(1, 10),
                   "http://www.66ip.cn/%s.html" % random.randint(1, 10),
                   "http://www.ip3366.net/free/?stype=1&page=%s" % random.randint(1, 5)]
        ip_url = random.choice(ip_addr)
        print('从[%s]网站中寻找代理ip' % ip_url)
        # print()
        time.sleep(0.1)
        content = requests.get(ip_url, headers={'User-Agent': random.choice(UA.random).strip()},timeout=20).text
        content = re.sub('\s+', '', content)
        ip_port_list = re.findall('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[^\.]*?(\d{1,6})', content)

        tasks = [asyncio.ensure_future(validate_ip('http://' + get_ip + ':' + get_port)) for get_ip, get_port in ip_port_list]
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(asyncio.gather(*tasks))

        for i in result:
            if i  :proxy_temp.append(i)
    print('total_spend_time: %s'%(time.time() - start))
    return proxy_temp





if __name__ == '__main__':


    print(get_ip_proxy())

