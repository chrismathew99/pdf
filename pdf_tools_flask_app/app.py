from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path
import os
import tempfile

app = Flask(__name__)

# Ensure the static and template folders are correctly linked
app.static_folder = 'static'
app.template_folder = 'templates'

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        if pdf_file:
            filename = os.path.join(tempfile.mkdtemp(), pdf_file.filename)
            pdf_file.save(filename)
            return render_template('options.html', filename=filename)
    return 'No file uploaded', 400

@app.route('/extract_text', methods=['POST'])
def extract_text():
    filename = request.form.get('filename')
    if filename:
        reader = PdfFileReader(filename)
        text = ''
        for page in range(reader.numPages):
            text += reader.getPage(page).extractText()
        return render_template('result.html', result=text, filename=filename, action='Extracted Text')
    return 'File not found', 404

@app.route('/convert_to_image', methods=['POST'])
def convert_to_image():
    filename = request.form.get('filename')
    if filename:
        images = convert_from_path(filename)
        image_folder = tempfile.mkdtemp()
        image_paths = []
        for i, image in enumerate(images):
            image_path = os.path.join(image_folder, f'page_{i}.jpg')
            image.save(image_path, 'JPEG')
            image_paths.append(image_path)
        return render_template('result.html', result=image_paths, filename=filename, action='Converted to Images')
    return 'File not found', 404

@app.route('/download_file', methods=['GET'])
def download_file():
    filepath = request.args.get('filepath')
    if filepath and os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return 'File not found', 404

if __name__ == '__main__':
    app.run(debug=True)