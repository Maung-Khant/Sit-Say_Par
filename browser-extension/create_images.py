from PIL import Image, ImageDraw, ImageFont

# Marquee tile 1400x560
width, height = 1400, 560
img = Image.new('RGB', (width, height), color='#2c3e50')
draw = ImageDraw.Draw(img)

try:
    font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    font_mid = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
except:
    font_big = ImageFont.load_default()
    font_mid = ImageFont.load_default()

text1 = "Sit-Say Par"
text2 = "Explainable Myanmar Phishing URL Risk Assessment"

bbox1 = draw.textbbox((0,0), text1, font=font_big)
w1 = bbox1[2] - bbox1[0]
draw.text(((width - w1)//2, 150), text1, fill='white', font=font_big)

bbox2 = draw.textbbox((0,0), text2, font=font_mid)
w2 = bbox2[2] - bbox2[0]
draw.text(((width - w2)//2, 300), text2, fill='#ecf0f1', font=font_mid)

img.save('marquee_promo_tile_1400x560.png')
print("Marquee promo tile created: marquee_promo_tile_1400x560.png")
