from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FILENAMES = []

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('about.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        FILENAMES.append(filename)
        with open('filenames.txt', 'w') as f:
            for name in FILENAMES:
                f.write(f"{name}\n")
        return jsonify({"success": True, "url": f"/uploads/{filename}"}), 201
    else:
        return jsonify({"success": False, "error": "File type not allowed"}), 400

# 把 upload 的 pic 丟到 uploads file 
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# run .sh file
@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        result = subprocess.run(['./runCode.sh', 'arg1', 'arg2'], capture_output=True, text=True)

        with open('HSVresult.txt', 'r') as file:
            hsv = file.read().strip()
        with open('SSIMresult.txt', 'r') as file:
            ssim = file.read().strip()
        
        return render_template('index.html', ssim=ssim, hsv=hsv)

        # return jsonify({"success": True, "output": result.stdout}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.stderr}), 500

if __name__ == '__main__':
    app.run(debug=True)
