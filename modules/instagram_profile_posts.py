#!/usr/bin/env python
import demjson
import requests
from credentials import creds
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor


class ProfilePosts:

    def __init__(self):

        self.proxy = self._get_proxy()
        self.session = FuturesSession(executor=ThreadPoolExecutor(max_workers=5))
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

        temp_list = []
        location_list = []
        user = data['graphql']['user']
        # temp['posts'] = user['edge_owner_to_timeline_media']['count']

        for i in user['edge_owner_to_timeline_media']['edges']:

            temp = dict()

            temp['is_video'] = i['node']['is_video']
            if temp['is_video'] is True:
                temp['views'] = i['node']['video_view_count']

            try:
                temp['content'] = i['node']['edge_media_to_caption']['edges'][0]['node']['text']
            except IndexError:
                temp['content'] = None

            temp['postid'] = i['node']['shortcode']
            temp['url'] = 'https://www.instagram.com/p/'+i['node']['shortcode']

            temp['comments'] = i['node']['edge_media_to_comment']['count']
            temp['likes'] = i['node']['edge_liked_by']['count']
            temp['datetime'] = i['node']['taken_at_timestamp']
            temp['location'] = i['node']['location']
            if temp['location'] is not None:
                temp['location'] = temp['location']['name']
                location_list.append((temp['location'], temp['postid']))
            else:
                location_list.append(('@', temp['postid']))

            temp['thumbnail'] = i['node']['display_url']
            temp['userid'] = i['node']['owner']['username']

            # checking the type of post
            temp['type'] = i['node']['__typename']
            if temp['type'] == 'GraphVideo':
                temp['type'] = 'video'
            elif temp['type'] == 'GraphImage':
                temp['type'] = 'image'
            elif temp['type'] == 'GraphSidecar':
                temp['type'] = 'image'

            temp_list.append(temp)

        print(temp_list)
        print('location list', location_list)
        rs = []
        for u in location_list:
            rs.append((self.session.get('https://maps.google.com/maps/api/geocode/json?address=' + str(
                u[0]) + '&key='+creds['google_api_key']), u[0], u[1]))

        print(rs)
        results = []
        for response in rs:
            temp_dict = {}
            r = response[0].result()
            lt = demjson.decode(r.content.decode('utf-8'))
            # print(lt)
            # print(lt['results'][0]['address_components'])
            try:
                for i in lt['results'][0]['address_components']:
                    if i['types'][0] == 'country':
                        # print(i['long_name'])
                        temp_dict['country_code'] = i['short_name']
                        temp_dict['country'] = i['long_name']
                        temp_dict['id'] = response[2]
                        temp_dict['location'] = response[1]
                        results.append(temp_dict)
            except:
                temp_dict['country_code'] = None
                temp_dict['country'] = None
                results.append(temp_dict)
        print(results)
        print(temp_list)

        final_list = []
        for i in range(len(temp_list)):
            final_dict = {}
            try:
                if results[i]['id'] == temp_list[i]['postid']:
                    final_dict['country'] = results[i]['country']
                    final_dict['country_code'] = results[i]['country_code']

            except:
                final_dict['country'] = None
                final_dict['country_code'] = None

            final_dict['content'] = temp_list[i]['content']
            final_dict['comments'] = temp_list[i]['comments']
            final_dict['is_video'] = temp_list[i]['is_video']
            final_dict['location'] = temp_list[i]['location']
            final_dict['datetime'] = temp_list[i]['datetime']
            final_dict['author_userid'] = temp_list[i]['userid']
            try:
                final_dict['author_name'] = user['full_name']
            except:
                final_dict['author_name'] = None

            final_dict['author_image'] = user['profile_pic_url_hd']
            final_dict['url'] = temp_list[i]['url']
            final_dict['likes'] = temp_list[i]['likes']
            final_dict['postid'] = temp_list[i]['postid']
            final_dict['thumbnail'] = temp_list[i]['thumbnail']
            final_dict['type'] = temp_list[i]['type']

            final_list.append(final_dict)
        return final_list

        # return temp_list

    def profile_posts(self, userid):

        url = 'https://www.instagram.com/{}/?__a=1'.format(userid)
        res = requests.get(url, headers=self.header, cookies=self.jar,
                           proxies={'http': "//socks5://" + self.proxy['proxy_host'] + ':' + self.proxy['proxy_port']})
        return self.data_processor(res.json())


if __name__ == '__main__':
    obj = ProfilePosts()
    print(obj.profile_posts('william_asher'))

# harrypotterfans
# thisisbillgates
# william_asher
# robbertrodenburg