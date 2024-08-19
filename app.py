from flask import Flask, render_template, request, send_file
import requests
from cryptography.fernet import Fernet
import os
import time
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle

app = Flask(__name__)

API_KEY_FILE = "apikey.txt"
KEY_FILE = "secret.key"
PSYCHO_PROFILE_URL = "https://irbis.espysys.com/api/developer/psycho_profile"
RESULTS_URL_TEMPLATE = "https://irbis.espysys.com/api/request-monitor/api-usage/{}?key={}"

# Encryption key generation/loading functions
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    return open(KEY_FILE, 'rb').read()

def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()

# Retrieve the stored API key
def get_stored_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'rb') as file:
            encrypted_key = file.read()
            return decrypt_message(encrypted_key)
    return None

# Store a new API key
def store_api_key(api_key):
    encrypted_key = encrypt_message(api_key)
    with open(API_KEY_FILE, 'wb') as file:
        file.write(encrypted_key)

# Validate the API key by making a test request
def validate_api_key(api_key):
    response = requests.get(
        f"https://irbis.espysys.com/api/request-monitor/credit-stat?key={api_key}",
        headers={"Content-Type": "application/json"}
    )
    return response.status_code == 200

# Trigger the psycho profile lookup
def trigger_psycho_profile(api_key, facebook_id):
    payload = {
        "key": api_key,
        "lookupType": "PSYCH",
        "value": facebook_id,
        "lookupId": 180
    }
    response = requests.post(PSYCHO_PROFILE_URL, headers={"Content-Type": "application/json"}, json=payload)
    if response.status_code == 201:
        return response.json().get('id')
    return None

