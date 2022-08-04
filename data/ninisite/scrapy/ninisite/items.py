# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass


@dataclass
class NinisiteItem:
    topic : str
    question : list
    answer : list
