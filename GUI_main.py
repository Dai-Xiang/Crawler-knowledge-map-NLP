from tkinter import *
from PIL import Image as PIL_Image
from PIL import ImageTk as PIL_ImageTk
# Tkinter进行编写
# 一个标题框、四个按钮。标题框是用来显示本课题的名称；
# 四个按钮分别用来执行不同的操作命令：运行爬虫程序、显示URL列表、显示爬取到的数据、构建知识图谱（带有查询功能）。


def gui(fun1, fun2, fun3, fun4, fun5, fun6):
    # 初始化Tk
    window = Tk()

    # 设置窗口标题
    window.title('爬虫——豆瓣Top250')

    # 设置窗口大小
    window.geometry('600x500')

    # 设置窗口的高、是的宽是否可变，False不可变，True可变
    window.resizable(width=True, height=True)


    # 设置一个框架frm1用来存放窗口部件
    frm1 = Frame(window, bd=2, height=600, width=800, relief='ridge')
    frm1.pack(side='top', padx=5, pady=5)
    # 设置Label显示标题
    label1 = Label(frm1, text='爬虫——豆瓣电影Top250', font=('楷体', 24), width=30, height=3)
    label1.grid(row=0,columnspan=2,padx=10, pady=10)

    # canvas = Canvas(frm1, height=576, width=1024)
    # canvas.grid(row=1,columnspan=2)
    # image = PIL_Image.open("pic2.png")
    # pyt = PIL_ImageTk.PhotoImage(image)
    # canvas.create_image((0, 0), image=pyt)

    # 设置button来进行各种功能的实现
    button1 = Button(frm1, text='启动爬虫程序', font=('楷体', 14), width=16, height=2, command=fun1)
    button1.grid(row=1, column=0, padx=2, pady=10)
    button2 = Button(frm1, text='查看URL列表', font=('楷体', 14), width=16, height=2, command=fun2)
    button2.grid(row=1, column=1, padx=2, pady=10)
    button3 = Button(frm1, text='查看爬取的数据', font=('楷体', 14), width=16, height=2, command=fun3)
    button3.grid(row=2, column=0, padx=2, pady=10)
    button4 = Button(frm1, text='构建知识图谱', font=('楷体', 14), width=16, height=2, command=fun4)
    button4.grid(row=2, column=1, padx=2, pady=10)
    button5 = Button(frm1, text='词频统计', font=('楷体', 14), width=16, height=2, command=fun5)
    button5.grid(row=3, column=0, padx=2, pady=10)
    button6 = Button(frm1, text='情感分析', font=('楷体', 14), width=16, height=2, command=fun6)
    button6.grid(row=3, column=1, padx=2, pady=10)
    # 进入消息循环
    window.mainloop()
