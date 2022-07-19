import matplotlib.pyplot as plt  # 用于生成词频条形图的库
import matplotlib.ticker as mticker
import wordcloud
from loguru import logger   # 用于记录日志
from tkinter import *
import tkinter.filedialog


# 选择文件
def select():
    fileName = tkinter.filedialog.askopenfilename(title='选择文件')
    e1.delete(0, END)
    e1.insert(0, fileName)
    start(fileName)


# 清理标点符号
def clean(line):
    punctuations = "',.()-[];!?<>/:{}\|_=+*&^%$#@~`"
    for c in punctuations:
        if c in line:
            line = line.replace(c, "")
    line = line.lower().strip().split()
    return line


# 开始执行
def start(fileName):
    # 添加日志
    logger.add('result_log_{time}.txt')

    # 打开文本文件，并按行读取
    with open(fileName, "r", encoding="utf-8") as f:
        rawLines = f.readlines()

    # 对每行文字进行清理
    cleanedLines = []
    for line in rawLines:
        line = clean(line)
        cleanedLines.append(line)

    # 分解出单词列表
    rawWords = []
    for line in cleanedLines:
        rawWords.extend(line)

    logger.success(f"1.分解出单词列表:{rawWords}")

    # 得出单词频次字典
    wordsFrequency = {}
    for line in cleanedLines:
        for word in line:
            wordsFrequency[word] = wordsFrequency.get(word, 0) + 1
    logger.success(f"2.得出单词频次字典:{wordsFrequency}")

    # 按单词频次逆序输出结果
    wordsFrequencyItems = []
    for item in wordsFrequency.items():
        word, amount = item
        newItem = (amount, word)
        wordsFrequencyItems.append(newItem)
    print("{:-^100}".format("3.按单词频次逆序输出结果"))
    sortedWords = sorted(wordsFrequencyItems, key=lambda x: x[0], reverse=True)
    logger.success(f"3.按单词频次逆序输出结果:{sortedWords}")

    # 按出现顺序给出指定单词的所有位置(行号)
    wordsLoaction = {}
    for i in range(len(cleanedLines)):
        if len(cleanedLines[i]) != 0:
            for word in cleanedLines[i]:
                wordsLoaction[word] = wordsLoaction.get(word, [])
                wordsLoaction[word].append(i + 1)
    logger.success(f"4.按出现顺序给出指定单词的所有位置(行号):{wordsLoaction}")

    # TOP10单词词频显示
    top10 = sortedWords[:10]
    top10Words = []
    top10WordsCount = []
    result = []

    for item in top10:
        top10Words.append(item[1])
        top10WordsCount.append(item[0])
        result.append(f"{item[1]}:{item[0]}")
    result = "\n".join(result)
    logger.success(f"5.TOP10单词词频显示:\n{result}")

    # 生成TOP10单词词频条形图
    fig, ax = plt.subplots()
    colors = ['#80D0C7']
    ax.barh(top10Words, top10WordsCount, align='center', color=colors)
    ylabels = ax.get_yticks()
    ax.yaxis.set_major_locator(mticker.FixedLocator(ylabels))
    ax.set_yticklabels(top10Words, fontproperties="SimHei")
    ax.invert_yaxis()
    ax.set_title('TOP10单词词频', fontproperties="SimHei", fontsize=18)
    ax.set_xlabel("出现次数", fontproperties="SimHei")
    plt.savefig("条形图.png")
    plt.show()

    # 生成词云
    words = " ".join(rawWords)
    cloud = wordcloud.WordCloud(max_words=10, background_color="white")
    cloud.generate(words)
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()
    cloud.to_file("词云.png")


# GUI窗口
root = Tk()
root.title('词频统计')
root.geometry('+500+300')
e1 = Entry(root, width=100)
e1.grid(row=0, column=0)
btn1 = Button(root, text=' 选择文本文件 ', command=select).grid(row=1, column=0, pady=5)
mainloop()
