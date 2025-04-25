import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

def generate_custom_qr(data, initials="AC", 
                      color_black="#000000", color_white="#FFFFFF", 
                      box_size=10, border=4):
    """
    Generate a QR code with custom initials in the center
    
    Args:
        data: The data to encode in the QR code
        initials: Text to display in the center (default: AC)
        color_black: Color for the QR code modules (default: black)
        color_white: Background color (default: white)
        box_size: Size of each QR code module
        border: Border size in modules
    
    Returns:
        Base64 encoded image data
    """
    # Generate the QR code
    qr = qrcode.QRCode(
        version=None,  # Auto-determine version for data
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Highest error correction for logo space
        box_size=box_size,
        border=border
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create the QR code image
    qr_img = qr.make_image(fill_color=color_black, back_color=color_white)
    
    # Convert to RGB mode if it's not already
    if qr_img.mode != 'RGB':
        qr_img = qr_img.convert('RGB')
    
    # Get QR code dimensions
    qr_width, qr_height = qr_img.size
    
    # Create a drawing context
    draw = ImageDraw.Draw(qr_img)
    
    # Determine font size (proportional to QR size)
    font_size = int(min(qr_width, qr_height) * 0.15)
    
    # Try to load a nice font, fall back to default if not available
    try:
        font = ImageFont.truetype("Arial Bold.ttf", font_size)
    except IOError:
        try:
            # Try another common font
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except IOError:
            # Fall back to default font
            font = ImageFont.load_default()
            font_size = int(min(qr_width, qr_height) * 0.1)  # Adjust for default font
    
    # Calculate text size
    if hasattr(draw, 'textsize'):
        text_width, text_height = draw.textsize(initials, font=font)
    else:
        # For newer Pillow versions
        bbox = font.getbbox(initials)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Calculate center position
    x = (qr_width - text_width) // 2
    y = (qr_height - text_height) // 2
    
    # Create a white or background color for the text
    padding = int(font_size * 0.5)
    draw.rectangle(
        [(x - padding, y - padding), (x + text_width + padding, y + text_height + padding)],
        fill=color_white
    )
    
    # Draw the text with the QR color
    draw.text((x, y), initials, font=font, fill=color_black)
    
    # Save to a bytes buffer instead of file
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    
    # Convert to base64 for embedding in HTML
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return f"data:image/png;base64,{img_str}"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.get('data', 'https://example.com')
    initials = request.form.get('initials', 'AC')
    color_black = request.form.get('color_black', '#000000')
    color_white = request.form.get('color_white', '#FFFFFF')
    box_size = int(request.form.get('box_size', 10))
    border = int(request.form.get('border', 4))
    
    img_data = generate_custom_qr(
        data=data,
        initials=initials,
        color_black=color_black,
        color_white=color_white,
        box_size=box_size,
        border=border
    )
    
    return jsonify({'image': img_data})

# Remove the if __name__ == '__main__' block
# Vercel needs the app variable to be directly accessible
