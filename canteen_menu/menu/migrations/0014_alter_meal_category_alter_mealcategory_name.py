# Generated by Django 4.2.2 on 2023-12-16 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0013_alter_meal_category_alter_mealcategory_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.mealcategory', to_field='name'),
        ),
        migrations.AlterField(
            model_name='mealcategory',
            name='name',
            field=models.CharField(max_length=150, unique='True'),
        ),
    ]