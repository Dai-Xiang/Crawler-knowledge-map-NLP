# coding:utf-8
import url_manager
import web_load
import web_resolve
import data_ouput
import get_user_agent
import knowledge_map
import requests
import GUI_main
import threading
import download_show
from tkinter import *
from tkinter import ttk
import csv
from py2neo import Graph, Node, Relationship, NodeMatcher
import time
from PIL import Image as PIL_Image
from PIL import ImageTk as PIL_ImageTk
import thulac
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
# proxypool_url = 'http://127.0.0.1:5555/random'
# target_url = 'proxy = get_random_proxy()'

num = 1
url_initial = ["https://movie.douban.com/top250", "https://movie.douban.com/top250?start=25&filter=",
               "https://movie.douban.com/top250?start=50&filter=", "https://movie.douban.com/top250?start=75&filter=",
               "https://movie.douban.com/top250?start=100&filter=", "https://movie.douban.com/top250?start=125&filter=",
               "https://movie.douban.com/top250?start=150&filter=", "https://movie.douban.com/top250?start=175&filter=",
               "https://movie.douban.com/top250?start=200&filter=", "https://movie.douban.com/top250?start=225&filter="]
url = []


def get_proxy():
    return requests.get("http://127.0.0.1:5000/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5000/delete/?proxy={}".format(proxy))



# 爬虫控制器
# 为爬虫运行器提供初始URL、代理IP以及控制爬虫运行器开始、停止的条件。


def spider(window_rain1, canvas1, rate1):
    global num
    global url_initial
    global url
    url = url_initial

    # items用来保存top250榜单数据
    items = []
    # items_data用来保存每一个影片的具体信息
    items_data = []
    test_len = 0
    # 爬取的内容以电影个数为界定，设置一个while语句便可解决爬虫控制器
    while num < 261:
        download_show.progress_rate(window_rain1, canvas1, rate1, num)
        # print(num)
        str_num = str(num)
        # 获取要抓取的url
        url_current = url_manager.remove(url, num)
        # 从代理池中随机筛选一个代理IP
        proxy = get_proxy().get("proxy")
        #proxy = get_random_proxy()

        # 如果请求失败，则返回的数据会小于60000，进行重新尝试
        while test_len < 60000:
            # 当代理池是空的时候，进行等待
            while not proxy:
                time.sleep(5)
                print('请等待，暂时无可用IP')
                proxy = get_proxy().get("proxy")
                # proxy = get_random_proxy()
                print('get random proxy', proxy)

            print(proxy)
            # 随机获取请求头
            headers = get_user_agent.agent()
            print(headers)
            # 获取网页内容
            test_len = web_load.load(url_current, headers, str_num, proxy)
            # 如果发现返回大小小于60000则说明IP被限制，要重新获取该网页内容
            if test_len < 60000:
                print('请求出错，请等待')
                time.sleep(10)
            print(test_len)
        new_url_list = web_resolve.resolver(str_num, items, num, items_data)
        if len(new_url_list) != 0:
            url_manager.load(new_url_list, url)
        test_len = 0
        num = num + 1
    # download_show.rate_of_progress(root_rain1, canvas1, rate1, num)
    data_ouput.data_out(items, items_data)
    num = num + 1
    # download_show.rate_of_progress(root_rain1, canvas1, rate1, num)
    return


def exit_window(root1):
    root1.destroy()
    return


# Btn2查看URL列表
# 主要是创建一个新的窗口
# 给窗口加上ListBox部件用以显示URL列表。
# 利用Tkinter中Listbox与Scrollbar来展示爬取过的url


def f_url_list():
    global url
    # 构造一个窗口，用来显示url列表
    window_url = Tk()
    window_url.title("URL LIST")
    window_url.geometry('800x600')
    window_url.resizable(width=True, height=True)
    Label(window_url, text='爬取豆瓣电影所用到的url').pack(side='top')
    Button(window_url, text='关闭', height=2, width=4, font=('楷体', 10),
           command=lambda: exit_window(window_url)).pack(side='bottom')
    sb = Scrollbar(window_url)
    sb.pack(side='right', fill='y')
    text_url = Listbox(window_url, bg='white', bd=2, font=('楷体', 20), fg='black', height=40,
                       width=60, yscrollcommand=sb.set)
    text_url.pack()
    sb.config(command=text_url.yview)
    for i in range(len(url)):
        text_url.insert('end', str(i+1)+'  '+url[i])
    window_url.mainloop()
    return


