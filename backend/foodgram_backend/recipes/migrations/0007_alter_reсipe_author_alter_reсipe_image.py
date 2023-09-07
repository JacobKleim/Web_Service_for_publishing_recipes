# Generated by Django 4.2.4 on 2023-09-05 21:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0006_alter_reсipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reсipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reсipe',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='recipes/images/'),
        ),
    ]
