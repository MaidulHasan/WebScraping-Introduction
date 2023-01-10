import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup

base_url = "https://news.ycombinator.com/news"
num_pages = 3  # num of pages to scrape data from
top_stories = []


def get_popular_posts():
    class_storylink = soup.select(".storylink")  # story title and link to the story
    class_subtext = soup.select(".subtext")  # subtext to the storylink includes classes - score, age
    class_age = soup.select(".age")  # time of posting
    print(class_storylink)
    print(class_subtext)
    print(class_age)
    for idx, item in enumerate(class_storylink):
        title = class_storylink[idx].get_text()
        link = class_storylink[idx].get("href")
        post_time = class_age[idx].get_text()
        class_score = class_subtext[idx].select(".score")
        if len(class_score) > 0:
            upvotes = class_score[0].getText()
            if int(upvotes.split(" ")[0]) >= 100:
                top_stories.append({"title": title, "link": link, "upvotes": upvotes, "posted": post_time})
    # return top_stories


for page_num in range(1, num_pages + 1):
    param_dict = {"p": page_num}
    res = requests.get(base_url, params=param_dict)
    soup = BeautifulSoup(res.text, "html.parser")
    get_popular_posts()


def get_sorted_posts():
    top_stories.sort(key=lambda post: post["upvotes"], reverse=True)
    for item in top_stories:
        print("---------------------------------------------------------------------------------------------")
        for key in item.keys():
            print(key, " : ", item[key])
        print("---------------------------------------------------------------------------------------------")


get_sorted_posts()
