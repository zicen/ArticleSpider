# coding=utf8
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, Completion, Keyword, Text, Integer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class ArticleType(DocType):
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    front_image_url = Keyword()
    create_date = Date()
    praise_nums = Integer()
    comment_nums = Integer()
    fav_nums = Integer()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")

    class Meta:
        index = "jobbole"
        doc_type = "article"


class LagouJobType(DocType):
    title = Text(analyzer="ik_max_word")
    salary = Text(analyzer="ik_max_word")
    tags = Text(analyzer="ik_max_word")
    job_addr = Text(analyzer="ik_max_word")
    job_advantage = Keyword()
    job_city = Keyword()
    job_type = Keyword()
    job_desc = Text(analyzer="ik_max_word")
    company_url = Keyword()
    company_name = Keyword()
    crawl_time = Date()

    class Meta:
        index = "lagou"
        doc_type = "job"





if __name__ == '__main__':
    ArticleType().init()
    # LagouJobType.init()
