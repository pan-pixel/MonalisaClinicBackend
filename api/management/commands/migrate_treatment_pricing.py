from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Treatment, TreatmentClinicPricing, Clinic


class Command(BaseCommand):
    help = 'Migrate existing treatment data to the new pricing structure'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )
        
        # Get all treatments that might have old clinic/price data
        # Since we removed the fields, we'll need to work with what we have
        treatments = Treatment.objects.all()
        
        if not treatments.exists():
            self.stdout.write(
                self.style.SUCCESS('No treatments found to migrate')
            )
            return
        
        self.stdout.write(f'Found {treatments.count()} treatments to process')
        
        # Get all clinics
        clinics = Clinic.objects.filter(is_active=True)
        if not clinics.exists():
            self.stdout.write(
                self.style.ERROR('No active clinics found. Please create clinics first.')
            )
            return
        
        self.stdout.write(f'Found {clinics.count()} active clinics')
        
        migrated_count = 0
        
        with transaction.atomic():
            for treatment in treatments:
                # Check if treatment already has pricing entries
                existing_pricing = treatment.clinic_pricing.exists()
                
                if existing_pricing:
                    self.stdout.write(
                        f'Treatment "{treatment.name}" already has pricing entries, skipping...'
                    )
                    continue
                
                # Create pricing entries for all clinics with a default price
                # You can customize this logic based on your needs
                default_price = "Contact for pricing"  # Default price for all clinics
                
                for clinic in clinics:
                    if not dry_run:
                        TreatmentClinicPricing.objects.create(
                            treatment=treatment,
                            clinic=clinic,
                            price=default_price,
                            is_active=True,
                            order=0
                        )
                    
                    self.stdout.write(
                        f'{"Would create" if dry_run else "Created"} pricing for '
                        f'"{treatment.name}" at "{clinic.name}" with price "{default_price}"'
                    )
                
                migrated_count += 1
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'DRY RUN COMPLETE: Would migrate {migrated_count} treatments'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Migration complete: Migrated {migrated_count} treatments'
                )
            )
            
            # Show summary
            total_pricing_entries = TreatmentClinicPricing.objects.count()
            self.stdout.write(
                f'Total pricing entries created: {total_pricing_entries}'
            )
