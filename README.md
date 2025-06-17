# Invoice Generator - A.T COMMODITIES

![Invoice Generator](https://via.placeholder.com/800x400?text=Professional+Invoice+Generation+Solution)

This project provides a complete solution for generating professional invoices for A.T COMMODITIES. It includes both a standalone Python script for command-line invoice generation and a web application built with Flask for browser-based invoice creation.

## Features

- **Standalone Invoice Generator**
  - Text-based invoice display in console
  - PDF invoice generation using ReportLab
  - Automatic total calculation
  - Amount conversion to words
  - Professional invoice formatting
  - Landscape-oriented PDFs
  - Date formatting (DD-MMM-YYYY)

- **Web Application**
  - Responsive HTML form for data entry
  - Form validation with JavaScript
  - PDF generation via Flask backend
  - Download generated invoices
  - Clean, professional UI with CSS styling
  - AJAX form submission
  - Error handling

## Installation

### Prerequisites
- Python 3.6+
- pip package manager

### Install Dependencies
```bash
pip install flask reportlab
```

## Project Structure

```
AT-Commodities-Invoice-Generator/
├── standalone/                 # Standalone invoice generator
│   └── invoice_generator.py
├── webapp/                     # Web application files
│   ├── app.py                  # Flask application
│   ├── invoice_generator.py    # PDF generation module
│   ├── templates/
│   │   └── invoice.html        # HTML form template
│   └── static/
│       └── style.css           # CSS stylesheet
└── README.md                   # This file
```

## Usage

### Standalone Invoice Generator
1. Navigate to the standalone directory:
   ```bash
   cd standalone
   ```
2. Run the script:
   ```bash
   python invoice_generator.py
   ```
3. Follow the prompts to enter invoice details:
   - Invoice Number
   - Delivery Date (YYYY-MM-DD format)
   - Vehicle Number
   - Quantity (M/TON)
   - Unit Price (Rs)
4. View the text invoice in the console
5. Find the generated PDF in the same directory

### Web Application
1. Navigate to the webapp directory:
   ```bash
   cd webapp
   ```
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Open your browser and visit: http://localhost:5000
4. Fill out the form with invoice details
5. Click "Generate Invoice"
6. Download the generated PDF invoice

## Customization

### Company Information
To customize the company information, modify the following constants in both `invoice_generator.py` files:

```python
COMPANY_NAME = "A.T COMMODITIES"
ADDRESS = "C-2 WESTLAND TRADE CENTER, SHAHEED E MILLAT ROAD, KARACHI"
PHONE = "021-34381222"
WEBSITE = "www.atcommodities.pk"
```

### Customer Information
The customer information is currently hardcoded as:
```python
# In generate_pdf function
invoice_details = [
    ["Invoice for", "Mr. Talha Niazi Sb - Niazi Bricks"],
    # ... other details ...
]
```
To change this, modify the "Invoice for" field in the `generate_pdf` function.

### PDF Formatting
To adjust the PDF layout:
1. Modify column widths in the `generate_pdf` function
2. Adjust table styles
3. Change page orientation (currently landscape)

## Screenshots

### Standalone Application
![Standalone Invoice Generator](https://via.placeholder.com/600x400?text=Console+Invoice+Output)

### Web Application
![Web Form](https://via.placeholder.com/600x400?text=Invoice+Form)
![Generated PDF](https://via.placeholder.com/600x400?text=PDF+Invoice+Example)

## Technical Details

### Key Technologies
- Python 3
- Flask (web framework)
- ReportLab (PDF generation)
- HTML5/CSS3 (frontend)
- JavaScript (form handling)

### Features
- Landscape-oriented PDF invoices
- Professional formatting with proper alignment
- Amount conversion to words (English)
- Date formatting (DD-MMM-YYYY)
- Error handling in both CLI and web versions
- Responsive web design

## Troubleshooting

### Template Not Found Error
If you encounter `jinja2.exceptions.TemplateNotFound`:
1. Verify directory structure:
   ```
   webapp/
   ├── templates/
   │   └── invoice.html
   ```
2. Ensure you're running the app from the webapp directory
3. Check for correct file naming (case-sensitive)

### Date Format Issues
- Always enter dates in YYYY-MM-DD format
- The system will automatically convert to DD-MMM-YYYY format

### PDF Generation Issues
- Ensure ReportLab is installed: `pip install reportlab`
- Check file permissions in the output directory

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## Support

For any issues or questions, please open an issue on the GitHub repository.
