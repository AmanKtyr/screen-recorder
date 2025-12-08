#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create a new logo for the screen recorder application.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_logo(output_path, size=(128, 128), bg_color=(76, 175, 80), text="SR", text_color=(255, 255, 255)):
    """Create a simple logo with text."""
    # Create a new image with a green background
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)

    # Try to use a font
    try:
        # Try to use Arial or a default system font
        font_size = size[0] // 2
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()

        # Calculate text position to center it
        try:
            # For newer Pillow versions
            left, top, right, bottom = font.getbbox(text)
            text_width, text_height = right - left, bottom - top
        except AttributeError:
            try:
                # For older Pillow versions
                text_width, text_height = draw.textsize(text, font=font)
            except:
                # Fallback
                text_width, text_height = font_size, font_size

        position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)

        # Draw the text
        draw.text(position, text, font=font, fill=text_color)
    except Exception as e:
        print(f"Error adding text to logo: {e}")
        # Fallback - draw a simple circle
        draw.ellipse([(10, 10), (size[0] - 10, size[1] - 10)], fill=text_color)

    # Save the image
    try:
        img.save(output_path, 'PNG')
        print(f"Logo created successfully at {output_path}")
        return True
    except Exception as e:
        print(f"Error saving logo: {e}")
        return False

if __name__ == "__main__":
    # Create the static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)

    # Create the logo
    create_logo("static/logo.png")

    # Create a theme icon (simple light/dark toggle icon)
    theme_size = (64, 64)
    theme_img = Image.new('RGBA', theme_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(theme_img)

    # Draw a half-filled circle (half light, half dark)
    draw.ellipse([(4, 4), (theme_size[0] - 4, theme_size[1] - 4)], outline=(100, 100, 100, 255), width=2)
    draw.pieslice([(4, 4), (theme_size[0] - 4, theme_size[1] - 4)], 0, 180, fill=(50, 50, 50, 255))
    draw.pieslice([(4, 4), (theme_size[0] - 4, theme_size[1] - 4)], 180, 360, fill=(220, 220, 220, 255))

    # Save the theme icon
    theme_img.save("static/theme_icon.png", 'PNG')
    print(f"Theme icon created successfully at static/theme_icon.png")
