import os
import re

def format_filename_to_snake_case(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            # 替换文件名中的空格为下划线
            new_filename = re.sub(r'\s+', '_', filename)
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)
            # 重命名文件
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{filename}' to '{new_filename}'")

# 示例使用，假设目录是'./your_directory'
directory_path = './resized_snapshot_img'
format_filename_to_snake_case(directory_path)