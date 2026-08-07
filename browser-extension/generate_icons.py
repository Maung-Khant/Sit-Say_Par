# generate_icons.py
from PIL import Image, ImageDraw, ImageFont

def create_icon(size, text="S"):
    # Create a dark blue background
    img = Image.new('RGBA', (size, size), (44, 62, 80, 255))  # #2c3e50
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font (may vary by OS)
    try:
        # For Linux, use a truetype font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=int(size*0.6))
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw white "S" in center
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1]
    draw.text((x, y), text, fill="white", font=font)
    
    return img

# Generate three sizes
for size in [16, 48, 128]:
    icon = create_icon(size, "S")
    icon.save(f'icons/icon{size}.png')

print("Icons generated successfully.")# generate_icons.py
from PIL import Image

# Create a simple blue square icon for 16, 48, 128 sizes
sizes = [16, 48, 128]
for size in sizes:
    img = Image.new('RGB', (size, size), color='#2c3e50')
    img.save(f'icons/icon{size}.png')
