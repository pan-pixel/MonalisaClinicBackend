from django.core.management.base import BaseCommand
from api.models import SiteSettings


class Command(BaseCommand):
    help = 'Populate initial site settings data'

    def handle(self, *args, **options):
        # Check if site settings already exist
        if SiteSettings.objects.exists():
            self.stdout.write(
                self.style.WARNING('Site settings already exist. Skipping creation.')
            )
            return

        # Create initial site settings
        site_settings = SiteSettings.objects.create(
            site_name="Monalisa Wellness",
            site_tagline="Skin Clinic", 
            site_description="Expert skincare treatments and products that transform your skin and enhance your natural beauty.",
            contact_email="info@monalisaclinic.com",
            contact_phone="092891 57655",
            address="Delhi & Gurugram\nMultiple Locations",
            social_facebook="",
            social_instagram="",
            social_twitter="",
            business_hours="Monday - Sunday: Open Daily\nCloses at: 7:30 PM\nCall for specific timings"
        )

        self.stdout.write(
            self.style.SUCCESS('Successfully created initial site settings.')
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Site Name: {site_settings.site_name}')
        )
        self.stdout.write(
            self.style.SUCCESS('You can now edit these settings in the Django admin interface.')
        ) 