from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from api.models import Clinic, Offer, Treatment
import random


class Command(BaseCommand):
    help = 'Populate sample offers and distribute treatments across clinics'

    def handle(self, *args, **options):
        self.stdout.write('Starting sample data population...')
        
        # Get all clinics
        clinics = list(Clinic.objects.all())
        if not clinics:
            self.stdout.write(self.style.ERROR('No clinics found. Please create clinics first.'))
            return
            
        self.stdout.write(f'Found {len(clinics)} clinics')
        
        # Create sample offers for each clinic
        self.create_sample_offers(clinics)
        
        # Distribute treatments across clinics
        self.distribute_treatments(clinics)
        
        self.stdout.write(self.style.SUCCESS('Sample data population completed!'))

    def create_sample_offers(self, clinics):
        """Create sample offers for clinics"""
        self.stdout.write('Creating sample offers...')
        
        offer_templates = [
            {
                'header': '20% Off First Treatment',
                'description': 'Get 20% discount on your first treatment session. Perfect for new clients looking to experience our premium services. Valid for all treatments except consultation fees.',
            },
            {
                'header': 'Summer Glow Package',
                'description': 'Complete skin rejuvenation package including facial treatment, consultation, and aftercare products. Get glowing skin ready for summer!',
            },
            {
                'header': 'Free Consultation Week',
                'description': 'Book your free consultation this week and get personalized treatment recommendations from our expert dermatologists.',
            },
            {
                'header': 'Holiday Special - Buy 2 Get 1 Free',
                'description': 'Purchase any two treatment sessions and get the third one absolutely free. Perfect time to invest in your skin health.',
            },
            {
                'header': 'Weekend Wellness Deal',
                'description': 'Special weekend rates on all premium treatments. Relax and rejuvenate with our expert care at discounted prices.',
            }
        ]
        
        created_offers = 0
        for clinic in clinics:
            # Create 2-3 random offers per clinic
            num_offers = random.randint(2, 3)
            selected_offers = random.sample(offer_templates, min(num_offers, len(offer_templates)))
            
            for i, offer_data in enumerate(selected_offers):
                # Create offers with different validity periods
                valid_from = timezone.now().date()
                valid_until = valid_from + timedelta(days=random.randint(30, 90))
                
                offer = Offer.objects.create(
                    clinic=clinic,
                    header=offer_data['header'],
                    description=offer_data['description'],
                    valid_from=valid_from,
                    valid_until=valid_until,
                    is_active=True,
                    is_featured=i == 0,  # Make first offer featured
                    order=i
                )
                created_offers += 1
                
        self.stdout.write(f'Created {created_offers} sample offers')

    def distribute_treatments(self, clinics):
        """Distribute existing treatments across clinics"""
        self.stdout.write('Distributing treatments across clinics...')
        
        treatments = Treatment.objects.filter(clinic__isnull=False)
        if not treatments.exists():
            self.stdout.write(self.style.WARNING('No treatments found to distribute'))
            return
            
        # Count treatments per clinic before redistribution
        before_distribution = {}
        for clinic in clinics:
            before_distribution[clinic.name] = clinic.treatments.count()
            
        # Get treatments that are already assigned to the first clinic (from our earlier assignment)
        assigned_treatments = list(treatments)
        
        # Redistribute some treatments to other clinics for variety
        for treatment in assigned_treatments[1::2]:  # Every other treatment
            new_clinic = random.choice(clinics)
            treatment.clinic = new_clinic
            treatment.save()
            
        # Count treatments per clinic after redistribution
        after_distribution = {}
        total_treatments = 0
        for clinic in clinics:
            count = clinic.treatments.count()
            after_distribution[clinic.name] = count
            total_treatments += count
            
        self.stdout.write('Treatment distribution:')
        for clinic_name in after_distribution:
            before = before_distribution.get(clinic_name, 0)
            after = after_distribution[clinic_name]
            self.stdout.write(f'  {clinic_name}: {before} → {after} treatments')
            
        self.stdout.write(f'Total treatments distributed: {total_treatments}') 