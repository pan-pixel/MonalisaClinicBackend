# Generated manually to allow blank treatment images

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_create_testimonials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='treatments/'),
        ),
    ]
