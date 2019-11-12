##  Python爬虫爬取京东双十一评价最多文胸的罩杯销量统计

### 调查京东获取商品评论Web API
> 1. 打开销量第一文胸的网页，按`F12`打开开发者界面，打开`网络`选项卡，在过滤框输入`comment`，`F5`刷新页面。如下图，可以定位到京东商品评论的请求的通信项目

![京东商品评论的请求的通信项目](comment_通信.png)

> 2. 打开`消息头`选项卡，可以看到该通信使用的Web API和请求头

![请求](request.png)

> 3. 分析请求信息。
请求URL=https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv891&productId=1578086&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1

根据程序员的命名经验，我们可以知道。
page=0表示请求第一页的评论。
pageSize=10表示每一页的评论数是10个。

另外，请求头里面的`Referer`和`User-Agent`也很关键，一些网站有反爬虫机制，我们在使用python爬虫模拟请求的时候，最好也在请求头中加入这些参数。

> 4.分析响应数据

![响应](response.png)

comments：看这个名字就知道是产品的评论信息

> 5.使用python 的`requests`库，模拟浏览器的请求抓取评论信息。

> 6.根据总评论页数循环发送请求，取得所有评论。

![统计结果](result.png)

> 7.数据整理（jieba）

> 8.词云（jieba）
生成云词我们需要用到numpy、matplotlib、wordcloud、Pillow这几个库，大家先自行下载。matplotlib库用于图像处理，wordcloud库用于生成词云。

### 总结
文章篇幅较长，详细的介绍了从需求到技术分析、爬取数据、清洗数据、最后的分析数据。来总结一下吧：

> 1. 如何分析并找出加载数据的url
> 2. 如何使用requests库的headers解决Referer和User-Agent反扒技术
> 3. 如何找出分页参数实现批量爬取
> 4. 数据的提取与保存到文件
> 5. 使用jieba库对数据分词清洗
> 6. 使用wordcloud生成指定形状的词云