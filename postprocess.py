
len(sentences)

for yue, en in sentences:
    print(yue)
    print(en)

def replace_hash(s: str) -> str:
    '''
    >>> replace_hash('因為個#計劃 有需要改動嘅地方，所以唯有延緩#執行。')
    '因為個計劃有需要改動嘅地方，所以唯有延緩執行。'
    >>> replace_hash('#Mac OS')
    'Mac OS'
    '''
    s = re.sub(r'#([\p{Unified_Ideograph}\u3006\u3007]+) (?=[\p{Unified_Ideograph}\u3006\u3007。，？！《》（）])', r'\1', s)  # 成嚿中文+空格+中文或中文標點
    s = s.replace('#', '')
    return s

def remove_space(s: str) -> str:
    '''
    >>> remove_space('摸 A B 12至 3')
    '摸A B 12至3'
    '''
    s = re.sub(r'(?<=[\p{Unified_Ideograph}\u3006\u3007]) (?=[\da-zA-Z])', r'', s)
    s = re.sub(r'(?<=[\da-zA-Z]) (?=[\p{Unified_Ideograph}\u3006\u3007])', r'', s)
    return s

all_texts = []
with open('all-1666469101.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if len(row) < 3:
            continue
        row = row[2]
        if '<eg>' in row:
            all_texts.append(row)

def should_keep(yue: str, eng: str) -> bool:
    if eng in ('X', 'x'):
        return False
    if re.search(r'[\p{Unified_Ideograph}\u3006\u3007]', eng):  # 有漢字
        return False
    if yue.count('（') != eng.count('('):
        return False
    return True

def g(s: str):
    return len(s[0]), s[0], s[1], s[2]

def f():
    seen = set()
    for text in all_texts:
        for match in re.finditer(r'<eg>\nyue:(.+?) ?\(([^(\n]+)\)\neng:(.+)', text):
            yue, jyp, eng = match.groups((1, 2, 3))

            m = re.fullmatch(r'(.+?); literal.+', eng)
            if m:  # 解釋性詞語
                eng = m[1]
                if ';' in eng:
                    eng = eng.split(';', 1)[0]  # take the first explanation

            if not should_keep(yue, eng) or yue in seen:
                continue
            yield yue, jyp, eng
            seen.add(yue)
all_sentences = list(sorted(f(), key=g))

with open('yue.txt', 'w') as f1, \
        open('yue-Latn.txt', 'w') as f2, \
        open('en.txt', 'w') as f3:
    for a, b, c in all_sentences:
        a = remove_space(replace_hash(a))
        if len(a) > 2:
            print(a, file=f1)
            print(b, file=f2)
            print(c, file=f3)
