import os
from flask import Flask, render_template_string, request, redirect, url_for, session
import csv

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session
app.config['BASE_FOLDER'] = 'uploads'

# HTML Templates
setup_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Setup Directory</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        h1 {
            text-align: center;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        button {
            margin: 10px;
            padding: 10px 20px;
            cursor: pointer;
        }
        button:hover {
            background-color: #ddd;
        }
    </style>
</head>
<body>
    <h1>Setup Directory</h1>
    <form method="post">
        <label for="base_folder">Base Folder:</label>
        <input type="text" id="base_folder" name="base_folder" value="uploads" required><br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

index_html = """
<!DOCTYPE html>
<html>
<head>
    <title>User Data Collection</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        h1 {
            text-align: center;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 10px;
            text-align: center;
        }
        button {
            margin: 10px;
            padding: 10px 20px;
            cursor: pointer;
        }
        button:hover {
            background-color: #ddd;
        }
    </style>
</head>
<body>
    <h1>User Data Collection</h1>
    <form method="post" enctype="multipart/form-data">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br>
        <label for="department">Department:</label>
        <input type="text" id="department" name="department" required><br>
        <label for="registration_id">Registration ID:</label>
        <input type="text" id="registration_id" name="registration_id" required><br>
        <label for="document">Document:</label>
        <input type="file" id="document" name="document" required><br>
        <button type="submit">Submit</button>
    </form>
    <a href="{{ url_for('view_data') }}"><button>View Data</button></a>
    <a href="{{ url_for('stop_application') }}"><button>Stop Application</button></a>
</body>
</html>
"""

view_data_html = """
<!DOCTYPE html>
<html>
<head>
    <title>View Data</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        h1 {
            text-align: center;
        }
        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse.
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Collected Data</h1>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Department</th>
                <th>Registration ID</th>
                <th>Document Name</th>
            </tr>
        </thead>
        <tbody>
            {% for row in data %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>{{ row[1] }}</td>
                    <td>{{ row[2] }}</td>
                    <td>{{ row[3] }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

stop_application_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Application Stopped</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        h1 {
            text-align: center.
        }
        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse.
        }
        table, th, td {
            border: 1px solid black.
        }
        th, td {
            padding: 10px.
            text-align: center.
        }
    </style>
</head>
<body>
    <h1>Final Collected Data</h1>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Department</th>
                <th>Registration ID</th>
                <th>Document Name</th>
            </tr>
        </thead>
        <tbody>
            {% for row in data %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>{{ row[1] }}</td>
                    <td>{{ row[2] }}</td>
                    <td>{{ row[3] }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        base_folder = request.form['base_folder']
        session['base_folder'] = base_folder

        upload_folder = os.path.join(base_folder, 'documents')
        csv_folder = os.path.join(base_folder, 'csv_files')

        session['upload_folder'] = upload_folder
        session['csv_folder'] = csv_folder

        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(csv_folder, exist_ok=True)

        return redirect(url_for('index'))
    return render_template_string(setup_html)


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'base_folder' not in session:
        # Check if the base directory exists on startup
        base_folder = app.config['BASE_FOLDER']
        upload_folder = os.path.join(base_folder, 'documents')
        csv_folder = os.path.join(base_folder, 'csv_files')
        if os.path.exists(upload_folder) and os.path.exists(csv_folder):
            session['base_folder'] = base_folder
            session['upload_folder'] = upload_folder
            session['csv_folder'] = csv_folder
        else:
            return redirect(url_for('setup'))

    upload_folder = session['upload_folder']
    csv_folder = session['csv_folder']

    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        registration_id = request.form['registration_id']
        document = request.files['document']

        if document:
            document_filename = document.filename
            document.save(os.path.join(upload_folder, document_filename))

            csv_file_path = os.path.join(csv_folder, f"{name}.csv")
            with open(csv_file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, department, registration_id, document_filename])

            return redirect(url_for('index'))

    return render_template_string(index_html)


@app.route('/view_data')
def view_data():
    if 'csv_folder' not in session:
        return redirect(url_for('setup'))

    csv_folder = session['csv_folder']
    data = []
    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith('.csv'):
            with open(os.path.join(csv_folder, csv_file), 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row)
    return render_template_string(view_data_html, data=data)


@app.route('/stop_application')
def stop_application():
    if 'csv_folder' not in session:
        return redirect(url_for('setup'))

    csv_folder = session['csv_folder']
    data = []
    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith('.csv'):
            with open(os.path.join(csv_folder, csv_file), 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row)
    return render_template_string(stop_application_html, data=data)


if __name__ == '__main__':
    app.run(debug=True)
