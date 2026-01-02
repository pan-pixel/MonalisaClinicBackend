# Generated migration for adding user_image to Testimonial model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_allow_blank_treatment_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='user_image',
            field=models.ImageField(blank=True, help_text='Profile picture of the reviewer (optional)', null=True, upload_to='testimonials/users/'),
        ),
    ]
