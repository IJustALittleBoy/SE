import pandas as pd
import sys


# 以追加的方式写入文件
def input_file(out_file):
    filename_out = 'yq_out.txt'
    fileopen = open(filename_out, "a")
    fileopen.writelines(out_file)
    fileopen.close()


# 将文件内容清空
def clear_file():
    filename_out = 'yq_out.txt'
    fileopen = open(filename_out, "w")
    fileopen.writelines('')
    fileopen.close()


# ff = sys.argv[1]

# 将txt文件转成csv
df = pd.read_csv('yq_in.txt', encoding='GBK', delimiter="\t")
df.to_csv("yq_1in.csv", encoding='GBK', index=False)
# 对数据进行相应类型转换处理
f1 = pd.read_csv("yq_1in.csv", encoding='GBK', header=None)
f1 = f1.values

province = []
l = []
i = 0
j = 0
# 按省份进行分割
for e in f1:
    if i > 0:
        if f1[i][0] != f1[i - 1][0]:
            l1 = f1[j:i]
            # 提取省份头部
            province.append(f1[i - 1][0])
            l.append(l1)
            j = i
        if i == len(f1) - 1:
            l1 = f1[j:i + 1]
            province.append(f1[i - 1][0])
            l.append(l1)
    i += 1

j = 0
# 清空文件
clear_file()
# 将各省份地区依次写入
for a in l:
    a = a[:, 1:]
    a.tolist()
    old = "'"
    new = ""
    if j > 0:
        input_file("\n")
    # 写入省份
    input_file(province[j])
    input_file("\n")
    for i in a:
        i = str(i)
        i = i.replace(old, new, 2)
        if "待明确地区 0" in i:
            continue
        # i = i.replace("待明确地区 0",new,len(province))
        i = i.replace(" ", "\t")
        input_file(i[1:len(i) - 1] + "\n")
    j += 1
