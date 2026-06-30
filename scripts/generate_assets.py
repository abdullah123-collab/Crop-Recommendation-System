from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('assets', exist_ok=True)

logo = Image.new('RGB', (400, 400), (255, 255, 255))
draw = ImageDraw.Draw(logo)
draw.ellipse((50, 50, 350, 350), fill=(142, 197, 61), outline=(60, 122, 29), width=12)
draw.rectangle((170, 120, 230, 320), fill=(255, 255, 255))
draw.polygon([(150, 180), (250, 180), (200, 80)], fill=(255, 255, 255))
logo.save('assets/logo.png')

banner = Image.new('RGB', (1400, 500), (237, 247, 237))
draw = ImageDraw.Draw(banner)
for i in range(0, 1400, 140):
    draw.ellipse((i, 340, i + 80, 420), fill=(142, 197, 61, 255))
    draw.ellipse((i + 70, 330, i + 150, 410), fill=(80, 170, 55, 255))

try:
    font = ImageFont.truetype('arial.ttf', 48)
except Exception:
    font = ImageFont.load_default()

text = 'AI Crop Advisor'
draw.text((60, 120), text, fill=(34, 83, 32), font=font)
draw.text((60, 190), 'Smart crop recommendations powered by soil, weather, and machine learning.', fill=(65, 95, 51), font=font)

banner.save('assets/banner.jpg', quality=85)
