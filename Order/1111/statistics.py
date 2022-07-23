import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
import pandas as pd


class Shop:
    def __init__(self, name, province, city, averageTemperature, commutersVolume, area, salesVolume, competitorsNumber):
        self.name = name
        self.province = province
        self.city = city
        self.averageTemperature = averageTemperature
        self.commutersVolume = commutersVolume
        self.area = area
        self.salesVolume = salesVolume
        self.competitorsNumber = competitorsNumber

    def toList(self):
        return [self.name, self.province, self.city, self.averageTemperature, self.commutersVolume, self.area, self.salesVolume, self.competitorsNumber]


class InformationSet:
    def __init__(self):
        self.fileName = ""
        self.data = []
        self.df = None

    def loadDataFrom(self, fileName):
        self.fileName = fileName
        try:
            self.df = pd.read_csv(fileName, encoding="utf-8", header=0)
        except:
            self.df = pd.read_csv(fileName, encoding="gbk", header=0)
        for _, data in self.df.iterrows():
            data = list(data)
            self.data.append(Shop(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))

    def addData(self, shopData: Shop):
        self.data.append(shopData)
        self.df.loc[len(self.df.index)] = shopData.toList()

    def saveData(self):
        self.df.to_csv(self.fileName, index=False, encoding="gbk")


class MainWindow:
    def __init__(self):
        root = tk.Tk()
        root.title("水果店信息统计")
        self.center(root, 800, 400)
        self.informationSet = InformationSet()
        self.mainWindow = root
        menuBar = tk.Menu(root)
        dataMenu = tk.Menu(menuBar, tearoff=0)
        dataMenu.add_command(label='读取数据', command=self.loadDataBegin)
        dataMenu.add_command(label='添加数据', command=self.addDataBegin)
        dataMenu.add_command(label='保存数据', command=self.saveDataBegin)
        menuBar.add_cascade(label='数据', menu=dataMenu)
        cleanMenu = tk.Menu(menuBar, tearoff=0)
        cleanMenu.add_command(label='展示清洗后的数据', command=self.showCleanBegin)
        menuBar.add_cascade(label='清洗', menu=cleanMenu)
        anaMenu = tk.Menu(menuBar, tearoff=0)
        anaMenu.add_command(label='基本统计量', command=self.showStatisticsBegin)
        anaMenu.add_command(label='相关性分析', command=self.showAnalyseBegin)
        anaMenu.add_command(label='查询指定省份店铺信息', command=self.showProvinceBegin)
        menuBar.add_cascade(label='分析', menu=anaMenu)
        root.config(menu=menuBar)
        columns = ["1", "2", "3", "4", "5", "6", "7", "8"]
        tree = ttk.Treeview(root, column=columns, show='headings', height=18)
        self.tree = tree
        tree.heading('1', text="店铺名称")
        tree.heading('2', text="省份")
        tree.heading('3', text="城市")
        tree.heading('4', text="当地平均气温")
        tree.heading('5', text="客流量")
        tree.heading('6', text="面积")
        tree.heading('7', text="销售额")
        tree.heading('8', text="附近水果店数量")
        tree.column('1', width=100)
        tree.column('2', width=100)
        tree.column('3', width=100)
        tree.column('4', width=100)
        tree.column('5', width=100)
        tree.column('6', width=100)
        tree.column('7', width=100)
        tree.column('8', width=100)
        tree.pack()
        root.mainloop()

    def loadDataBegin(self):
        fileName = tkinter.filedialog.askopenfilename(title='选择文件')
        self.informationSet.loadDataFrom(fileName)
        try:
            for i in self.informationSet.data:
                self.tree.insert(parent='', index='end', text='', values=tuple(i.toList()))
            tkinter.messagebox.showinfo("成功", "读取数据成功")
        except:
            tkinter.messagebox.showerror("失败", "读取数据失败")

    def saveDataBegin(self):
        try:
            self.informationSet.saveData()
            tkinter.messagebox.showinfo("成功", "保存数据成功")
            self.mainWindow.destroy()
        except:
            tkinter.messagebox.showerror("失败", "保存数据失败")

    def addDataBegin(self):
        addWindow = AddWindow(self)

    def showCleanBegin(self):
        cleanWindow = CleanWindow(self)

    def showStatisticsBegin(self):
        statisticsWindow = StatisticsWindow(self)

    def showAnalyseBegin(self):
        analyseWindow = AnalyseWindow(self)

    def showProvinceBegin(self):
        provinceWindow = ProvinceWindow(self)

    @staticmethod
    def center(window, width, hight):
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        x = (w - width) / 2
        y = (h - hight) / 2
        window.geometry('%dx%d+%d+%d' % (width, hight, x, y))


