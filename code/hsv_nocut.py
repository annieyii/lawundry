import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import sys
import os

def load_and_convert_to_hsv(image_path):
    # Load the image
    image = cv2.imread(image_path)
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv_image

def compute_histogram(image, bins=50):
    # Compute histograms for each channel (Hue, Saturation, Value)
    hist_h = cv2.calcHist([image], [0], None, [bins], [0, 256])
    hist_s = cv2.calcHist([image], [1], None, [bins], [0, 256])
    hist_v = cv2.calcHist([image], [2], None, [bins], [0, 256])
    # Normalize the histograms
    hist_h = cv2.normalize(hist_h, hist_h).flatten()
    hist_s = cv2.normalize(hist_s, hist_s).flatten()
    hist_v = cv2.normalize(hist_v, hist_v).flatten()
    return hist_h, hist_s, hist_v

def cosine_similarity_between_histograms(hist1, hist2):
    # Compute cosine similarity between two histograms
    return cosine_similarity(hist1.reshape(1, -1), hist2.reshape(1, -1))[0][0]

def compare_images(image_path1, image_path2):
    # Load and convert images to HSV
    hsv_image1 = load_and_convert_to_hsv(image_path1)
    hsv_image2 = load_and_convert_to_hsv(image_path2)
    
    # Compute histograms for each image
    hist_h1, hist_s1, hist_v1 = compute_histogram(hsv_image1)
    hist_h2, hist_s2, hist_v2 = compute_histogram(hsv_image2)
    
    # Compute cosine similarities for each channel
    sim_h = cosine_similarity_between_histograms(hist_h1, hist_h2)
    sim_s = cosine_similarity_between_histograms(hist_s1, hist_s2)
    sim_v = cosine_similarity_between_histograms(hist_v1, hist_v2)

    print(f'{sim_h:.2f}%')
    print(f'{sim_s:.2f}%')
    print(f'{sim_v:.2f}%')
    
    # Average the cosine similarities for the final similarity score
    final_similarity = (sim_h + sim_s + sim_v) / 3.0
    
    # Convert similarity score to percentage
    similarity_percentage = final_similarity * 100
    return similarity_percentage

def main(image_path1, image_path2,dir_path):
    # Compare the images and print the similarity score
    similarity_score = compare_images(image_path1, image_path2)
    result_cut = (
        f'{luminance * 100:.4f}%\n'
        f'{contrast * 100:.4f}%\n'
        f'{structure * 100:.4f}%\n'
    )

    result_hsv = f'{average_similarity * 100:.2f}%\n'

    cutresult_path = os.path.join(dir_path, 'HSVCUTresult.txt')
    print(cutresult_path)
    hsvresult_path = os.path.join(dir_path, 'HSVresult.txt')
    print(hsvresult_path)

    with open(cutresult_path, 'w') as cut_file:
        cut_file.write(result_cut)

    with open(hsvresult_path, 'w') as hsv_file:
        hsv_file.write(result_hsv)


if __name__ == "__main__":

    # Get the directory of the Python file
    image_path1 = sys.argv[1]
    image_path2 = sys.argv[2]
    dir_path = sys.argv[3]
    
    main(image_path1, image_path2,dir_path)