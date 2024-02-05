from flask import Flask, request, jsonify
from rembg import remove
import os

app = Flask(__name__) 

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def process_image(input_path, output_path):
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input_data = i.read()
            output_data = remove(input_data)
            o.write(output_data)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png')

        file.save(input_path)

        process_image(input_path, output_path)

        return jsonify({'message': 'Image processed successfully', 'output_path': output_path})

if __name__ == '__main__':
    app.run(debug=True)


# from rembg import remove
# from PIL import Image

# inputPath = easygui.fileopenbox(title="Select image file");
# outputPath = easygui.filesavebox(title="Save as");

# input = Image.open(inputPath)
# output = remove(input)
# output.save(outputPath) 
