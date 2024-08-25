import numpy as np
import cv2
from scipy.signal import convolve2d
import os
import sys

# 樣式處裡
def matlab_style_gauss2D(shape=(3, 3), sigma=0.5):
    m, n = [(ss - 1.) / 2. for ss in shape]
    y, x = np.ogrid[-m:m + 1, -n:n + 1]
    h = np.exp(-(x * x + y * y) / (2. * sigma * sigma))
    h[h < np.finfo(h.dtype).eps * h.max()] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

# 過濾
def filter2(x, kernel, mode='same'):
    return convolve2d(x, np.rot90(kernel, 2), mode=mode)

# 計算亮度、對比度、結構和 SSIM
def compute_ssim(im1, im2, k1=0.01, k2=0.04, win_size=11, L=255):
    if not im1.shape == im2.shape:
        raise ValueError("Input images must have the same dimensions")
    if len(im1.shape) > 2:
        raise ValueError("Please input the images with 1 channel")

    C1 = (k1 * L) ** 2
    C2 = (k2 * L) ** 2
    window = matlab_style_gauss2D(shape=(win_size, win_size), sigma=0.5)
    window = window / np.sum(np.sum(window))

    if im1.dtype == np.uint8:
        im1 = np.double(im1)
    if im2.dtype == np.uint8:
        im2 = np.double(im2)

    mu1 = filter2(im1, window, 'valid')
    mu2 = filter2(im2, window, 'valid')
    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = filter2(im1 * im1, window, 'valid') - mu1_sq
    sigma2_sq = filter2(im2 * im2, window, 'valid') - mu2_sq
    sigma12 = filter2(im1 * im2, window, 'valid') - mu1_mu2

    # 确保方差為非負數
    sigma1_sq = np.maximum(sigma1_sq, 0)
    sigma2_sq = np.maximum(sigma2_sq, 0)

    # 計算亮度相似度 (luminance)
    luminance = (2 * mu1_mu2 + C1) / (mu1_sq + mu2_sq + C1)
    
    # 計算對比度相似度 (contrast)
    contrast = (2 * np.sqrt(sigma1_sq * sigma2_sq) + C2) / (sigma1_sq + sigma2_sq + C2)
    
    # 計算結構相似度 (structure)
    structure = (sigma12 + C2 / 2) / (np.sqrt(sigma1_sq) * np.sqrt(sigma2_sq) + C2 / 2)
    
    # 計算 SSIM 地圖
    ssim_map = luminance * contrast * structure

    # 計算平均 SSIM
    ssim = np.mean(np.mean(ssim_map))
    
    return np.mean(luminance), np.mean(contrast), np.mean(structure), ssim

# 指定圖片路徑
image_path1 = sys.argv[1]
image_path2 = sys.argv[2]
dir_path = sys.argv[3]

img1 = cv2.imread(image_path1)
img2 = cv2.imread(image_path2)

im1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
im2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

im1 = cv2.resize(im1, (520, 520))
im2 = cv2.resize(im2, (520, 520))

luminance, contrast, structure, ssim = compute_ssim(im1, im2)

result_cut = (
    f'{luminance * 100:.4f}%\n'
    f'{contrast * 100:.4f}%\n'
    f'{structure * 100:.4f}%\n'
)
print(result_cut)

result_ssim = f'{ssim * 100:.2f}%\n'
print(result_cut)

cutresult_path = os.path.join(dir_path, 'SSIMCUTresult.txt')
print(cutresult_path)
ssimresult_path = os.path.join(dir_path, 'SSIMresult.txt')
print(ssimresult_path)

with open(cutresult_path, 'w') as cut_file:
    cut_file.write(result_cut)

with open(ssimresult_path, 'w') as ssim_file:
    ssim_file.write(result_ssim)