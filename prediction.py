import os

import albumentations
import cv2
import torch.utils.data.distributed
from albumentations.pytorch import ToTensorV2
from torch.autograd import Variable

from functions import detect_best_device

"""
实例化Predict类，然后调用predict方法，传入图片路径，返回预测结果
"""


class Predict:
    def __init__(self, model_path: str):
        self.classes = ('benign', 'malignant')

        __RESIZE_SIZE = 224
        self.transform = albumentations.Compose([
            albumentations.Resize(__RESIZE_SIZE, __RESIZE_SIZE),
            # albumentations.OneOf([
            #     albumentations.RandomGamma(gamma_limit=(60, 120), p=0.9),
            #     albumentations.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.9),
            #     albumentations.CLAHE(clip_limit=4.0, tile_grid_size=(4, 4), p=0.9),
            # ]),
            albumentations.CLAHE(clip_limit=4.0, tile_grid_size=(4, 4), p=0.9),
            # albumentations.HorizontalFlip(p=0.5),
            # albumentations.ShiftScaleRotate(shift_limit=0.2, scale_limit=0.2, rotate_limit=20,
            #                                 interpolation=cv2.INTER_LINEAR, border_mode=cv2.BORDER_CONSTANT, p=1),
            albumentations.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0,
                                     p=1.0),
            ToTensorV2()
        ])

        self.DEVICE = torch.device(detect_best_device())
        self.model = torch.load(model_path)
        self.model.eval()
        self.model.to(self.DEVICE)

    def predict(self, img_path: str) -> str:
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = self.transform(image=img)["image"]
        img.unsqueeze_(0)
        img = Variable(img).to(self.DEVICE)
        out = self.model(img)
        # Predict
        _, pred = torch.max(out.data, 1)
        return self.classes[pred.data.item()]


class Voting:
    def __init__(self, model1: str, model2: str, model3: str):
        self.M1 = Predict(model1)
        self.M2 = Predict(model2)
        self.M3 = Predict(model3)

    def predict(self, img_path: str) -> str:
        result = [self.M1.predict(img_path), self.M2.predict(img_path), self.M3.predict(img_path)]
        return max(set(result), key=result.count)


if __name__ == '__main__':
    # fileFolder 是测试的源文件夹
    fileFolder = 'data/final_test/'
    testList = os.listdir(fileFolder)
    result = {}
    V = Voting(model1='model2.pth', model2='model4.pth', model3='model5.pth')
    for file in testList:
        if file.endswith('.jpg'):
            result[file] = V.predict(img_path=fileFolder + file)
    result = sorted(result.items(), key=lambda x: int(x[0].strip('.jpg')))

    # 将结果保存在 results.txt 中
    # ID 为文件名，Category 为预测结果
    # 0 表示良性，1 表示恶性
    with open('results.txt', 'w') as f:
        f.write('ID,Category\n')
        for i in result:
            f.write(f'{i[0][:-4]},{0 if i[1] == "benign" else 1}\n')

    print("预测完毕，结果保存在 result.txt 中")
