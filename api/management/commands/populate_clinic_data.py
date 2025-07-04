from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from api.models import Clinic, ClinicImage, ClinicTeamMember
import requests
from io import BytesIO
import os


class Command(BaseCommand):
    help = 'Populate sample clinic data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating clinic data...'))
        
        # Clear existing data
        Clinic.objects.all().delete()
        
        # Create Delhi Clinic
        delhi_clinic = Clinic.objects.create(
            name="The Monalisa - Best Skin, Hair & Laser Clinic in Delhi",
            specialization="Senior Dermatologist, Plastic Surgeon, Advanced Laser Treatments, Hair Restoration",
            description="Our Delhi clinic is a state-of-the-art facility offering comprehensive dermatological and aesthetic treatments. With over 15 years of experience, we provide personalized care using the latest technology and proven treatment methods. Our team of certified specialists ensures the highest quality care in a comfortable, hygienic environment.",
            address="1965, Basement, Outram Ln, Kingsway Camp",
            city="GTB Nagar, New Delhi, Delhi 110009",
            phone="092891 57655",
            email="delhi@monalisaclinic.com",
            rating=4.6,
            reviews_count=150,
            reviews_text="Google reviews",
            business_hours="Open Daily - Closes 7:30 PM",
            hours_note="Call for specific timings",
            google_maps_url="https://g.co/kgs/XW9qzHx",
            map_embed_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3500.0!2d77.2!3d28.7!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjjCsDQyJzAwLjAiTiA3N8KwMTInMDAuMCJF!5e0!3m2!1sen!2sin!4v1234567890",
            order=1,
            is_active=True
        )
        
        # Set main image for Delhi clinic (using existing image)
        try:
            with open('media/delhi-clinic-interior.jpg', 'rb') as f:
                delhi_clinic.main_image.save('delhi-main.jpg', ContentFile(f.read()), save=True)
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Delhi clinic main image not found, skipping...'))
        
        # Create additional images for Delhi clinic
        delhi_images = [
            ("Reception Area", "Our welcoming reception area with modern amenities", "media/about/landing/IMG_2367.jpeg"),
            ("Treatment Room", "State-of-the-art treatment rooms with advanced equipment", "media/treatments/IMG_2333.jpeg"),
            ("Consultation Room", "Private consultation rooms for personalized care", "media/results/after/IMG_2384.jpeg"),
            ("Waiting Lounge", "Comfortable waiting area for our patients", "media/landing/bg/IMG_2333.jpeg")
        ]
        
        for i, (caption, description, image_path) in enumerate(delhi_images):
            clinic_image = ClinicImage.objects.create(
                clinic=delhi_clinic,
                caption=caption,
                order=i + 1,
                is_active=True
            )
            
            # Set image file if it exists
            try:
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        clinic_image.image.save(f'delhi-gallery-{i+1}.jpg', ContentFile(f.read()), save=True)
                else:
                    self.stdout.write(self.style.WARNING(f'Gallery image not found: {image_path}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error setting gallery image: {e}'))
        
        # Create team members for Delhi clinic
        delhi_team = [
            {
                "name": "Dr. Rajesh Kumar",
                "role": "Senior Dermatologist & Clinic Director",
                "bio": "With over 20 years of experience in dermatology, Dr. Kumar specializes in advanced laser treatments and cosmetic procedures. He holds an MD in Dermatology and is certified in multiple laser technologies.",
                "order": 1,
                "image_path": "media/about/landing/lp_image.jpeg"
            },
            {
                "name": "Dr. Priya Sharma",
                "role": "Cosmetic Dermatologist",
                "bio": "Dr. Sharma is an expert in anti-aging treatments and skin rejuvenation. She has extensive training in injectables and non-invasive cosmetic procedures.",
                "order": 2,
                "image_path": "media/results/before/IMG_2354.jpeg"
            },
            {
                "name": "Nurse Anjali Singh",
                "role": "Senior Treatment Coordinator",
                "bio": "Anjali has 10+ years of experience in aesthetic treatments and patient care. She ensures every patient receives personalized attention and care.",
                "order": 3,
                "image_path": "media/treatments/lp_image.jpeg"
            }
        ]
        
        for member_data in delhi_team:
            image_path = member_data.pop('image_path', None)
            order = member_data['order']
            team_member = ClinicTeamMember.objects.create(
                clinic=delhi_clinic,
                **member_data,
                is_active=True
            )
            
            # Set image file if it exists
            if image_path:
                try:
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as f:
                            team_member.image.save(f'delhi-team-{order}.jpg', ContentFile(f.read()), save=True)
                    else:
                        self.stdout.write(self.style.WARNING(f'Team member image not found: {image_path}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error setting team member image: {e}'))
        
        # Create Gurugram Clinic
        gurugram_clinic = Clinic.objects.create(
            name="The Monalisa Clinic Gurugram",
            specialization="Skin Care, Hair Treatments, Laser Therapy, Advanced Aesthetics, Anti-Aging Solutions",
            description="Our Gurugram facility is designed to provide world-class aesthetic and dermatological services. Located in the heart of Gurugram, we offer a complete range of treatments from basic skin care to advanced cosmetic procedures. Our modern facility combines cutting-edge technology with expert medical care to deliver exceptional results.",
            address="Unitech Business Zone, A 405, Golf Course Ext Rd",
            city="Nirvana Country, Sector 50, Gurugram, Haryana 122018",
            phone="08800230404",
            email="gurugram@monalisaclinic.com",
            rating=4.9,
            reviews_count=22,
            reviews_text="Google reviews",
            business_hours="Open Daily - Closes 7:30 PM",
            hours_note="Call for specific timings",
            google_maps_url="https://g.co/kgs/WWBsJCF",
            map_embed_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3500.0!2d77.1!3d28.4!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjjCsDI0JzAwLjAiTiA3N8KwMDYnMDAuMCJF!5e0!3m2!1sen!2sin!4v1234567891",
            order=2,
            is_active=True
        )
        
        # Set main image for Gurugram clinic (using existing image)
        try:
            with open('media/gurugram-clinic-entrance.jpg', 'rb') as f:
                gurugram_clinic.main_image.save('gurugram-main.jpg', ContentFile(f.read()), save=True)
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Gurugram clinic main image not found, skipping...'))
        
        # Create additional images for Gurugram clinic
        gurugram_images = [
            ("Modern Facade", "Contemporary clinic exterior with premium finishes", "media/landing/bg/lp_image.jpeg"),
            ("Laser Treatment Suite", "Advanced laser therapy room with latest equipment", "media/treatments/IMG_2404.png"),
            ("VIP Treatment Room", "Luxury treatment rooms for premium services", "media/results/after/lp_image.jpeg"),
            ("Recovery Lounge", "Comfortable post-treatment recovery area", "media/results/before/IMG_2384.jpeg")
        ]
        
        for i, (caption, description, image_path) in enumerate(gurugram_images):
            clinic_image = ClinicImage.objects.create(
                clinic=gurugram_clinic,
                caption=caption,
                order=i + 1,
                is_active=True
            )
            
            # Set image file if it exists
            try:
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        clinic_image.image.save(f'gurugram-gallery-{i+1}.jpg', ContentFile(f.read()), save=True)
                else:
                    self.stdout.write(self.style.WARNING(f'Gallery image not found: {image_path}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error setting gallery image: {e}'))
        
        # Create team members for Gurugram clinic
        gurugram_team = [
            {
                "name": "Dr. Neha Agarwal",
                "role": "Lead Aesthetic Physician",
                "bio": "Dr. Agarwal is a board-certified dermatologist with expertise in cosmetic dermatology and aesthetic medicine. She has trained internationally and specializes in advanced anti-aging treatments.",
                "order": 1,
                "image_path": "media/results/after/IMG_2384.jpeg"
            },
            {
                "name": "Dr. Vikram Mehta",
                "role": "Hair Restoration Specialist",
                "bio": "With a focus on hair transplantation and restoration, Dr. Mehta has helped hundreds of patients regain their confidence through innovative hair treatment solutions.",
                "order": 2,
                "image_path": "media/about/landing/IMG_2367.jpeg"
            },
            {
                "name": "Sarah Johnson",
                "role": "International Treatment Coordinator",
                "bio": "Sarah specializes in coordinating care for international patients and ensuring a seamless treatment experience from consultation to recovery.",
                "order": 3,
                "image_path": "media/treatments/IMG_2333.jpeg"
            }
        ]
        
        for member_data in gurugram_team:
            image_path = member_data.pop('image_path', None)
            order = member_data['order']
            team_member = ClinicTeamMember.objects.create(
                clinic=gurugram_clinic,
                **member_data,
                is_active=True
            )
            
            # Set image file if it exists
            if image_path:
                try:
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as f:
                            team_member.image.save(f'gurugram-team-{order}.jpg', ContentFile(f.read()), save=True)
                    else:
                        self.stdout.write(self.style.WARNING(f'Team member image not found: {image_path}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error setting team member image: {e}'))
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {Clinic.objects.count()} clinics with '
                f'{ClinicImage.objects.count()} images and '
                f'{ClinicTeamMember.objects.count()} team members'
            )
        ) 