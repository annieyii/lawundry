from PIL import Image
import os

def process_image(image_path, output_folder, prefix):
    image = Image.open(image_path)
    width, height = image.size
    grid_width = width // 3
    grid_height = height // 3
    
    for i in range(3):
        for j in range(3):
            box = (j * grid_width, i * grid_height, (j + 1) * grid_width, (i + 1) * grid_height)
            grid_image = image.crop(box)
            grid_image.save(os.path.join(output_folder, f'{prefix}-{i+1}-{j+1}.png'))

def main():
    # 圖像路徑
    image1_path = 'path/to/your/image1.png'
    image2_path = 'path/to/your/image2.jpg'
    
    # 輸出資料夾
    output_folder = 'path/to/output/folder'
    os.makedirs(output_folder, exist_ok=True)
    
    # 處理圖像
    process_image(image1_path, output_folder, 'img1')
    process_image(image2_path, output_folder, 'img2')

if __name__ == '__main__':
    main()
