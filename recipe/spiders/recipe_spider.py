import scrapy
import os
from os import path
import time
import requests
import shutil
import json

class RecipeSpider(scrapy.Spider):
    name = "recipe"
    # start_urls = [
    #   "https://www.allrecipes.com/recipes",
    # ]

    start_urls = [
        "https://www.allrecipes.com/recipes/76/appetizers-and-snacks/",
        "https://www.allrecipes.com/recipes/88/bbq-grilling/",
        "https://www.allrecipes.com/recipes/156/bread/",
        "https://www.allrecipes.com/recipes/78/breakfast-and-brunch/",
        "https://www.allrecipes.com/recipes/79/desserts/",
        "https://www.allrecipes.com/recipes/17562/dinner/",
        "https://www.allrecipes.com/recipes/1642/everyday-cooking/",
        "https://www.allrecipes.com/recipes/1116/fruits-and-vegetables/",
        "https://www.allrecipes.com/recipes/84/healthy-recipes/",
        "https://www.allrecipes.com/recipes/85/holidays-and-events/",
        "https://www.allrecipes.com/recipes/17567/ingredients/",
        "https://www.allrecipes.com/recipes/17561/lunch/",
        "https://www.allrecipes.com/recipes/80/main-dish/",
        "https://www.allrecipes.com/recipes/92/meat-and-poultry/",
        "https://www.allrecipes.com/recipes/95/pasta-and-noodles/",
        "https://www.allrecipes.com/recipes/96/salad/",
        "https://www.allrecipes.com/recipes/93/seafood/",
        "https://www.allrecipes.com/recipes/81/side-dish/",
        "https://www.allrecipes.com/recipes/94/soups-stews-and-chili/",
        "https://www.allrecipes.com/recipes/236/us-recipes/",
        "https://www.allrecipes.com/recipes/86/world-cuisine/"
    ]

    def parse(self, response):
        # base_url = "https://www.allrecipes.com/recipes"
        data = response.xpath('/html/body/main/div[2]/div/nav/div/ul/li/a/@href').getall()
        # with open('recipe.json', 'w') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)

        for link in data:
            # item_link = base_url + link
            yield scrapy.Request(link, callback=self.parse_single_item)

    def parse_single_cat(self, response):
        data = response.xpath('/html/body/main/div[2]/div/nav/div/ul/li/a/@href').getall()
        # with open('recipe.json', 'w') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)

        for link in data:
            # item_link = base_url + link
            yield scrapy.Request(link, callback=self.parse_single_item)

    def parse_single_item(self, response):
        data = response.xpath('/html/body/main/div/div/div/div[1]/a/@href').getall()
        with open('item.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        for link in data:
            if link.split('/')[3] == 'recipe':
                yield scrapy.Request(link, callback=self.parse_info_item)

    def parse_info_item(self, response):

        # response.xpath('').get().strip()
        dictionary = {}
        dictionary['link'] = response.url
        dictionary['id'] = response.url.split('/')[4]
        dictionary['name'] = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[1]/div[1]/div/h1/text()').get().strip()
        rate = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/a[1]/span[1]/text()').get().strip()
        rate = rate.replace('Rating:','')
        rate = rate.replace('stars', '').strip()
        dictionary['rate'] = rate
        num_rate = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/ul/li[1]/span[1]/text()').get().strip()
        num_rate = num_rate.replace(' Ratings', '').strip()
        dictionary['num_rate'] = num_rate
        category = response.xpath('/html/body/div[2]/div/main/div[1]/div[1]/div/nav/ol/li/a/span/text()').getall()
        category = [i.strip() for i in category[2:]]
        dictionary['cate'] = category
        dictionary['prep'] = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/section/div[1]/div[1]/div[2]/text()').get().strip()
        total = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/section/div[1]/div[2]/div[2]/text()').get().strip()
        if total is None:
            total = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/section/div[1]/div[2]/div[2]/text()').get().strip()
        dictionary['total'] = total
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

        img_link = response.xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div/div/a/div/div[1]/img/@src').getall()
        dictionary['img_link'] = img_link
        time.sleep(1)
        yield dictionary
        # for img in img_link:
        #     yield scrapy.Request(img, callback=self.parse_img, cb_kwargs=dict(dictionary = dictionary))

    def parse_img(self, response, dictionary):

        with open("image/%s" % response.url.split('/')[-1], 'wb') as f:
            f.write(response.body)