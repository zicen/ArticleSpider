# coding=utf8
#将伯乐在线mysql中的数据存到es中
import MySQLdb
from ArticleSpider.moudles.es_types import ArticleType
# 连接到数据库，并获得图标
connection = MySQLdb.connect('127.0.0.1', 'root', '111111', 'spider', charset="utf8", use_unicode=True)
cursor = connection.cursor()
from elasticsearch_dsl.connections import connections
from w3lib.html import remove_tags
es = connections.create_connection(ArticleType._doc_type.using)

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

cursor.execute("select title, url, create_date,  praise_nums, comment_nums, fav_nums, front_image_url, tags, content from article")

for title, url, create_date,  praise_nums, comment_nums, fav_nums, front_image_url, tags, content in cursor.fetchall():
    article = ArticleType()
    article.title = title
    article.create_date = create_date
    article.content = remove_tags(content)
    article.praise_nums = praise_nums
    article.fav_nums = fav_nums
    article.comment_nums = comment_nums
    article.tags = tags
    article.url = url
    article.front_image_url = front_image_url
    article.suggest = gen_suggests(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))
    article.save()
    print(url,title)




