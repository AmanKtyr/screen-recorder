from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import random

def create_default_profile_image(username):
    """Create a default profile image with the user's initials"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.join(settings.MEDIA_ROOT), exist_ok=True)

    # Create a default profile image with the user's initials
    size = 300
    img = Image.new('RGB', (size, size), color=(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)))
    draw = ImageDraw.Draw(img)

    # Try to use a font, or use default if not available
    try:
        font = ImageFont.truetype("arial.ttf", size//3)
    except IOError:
        font = ImageFont.load_default()

    # Get initials
    if username:
        initials = username[0].upper()
    else:
        initials = "U"

    # Draw text
    try:
        # For newer versions of PIL
        if hasattr(font, 'getbbox'):
            bbox = font.getbbox(initials)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        # For older versions of PIL
        elif hasattr(draw, 'textsize'):
            text_width, text_height = draw.textsize(initials, font=font)
        else:
            text_width, text_height = size//3, size//3

        draw.text(
            ((size-text_width)//2, (size-text_height)//2),
            initials,
            font=font,
            fill=(255, 255, 255)
        )
    except Exception as e:
        # Fallback to simple centered text
        draw.text(
            (size//3, size//3),
            initials,
            font=font,
            fill=(255, 255, 255)
        )

    # Save the image
    default_path = os.path.join(settings.MEDIA_ROOT, 'default.jpg')
    img.save(default_path)
    return default_path

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a Profile when a new User is created"""
    if created:
        # Create default profile image if it doesn't exist
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'default.jpg')):
            create_default_profile_image(instance.username)

        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Save the Profile when the User is saved"""
    instance.profile.save()
