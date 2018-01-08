"""
Gets list of kanji from WaniKani by level.
"""

import json
import requests
import sys
import codecs

API_BASE = "https://www.wanikani.com/api/v2"
API_KEY = open("API_KEY").read()
AUTH_HEADER = {"Authorization": "Bearer " + API_KEY}

def get_kanjis():
    """Gets list of kanji from WaniKani"""
    all_data = []
    result = {"pages": {"next_url": "{}/subjects/?types=kanji".format(API_BASE)}}
    while result["pages"]["next_url"] != None:
        resp = requests.get(result["pages"]["next_url"], headers=AUTH_HEADER)
        result = json.loads(resp.text)
        all_data.extend(result["data"])

    print("Fetched {} kanji".format(len(all_data)))
    return all_data

# get_kanjis() returns a list of objects.
# Each of those objects have the following structure:
#
# {
#   'id': 440,
#   'data_updated_at': '2017-10-04T18:56:21.270971Z',
#   'data': {
#       'level': 1,
#       'created_at': '2012-02-27T19:55:19.000000Z',
#       'document_url': 'https://www.wanikani.com/kanji/%E4%B8%80',
#       'character': '一',
#       'component_subject_ids': [1],
#       'readings': [{'type': 'onyomi', 'primary': True, 'reading': 'いち'},
#                    {'type': 'kunyomi', 'primary': False, 'reading': 'ひと'},
#                    {'type': 'nanori', 'primary': False, 'reading': 'かず'}],
#       'slug': '一',
#       'meanings': [{'meaning': 'One', 'primary': True}]
#   },
#   'url': 'https://www.wanikani.com/api/v2/subjects/440',
#   'object': 'kanji'
# }

levels = [[] for i in range(0,61)]
for kanji in get_kanjis():
    levels[kanji["data"]["level"]].append(kanji["data"]["character"])

with open("levels.txt", "w", encoding="utf-8") as outfile:
    json.dump(levels, outfile, ensure_ascii=False)
