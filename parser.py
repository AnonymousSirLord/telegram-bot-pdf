import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def parse_rate_info(text):
    import re
    info = {}
    info['Rate'] = re.findall(r'\$\s?\d+(?:,\d+)?(?:\.\d{2})?', text)
    info['Pickup Date'] = re.findall(r'Pickup(?: Date)?:?\s*(\d{1,2}/\d{1,2}/\d{2,4})', text, re.I)
    info['Delivery Date'] = re.findall(r'Delivery(?: Date)?:?\s*(\d{1,2}/\d{1,2}/\d{2,4})', text, re.I)
    info['Origin'] = re.findall(r'Shipper(?: Name)?:?\s*(.*)', text)
    info['Destination'] = re.findall(r'Consignee(?: Name)?:?\s*(.*)', text)
    return info
