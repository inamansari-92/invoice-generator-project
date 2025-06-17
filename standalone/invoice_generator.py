from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import os

# Fixed company information
COMPANY_NAME = "A.T COMMODITIES"
ADDRESS = "C-2 WESTLAND TRADE CENTER, SHAHEED E MILLAT ROAD, KARACHI"
PHONE = "021-34381222"
WEBSITE = "www.atcommodities.pk"

def number_to_words(num):
    """Convert number to words (improved for large numbers)"""
    # Convert to integer for words
    n = int(round(num))
    
    if n == 0:
        return "Zero"
    
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", 
             "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    
    def convert_below_thousand(n):
        if n == 0:
            return ""
        elif n < 10:
            return units[int(n)]
        elif n < 20:
            return teens[int(n)-10]
        elif n < 100:
            return tens[int(n//10)] + (" " + units[int(n%10)] if n%10 !=0 else "")
        else:
            return units[int(n//100)] + " Hundred" + (" and " + convert_below_thousand(n%100) if n%100 !=0 else "")
    
    # Handle millions
    result = ""
    if n >= 1000000:
        millions = n // 1000000
        result += convert_below_thousand(millions) + " Million "
        n %= 1000000
    
    # Handle thousands
    if n >= 1000:
        thousands = n // 1000
        result += convert_below_thousand(thousands) + " Thousand "
        n %= 1000
    
    # Handle hundreds and below
    if n > 0:
        result += convert_below_thousand(n)
    
    return result.strip()

def format_date(date_str):
    """Convert date from YYYY-MM-DD to DD-MMM-YYYY format"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d-%b-%Y")
    except ValueError:
        return date_str  # Return original if format is invalid

def generate_pdf(invoice_number, delivery_date, vehicle_number, quantity, unit_price, total_price):
    # Format delivery date
    formatted_date = format_date(delivery_date)
    
    # Create PDF document in landscape orientation
    filename = f"Invoice_{invoice_number}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
    
    # Create story
    story = []
    styles = getSampleStyleSheet()
    
    # Company header - centered
    company_info = [
        [COMPANY_NAME],
        [ADDRESS],
        [f"Phone: {PHONE}"],
        [f"Website: {WEBSITE}"]
    ]
    
    # Invoice details
    invoice_details = [
        ["Invoice for", "Mr. Talha Niazi Sb - Niazi Bricks"],
        ["Payable to", COMPANY_NAME],
        ["Invoice #", invoice_number]
    ]
    
    # Item table
    item_data = [
        ["Description", "Delivery Date", "Qty (M/TON)", "Unit price", "Total price"],
        [f"Coal ({vehicle_number})", formatted_date, f"{quantity:.3f}", f"Rs{unit_price:,.2f}", f"Rs{total_price:,.2f}"]
    ]
    
    # Convert total to integer for words
    total_rupees = round(total_price)
    amount_in_words = number_to_words(total_rupees) + " Rupees Only"
    
    # Create a paragraph for the amount in words to enable wrapping
    word_style = ParagraphStyle(
        name='Normal',
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        wordWrap='LTR'
    )
    amount_paragraph = Paragraph(amount_in_words, word_style)
    
    # Summary
    summary = [
        ["Total Amount:", f"Rs{total_price:,.2f}"],
        ["Amount in Words:", amount_paragraph]
    ]
    
    # Create tables with adjusted column widths for landscape
    company_table = Table(company_info, colWidths=[700])  # Wider column for landscape
    invoice_table = Table(invoice_details, colWidths=[200, 500])
    item_table = Table(item_data, colWidths=[250, 100, 100, 100, 150])
    summary_table = Table(summary, colWidths=[200, 500])
    
    # Apply styles
    company_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (0,0), 14),
        ('BOTTOMPADDING', (0,0), (0,0), 12),
    ]))
    
    invoice_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 10),
    ]))
    
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (2,1), (4,1), 'RIGHT'),
    ]))
    
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (0,0), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEABOVE', (0,0), (-1,0), 1, colors.black),
        ('LINEABOVE', (0,1), (-1,1), 1, colors.black),
        # Special handling for amount in words cell
        ('VALIGN', (1,1), (1,1), 'TOP'),
        ('LEFTPADDING', (1,1), (1,1), 5),
        ('RIGHTPADDING', (1,1), (1,1), 5),
        ('TOPPADDING', (1,1), (1,1), 2),
        ('BOTTOMPADDING', (1,1), (1,1), 5),
    ]))
    
    # Add elements to story
    story.append(company_table)
    story.append(Spacer(1, 0.25*inch))
    story.append(invoice_table)
    story.append(Spacer(1, 0.25*inch))
    story.append(item_table)
    story.append(Spacer(1, 0.25*inch))
    story.append(summary_table)
    
    # Build PDF
    doc.build(story)
    return os.path.abspath(filename)

def generate_invoice():
    # Get user inputs
    invoice_number = input("Enter Invoice Number: ")
    delivery_date = input("Enter Delivery Date (YYYY-MM-DD): ")
    vehicle_number = input("Enter Vehicle Number: ")
    quantity = float(input("Enter Quantity (M/TON): "))
    unit_price = float(input("Enter Unit Price (Rs): "))
    
    # Calculate total
    total_price = quantity * unit_price
    
    # Format delivery date for display
    formatted_date = format_date(delivery_date)
    
    # Print text invoice
    print("\n" + "="*60)
    print(f"{COMPANY_NAME:^60}")
    print(f"{ADDRESS:^60}")
    print(f"Phone: {PHONE:^50}")
    print(f"Website: {WEBSITE:^50}")
    print("="*60)
    print(f"Invoice for: Mr. Talha Niazi Sb - Niazi Bricks")
    print(f"Payable to: {COMPANY_NAME}")
    print(f"Invoice #: {invoice_number}")
    print("-"*60)
    print(f"{'Description':<20}{'Delivery Date':<15}{'Qty (M/TON)':>12}{'Unit Price':>12}{'Total Price':>15}")
    print(f"{'Coal (' + vehicle_number + ')':<20}{formatted_date:<15}{quantity:>12.3f}{unit_price:>12,.2f}{total_price:>15,.2f}")
    print("-"*60)
    print(f"Total: Rs{total_price:,.2f}")
    print("="*60)
    print(f"\nAmount in Words: {number_to_words(total_price)} Rupees Only\n")
    
    # Generate PDF
    generate_pdf(invoice_number, delivery_date, vehicle_number, quantity, unit_price, total_price)

if __name__ == '__main__':
    generate_invoice()