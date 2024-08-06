from PIL import Image, ImageFilter
import cv2
import os
from ultralytics import YOLO

# 加載 YOLOv9 訓練模型 # pip install ultralytics
model = YOLO('yolov9s.pt')

# 加載圖片
img_path = '1.jpg'  # 之後記得改圖片
img_cv2 = cv2.imread(img_path)

if img_cv2 is None:
    raise FileNotFoundError(f"Cannot load image file: {img_path}")

# 圖片大小處理
scale_percent = 200  # 圖片放大100%
width = int(img_cv2.shape[1] * scale_percent / 100)
height = int(img_cv2.shape[0] * scale_percent / 100)
dim = (width, height)
img_cv2 = cv2.resize(img_cv2, dim, interpolation=cv2.INTER_LINEAR)

# 圖片轉換為 PIL 圖片，然後轉換為 RGB 格式
img_pil = Image.fromarray(cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB))

# 進行檢測
results = model(img_pil)

# 獲取檢測結果
detections = results[0].boxes.data.cpu().numpy() # 0代表第一張圖片

# 讀取圖片作為 numpy 陣列
height, width, _ = img_cv2.shape

# 用來計算物件類別數量
object_counts = {}

# 創建存儲檢測範圍截圖的目錄
output_dir = "partpic"
os.makedirs(output_dir, exist_ok=True)

# 處理每個檢測到的物件
for idx, (*box, conf, cls) in enumerate(detections):
    x1, y1, x2, y2 = map(int, box)
    label = f"{model.names[int(cls)]} {conf:.2f}"

    # 更新物件數量
    class_name = model.names[int(cls)]
    if class_name in object_counts:
        object_counts[class_name] += 1
    else:
        object_counts[class_name] = 1

    # 繪製邊框
    cv2.rectangle(img_cv2, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # 繪製標籤
    cv2.putText(img_cv2, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    print(f"ObjectName: {model.names[int(cls)]}")

    # 截取範圍內的圖像並保存
    cropped_img = img_cv2[y1:y2, x1:x2]
    cropped_img_path = os.path.join(output_dir, f"detection_{idx}_{class_name}.jpg")
    cv2.imwrite(cropped_img_path, cropped_img)

    # 將截取的圖像轉換為 PIL 圖像並銳化
    cropped_img_pil = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
    sharp_img = cropped_img_pil.filter(ImageFilter.UnsharpMask(radius=5, percent=100, threshold=10))
    sharp_img_path = os.path.join(output_dir, f"sharp_{idx}_{class_name}.jpg")
    sharp_img.save(sharp_img_path)

# 輸出物件數量
for object_name, count in object_counts.items():
    print(f"Number of {object_name}: {count}")

# 顯示結果圖片
cv2.imshow('Detected Image', img_cv2)  # colab上要註解掉這行
cv2.waitKey(0)
cv2.destroyAllWindows()