class AddWindow():
    def __init__(self, mainWindow):
        root = tk.Tk()
        root.title("添加店铺数据")
        self.center(root, 400, 400)
        self.mainWindow = mainWindow
        self.addWindow = root
        nameLabel = tk.Label(root, text="店铺名称：")
        nameLabel.pack()
        self.nameEntry = tk.Entry(root)
        self.nameEntry.pack()
        provinceLabel = tk.Label(root, text="省份：")
        provinceLabel.pack()
        self.provinceEntry = tk.Entry(root)
        self.provinceEntry.pack()
        cityLabel = tk.Label(root, text="城市：")
        cityLabel.pack()
        self.cityEntry = tk.Entry(root)
        self.cityEntry.pack()
        averageTemperatureLabel = tk.Label(root, text="当地月平均气温：")
        averageTemperatureLabel.pack()
        self.averageTemperatureEntry = tk.Entry(root)
        self.averageTemperatureEntry.pack()
        commutersVolumeLabel = tk.Label(root, text="客流量：")
        commutersVolumeLabel.pack()
        self.commutersVolumeEntry = tk.Entry(root)
        self.commutersVolumeEntry.pack()
        areaLabel = tk.Label(root, text="面积：")
        areaLabel.pack()
        self.areaEntry = tk.Entry(root)
        self.areaEntry.pack()
        salesVolumeLabel = tk.Label(root, text="销售额：")
        salesVolumeLabel.pack()
        self.salesVolumeEntry = tk.Entry(root)
        self.salesVolumeEntry.pack()
        competitorsNumberLabel = tk.Label(root, text="附近水果店数量：")
        competitorsNumberLabel.pack()
        self.competitorsNumberEntry = tk.Entry(root)
        self.competitorsNumberEntry.pack()
        addButton = tk.Button(root, text=' 确认添加 ', command=self.addDataBegin)
        addButton.pack()
        root.mainloop()

    def addDataBegin(self):
        name = self.nameEntry.get()
        province = self.provinceEntry.get()
        city = self.cityEntry.get()
        averageTemperature = self.averageTemperatureEntry.get()
        commutersVolume = self.commutersVolumeEntry.get()
        area = self.areaEntry.get()
        salesVolume = self.salesVolumeEntry.get()
        competitorsNumber = self.competitorsNumberEntry.get()
        try:
            assert(len(name) != 0 and len(province) != 0 and len(city) != 0 and len(averageTemperature) != 0 and len(
                commutersVolume) != 0 and len(area) != 0 and len(salesVolume) != 0 and len(competitorsNumber) != 0)
        except:
            tkinter.messagebox.showerror("失败", "数据不能为空")
            self.addWindow.destroy()
            return
        try:
            shop = Shop(name, province, city, int(averageTemperature), int(commutersVolume), int(area), int(salesVolume), int(competitorsNumber))
            self.addData(shop)
        except:
            tkinter.messagebox.showerror("失败", "添加数据失败")

    def addData(self, shopData: Shop):
        try:
            self.mainWindow.informationSet.addData(shopData)
            self.mainWindow.tree.insert(parent='', index='end', text='', values=tuple(shopData.toList()))
            tkinter.messagebox.showinfo("成功", "添加数据成功")
            self.addWindow.destroy()
            return
        except:
            tkinter.messagebox.showerror("失败", "添加数据失败")

    @staticmethod
    def center(window, width, hight):
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        x = (w - width) / 2
        y = (h - hight) / 2
        window.geometry('%dx%d+%d+%d' % (width, hight, x, y))


