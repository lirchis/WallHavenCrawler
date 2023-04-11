'''
爬取http://Wallhaven.cc壁纸网站中Toplist前50页壁纸
'''
# 导入所需库
import requests
from lxml import etree
import os
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}
# 定义获取每页html信息的函数
def get_html_info(page):
    url = f'https://wallhaven.cc/toplist?page={page}'
    resp = requests.get(url,headers=headers)
    resp_html = etree.HTML(resp.text)
    return resp_html
def get_pic(resp_html):
    pic_url_list = []
    lis = resp_html.xpath('//*[@id="thumbs"]/section[1]/ul/li') # 获取该页所有缩略图包含的信息
    for li in lis:
        pic_url = li.xpath('./figure/a/@href')[0] # 获取存放在缩略图信息中的缩略图原图网址
        pic_url_list.append(pic_url)
    for pic_url in pic_url_list:
        resp2 = requests.get(pic_url,headers=headers)
        r_html2 = etree.HTML(resp2.text)
        pic_size = r_html2.xpath('//*[@id="showcase-sidebar"]/div/div[1]/h3/text()')[0] #用照片分辨率作为名称一部分
        final_url = r_html2.xpath('//*[@id="wallpaper"]/@src')[0] # 获取原图下载地址
        pic = requests.get(url=final_url,headers=headers).content
        if not os.path.exists('Wallhaven'):
            os.mkdir('Wallhaven')
        with open('Wallhaven\\' + pic_size +final_url[-10:],mode='wb') as f:
            f.write(pic) # 保存图片
            print(pic_size + final_url[-10:]+'，下载完毕，已下载{}张壁纸'.format(len(os.listdir('Wallhaven'))))
def main():
    page_range = range(1,51) # 爬取1-50页的壁纸
    for i in page_range:
        r = get_html_info(i)
        get_pic(r)
        print(f'===============第{i}页下载完毕=============')
if __name__ == '__main__':
    main()