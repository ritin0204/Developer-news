from flask import Flask, render_template, url_for
import requests
from bs4 import BeautifulSoup
import pprint
app = Flask(__name__)


def Posts(links, votes):
    hn = []
    for idx, link in enumerate(links):
        title = link.get_text()
        href = link.get('href', None)
        vote = votes[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if int(points) > 99:
                hn.append({'title': title, 'link': href, 'point': points})
    return sort_posts(hn)

# To sort hacker News Posts By Votes
def sort_posts(postes):
    return sorted(postes, key=lambda k: k['point'], reverse=True)

@app.route('/')
def hello():
    url = requests.get('https://news.ycombinator.com/news')
    url_2 = requests.get('https://news.ycombinator.com/news?p=2')
    soup = BeautifulSoup(url.content, 'html.parser') 
    soup_2 = BeautifulSoup(url_2.content, 'html.parser')
    links_1 = soup.select('.storylink')
    links_2 = soup_2.select('.storylink')
    votes_1 = soup.select('.subtext')
    votes_2 = soup_2.select('.subtext')
    links = links_1+links_2
    votes = votes_1+votes_2
    News = Posts(links, votes)
    # pprint.pprint(News)
    return render_template('index.html',news = News)


if __name__ == '__main__':
    app.run()
