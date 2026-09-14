#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cars_empire_project.settings')
django.setup()

from merchants.models import Merchant
from deals.models import DealImage

def fix_merchant_logos():
    """Fix merchant logo paths from merchants/logos/ to merchant_logos/"""
    updated = 0
    for merchant in Merchant.objects.filter(logo__isnull=False):
        old_path = str(merchant.logo)
        if 'merchants/logos/' in old_path:
            new_path = old_path.replace('merchants/logos/', 'merchant_logos/')
            merchant.logo = new_path
            merchant.save()
            updated += 1
            print(f'Updated {merchant.name}: {old_path} -> {new_path}')
    print(f'Total merchant logos updated: {updated}')

def fix_deal_images():
    """Fix deal image paths if needed"""
    updated = 0
    for deal_image in DealImage.objects.all():
        old_path = str(deal_image.image)
        if 'deal_images/' in old_path:
            # Check if file exists in the new location
            new_path = old_path
            if os.path.exists(os.path.join('/home/carsempire/repositories/cars_empire/public_html/media', new_path)):
                print(f'Deal image exists: {new_path}')
            else:
                print(f'Deal image missing: {new_path}')
        updated += 1
    print(f'Total deal images checked: {updated}')

if __name__ == '__main__':
    print('Fixing media file paths...')
    fix_merchant_logos()
    fix_deal_images()
    print('Done!')
