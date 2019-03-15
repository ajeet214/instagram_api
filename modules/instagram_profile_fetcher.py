#!/usr/bin/env python
import requests
from credentials import creds


class ProfileFetcher:

    def __init__(self):

        self.proxy = self._get_proxy()

        self.header = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'accept-language': 'en-US,en;q=0.9'
                 }

        self.jar = requests.cookies.RequestsCookieJar()

        for cookie in creds['cookies']:
            # print(cookie)
            self.jar.set(domain=cookie['domain'], value=cookie["value"], path=cookie['path'], name=cookie['name'])

    # get proxy
    def _get_proxy(self):

        url = "http://credsnproxy/api/v1/proxy"
        try:
            creds = requests.get(url=url).json()

        except:
            return {
                "proxy_host": '5.39.20.153',
                "proxy_port": '25567'
            }

    def data_processor(self, data):

        temp = dict()
        user = data['graphql']['user']

        temp['userid'] = user['username']
        temp['business_phone_number'] = user['business_phone_number']
        if not temp['business_phone_number']:
            temp['business_phone_number'] = None

        temp['following'] = user['edge_follow']['count']
        temp['followers'] = user['edge_followed_by']['count']
        temp['description'] = user['biography']
        if not temp['description']:
            temp['description'] = None

        temp['image'] = user['profile_pic_url_hd']
        temp['name'] = user['full_name']
        if not temp['name']:
            temp['name'] = None

        temp['is_business_account'] = user['is_business_account']
        temp['verified'] = user['is_verified']
        temp['business_email'] = user['business_email']
        if not temp['business_email']:
            temp['business_email'] = None

        temp['connected_fb_page'] = user['connected_fb_page']
        temp['is_joined_recently'] = user['is_joined_recently']
        temp['linked_url'] = user['external_url']
        temp['posts'] = user['edge_owner_to_timeline_media']['count']
        temp['business_category_name'] = user['business_category_name']
        temp['business_address_json'] = user['business_address_json']
        temp['url'] = 'https://www.instagram.com/' + user['username']
        temp['type'] = 'identity'

        return temp

    def profile_fetcher(self, userid):

        url = 'https://www.instagram.com/{}/?__a=1'.format(userid)
        res = requests.get(url, headers=self.header, cookies=self.jar, proxies={'http': "//socks5://" + self.proxy['proxy_host'] + ':' + self.proxy['proxy_port']})
        return self.data_processor(res.json())


if __name__ == '__main__':
    obj = ProfileFetcher()
    print(obj.profile_fetcher('harrypotterfans'))

# harrypotterfans
# thisisbillgates
# yip.kit.hung