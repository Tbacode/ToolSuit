'''
 * @Description  : 开始根据图像数据训练模型及预测
 * @Autor        : Tommy
 * @Date         : 2021-02-21 18:51:11
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-02-21 22:39:33
'''
from stagesepx.classifier.keras import KerasClassifier

# 训练模型文件
cl = KerasClassifier(
    # 设置这个数，需要保证小于总样本数，否则报错。
    nb_train_samples=80,
    # 训练轮数
    epochs=30)

cl.train('./stable_frame')
cl.save_model('./model.h5', overwrite=True)
