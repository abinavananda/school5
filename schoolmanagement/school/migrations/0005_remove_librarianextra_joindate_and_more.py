# Generated by Django 5.1.2 on 2024-10-26 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_alter_book_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='librarianextra',
            name='joindate',
        ),
        migrations.AlterField(
            model_name='libraryhistory',
            name='borrow_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='libraryhistory',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
