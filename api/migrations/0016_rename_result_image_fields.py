# Generated migration to rename after_image to result_image and remove before_image

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_add_user_image_to_testimonial'),
    ]

    operations = [
        # Remove before_image field
        migrations.RemoveField(
            model_name='result',
            name='before_image',
        ),
        # Rename after_image to result_image and update upload path
        migrations.RenameField(
            model_name='result',
            old_name='after_image',
            new_name='result_image',
        ),
        # Update the field to change upload_to path
        migrations.AlterField(
            model_name='result',
            name='result_image',
            field=models.ImageField(help_text='Result image showing treatment outcome', upload_to='results/'),
        ),
    ]