# Poll for results until analysis is complete
def poll_for_results(api_key, lookup_id):
    url = RESULTS_URL_TEMPLATE.format(lookup_id, api_key)
    status = "progress"
    
    while status != "FINISHED":
        response = requests.get(url, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            print(f"API response received: {json.dumps(data, indent=2)}")  # Debug message for the full API response
            if 'data' in data and len(data['data']) > 0:
                status = data['data'][0]['status']
                if status == "FINISHED":
                    print("Profile analysis completed. Retrieving final data...")
                    time.sleep(10)
                    final_response = requests.get(url, headers={"Content-Type": "application/json"})
                    final_data = final_response.json()
                    print(f"Final API response received: {json.dumps(final_data, indent=2)}")  # Debug message for final API response
                    if 'data' in final_data and len(final_data['data']) > 0:
                        print("Final data retrieved.")
                        return final_data['data'][0]['psychAnalyst']['profiles'][0], final_data['data'][0]['psychAnalyst'].get('image', '')
        print(f"Current status: {status}. Polling again in 10 seconds...")
        time.sleep(10)  # Poll every 10 seconds
    return None, None

@app.route('/')
def home():
    print("Rendering home page.")
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    test_mode = False
    if test_mode:
        try:
            print("Test mode: Loading test JSON.")
            with open('test_response.json', 'r') as f:
                response_data = json.load(f)
                profile_result = response_data['data'][0]['psychAnalyst']['profiles'][0]
                image_url = response_data['data'][0]['psychAnalyst'].get('image', '')
                print(f"Test mode image URL: {image_url}")  # Debug for test mode
        except Exception as e:
            print(f"Error loading test JSON: {str(e)}")
            return f"Error loading test JSON: {str(e)}", 500
    else:
        facebook_id = request.form['facebook_id']
        print(f"Received Facebook ID: {facebook_id}")
        api_key = get_stored_api_key()
        if not api_key:
            print("API key not found.")
            return "API key not found. Please set your API key in the settings.", 400

        print("Triggering psycho profile lookup...")
        lookup_id = trigger_psycho_profile(api_key, facebook_id)
        if not lookup_id:
            print("Failed to initiate profile lookup.")
            return "Failed to initiate profile lookup. Please try again.", 500

        print(f"Profile lookup initiated. Lookup ID: {lookup_id}")
        profile_result, image_url = poll_for_results(api_key, lookup_id)
        if not profile_result:
            print("Profile analysis failed.")
            return "Profile analysis failed. Please try again later.", 500
        
        print(f"Image URL retrieved: {image_url}")

    # Prepare result with emojis, colored danger level, and profile picture
    name = profile_result.get('personName', 'Name not available')
    print(f"Person name: {name}")
    psycho_portrait = profile_result.get('psychologicalPortrait', 'No data available')
    danger_level = profile_result.get('levelOfDanger', 'No data available')
    characteristics = profile_result.get('predictedCharacteristics', [])

    # Store profile data in the session for PDF export
    profile_data = {
        "name": name,
        "psycho_portrait": psycho_portrait,
        "danger_level": danger_level,
        "characteristics": characteristics,
        "image_url": image_url
    }
    with open('profile_data.json', 'w') as f:
        json.dump(profile_data, f)

    formatted_output = f"""
    <div style="display: flex; align-items: flex-start;">
        <div style="margin-right: 20px; width: 200px;">
            <img src="{image_url}" alt="Profile Picture" style="width: 200px; height: 200px; border-radius: 50%; object-fit: cover;" onerror="this.src='/static/default_profile.png';">
        </div>
        <div>
            <span style="font-size: 28px; font-weight: bolder;">{name}</span><br><br>
            <strong>🧠 PsychoPortrait:</strong><br>
            <p style="text-align: left;">{psycho_portrait}</p><br>
            <strong>⚠️ Level Of Danger:</strong> <span style='color: {"green" if danger_level.lower() == "low" else "red"};'>{danger_level}</span><br><br>
            <strong>🔍 Predicted Characteristics:</strong><br>
            <ul style="text-align: left;">
            {"".join([f"<li>{c}</li>" for c in characteristics])}
            </ul>
        </div>
    </div>
    <div style="text-align: right; margin-top: 20px;">
        <a href="/export" class="btn btn-primary" style="background-color: #007bff; color: white; text-decoration: none; padding: 10px 20px; border-radius: 5px;">Export to PDF</a>
    </div>
    """

    return formatted_output

@app.route('/export')
def export_pdf():
    # Load profile data from the session (or a file in this case)
    with open('profile_data.json', 'r') as f:
        profile_data = json.load(f)

    return export_to_pdf(
        profile_data['name'],
        profile_data['psycho_portrait'],
        profile_data['danger_level'],
        profile_data['characteristics'],
        profile_data['image_url']
    )

def export_to_pdf(name, psycho_portrait, danger_level, characteristics, image_url):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Add a custom style for the title
    title_style = ParagraphStyle(
        'Title',
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=colors.blue,
        alignment=1,  # Center align
    )

    # Add a custom style for the subtitles
    subtitle_style = ParagraphStyle(
        'Subtitle',
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=colors.black,
    )

    # Add a custom style for the text
    text_style = ParagraphStyle(
        'Text',
        fontName="Helvetica",
        fontSize=12,
        textColor=colors.black,
    )

    # Elements list to hold the components of the PDF
    elements = []

    # Logo and App Name as a single row (to align on the same line)
    logo_path = "static/icon.png"  # Assuming you have a logo image in your static folder
    if os.path.exists(logo_path):
        # Adding the logo and title in a table to align them horizontally
        logo = RLImage(logo_path, 0.8*inch, 0.8*inch)
        title = Paragraph("PersonaAI", title_style)
        table_data = [[logo, title]]
        table = Table(table_data, colWidths=[1*inch, 4*inch])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))
    else:
        elements.append(Paragraph("PersonaAI", title_style))
        elements.append(Spacer(1, 20))

    # Add profile image if available, and move it to the left
    if image_url:
        elements.append(RLImage(image_url, 2*inch, 2*inch))
        elements.append(Spacer(1, 20))

    # Add Name
    elements.append(Paragraph(f"<b>{name}</b>", subtitle_style))
    elements.append(Spacer(1, 12))

    # Add PsychoPortrait with extra space
    elements.append(Paragraph(f"🧠 <b>PsychoPortrait:</b>", subtitle_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(psycho_portrait, text_style))
    elements.append(Spacer(1, 12))

    # Add Level of Danger
    elements.append(Paragraph(f"⚠️ <b>Level Of Danger:</b> <span color='{colors.green if danger_level.lower() == 'low' else colors.red}'>{danger_level}</span>", subtitle_style))
    elements.append(Spacer(1, 12))

    # Add Predicted Characteristics
    elements.append(Paragraph(f"🔍 <b>Predicted Characteristics:</b>", subtitle_style))
    elements.append(Spacer(1, 6))
    for characteristic in characteristics:
        elements.append(Paragraph(f"- {characteristic}", text_style))

    # Build the PDF
    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="profile_report.pdf", mimetype='application/pdf')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        api_key = request.form.get('apikey')
        if api_key:
            if validate_api_key(api_key):
                store_api_key(api_key)
                message = "API key saved successfully!"
                message_type = "alert-success"  # Bootstrap class for success
            else:
                message = "Invalid API key. Please try again."
                message_type = "alert-danger"  # Bootstrap class for error
        else:
            message = "API key is required."
            message_type = "alert-danger"

        return render_template('settings.html', api_key=api_key, message=message, message_type=message_type)

    # GET request or no API key submitted
    api_key = get_stored_api_key() or ""
    return render_template('settings.html', api_key=api_key)

if __name__ == '__main__':
    app.run(debug=True)
