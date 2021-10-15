from flask import Flask, jsonify, request, render_template
import io, base64

from app.utils.prediction import get_top5


app = Flask(__name__)

ALLOWED_EXTENSION = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/infer', methods = ['POST', 'GET'])
def predict():
    if request.method == 'POST':
        img_bytes = []
        for key in request.files.keys():
            file = request.files.get(key)
            if file is None or file.filename == "":
                return jsonify({'error': 'No file selected'})
            if not allowed_file(file.filename):
                return jsonify({'error': 'File extension not allowed'})
            
            img_bytes.append(file.read())

        try:
            result = get_top5(img_bytes)
            data = io.BytesIO(img_bytes[0])
            encoded_img_data = base64.b64encode(data.getvalue())
            return render_template('inference.html', result = result, img_data=encoded_img_data.decode('utf-8'))
        except Exception as e:
            print(e)
            return jsonify({'error': 'Error in prediction'})