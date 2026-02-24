from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import os
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit

def detect_date_columns(df):
    date_cols = []
    for c in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[c]):
            date_cols.append(c)
        else:
            try:
                parsed = pd.to_datetime(df[c], errors='coerce')
                if parsed.notna().sum() > 0:
                    df[c] = parsed
                    date_cols.append(c)
            except Exception:
                pass
    return date_cols, df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'no file part'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'no selected file'}), 400
    filename = secure_filename(f.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(save_path)
    # try read into pandas
    try:
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(save_path)
        else:
            df = pd.read_excel(save_path)
    except Exception as e:
        return jsonify({'error': f'failed reading file: {e}'}), 400

    # store dataframe in app config so drilldown can access original rows
    app.config['DATAFRAME'] = df.copy()

    # detect numeric and date columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    date_columns, df = detect_date_columns(df)
    preview = df.head(10).fillna('').to_dict(orient='records')
    cols = df.columns.tolist()

    return jsonify({
        'filename': filename,
        'columns': cols,
        'numeric_columns': numeric_columns,
        'date_columns': date_columns,
        'preview': preview
    })

@app.route('/aggregate', methods=['POST'])
def aggregate():
    data = request.form
    filename = data.get('filename')
    dimensions_raw = data.get('dimensions','')
    dimensions = [d.strip() for d in dimensions_raw.split(',') if d.strip()]
    measure = data.get('measure')
    agg = data.get('agg','sum')
    date_column = data.get('date_column')
    time_granularity = data.get('time_granularity','Month')

    if not filename:
        return jsonify({'error':'filename required'}), 400
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if not os.path.exists(file_path):
        return jsonify({'error':'file not found on server'}), 400

    try:
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        return jsonify({'error': f'failed reading file: {e}'}), 400

    if len(dimensions) == 0:
        return jsonify({'error':'no dimensions provided'}), 400
    if not measure:
        return jsonify({'error':'no measure provided'}), 400

    # coerce measure numeric
    df[measure] = pd.to_numeric(df[measure], errors='coerce')
    required = dimensions + [measure]
    df_clean = df.dropna(subset=required, how='any').copy()

    try:
        agg_map = {measure: agg if agg != 'count' else 'count'}
        grouped = df_clean.groupby(dimensions).agg(agg_map).reset_index()
        measure_col = f"{agg}_{measure}" if agg != 'count' else f"count_{measure}"
        # rename resulting numeric column
        grouped = grouped.rename(columns={measure: measure_col})
        pivot = grouped.fillna('').to_dict(orient='records')
    except Exception as e:
        return jsonify({'error': f'aggregation failed: {e}'}), 500

    result = {'pivot': pivot, 'measure_col': measure_col}

    # timeseries
    if date_column and date_column in df.columns:
        try:
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            df_ts = df.dropna(subset=[date_column]).copy()
            if time_granularity == 'Month':
                df_ts['period'] = df_ts[date_column].dt.to_period('M').dt.to_timestamp()
            elif time_granularity == 'Quarter':
                df_ts['period'] = df_ts[date_column].dt.to_period('Q').dt.start_time
            else:
                df_ts['period'] = df_ts[date_column].dt.to_period('Y').dt.start_time

            metrics = {}
            for c in df_ts.columns:
                low = c.lower()
                if 'sale' in low and 'sales' not in metrics:
                    metrics['sales'] = c
                if ('purch' in low or 'purchase' in low) and 'purchases' not in metrics:
                    metrics['purchases'] = c
            metrics['measure'] = measure
            agg_cols = list(set(metrics.values()))
            for c in agg_cols:
                df_ts[c] = pd.to_numeric(df_ts[c], errors='coerce').fillna(0)

            ts = df_ts.groupby('period')[agg_cols].sum().reset_index().sort_values('period')
            ts['period'] = ts['period'].dt.strftime('%Y-%m-%d')
            result['timeseries'] = ts.fillna(0).to_dict(orient='records')
        except Exception as e:
            result['timeseries_error'] = str(e)

    return jsonify(result)

@app.route('/drilldown', methods=['POST'])
def drilldown():
    # Uses the stored original dataframe in app.config['DATAFRAME']
    df = app.config.get('DATAFRAME')
    if df is None:
        return jsonify({'error': 'No data uploaded yet'}), 400
    try:
        payload = request.get_json(force=True)
        filters = payload.get('filters', {})
        # Apply filters: equality-match
        filtered = df.copy()
        for col, val in filters.items():
            # try to match types: if column is datetime, parse val
            if col in filtered.columns and pd.api.types.is_datetime64_any_dtype(filtered[col]):
                # compare date part if val looks like YYYY-MM-DD
                try:
                    parsed = pd.to_datetime(val, errors='coerce')
                    filtered = filtered[filtered[col] == parsed]
                except Exception:
                    filtered = filtered[filtered[col].astype(str) == str(val)]
            else:
                filtered = filtered[filtered[col].astype(str) == str(val)]
        # return records (limit to first 1000 rows)
        return jsonify(filtered.fillna('').to_dict(orient='records')[:1000])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
