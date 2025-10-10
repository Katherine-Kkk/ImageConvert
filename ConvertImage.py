import cv2
import numpy as np
import os
import argparse
from glob import glob

def adjust_exposure(image, factor):
    # 当 factor > 1 时增强曝光；当 0 < factor < 1 时减弱曝光
    # 当 factor = 1 时：图像保持不变
    """调整图像曝光度"""
    # 将图像的像素值（通常是 0-255 的 uint8 类型）转换为 0.0-1.0 范围的 float32 类型
    img_float = image.astype(np.float32) / 255.0

    if factor > 0:
        adjusted = np.power(img_float, 1.0 / factor)
    else: # factor输入错误，直接返回原图
        adjusted = img_float
    
    return np.clip(adjusted * 255, 0, 255).astype(np.uint8)
    # adjusted * 255：将归一化的像素值还原为 0-255 范围
    # np.clip(..., 0, 255)：确保像素值不会超出 0-255 范围（避免过曝导致的像素值溢出）
    # 转换回 uint8 类型：符合图像存储的常规格式


def adjust_gamma(image, gamma=1.0):
    """伽马校正"""
    # 当 gamma < 1 时：图像变亮（增强暗部细节）
    # 当 gamma > 1 时：图像变暗（增强亮部细节）
    # 当 gamma = 1 时：图像保持不变（无校正）

    # 建议不要添加校正，校正后基本上和原图差别不大
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def create_dark_effect(image, strength=0.5):
    """创建暗光效果"""
    strength = max(0.1, min(1.0, strength))
    dark = adjust_exposure(image, 1.0 - strength * 0.8)
    dark = cv2.addWeighted(dark, 1.0 - strength * 0.5, np.zeros_like(dark), 0, 0)
    # dark = adjust_gamma(dark, 1.0 + strength * 2.0)
    return dark

def create_overexposure_effect(image, strength=0.5):
    """创建过曝效果"""
    strength = max(0.1, min(1.0, strength))
    overexposed = adjust_exposure(image, 1.0 + strength * 1.2)
    overexposed = cv2.addWeighted(overexposed, 1.0 + strength * 0.5, np.zeros_like(overexposed), 0, 0)
    # overexposed = adjust_gamma(overexposed, 1.0 - strength * 0.8)
    return overexposed

def process_images(input_dir, output_dir, effect, strength):
    """批量处理文件夹中的图像"""
    # 确保输出文件夹存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 支持的图像格式
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
    image_paths = []
    
    # 收集所有图像路径
    for ext in image_extensions:
        image_paths.extend(glob(os.path.join(input_dir, ext), recursive=False))
    
    if not image_paths:
        print(f"警告：在 {input_dir} 中未找到任何图像文件")
        return
    
    # 处理每张图像
    total = len(image_paths)
    for i, path in enumerate(image_paths):
        # 读取图像
        image = cv2.imread(path)
        if image is None:
            print(f"警告：无法读取图像 {path}，已跳过")
            continue
        
        # 处理图像
        if effect == 'dark':
            processed = create_dark_effect(image, strength)
        else:
            processed = create_overexposure_effect(image, strength)
        
        # 获取文件名并保存
        filename = os.path.basename(path)
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, processed)
        
        # 显示进度
        if (i + 1) % 10 == 0 or (i + 1) == total:
            print(f"已处理 {i + 1}/{total} 张图像")
    
    print(f"处理完成！所有图像已保存到 {output_dir}")

def main():
    parser = argparse.ArgumentParser(description='批量调整图像曝光度')
    parser.add_argument('input_dir', help='输入图像所在文件夹路径')
    parser.add_argument('output_dir', help='输出处理后图像的文件夹路径')
    parser.add_argument('--effect', choices=['dark', 'overexpose'], required=True,
                      help='效果类型：dark（暗光）或 overexpose（过曝）')
    parser.add_argument('--strength', type=float, default=0.5,
                      help='效果强度（0.1-1.0之间），默认0.5')
    args = parser.parse_args()
    
    # 检查输入文件夹是否存在
    if not os.path.isdir(args.input_dir):
        print(f"错误：输入文件夹 {args.input_dir} 不存在")
        return
    
    process_images(args.input_dir, args.output_dir, args.effect, args.strength)

if __name__ == "__main__":
    main()
    