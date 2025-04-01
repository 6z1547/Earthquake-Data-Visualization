# import pandas as pd
# import chardet
#
# def detect_and_read_csv(file_path):
#     with open(file_path, 'rb') as f:
#         result = chardet.detect(f.read())
#         print(result)
#     encoding = result['encoding']
#     df = pd.read_csv(file_path, encoding=encoding)
#     return df
#
# file_path = 'query.csv'
# data = detect_and_read_csv(file_path)
# print(data.head())
import pandas as pd

def convert_csv_to_utf8(input_file_path, output_file_path):
    # 读取CSV文件
    df = pd.read_csv(input_file_path, encoding='GB2312')
    print(df)
    # 将数据写入新的UTF - 8编码的CSV文件
    df.to_csv(output_file_path, encoding='utf - 8', index=False)

# 示例调用
input_file = 'query.csv'
output_file = 'query_utf8.csv'
convert_csv_to_utf8(input_file, output_file)
