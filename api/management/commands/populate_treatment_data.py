from django.core.management.base import BaseCommand
from api.models import TreatmentBenefit, TreatmentStep


class Command(BaseCommand):
    help = 'Populate treatment benefits and steps with default data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate treatment data...'))

        # Treatment Benefits Data (from the frontend)
        benefits_data = [
            {
                'title': 'Professional Results',
                'description': 'Achieve noticeable improvements with our expert treatments.',
                'order': 1,
            },
            {
                'title': 'Safe & Effective',
                'description': 'FDA-approved procedures performed by licensed professionals.',
                'order': 2,
            },
            {
                'title': 'Personalized Care',
                'description': 'Customized treatment plans tailored to your unique needs.',
                'order': 3,
            },
            {
                'title': 'Long-lasting Results',
                'description': 'Enjoy improvements that last with proper maintenance.',
                'order': 4,
            },
            {
                'title': 'Minimal Downtime',
                'description': 'Return to your daily activities quickly after treatment.',
                'order': 5,
            },
            {
                'title': 'Expert Guidance',
                'description': 'Receive comprehensive aftercare instructions and support.',
                'order': 6,
            },
        ]

        # Treatment Steps Data (from the frontend "What to Expect")
        steps_data = [
            {
                'title': 'Consultation',
                'description': 'Initial assessment of your skin and treatment goals.',
                'step_number': 1,
                'order': 1,
            },
            {
                'title': 'Treatment',
                'description': 'Professional application of the treatment procedure.',
                'step_number': 2,
                'order': 2,
            },
            {
                'title': 'Aftercare',
                'description': 'Follow-up guidance and maintenance recommendations.',
                'step_number': 3,
                'order': 3,
            },
        ]

        # Create Treatment Benefits
        created_benefits = 0
        for benefit_data in benefits_data:
            benefit, created = TreatmentBenefit.objects.get_or_create(
                title=benefit_data['title'],
                defaults={
                    'description': benefit_data['description'],
                    'order': benefit_data['order'],
                    'is_active': True,
                }
            )
            if created:
                created_benefits += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created benefit: {benefit.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Benefit already exists: {benefit.title}')
                )

        # Create Treatment Steps
        created_steps = 0
        for step_data in steps_data:
            step, created = TreatmentStep.objects.get_or_create(
                title=step_data['title'],
                step_number=step_data['step_number'],
                defaults={
                    'description': step_data['description'],
                    'order': step_data['order'],
                    'is_active': True,
                }
            )
            if created:
                created_steps += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created step {step.step_number}: {step.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Step already exists: {step.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created {created_benefits} benefits and {created_steps} steps.'
            )
        ) 