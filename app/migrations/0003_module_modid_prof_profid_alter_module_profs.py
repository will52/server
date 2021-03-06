# Generated by Django 4.0.3 on 2022-03-22 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_prof_modules_module_profs'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='modID',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='prof',
            name='profID',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='profs',
            field=models.ManyToManyField(related_name='modules', to='app.prof'),
        ),
    ]
