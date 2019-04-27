import re
import  bike.utils as utils

class BikePipeline(object):
    def process_item(self, item, spider):
        for k in item:
            item[k] = utils.clean(item[k])

        item['price'] = re.sub(r'\s', '', item['price'].replace('Kč', ''))
        item['name'] = item['name'].strip()
        item['site'] = spider.name 

        return item
