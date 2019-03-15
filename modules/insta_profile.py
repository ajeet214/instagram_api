# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class BooksSpider(Spider):
    name = 'books'
    # allowed_domains = ['books.toscrape.com']
    allowed_domains = ['web.stagram.com']

    def __init__(self, category):
        self.start_urls = [category]

    def parse(self, response):
        pass
        profiles = response.xpath('//*[@class="card min-height"]/a/@href').extract()
        # books = response.xpath('//h3/a/@href').extract()
        for each in profiles:
            # print(each)
            if each.startswith('/tag'):
                pass
            elif each.startswith('/location'):
                pass
            else:

                absolute_url = 'https://web.stagram.com'+each
                # print(absolute_url)
            # absolute_url = response.urljoin(each)
                yield Request(absolute_url, callback=self.parse_book)

        # process next page
        # next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        # absolute_next_page_url = response.urljoin(next_page_url)
        # yield Request(absolute_next_page_url)

    def parse_book(self, response):

        # profile username
        username = response.xpath('//h1/text()').extract_first()
        # profile image
        profile_image = response.xpath("//h1/img/@data-src").extract_first()
        # list of number of posts, followers and followings
        posts_followers_followings = response.xpath('//*[@class="userdata clearfix text-center mb-4"]/p[1]/span/text()').extract()
        # profile name
        name = response.xpath('//*[@class="userdata clearfix text-center mb-4"]/p[2]/span/text()').extract_first()
        details = response.xpath('//*[@class="userdata clearfix text-center mb-4"]/p[2]/text()').extract_first()
        details = details.split('\n')
        lst = ['posts', 'followers', 'followings']

        yield {'profile_id': username,
               'profile_image': profile_image,
               'posts': posts_followers_followings[0],
               'followers': posts_followers_followings[1],
               'followings': posts_followers_followings[2],
               'profile_url': ('https://www.instagram.com/{}'.format(username)).replace(' ', ''),
               'profile_name': name,
               'details': details}

# scrapy runspider insta_profile.py -a category=https://web.stagram.com/search?query=trump -o insta_user.csv