from bs4 import BeautifulSoup
import regex as re
from glob import glob

filename = glob('Wenlin+Dictionaries-*.xml')[-1]

with open(filename, encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')

sentences = []

for page in soup.select('page'):
    content = page.select_one('text').get_text().removeprefix('<WL>').removesuffix('</WL>')

    for match in re.finditer(r'^[^ ]*hz +(.+)\n[^ ]*tr +(.+)', content, flags=re.MULTILINE):
        yue, en = match.groups((1, 2))
        if yue == '(empty band???)' or en == '(empty band???)':
            continue
        assert '\n' not in yue
        assert '\n' not in en
        sentences.append((yue, en))

def key(item):
    yue, en = item
    return len(yue), yue, en

sentences.sort(key=key)

with open('sentences.txt', 'w', encoding='utf-8') as f:
    for yue, en in sentences:
        print(yue, file=f)
        print(en, file=f)
