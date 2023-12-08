# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PatentItem(scrapy.Item):
    # define the fields for your item here like:
    patent_search_cat = scrapy.Field()
    # patent_name = scrapy.Field()
    # ipc = scrapy.Field()
    # application_number = scrapy.Field()
    # application_date = scrapy.Field()
    # applicant = scrapy.Field()
    # current_assignee = scrapy.Field()
    patents = scrapy.Field()