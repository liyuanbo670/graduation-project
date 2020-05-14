import json
import re

class Data_process():
    def __init__(self,kw):
        self.kw = kw
    def get_city_salary(self):
        with open("{}.txt".format(self.kw),"r",encoding="utf8") as f:
            data_lt = f.readlines()

        all_data = {}

        for onedata in data_lt:
            data = json.loads(onedata) # 将data转化为字典，与json功能一样
            if data["city"] not in all_data.keys():
                all_data[data["city"]] = []
                all_data[data["city"]].append(data)
            else:
                all_data[data["city"]].append(data)
        # print("all_data:",all_data)

        city_salary={}

        for key in all_data:
            for item in all_data[key]:
                salary = item["salary"]
                if key not in city_salary:
                    city_salary[key] = []
                    city_salary[key].append(salary)
                else:
                    city_salary[key].append(salary)
        # print("city_salary:",city_salary)

        city_avg_salary = {}

        for key in city_salary:
            salary_list = city_salary[key] # 获取某城市所有职位薪资列表
            i = len(salary_list) # 薪资列表的总长度
            for salary in salary_list:
                two_salary = re.findall("\d+",salary) # 薪资列表每个元素的两个薪资
                low_salary = int(two_salary[0]) # 每个元素的薪资下限
                high_salary = int(two_salary[1]) # 每个元素的薪资上限
                avg_salary = (low_salary+high_salary)/2 # 每个元素的中位薪资
                if key not in city_avg_salary:
                    city_avg_salary[key] = []
                    city_avg_salary[key].append(avg_salary)
                else:
                    city_avg_salary[key].append(avg_salary)
        # print("city_avg_salary:",city_avg_salary)

        # 计算每个城市该类程序设计的平均薪资
        city_detial_avg_salary={} # 定义一个空的字典

        for key in city_avg_salary:
            sum_salary = 0 # 初始化某城市该程序语言所有职位的总薪资
            detial_avg_salary = city_avg_salary[key] # 列表形式的里面存储一个一个的int数据类型的薪资
            for i in detial_avg_salary:
                sum_salary+=i # 求某城市该种程序语言的总薪资

            # print(key, sum_salary)
            true_avg_salary=sum_salary/(len(detial_avg_salary))
            city_detial_avg_salary[key] = "%.2f"%true_avg_salary # 算出某城市该程序语言的平均薪资
        # print(city_detial_avg_salary)


        return city_detial_avg_salary
