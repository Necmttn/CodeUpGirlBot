BOT_NAME = 'scrap'

SPIDER_MODULES = ['scrap.spiders']
NEWSPIDER_MODULE = 'scrap.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
    'scrap.pipelines.SQLiteStorePipeline': 300, # value represents the importance weight.
}
