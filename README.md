# 📊 Business Growth Analyzer (OLAP with Flask)

A Flask-based **OLAP (Online Analytical Processing) web application** that lets you upload Excel/CSV data, perform drill-down, roll-up, slice, and dice operations, and visualize business insights using Plotly.

## 🚀 Features
- Upload Excel/CSV file for analysis  
- OLAP operations: **Drill-down, Roll-up, Slice, Dice**  
- Interactive **charts and graphs** with Plotly.js  
- Data processing using **Pandas & NumPy**  
- Excel support via **OpenPyXL**  
- Simple and clean Flask web interface  

## 🛠️ Tech Stack
- **Flask** → Web framework  
- **Pandas & NumPy** → Data analysis and manipulation  
- **OpenPyXL** → Excel file support  
- **Plotly.js** → Interactive charting  
- **Werkzeug** → WSGI utility for Flask  


## 📂 How It Works
1. Upload your Excel/CSV dataset  
2. Flask backend processes data with Pandas  
3. Apply OLAP operations (aggregation, filtering, drill-down)  
4. Data is converted to JSON  
5. Plotly.js renders interactive charts  

## 📌 Use Cases
- Sales & purchase trend analysis  
- Profit/loss visualization  
- Business intelligence for SMEs  
- Data-driven decision making  


## ▶️ Getting Started

### Prerequisites
Make sure you have Python 3.9+ installed.  
Install the required dependencies:
```bash
pip install -r requirements.txt

Run the App
python app.py


Then open http://127.0.0.1:5000/
in your browser. ✅
