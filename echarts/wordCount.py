import jieba
import zhon.hanzi
from nltk.corpus import stopwords

punc = zhon.hanzi.punctuation  # 要去除的中文标点符号
# 读入文件
with open('keywords.txt', encoding="utf-8") as fp:
    text = fp.read()

ls = jieba.lcut(text)  # 分词

# 统计词频
counts = {}
for i in ls:
    if len(i) > 1:
        counts[i] = counts.get(i, 0) + 1

ls1 = sorted(counts.items(), key=lambda x: x[1], reverse=True)  # 词频排序

print(ls1[:300])
