from flask import Flask, request, render_template, send_file, abort
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
        filename = secure_filename(file.filename)  # Sanitize the filename
        filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filename)
        return render_template('options.html', filename=file.filename)
    else:
        return render_template('result.html', message='Invalid file format')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    files = request.files.getlist('file')
    if len(files) != 2:
        return render_template('result.html', message='Please upload exactly two PDF files.')
    merger = PdfFileMerger()
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Sanitize the filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            merger.append(filepath)
        else:
            return render_template('result.html', message='Invalid file format')
    output = io.BytesIO()
    merger.write(output)
    output.seek(0)
    return send_file(output, attachment_filename='merged.pdf', as_attachment=True)

@app.route('/split', methods=['POST'])
def split_pdf():
    filename = request.form['filename']
    filename = secure_filename(filename)  # Sanitize the filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        pdf = PdfFileReader(filepath)
        outputs = []
        for page in range(pdf.getNumPages()):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))
            output_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'split_{filename}_page_{page}.pdf')
            with open(output_filename, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
            outputs.append(output_filename)
    except Exception as e:
        return abort(500, description=f"Error processing file: {str(e)}")
    try:
        return send_file(outputs[0], attachment_filename=os.path.basename(outputs[0]), as_attachment=True)
    except Exception as e:
        return abort(500, description=f"Error sending file: {str(e)}")

@app.route('/extract_text', methods=['POST'])
def extract_text():
    filename = request.form['filename']
    filename = secure_filename(filename)  # Sanitize the filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf = PdfFileReader(filepath)
    text = ''
    for page in range(pdf.getNumPages()):
        text += pdf.getPage(page).extractText()
    return render_template('result.html', message='Extracted Text', text=text)

@app.route('/convert_to_image', methods=['POST'])
def convert_to_image():
    filename = request.form['filename']
    filename = secure_filename(filename)  # Sanitize the filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    images = convert_from_path(filepath)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}.jpg')
    images[0].save(image_path, 'JPEG')
    return send_file(image_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)