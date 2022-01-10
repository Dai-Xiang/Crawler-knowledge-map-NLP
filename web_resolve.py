import requests
from bs4 import BeautifulSoup
import re


# resolver函数用来解析网页内容
#接受本地网页数据库中传进来的数据，
# 对其进行分析，得到电影名称、导演、演员等信息，并将其保存在列表中，
def resolver(temp, items1, num1, items_data1):
    path = 'database/' + temp + '.html'
    f1 = open(path, 'r', encoding='utf-8')
    ret = f1.read()
    f1.close()
    soup = BeautifulSoup(ret, 'lxml')
    # 提取榜单数据
    if num1 <= 10:
        new_urls = []
        result = soup.select('div[class="info"]')
        for i in result:
            name = []
            year = []
            grade = []
            number = []
            commentator = []
            if len(i.select('a')) != 0:
                new_url = i.select('a')[0].get("href")
                new_urls.append(new_url)
            if len(i.select('div a span')) != 0:
                name = i.select('div a span')[0].get_text()
            if len(i.select('div div p')) != 0:
                string = i.select('div div p')[0].get_text()
                year = re.findall('(\w*[0-9]+)\w*', string)[0]  # 用re模块处理数据，提取数值
            if len(i.select('div')) > 1:
                if len(i.select('div')[1].select('div div span')) > 1:
                    grade = i.select('div')[1].select('div div span')[1].get_text()
                if len(i.select('div')[1].select('div div span')) > 3:
                    b = i.select('div')[1].select('div div span')[3].get_text()
                    number = re.findall('(\w*[0-9]+)\w*', b)[0]  # 用re模块处理数据，提取数值
            if len(i.select('div')) > 1:
                if len(i.select('div')[1].select('div p span')) > 0:
                    commentator = i.select('div')[1].select('div p span')[0].get_text()
            item = {"电影名": name, "年份": year, "评分": grade, "评价人数": number, "最热评论": commentator}
            items1.append(item)
        return new_urls
    else:
        new_urls = []
        result = soup.select('div[id="content"]')
        # 获取该影片在top250中的排名
        data_rank = []
        result_rank = result[0].select('div[class="top250"]')
        data_rank = result_rank[0].select('span')[0].get_text()

        # 获取该影片的中外文名，以及其上映年份
        data_name = []
        data_time = []
        result_data_main = result[0].select('h1')[0]
        data_name = result_data_main.select('span')[0].get_text()
        data_time = result_data_main.select('span')[1].get_text()

        # 获取该影片的导演、编剧、主要演员等详细信息
        data_detail = []
        result_data_information = result[0].select('div[id="info"]')
        data_detail = result_data_information[0].get_text()

        # 获取该影片的剧情简介
        data_synopsis = []
        result_synopsis = result[0].select('div[class="related-info"]')
        result_synopsis = result_synopsis[0].select('div[class="indent"]')
        data_synopsis = result_synopsis[0].get_text()
        l_index = data_synopsis.find("(展开全部)")
        r_index = data_synopsis.find("©豆瓣")
        if l_index == -1:
            data_synopsis = data_synopsis[:r_index]
        else:
            data_synopsis = data_synopsis[l_index+6:r_index]
        # if len(result_synopsis) == 4:
        #     data_synopsis = result_synopsis[3].get_text()
        # elif len(result_synopsis) == 3:
        #     data_synopsis = result_synopsis[2].get_text()
        # elif len(result_synopsis) <= 2:
        #     data_synopsis = result_synopsis[0].get_text()
        data_detail = data_detail.replace('\n', ':')
        temp_list = data_detail.split(':')
        data_director = []
        data_scriptwriter = []
        data_actor = []
        data_type = []
        data_country = []
        data_language = []
        data_release_data = []
        data_duration = []
        data_alias = []
        i = 0
        while i < len(temp_list) - 1:
            if temp_list[i] == '导演':
                data_director = temp_list[i+1]
            elif temp_list[i] == '编剧':
                data_scriptwriter = temp_list[i+1]
            elif temp_list[i] == '主演':
                data_actor = temp_list[i+1]
            elif temp_list[i] == '类型':
                data_type = temp_list[i+1]
            elif temp_list[i] == '制片国家/地区':
                data_country = temp_list[i+1]
            elif temp_list[i] == '语言':
                data_language = temp_list[i+1]
            elif temp_list[i] == '上映日期':
                data_release_data = temp_list[i+1]
            elif temp_list[i] == '片长':
                data_duration = temp_list[i+1]
            elif temp_list[i] == '又名':
                data_alias = temp_list[i+1]
            else:
                i = i - 1
            i = i + 2
        item_data = {"排名": data_rank, "电影名称": data_name, "年份": data_time, "导演": data_director,
                     "编剧": data_scriptwriter, "主演": data_actor, "类型": data_type, "制片国家": data_country,
                     "语言": data_language, "上映日期": data_release_data, "片长": data_duration,
                     "别名": data_alias, "剧情简介": data_synopsis}
        items_data1.append(item_data)
        return new_urls




