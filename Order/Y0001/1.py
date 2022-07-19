class Student:  # 数据类
    def __init__(self, ID, name, course):
        self.name = name
        self.ID = ID
        self.course = course

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_course(self):
        return self.course

    def get_scores_mean(self):
        return float(sum(self.course.values())) / len(self.course)

    def add_course(self, cname, grade):
        self.course[cname] = grade


class ManaStuInfo:  # 业务逻辑类
    def __init__(self):
        self.info = []

    def loadFile(self, txtName):
        with open(txtName, "r", encoding="utf-8") as f:
            data = f.readlines()
            for i in data:
                i = i.split(",")
                name = i[0]
                ID = i[1]
                courses = i[2:]
                coursesdic = {}
                for c in courses:
                    temp = c.split(":")
                    cname = temp[0]
                    grade = float(temp[1])
                    coursesdic[cname] = grade
                self.info.append(Student(ID, name, coursesdic))

    def saveFile(self, txtName):
        with open(txtName, "w", encoding="utf-8") as f:
            for i in self.info:
                name = i.name
                ID = i.ID
                coursesdic = i.course
                temp = [name, ID]
                for c in coursesdic:
                    temp.append(f"{c}:{coursesdic[c]}")
                f.write(",".join(temp) + "\n")

    def queryID(self, ID):
        for i in range(len(self.info)):
            if self.info[i].ID == ID:
                return -1
        return 0

    def queryStu(self, ID):
        for i in self.info:
            if i.ID == ID:
                name = i.get_name()
                course = i.get_course()
                means = i.get_scores_mean()
                temp = []
                for j in course:
                    temp.append(f"{j}:{course[j]}")
                temp = "\n".join(temp)
                print(f"名字：{name}\n学号：{ID}\n修读的课程及成绩：{temp}\n平均分：{means}")
                return
        print("未查询到该生的信息")

    def addStudent(self, stuInfo):
        idx = self.queryID(stuInfo.ID)
        if idx == -1:
            print(f"学号为{stuInfo.ID}的同学已存在，不能重复添加")
            return -1
        else:
            self.info.append(stuInfo)
            return 0

    def reviseStuInfo(self, stuInfo):
        for i in range(len(self.info)):
            if self.info[i].ID == stuInfo.ID:
                self.info[i] = stuInfo
                return


class MainWindow:  # 命令行交互界面类
    def __init__(self):
        self.manaStu = ManaStuInfo()

    def selectCommand(self):  # 菜单选择
        menu = ["1.显示所有学生信息", "2.查询指定学生的信息", "3.添加学生信息", "4.保存数据并退出", "5.不保存并退出"]
        print("*" * 50)
        print("\n".join(menu))
        print("*" * 50)
        ch = input("请输入选择的功能编号：")
        return ch

    def addStuinfo(self):  # 添加学生信息
        addID = input("请输入要添加的学生学号：")
        name = input("请输入学生姓名：")
        stu = Student(addID, name, {})
        s = input("请输入课程名称和成绩（用,分隔）：")
        while s != "":
            ss = s.split(",")
            cname, grade = ss[0], round(float(ss[1]), 1)
            if(cname != "" and grade > 0 and grade <= 100):
                stu.add_course(cname, grade)
            else:
                print("输入数据不合法，请重新输入！")
            s = input("请输入课程名称和成绩（用,分隔）：")

        if (self.manaStu.addStudent(stu) == -1):
            ch = input("该生信息已存在，是否覆盖？(Y/N)：")
            if ch == 'Y':
                self.manaStu.reviseStuInfo(stu)

    def showStuInfo(self, ID):  # 显示某学生信息
        self.manaStu.queryStu(ID)

    def showAllInfo(self):  # 显示所有学生信息
        for i in self.manaStu.info:
            name = i.get_name()
            ID = i.get_ID()
            course = i.get_course()
            means = i.get_scores_mean()
            temp = []
            for j in course:
                temp.append(f"{j}:{course[j]}")
            temp = "\n".join(temp)
            print("*" * 50)
            print(f"名字：{name}\n学号：{ID}\n修读的课程及成绩：\n{temp}\n平均分：{means}")
            print("*" * 50)

    def loadData(self, txtName):
        self.manaStu.loadFile(txtName)

    def saveData(self, txtName):
        self.manaStu.saveFile(txtName)

    def queryID(self, ID):
        return self.manaStu.queryID(ID)


def main():
    mWin = MainWindow()  # 初始化 显示菜单
    mWin.loadData("StudentInfo.txt")
    while True:
        ch = mWin.selectCommand()
        if ch == "1":
            mWin.showAllInfo()
        elif ch == "2":
            ID = input("请输入要查询的学生学号：")
            mWin.showStuInfo(ID)
        elif ch == "3":
            mWin.addStuinfo()
        elif ch == "4":
            mWin.saveData("StudentInfo.txt")
            return
        else:
            return


if __name__ == '__main__':
    main()
