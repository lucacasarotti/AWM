# Generated by Django 3.1.7 on 2021-03-15 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inviti', '0004_auto_20210315_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='invito',
            name='tipologia',
            field=models.CharField(choices=[('Cinema', 'Cinema'), ('Netflix', 'Netflix'), ('Prime Video', 'Prime Video'), ('Disney+', 'Disney+')], default='Cinema', max_length=100),
        ),
        migrations.AlterField(
            model_name='invito',
            name='cinema',
            field=models.CharField(blank=True, choices=[('Victoria Cinema', 'Victoria Cinema'), ('Cinema Raffaello', 'Cinema Raffaello'), ('Cinema Astra', 'Cinema Astra')], max_length=100),
        ),
    ]