'''
 * @Description  : 预测
 * @Autor        : Tommy
 * @Date         : 2021-02-21 19:07:26
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-02-22 15:48:52
'''
from stagesepx.classifier.keras import KerasClassifier
from stagesepx.cutter import VideoCutter
from stagesepx.video import VideoObject
from stagesepx.reporter import Reporter

# 使用Keras方法进行预测
cl = KerasClassifier()
cl.load_model('./model.h5')

# 将视频切分成帧
file_name = './video/long.mp4'
video = VideoObject(file_name)

# 新建帧，计算视频总共多少帧，每帧多少ms
video.load_frames()

# 压缩视频
cutter = VideoCutter()

# 计算每一帧视频的每一个block的ssim和psnr
res = cutter.cut(video)

# 判断A帧到B帧之间是否稳定还是不稳定
stable, unstable = res.get_range()

# 把分类好的稳定阶段图片保存本地
res.pick_and_save(stable, 20, to_dir='./forecast_frame', meaningful_name=True)

# 把切分号的稳定区间，进行归类
classify_result = cl.classify(file_name, stable, keep_data=True)
result_dict = classify_result.to_dict()

# 打印结果
print(result_dict)
with open('./result.txt', 'w') as f:
    f.write(str(result_dict))

# 输出HTML报告
r = Reporter()
r.draw(classify_result, './result.html')
# TODO: 时间计算 = 3[0]-0[-1]
