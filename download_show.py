from tkinter import *
import random
import time
import threading


# # rain_make函数实现随机构造数字雨滴
# def rain_make(canvas1, text1, drop1, height1):
#     # char_h为各个字符的间距
#     char_h = 20
#     for i1 in text1:
#         temp1 = []
#         # 随机生成数字雨的x坐标
#         x1 = random.randrange(10, 790, 20)
#         # height1用来标记数字雨的存活时间
#         height1.append(0)
#         for j1 in range(len(i1)):
#             y1 = -1*j1*char_h
#             # if语句是用来设置数字雨的颜色
#             if j1 < 5:
#                 color = 'Lime'
#             elif j1 < 10:
#                 color = 'LimeGreen'
#             else:
#                 color = 'Green'
#             # 将数字雨对象的ID存放到temp1中，一组ID代表一个数字雨
#             temp1.append(canvas1.create_text(x1, y1, fill=color, font=('楷体', 20), text=i1[j1], width=2))
#         # 将构造好的数字雨ID组添加到drop1列表中，drop1列表用于后续数字雨的移动
#         drop1.append(temp1)
#
#
# # rain_drop函数是用来控制数字雨滴的移动
# def rain_drop(window1, canvas1, drop1, height1):
#     # time.sleep(0.001)
#     i1 = 0
#     while i1 < len(drop1):
#         # 随机生成移动步长，用来产生各数字雨滴移动快慢不同的现象
#         rnd = random.randint(10, 50)
#         # height1当其大于50，则雨滴消失
#         height1[i1] = height1[i1] + 1
#         for j1 in range(len(drop1[i1])):
#             # 进行雨滴的整体移动
#             canvas1.move(drop1[i1][j1], 0, rnd)
#             window1.update()
#         if height1[i1] > 50:
#             # 雨滴消失判定条件成立，则将雨滴的ID从drop1中移除
#             for z in range(len(drop1[i1])):
#                 canvas1.delete(drop1[i1][z])
#                 window1.update()
#             drop1.pop(0)
#             height1.pop(0)
#             i1 = i1 - 1
#         i1 = i1 + 1
#
#
# # work函数用来产生数字雨的整体效果
# def work(window1, canvas1, drop1, height1):
#     letter = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd']
#     n = 0
#     while n < 100:
#         text_len = random.randint(10, 20)
#         text_num = random.randint(6, 12)
#         text = []
#         for i in range(text_num):
#             # 构造数字雨滴的序列
#             temp_text = []
#             for j in range(text_len):
#                 temp_text.append(random.choice(letter))
#             text.append(temp_text)
#         rain_make(canvas1, text, drop1, height1)
#         temp_n = random.randint(5, 10)
#         while temp_n > 0:
#             rain_drop(window1, canvas1, drop1, height1)
#             temp_n = temp_n - 1
#         n = n + 1
#     n = 0
#     # while循环用来实现最后一组雨滴的完整落下
#     while n < 100:
#         rain_drop(window1, canvas1, drop1, height1)
#         n = n + 1


# progress_rate函数用来实现展示进度条
def progress_rate(window1, canvas1, rate1, num1):
    if num1 < 261:
        print(num1)
        time.sleep(0.01)
        rate_num = round(num1*100/260)
        canvas1.create_rectangle((1, 290, rate_num*7.99, 310), fill='white', outline='white')
        canvas1.itemconfig(rate1, text=str(rate_num)+'%')
        window1.update()
        return
    elif num1 == 261:
        canvas1.itemconfig(rate1, text='正在导出数据')
        return
    else:
        time.sleep(5)
        canvas1.itemconfig(rate1, text='导出数据完成')


# def work_all():
#     window = Tk()
#     window.title("hello world")
#     window.geometry('800x600')
#     window.resizable(width=True, height=True)
#     canvas = Canvas(window, bg='black', height=600, width=800)
#     canvas.pack()
#     drop = []
#     height = []
#     rec = canvas.create_rectangle((1, 290, 799, 310), outline='white', width=2)
#     rate = canvas.create_text(780, 300, fill='gray', font=('宋体', 20), text='0%')
#     m2 = threading.Thread(target=rate_of_progress, args=(window, canvas, rate))
#     m1 = threading.Thread(target=work, args=(window, canvas, drop, height))
#     m2.start()
#     m1.start()
#     window.mainloop()
