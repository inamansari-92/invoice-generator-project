import os
from flask import Flask, render_template, request, send_file, jsonify
from invoice_generator import generate_pdf, format_date
from datetime import datetime

# Get absolute path to current directory
base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
            template_folder=os.path.join(base_dir, 'templates'),
            static_folder=os.path.join(base_dir, 'static'))

# Debugging: Print paths to verify
print(f"Base directory: {base_dir}")
print(f"Template folder: {app.template_folder}")
print(f"Static folder: {app.static_folder}")

@app.route('/')
def index():
    return render_template('invoice.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    data = request.json
    invoice_number = data['invoice_number']
    delivery_date = data['delivery_date']
    vehicle_number = data['vehicle_number']
    quantity = float(data['quantity'])
    unit_price = float(data['unit_price'])
    total_price = quantity * unit_price
    
    try:
        # Generate PDF and get its absolute path
        filename = generate_pdf(
            invoice_number=invoice_number,
            delivery_date=delivery_date,
            vehicle_number=vehicle_number,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price
        )
        
        # Return just the filename without path for download
        return jsonify({
            'success': True,
            'filename': os.path.basename(filename)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error downloading file: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)