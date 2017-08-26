#-*-coding:utf8;-*-
#qpy:2
#qpy:console
import requests
import Queue,re,os
import threading,time
import warnings
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
header={	
        'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-CN; ZTE Grand S II LTE Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 Quark/2.0.0.918 Mobile Safari/537.36',
#第一次修改
#rrrrrr        
	}
h=open('/sdcard/html','r')
html=h.read()
SHARE_Q = Queue.Queue()  #构造一个不限制大小的的队列
_WORKER_THREAD_NUM = 10 #设置线程个数
class MyThread(threading.Thread) :

    def __init__(self, func) :
        super(MyThread, self).__init__()
        self.func = func

    def run(self) :
        self.func()
#返回文件名        
def getname(url):
  filename=re.findall(r'https*://pic\d{1}\.zhimg\.com/(.{10,50}_b.\w{3,4})',url)
  if len(filename)!=0:
   return filename
  else:
   return ['no pictire']
def kai():



#290
 totals=290
 i=251
 name=u'短短'
 ids=26489045
 while i<=totals:
  get_url('https://www.zhihu.com/collection/%s?page=%s'%(ids,i),name)
  i+=1
  print '#'*45
  print i

def download() :#下载图片的线程
    global SHARE_Q
    while not SHARE_Q.empty():
       
        url = SHARE_Q.get()
        print '图片还有%s张'%SHARE_Q.qsize()
        url2= url.replace('"','') #获得任务
#        print url2
        r=requests.get(url2,verify=False,headers=header)
        
        with open('/sdcard/my/images/%s'%getname(url)[0],'wb') as f:
            f.write(r.content)
            f.close()
        time.sleep(1)
        if SHARE_Q.qsize()==0:
         return
def get_url(url,fm):
    r=requests.get(url,headers=header,verify=False)
    soup = BeautifulSoup(r.text.replace('&gt;','>').replace('&lt;','<') ,'lxml')
#    soup_a=soup.prettify()
    #获取正文
    tags = soup.find_all('textarea')
    if False==os.path.exists('/sdcard/my/%s'%fm):
	     os.mkdir('/sdcard/my/%s'%fm)  

    counts=soup.find_all('span',class_='count')
    title=soup.find_all('h2',class_='zm-item-title')
    url_list=[]
    title_list=[]
    count_list=[]
    for title_a in title:
      filename=re.sub(r'[\n\?/\\:\ *"<>|]','',title_a.get_text())
      
      title_list.append(filename)
    del title_list[0]
    for c in counts:
#      print c.get_text()
      if c.get_text().find('K')!=-1:
        i=re.findall(r'(\d*?)K',c.get_text())[0]
        count_list.append(int(i)*1000)
      else:
        count_list.append(c.get_text().replace('\n',''))
    count_list.append('000000')
    for tag in tags:
        #获取图片地址，用于开启另一个线程下载
     for tag_a in tag.find_all('img'):
       url_list.append( tag_a['src'])
    for task in url_list:
        global SHARE_Q
        SHARE_Q.put(task)#存入消息队列
        print SHARE_Q.qsize()
    a=0
    for ct in tags:#储存数据
        #获取全部的图片地址
        for ct_a in ct.find_all('img'):
              r=re.findall(r'https*://pic\d{1}.zhimg.com/(.{10,50}_b\.\w{3,4})',str(ct_a['src']))
              if len(r)!=0:
               ct_a['src']='/sdcard/my/images/'+r[0]
        if len(title_list)==9:
         if a==9:
          a-=1      
        #图片地址转换
        try:
         with open('/sdcard/my/%s/%s.html'%(fm,(str(count_list[a])+title_list[a])),'wb') as f:
            f.write(html.replace('aacc=ddee',str(ct).replace('<textarea class="content" hidden="">','').replace('</textarea>','')))
         a+=1
        except IOError,i:
         print i
         print count_list
        
global SHARE_Q
start = time.clock()
kai()
threads = []
#负责开启线程
for i in xrange(_WORKER_THREAD_NUM) :
        thread = threading.Thread(target=download,args=())
        thread.start()
        threads.append(thread)
        print '我开启线程'
for thread in threads :
        thread.join()
        print len(threads)
print time.time()
end = time.clock()
print '%.03f seconds'%(end-start)
