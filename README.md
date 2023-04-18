<h1 align="center">
  <img src="https://github.com/ArchontisKostis/CodeInspector/blob/master/static/assets/svg/logo_1.svg" width="48" height="48" />
  CodeInspector Web App
</h1>

<p align="center">
  <em>🔍 A web app for generating software quality analysis based on hotspot prioritization 🛠️</em> 
</p>

<p align="center">
  <em><b>Made with:</b></em> <br>
  <img src="https://img.shields.io/badge/Flask-blue" alt="Made with Flask" />
  <img src="https://img.shields.io/badge/Bootstrap-purple" alt="Made with Bootstrap" />
  <img src="https://img.shields.io/badge/PyDriller-green" alt="Made with PyDriller" />
  <img src="https://img.shields.io/badge/Plotly-orange" alt="Made with Plotly" />
</p>

## 🚀 Overview
CodeInspector is a web app that provides software quality analysis based on hotspot prioritization.
It takes a repository URL (currently for Java projects) and generates insights on modified files, file churn, complexity, and priority for quality improvement.
The app uses Flask for web development, Bootstrap for styling, PyDriller for repository mining, and Plotly for visualizing data.

## 🛠️ Installation

### 🐙 Clone the Repository
To clone this repository, follow the steps below:
1. Open your terminal and navigate to the directory where you want to clone the repository.
2. Run the following command:
```
git clone https://github.com/yourusername/codeinspector-web-app.git
```

### ⚙️ Install Dependencies
This Flask web app requires certain dependencies to be installed. The list of dependencies, along with their versions, are listed in the requirements.txt file. Follow the steps below to install the dependencies:

1. Navigate to the cloned repository's directory in your terminal.
2. Create a virtual environment (optional but recommended) using the following command:
```
python -m venv venv
```

3. Activate the virtual environment (if created) using the appropriate command for your operating system:
For Windows:
```
venv\Scripts\activate
```

For Unix/Linux
```
source venv/bin/activate
```

4. Install the dependencies using pip with the following command:
```
pip install -r requirements.txt
```

This will install all the required dependencies listed in the requirements.txt file into your virtual environment.

## 🚀 Run the CodeInspector Web App

After successfully installing the dependencies, you can run the CodeInspector web app locally. Follow the steps below:

1. Make sure you are still in the cloned repository's directory and that your virtual environment is active (if created).
2. Run the following command:
```
flask --app app run -h localhost -p 3000
```
This will start the CodeInspector web app and it will be accessible at http://localhost:3000 in your web browser.
