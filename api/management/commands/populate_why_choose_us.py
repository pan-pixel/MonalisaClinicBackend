from django.core.management.base import BaseCommand
from api.models import WhyChooseUs


class Command(BaseCommand):
    help = 'Populate Why Choose Us benefits with initial data'

    def handle(self, *args, **options):
        # Clear existing data
        WhyChooseUs.objects.all().delete()
        
        # Initial data matching the frontend static data
        benefits_data = [
            {
                'title': 'Years of Experience',
                'description': 'Our team brings decades of specialized expertise in advanced skincare therapies and treatments.',
                'icon': 'clock',
                'order': 1,
                'is_active': True
            },
            {
                'title': 'Personalized Plans',
                'description': 'Every treatment plan is customized to your unique skin type, concerns, and aesthetic goals.',
                'icon': 'award',
                'order': 2,
                'is_active': True
            },
            {
                'title': 'Advanced Technology',
                'description': 'We utilize the latest innovations in skincare technology to deliver superior, lasting results.',
                'icon': 'zap',
                'order': 3,
                'is_active': True
            },
            {
                'title': 'Proven Results',
                'description': 'Our treatments are designed to deliver visible improvements and long-term satisfaction.',
                'icon': 'heart',
                'order': 4,
                'is_active': True
            }
        ]
        
        created_count = 0
        for benefit_data in benefits_data:
            benefit, created = WhyChooseUs.objects.get_or_create(
                title=benefit_data['title'],
                defaults=benefit_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created benefit: {benefit.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Benefit already exists: {benefit.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} Why Choose Us benefits')
        ) 