class CleanWindow():
    def __init__(self, mainWindow):
        root = tk.Tk()
        root.title("清洗后的数据展示")
        self.center(root, 800, 400)
        self.mainWindow = mainWindow
        self.cleanWindow = root
        self.cleanData()
        label = tk.Label(root, text="本数据为清洗后的数据，若温度、客流量、店铺规模和周围水果店数量数据缺失，则使用其他店铺数据的均值替代，若销售额缺失，则直接删除该行数据")
        label.pack()
        columns = ["1", "2", "3", "4", "5", "6", "7", "8"]
        tree = ttk.Treeview(root, column=columns, show='headings', height=18)
        tree.heading('1', text="店铺名称")
        tree.heading('2', text="省份")
        tree.heading('3', text="城市")
        tree.heading('4', text="当地平均气温")
        tree.heading('5', text="客流量")
        tree.heading('6', text="面积")
        tree.heading('7', text="销售额")
        tree.heading('8', text="附近水果店数量")
        tree.column('1', width=100)
        tree.column('2', width=100)
        tree.column('3', width=100)
        tree.column('4', width=100)
        tree.column('5', width=100)
        tree.column('6', width=100)
        tree.column('7', width=100)
        tree.column('8', width=100)
        a = self.mainWindow.informationSet.df.shape[0]
        for i in range(0, a):
            value = list(self.mainWindow.informationSet.df.iloc[i])
            tree.insert(parent='', index='end', text='', values=tuple(value))
        tree.pack()
        root.mainloop()

    def cleanData(self):
        self.mainWindow.informationSet.df['当地平均温度'].fillna(value=self.mainWindow.informationSet.df['当地平均温度'].mean(), inplace=True)
        self.mainWindow.informationSet.df['客流量'].fillna(value=self.mainWindow.informationSet.df['客流量'].mean(), inplace=True)
        self.mainWindow.informationSet.df['面积'].fillna(value=self.mainWindow.informationSet.df['面积'].mean(), inplace=True)
        self.mainWindow.informationSet.df['附近水果店数量'].fillna(value=self.mainWindow.informationSet.df['附近水果店数量'].mean(), inplace=True)
        self.mainWindow.informationSet.df = self.mainWindow.informationSet.df.dropna()

    @staticmethod
    def center(window, width, hight):
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        x = (w - width) / 2
        y = (h - hight) / 2
        window.geometry('%dx%d+%d+%d' % (width, hight, x, y))


class StatisticsWindow():
    def __init__(self, mainWindow):
        root = tk.Tk()
        root.title("基本统计量展示")
        self.center(root, 600, 100)
        self.mainWindow = mainWindow
        self.statisticsWindow = root
        aa = self.mainWindow.informationSet.df[['客流量']]
        maxx = aa.max()
        minn = aa.min()
        meann = aa.mean()
        text1 = '所有连锁店中，平均客流量为', float(meann), '人/天，最大客流量为', int(maxx), '人/天，最小客流量为', int(minn), '人/天'
        aaa = self.mainWindow.informationSet.df[['水果销售额']]
        meannn = aaa.mean()
        varr = aaa.var()
        text2 = '平均水果销售额为', float(meannn), '元，销售额的方差为：', float(varr)
        label1 = tk.Label(root, text=text1)
        label1.pack()
        label2 = tk.Label(root, text=text2)
        label2.pack()
        root.mainloop()

    @staticmethod
    def center(window, width, hight):
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        x = (w - width) / 2
        y = (h - hight) / 2
        window.geometry('%dx%d+%d+%d' % (width, hight, x, y))


