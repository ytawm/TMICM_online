"""
注意：代码运行前，data文件夹应已有train、test文件夹。train、test文件夹中应有benign和malignant两个空的子文件夹。

运行下面代码，代码会根据列表序号将图片划分进相应的文件夹中。
运行Train_ResNet18.py进行训练，记录acc

第2次选part4为测试集，其余part为训练集，开始训练。

以此类推共重复上述步骤5次，取5次acc平均值为模型最终acc。调参重复进行5折训练
"""


from functions import five_fold_cross_validation, clear_folder
import numpy as np
import os
import shutil

# 第一次选part1为测试集，其余part为训练集。
all_data = five_fold_cross_validation(dir_path='data/go/all_data')
test = all_data["part4"]
train = np.concatenate((all_data["part0"], all_data["part1"], all_data["part2"], all_data["part3"]))

print(len(test))
print(len(train))

# 清空train/malignant、train/benign、test/malignant、test/benign文件夹
clear_folder('data/go/train/malignant')
clear_folder('data/go/train/benign')
clear_folder('data/go/test/malignant')
clear_folder('data/go/test/benign')
print("文件夹已清空，正在分配新数据集")

# 前 B 项目图片为良性，B+1 项目图片为恶性
B = 13

# 根据列表序号将图片分配进相应的文件夹中
for file_name in os.listdir('data/go/all_data'):
    # 如果文件名以jpg结尾
    if file_name.endswith('.jpg'):
        # 取出文件名（不包含后缀）
        file_name_without_ext = int(os.path.splitext(file_name)[0])
        # 如果文件名在test中且编号小于等于B，将其拷贝到test/benign文件夹中.如果文件名在test中且编号大于等于B，将其拷贝到test/malignant文件夹中
        if file_name_without_ext in test and file_name_without_ext <= B:
            shutil.copy(f'data/go/all_data/{file_name}',
                        f'data/go/test/benign/{file_name}')
        elif file_name_without_ext in test and file_name_without_ext >= B+1:
            shutil.copy(f'data/go/all_data/{file_name}',
                        f'data/go/test/malignant/{file_name}')
        # 如果文件名在train中且编号小于等于B，将其拷贝到train/benign文件夹中.如果文件名在train中且编号大于等于B，将其拷贝到train/malignant文件夹中
        elif file_name_without_ext in train and file_name_without_ext <= B:
            shutil.copy(f'data/go/all_data/{file_name}',
                        f'data/go/train/benign/{file_name}')
        elif file_name_without_ext in train and file_name_without_ext >= B+1:
            shutil.copy(f'data/go/all_data/{file_name}',
                        f'data/go/train/malignant/{file_name}')
