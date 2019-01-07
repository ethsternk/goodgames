# Generated by Django 2.1.4 on 2019-01-05 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goodgames', '0003_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='profile',
        ),
        migrations.AlterField(
            model_name='post',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodgames.Game'),
        ),
        migrations.AlterField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodgames.Profile'),
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]
