import jieba
import zhon.hanzi
from nltk.corpus import stopwords

punc = zhon.hanzi.punctuation  # 要去除的中文标点符号
# baidu_stopwords = stopwords.words('baidu_stopwords')  # 导入停用词表
# 读入文件
with open('keywords.txt', encoding="utf-8") as fp:
    text = fp.read()

ls = jieba.lcut(text)  # 分词

# 统计词频
counts = {}
for i in ls:
    if len(i) > 1:
        counts[i] = counts.get(i, 0) + 1

# 去标点（由于我这里不统计长度为1的词，去标点这步可省略）
# for p in punc:
#     counts.pop(p,0)

# for word in baidu_stopwords:  # 去掉停用词
#     counts.pop(word, 0)

ls1 = sorted(counts.items(), key=lambda x: x[1], reverse=True)  # 词频排序

print(ls1[:300])
