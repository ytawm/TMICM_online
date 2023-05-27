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
        __RESIZE_SIZE = 224
        self.classes = ('benign', 'malignant')

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
        self.model = torch.load(model_path, map_location = 'cpu')
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


if __name__ == '__main__':


    img_path = r'./data/test/1.jpg'
    model_name = 'model.pth'


    P = Predict(model_path=model_name)

    if img_path.endswith('.jpg'):
        a = P.predict(img_path=img_path)

    print(a)