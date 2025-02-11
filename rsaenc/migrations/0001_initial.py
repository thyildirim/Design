# Generated by Django 5.1.4 on 2025-01-16 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EncryptedDNA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.CharField(max_length=1000, unique=True)),
                ('encrypted_sequence', models.CharField(blank=True, max_length=1000, null=True)),
                ('gene_name', models.CharField(blank=True, max_length=255, null=True)),
                ('gen_description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
