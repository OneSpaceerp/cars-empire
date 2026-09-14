#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cars_empire_project.settings')
django.setup()

from merchants.models import Merchant, MerchantImage
from deals.models import DealImage

def fix_merchant_logos():
    """Fix merchant logo paths from merchant_logos/ to merchants/logos/"""
    updated = 0
    for merchant in Merchant.objects.filter(logo__isnull=False):
        old_path = str(merchant.logo)
        if 'merchant_logos/' in old_path:
            new_path = old_path.replace('merchant_logos/', 'merchants/logos/')
            merchant.logo = new_path
            merchant.save()
            updated += 1
            print(f'Updated {merchant.name}: {old_path} -> {new_path}')
    print(f'Total merchant logos updated: {updated}')

def fix_merchant_images():
    """Fix merchant image paths to match actual structure"""
    updated = 0
    for merchant_image in MerchantImage.objects.all():
        old_path = str(merchant_image.image)
        if 'merchants/images/' not in old_path:
            # Update to correct path
            new_path = f'merchants/images/{os.path.basename(old_path)}'
            merchant_image.image = new_path
            merchant_image.save()
            updated += 1
            print(f'Updated merchant image: {old_path} -> {new_path}')
    print(f'Total merchant images updated: {updated}')

def fix_deal_images():
    """Fix deal image paths to match actual structure"""
    updated = 0
    for deal_image in DealImage.objects.all():
        old_path = str(deal_image.image)
        if 'deal_images/' not in old_path:
            # Update to correct path
            new_path = f'deal_images/{os.path.basename(old_path)}'
            deal_image.image = new_path
            deal_image.save()
            updated += 1
            print(f'Updated deal image: {old_path} -> {new_path}')
    print(f'Total deal images updated: {updated}')

if __name__ == '__main__':
    print('Fixing all media file paths to match actual structure...')
    fix_merchant_logos()
    fix_merchant_images()
    fix_deal_images()
    print('Done!')
