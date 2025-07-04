# Configuration file for MonalisaWellness Django Backend
# Replace these values with your actual credentials
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Database Configuration
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')

# AWS S3 Configuration
# Get these from your AWS Console > IAM > Users > Your User > Security credentials
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Create an S3 bucket in your AWS Console and put the name here
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

# Django Settings
# SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = 'django-insecure-fallback-key'
# DEBUG = os.getenv('DEBUG')
DEBUG = os.getenv('DEBUG')
ALLOWED_HOSTS = ['*']

# Email Configuration (for appointment notifications)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
EMAIL_USE_TLS = True
OWNER_EMAIL = 'owner@monalisawellness.com' 