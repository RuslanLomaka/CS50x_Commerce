# Generated by Django 5.1.5 on 2025-03-23 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('ELEC', 'Electronics'), ('BOOK', 'Books'), ('FASH', 'Fashion'), ('HOME', 'Home & Garden'), ('TOY', 'Toys'), ('AUTO', 'Automotive'), ('SPORT', 'Sports & Outdoors'), ('OTHER', 'Other')], default='OTHER', max_length=20),
        ),
    ]
