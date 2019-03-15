import requests
from modules.sentiment import SentimentAnalysis
import json
from urllib.parse import quote


class InstaPost:

    def __init__(self):

        self.neg_count = 0
        self.neu_count = 0
        self.pos_count = 0
        self.obj = SentimentAnalysis()
        self.results = []
        self.proxy = self._get_proxy()

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

    def data_processor(self, c):

        for each_post in c:

            # self.results.append(each_post)
            dictionary = dict()
            dictionary['datetime'] = each_post['node']['taken_at_timestamp']
            dictionary['postid'] = each_post['node']['shortcode']

            # checking the type of post
            dictionary['type'] = each_post['node']['__typename']
            if dictionary['type'] == 'GraphVideo':
                dictionary['type'] = 'video'
            elif dictionary['type'] == 'GraphImage':
                dictionary['type'] = 'image'
            elif dictionary['type'] == 'GraphSidecar':
                dictionary['type'] = 'image'


            # dictionay['is_video'] = each_post['node']['is_video']
            # try:
            #     dictionay['video_view_count'] = each_post['node']['video_view_count']
            # except:
            #     pass

            dictionary['thumbnail'] = each_post['node']['thumbnail_src']
            try:
                dictionary['content'] = each_post['node']['edge_media_to_caption']['edges'][0]['node']['text']
                pol = self.obj.analize_sentiment(dictionary['content'])
                each_post['node']['polarity'] = pol
                dictionary['polarity'] = each_post['node']['polarity']

                if pol == 1:
                    dictionary['polarity'] = "positive"
                    self.pos_count += 1
                elif pol == -1:
                    dictionary['polarity'] = "negative"
                    self.neg_count += 1
                else:
                    dictionary['polarity'] = "neutral"
                    self.neu_count += 1
            except:
                pass
            dictionary['likes'] = each_post['node']['edge_liked_by']['count']
            # dictionay['profile_id'] = each_post['node']['owner']['id']
            dictionary['comments'] = each_post['node']['edge_media_to_comment']['count']
            # dictionay['profile_url'] = 'https://www.instagram.com/web/friendships/' + dictionay['user_id'] + '/follow'
            dictionary['url'] = 'https://www.instagram.com/p/' + dictionary['postid'] # + '/?taken-by=' + dictionay[
            #     'user_id']
            self.results.append(dictionary)

    def instagram_post(self, query):

        query = quote(query.replace(" ", "_"))
        try:
            url = 'https://www.instagram.com/explore/tags/%s/?__a=1' % query
            # print(url)
            page = requests.get(url, proxies={"http": "socks5://"+self.proxy['proxy_host']+':'+self.proxy['proxy_port']}).content.decode('utf-8')
            p = json.loads(page)

            c = p['graphql']['hashtag']['edge_hashtag_to_media']['edges']
            self.data_processor(c)

        except json.decoder.JSONDecodeError:
            pass

        ps = self.pos_count
        ng = self.neg_count
        nu = self.neu_count
        total = ps + ng + nu

        sentiments = dict()
        sentiments["positive"] = ps
        sentiments["negative"] = ng
        sentiments["neutral"] = nu

        # return {'data': {'results': self.results,
        #                  'sentiments': Sentiments,
        #                  'total': len(self.results)}
        #         }
        return {'data': self.results}


if __name__ == '__main__':

    obj = InstaPost()
    # obj.instagram_post()

    print(obj.instagram_post('steph'))
