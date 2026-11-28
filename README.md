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

## How to use

1. Start the app (`python app.py`) and open http://127.0.0.1:5000/ in your browser.
2. Upload a file: try the included `sample_data.xlsx`, or your own Excel (`.xlsx`, `.xls`) or CSV file (up to 50 MB). The app detects the numeric and date columns and shows a 10-row preview of your data.
3. Build an analysis: pick up to three dimensions, a numeric measure and an aggregation (sum by default), then click **Build OLAP & Charts**. The aggregated table appears with a 3D scatter chart.
4. Add a time series: choose a date column and a granularity — Month, Quarter or Year. Columns with "sale" or "purchase" in their name are picked up automatically for the time-series line chart.
5. Drill down: use **Slice**, **Dice** and **Pivot** to filter the original rows by column values. Drill-down returns up to the first 1000 matching rows.

## Troubleshooting

- **Port 5000 already in use:** the app binds port 5000 (`app.run(debug=True, port=5000)` in `app.py`). Stop the other process using the port, or change the port in `app.py`.
- **Upload fails or the file can't be read:** only `.xlsx`, `.xls` and `.csv` files are accepted, and files over 50 MB are rejected.
- **Drill-down says "No data uploaded yet":** upload a file first — drill-down filters the rows of the most recently uploaded file.

## Project structure

```
Web-OLAP/
├── app.py             # Flask backend: upload, aggregate, drill-down, time series
├── templates/
│   └── index.html     # Frontend: upload form, OLAP controls, Plotly charts
├── static/
│   └── style.css      # Frontend styling
├── requirements.txt   # Flask, pandas, openpyxl, numpy, werkzeug
└── sample_data.xlsx   # Sample dataset to try the app with
```
