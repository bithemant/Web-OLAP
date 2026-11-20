# Web-OLAP — Business Growth Analyzer

A Flask web app that turns an Excel or CSV file into OLAP-style analysis: upload your data, group and aggregate it, drill down into rows, and view the results as interactive Plotly charts.

## What it does

Upload a spreadsheet (sales data, purchases, or any tabular data) and the app detects numeric and date columns, shows a 10-row preview, and lets you aggregate a measure grouped by one or more dimensions, drill down into the underlying rows with filters, and see a time series grouped by month, quarter or year.

## Features

- Upload Excel (`.xlsx`, `.xls`) or CSV files, up to 50 MB
- Automatic detection of numeric and date columns
- 10-row data preview after upload
- Aggregation: group a measure by one or more dimensions (sum, count and other aggregations)
- Drill-down: filter the original rows by column values (returns up to 1000 rows)
- Time series: totals over time grouped by month, quarter or year, with sales and purchase columns picked up automatically when their names match
- Interactive charts with Plotly.js: a 3D scatter chart for aggregated results and a time-series line chart
- Sample dataset included (`sample_data.xlsx`) so you can try it without your own file

## Tech stack

- Flask — web framework
- Pandas and NumPy — data loading and analysis
- OpenPyXL — reading Excel files
- Werkzeug — WSGI utilities and secure file uploads
- Plotly.js 2.26.1 (CDN) — interactive charts

## How to run

You need Python 3.9+.

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000/ in your browser.

> Note: `app.py` looks for the page in a `templates/` folder and the stylesheet in a `static/` folder, so before running, move `index.html` into `templates/` and `style.css` into `static/`. The files are currently at the repo root.

## Project structure

```
Web-OLAP/
├── app.py             # Flask backend: upload, aggregate, drill-down, time series
├── index.html         # Frontend: upload form, OLAP controls, Plotly charts
├── style.css          # Frontend styling
├── requirements.txt   # Flask, pandas, openpyxl, numpy, werkzeug
└── sample_data.xlsx   # Sample dataset to try the app with
```
