import os
import re
import jieba
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image

# 设置中文字体路径 (Windows系统可能需要调整路径)
font_path = 'C:/Windows/Fonts/simhei.ttf'  # 黑体

# 读取Markdown文件
def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# 预处理文本
def preprocess_text(text):
    # 去除时间戳、日期和其他非必要内容
    text = re.sub(r'\d+年\d+月\d+日 \d+:\d+', '', text)
    text = re.sub(r'\[图片\]|\[动画表情\]', '', text)
    text = re.sub(r'引用.*的消息 : ', '', text)
    return text

# 主函数
def generate_wordcloud(markdown_file):
    # 读取文件
    content = read_markdown_file(markdown_file)

    # 预处理文本
    processed_text = preprocess_text(content)

    # 使用jieba分词
    words = jieba.cut(processed_text)
    text = ' '.join(words)

    # 设置停用词
    stopwords = set(STOPWORDS)
    stopwords.update(['的', '了', '和', '是', '在', '我', '你', '他', '她', '们', '这', '那', '有', '就', '不', '也', '都', '说', '呢', '吧', '吗', '啊', '嗯', '哦', '好', '哈哈', '引用', '消息'])

    # 创建词云
    wordcloud = WordCloud(
        font_path=font_path,
        background_color='white',
        max_words=100,
        max_font_size=100,
        width=800,
        height=400,
        stopwords=stopwords,
        contour_width=1,
        contour_color='steelblue'
    ).generate(text)

    # 保存图片
    output_file = os.path.splitext(markdown_file)[0] + '_wordcloud.png'
    wordcloud.to_file(output_file)
    print(f'词云已保存至: {output_file}')

    # 显示词云图
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.show()

if __name__ == '__main__':
    # 扫描exports目录下的所有md文件
    exports_dir = 'exports'
    for file in os.listdir(exports_dir):
        if file.endswith('.md'):
            markdown_file = os.path.join(exports_dir, file)
            print(f'正在处理: {markdown_file}')
            generate_wordcloud(markdown_file)