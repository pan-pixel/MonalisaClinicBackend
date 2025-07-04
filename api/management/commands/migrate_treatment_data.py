from django.core.management.base import BaseCommand
from api.models import Treatment, TreatmentBenefit, TreatmentStep


class Command(BaseCommand):
    help = 'Migrate existing global benefits and steps to be treatment-specific'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to migrate treatment data...'))

        # Get all treatments
        treatments = Treatment.objects.filter(is_active=True)
        if not treatments.exists():
            self.stdout.write(self.style.ERROR('No active treatments found. Please create treatments first.'))
            return

        # Get all global benefits and steps (ones without treatment assigned)
        global_benefits = TreatmentBenefit.objects.filter(treatment__isnull=True, is_active=True)
        global_steps = TreatmentStep.objects.filter(treatment__isnull=True, is_active=True)

        if not global_benefits.exists() and not global_steps.exists():
            self.stdout.write(self.style.WARNING('No global benefits or steps found to migrate.'))
            return

        self.stdout.write(f'Found {treatments.count()} treatments')
        self.stdout.write(f'Found {global_benefits.count()} global benefits')
        self.stdout.write(f'Found {global_steps.count()} global steps')

        created_benefits = 0
        created_steps = 0

        # For each treatment, create copies of all global benefits and steps
        for treatment in treatments:
            self.stdout.write(f'\nProcessing treatment: {treatment.name}')

            # Create benefits for this treatment
            for benefit in global_benefits:
                new_benefit = TreatmentBenefit.objects.create(
                    treatment=treatment,
                    title=benefit.title,
                    description=benefit.description,
                    order=benefit.order,
                    is_active=benefit.is_active
                )
                created_benefits += 1
                self.stdout.write(f'  ✓ Created benefit: {new_benefit.title}')

            # Create steps for this treatment
            for step in global_steps:
                new_step = TreatmentStep.objects.create(
                    treatment=treatment,
                    title=step.title,
                    description=step.description,
                    step_number=step.step_number,
                    order=step.order,
                    is_active=step.is_active
                )
                created_steps += 1
                self.stdout.write(f'  ✓ Created step: {new_step.title}')

        # Ask user if they want to delete the old global benefits and steps
        if global_benefits.exists() or global_steps.exists():
            self.stdout.write(f'\nCreated {created_benefits} treatment-specific benefits')
            self.stdout.write(f'Created {created_steps} treatment-specific steps')
            
            delete_confirm = input('\nDo you want to delete the old global benefits and steps? (y/N): ')
            if delete_confirm.lower() in ['y', 'yes']:
                deleted_benefits = global_benefits.count()
                deleted_steps = global_steps.count()
                
                global_benefits.delete()
                global_steps.delete()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Deleted {deleted_benefits} global benefits and {deleted_steps} global steps'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        'Kept the old global benefits and steps. You may want to delete them manually later.'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nMigration completed! Created {created_benefits} benefits and {created_steps} steps.'
            )
        ) 