# 利用Tkinter中的Treeview创建表格界面用来展示爬取到的信息（信息以csv文件保存）
# Btn3查看爬取的数据


def f_data():
    window_data = Tk()
    window_data.title("DATA")
    window_data.geometry('800x600')
    window_data.resizable(width=True, height=True)
    Button(window_data, text='关闭', height=2, width=4, font=('楷体', 10),
           command=lambda: exit_window(window_data)).pack(side='bottom')
    f = open('电影详细信息.csv', 'r', encoding='utf-8')
    # data_all为列表，列表元素为字典
    data = csv.DictReader(f)
    data_all = []
    for i in data:
        i = dict(i)
        data_all.append(i)
    f.close()
    y_bar = Scrollbar(window_data, orient=VERTICAL)
    y_bar.pack(side='right', fill='y')
    x_bar = Scrollbar(window_data, orient=HORIZONTAL)
    x_bar.pack(side='bottom', fill='x')
    label = Label(window_data, text='豆瓣Top250电影详细信息').pack(side='top')
    ac = ["排名", "电影名称", "年份", "导演", "编剧", "主演", "类型", "制片国家", "语言", "上映日期", "片长", "别名",
          "剧情简介"]
    w_size = [60, 200, 60, 100, 100, 400, 60, 60, 60, 80, 80, 100, 300]
    # 构建一个树形部件
    # 建一个窗口变为添加Treeview部件来显示表格信息,可以以表格的方式进行显示，使用父类、子类相对较为方便。
    tree_data = ttk.Treeview(window_data, columns=ac, displaycolumns='#all', height=40, show='headings',
                             xscrollcommand=x_bar.set, yscrollcommand=y_bar.set)
    for i in range(len(ac)):
        tree_data.column(ac[i], width=w_size[i], anchor='center')
        tree_data.heading(ac[i], text=ac[i])
    # 将data_all中字典元素转化为列表
    data_all_list = []
    for i in data_all:
        temp = []
        for j in ac:
            if j == '剧情简介':
                i[j] = i[j].replace(' ', '')
                i[j] = i[j].replace('\n', '')
            temp.append(i[j])
        data_all_list.append(temp)
    for i in data_all_list:
        tree_data.insert('', 'end', value=i)
    tree_data.pack()
    y_bar.config(command=tree_data.yview)
    x_bar.config(command=tree_data.xview)
    window_data.mainloop()


# Button 5 token frequency statistics


def f_statistics():
    window_data = Tk()
    window_data.title("STATISTICS")
    window_data.geometry('800x600')
    window_data.resizable(width=True, height=True)
    Button(window_data, text='关闭', height=2, width=4, font=('楷体', 10),
           command=lambda: exit_window(window_data)).pack(side='bottom')
    y_bar = Scrollbar(window_data, orient=VERTICAL)
    y_bar.pack(side='right', fill='y')
    x_bar = Scrollbar(window_data, orient=HORIZONTAL)
    x_bar.pack(side='bottom', fill='x')
    label = Label(window_data, text='豆瓣Top250电影剧情简介词频统计').pack(side='top')
    ac = ["分词", "出现次数"]
    w_size = [60, 60]
    tree_data = ttk.Treeview(window_data, columns=ac, displaycolumns='#all', height=40, show='headings',
                             xscrollcommand=x_bar.set, yscrollcommand=y_bar.set)
    for i in range(len(ac)):
        tree_data.column(ac[i], width=w_size[i], anchor='center')
        tree_data.heading(ac[i], text=ac[i])
    df = pd.read_csv('token_freq.csv')
    for i in range(len(df['分词'])):
        tree_data.insert('', 'end', value=[df['分词'][i], df['出现次数'][i]])
    tree_data.pack()
    window_data.mainloop()


# Button 6 情感分析


def sentiment_analysis(tk1, tk2):
    bert_tokenizer = BertTokenizer.from_pretrained('../../bert-base-chinese')
    bert_cls_model = BertForSequenceClassification.from_pretrained('../../bert-base-chinese/bert_chn_movie')
    text = tk1.get(1.0, END)  # 获取所有
    encoding = bert_tokenizer(text, truncation=True, padding=True, return_tensors='pt')
    with torch.no_grad():
        output = bert_cls_model(**encoding)
        prob = torch.softmax(output.logits, dim=-1).view(-1)
        pred = torch.argmax(output.logits, dim=-1)
    tk2.delete(1.0, END)
    result = '积极评论, ' if pred == 1 else '消极评论, '
    result += '置信度为 {}'.format(str(prob[pred].item()))
    tk2.insert(1.0, result)


