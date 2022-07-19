import matplotlib.pyplot as plt  # 用于生成词频条形图的库
import matplotlib.ticker as mticker
import wordcloud
import json
from tkinter import *
import tkinter.filedialog

fileName = ""
logFileName = 'result_log.txt'
defaultCount = 50
excludeWords = ['a', 'the', 'en', 'hello', 'where', 'why', 'there', 'for', 'as', 'because', 'but', 'not', 'is', 'he', 'she', 'her', 'his', 'about', 'and', 'upon', 'on',
                'at', 'in', 'after', 'with', 'by', 'was', 'were', 'still', 'then', 'so', 'to', 'did', 'do', 'dose', 'it', 'its', 'by', 'whom', 'what', 'an', 'does', 'am', 'i', 'of']

# 选择文件


def select1():
    global fileName
    fileName = tkinter.filedialog.askopenfilename(title='选择文件')
    fileNameEntry.delete(0, END)
    fileNameEntry.insert(0, fileName)


def select2():
    global logFileName
    logFileName = tkinter.filedialog.askopenfilename(title='选择文件')
    logFileNameEntry.delete(0, END)
    logFileNameEntry.insert(0, logFileName)


def revise():
    global defaultCount
    defaultCount = int(countLimitEntry.get())


# 清理标点符号
def clean(line):
    punctuations = "',.()-[];!?<>/:{}\|_=+*&^%$#@~`"
    for c in punctuations:
        if c in line:
            line = line.replace(c, "")
    line = line.lower().strip().split()
    return line


# 开始执行
def analyse():
    logFile = open(logFileName, "w+", encoding="utf-8")
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
    logFile.write(f"1.分解出单词列表:\n{rawWords}\n")
    print("{:-^100}".format("1.分解出单词列表"))
    for i in range(defaultCount):
        print(rawWords[i])
    print("{:-^120}".format("1"))

    # 得出单词频次字典
    wordsFrequency = {}
    for line in cleanedLines:
        for word in line:
            if word not in excludeWords:
                wordsFrequency[word] = wordsFrequency.get(word, 0) + 1
    logFile.write(f"2.得出单词频次字典:\n{wordsFrequency}\n")
    print("{:-^100}".format("2.得出单词频次字典"))
    tempWordsFrequency = {}
    i = 0
    for k in wordsFrequency:
        if i < defaultCount:
            i += 1
            tempWordsFrequency.update({k: wordsFrequency[k]})
        else:
            break
    print(json.dumps(tempWordsFrequency, indent=4, ensure_ascii=False))
    print("{:-^120}".format("2"))

    # 按单词频次逆序输出结果
    wordsFrequencyItems = []
    for item in wordsFrequency.items():
        word, amount = item
        newItem = (amount, word)
        wordsFrequencyItems.append(newItem)
    sortedWords = sorted(wordsFrequencyItems, key=lambda x: x[0], reverse=True)
    logFile.write(f"3.按单词频次逆序输出结果:\n{sortedWords}\n")
    print("{:-^100}".format("3.按单词频次逆序输出结果"))
    for i in range(defaultCount):
        print(sortedWords[i])
    print("{:-^120}".format("3"))

    # 按出现顺序给出指定单词的第一次出现的位置(行号)
    wordsLoaction = {}
    for i in range(len(cleanedLines)):
        if len(cleanedLines[i]) != 0:
            for word in cleanedLines[i]:
                if word not in excludeWords:
                    wordsLoaction[word] = wordsLoaction.get(word, -1)
                    if wordsLoaction[word] == -1:
                        wordsLoaction[word] = i + 1
    logFile.write(f"4.按出现顺序给出指定单词的第一次出现的位置(行号):\n{wordsLoaction}\n")
    print("{:-^100}".format("4.按出现顺序给出指定单词的第一次出现的位置(行号)"))
    tempWordsLoaction = {}
    i = 0
    for k in wordsLoaction:
        if i < defaultCount:
            i += 1
            tempWordsLoaction.update({k: wordsLoaction[k]})
        else:
            break
    print(json.dumps(tempWordsLoaction, indent=4))
    print("{:-^120}".format("4"))

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
    logFile.write(f"5.TOP10单词词频显示:\n{result}\n")
    print("{:-^100}".format("5.TOP10单词词频显示"))
    print(result)
    print("{:-^120}".format("5"))
    logFile.close()

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
    plt.savefig(f'{fileName.replace(".txt","")}条形图.png')
    plt.show()

    # 生成词云
    words = " ".join(rawWords)
    cloud = wordcloud.WordCloud(max_words=10, background_color="white")
    cloud.generate(words)
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()
    cloud.to_file(f'{fileName.replace(".txt","")}词云.png')


# GUI窗口
root = Tk()
root.title('词频统计')
root.geometry('+800+600')

fileNameLabel = Label(root, text="待分析文本文件所在路径：")
fileNameLabel.pack()
fileNameEntry = Entry(root, width=80)
fileNameEntry.pack()
button1 = Button(root, text=' 选择文件 ', command=select1)
button1.pack()

logFileNameLabel = Label(root, text="日志文件所在路径：")
logFileNameLabel.pack()
logFileNameEntry = Entry(root, width=80)
logFileNameEntry.pack()
logFileNameEntry.delete(0, END)
logFileNameEntry.insert(0, logFileName)
button2 = Button(root, text=' 选择文件 ', command=select2)
button2.pack()

countLimitLabel = Label(root, text="控制台输出单词个数限制：")
countLimitLabel.pack()
countLimitEntry = Entry(root, width=80)
countLimitEntry.pack()
countLimitEntry.delete(0, END)
countLimitEntry.insert(0, str(defaultCount))
button3 = Button(root, text=' 确认修改 ', command=revise)
button3.pack()

finalLabel = Label(root, text="执行：")
finalLabel.pack()
button4 = Button(root, text=' 开始分析 ', command=analyse)
button4.pack()

mainloop()
print("结束运行")
