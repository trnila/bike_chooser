#!/bin/sh

mkdir -p data

for path in bike/spiders/[^_]*.py; do
  name=$(basename "$path" .py)
  dest=data/"$name".csv

  rm "$dest"
  scrapy crawl "$name" -o "$dest" -t csv
done
