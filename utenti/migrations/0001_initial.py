# Generated by Django 3.1.7 on 2021-03-13 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indirizzo', models.CharField(max_length=100)),
                ('citta', models.CharField(max_length=50)),
                ('sesso', models.CharField(default='', max_length=10)),
                ('data_nascita', models.DateField(null=True)),
                ('provincia', models.CharField(max_length=2)),
                ('regione', models.CharField(max_length=50)),
                ('latitudine', models.FloatField(blank=True, default=0, null=True)),
                ('longitudine', models.FloatField(blank=True, default=0, null=True)),
                ('telefono', models.CharField(max_length=20)),
                ('foto_profilo', models.FileField(blank=True, default='', null=True, upload_to='')),
                ('guidatore', models.BooleanField(default=False)),
                ('posti_macchina', models.IntegerField(default=0)),
                ('generi_preferiti', models.CharField(default='', max_length=500)),
                ('feedback_user', models.FloatField(default=0)),
                ('feedback_guidatore', models.FloatField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
