import pdfplumber
import re

def parse_rate_confirmation(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(page.extract_text() for page in pdf.pages)

    data = {}

    # Basic Fields
    data["Rate Confirmation Date"] = re.search(r'Date:\s*(\d{1,2}-\w+-\d{4})', full_text).group(1)
    data["Carrier Name"] = re.search(r'Carrier Name\s+(.*?)\s', full_text).group(1)
    data["Carrier Phone"] = re.search(r'Carrier #.*?\((\d{3}\)\d{3}-\d{4})', full_text).group(1)
    data["Carrier Email"] = re.search(r'Carrier Email\s+(\S+@\S+)', full_text).group(1)
    data["Driver Name"] = re.search(r'Driver Name\s+(.*?)\s', full_text).group(1)
    data["Driver Phone"] = re.search(r'Driver Name.*?\((\d{3}\)\d{3}-\d{4})', full_text).group(1)
    data["Carrier Pay"] = re.search(r'Carrier Pay\s+\$(\d+(?:,\d{3})*(?:\.\d{2}))', full_text).group(1)

    # Load Info
    data["Commodity"] = re.search(r'Commodity:\s*(.*?)\n', full_text).group(1)
    data["Weight"] = re.search(r'Weight\s+(\d+)', full_text).group(1)
    data["Equipment"] = re.search(r'Equipment:\s*(.*?)\n', full_text).group(1)

    # Pickup Info
    pickup_match = re.search(r'PRECOAT METALS\n(.*?)\n(.*?)\n(\d{2}-\w+-\d{4}.*?)\n', full_text)
    if pickup_match:
        data["Pickup Company"] = "PRECOAT METALS"
        data["Pickup Address"] = pickup_match.group(1) + ", " + pickup_match.group(2)
        data["Pickup Time Window"] = pickup_match.group(3)

    # Delivery Info
    delivery_match = re.search(r'CARLISLE ARCHITECTURAL METALS\n(.*?)\n(.*?)\n(\d{2}-\w+-\d{4}.*?)\n', full_text)
    if delivery_match:
        data["Delivery Company"] = "CARLISLE ARCHITECTURAL METALS"
        data["Delivery Address"] = delivery_match.group(1) + ", " + delivery_match.group(2)
        data["Delivery Time Window"] = delivery_match.group(3)

    # ACE Load Number
    ace_order_match = re.search(r'Ace Order #:\s*\n\s*(\d+)', full_text)
    if ace_order_match:
        data["ACE Order #"] = ace_order_match.group(1)

    return data


# Example usage
pdf_file = "431.pdf"  # Replace with your file path
result = parse_rate_confirmation(pdf_file)

# Print result
for key, value in result.items():
    print(f"{key}: {value}")
