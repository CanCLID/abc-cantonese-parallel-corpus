from bs4 import BeautifulSoup
import regex as re
from glob import glob

def normalise(yue: str, en: str) -> tuple[str, str]:
    yue = yue.replace(',', '，')
    yue = yue.replace('!', '！')
    yue = yue.replace('?', '？')
    return yue, en

filename = glob('Wenlin+Dictionaries-*.xml')[-1]

with open(filename, encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')

pattern = re.compile(r'^[^ ]*hz +(.+)\n[^ ]*tr +(.+)', flags=re.MULTILINE)
sentences = []

for page in soup.select('page'):
    content = page.select_one('text').get_text().removeprefix('<WL>').removesuffix('</WL>')

    for match in pattern.finditer(content):
        yue, en = match.groups((1, 2))
        if yue == '(empty band???)' or en == '(empty band???)':
            continue
        assert '\n' not in yue
        assert '\n' not in en
        yue, en = normalise(yue, en)
        sentences.append((yue, en))

def key(item):
    yue, en = item
    return len(yue), yue, en

sentences.sort(key=key)

with open('yue.txt', 'w', encoding='utf-8') as f1, \
        open('en.txt', 'w', encoding='utf-8') as f2:
    for yue, en in sentences:
        print(yue, file=f1)
        print(en, file=f2)
