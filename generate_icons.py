from PIL import Image, ImageDraw, ImageFont

def create_icon(size, text="S"):
    img = Image.new('RGBA', (size, size), (44, 62, 80, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=int(size*0.6))
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1]
    draw.text((x, y), text, fill="white", font=font)
    return img

for size in [16, 48, 128]:
    icon = create_icon(size, "S")
    icon.save(f'icons/icon{size}.png')
