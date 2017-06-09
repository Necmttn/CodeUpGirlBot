#!/bin/bash
> /app/results.json
/usr/local/bin/scrapy runspider /app/scrap.py -o /app/results.json &> /app/scrap.log
