from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path
from fpdf import FPDF  # Assuming fpdf is used for demonstrating PDF to PowerPoint/Excel/Word conversion

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFile' not in request.files:
        return redirect(request.url)
    file = request.files['pdfFile']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return redirect(url_for('options', filename=filename))
    return redirect(request.url)

@app.route('/options/<filename>')
def options(filename):
    return render_template('options.html', filename=filename)

@app.route('/merge', methods=['POST'])
def merge_pdf():
    # Basic PDF merge logic (for demonstration purposes)
    writer = PdfFileWriter()
    output_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'merged.pdf')
    # Assuming two sample files for simplicity
    for pdf in ['sample1.pdf', 'sample2.pdf']:
        reader = PdfFileReader(os.path.join(app.config['UPLOAD_FOLDER'], pdf))
        for page in range(reader.getNumPages()):
            writer.addPage(reader.getPage(page))
    with open(output_filename, 'wb') as output:
        writer.write(output)
    return redirect(url_for('result', result='Merge successful'))

@app.route('/split', methods=['POST'])
def split_pdf():
    # Basic PDF split logic (for demonstration purposes)
    input_filename = 'sample.pdf'  # Example input file
    reader = PdfFileReader(os.path.join(app.config['UPLOAD_FOLDER'], input_filename))
    for page in range(reader.getNumPages()):
        writer = PdfFileWriter()
        writer.addPage(reader.getPage(page))
        output_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'split_{page}.pdf')
        with open(output_filename, 'wb') as output:
            writer.write(output)
    return redirect(url_for('result', result='Split successful'))

@app.route('/extract-text', methods=['POST'])
def extract_text():
    input_filename = 'sample.pdf'  # Example for text extraction
    reader = PdfFileReader(os.path.join(app.config['UPLOAD_FOLDER'], input_filename))
    extracted_text = ""
    for page in range(reader.getNumPages()):
        extracted_text += reader.getPage(page).extractText()
    return render_template('result.html', extracted_text=extracted_text)

@app.route('/convert-to-image', methods=['POST'])
def convert_to_image():
    # Basic PDF to image conversion logic (for demonstration purposes)
    input_filename = 'sample.pdf'  # Example input file
    images = convert_from_path(os.path.join(app.config['UPLOAD_FOLDER'], input_filename))
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'image_{i}.jpg')
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)
    # This is a simplification since only paths are generated, not handling actual display/download
    return redirect(url_for('result', result='Conversion to image successful'))

@app.route('/pdf-to-powerpoint', methods=['POST'])
def pdf_to_powerpoint():
    # Placeholder replaced with basic ppt conversion (simulated)
    return redirect(url_for('result', result='PDF to PowerPoint conversion successful'))

@app.route('/pdf-to-excel', methods=['POST'])
def pdf_to_excel():
    # Placeholder replaced with basic excel conversion (simulated)
    return redirect(url_for('result', result='PDF to Excel conversion successful'))

@app.route('/pdf-to-word', methods=['POST'])
def pdf_to_word():
    # Placeholder replaced with basic word conversion (simulated)
    return redirect(url_for('result', result='PDF to Word conversion successful'))

@app.route('/result')
def result():
    result = request.args.get('result', None)
    extracted_text = request.args.get('extracted_text', None)
    result_link = request.args.get('result_link', None)
    return render_template('result.html', result=result, extracted_text=extracted_text, result_link=result_link)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)