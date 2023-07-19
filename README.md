# 项目介绍
该项目主要基于 flask 轻量级框架，前端使用了echarts和3d-force-graph，后端数据存储主要使用了mysql和neo4j
对豆瓣图书top250进行爬取分析，并组建每本书的推荐目录网
## 运行步骤
运行前请确保neo4j和mysql正常运行
先运行data文件中的data_analysis.py文件
然后再运行graph_database中test.py
最后再运行app.py

## 环境
#### neo4j_v5 
#### jdk17
#### python 3.10.2
#### mysql 5.8
## 代理
代理需要自行添加
