# Place this in /web/static/images/ directory as create_logo.py
# Run: python create_logo.py

from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    """Create a simple logo for the spam detector"""
    # Create image
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw circle background
    draw.ellipse((20, 20, 180, 180), fill='#6c5ce7')
    
    # Add text
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 60)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 70), '📧', fill='white', font=font)
    draw.text((30, 140), 'SPAM', fill='white', font=ImageFont.load_default())
    
    # Save
    img.save('logo.png')
    print("Logo created successfully!")

if __name__ == '__main__':
    create_logo()