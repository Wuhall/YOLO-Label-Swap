import os
import uuid

# 设置images和labels文件夹的路径
images_path = '/Volumes/Disk0/pre-dataset16/val/images' 
labels_path = '/Volumes/Disk0/pre-dataset16/val/labels'  

# 指定要替换的标号映射，键为原标号，值为新标号
label_mapping = {
    '0': '18',
    '1': '19'
}

# 获取所有图像和标签文件的列表
image_files = [f for f in os.listdir(images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
label_files = {os.path.splitext(f)[0] for f in os.listdir(labels_path) if f.endswith('.txt')}

# 找出没有对应标签的图像文件并删除
for image_file in image_files:
    image_name = os.path.splitext(image_file)[0]
    if image_name not in label_files:
        os.remove(os.path.join(images_path, image_file))
        print(f"Deleted image without label: {image_file}")

# 获取更新后的图像和标签文件列表
image_files = [f for f in os.listdir(images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
label_files = [f for f in os.listdir(labels_path) if f.endswith('.txt')]

# 为每个图像和标签生成新的UUID并重命名
for image_file in image_files:
    # 生成新的UUID并去掉`-`
    new_name = str(uuid.uuid4()).replace('-', '')
    
    # 获取旧文件路径
    old_image_path = os.path.join(images_path, image_file)
    old_label_path = os.path.join(labels_path, os.path.splitext(image_file)[0] + '.txt')

    # 构建新文件路径
    new_image_path = os.path.join(images_path, new_name + os.path.splitext(image_file)[1])
    new_label_path = os.path.join(labels_path, new_name + '.txt')

    # 重命名图像文件
    os.rename(old_image_path, new_image_path)

    # 读取并修改标签文件内容
    with open(old_label_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if parts and parts[0] in label_mapping:
            parts[0] = label_mapping[parts[0]]  # 使用字典替换标号
        new_lines.append(' '.join(parts) + '\n')

    # 写回修改后的标签文件
    with open(new_label_path, 'w') as file:
        file.writelines(new_lines)

    # 删除旧标签文件
    os.remove(old_label_path)

    print(f"Renamed {image_file} to {new_name} and updated labels")

print("All tasks completed.")