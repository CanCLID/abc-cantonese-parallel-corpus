from bs4 import BeautifulSoup
import regex as re
from glob import glob
import unicodedata

substitution_yue = (
    ('!', '！'),
    (',', '，'),
    (':', '：'),
    ('?', '？'),
    ('啝', '喎'),
    ('噖', '琴'),  # 噖[日晚] -> 琴[日晚]
    ('嚫', '親'),
    ('衭', '褲'),
    ('贃', '賺'),
    ('𡄯', '噎'),
    ('𠶧', '掂'),
    ('𠹺', '埋'),
    ('𡁵', '緊'),
    ('𡃶', '錫'),
    ('𧨾', '氹'),
    ('依𠺢', '依家'),
    ('而𠺢', '而家'),
    ('𠺢吓', '家下'),
    ('𠺢陣', '家陣'),
    ('星架波', '新加坡'),
    ('自覺得己', '覺得自己'),
)

trans = None

def full_width_to_half_width(s: str) -> str:
    global trans
    if trans is None:
        fw = 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０'
        hw = unicodedata.normalize('NFKC', fw)
        trans = str.maketrans(fw, hw)
    return s.translate(trans)

def normalise(yue: str, en: str) -> tuple[str, str]:
    for src, dst in substitution_yue:
        yue = yue.replace(src, dst)
    yue = full_width_to_half_width(yue)
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
        if '(empty band???)' in (yue, en) or \
                '[missing example characters???]' in (yue, en):
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
