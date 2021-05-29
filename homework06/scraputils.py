import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    table = parser.body.center.table
    rows = []
    for row in table.findAll("tr"):
        rows.append(row)
    data = rows[3].findAll("tr")
    for i in range(0, len(data) - 2, 3):
        page = dict()
        links = data[i + 1].findAll("td")[1].findAll("a")
        if len(links) < 4:
            continue
        page["points"] = int(data[i + 1].findAll("td")[1].span.text.split()[0])
        page["author"] = links[0].text
        comments = "discuss"
        if len(links) == 4:
            comments = links[3].text.split()[0]
        if comments == "discuss":
            page["comments"] = 0
        else:
            page["comments"] = int(comments)
        link = data[i].findAll("td")[2].find("a")
        page["url"] = link["href"]
        page["title"] = link.text
        news_list.append(page)

    return news_list


def extract_next_page(parser):
    table = parser.body.center.table
    rows = []
    for row in table.findAll("tr"):
        rows.append(row)
    data = rows[3].findAll("tr")
    page = data[-1].findAll("td")[1]
    return page.find("a")["href"]

def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

