import numpy as np
from PIL import Image, ImageDraw, ImageFont

def render_overlay(topLine, bottomLine):
  res = (600, 600)
  overlay = np.zeros((res[0],res[1], 4), dtype=np.uint8)
  overlay_image = Image.fromarray(overlay)
  draw = ImageDraw.Draw(overlay_image)
  font = ImageFont.load_default()  

  draw.rectangle([0, 0, res[0], 12], fill=(44, 44, 44, 200))
  draw.rectangle([0, res[1] - 12, res[0], res[1]], fill=(44, 44, 44, 200))


  draw.text((0, 0), topLine, font=font, fill=(155, 200, 255, 255))  # White text
  draw.text((0, res[1] - 12), bottomLine, font=font, fill=(155, 200, 255, 255))  # White text
    
  overlay = np.array(overlay_image)

  return overlay

