#! python3
# quotescraper.py - Scrapes quotes from www.goodreads.com into .txt file
# author - Jordan Dominguez

from lxml import html
import requests


# function to parse quotes and return list of all quotes from that tag
def parseQuotes(link):
    print('Downloading page %s...' % (link))
    page = requests.get(link)
    text_tree = html.fromstring(page.text)
    content_tree = html.fromstring(page.content)
    next_page = content_tree.xpath('//a[@class="next_page"]//@href')
    quotes = text_tree.xpath('//div[@class="quoteText"]/text()')
    quotes = [x.strip() for x in quotes]
    quotes = [x for x in quotes if len(x) > 30]
    if len(next_page) > 0:
        next_page_url = 'https://www.goodreads.com' + str(next_page[0])
        print('Scraping next page...')
        return quotes + parseQuotes(next_page_url)
    else:
        print('Done downloading quotes!')
        return quotes


# picking the topic of quotes to scrape (from goodreads.com)
topic_list = ["love", "life", "inspirational", "humor", "philosophy", "truth", "god", "wisdom", "inspirational-quotes", "happiness", "romance", "hope", "death", "quotes", "poetry", "faith", "writing", "inspiration", "religion", "knowledge", "success", "education", "relationships", "motivational", "life-lessons", "time", "science", "funny", "books", "spirituality"]


print("List of topics:")
print(topic_list)

topic = input("Pick a quote topic: ")
while topic not in topic_list:
    topic = input("Pick a quote topic: ")
else:
    quote_page = ('https://www.goodreads.com/quotes/tag/' + topic)

# running the parseQuotes function on the quote page URL created from user topic input
quotes=parseQuotes(quote_page)

# writes all quotes in list to a text file
print("Writing quotes to file")
file = open((topic+"_quoteList.txt"), "w")
for item in quotes:
    file.write("%s\n" % item)
file.close()
print('Done writing quotes to file!')
