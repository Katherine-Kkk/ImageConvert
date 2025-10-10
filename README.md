# python 改变图片亮度



使用numpy处理，对图像各个通道的每个像素点做线性变换，支持伽马校正。

# 安装依赖库

    pip install numpy
    pip install opencv-python

# 代码运行

    # python 脚本文件名.py 输入文件夹路径 输出文件夹路径 --effect 效果类型 --strength 效果强度



    输入文件夹路径：存放原始图像的文件夹（绝对路径或相对路径均可）
    输出文件夹路径：保存处理后图像的文件夹（不存在会自动创建）
    --effect：必须指定，可选 dark（暗光）或 overexpose（过曝）
    --strength：可选，默认 0.5，范围 0.1-1.0（值越大效果越明显）
    
# 暗光处理

    # 对于dark：0-0.2正常 0.3-0.5弱暗光(实例取0.3) 0.7-0.8强暗光(实例取0.6)
    python ConvertImage.py ./input ./output --effect dark --strength 0.3
    python ConvertImage.py ./GoPro/input ./GoPro_dark/weak03 --effect dark --strength 0.3
    
# 过曝光处理

    # 对于overexpose：0-0.2正常 0.3-0.4弱暗光(实例取0.3) 0.5-0.7强暗光(实例取0.6)
    python ConvertImage.py ./input ./output --effect overexpose --strength 0.3
    python ConvertImage.py ./GoPro/input ./GoPro_overexpose/weak03 --effect overexpose --strength 0.3
    
# 添加伽马校正

加入adjust_gamma(image, gamma=1.0)函数即可。
当 gamma < 1 时：图像变亮（增强暗部细节）
当 gamma > 1 时：图像变暗（增强亮部细节）
当 gamma = 1 时：图像保持不变（无校正）

    
