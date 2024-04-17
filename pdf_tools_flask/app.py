from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from pdf2image import convert_from_path
import io

app = Flask(__name__)

# Configure upload folder and allowed extensions
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
    if 'file' not in request.files:
        return render_template('result.html', message='No file part')
    file = request.files['file']
    if file.filename == '':
        return render_template('result.html', message='No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) # Sanitize the filename
        filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filename)
        return render_template('options.html', filename=file.filename)
    else:
        return render_template('result.html', message='Invalid file format')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    files = request.form.getlist('files')
    merger = PdfFileMerger()
    for filename in files:
        filename = secure_filename(filename) # Sanitize the filename
        merger.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    output = io.BytesIO()
    merger.write(output)
    output.seek(0)
    return send_file(output, attachment_filename='merged.pdf', as_attachment=True)

@app.route('/split', methods=['POST'])
def split_pdf():
    filename = request.form['filename']
    filename = secure_filename(filename) # Sanitize the filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf = PdfFileReader(filepath)
    outputs = []
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        outputs.append(output)
    # For simplicity, return only the first page as a response
    return send_file(outputs[0], attachment_filename=f'split_{filename}', as_attachment=True)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    filename = request.form['filename']
    filename = secure_filename(filename) # Sanitize the filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf = PdfFileReader(filepath)
    text = ''
    for page in range(pdf.getNumPages()):
        text += pdf.getPage(page).extractText()
    return render_template('result.html', message='Extracted Text', text=text)

@app.route('/convert_to_image', methods=['POST'])
def convert_to_image():
    filename = request.form['filename']
    filename = secure_filename(filename) # Sanitize the filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    images = convert_from_path(filepath)
    # For simplicity, save and return only the first page as an image
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}.jpg')
    images[0].save(image_path, 'JPEG')
    return send_file(image_path, as_attachment=True)

# Error handling and security practices are important considerations omitted in the initial version of the code.
# Here, we've added filename sanitation to protect against path traversal vulnerabilities. However, for a
# complete and secure implementation, consider adding validation for the content of PDFs and handling exceptions gracefully.

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)