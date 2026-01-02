# Email Configuration Guide

This guide explains how to set up email credentials for appointment notifications.

## Option 1: Gmail (Recommended for Development/Testing)

### Step 1: Enable 2-Step Verification
1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to **Security** → **2-Step Verification**
3. Enable 2-Step Verification if not already enabled

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select **Mail** as the app
3. Select **Other (Custom name)** as the device
4. Enter a name like "Monalisa Clinic Backend"
5. Click **Generate**
6. **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)

### Step 3: Set Environment Variables
- **EMAIL_HOST_USER**: Your Gmail address (e.g., `yourname@gmail.com`)
- **EMAIL_HOST_PASSWORD**: The 16-character app password (remove spaces: `abcdefghijklmnop`)

## Option 2: Other Email Providers

### SendGrid (Recommended for Production)
1. Sign up at https://sendgrid.com/
2. Create an API Key:
   - Go to Settings → API Keys
   - Create a new API key with "Mail Send" permissions
3. Update settings:
   ```
   EMAIL_HOST = 'smtp.sendgrid.net'
   EMAIL_PORT = 587
   EMAIL_HOST_USER = 'apikey'
   EMAIL_HOST_PASSWORD = 'your_sendgrid_api_key'
   EMAIL_USE_TLS = True
   ```

### Outlook/Office 365
1. Use your Office 365 email
2. Generate an app password:
   - Go to https://account.microsoft.com/security
   - Security → Advanced security options → App passwords
3. Settings:
   ```
   EMAIL_HOST = 'smtp.office365.com'
   EMAIL_PORT = 587
   EMAIL_HOST_USER = 'your_email@outlook.com'
   EMAIL_HOST_PASSWORD = 'your_app_password'
   EMAIL_USE_TLS = True
   ```

### Custom SMTP Server
If you have your own email server:
```
EMAIL_HOST = 'smtp.yourdomain.com'
EMAIL_PORT = 587  # or 465 for SSL
EMAIL_HOST_USER = 'noreply@yourdomain.com'
EMAIL_HOST_PASSWORD = 'your_password'
EMAIL_USE_TLS = True  # Use False if using port 465 with SSL
```

## Setting Environment Variables in Railway

1. Go to your Railway project dashboard
2. Click on your service
3. Go to **Variables** tab
4. Add the following environment variables:
   - `EMAIL_HOST_USER` = your email address
   - `EMAIL_HOST_PASSWORD` = your app password or API key
   - `OWNER_EMAIL` = email address to receive appointment notifications

## Setting Environment Variables Locally

Create a `.env` file in the `MonalisaWellness` directory:

```env
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password_here
OWNER_EMAIL=owner@monalisawellness.com
```

**Important**: Add `.env` to `.gitignore` to keep credentials secure!

## Testing Email Configuration

After setting up, test the email configuration:

```python
# In Django shell: python manage.py shell
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email',
    'This is a test email from Monalisa Clinic.',
    settings.DEFAULT_FROM_EMAIL,
    [settings.OWNER_EMAIL],
    fail_silently=False,
)
```

## Troubleshooting

### "Authentication failed" error
- Make sure you're using an **App Password**, not your regular Gmail password
- Verify 2-Step Verification is enabled
- Check that the app password was copied correctly (no spaces)

### "Connection timeout" error
- Check firewall settings
- Verify EMAIL_HOST and EMAIL_PORT are correct
- Try using port 465 with SSL instead of 587 with TLS

### Emails going to spam
- Use a professional email service (SendGrid, Mailgun) for production
- Set up SPF and DKIM records for your domain
- Use a proper "From" email address
