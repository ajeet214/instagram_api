import asyncio
import concurrent.futures
import requests
import json
from urllib.parse import quote
from bs4 import BeautifulSoup
import demjson
from datetime import datetime
# ----------------------------

startTime = datetime.now()


async def main(loop, urls):
    list2 = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:

        # loop = asyncio.get_event_loop()

        futures = [loop.run_in_executor(executor, requests.get, i)for i in urls]
        for response in await asyncio.gather(*futures):
            # print(response.text)
            temp = {}
            soup1 = BeautifulSoup(response.text, 'lxml')
            body = soup1.find('body')
            scripts = body.find_all('script')[0].get_text()
            if scripts.startswith('window'):
                d = demjson.decode(scripts[21:-1])
                user = d['entry_data']['ProfilePage'][0]['graphql']['user']
                # print(user)

                temp['userid'] = user['username']
                temp['business_phone_number'] = user['business_phone_number']
                temp['following'] = user['edge_follow']['count']
                temp['followers'] = user['edge_followed_by']['count']
                temp['description'] = user['biography']
                temp['image'] = user['profile_pic_url_hd']
                temp['name'] = user['full_name']
                temp['is_business_account'] = user['is_business_account']
                temp['verified'] = user['is_verified']
                temp['business_email'] = user['business_email']
                temp['connected_fb_page'] = user['connected_fb_page']
                temp['is_joined_recently'] = user['is_joined_recently']
                temp['linked_url'] = user['external_url']
                temp['posts'] = user['edge_owner_to_timeline_media']['count']
                temp['business_category_name'] = user['business_category_name']
                temp['business_address_json'] = user['business_address_json']
                temp['url'] = 'https://www.instagram.com/'+user['username']
                list2.append(temp)

                # print(user)
    return list2


class Instagram:

    def __init__(self):

        self.proxy = self._get_proxy()
        self.list1 = []

    def _get_proxy(self):
        url = "http://credsnproxy/api/v1/proxy"
        try:
            req = requests.get(url=url)
            if req.status_code != 200:
                raise ValueError
            return req.json()
        except:
            return {"proxy_host": '185.121.139.55',
                    "proxy_port": '21186'}

    def search_api(self, query, stype=None):

            query = quote(query)
            url = "https://www.instagram.com/web/search/topsearch/?context=blended&query="+query+"&include_reel=true"

            r = requests.get(url, proxies={"http": "socks5://"+self.proxy['proxy_host']+':'+self.proxy['proxy_port']})
            users = json.loads(r.text)
            results = self._insertProfile(users['users'])

            print(self.list1)
            print(len(self.list1))
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(main(loop, self.list1))
            return result


    def _insertProfile(self, r):

        for i in r:
            user = i['user']['username']

            profile_ = "https://www.instagram.com/"+user
            self.list1.append(profile_)


if __name__ == "__main__":
    obj = Instagram()
    print(obj.search_api("chris"))
    print('Task duration: ' + str(datetime.now() - startTime))