class AnalyseWindow():
    def __init__(self, mainWindow):
        root = tk.Tk()
        root.title("相关性分析")
        self.center(root, 320, 100)
        self.mainWindow = mainWindow
        self.analyseWindow = root
        chooseLabel = tk.Label(root, text="请选择变量：")
        chooseLabel.pack()
        cbox = ttk.Combobox(root)
        self.cbox = cbox
        cbox['values'] = ['请选择变量', '当地平均温度', '客流量', '面积']
        cbox['state'] = 'readonly'
        cbox.current(0)
        cbox.pack()
        chooseButton = tk.Button(root, text=" 确认 ", command=self.buttonchoose)
        chooseButton.pack()
        root.mainloop()

    def buttonchoose(self):
        value = self.cbox.get()
        corr = self.mainWindow.informationSet.df[str(value)].corr(self.mainWindow.informationSet.df['水果销售额'])
        if corr > 0:
            if corr > 0.2:
                a = "呈正相关"
            else:
                a = "相关性较弱"
        else:
            if corr < 0.2:
                a = "呈负相关"
            else:
                a = "相关性较弱"
        window2 = tk.Tk()
        window2.title('相关性分析')
        self.center(window2, 320, 80)
        word = "水果销售额和", value, a
        word2 = "相关系数为", corr
        anaLabel = tk.Label(window2, text=word)
        anaLabel.pack()
        anaLabel2 = tk.Label(window2, text=word2)
        anaLabel2.pack()
        window2.mainloop()

    @staticmethod
    def center(window, width, hight):
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        x = (w - width) / 2
        y = (h - hight) / 2
        window.geometry('%dx%d+%d+%d' % (width, hight, x, y))


class ProvinceWindow():
    def __init__(self, mainWindow):
        root = tk.Tk()
        root.title("按省份查询")
        self.center(root, 320, 100)
        self.mainWindow = mainWindow
        self.provinceWindow = root
        chooseLabel = tk.Label(root, text="请选择要查询的省份")
        chooseLabel.pack()
        cbox = ttk.Combobox(root)
        self.cbox = cbox
        cbox['values'] = ['请选择变量', '山东', '上海', '江苏']
        cbox['state'] = 'readonly'
        cbox.current(0)
        cbox.pack()
        okButton = tk.Button(root, text=" 确认 ", command=self.show)
        okButton.pack()
        root.mainloop()

    def show(self):
        show = tk.Tk()
        show.title("条件查找的数据")
        self.center(show, 800, 400)
        label1 = tk.Label(show, text="以下为符合条件的数据")
        label1.pack()
        columns = ["1", "2", "3", "4", "5", "6", "7", "8"]
        tree = ttk.Treeview(show, column=columns, show='headings', height=18)
        tree.heading('1', text="店铺名称")
        tree.heading('2', text="省份")
        tree.heading('3', text="城市")
        tree.heading('4', text="当地平均气温")
        tree.heading('5', text="客流量")
        tree.heading('6', text="面积")
        tree.heading('7', text="销售额")
        tree.heading('8', text="附近水果店数量")
        tree.column('1', width=100)
        tree.column('2', width=100)
        tree.column('3', width=100)
        tree.column('4', width=100)
        tree.column('5', width=100)
        tree.column('6', width=100)
        tree.column('7', width=100)
        tree.column('8', width=100)
        province = self.cbox.get()
        provinceInfo = self.mainWindow.informationSet.df[self.mainWindow.informationSet.df['省份'] == province]
        a = provinceInfo.shape[0]
        for i in range(0, a):
            value = list(provinceInfo.iloc[i])
            tree.insert(parent='', index='end', text='', values=tuple(value))
        tree.pack()
        show.mainloop()

    @staticmethod
    def center(window, width, hight):
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        x = (w - width) / 2
        y = (h - hight) / 2
        window.geometry('%dx%d+%d+%d' % (width, hight, x, y))


if __name__ == "__main__":
    mainWindow = MainWindow()
