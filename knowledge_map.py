# coding:utf-8
from py2neo import Graph, Node, Relationship, NodeMatcher
import csv
from tkinter import *


#调用node_set()函数和relationship_set()函数进行结点和关系的创建。
def node_set(dict1, node_list1, key1, label1):
    temp1 = dict1[key1].replace(' ', '')
    temp_list1 = temp1.split('/')
    for j1 in temp_list1:
        node_list1.append(Node(label1, name=j1))
    return


def relationship_set(graph1, node1, node2, node2_label, relationship1):
    matcher = NodeMatcher(graph1)
    nodelist = list(matcher.match(node2_label, name=node2['name']))
    if len(nodelist) > 0:  # 表示节点存在，不需创建新的节点
        node_temp = nodelist[0]
        relation_temp = Relationship(node_temp, relationship1, node1)
        graph1.create(relation_temp)
    else:
        graph1.create(node2)
        relation_temp = Relationship(node2, relationship1, node1)
        graph1.create(relation_temp)
    return


def produce(graph, root1, canvas1):
    # 曾睿的电脑neo4j密码如下
    # graph = Graph('http://localhost:7474', username='neo4j', password='123456')

    # 将csv文件变成列表，以字典的形式存储数据
    f = open('电影详细信息.csv', 'r', encoding='utf-8')
    data = csv.DictReader(f)
    data_all = []
    for i in data:
        i = dict(i)
        data_all.append(i)
    f.close()

    # 这是一种将str里的空格去除，并将其按照'/'分割成列表的一种方法，下面会用到
    # temp = data_all[0]['主演'].replace(' ', '')
    # temp_list = temp.split('/')
    test_num = 1
    for i in data_all:
        # 构造films节点
        node_films = Node('films', name=i['电影名称'])

        # 添加films的属性值，包括排名、语言、上映日期、片长、别名、剧情简介
        node_films['rank'] = i['排名']
        node_films['language'] = i['语言']
        node_films['release_data'] = i['上映日期']
        node_films['duration'] = i['片长']
        node_films['alias'] = i['别名']
        temp = i['剧情简介'].replace(' ', '')
        node_films['synopsis'] = temp.replace('\n', '')

        # 构造year节点
        node_year = Node('year', name=i['年份'])
        # 构造director节点列表
        node_director = []
        node_set(i, node_director, '导演', 'director')
        # 构造scriptwriter节点列表
        node_scriptwriter = []
        node_set(i, node_scriptwriter, '编剧', 'scriptwriter')
        # 构造actor节点列表
        node_actor = []
        node_set(i, node_actor, '主演', 'actor')
        # 构造type节点列表
        node_type = []
        node_set(i, node_type, '类型', 'type')
        # 构造country节点列表
        node_producer_country = []
        node_set(i, node_producer_country, '制片国家', 'producer_country')

        # 创建各种节点到neo4j
        graph.create(node_films)
        relationship_set(graph, node_films, node_year, 'year', '上映年份')
        for node_i in node_director:
            relationship_set(graph, node_films, node_i, 'director', '导演')
        for node_i in node_scriptwriter:
            relationship_set(graph, node_films, node_i, 'scriptwriter', '编剧')
        for node_i in node_actor:
            relationship_set(graph, node_films, node_i, 'actor', '参演')
        for node_i in node_type:
            relationship_set(graph, node_films, node_i, 'type', '类型')
        for node_i in node_producer_country:
            relationship_set(graph, node_films, node_i, 'producer_country', '制片地区')
        print(test_num)
        rate_num = round(test_num * 100 / 250)
        canvas1.create_rectangle((0, 0, rate_num * 8, 20), fill='white', outline='white')
        root1.update()
        test_num = test_num + 1
    return
