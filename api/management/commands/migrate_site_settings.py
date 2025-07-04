from django.core.management.base import BaseCommand
from api.models import SiteSettings


class Command(BaseCommand):
    help = 'Migrate existing SiteSettings to use multiple contact fields'

    def add_arguments(self, parser):
        parser.add_argument(
            '--add-examples',
            action='store_true',
            help='Add example contact emails and phones',
        )

    def handle(self, *args, **options):
        try:
            # Get or create site settings
            site_settings, created = SiteSettings.objects.get_or_create(
                defaults={
                    'site_name': "Monalisa Wellness",
                    'site_tagline': "Skin Clinic",
                    'site_description': "Expert skincare treatments and products that transform your skin and enhance your natural beauty.",
                    'contact_emails': ["info@monalisaclinic.com", "appointments@monalisaclinic.com"],
                    'contact_phones': ["+91-92891-57655", "+91-98765-43210"],
                    'contact_email': "info@monalisaclinic.com",  # Legacy field
                    'contact_phone': "+91-92891-57655",  # Legacy field
                    'address': "Delhi & Gurugram\nMultiple Locations",
                    'business_hours': "Monday-Friday: 9:00 AM - 7:30 PM\nSaturday-Sunday: 10:00 AM - 6:00 PM\nCall for specific timings"
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS('Successfully created new SiteSettings with multiple contact support.')
                )
            else:
                # Migrate existing data
                migrated = False
                
                # Migrate legacy email to multiple emails if not already set
                if site_settings.contact_email and not site_settings.contact_emails:
                    site_settings.contact_emails = [site_settings.contact_email]
                    migrated = True
                    self.stdout.write(f"Migrated legacy email: {site_settings.contact_email}")
                
                # Migrate legacy phone to multiple phones if not already set
                if site_settings.contact_phone and not site_settings.contact_phones:
                    site_settings.contact_phones = [site_settings.contact_phone]
                    migrated = True
                    self.stdout.write(f"Migrated legacy phone: {site_settings.contact_phone}")
                
                # Add example contacts if requested
                if options['add_examples']:
                    example_emails = [
                        "info@monalisaclinic.com",
                        "appointments@monalisaclinic.com", 
                        "support@monalisaclinic.com"
                    ]
                    example_phones = [
                        "+91-92891-57655",
                        "+91-98765-43210", 
                        "+91-11-1234-5678"
                    ]
                    
                    # Add emails that don't already exist
                    current_emails = site_settings.contact_emails or []
                    for email in example_emails:
                        if email not in current_emails:
                            current_emails.append(email)
                            migrated = True
                    site_settings.contact_emails = current_emails
                    
                    # Add phones that don't already exist
                    current_phones = site_settings.contact_phones or []
                    for phone in example_phones:
                        if phone not in current_phones:
                            current_phones.append(phone)
                            migrated = True
                    site_settings.contact_phones = current_phones
                    
                    self.stdout.write("Added example contact emails and phones.")
                
                # Update business hours format if needed
                if site_settings.business_hours and "7:30" in site_settings.business_hours and "7:30 PM" not in site_settings.business_hours:
                    # Fix common formatting issue
                    site_settings.business_hours = site_settings.business_hours.replace("7:30", "7:30 PM")
                    migrated = True
                    self.stdout.write("Fixed business hours formatting to avoid frontend parsing issues.")
                
                if migrated:
                    site_settings.save()
                    self.stdout.write(
                        self.style.SUCCESS('Successfully migrated existing SiteSettings.')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('SiteSettings already properly configured.')
                    )

            # Display current configuration
            self.stdout.write("\n" + "="*50)
            self.stdout.write(f"Current Site Settings Configuration:")
            self.stdout.write("="*50)
            self.stdout.write(f"Site Name: {site_settings.site_name}")
            self.stdout.write(f"Contact Emails: {site_settings.get_contact_emails()}")
            self.stdout.write(f"Contact Phones: {site_settings.get_contact_phones()}")
            self.stdout.write(f"Primary Email: {site_settings.get_primary_email()}")
            self.stdout.write(f"Primary Phone: {site_settings.get_primary_phone()}")
            self.stdout.write(f"Business Hours: {site_settings.business_hours}")
            
            # API Usage Examples
            self.stdout.write("\n" + "="*50)
            self.stdout.write("API Usage Examples:")
            self.stdout.write("="*50)
            self.stdout.write("Frontend can now access:")
            self.stdout.write("• contact_emails: Multiple email addresses as JSON array")
            self.stdout.write("• contact_phones: Multiple phone numbers as JSON array") 
            self.stdout.write("• all_contact_emails: Combined emails from both new and legacy fields")
            self.stdout.write("• all_contact_phones: Combined phones from both new and legacy fields")
            self.stdout.write("• primary_email: First email address")
            self.stdout.write("• primary_phone: First phone number")
            self.stdout.write("• Legacy fields (contact_email, contact_phone) still work for backward compatibility")

            # Admin Usage
            self.stdout.write("\n" + "="*50)
            self.stdout.write("Django Admin Usage:")
            self.stdout.write("="*50)
            self.stdout.write("1. Go to Django Admin > Site Settings")
            self.stdout.write("2. Use 'Contact Information - Multiple Contacts' section")
            self.stdout.write("3. Enter emails as JSON array: [\"email1@domain.com\", \"email2@domain.com\"]")
            self.stdout.write("4. Enter phones as JSON array: [\"+91-1234567890\", \"+91-0987654321\"]")
            self.stdout.write("5. Legacy single fields are still available for backward compatibility")
            self.stdout.write("6. For business hours, use complete format: 'Monday-Friday: 9:00 AM - 7:30 PM'")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error migrating site settings: {str(e)}')
            ) 