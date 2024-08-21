import cv2
import numpy as np
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from PIL import Image, ImageTk

def calculate_cnn_similarity(image1_path, image2_path):
    # Load VGG16 model pretrained on ImageNet
    base_model = VGG16(weights='imagenet')
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
    
    # Read and preprocess images
    def preprocess_image(image_path):
        image = cv2.imread(image_path)
        image = cv2.resize(image, (224, 224))
        image = image.astype('float32')
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)  # Preprocess using VGG16's preprocess_input
        return image
    
    image1 = preprocess_image(image1_path)
    image2 = preprocess_image(image2_path)
    
    # Extract features from both images
    features1 = model.predict(image1)
    features2 = model.predict(image2)
    
    # Compute cosine similarity
    similarity = cosine_similarity(features1, features2)
    
    return similarity[0][0]

# Replace these paths with the actual paths to your image files
image1_path = 'code/pic1.jpg'
image2_path = 'code/pic2.jpg'

# 建立視窗
top = tk.Tk() 
top.title('對比') 
top.geometry('1200x700+200+100') 

# 讀取圖片
picture1 = ImageTk.PhotoImage(Image.open(image1_path))
picture2 = ImageTk.PhotoImage(Image.open(image2_path))

#按鈕函式
def compare_images():
    similarity = calculate_cnn_similarity(image1_path, image2_path)
    compare_text = f"CNN相似度: {similarity:.4f}"
    label_left_text.config(text=compare_text)

# 顯示圖片
label_left = tk.Label(top, height=560, width=480, bg='gray94', fg='blue', image=picture1) 
label_right = tk.Label(top, height=560, width=480, bg='gray94', fg='blue', image=picture2) 

label_left.grid(row=0, column=0, padx=10, pady=10)
label_right.grid(row=0, column=1, padx=10, pady=10)

# 建立文字label
label_left_text = tk.Label(top, text="", height=10, width=30)
label_left_text.grid(row=1, column=0, padx=10, pady=10)
# 建立比較按鈕
compare_button = tk.Button(top, text="比較圖片", command=compare_images)
compare_button.grid(row=1, column=1, padx=10, pady=10)

# 執行gui
top.mainloop()