def f_senti_analysis():
    # =========1.主窗口============
    root = Tk()  # 创建主窗口
    # =========2.创建、安放组件===========
    # label_2 = Label(root, text='情感分析结果', font=('楷体', 20))
    t_1 = Text(root, width=50, height=8, font=('楷体', 18))
    label_1 = Label(root, text='请输入电影评论', font=('楷体', 18))
    label_1.grid(row=0, column=0)
    t_1.grid(row=0, column=1, columnspan=3)

    t_2 = Text(root, width=50, height=3, font=('楷体', 18))
    label_2 = Label(root, text='情感分析结果', font=('楷体', 18))
    label_2.grid(row=1, column=0)
    t_2.grid(row=1, column=1, columnspan=3)
    b3 = Button(root, text='情感分析', font=('楷体', 12), command=lambda: sentiment_analysis(t_1, t_2))
    b3.grid(row=2, column=2)

    root.mainloop()  # 阻止窗口关闭


def show_result(graph1, query_name1, text1):
    content_list = ["排名", "电影名称", "年份", "导演", "编剧", "主演", "类型", "制片国家", "语言", "上映日期", "片长", "别名",
             "剧情简介"]
    content_dic = {"排名": [], "电影名称": [], "年份": [], "导演": [], "编剧": [], "主演": [], "类型": [], "制片国家": [],
               "语言": [], "上映日期": [], "片长": [], "别名": [], "剧情简介": []}
    title = []
    input_name = query_name1.get()
    print(input_name)

    # 使用cypher语句首先将知识图谱中的结点和关系都找到，
    # 然后在结点和关系中进行匹配，来找到相应的结点或者关系，然后显示在gui上

    cypher_1 = "MATCH (n) RETURN id(n) as id, labels(n) as labels, n.name, n.rank, n.language, n.duration, n.alias, n.release_data, n.synopsis LIMIT 5000"
    cypher_2 = "MATCH (a)-[r]->(b) RETURN id(a) as a_id, a.name, type(r), id(b) as b_id, b.name LIMIT 5000"
    # 在知识图谱neo4j中查询，并使用.data()序列化数据
    nodes_data = graph1.run(cypher_1).data()
    links_data = graph1.run(cypher_2).data()
    link_name = ['a.name', 'b.name']
    tag = 0
    for link in nodes_data:
        if link['n.name'].find(input_name) != -1:
            if link['labels'] == ['films']:
                tag = 1
                title.append(link['n.name'])
                title.append(link['labels'][0])
                content_dic['电影名称'].append(link['n.name'])
                content_dic['排名'].append(link['n.rank'])
                content_dic['语言'].append(link['n.language'])
                content_dic['片长'].append(link['n.duration'])
                content_dic['别名'].append(link['n.alias'])
                content_dic['上映日期'].append(link['n.release_data'])
                content_dic['剧情简介'].append(link['n.synopsis'])
            else:
                tag = 0
                title.append(link['n.name'])
                title.append(link['labels'][0])
    for link in links_data:
        if link[link_name[tag]].find(input_name) != -1:
            if link['type(r)'] == '上映年份':
                content_dic['年份'].append(link[link_name[1-tag]])
            elif link['type(r)'] == '导演':
                content_dic['导演'].append(link[link_name[1-tag]])
            elif link['type(r)'] == '编剧':
                content_dic['编剧'].append(link[link_name[1-tag]])
            elif link['type(r)'] == '参演':
                content_dic['主演'].append(link[link_name[1-tag]])
            elif link['type(r)'] == '类型':
                content_dic['类型'].append(link[link_name[1-tag]])
            elif link['type(r)'] == '制片地区':
                content_dic['制片国家'].append(link[link_name[1-tag]])
    # 展现匹配所得节点或关系
    text1.delete('1.0', 'end')
    if len(title) == 0:
        text1.insert('1.0', '很抱歉并未找到你所需要的内容')
        text1.tag_add('tag1', '1.0', '1.end')
        text1.tag_config('tag1', font=('行楷', 20))
        return
    text1.insert('1.0', title[0])
    text1.insert('1.end', ' ('+title[1]+')')
    text1.tag_add('tag1', '1.0', '1.'+str(len(title[0])))
    text1.tag_config('tag1', font=('行楷', 20))
    text1.insert(INSERT, '\n')

    for i in content_list:
        mark = 0
        if len(content_dic[i]) != 0:
            mark = 1
            if tag == 0:
                text1.insert('end', i+'的电影: ')
            else:
                text1.insert('end', i + ': ')
            for j in content_dic[i]:
                text1.insert('end', j+'   ')
        if mark == 1:
            text1.insert(INSERT, '\n')
    print(title)
    print(content_dic)


