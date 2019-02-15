
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_PATH = os.path.join(BASE_DIR, 'static')

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

MEDIA_PATH = os.path.join(STATIC_PATH, 'media')
