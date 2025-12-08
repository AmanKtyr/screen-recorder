import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_screen_recorder.settings')
django.setup()

from users.signals import create_default_profile_image

if __name__ == "__main__":
    # Create default profile image
    default_path = create_default_profile_image("U")
    print(f"Default profile image created at: {default_path}")
