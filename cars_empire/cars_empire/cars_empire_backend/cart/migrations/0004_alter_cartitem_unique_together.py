# Generated manually for Cars Empire
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_cartitem_deal'),
        ('deals', '0007_alter_deal_category_deal_clicks_count_deal_deal_type_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'deal')},
        ),
    ]
