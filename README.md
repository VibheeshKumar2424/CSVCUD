# User Data Collection Application

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-green.svg)
![Pandas](https://img.shields.io/badge/Data-Pandas-orange.svg)

## Description
This is a Python application using **Tkinter** for the UI and **Pandas** for data management. It allows users to:
- Collect and store user data (Name, Department, Register ID, and File Name).
- Specify or browse a directory to save collected data as a **CSV file**.
- Import data from an existing CSV file located in another folder.
- Display collected and imported data in a **table view**.
- Show the data table when the application stops.

## Features
- 📝 **User Input Form:** Users can enter their details and save them in a CSV file.
- 📂 **Browse Folder Option:** Users can select a directory to store the collected data.
- 🔄 **Import CSV Feature:** Users can import a CSV file from another folder.
- 📊 **View Data Table:** A table representation of all collected and imported data.
- 🛑 **Stop and View Data:** When stopping the application, the collected data is displayed.
- 🚀 **Uses Pandas for Data Management and Tkinter for UI.**

## Installation

### Prerequisites
Ensure you have **Python 3.8+** installed.

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/user-data-collection.git
   cd user-data-collection
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python app.py
   ```

## Usage
1. Open the application.
2. Enter user details: **Name, Department, Register ID, File Name.**
3. Click **Browse Folder** to choose a directory where the data should be saved.
4. Click **Save Data** to store the data in the selected directory as a CSV file.
5. Click **Import CSV** to load data from another CSV file.
6. Click **View Data** to display the collected and imported data.
7. Click **Stop Application** to exit and show the final data table.

## Uploading to GitHub
### First-time setup
1. Initialize a Git repository (if not already initialized):
   ```sh
   git init
   ```
2. Add all project files:
   ```sh
   git add .
   ```
3. Commit the changes:
   ```sh
   git commit -m "Initial commit"
   ```
4. Connect to a GitHub repository:
   ```sh
   git remote add origin https://github.com/VibheeshKumar2424/CSVCUD.git
   ```
5. Push the code to GitHub:
   ```sh
   git branch -M main
   git push -u origin main
   ```

## Folder Structure
```
user-data-collection/
│── app.py
│── requirements.txt
│── templates/
│── README.md
│── uploads/ (User-specified directory for storing CSV files)
│── imported/ (Imported CSV files are stored here)
```

## License
This project is licensed under the **MIT License**.

