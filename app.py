from flask import Flask, jsonify, request
from src.prediction import get_top5


app = Flask(__name__)

ALLOWED_EXTENSION = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route('/predict/', methods = ['POST', 'GET'])
def predict():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({'error': 'No file selected'})
        if not allowed_file(file.filename):
            return jsonify({'error': 'File extension not allowed'})

        try:
            img_bytes = file.read()
            top5_per, top5_classes = get_top5(img_bytes)
            data = {'classes': top5_classes, 'percentages': top5_per}
            return jsonify(data)
        except:
            return jsonify({'error': 'Error in prediction'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')