# Btn4构建知识图谱（带有查询功能）
# 调用创建知识图谱的主函数，同时在知识图谱主函数中添加了进度条函数,方便知晓何时创建完成知识图谱


def k_map():
    graph = Graph('http://localhost:7474', auth=('neo4j', 'qwe123456789'))
    graph.delete_all()
    root_finder = Tk()
    root_finder.title("查找各种关系")
    root_finder.geometry('800x600')
    root_finder.resizable(width=False, height=False)
    query_name = StringVar(root_finder)
    Label(root_finder, text='查询界面').pack(side='top')
    entry = Entry(root_finder, bg='white', bd=3, font=('宋体', 20), fg='black',
                  relief='raised', width=54, textvariable=query_name).place(x=10, y=30)
    # btn_inquire创建一个用于调用查询函数的按钮
    # btn_inquire = Button(root_finder, font=('楷体', 15), text='查询', bd=2, width=4)
    # btn_inquire.place(x=730, y=20)

    # 创建进度条
    canvas = Canvas(root_finder, bg='black', height=20, width=800)
    canvas.pack(side='bottom')
    canvas.create_rectangle((0, 0, 800, 20), outline='white', width=2)

    # 调用mapping_knowledge_domain.produce进行知识图谱的绘制
    knowledge_map.produce(graph, root_finder, canvas)

    # 进度条销毁
    canvas.destroy()
    # btn_exit创建一个用于关闭查询界面的按钮
    # Button(root_finder, font=('楷体', 15), text='加载完成可以查询，点击关闭', bd=2, width=30,
    #        command=lambda: exit_window(root_finder)).place(x=700, y=560)

    y_bar = Scrollbar(root_finder, orient=VERTICAL)
    y_bar.pack(side='right', fill='y')

    text = Text(root_finder, bg='LightBlue', bd=3, font=('宋体', 10), fg='black', spacing1=10, height=21, width=120,
                wrap='char', yscrollcommand=y_bar.set)
    text.pack(side='bottom')

    Button(root_finder, font=('宋体', 15), text='点击查询', bd=2, width=8,
           command=lambda: show_result(graph, query_name, text)).place(x=50, y=560)
    root_finder.update()
    root_finder.mainloop()
    return

# 点击Btn1按钮,启动爬虫程序


def spider_run():
    ################################################################################################################
    window_rain = Toplevel()
    window_rain.title("SPIDER")
    window_rain.geometry('800x600')
    window_rain.resizable(width=True, height=True)
    Button(window_rain, text='当数据导出完成时关闭', height=2, width=20, font=('楷体', 10),
           command=lambda: exit_window(window_rain)).pack(side='bottom')
    canvas = Canvas(window_rain, height=600, width=800)
    canvas.pack()
    image = PIL_Image.open("spider.png")
    pyt = PIL_ImageTk.PhotoImage(image)
    canvas.create_image((400, 300), image=pyt)
    drop = []
    height = []
    rec = canvas.create_rectangle((1, 290, 799, 310), outline='black', fill='Wheat', width=2)
    rate = canvas.create_text(400, 280, fill='black', font=('楷体', 20), text='0%')
    canvas.pack()
    # m1 = threading.Thread(target=download_show.work, args=(window_rain, canvas, drop, height))
    # 一个线程用来加载数字雨背景。
    m2 = threading.Thread(target=spider, args=(window_rain, canvas, rate))
    # 一个线程更新速度
    # m3 = threading.Thread(target=download_show.rate_of_progress, args=(window_rain, canvas, rate))
    # 启动爬虫程序
    # m1.start()
    m2.start()
    # m3.start()
    window_rain.mainloop()
    ################################################################################################################



# spider()
if __name__ == '__main__':
    GUI_main.gui(spider_run, f_url_list, f_data, k_map, f_statistics, f_senti_analysis)



