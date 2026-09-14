from django.core.management.base import BaseCommand
from deals.models import Deal
from django.utils.text import slugify
from django.db import transaction

class Command(BaseCommand):
    help = 'Generate slugs for deals that don\'t have them'

    def handle(self, *args, **options):
        deals_without_slugs = Deal.objects.filter(slug='')
        deals_with_none_slugs = Deal.objects.filter(slug__isnull=True)
        
        total_deals = deals_without_slugs.count() + deals_with_none_slugs.count()
        
        if total_deals == 0:
            self.stdout.write(
                self.style.SUCCESS('All deals already have slugs!')
            )
            return
        
        self.stdout.write(f'Found {total_deals} deals without slugs. Generating...')
        
        with transaction.atomic():
            # Handle empty slugs
            for deal in deals_without_slugs:
                base_slug = slugify(deal.title)
                slug = base_slug
                counter = 1
                
                # Ensure slug uniqueness
                while Deal.objects.filter(slug=slug).exclude(id=deal.id).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                deal.slug = slug
                deal.save(update_fields=['slug'])
                self.stdout.write(f'Generated slug "{slug}" for deal "{deal.title}"')
            
            # Handle None slugs
            for deal in deals_with_none_slugs:
                base_slug = slugify(deal.title)
                slug = base_slug
                counter = 1
                
                # Ensure slug uniqueness
                while Deal.objects.filter(slug=slug).exclude(id=deal.id).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                deal.slug = slug
                deal.save(update_fields=['slug'])
                self.stdout.write(f'Generated slug "{slug}" for deal "{deal.title}"')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated slugs for {total_deals} deals!')
        ) 