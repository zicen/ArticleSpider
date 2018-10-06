# coding=utf8
#将伯乐在线mysql中的数据存到es中
import MySQLdb
from ArticleSpider.moudles.es_types import LagouJobType
# 连接到数据库，并获得图标
connection = MySQLdb.connect('127.0.0.1', 'root', '111111', 'spider', charset="utf8", use_unicode=True)
cursor = connection.cursor()
from elasticsearch_dsl.connections import connections
from w3lib.html import remove_tags
import re
import datetime

es = connections.create_connection(LagouJobType._doc_type.using)

def gen_suggests(index, info_tuple):
    # 根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests


cursor.execute("select title, salary, tags,  job_addr, job_advantage, job_city, job_type, job_desc, company_url,url,company_name,publish_time from lagou_job")

for title, salary, tags,  job_addr, job_advantage, job_city, job_type, job_desc, company_url,url,company_name,publish_time in cursor.fetchall():
    job = LagouJobType()
    job.title = title
    job.salary = salary
    job.tags = tags
    job.job_addr = job_addr
    job.job_advantage = job_advantage
    job.job_city = job_city
    job.job_type = job_type
    job.job_desc = remove_tags(job_desc)
    job.company_url = company_url
    job.url = url
    job.company_name = company_name
    mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", publish_time)
    if mat is not None and mat.groups()[0]:
        job.publish_time = mat.groups()[0]
    else:
        job.publish_time = datetime.datetime.now()

    job.suggest = gen_suggests(LagouJobType._doc_type.index, ((job.title, 10), (job.tags, 7),(job.job_desc,7)))
    job.save()
    print(url,title)




