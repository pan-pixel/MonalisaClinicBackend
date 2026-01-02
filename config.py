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
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = ['*']

# Email Configuration (for appointment notifications)
# 
# For Gmail:
# 1. Enable 2-Step Verification: https://myaccount.google.com/security
# 2. Generate App Password: https://myaccount.google.com/apppasswords
# 3. Use the 16-character app password (not your regular password)
#
# Set these via environment variables:
# - EMAIL_HOST_USER: Your email address (e.g., 'yourname@gmail.com')
# - EMAIL_HOST_PASSWORD: Your app password (16 characters, no spaces)
# - OWNER_EMAIL: Email to receive appointment notifications
#
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
# SSL Certificate Verification
# Set to 'False' for development/local (fixes macOS SSL certificate issues)
# Set to 'True' for production (recommended)
EMAIL_SSL_VERIFY = os.getenv('EMAIL_SSL_VERIFY', 'False').lower() == 'true'
OWNER_EMAIL = os.getenv('OWNER_EMAIL', 'owner@monalisawellness.com') 