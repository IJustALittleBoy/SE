import py_module
from py_module import Yq_process


file = input('输入要处理的文件名:')
outfile = input('输入指定文件名（默认为"yq_out.txt"）:')
if len(outfile) > 0:
    test = Yq_process(file,outfile)
else:
    test = Yq_process(file)


while True:
    option = int(input('输入1普通处理,2按总数排序处理输出,3指定省份处理输出,4重设输出文件名,5退出程序: '))
    if option == 1:
        test.reWrite()
    elif option == 2:
        test.reWriteBySum()
    elif option == 3:
        province = input('省份:')
        test.reWriteByProvince(province)
    elif option == 4:
        filename = input('文件名:')
        test.reSetName(filename)
    elif option == 5:
        break
    print('处理完成')