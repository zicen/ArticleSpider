# -*- coding: utf-8 -*-
import scrapy
import re
import json
import datetime

try:
    import urlparse as parse
except:
    from urllib import parse

from scrapy.loader import ItemLoader

from ArticleSpider.items import ZhihuQuestionItem, ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=5&offset={1}&sort_by=default"
    headers = {
        "HOST": "www.zhihu.com",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"
    }

    cookies = {
        'srf': 'LNcfBivnLzMYzt5nyE751maKzw67Zn7i',
        '_zap': '5c72ad41-cb3b-43b3-b360-e637146359f6',
        'd_c0': 'APBlU1O5Rg6PTqfpMtviAMlPs3tM6MTq9T8=|1538044371',
        'capsion_ticket': "2|1:0|10:1538057088|14:capsion_ticket|44:YTczNmJkZmE3Y2U0NGJmODk0MjEzM2VmOTUxNmZiNDg=|22256e042bb2c68fbfa757dcbb8d2626b94d925c74c271d6966cb22f80b6d221",
        'q_c1': 'a56de1a5de0b40ec831f9fd63027e968|1538046267000|1538046267000',
        'l_cap_id': "MjU3NDM3MTc2NWU5NDA1MThlMzFhYmFmNTdhZWM1MDY=|1538054118|513f862adce9af9bc9bd54bceeb1549c7fc1fd55",
        'r_cap_id': "MjZkNjJkY2RiNzA4NDlkMTk1MjdjYzhiMTMwZDdhMjc=|1538054118|f4b31954406a0a0b340d05c6a3f92c693cb32789",
        'cap_id': "MDQ5YzA4N2I5ZDJlNDkzNmEzNzZmZTY4Y2JhYzlkNzY=|1538054118|53af0a83f90db933b80d5b7525054590627c6336",
        '__utma': '155987696.1789289973.1538052029.1538052029.1538052029.1',
        '__utmz': '155987696.1538052029.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'z_c0': '2|1:0|10:1538057101|4:z_c0|92:Mi4xVUJKbkFBQUFBQUFBOEdWVFU3bEdEaVlBQUFCZ0FsVk5qVEdhWEFEWjFtQUxNRWVZY05jbS04elpmRVlLX1VZM1Z3|8012bf863a812ccb4f296708cbc743f4dfacce712ea421c32974d4653632ce75',
        'tgw_l7_route': 'e0a07617c1a38385364125951b19eef8'
    }

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        all_urls = filter(lambda x: True if re.match("(.*zhihu.com/question/(\d+))(/|$).*", x) else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                yield scrapy.Request(url, headers=self.headers, callback=parse)

    def parse_question(self, response):
        # 处理question页面， 从页面中提取出具体的question item
        if "QuestionHeader-title" in response.text:
            # 处理新版本
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_css("watch_user_num", ".QuestionFollowStatus-counts .NumberBoard-itemValue::text")
            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")
            question_item = item_loader.load_item()
        else:
            # 处理老版本页面的item提取
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            # item_loader.add_css("title", ".zh-question-title h2 a::text")
            item_loader.add_xpath("title",
                                  "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            # item_loader.add_css("watch_user_num", "#zh-question-side-header-wrap::text")
            item_loader.add_xpath("watch_user_num",
                                  "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")
            question_item = item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(question_id, 0), headers=self.headers,
                             callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]
        # 提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)

    def start_requests(self):
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, headers=self.headers, cookies=self.cookies)]
