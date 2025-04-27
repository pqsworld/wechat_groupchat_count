import os
import re
import pandas as pd
from collections import Counter

# 读取Markdown文件并按行处理
def generate_line_frequency_excel(markdown_file):
    # 读取文件的所有行
    with open(markdown_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 清理行内容
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # 跳过空行、日期行、引用标记行和Markdown格式行
        if not line or re.match(r'\d+年\d+月\d+日', line) or line.startswith('```') or re.match(r'#', line) or\
           line.startswith('开始时间:') or line.startswith('结束时间:') or line.startswith('导出时间:') or\
           line == '消息':
            continue
        # 去除引用格式
        if ' : ' in line and '引用' in line:
            continue
        # 保留实际消息内容
        cleaned_lines.append(line)

    # 统计频率
    line_counts = Counter(cleaned_lines)

    # 转换为DataFrame
    df = pd.DataFrame(line_counts.items(), columns=['消息内容', '出现次数'])

    # 按频次降序排序
    df = df.sort_values(by='出现次数', ascending=False)

    # 保存为Excel
    output_file = os.path.splitext(markdown_file)[0] + '_行频率统计.xlsx'
    df.to_excel(output_file, index=False)

    print(f'行频率统计已保存至: {output_file}')
    return output_file

if __name__ == '__main__':
    # 扫描exports目录下的所有md文件
    exports_dir = 'exports'
    for file in os.listdir(exports_dir):
        if file.endswith('.md'):
            markdown_file = os.path.join(exports_dir, file)
            print(f'正在处理: {markdown_file}')
            generate_line_frequency_excel(markdown_file)