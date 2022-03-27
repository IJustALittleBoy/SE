import pandas as pd
import sys
import numpy as np


class Yq_process:
    outfileName = 'yq_out.txt'

    def __init__(self, filename, *user_outNmae):
        self.filename = filename
        if len(user_outNmae) > 0:
            self.outfileName = user_outNmae[0]

    def input_file(self, file, fout):
        filename_out = fout
        fileopen = open(filename_out, "a")
        fileopen.writelines(file)
        fileopen.close()

    # 将文件内容清空
    def clear_file(self, FileName):
        # filename_out = 'yq_out.txt'
        fileopen = open(FileName, "w")
        fileopen.writelines('')
        fileopen.close()

    def reSetName(self, filename):
        self.outfileName = filename

    def pretreament(self, fileName):
        df = pd.read_csv(fileName, encoding='GBK', delimiter="\t")
        df.to_csv("yq_in.csv", encoding='GBK', index=False)
        # 对数据进行相应类型转换处理
        f1 = pd.read_csv("yq_in.csv", encoding='GBK', header=None)
        f1 = f1.values
        return f1

    def separation(self, fileName):
        province = []
        l = []
        i = 0
        j = 0
        # 按省份进行分割
        for e in fileName:
            if i > 0:
                if fileName[i][0] != fileName[i - 1][0]:
                    l1 = fileName[j:i]
                    # 提取省份头部
                    province.append(fileName[i - 1][0])
                    l.append(l1)
                    j = i
                if i == len(fileName) - 1:
                    l1 = fileName[j:i + 1]
                    province.append(fileName[i - 1][0])
                    l.append(l1)
            i += 1
        return [province, l]

    def sortOfprovince(self, fileName):
        province = fileName[0]
        l = fileName[1]
        L_sort = []
        province_sort = []
        SumList = []
        for a in l:
            Sum = 0
            for k in a:
                Sum += k[2]
            SumList.append(Sum)
            SumList_sort = SumList.copy()
            SumList_sort.sort()
            SumList_sort.reverse()

        for num in SumList_sort:
            L_sort.append(l[SumList.index(num)])
            province_sort.append(province[SumList.index(num)])
        return [province_sort, L_sort, SumList_sort]

    def reWrite(self):
        self.clear_file(self.outfileName)
        filename = self.filename
        f1 = self.pretreament(self.filename)
        result = self.separation(f1)
        province = result[0]
        l = result[1]
        fout = self.outfileName
        j = 0
        for a in l:
            a = a[:, 1:]
            old = "'"
            new = ""
            if j > 0:
                self.input_file("\n", fout)
            # 写入省份
            self.input_file(province[j] + '\t' + '\n', fout)
            for i in a:
                i = str(i)
                i = i.replace(old, new, 2)
                if "待明确地区 0" in i:
                    continue
                # i = i.replace("待明确地区 0",new,len(province))
                i = i.replace(" ", "\t")
                self.input_file(i[1:len(i) - 1] + "\n", fout)
            j += 1

    def reWriteBySum(self):
        self.clear_file(self.outfileName)
        filename = self.filename
        self.clear_file
        f1 = self.pretreament(filename)
        result = self.separation(f1)
        result_sort = self.sortOfprovince(result)
        province_sort = result_sort[0]
        L_sort = result_sort[1]
        SumList_sort = result_sort[2]
        fout = self.outfileName
        j = 0
        for a in L_sort:
            a_sort = []
            a = a[:, 1:]
            # 省内各市按人数从大到小排序
            for b in np.lexsort(a.T):
                a_sort.append(a[b])
            a_sort.reverse()
            old = "'"
            new = ""
            if j > 0:
                self.input_file("\n", fout)
            # 写入省份
            self.input_file(province_sort[j] + '\t' + str(SumList_sort[j]) + "\n", fout)
            for i in a_sort:
                i = str(i)
                i = i.replace(old, new, 2)
                if "待明确地区 0" in i:
                    continue
                # i = i.replace("待明确地区 0",new,len(province))
                i = i.replace(" ", "\t")
                self.input_file(i[1:len(i) - 1] + "\n", fout)
            j += 1

    def reWriteByProvince(self, province):
        self.clear_file(self.outfileName)
        filename = self.filename
        self.clear_file
        f1 = self.pretreament(filename)
        result = self.separation(f1)
        result_sort = self.sortOfprovince(result)
        province_sort = result_sort[0]
        L_sort = result_sort[1]
        SumList_sort = result_sort[2]
        fout = self.outfileName
        j = 0
        for a in L_sort:
            if province == province_sort[j]:
                a_sort = []
                a = a[:, 1:]
                # 省内各市按人数从大到小排序
                for b in np.lexsort(a.T):
                    a_sort.append(a[b])
                a_sort.reverse()
                old = "'"
                new = ""

                # 写入省份
                self.input_file(province_sort[j] + '\t' + str(SumList_sort[j]) + '\n', fout)
                for i in a_sort:
                    i = str(i)
                    i = i.replace(old, new, 2)
                    if "待明确地区 0" in i:
                        continue
                    # i = i.replace("待明确地区 0",new,len(province))
                    i = i.replace(" ", "\t")
                    self.input_file(i[1:len(i) - 1] + "\n", fout)
            j += 1
