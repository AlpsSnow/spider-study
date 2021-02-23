import requests
import json
import time

maxPage = 0         #非默认评论总页数
commentCount = 0    #总评论数（包含默认评论数）

L = 0   #L码销量
M = 0   #M码销量
productSize = ""
comment_content = []    #所有评论内容
productColor = ""
blackcolors = 0         #黑色销量
whitecolors = 0         #白色销量
skincolors = 0          #肤色销量
comment_count = 0       #非默认评论总评论数

L_size = "75~85" #L码的尺寸
M_size = "65~75" #M码的尺寸

# 小数点后取两位
def get_two_float(f_str, n):
    f_str = str(f_str)
    a, b, c = f_str.partition('.')
    c = (c+"0"*n)[:n]
    return ".".join([a, c])

# 解析每一页的评论
def analyzecomments(comments_json):
    global L,M,productSize,comment_content,productColor,blackcolors,whitecolors,skincolors,comment_count    
    for comment in comments_json['comments']:
        comment_count += 1
        comment_content.append(comment['content'])
        productColor = comment['productColor']
        if productColor.find('黑') != -1:
            blackcolors += 1
        elif productColor.find('白') != -1:
            whitecolors += 1
        elif productColor.find('肤') != -1:
            skincolors += 1
        else:
            pass
        productSize = comment['productSize']
        if productSize.find('L') != -1:
            L += 1
        elif productSize.find('M') != -1:
            M += 1
        else:
            pass            
        print('每一条评论的具体信息：L：{},M: {}, size:{}; blackcolors:{},whitecolors:{},skincolors:{},productColor:{}'.format(L,M, productSize, blackcolors,whitecolors,skincolors,productColor))
    print('总评论数：{}'.format(comment_count))

# 打印结果   
def  print_result():
    global L_size,M_size,commentCount,L,M,blackcolors,whitecolors,skincolors,comment_count
    print('包含默认评论的总评论数：{} 件'.format(commentCount))
    print('非默认评论的总评论数：{} 件'.format(comment_count))
    print('L码{}件，胸围：{}，占比：{} %'.format(L, L_size, get_two_float(L*100/comment_count, 2)))
    print('M码{}件，胸围：{}，占比：{} %'.format(M, M_size,get_two_float(M*100/comment_count, 2)))
    print('黑色{}件，占比：{} %'.format(blackcolors, get_two_float(blackcolors*100/comment_count, 2)))
    print('白色{}件，占比：{} %'.format(whitecolors, get_two_float(whitecolors*100/comment_count, 2)))
    print('肤色{}件，占比：{} %'.format(skincolors, get_two_float(skincolors*100/comment_count, 2)))

# 获取每一页评论 
def getcomments(page):
    url = 'https://sclub.jd.com/comment/productPageComments.action'

    # 请求参数
    payload = {
        'callback': 'fetchJSON_comment98vv891',
        'productId': 1578086,                       # 商品ID
        'score': 0,
        'sortType':	5,
        'page': page,                               # 想要获取第几页的评论
        'pageSize': 10,                             # 每一页评论数
        'isShadowSku': 0,
        'fold': 1
        }

    # 请求头部，应对反爬虫
    headers = {
        'Referer': 'https://item.jd.com/1578086.html?dist=jd',  #告诉服务器该网页是从哪个页面链接过来的
        'User-Agent': 'Mozilla/5.0'     #告诉服务器该请求的用户代理软件的应用类型、操作系统、软件开发商以及版本号
    }

    # 发起请求
    req = requests.get(url=url,params=payload,verify=False, headers=headers)
    if req.status_code == 200:
        print('请求成功 status_code =200！')
        comments_str = req.text[25:-2]              #解析返回字符串，截取json字符串
        comments_json = json.loads(comments_str)    #json字符串转dict型
        return comments_json
    else:
        print('请求失败！')
        return 0

if __name__ == "__main__":
    # 获取第一页评论   
    comments_json = getcomments(0)
    # 评论的最大页数    
    maxPage = comments_json['maxPage']
    print('评论的最大页数:{}'.format(maxPage))
    # 总的评论数
    commentCount = comments_json['productCommentSummary']['commentCount']
    print('总的评论数:{}'.format(commentCount))

    # 获取第二页~最后一页的请求
    for i in range(1,maxPage+1):
        time.sleep(5)
        comments_json = getcomments(i)
        while comments_json == 0:        
            time.sleep(5)
            comments_json = getcomments(i)
        analyzecomments(comments_json)
    print_result() 

    

