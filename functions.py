"""
5折交叉验证法
一次模型训练中,训练集与测试集严格对立,不能有数据重复.
其中一份做测试集，另外四份为训练集。
重复5次（每份都当一次测试集）
"""


def five_fold_cross_validation(dir_path: str) -> dict:
    import os
    import numpy as np
    fileseq = np.arange(1, len(os.listdir(dir_path)) + 1)
    np.random.shuffle(fileseq)
    filegroup = np.array_split(fileseq, 5)
    filegroup = {f'part{i}': filegroup[i] for i in range(5)}
    return filegroup


# Test
# filegroup = five_fold_cross_validation(dir_path='data/all_data')

"""
清空文件夹
"""


def clear_folder(folder_path: str) -> None:
    import os
    import shutil
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                # 如果是文件则删除
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                # 如果是文件夹则使用shutil.rmtree递归删除
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'删除{file_path}时出错: {e}')


# Test
# clear_folder(folder_path='data/all_data')

"""
选用最佳设备
"""


def detect_best_device() -> str:
    import torch
    if torch.cuda.is_available():
        return 'cuda'
    # elif torch.backends.mps.is_available():
    #     return 'mps'
    else:
        return 'cpu'

# Test
# detect_best_device()


"""
提取指定文件夹的图片，然后从 start 开始编号，保存到指定文件夹
"""


def extract_images(dir_path: str, start: int, save_path: str) -> int:
    import os
    import shutil
    # 保留图片顺序
    files_name = []
    for file_name in os.listdir(dir_path):
        if file_name.endswith('.jpg'):
            files_name.append(file_name)
    files_name.sort(key=lambda x: int(x.split('_')[0]))

    for file_name in files_name:
        if file_name.endswith('.jpg'):
            shutil.copy(f'{dir_path}/{file_name}', f'{save_path}/{start}.jpg')
            start += 1

    # 返回最后一个编号
    return start-1

# Test
# extract_images(dir_path='data/all_data', start=1, save_path='data/all_data')
