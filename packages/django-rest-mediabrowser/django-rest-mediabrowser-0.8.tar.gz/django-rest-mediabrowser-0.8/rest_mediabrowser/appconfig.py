from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage

MB_ROOT = getattr(settings, 'MEDIA_BROWSER_ROOT',
                  os.path.join(settings.BASE_DIR, 'mediabrowser_files'))

MB_STORAGE = FileSystemStorage(location=MB_ROOT)
MEDIA_BROWSER_AUTH_FUNCTION = 'rest_mediabrowser.utils.default_auth'
MB_THUMBNAIL_FORMAT = getattr(
    settings, 'MEDIA_BROWSER_THUMBNAIL_FORMAT', 'WEBP')
