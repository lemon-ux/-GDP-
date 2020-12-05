import matplotlib.pyplot as plt
from matplotlib import animation   #实现动图的核心函数
import matplotlib.animation as animation
import pandas as pd


years = []
for i in range(1960,2019):
    years.append(i)
years.reverse()


class Plot(object):
    """用plot绘图"""
    def __init__(self,data):
        plt.rcParams['font.sans-serif'] = ['SimHei']    #中文显示
        plt.rcParams['axes.unicode_minus'] = False     #设置正常显示字符
        fig,ax = plt.subplots(figsize = (12,6))      #设置图表的宽度和高度
        self.fig = fig
        self.ax = ax
        self.data = data

    def showGif(self,save_path,writer = 'imagemagick'):
        """制作gif动画"""
        #清除当前图形中的当前活动轴,其他轴不受影响
        plt.cla()
        #fig绘制动画的名称，func定义动画函数，frames动画长度，init_func初始化函数，interval更新频率，blit更新点
        ani = animation.FuncAnimation(fig = self.fig,
                                      func = self.update,
                                      frames = len(self.data),
                                      init_func = self.init,
                                      interval = 0.5,
                                      blit = False,
                                      repeat = False)
        #保存为html
        ani.save(save_path,writer = writer, fps = 3)

    def init(self):
        """初始化，绘制横向水平柱状图"""
        bar = self.ax.barh([],[],color = '#6699CC')
        return bar

    def update(self,i):
        """不断更新数据"""
        self.ax.cla()
        data = self.data[i]
        x = data[1]
        y = data[2]
        year = data[0]
        #设置坐标
        bars = []
        for k in range(len(x)):
            tmp = y[k]
            if tmp in ["中国"]:
                bar = self.ax.barh(k,x[k],color = 'r')
            else:
                bar = self.ax.barh(k,x[k],color = '#6699CC')
            bars.append(bar)
        #为柱状图右侧添加数据标签
        for rect in bars:
            rect = rect[0]
            w = rect.get_width()
            self.ax.text(w,rect.get_y() + rect.get_height() / 2,'%.2lf' % float(w),ha = 'left',va = 'center')

        #设置X,Y轴刻度线标签
        self.ax.set_title(year)
        self.ax.set_yticks(range(len(y)))
        self.ax.set_yticklabels(y)
        self.ax.set_xlabel("GDP(百亿)")
        return bar


def main():
    """读取数据"""
    gdp = pd.read_excel("gdp_analysis.xls")

    datas = []
    for year in years:
        year = str(year)
        #将数据进行降序排序
        gdp.sort_values(year,inplace = True,ascending = False)
        print(year,"=======================================")
        print(gdp[0:15][["Country Name",year]])

        data = gdp[0:15]
        data.sort_values(year,inplace = True,ascending = True)
        #用科学计数法输出
        data[year] = data[year] / 10 ** 11    
        
        datas.append([year,data[year].tolist(),data["Country Name"].tolist()])       

    plot = Plot(datas)
    plot.showGif("gdp.html",writer = "html")

if __name__ == '__main__':
    main()
