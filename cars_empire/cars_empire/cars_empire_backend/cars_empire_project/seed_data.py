# cars_empire_project/seed_data.py
"""
Utility script to seed initial demo data into Cars Empire database.
Ensures categories, car makes/models, merchants, deals, and legal pages
exist so that visiting any frontend link or API endpoint succeeds.
"""

from datetime import timedelta
from decimal import Decimal
from django.utils import timezone


def seed_demo_data(out=None):
    def log(msg):
        if out is not None:
            out.write(msg + "\n")
        else:
            print(msg)

    log("Starting demo data seeding...")

    # 1. Superuser
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admin_email = 'admin@carsempire.net'
        admin_user = User.objects.filter(email=admin_email).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                email=admin_email,
                password='Admin123456!',
                phone='+201000000000',
                username='admin'
            )
            log(f"Admin created: {admin_email} / Admin123456!")
        else:
            admin_user.set_password('Admin123456!')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            log(f"Admin verified: {admin_email}")
    except Exception as e:
        log(f"Admin seed note: {e}")

    # 2. Categories
    try:
        from merchants.models import Category

        categories_data = [
            (1, "Maintenance & Repair", "maintenance-repair", "Comprehensive mechanical inspection, engine tuning, and general automotive repair."),
            (2, "Car Wash & Detailing", "car-wash-detailing", "Professional exterior washing, interior steam cleaning, polishing, and ceramic coating."),
            (3, "Tire Services & Alignment", "tire-services-alignment", "Tire sales, computer wheel balancing, laser alignment, and puncture repair."),
            (4, "Oil & Filter Service", "oil-filter-service", "Engine oil change with synthetic blends, oil filter replacement, and fluid top-ups."),
            (5, "Brakes & Suspension", "brakes-suspension", "Brake pad replacement, rotor resurfacing, shocks, struts, and suspension service."),
            (6, "Batteries & Electrical", "batteries-electrical", "Battery testing, alternator check, starter repair, and automotive electronics."),
            (7, "Body & Paint", "body-paint", "Dent repair, scratch removal, computerized color matching, and spray painting."),
            (8, "Diagnostics & Inspection", "diagnostics-inspection", "OBD-II computer diagnostics, pre-purchase vehicle inspection, and emissions checks."),
        ]

        created_cats = {}
        for cat_id, name, slug, desc in categories_data:
            cat = Category.objects.filter(id=cat_id).first()
            if not cat:
                cat = Category.objects.filter(slug=slug).first()
            if not cat:
                cat = Category.objects.create(
                    id=cat_id,
                    name=name,
                    slug=slug,
                    description=desc,
                    is_active=True,
                    parent=None
                )
            else:
                cat.name = name
                cat.slug = slug
                cat.description = desc
                cat.is_active = True
                cat.parent = None
                cat.save()
            created_cats[cat_id] = cat

        # Subcategories
        subcats_data = [
            ("Synthetic Oil Change", "synthetic-oil-change", "Premium full synthetic oil change", 4),
            ("Conventional Oil Change", "conventional-oil-change", "Standard multi-grade oil change", 4),
            ("Transmission Fluid Service", "transmission-fluid-service", "Transmission flush and filter replacement", 4),
            ("Ceramic Coating", "ceramic-coating", "Nano-ceramic hydrophobic protective layer", 2),
            ("Interior Detailing", "interior-detailing", "Deep steam upholstery extraction and conditioning", 2),
            ("Express Exterior Wash", "express-exterior-wash", "Hand wash and shine exterior service", 2),
            ("Engine Tune-up", "engine-tune-up", "Complete ignition, plugs, and fuel system service", 1),
            ("AC Service & Recharge", "ac-service-recharge", "Cabin AC refrigerant vacuum, refill, and leak test", 1),
            ("Wheel Alignment", "wheel-alignment", "Precision 4-wheel computerized laser alignment", 3),
            ("Tire Balancing", "tire-balancing", "Dynamic wheel and tire balancing", 3),
        ]

        for name, slug, desc, parent_id in subcats_data:
            parent_cat = created_cats.get(parent_id)
            if parent_cat:
                subcat = Category.objects.filter(slug=slug).first()
                if not subcat:
                    Category.objects.create(
                        name=name,
                        slug=slug,
                        description=desc,
                        is_active=True,
                        parent=parent_cat
                    )
                else:
                    subcat.parent = parent_cat
                    subcat.is_active = True
                    subcat.save()

        log(f"Categories seeded: {Category.objects.count()} total categories")
    except Exception as e:
        log(f"Category seed error: {e}")

    # 3. Car Makes & Models
    try:
        from cars.models import CarMake, CarModel

        makes_data = [
            ("Toyota", "toyota", ["Corolla", "Camry", "RAV4", "Land Cruiser", "Yaris"]),
            ("Mercedes-Benz", "mercedes-benz", ["C-Class", "E-Class", "S-Class", "GLC", "A-Class"]),
            ("BMW", "bmw", ["3 Series", "5 Series", "7 Series", "X5", "X3"]),
            ("Hyundai", "hyundai", ["Elantra", "Tucson", "Sonata", "Accent", "Creta"]),
            ("Kia", "kia", ["Sportage", "Cerato", "Sorento", "Rio", "Carens"]),
        ]

        for make_name, make_slug, models_list in makes_data:
            make, _ = CarMake.objects.get_or_create(name=make_name, defaults={'slug': make_slug})
            for model_name in models_list:
                CarModel.objects.get_or_create(make=make, name=model_name, defaults={'year_start': 2015, 'year_end': 2025})

        log(f"Cars seeded: {CarMake.objects.count()} makes, {CarModel.objects.count()} models")
    except Exception as e:
        log(f"Car makes/models seed error: {e}")

    # 4. Merchants & Branches
    try:
        from merchants.models import Merchant, Branch
        from cars.models import CarMake

        merchants_data = [
            {
                'id': 1,
                'name': 'Speedy Auto Service',
                'slug': 'speedy-auto-service',
                'description': 'Downtown premier auto repair facility specializing in mechanical overhauls, brake systems, and rapid routine servicing.',
                'address_text': '15 Al-Tahrir Square, Downtown, Cairo',
                'latitude': Decimal('30.044420'),
                'longitude': Decimal('31.235712'),
                'phone_number': '+201011112222',
                'email': 'speedy@carsempire.net',
                'rating': Decimal('4.85'),
                'is_verified': True,
                'is_featured': True,
                'branch_name': 'Downtown Main Branch',
            },
            {
                'id': 2,
                'name': 'Elite Detailing Studio',
                'slug': 'elite-detailing-studio',
                'description': 'Luxury car care and detailing centre offering premium ceramic coating, paint correction, and deep interior restoration.',
                'address_text': 'Road 90, 5th Settlement, New Cairo',
                'latitude': Decimal('30.013145'),
                'longitude': Decimal('31.491320'),
                'phone_number': '+201022223333',
                'email': 'elite@carsempire.net',
                'rating': Decimal('4.95'),
                'is_verified': True,
                'is_featured': True,
                'branch_name': 'New Cairo Flagship',
            },
            {
                'id': 3,
                'name': 'German Auto Care',
                'slug': 'german-auto-care',
                'description': 'Certified European auto specialists providing diagnostics, transmission repair, and maintenance for German marques.',
                'address_text': 'Al-Bostan St, Sheikh Zayed City, Giza',
                'latitude': Decimal('30.021650'),
                'longitude': Decimal('30.983340'),
                'phone_number': '+201033334444',
                'email': 'german@carsempire.net',
                'rating': Decimal('4.78'),
                'is_verified': True,
                'is_featured': True,
                'branch_name': 'Sheikh Zayed Workshop',
            },
            {
                'id': 4,
                'name': 'Quick Lube & Tire Express',
                'slug': 'quick-lube-tire-express',
                'description': 'Express oil changes, laser wheel alignments, and comprehensive tire inspection in the heart of Maadi.',
                'address_text': 'Street 9, Degla, Maadi, Cairo',
                'latitude': Decimal('29.960230'),
                'longitude': Decimal('31.256910'),
                'phone_number': '+201044445555',
                'email': 'quicklube@carsempire.net',
                'rating': Decimal('4.65'),
                'is_verified': True,
                'is_featured': True,
                'branch_name': 'Maadi Branch',
            },
        ]

        all_cats = list(Category.objects.all())
        all_makes = list(CarMake.objects.all())

        for m_data in merchants_data:
            m_id = m_data.pop('id')
            b_name = m_data.pop('branch_name')

            merchant = Merchant.objects.filter(id=m_id).first()
            if not merchant:
                merchant = Merchant.objects.filter(slug=m_data['slug']).first()
            if not merchant:
                merchant = Merchant.objects.create(id=m_id, **m_data)
            else:
                for k, v in m_data.items():
                    setattr(merchant, k, v)
                merchant.save()

            if all_cats:
                merchant.categories.set(all_cats[:4])
            if all_makes:
                merchant.makes.set(all_makes[:3])

            Branch.objects.get_or_create(
                merchant=merchant,
                name=b_name,
                defaults={
                    'address_text': merchant.address_text,
                    'latitude': merchant.latitude,
                    'longitude': merchant.longitude,
                    'contact_phone': merchant.phone_number,
                    'email': merchant.email,
                    'is_main': True,
                }
            )

        log(f"Merchants seeded: {Merchant.objects.count()} merchants")
    except Exception as e:
        log(f"Merchant seed error: {e}")

    # 5. Deals
    try:
        from deals.models import Deal
        from merchants.models import Merchant, Category

        now = timezone.now()

        merchants = {m.slug: m for m in Merchant.objects.all()}
        categories = {c.id: c for c in Category.objects.all()}

        deals_data = [
            {
                'id': 1,
                'merchant': merchants.get('speedy-auto-service'),
                'category': categories.get(1),
                'title': 'Comprehensive 10,000 KM Maintenance Package',
                'slug': 'comprehensive-10000-km-maintenance-package',
                'description': 'Complete vehicle maintenance including 30-point safety check, brake pads check, spark plugs inspection, filter review, and computerized diagnostic report.',
                'original_price': Decimal('850.00'),
                'discount_price': Decimal('499.00'),
                'start_datetime': now - timedelta(days=5),
                'end_datetime': now + timedelta(days=90),
                'status': 'active',
                'deal_type': 'service',
                'urgency_level': 'high',
                'is_featured': True,
                'is_trending': True,
                'is_flash_sale': False,
                'terms_and_conditions': 'Valid for all passenger sedans and SUVs. Prior appointment required.',
                'redemption_instructions': 'Present coupon QR code at service desk upon arrival.',
            },
            {
                'id': 2,
                'merchant': merchants.get('elite-detailing-studio'),
                'category': categories.get(2),
                'title': 'Premium Diamond Ceramic Coating & Full Detail',
                'slug': 'premium-diamond-ceramic-coating-full-detail',
                'description': 'Multi-stage paint correction followed by 9H dual-layer ceramic coating with 2-year warranty, plus complete deep interior conditioning.',
                'original_price': Decimal('2500.00'),
                'discount_price': Decimal('1299.00'),
                'start_datetime': now - timedelta(days=3),
                'end_datetime': now + timedelta(days=60),
                'status': 'active',
                'deal_type': 'service',
                'urgency_level': 'flash',
                'is_featured': True,
                'is_trending': True,
                'is_flash_sale': True,
                'terms_and_conditions': 'Requires vehicle drop-off for 24 hours. Valid for all vehicle sizes.',
                'redemption_instructions': 'Book appointment 48 hours in advance via phone or WhatsApp.',
            },
            {
                'id': 3,
                'merchant': merchants.get('quick-lube-tire-express'),
                'category': categories.get(4),
                'title': 'Mobil 1 Full Synthetic Oil Change + 20-Point Inspection',
                'slug': 'mobil-1-synthetic-oil-change-inspection',
                'description': 'Up to 5 liters of premium Mobil 1 5W-30 fully synthetic oil, genuine oil filter, and complementary 20-point mechanical safety check.',
                'original_price': Decimal('480.00'),
                'discount_price': Decimal('299.00'),
                'start_datetime': now - timedelta(days=7),
                'end_datetime': now + timedelta(days=90),
                'status': 'active',
                'deal_type': 'maintenance',
                'urgency_level': 'medium',
                'is_featured': True,
                'is_trending': True,
                'is_flash_sale': False,
                'terms_and_conditions': 'Extra liters billed separately at regular rate. Filter replacement included.',
                'redemption_instructions': 'Drive-in service available, no appointment necessary.',
            },
            {
                'id': 4,
                'merchant': merchants.get('quick-lube-tire-express'),
                'category': categories.get(3),
                'title': '4-Wheel Laser Alignment & High-Speed Balancing',
                'slug': '4-wheel-laser-alignment-high-speed-balancing',
                'description': 'Precision computerized 4-wheel alignment and dynamic tire balancing to ensure smooth steering, improved fuel efficiency, and even tread wear.',
                'original_price': Decimal('350.00'),
                'discount_price': Decimal('179.00'),
                'start_datetime': now - timedelta(days=2),
                'end_datetime': now + timedelta(days=60),
                'status': 'active',
                'deal_type': 'service',
                'urgency_level': 'low',
                'is_featured': True,
                'is_trending': False,
                'is_flash_sale': False,
                'terms_and_conditions': 'Valid for all passenger cars and SUVs with wheel sizes up to 21 inches.',
                'redemption_instructions': 'Present coupon at reception.',
            },
            {
                'id': 5,
                'merchant': merchants.get('german-auto-care'),
                'category': categories.get(5),
                'title': 'Front & Rear Ceramic Brake Pad Replacement',
                'slug': 'front-rear-ceramic-brake-pad-replacement',
                'description': 'High performance low-dust ceramic brake pads installation with rotor resurfacing and brake fluid flush.',
                'original_price': Decimal('1100.00'),
                'discount_price': Decimal('649.00'),
                'start_datetime': now - timedelta(days=4),
                'end_datetime': now + timedelta(days=75),
                'status': 'active',
                'deal_type': 'maintenance',
                'urgency_level': 'high',
                'is_featured': True,
                'is_trending': False,
                'is_flash_sale': False,
                'terms_and_conditions': 'Includes parts and labor for front and rear axles.',
                'redemption_instructions': 'Advance reservation recommended.',
            },
        ]

        for d_data in deals_data:
            d_id = d_data.pop('id')
            if d_data['merchant'] and d_data['category']:
                deal = Deal.objects.filter(id=d_id).first()
                if not deal:
                    deal = Deal.objects.filter(slug=d_data['slug']).first()
                if not deal:
                    Deal.objects.create(id=d_id, **d_data)
                else:
                    for k, v in d_data.items():
                        setattr(deal, k, v)
                    deal.save()

        log(f"Deals seeded: {Deal.objects.count()} deals")
    except Exception as e:
        log(f"Deal seed error: {e}")

    # 6. Info Pages (Legal & Content)
    try:
        from pages.models import InfoPage

        pages_data = [
            (
                "about",
                "About Cars Empire",
                "<h3>Welcome to Cars Empire</h3><p>Cars Empire is Egypt's leading digital marketplace connecting car owners with certified automotive service providers, workshops, and verified parts dealers. Our mission is to make vehicle maintenance transparent, affordable, and accessible to everyone.</p>"
            ),
            (
                "terms-and-conditions",
                "Terms & Conditions",
                "<h3>Terms and Conditions</h3><p>By accessing and using Cars Empire, you agree to comply with our user agreement, merchant participation guidelines, and fair pricing commitments. Coupons purchased through the platform must be redeemed prior to their stated expiration date.</p>"
            ),
            (
                "privacy-policy",
                "Privacy Policy",
                "<h3>Privacy Policy</h3><p>Cars Empire respects your privacy and is dedicated to protecting your personal data. We utilize industry-standard encryption for all transactions and never share your vehicle or payment details with unauthorized third parties.</p>"
            ),
            (
                "refund-policy",
                "Refund & Return Policy",
                "<h3>Refund Policy</h3><p>We guarantee a hassle-free 100% refund on unredeemed coupons requested within 14 days of purchase. If a merchant fails to honor a verified coupon, our support team will instantly issue a full platform credit or refund to your original payment method.</p>"
            ),
        ]

        for slug, title, content in pages_data:
            InfoPage.objects.update_or_create(
                slug=slug,
                defaults={'title': title, 'content': content, 'is_active': True}
            )

        log(f"Info pages seeded: {InfoPage.objects.count()} pages")
    except Exception as e:
        log(f"InfoPage seed error: {e}")

    # 7. Page Adverts
    try:
        from merchants.models import PageAdvert
        PageAdvert.objects.get_or_create(
            page_type='home',
            defaults={'title': 'Cars Empire Exclusive Automotive Deals', 'is_active': True}
        )
        PageAdvert.objects.get_or_create(
            page_type='merchant',
            defaults={'title': 'Certified Auto Service Centers in Cairo & Giza', 'is_active': True}
        )
        log("Page adverts seeded successfully.")
    except Exception as e:
        log(f"Page advert seed note: {e}")

    log("Demo data seeding completed successfully!")
