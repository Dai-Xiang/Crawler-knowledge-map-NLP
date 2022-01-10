# load函数用来将新的url存储进列表，以队列形式进行存放，以实现广度优先
def load(new_url, url1):
    for temp in new_url:
        if temp in url1:
            continue
        else:
            url1.append(temp)
    return


# remove函数用来将url弹出并删除，每次只弹出一个
def remove(url1, n):
    return url1[n-1]
