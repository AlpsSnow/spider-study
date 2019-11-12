import requests
import json
import time

maxPage = 0
commentCount = 0

def get_two_float(f_str, n):
    f_str = str(f_str)
    a, b, c = f_str.partition('.')
    c = (c+"0"*n)[:n]
    return ".".join([a, c])

def analyzecomments(comments_list):
    L = 0
    M = 0
    productSize = ""
    comment_content = []
    productColor = ""
    blackcolors = 0
    whitecolors = 0
    skincolors = 0
    
    for comments in comments_list:
        for comment in comments['comments']:
            comment_content.append(comment['content'])
            productColor = comment['productColor']
            if productColor == "经典-黑色":
                blackcolors += 1
            elif productColor == "经典-白色":
                whitecolors += 1
            else :
                skincolors += 1
            productSize = comment['productSize']
            if productSize == "L":
                L += 1
            else :
                M += 1
            print('L：{},M: {}, size:{}; blackcolors:{},whitecolors:{},skincolors:{},productColor:{}'.format(L,M, productSize, blackcolors,whitecolors,skincolors,productColor))
    print('总评论数：{} 件'.format(commentCount))
    print('L码{}件，占比：{} %'.format(L, get_two_float(L*100/commentCount, 2)))
    print('M码{}件，占比：{} %'.format(M, get_two_float(M*100/commentCount, 2)))
    print('黑色{}件，占比：{} %'.format(blackcolors, get_two_float(blackcolors*100/commentCount, 2)))
    print('白色{}件，占比：{} %'.format(whitecolors, get_two_float(whitecolors*100/commentCount, 2)))
    print('肤色{}件，占比：{} %'.format(skincolors, get_two_float(skincolors*100/commentCount, 2)))
    
    
def getcomments(page):
    url = 'https://sclub.jd.com/comment/productPageComments.action'
    payload = {
        'callback': 'fetchJSON_comment98vv891',
        'productId': 1578086,
        'score': 0,
        'sortType':	5,
        'page': page,
        'pageSize': 10,
        'isShadowSku': 0,
        'fold': 1
        }
    headers = {
        'Referer': 'https://item.jd.com/1578086.html?dist=jd',
        'User-Agent': 'Mozilla/5.0'
    }
    req = requests.get(url=url,params=payload,verify=False, headers=headers)
    if req.status_code == 200:
        comments_str = req.text[25:-2]
        #print(comments_str)
        comments_json = json.loads(comments_str)
        #print(comments_json)
        return comments_json
    else:
        print("请求失败！")
        return 0

if __name__ == "__main__":
    comments_list = []   
    comments_json = getcomments(0)
    comments_list.append(comments_json)
    maxPage = comments_json['maxPage']    
    commentCount = comments_json['productCommentSummary']['commentCount']
    
    for i in range(1,maxPage+1):
        time.sleep(5)
        comments_json = getcomments(i)
        while comments_json == 0:        
            time.sleep(5)
            comments_json = getcomments(i)
        comments_list.append(comments_json)
    analyzecomments(comments_list)

    

