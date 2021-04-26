from django.conf import settings

VALID_EXCEL_UPLOAD_DIR = getattr(settings, 'WEB_TOOLS_VALID_EXCEL_UPLOAD_DIR')
NUM_ERROR_LIMIT = getattr(settings, 'WEB_TOOLS_NUM_ERROR_LIMIT', 100)