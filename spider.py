# 导入各种模块：正则模块，driver模块，网页解析模块（lxml），时间模块，显示等待模块，条件模块，界面模块
from selenium import webdriver
from lxml import etree
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium.webdriver.common.by import By
class Lagou_spider(object):# 定义一个爬虫类
    driver_path = r"E:\Anaconda\chromedriver1\chromedriver.exe" # 获取driver可执行文件的文件路径
    def __init__(self,kw):
        self.kw = kw
        self.driver = webdriver.Chrome(executable_path=Lagou_spider.driver_path)# 定义driver
        # 拉钩的python职位主页的url
        self.url = "https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput=".format(kw)
        # 定义一个职位空列表，用来存储职位详细信息
        self.positions = []
    def run(self): # 定义对象方法
        # 获取拉钩的python职位主页
        self.driver.get(self.url)
        page_btn = self.driver.find_element_by_xpath("//div[@class='body-btn']")
        page_btn.click()
        i = 0
        while 1:
            i += 1
            print("爬取第{}页".format(i))
            # 显示等待，最多等待10秒钟，一旦条件满足立即执行后面代码，不再等待
            WebDriverWait(driver=self.driver,timeout=10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='pager_container']/span[last()]")))
            # 获取网页源代码
            source = self.driver.page_source
            # 解析网页（调用解析方法）
            self.parse_list_page(source)
            # 设置自动点击下一页

            next_btn = self.driver.find_element_by_xpath("//div[@class='item_con_pager']/div[@class='pager_container']/span[last()]")

            # 如果下一页不能点击，则跳出循环，否则的继续循环（直到循环到最后一页）
            if "pager_next pager_next_disabled" == next_btn.get_attribute("class"):
                break
            else:
                next_btn.click()
             # 循环一次停三秒
            time.sleep(3)
        self.driver.close()
    def parse_list_page(self,source):
        # 解析首页源码
        i = 0
        html = etree.HTML(source)
        # 获取职位详细页面的url链接的列表links
        links = html.xpath("//a[@class='position_link']/@href")
        # 从links中获取每一个链接link
        for link in links:
            i += 1
            print("     爬取第{}条".format(i))
            self.request_detial_page(link)
            time.sleep(3)

    def request_detial_page(self,url):
        # 打开一个新的页面
        self.driver.execute_script("window.open('%s')"%url)
        # 将页面句柄转移到新的页面上来
        self.driver.switch_to.window(self.driver.window_handles[1])
        # 显示等待 10秒
        WebDriverWait(self.driver,timeout=10).until(EC.presence_of_all_elements_located((By.XPATH,"//span[@class='name']")))
        # 获取详细页面的源代码
        source = self.driver.page_source
        # 调用详细页面解析方法来解析详细页面
        self.parse_detial_page(source)
        #关闭当前页面
        self.driver.close()
        # 切换回职位列表页
        self.driver.switch_to.window(self.driver.window_handles[0])

    # 职位的详细页面解析，使用的有正则表达式和xpath
    def parse_detial_page(self,source):
        html = etree.HTML(source)
        # position_name = html.xpath("//div[@class='job-name']/text()")[0]
        position_name = html.xpath("//div[@class='job-name']/@title")
        job_request_spans = html.xpath("//dd[@class='job_request']//span")
        salary = job_request_spans[0].xpath('.//text()')[0].strip()
        city = job_request_spans[1].xpath(".//text()")[0].strip()
        city = re.sub(r"[\s/]","",city)
        work_years = job_request_spans[2].xpath(".//text()")[0].strip()
        work_years = re.sub(r"[\s/]","",work_years)
        education = job_request_spans[3].xpath(".//text()")[0].strip()
        education = re.sub(r"[\s/]","",education)
        # desc = "".join(html.xpath("//dd[@class='job_bt']//text()")).strip()
        company_name = html.xpath("//em[@class='fl-cn']/text()")[0].strip()
        position = {
            'name':position_name,
            'company':company_name,
            'salary':salary,
            'city':city,
            'work_years':work_years,
            'education':education,
            # 'desc':desc
        }
        self.positions.append(position)
        # print(position)
        position_json = json.dumps(position,ensure_ascii=False)
        with open("{}.txt".format(self.kw),mode='a',encoding='utf8') as f:
            f.write(position_json+"\n")
        print("     "+"*"*40)

