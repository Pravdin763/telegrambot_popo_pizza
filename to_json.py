import json

mat = []

with open('мат для фильтра.txt', encoding='utf-8') as file:
    wr = file.read()
    for i in wr.split(', '):
        mat.append(i)

with open('mat.json', 'w', encoding='utf-8') as file2:
    json.dump(mat, file2)