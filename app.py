import os
from flask import Flask, render_template, request, redirect, url_for, session
import csv

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'csv_files'), exist_ok=True)

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        base_folder = request.form['base_folder']
        session['base_folder'] = base_folder
        session['upload_folder'] = os.path.join(base_folder, 'documents')
        session['csv_folder'] = os.path.join(base_folder, 'csv_files')

        os.makedirs(session['upload_folder'], exist_ok=True)
        os.makedirs(session['csv_folder'], exist_ok=True)

        return redirect(url_for('index'))
    return render_template('setup.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'base_folder' not in session:
        session['base_folder'] = app.config['UPLOAD_FOLDER']
        session['upload_folder'] = os.path.join(app.config['UPLOAD_FOLDER'], 'documents')
        session['csv_folder'] = os.path.join(app.config['UPLOAD_FOLDER'], 'csv_files')

    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        registration_id = request.form['registration_id']
        document = request.files['document']

        if document:
            document_filename = document.filename
            document.save(os.path.join(session['upload_folder'], document_filename))

            csv_file_path = os.path.join(session['csv_folder'], f"{name}.csv")
            with open(csv_file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, department, registration_id, document_filename])

            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/view_data')
def view_data():
    data = []
    csv_folder = session.get('csv_folder', app.config['UPLOAD_FOLDER'])

    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith('.csv'):
            with open(os.path.join(csv_folder, csv_file), 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row)
    return render_template('view_data.html', data=data)

@app.route('/stop_application')
def stop_application():
    data = []
    csv_folder = session.get('csv_folder', app.config['UPLOAD_FOLDER'])

    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith('.csv'):
            with open(os.path.join(csv_folder, csv_file), 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row)
    return render_template('stop_application.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
