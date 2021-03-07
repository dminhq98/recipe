import scrapy
import os
from os import path
import time
import requests
import shutil
import json

class RecipeSpider(scrapy.Spider):
    name = "recipe"
    start_urls = [
      "https://www.allrecipes.com/recipes",
    ]

    def parse(self, response):
        # base_url = "https://www.allrecipes.com/recipes"
        data = response.xpath('/html/body/main/div[2]/div/nav/div/ul/li/a/@href').getall()
        # with open('recipe.json', 'w') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)

        for link in data:
            # item_link = base_url + link
            yield scrapy.Request(link, callback=self.parse_single_cat)

    def parse_single_cat(self, response):
        data = response.xpath('/html/body/main/div[2]/div/nav/div/ul/li/a/@href').getall()
        # with open('recipe.json', 'w') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)

        for link in data:
            # item_link = base_url + link
            yield scrapy.Request(link, callback=self.parse_single_item)

    def parse_single_item(self, response):
        data = response.xpath('/html/body/main/div[4]/div/div/div[1]/a/@href').getall()
        for link in data:
            # item_link = base_url + link
            yield scrapy.Request(link, callback=self.parse_info_item)

    def parse_info_item(self, response):
        dictionary = {}
        dictionary['link'] = response.url
        dictionary['id'] = response.url.split('/')[4]
        category = response.xpath('/html/body/div[2]/div/main/div[1]/div[1]/div/nav/ol/li/a/span/text()').getall()
        category = [i.strip() for i in category[2:]]
        dictionary['cate'] = category
        dictionary['prep'] = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/section/div[1]/div[1]/div[2]/text()').get().strip()
        dictionary['cook'] = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/section/div[1]/div[2]/div[2]/text()').get().strip()
        dictionary['total'] = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/section/div[1]/div[3]/div[2]/text()').get().strip()
        dictionary['servings'] = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/section/div[2]/div[1]/div[2]/text()').get().strip()
        dictionary['yield'] = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/section/div[2]/div[2]/div[2]/text()').get().strip()

        ingred = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[5]/section[1]/fieldset/ul/li/label/span/span/text()').getall()
        ingred = [i.strip() for i in ingred]
        dictionary['ingredients'] =ingred
        direct = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/section[1]/fieldset/ul/li/div/div/p/text()').getall()
        direct = [i.strip() for i in direct]
        dictionary['directions'] = direct

        notes = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[6]/div/div[1]/p/text()').get()
        if notes:
            notes = notes.strip()
        dictionary['notes'] = notes
        dictionary['nutrition'] = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/section[2]/div/div[2]/text()').get().strip()

        img_link = response.xpath('//*[@id="dialog-4e81f5f4-ca3d-4bd0-af90-7920bf655c96"]/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/div/div/div/div[1]/div/div[1]/img/@src').getall()
        dictionary['img_link'] = img_link
        time.sleep(1)
        yield dictionary
        # for img in img_link:
        #     yield scrapy.Request(img, callback=self.parse_img, cb_kwargs=dict(dictionary = dictionary))

    def parse_img(self, response, dictionary):

        with open("image/%s" % response.url.split('/')[-1], 'wb') as f:
            f.write(response.body)