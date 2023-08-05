# -*- coding: utf-8 -*-
from news_extractor.language_deal_title import title_filter
from news_extractor.exception import TextMissingError
import re,os,chardet
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import requests
from w3lib.html import remove_tags
from logging import getLogger
from urllib import parse
from lxml import etree
logger = getLogger(__name__)

class BodyExtractor():
    def __init__(self, html,url,encoding='utf-8'):
        if type(html) == bytes:
            self.html = html.decode(encoding)
        else:
            self.html = html
        self.url=url
        self.pureText = ''  # 去除标签后的
        self.THRESHOLD = 50  # 骤升点阈值
        self.K = 3  # 行块中行数
        self.j = 3  # 行块末尾检测阈值
        self.wordCount = []  # 每个行块中的字符个数
        self.lines = []
        self.content = ''  # 抽取的正文
        self.title = ''
        self.author=''
        self.time=''
        self.img=''
        self.file=''
        # self.css_url
        self.maxIndex = -1  # 字符最多的行块索引
        self.start = -1
        self.end = -1
        # logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        try:
            self._preprocess()
            self._start()
            self._end()
        except:
            logger.info(f'获取网页文本内容失败！')
            raise TextMissingError(f'获取网页文本内容失败！')

        if self.end != -1:
            self.content = ''.join(self.lines[self.start:self.end + self.K - 1])
            title_list = self.get_title()
            #print(title_list)
            #标题抽取函数
            if len(title_list):
                print(title_filter(title_list,self.content))
                title_req = re.compile(r'\s+')
                self.title = title_req.sub('',title_filter(title_list,self.content))
            else:
                logger.info(f'标题抽取失败！')    
    def check_contain_chinese(self,check_str):
        '''
        判断字符串中是否含有文字
        '''
        tag = 0
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                tag += 1
            else:
                continue
        if tag == 0:
            return False
        else:
            return True

    def get_title(self):
        '''
        获取标题列表title_list
        '''
        #匹配css样式表
        reqTitle = re.findall(r'<link.*?href="(.*?)".*?',self.html)
        doc = pq(self.html)
        soup = BeautifulSoup(self.html,'html.parser')
        title_list = set()
        if soup.find_all('h1'):
            for i in soup.find_all('h1'):
                if self.check_contain_chinese(i.text):
                    title_list.add(i.text)
        if soup.find_all('h2'):
            for i in soup.find_all('h2'):
                if self.check_contain_chinese(i.text):
                    title_list.add(i.text)
        if soup.find_all('h3'):
            for i in soup.find_all('h3'):
                if self.check_contain_chinese(i.text):
                    title_list.add(i.text)
        if reqTitle:
            for url in reqTitle:
                if url.split('.')[-1] == 'css':
            # print(titleTag)
                    css_url=parse.urljoin(self.url, url)
                    # print(css_url)
                    headers={
                        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
                    }
                    res = requests.get(css_url,headers=headers)
                    encode_info = chardet.detect(res.content)
                    res.encoding = encode_info['encoding']
                    # print(res)
                    # print('1',res.text)
                    fontinfo = re.findall(r'\.{1}(.*?){(.*?)}.*?.',res.text,re.S)
                    # print('------------',fontinfo)
                    infolist = []
                    for item in fontinfo:
                        if 'font-weight:bold' in item[1] or 'font-weight: bold' in item[1] or 'FONT-WEIGHT:bold' in item[1] or 'FONT-WEIGHT: bold' in item[1] or '微软雅黑' in item[1] or 'Microsoft Yahei' in item[1] or 'text-align:center' in item[1] or 'text-align: center' in item[1] or 'TEXT-ALIGN:center' in item[1] or 'TEXT-ALIGN: center' in item[1]:
                            # print('classlabel',item[1])
                            fontsize = re.findall(r'font-size:\s{0,}(\d+)px',item[1])
                            fontsize1 = re.findall(r'FONT-SIZE:\s{0,}(\d+)px',item[1])
                            
                            if fontsize and int(fontsize[0]) >= 18:
                                # print(fontsize)
                                infolist.append(item[0])
                            if fontsize1 and int(fontsize1[0]) >= 18:
                                # print(fontsize1)
                                infolist.append(item[0])

                        if len(infolist) == 0:
                            continue 
                    # print(infolist)
                    for i in infolist:
                        try:
                            a = [j.text for j in soup.select('.'+i)]
                            b = [j.text for j in doc('.'+i)]
                            # print(a,b)
                            if len(a) and len(b):
                                titles = []
                                for j in range(len(a)):
                                    if a[j] == None and b[j] != None:
                                        titles.append(b[j])
                                    elif b[j] == None and a[j] != None:
                                        titles.append(a[j])
                                    elif b[j] == None and a[j] == None:
                                        continue
                                    else:
                                        if len(a[j]) >= len(b[j]):
                                            titles.append(a[j])
                                        else:
                                            titles.append(b[j])
                            for title in titles:
                                title_list.add(title)
                        except:
                            pass
        return title_list

    def _preprocess(self):
        regex = re.compile(
            r'(?:<!DOCTYPE.*?>)|'  # doctype
            r'(?:<head[\S\s]*?>[\S\s]*?</head>)|'
            r'(?:<!--[\S\s]*?-->)|'  # comment
            r'(?:<img[\s\S]*?>)|'  # 图片
            r'(?:<br[\s\S]*?>\s*[\n])|'
            r'(?:<script[\S\s]*?>[\S\s]*?</script>)|'  # js...
            r'(?:<style[\S\s]*?>[\S\s]*?</style>)', re.IGNORECASE)  # css
        
        body=re.sub(r'(?:<head[\S\s]*?>[\S\s]*?</head>)','',self.html)
        reqImg=re.findall(r'<img[\s\S]*?>',body)
        reqFile=re.findall(r'<a.*?href="(.*?)".*>',body)

        #图片地址
        if reqImg is not None:
            f=[]
            for x in reqImg:
                b=re.findall(r'<img\s+src="(.*?)".*?',x)
                try:
                    imgs=os.path.splitext(b[0])
                    filename,type1=imgs
                    if 'weixin' not in b[0] and 'xhtml' not in b[0]  and type1 !='.png' and type1 !='.gif' and type1 !='.php' :                    
                        f.append(b[0])
                except:
                    pass
            self.img=f

        #附件地址
        if reqFile is not None:
            k=[]
            for ss in reqFile:
                files=os.path.splitext(ss)
                filename,type2=files
                if type2 == '.pdf' or type2 =='.doc' or type2=='.docx' or type2 =='.xlsx' or type2 =='zip':
                    k.append(ss)
            if k:
                self.file=set(k)     
        filteredHtml = self.html_escape(regex.sub('', self.html))
        soup = BeautifulSoup(filteredHtml, 'lxml')

        #时间正则匹配
        reqTime=re.search(r'(\d{4}-\d{1,2}-\d{1,2})',soup.get_text())
        if reqTime:
            reqTag = reqTime.group(0)
            self.time=reqTag
        else:
            reqTime=re.search(r'(\d{4}\S+\d{1,2}\S+\d{1,2})',soup.get_text())
            reqTag = reqTime.group(0)
            self.time=reqTag
        '''
        暂不支持表格正文提取
        '''
        # table=soup.findAll('table')
        # if table[0].text:              
        #     self.pureText=table[0].text
        #     # print(self.pureText)
        #     self.lines = list(map(lambda s: re.sub(r'\s+', '', s), self.pureText.splitlines()))
        #     count = list(map(lambda s: len(s), self.lines))
        #     for i in range(len(count) - self.K + 1):
        #         self.wordCount.append(count[i] + count[i + 1] + count[i + 2])
        #     self.maxIndex = self.wordCount.index(max(self.wordCount))
        self.pureText = soup.get_text()
        # print(self.pureText)
        self.lines = list(map(lambda s: re.sub(r'\s+', '', s), self.pureText.splitlines()))
        #行数统计
        count = list(map(lambda s: len(s), self.lines))
        for i in range(len(count) - self.K + 1):
            self.wordCount.append(count[i] + count[i + 1] + count[i + 2])
        #找出连续三行中文字最多的行块索引
        self.maxIndex = self.wordCount.index(max(self.wordCount))
        # print('1',self.wordCount)

    def html_escape(self,text):
        """
        html转义
        """
        text = (text.replace("&quot;", "\"").replace("&ldquo;", "“").replace("&rdquo;", "”")
                .replace("&middot;", "·").replace("&#8217;", "’").replace("&#8220;", "“")
                .replace("&#8221;", "\”").replace("&#8212;", "——").replace("&hellip;", "…")
                .replace("&#8226;", "·").replace("&#40;", "(").replace("&#41;", ")")
                .replace("&#183;", "·").replace("&amp;", "&").replace("&bull;", "·")
                .replace("&lt;", "<").replace("&#60;", "<").replace("&gt;", ">")
                .replace("&#62;", ">").replace("&nbsp;", " ").replace("&#160;", " ")
                .replace("&tilde;", "~").replace("&mdash;", "—").replace("&copy;", "@")
                .replace("&#169;", "@").replace("♂", "").replace("\r\n|\r", "\n"))
        return text
    #文本开始行快索引
    def _start(self):
        for i in [-x - 1 + self.maxIndex for x in range(self.maxIndex)]:
            # print('--',i,self.maxIndex)
            gap = min(self.maxIndex - i, self.K)
            if sum(self.wordCount[i + 1:i + 1 + gap]) > 0:
                if self.wordCount[i] > self.THRESHOLD:
                    continue
                else:
                    break
        self.start = i + 1
        # print('2',self.start)
    #文本结束行块索引
    def _end(self):
        for i in [x + self.maxIndex for x in range(len(self.wordCount) - self.maxIndex - 2)]:
            if self.wordCount[i] == 0 and sum(self.wordCount[i:i+self.j]) < self.wordCount[self.start+1]:
                self.end = i
                break
        # print('3',self.end)

