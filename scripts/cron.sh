#!/bin/bash
> /app/results.json
/usr/local/bin/scrapy runspider /app/scrap/scrapy.py -o /app/scrap/results.json &> /app/logs/scrap.log
