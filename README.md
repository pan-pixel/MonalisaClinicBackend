# Monalisa Wellness - Skincare Clinic Backend

A comprehensive Django REST API backend for a skincare clinic website with a beautiful admin panel for content management.

## Features

- 🎨 **Beautiful Admin Interface** - Enhanced admin panel with better UI using django-admin-interface
- 📱 **RESTful API** - Complete API endpoints for frontend integration
- 🖼️ **AWS S3 Integration** - Image storage with S3 bucket integration
- 📧 **Email Notifications** - Automatic email alerts for appointments and contact messages
- 🗄️ **PostgreSQL Database** - Production-ready database setup
- 🔒 **CORS Support** - Cross-origin resource sharing for frontend integration

## API Endpoints

### Content Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/landing-bg/` | GET | Landing page background image or carousel | - |
| `/api/about-us/` | GET | About us content | `?isLanding=true` for landing page |
| `/api/treatments/` | GET | Treatment categories and items | `?isLanding=true` for featured treatments |
| `/api/treatments/faq/` | GET | Treatment FAQs | - |
| `/api/results/` | GET | Before/after results | `?isLanding=true` for featured result |
| `/api/skin-concerns/` | GET | Skin concerns list | - |
| `/api/landing/faq/` | GET | Landing page FAQs | - |

### Form Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/appointments/` | POST | Book an appointment |
| `/api/contact/` | POST | Send contact message |

### Utility Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health/` | GET | Health check |
| `/api/endpoints/` | GET | List all endpoints |

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MonalisaWellness
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Update the `config.py` file with your actual credentials:

```python
# Database Configuration
DATABASE_NAME = 'your_database_name'
DATABASE_USER = 'your_db_user'
DATABASE_PASSWORD = 'your_db_password'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = 'your_aws_access_key'
AWS_SECRET_ACCESS_KEY = 'your_aws_secret_key'
AWS_STORAGE_BUCKET_NAME = 'your_s3_bucket_name'
AWS_S3_REGION_NAME = 'us-east-1'

# Django Settings
SECRET_KEY = 'your-secret-key-here'
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your-domain.com']

# Email Configuration (for appointment notifications)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
EMAIL_USE_TLS = True
OWNER_EMAIL = 'owner@monalisawellness.com'
```

### 5. Set Up PostgreSQL Database

Create a PostgreSQL database and user:

```sql
CREATE DATABASE monalisa_wellness_db;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE monalisa_wellness_db TO your_db_user;
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Collect Static Files (if using S3)

```bash
python manage.py collectstatic
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/` and the admin panel at `http://localhost:8000/admin/`.

## Admin Panel Usage

### 1. Access Admin Panel

Navigate to `http://localhost:8000/admin/` and log in with your superuser credentials.

### 2. Content Management

#### Landing Page Background
- Choose between static image or carousel
- Upload background images
- Manage carousel items with title, description, and images

#### About Us Content
- Create separate content for normal and landing pages
- Add team members with photos and bios
- Manage philosophy highlights

#### Treatments
- Create treatment categories
- Add individual treatments with pricing and images
- Mark treatments as featured for landing page
- Manage treatment FAQs

#### Results Gallery
- Upload before/after images
- Add case descriptions
- Mark results as featured for landing page

#### Skin Concerns
- Add skin concern categories with icons
- Include treatment recommendations

#### FAQs
- Manage landing page FAQs
- Organize with display order

### 3. Appointment Management

- View all appointment requests
- Update appointment status (pending, confirmed, completed, cancelled)
- Add internal notes
- Email notifications sent automatically

### 4. Contact Messages

- View all contact form submissions
- Mark messages as read/unread
- Email notifications for new messages

## API Response Examples

### Landing Page Background (Static)

```json
"https://your-bucket.s3.amazonaws.com/landing/bg/background.jpg"
```

### Landing Page Background (Carousel)

```json
[
  {
    "title": "Rejuvenating Treatments",
    "description": "Transform your skin with our advanced treatments",
    "imageUrl": "https://your-bucket.s3.amazonaws.com/landing/carousel/image1.jpg"
  }
]
```

### About Us (Normal Page)

```json
{
  "desp1": "Welcome to Monalisa Wellness...",
  "desp2": "Our expert team...",
  "team": [
    {
      "name": "Dr. Jane Smith",
      "role": "Lead Dermatologist",
      "bio": "With over 15 years of experience...",
      "image": "https://your-bucket.s3.amazonaws.com/team/jane.jpg"
    }
  ],
  "philosophy": {
    "title": "Our Philosophy",
    "highlights": [
      {
        "title": "Personalized Care",
        "description": "Every treatment is tailored to your unique needs"
      }
    ]
  }
}
```

### Treatments (Landing Page)

```json
[
  {
    "id": 1,
    "name": "HydraFacial",
    "description": "Deep cleansing and hydrating treatment",
    "image": "https://your-bucket.s3.amazonaws.com/treatments/hydrafacial.jpg",
    "price": "$150",
    "duration": "60 minutes"
  }
]
```

### Appointment Booking

**POST Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "preferred_date": "2024-01-15",
  "preferred_time": "14:30:00",
  "treatment_interest": "HydraFacial",
  "message": "Looking forward to the consultation"
}
```

**Response:**
```json
{
  "message": "Appointment request submitted successfully. We will contact you soon.",
  "appointment_id": 123
}
```

## Deployment

### Production Settings

1. Set `DEBUG = False` in config.py
2. Add your domain to `ALLOWED_HOSTS`
3. Configure proper database settings
4. Set up AWS S3 bucket with proper permissions
5. Configure email settings for notifications

### AWS S3 Setup

1. Create an S3 bucket
2. Configure bucket policy for public read access
3. Create IAM user with S3 permissions
4. Add credentials to config.py

### Database Backup

Regular backup is recommended:

```bash
pg_dump monalisa_wellness_db > backup.sql
```

## Security Notes

- Keep your SECRET_KEY secure
- Use environment variables for sensitive data
- Regularly update dependencies
- Configure proper CORS settings
- Use HTTPS in production

## Support

For any issues or questions, please create an issue in the repository or contact the development team.

## License

This project is proprietary software for Monalisa Wellness clinic. 