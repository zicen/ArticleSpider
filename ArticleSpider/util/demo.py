#coding=utf8
import re
if __name__ == '__main__':
    aaa = re.match("(.*zhihu.com/question/(\d+))(/|$).*", "https://www.zhihu.com/question/36965606")
    if aaa:
        print(aaa.group(1))
        print(aaa.group(2))