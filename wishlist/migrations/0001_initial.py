# Generated by Django 5.1.1 on 2024-09-08 23:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wishlist_id', models.CharField(blank=True, max_length=250)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.products')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wishlist.wishlist')),
            ],
        ),
    ]
