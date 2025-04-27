import os
import re
import jieba
import pandas as pd
from collections import Counter

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
def generate_word_count_excel(markdown_file):
    # 读取文件
    content = read_markdown_file(markdown_file)

    # 预处理文本
    processed_text = preprocess_text(content)

    # 使用jieba分词
    words = [word for word in jieba.cut(processed_text) if len(word.strip()) > 1 and not word.isdigit()]

    # 统计词频
    word_counts = Counter(words)

    # 转换为DataFrame
    df = pd.DataFrame(word_counts.items(), columns=['词语', '频次'])

    # 按频次降序排序
    df = df.sort_values(by='频次', ascending=False)

    # 保存为Excel
    output_file = os.path.splitext(markdown_file)[0] + '_词频统计.xlsx'
    df.to_excel(output_file, index=False)

    print(f'词频统计已保存至: {output_file}')
    return output_file

if __name__ == '__main__':
    # 扫描exports目录下的所有md文件
    exports_dir = 'exports'
    for file in os.listdir(exports_dir):
        if file.endswith('.md'):
            markdown_file = os.path.join(exports_dir, file)
            print(f'正在处理: {markdown_file}')
            generate_word_count_excel(markdown_file)