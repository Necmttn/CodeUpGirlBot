#!/bin/bash
> /app/results.json
/usr/local/bin/scrapy crawl fcc_crawl &> /app/logs/scrap.log
