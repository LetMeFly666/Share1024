# Generated by Django 3.2 on 2022-10-28 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apps', '0002_cards_got_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='got',
            name='th',
            field=models.IntegerField(default=0, verbose_name='此卡的第几次被领取'),
            preserve_default=False,
        ),
    ]
