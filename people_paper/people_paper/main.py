
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud,  ImageColorGenerator
import jieba.analyse

def rewrite(path, newpath):      #将获取到的数据重新编写
    newf = open(newpath,'w')

    with open(path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            tmp = eval(line)    #转化为字典格式
            newline = ''
            for key in tmp:
                if(type(tmp[key])==list):
                    if(tmp[key]):
                        t = (tmp[key])[0]
                elif(type(tmp[key])==str):
                    t = tmp[key]
                newline = newline + t + ' '
            newline += '\n'
            newf.write(newline)
    newf.close()


if __name__ == '__main__':

   # cmdline.execute('scrapy crawl PaperSpider'.split())    #执行爬虫，爬取新闻内容

    Path = 'PeoplePaperNewsInfo.txt'
    newPath = 'NewsInfo.txt'
    ImagePath = 'peoplepaper.jpg'     #背景图片
    stopwords_path = 'stopwords_ch.txt'
    set_font_path = 'simfang.ttf'
    saveImage = '1.png'     #词云展示图片

    rewrite(Path, newPath)

    text = open(newPath,'rb').read()     #开始用词云处理
    paper_mask = imread(ImagePath)  #设置背景图片

    tags = jieba.analyse.extract_tags (text,topK=300,withWeight=False)     #关键字提取
    content = " ".join(tags)


    #设置词云属性
    wc = WordCloud(font_path=set_font_path,
                background_color="white",
                max_words=2000,
                mask=paper_mask,
                max_font_size=800,
                random_state=42,
                width=1800, height=2000, margin=2,
                )

    wc.generate(content)
    image_colors = ImageColorGenerator(paper_mask)   #从背景图片中产生颜色

    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    wc.to_file(saveImage)