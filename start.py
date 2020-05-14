from data_process import Data_process
from spider import Lagou_spider
from visualization import Data_visualization
def all_process_run(kw):
    spider = Lagou_spider("{}".format(kw))
    spider.run()
    process = Data_process("{}".format(kw))
    dic = process.get_city_salary()
    visualize = Data_visualization(dic)
    visualize.data_visualization(dic)

if __name__ == '__main__':
    all_process_run("php") # 在这里的参数是是一个关键字，可以传递给三个类
