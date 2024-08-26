from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
import subprocess
import re
from datetime import datetime
import shutil
import atexit
import random
from PIL import Image
# import logging

app = Flask(__name__, template_folder='templates', static_folder='static')

# # Configure logging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('app.log'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FILENAMES = ["", ""] # filename 永遠只有2個
dir_name = ''
save_path = ''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def sanitize_filename(filename):
    filename = secure_filename(filename)
    # 對檔名做時間處理
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_number = random.randint(1000, 9999)  # 生成 4 位的隨機數
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_{timestamp}_{random_number}{ext}"
    return re.sub(r'\s+', '_', new_filename)

@app.route('/')
def home():
    global dir_name, save_path
    run_before_request(dir_name)
    dir_name = datetime.now().strftime('%Y%m%d%H%M%S%f')
    save_path = os.path.join('static', dir_name)
    os.makedirs(save_path, exist_ok=True)
    return render_template('index.html')
@app.route('/about')
def about():
    run_before_request(dir_name)
    return render_template('about.html')
@app.route('/index')
def index():
    global dir_name, save_path
    run_before_request(dir_name)
    dir_name = datetime.now().strftime('%Y%m%d%H%M%S%f')
    save_path = os.path.join('static', dir_name)
    os.makedirs(save_path, exist_ok=True)
    return render_template('index.html')
@app.route('/index/compare')
def comapre():
    image1_url = request.args.get('image1')
    image2_url = request.args.get('image2')
    return render_template('compare.html', image1=image1_url, image2=image2_url)
@app.route('/index/compare/introSSIM')
def introSSIM():
    return render_template('introSSIM.html')
@app.route('/index/compare/introHSV')
def introHSV():
    return render_template('introHSV.html')
@app.route('/index/compare/introCNN')
def introCNN():
    return render_template('introCNN.html')
@app.route('/index/compare/introRandomForest')
def introRandomForest():
    return render_template('introRandomForest.html')

#清空之前的資料 不然電腦早晚會爆炸
def run_before_request(dir_name):
    if dir_name and os.path.isdir(f'static/{dir_name}'):
        shutil.rmtree(f'static/{dir_name}')
        print(f"Directory static/{dir_name} deleted successfully")
    else:
        print(f"No directory found to delete for static/{dir_name}")

# uploads images
@app.route('/upload', methods=['POST'])
def upload_file():
    global dir_name, save_path

    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400
    
    file = request.files['file']
    box_id = request.form['box_id']

    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = sanitize_filename(file.filename)
        file.save(os.path.join(save_path, filename))
        
        # 根据 box_id 更新 FILENAMES
        if box_id == 'image-box1':
            FILENAMES[0] = filename
        elif box_id == 'image-box2':
            FILENAMES[1] = filename
        else:
            return jsonify({"success": False, "error": "Invalid box_id"}), 400

        with open(os.path.join(save_path, 'filenames.txt'), 'w') as f:
            for name in FILENAMES:
                f.write(f"{name}\n")
        return jsonify({"success": True, "url": f"/{save_path}/{filename}"}), 201
    else:
        return jsonify({"success": False, "error": "File type not allowed"}), 400

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# run runOverall.sh file
@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        result = subprocess.run(['./runOverall.sh', save_path], capture_output=True, text=True, check=True)
        hsv = read_file(os.path.join(save_path, 'HSVresult.txt'))
        ssim = read_file(os.path.join(save_path, 'SSIMresult.txt'))
        cnn = read_file(os.path.join(save_path, 'CNNresult.txt'))
        
        return jsonify(success=True, random_dir=dir_name, ssim=ssim, hsv=hsv, cnn=cnn), 200
    
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.stderr}), 500
    
# 讀 yolo特徵然後回傳給前端
@app.route('/get_features', methods=['POST'])
def get_features():
    print("run get features")
    global save_path

    features1 = []
    features2 = []

    filenames = [os.path.join(save_path, 'YOLOresult1.txt'), os.path.join(save_path, 'YOLOresult2.txt')]
    for index, filename in enumerate(filenames):
        # 如果文件不存在就404
        if not os.path.isfile(filename):
            return jsonify({'error': f'File {filename} not found'}), 404

        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                print(f"Lines from {filename}: {lines}")
                num_features = int(lines[0].strip())
                features = [lines[i].strip() for i in range(1, num_features + 1)]
                if index == 0:
                    features1 = features
                else:
                    features2 = features
        except Exception as e:
            return jsonify({'error': f'Error reading file {filename}: {str(e)}'}), 500
    print("Features1:", features1)
    print("Features2:", features2)
    return jsonify({'dir_name': dir_name, 'features1': features1, 'features2': features2})

# 存被勾選的檔案是啥
@app.route('/save_image_src', methods=['POST'])
def save_image_src():
    global save_path

    data = request.json
    src1_path = data.get('src1', '').split('static')[-1]
    src2_path = data.get('src2', '').split('static')[-1]

    try:
        with open(os.path.join(save_path, 'partial-imagesChecked.txt'), 'w') as file:
            file.write(f"{src1_path}\n")
            file.write(f"{src2_path}\n")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# run runpartial.sh
@app.route('/run_partial_script', methods=['POST'])
def run_partial_script():
    global save_path
    try:
        
        result = subprocess.run(['./runPartial.sh', save_path], capture_output=True, text=True, check=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)


        hsv = read_file(os.path.join(save_path, 'PartialHSVresult.txt'))
        ssim = read_file(os.path.join(save_path, 'PartialSSIMresult.txt'))
        cnn = read_file(os.path.join(save_path, 'PartialCNNresult.txt'))
        
        return jsonify({"success": True, "ssim": ssim, "hsv": hsv, "cnn": cnn}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 回傳給 js save_path
@app.route('/get-folder-name', methods=['GET'])
def get_folder_name():
    return jsonify({"folder_name": save_path})

# 清掉資料夾
def cleanup():
    global dir_name
    if dir_name and os.path.isdir(f'static/{dir_name}'):
        shutil.rmtree(f'static/{dir_name}')
        print(f"Directory static/{dir_name} deleted successfully")
    else:
        print(f"No directory found to delete for static/{dir_name}")

atexit.register(cleanup)   

if __name__ == '__main__':
    # run
    app.run(debug=True)
