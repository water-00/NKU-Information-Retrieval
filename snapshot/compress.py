from PIL import Image
import os

def resize_png_images(source_dir, output_dir, scale=0.5):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.png'):
                file_path = os.path.join(root, file)
                img = Image.open(file_path)

                # 计算新的尺寸
                new_size = tuple([int(dim * scale) for dim in img.size])
                img.thumbnail(new_size, Image.ANTIALIAS)

                # 保存缩放后的图片
                output_path = os.path.join(output_dir, file)
                img.save(output_path)

# 要缩放的文件夹路径
source_dir = './snapshot_img'
# 缩放后的图片保存路径
output_dir = './resized_snapshot_img'

# 执行缩放
resize_png_images(source_dir, output_dir)
