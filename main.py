import os
import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads/documents/'
app.config['CSV_FOLDER'] = 'uploads/csv_files/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CSV_FOLDER'], exist_ok=True)

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        registration_id = request.form['registration_id']
        document = request.files['document']

        if document:
            document_filename = document.filename
            document.save(os.path.join(app.config['UPLOAD_FOLDER'], document_filename))

            csv_file_path = os.path.join(app.config['CSV_FOLDER'], f"{name}.csv")
            with open(csv_file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, department, registration_id, document_filename])

            return redirect(url_for('index'))

    return render_template('index.html')

# Route for viewing data
@app.route('/view_data')
def view_data():
    data = []
    for csv_file in os.listdir(app.config['CSV_FOLDER']):
        if csv_file.endswith('.csv'):
            with open(os.path.join(app.config['CSV_FOLDER'], csv_file), 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row)
    return render_template('view_data.html', data=data)

# Route for stopping the application
@app.route('/stop_application')
def stop_application():
    data = []
    for csv_file in os.listdir(app.config['CSV_FOLDER']):
        if csv_file.endswith('.csv'):
            with open(os.path.join(app.config['CSV_FOLDER'], csv_file), 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row)
    return render_template('stop_application.html', data=data)

# Main function
if __name__ == '__main__':
    app.run(debug=True)

# Templates
index_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>User Data Collection</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">
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
'''

view_data_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>View Data</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">
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
'''

stop_application_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Application Stopped</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">
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
'''

# CSS
style_css = '''
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
'''

# Write templates and static files
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)

with open('templates/index.html', 'w') as f:
    f.write(index_html)

with open('templates/view_data.html', 'w') as f:
    f.write(view_data_html)

with open('templates/stop_application.html', 'w') as f:
    f.write(stop_application_html)

with open('static/css/style.css', 'w') as f:
    f.write(style_css)
