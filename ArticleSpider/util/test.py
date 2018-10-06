import re

s = "2018-09-18\\xa0 发布于拉勾网"
mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", s)
print(mat.groups()[0])
