# Generated by Django 4.1.4 on 2023-04-21 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_auctionlisting_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='auc_image',
            field=models.ImageField(blank=True, upload_to='auc_images/'),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='imageUrl',
            field=models.URLField(blank=True, null=True),
        ),
    ]
