# Generated manually for Cars Empire PRD v1.2
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_vehicle_make_alter_vehicle_model'),
        ('payments', '0004_remove_paymenttransaction_paymob_order_id_and_more'),
        ('merchants', '0012_pageadvert_pageadvertimage_pageadvertvideo_and_more'),
        ('deals', '0007_alter_deal_category_deal_clicks_count_deal_deal_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'ordering': ['-is_primary', '-created_at']},
        ),
        migrations.AddField(
            model_name='vehicle',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='license_plate',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='mileage_km',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='fuel_type',
            field=models.CharField(blank=True, choices=[('petrol', 'Petrol'), ('diesel', 'Diesel'), ('hybrid', 'Hybrid'), ('electric', 'Electric')], default='petrol', max_length=20),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='is_primary',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(blank=True, db_index=True, max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='order',
            name='currency',
            field=models.CharField(default='EGP', max_length=3),
        ),
        migrations.AddField(
            model_name='order',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='discount_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='fee_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='tax_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='wallet_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='payments.paymenttransaction'),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('pending_payment', 'Pending Payment'), ('paid', 'Paid'), ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('refunded', 'Refunded'), ('failed', 'Failed')], db_index=True, default='pending_payment', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Grand total payable', max_digits=10),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='users.vehicle'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='merchants.branch'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='line_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='booking_required',
            field=models.BooleanField(default=False),
        ),
    ]
