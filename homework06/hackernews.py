from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    row = s.query(News).filter_by(id=request.query.id).first()
    row.label = request.query.label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    rows = s.query(News).filter().all()
    url = rows[0].url
    print(url)
    new = get_news("https://news.ycombinator.com/newest")
    for news in new[::-1]:
        if url == news["url"]:
            break
        else:
            s = session()
            news = News(title=news['title'],
                        author=news['author'],
                        url=news['url'],
                        comments=news['comments'],
                        points=news['points'])
            s.add(news)
            s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    redirect("/news")


if __name__ == "__main__":
    run(host="localhost", port=8080)

