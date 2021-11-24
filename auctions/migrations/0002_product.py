# Generated by Django 3.2.7 on 2021-11-17 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('image', models.ImageField(upload_to='images')),
                ('description', models.CharField(max_length=500)),
                ('detailed', models.URLField(null=True, unique=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(max_length=60, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='auctions.category')),
            ],
        ),
    ]