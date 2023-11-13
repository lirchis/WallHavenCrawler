"""
爬取http://Wallhaven.cc壁纸网站中Toplist前50页壁纸
"""
# 导入所需库
import requests
from lxml import etree
import os

# 每个网站都会又鉴权，这个鉴权一般都是放在https请求头的，很多时候都是Cookies。
# 怎么获取这个鉴权呢？在网页上按F12查看当前页面来往的网络包（F12打开查看栏后刷新页面，就会发现网络那里又很多网络包），你点开其中一个，看他的http头
# 看http头有没有参数像是用来鉴权的，复制过来这里就好了。到时候python脚本发生http包的时候，请求头里会有你的鉴权，这样网站服务器才知道是你，是登录了的
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}


# 定义获取每页html信息的函数
# 这里就是去获取html，至于url填什么，就也是通过F12去看网络包，看返回是html的那个包的请求路径是什么。
# 几乎一切互联网应用的都是客户端发生http请求到服务端，服务端返回信息，也就是说和网站交互都是http包实现的
# 爬虫就是自动发生http请求，把返回的结果拿到，用一定的代码去处理这些返回值就可以了
def get_html_info(page):
    url = f'https://wallhaven.cc/toplist?page={page}'
    resp = requests.get(url, headers=headers)
    resp_html = etree.HTML(resp.text)
    return resp_html


# 这里就是通过返回的html获取图片地址。爬虫爬回html后，就直接去处理html就拿到自己想要的了，那么怎么样才知道自己要的信息在html的哪个位置呢？
# 也是在网页上用F12去看，看元素那一栏，里面有当前页面的html代码，一点点点开来找到就好了，这样就知道自己要的信息在html哪个位置
# 然后在这下面把要的信息取出来，直接处理就好了，例如存储起来。这里就是拿到图片地址，然后那这图片地址去下载图片。
# python提供了非常完整的http工具，和解析html的工具，在网上去找都能找到用法
def get_pic(resp_html):
    pic_url_list = []
    lis = resp_html.xpath('//*[@id="thumbs"]/section[1]/ul/li')  # 获取该页所有缩略图包含的信息
    for li in lis:
        pic_url = li.xpath('./figure/a/@href')[0]  # 获取存放在缩略图信息中的缩略图原图网址
        pic_url_list.append(pic_url)
    for pic_url in pic_url_list:
        resp2 = requests.get(pic_url, headers=headers)
        r_html2 = etree.HTML(resp2.text)
        pic_size = r_html2.xpath('//*[@id="showcase-sidebar"]/div/div[1]/h3/text()')[0]  # 用照片分辨率作为名称一部分
        final_url = r_html2.xpath('//*[@id="wallpaper"]/@src')[0]  # 获取原图下载地址
        pic = requests.get(url=final_url, headers=headers).content
        if not os.path.exists('Wallhaven'):
            os.mkdir('Wallhaven')
        with open('Wallhaven\\' + pic_size + final_url[-10:], mode='wb') as f:
            f.write(pic)  # 保存图片
            print(pic_size + final_url[-10:] + '，下载完毕，已下载{}张壁纸'.format(len(os.listdir('Wallhaven'))))


def main():
    page_range = range(1, 51)  # 爬取1-50页的壁纸
    for i in page_range:
        r = get_html_info(i)
        get_pic(r)
        print(f'===============第{i}页下载完毕=============')


if __name__ == '__main__':
    main()
