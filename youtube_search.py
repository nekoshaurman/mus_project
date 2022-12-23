import urllib.request
import re


def search(keyword):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + under(keyword))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    video_url = "https://www.youtube.com/watch?v=" + video_ids[0]
    return video_url

def under(word):
    splited = word.split()
    new_word = '_'.join(splited)
    return new_word

