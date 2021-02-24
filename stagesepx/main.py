'''
 * @Description  : 视频切割和判断稳定区间
 * @Autor        : Tommy
 * @Date         : 2021-02-21 17:17:07
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-02-22 15:25:08
'''
from stagesepx.cutter import VideoCutter
from stagesepx.video import VideoObject


# 将视频切分成帧
file_name = './video/long.mp4'
video = VideoObject(file_name, pre_load=True)

# 新建帧，计算视频总共有多少帧，每帧多少ms
video.load_frames()

# 压缩视频
cutter = VideoCutter()

# 计算每一帧视频的每一个block的ssim和psnr
res = cutter.cut(video, block=8)

# 计算出判断A帧到B帧之间是稳定还是不稳定
stable, unstable = res.get_range(threshold=0.97, offset=3)

# 把分类号的稳定阶段图片保存本地
res.pick_and_save(stable, 20, to_dir='./stable_frame', meaningful_name=True)
