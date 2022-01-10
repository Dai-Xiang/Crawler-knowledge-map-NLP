import xlwt
import csv

#数据输出器
#该函数为out(),主要是通过调用python的csv库文件，对列表数据进行写文件的操作来完成电影信息csv文件的输出。
# out函数用来保存数据到本地
def data_out(items1, items_data1):
    title = ["电影名", "年份", "评分", "评价人数", "最热评论"]
    # book = xlwt.Workbook()  # 创建一个excel对象
    # sheet = book.add_sheet('Sheet1', cell_overwrite_ok=True)  # 添加一个sheet页
    # # 添加标题和数据
    # for m in range(len(title)):
    #     sheet.write(0, m, title[m])
    # for i in range(len(items1)):  # 循环列
    #     for j in range(len(items1[i])):
    #         sheet.write(i + 1, j, items1[i][j])  # 将title数组中的字段写入到0行i列中
    # # 保存数据
    # book.save('C:/Users/89829/Desktop/Software_curriculum_design/电影信息.xlsx')  # 保存excel
    with open('电影信息.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=title)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writeheader()  # 写入列名
        writer.writerows(items1)  # 写入数据

    ###################################################################################################
    title = ["排名", "电影名称", "年份", "导演", "编剧", "主演", "类型", "制片国家", "语言", "上映日期", "片长", "别名",
             "剧情简介"]
    # book = xlwt.Workbook()  # 创建一个excel对象
    # sheet = book.add_sheet('Sheet1', cell_overwrite_ok=True)  # 添加一个sheet页
    # # 添加标题和数据
    # for m in range(len(title)):
    #     sheet.write(0, m, title[m])
    # for i in range(len(items_data1)):  # 循环列
    #     for j in range(len(items_data1[i])):
    #         sheet.write(i + 1, j, items_data1[i][j])  # 将title数组中的字段写入到0行i列中
    # # 保存数据
    # book.save('C:/Users/89829/Desktop/Software_curriculum_design/电影详细信息.xlsx')  # 保存excel
    with open('电影详细信息.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=title)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writeheader()  # 写入列名
        writer.writerows(items_data1)  # 写入数据
    return
