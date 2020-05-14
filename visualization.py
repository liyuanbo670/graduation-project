from pyecharts.charts import Bar

class Data_visualization():
    def __init__(self,dic,):
        self.dic = dic
    def data_visualization(self,dic):
        bar = Bar()
        # 根据salary值排序， reverse为False代表升序
        dt = dict(sorted(dic.items(), key=lambda x: float(x[1]), reverse=False))
        # 横坐标
        bar.add_xaxis(list(dt.keys()))
        # 纵坐标
        bar.add_yaxis('城市平均薪资', list(dt.values()))
        # 渲染
        bar.render()
