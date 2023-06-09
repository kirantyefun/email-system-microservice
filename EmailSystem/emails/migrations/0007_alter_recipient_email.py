# Generated by Django 4.1.7 on 2023-03-26 13:15

from django.db import migrations, models
import emails.validators


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0006_recipient_remove_sentemail_recipient_email_addresses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True, validators=[emails.validators.validate_email]),
        ),
    ]
