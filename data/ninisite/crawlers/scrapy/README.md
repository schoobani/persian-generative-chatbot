# NiniSite Crawler (Scrapy)
This crawler crawl [Ninisite](https://www.ninisite.com/discussion) and export data item like one in [main README](https://github.com/anvaari/persian-generative-chatbot/blob/ninisite-scrapy/README.md).

# Usage 
- `cd path/to/project/data/ninisite/scrapy`
- `python -m venv .env`
- `source activate .env/bin/activate`
- `python -m pip install --upgrage pip`
- `python -m pip install scrapy`
- Crawl nini site and export data as jsonline file : `python -m scrapy crawl ninisite_cawler -O data.jsonlines -L INFO`
`-L INFO` set logging level to INFO (default if DEBUG).
