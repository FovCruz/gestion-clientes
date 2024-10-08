# Generated by Django 5.1 on 2024-08-30 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_usuarios', '0006_alter_sliderimage_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='logos/')),
            ],
            options={
                'verbose_name': 'Logo',
                'verbose_name_plural': 'Carrusel de logos',
            },
        ),
    ]
