import json
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup


class Instagram:

    def __init__(self):
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

    def search_api(self, query, stype=None):

            query = quote(query)
            r = requests.get('https://web.stagram.com/search?query=%s' % query,
                             proxies={"http": "socks5://"+self.proxy['proxy_host']+':'+self.proxy['proxy_port']})
            results = self._insertProfile(r)
            return dict(
                data=dict(
                    results=results,
                    total=len(results)
                )
            )

    def _insertProfile(self, r):

        bsObj = BeautifulSoup(r.text, "html.parser")
        # print(bsObj.prettify())
        image = bsObj.findAll('div', {'class': "card min-height"})

        output = []

        for i in image:
            ref2 = BeautifulSoup(str(i), "lxml")
            # print(ref2)
            post = {}
            post['url'] = "https://www.instagram.com/" + str(ref2.h4.get_text())
            post['userid'] = str(ref2.h4.get_text())
            post['image'] = str(ref2.img['src'])

            try:
                post['name'] = str(ref2.p.get_text())
            except:
                continue
            output.append(post)

        return output


if __name__ == "__main__":
    obj = Instagram()
    print(json.dumps(obj.search_api("trump")))
