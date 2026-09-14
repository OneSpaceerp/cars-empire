# Generated manually for Cars Empire PRD Section 17
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0005_alter_coupon_options_coupon_created_at_and_more'),
        ('users', '0009_order_enhancements_vehicle_fields'),
        ('merchants', '0012_pageadvert_pageadvertimage_pageadvertvideo_and_more'),
        ('deals', '0007_alter_deal_category_deal_clicks_count_deal_deal_type_and_more'),
        ('payments', '0004_remove_paymenttransaction_paymob_order_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=50, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('discount_type', models.CharField(choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')], default='percentage', max_length=10)),
                ('discount_value', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('min_purchase', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('max_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('usage_limit', models.PositiveIntegerField(blank=True, null=True)),
                ('times_used', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Promo / Discount Code',
                'verbose_name_plural': 'Promo / Discount Codes',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='coupon',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coupons', to='users.order'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='order_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coupons', to='users.orderitem'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='merchant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issued_coupons', to='merchants.merchant'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branch_coupons', to='merchants.branch'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicle_coupons', to='users.vehicle'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='code_hash',
            field=models.CharField(blank=True, db_index=True, help_text='SHA-256 hash for fast secure lookup', max_length=64),
        ),
        migrations.AddField(
            model_name='coupon',
            name='qr_token',
            field=models.CharField(blank=True, db_index=True, help_text='Cryptographically secure opaque token for QR code', max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='issued_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='coupon',
            name='valid_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='redeemed_by_staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='redeemed_coupons', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='coupon_code',
            field=models.CharField(db_index=True, editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('validated', 'Validated'), ('redeeming', 'Redeeming'), ('redeemed', 'Redeemed'), ('expired', 'Expired'), ('cancelled', 'Cancelled'), ('refunded', 'Refunded'), ('suspended', 'Suspended'), ('issued', 'Issued (Available)')], db_index=True, default='available', max_length=20),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupons', to=settings.AUTH_USER_MODEL, verbose_name='Customer'),
        ),
        migrations.CreateModel(
            name='Redemption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_fingerprint', models.CharField(blank=True, default='', max_length=255)),
                ('redeemed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('method', models.CharField(choices=[('qr_scan', 'QR Code Scan'), ('code_entry', 'Manual Code Entry'), ('pos_sync', 'POS Sync'), ('manual', 'Admin Override')], default='qr_scan', max_length=20)),
                ('receipt_number', models.CharField(blank=True, max_length=50, unique=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('reversed', 'Reversed'), ('disputed', 'Disputed')], default='completed', max_length=20)),
                ('reversal_reason', models.TextField(blank=True, default='')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='redemptions', to='merchants.branch')),
                ('coupon', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='redemption', to='coupons.coupon')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='redemptions', to='merchants.merchant')),
                ('staff_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_redemptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-redeemed_at'],
            },
        ),
        migrations.CreateModel(
            name='CouponEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('issued', 'Issued'), ('validated', 'Validated'), ('redeeming', 'Redemption In Progress'), ('redeemed', 'Redeemed'), ('reversed', 'Reversed'), ('expired', 'Expired'), ('cancelled', 'Cancelled'), ('refunded', 'Refunded')], max_length=30)),
                ('notes', models.TextField(blank=True, default='')),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='merchants.branch')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='coupons.coupon')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_order_number', models.CharField(blank=True, db_index=True, max_length=50, unique=True)),
                ('status', models.CharField(choices=[('opened', 'Opened / Checked In'), ('diagnosing', 'Diagnosing'), ('in_progress', 'In Progress'), ('awaiting_parts', 'Awaiting Parts / Approval'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], db_index=True, default='opened', max_length=30)),
                ('arrival_mileage_km', models.PositiveIntegerField(blank=True, help_text='Odometer reading when vehicle arrives', null=True)),
                ('completion_note', models.TextField(blank=True, default='')),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='work_orders', to='merchants.branch')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='work_orders', to='coupons.coupon')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_work_orders', to=settings.AUTH_USER_MODEL)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='work_orders', to='merchants.merchant')),
                ('redemption', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='work_order', to='coupons.redemption')),
                ('technician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_work_orders', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='work_orders', to='users.vehicle')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='coupon',
            index=models.Index(fields=['coupon_code', 'status'], name='coupons_cou_coupon__6c879d_idx'),
        ),
        migrations.AddIndex(
            model_name='coupon',
            index=models.Index(fields=['qr_token', 'status'], name='coupons_cou_qr_toke_5ef678_idx'),
        ),
        migrations.AddIndex(
            model_name='coupon',
            index=models.Index(fields=['merchant', 'status', 'valid_until'], name='coupons_cou_merchan_a83152_idx'),
        ),
    ]
