# Generated manually for Testimonials model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_clinic_phone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot', models.ImageField(help_text='Screenshot of the Google review', upload_to='testimonials/')),
                ('reviewer_name', models.CharField(blank=True, help_text='Name of the reviewer (optional, for SEO)', max_length=200)),
                ('review_text', models.TextField(blank=True, help_text='Text content of the review (optional, for SEO and accessibility)')),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5, help_text='Rating out of 5 stars')),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order (lower numbers appear first)')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this testimonial should be displayed')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
