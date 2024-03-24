import csv
import logging
from flask import Flask, request, jsonify



app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    filename = data['file']
    product = data['product']
    file_path = f'/parth_PV_dir/{filename}'

    try:
        total_sum = 0
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            if not csv_reader.fieldnames or 'product' not in csv_reader.fieldnames or 'amount' not in csv_reader.fieldnames:
                raise csv.Error
            for row in csv_reader:
                if row['product'] == product:
                    total_sum += int(row['amount'])

        logging.info("File processed successfully: %s", file_path)
        return jsonify(file=filename, sum=total_sum)

    except FileNotFoundError:
        logging.warning("File not found: %s", file_path)
        return jsonify(file=filename, error="File not found."), 404

    except csv.Error:
        logging.error("Input file not in CSV format: %s", file_path)
        return jsonify(file=filename, error="Input file not in CSV format."), 400

    except Exception as err:
        logging.error("An unexpected error occurred: %s", err)
        return jsonify(file=filename, error=str(err)), 500



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
