from jianping_extractor import BodyExtractor
import requests,chardet
url = 'http://chinagrain.gov.cn/html/xinwen/2019-03/25/content_243878.shtml'
res = requests.get(url)
# print(res.status_code)
# print(res.text)
encode_info = chardet.detect(res.content)
res.encoding = encode_info['encoding']
extractor = BodyExtractor(res.text)
print(extractor.content) # 抽取的正文部分
print(extractor.title)
print(extractor.author)
print(extractor.form)
print(extractor.time)
print(extractor.img)
print(extractor.file)
