import numpy as np
from PIL import Image

# Create a simple logo - a green square
logo_size = 128
logo = np.zeros((logo_size, logo_size, 3), dtype=np.uint8)
logo[:, :] = [76, 175, 80]  # Green color (RGB)

# Add a white circle in the middle
center = logo_size // 2
radius = logo_size // 3
y, x = np.ogrid[:logo_size, :logo_size]
dist_from_center = np.sqrt((x - center)**2 + (y - center)**2)
circle = dist_from_center <= radius
logo[circle] = [255, 255, 255]  # White color

# Save the logo
img = Image.fromarray(logo)
img.save('static/logo.png')
print("Logo created successfully!")

# Create a simple theme icon
theme_size = 64
theme_icon = np.zeros((theme_size, theme_size, 4), dtype=np.uint8)
theme_icon[:, :] = [0, 0, 0, 0]  # Transparent background

# Draw a circle outline
center = theme_size // 2
radius = theme_size // 2 - 4
y, x = np.ogrid[:theme_size, :theme_size]
dist_from_center = np.sqrt((x - center)**2 + (y - center)**2)
circle_outline = (radius - 2 <= dist_from_center) & (dist_from_center <= radius)
theme_icon[circle_outline] = [100, 100, 100, 255]  # Gray outline

# Fill half with dark color
half_circle = (dist_from_center <= radius) & (y <= center)
theme_icon[half_circle] = [50, 50, 50, 255]  # Dark gray

# Fill other half with light color
half_circle = (dist_from_center <= radius) & (y > center)
theme_icon[half_circle] = [220, 220, 220, 255]  # Light gray

# Save the theme icon
theme_img = Image.fromarray(theme_icon, 'RGBA')
theme_img.save('static/theme_icon.png')
print("Theme icon created successfully!")
