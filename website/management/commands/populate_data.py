from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware
from website.models import (
    NewsArticle, ManifestoItem, CoreValue,
    KabaleFeature, SiteConfiguration,
    ProjectCategory, ImpactProject,
    GalleryCategory, GalleryItem,
)


def dt(year, month, day):
    """Return a timezone-aware datetime for a given date."""
    import datetime
    return make_aware(datetime.datetime(year, month, day))


class Command(BaseCommand):
    help = 'Populate the database with initial data from the original website'

    def handle(self, *args, **options):
        self.stdout.write('Starting data population...')

        # Create or update site configuration
        config, created = SiteConfiguration.objects.get_or_create(
            defaults={
                'site_name': 'Aunt Enid',
                'tagline': 'Aspiring Woman Member of Parliament',
                'subtitle': 'NRM FLAG BEARER Kabale District 2026-2031',
                'hero_description': 'A compassionate leader who empowers, connects, and transforms communities',
                'phone': '+256 705 357 149',
                'email': 'auntenid@kabale2026.com',
                'location': 'Kabale District, Uganda',
                'whatsapp': '256764195740',
                'tiktok_url': 'https://tiktok.com/@auntenid',
                'about_title': 'Who is Aunt Enid?',
                'about_subtitle': 'A dedicated community leader with a heart for service and transformation',
                'why_running': 'As a woman leader deeply rooted in Kabale District, I believe in the power of inclusive governance that uplifts every voice, especially those often unheard. Our community deserves leadership that understands the unique challenges we face and has the compassion to address them with wisdom and determination.',
                'vision': 'I envision a Kabale District where every family thrives, where women and youth are empowered, where education is accessible to all, and where our natural resources benefit our entire community. This vision drives my commitment to serve as your representative in Parliament.',
                'kabale_title': 'Kabale District',
                'kabale_subtitle': 'Our beautiful home with unlimited potential',
                'kabale_description': 'Kabale, often called the "Switzerland of Africa" because of its cool climate and rolling green hills, is a district that shows how resilience and determination can shape destiny.',
                'footer_description': 'Empowering Kabale District through compassionate leadership and inclusive development.',
                'copyright_text': '2025 Aunt Enid Campaign. All rights reserved.',
            }
        )

        if created:
            self.stdout.write('[OK] Site configuration created')
        else:
            self.stdout.write('[OK] Site configuration already exists')

        # Create core values
        core_values_data = [
            {'title': 'Compassion', 'icon': 'heart',      'description': 'Leading with empathy and understanding',            'order': 1},
            {'title': 'Integrity',  'icon': 'handshake',  'description': 'Transparent and accountable leadership',            'order': 2},
            {'title': 'Inclusivity','icon': 'users',      'description': 'Representing all voices in our community',          'order': 3},
            {'title': 'Innovation', 'icon': 'lightbulb',  'description': 'Creative solutions for our challenges',             'order': 4},
        ]
        for value_data in core_values_data:
            value, created = CoreValue.objects.get_or_create(title=value_data['title'], defaults=value_data)
            if created:
                self.stdout.write(f'[OK] Core value "{value.title}" created')

        # Create manifesto items
        manifesto_data = [
            {
                'title': 'Education & Youth Empowerment',
                'icon': 'graduation-cap',
                'description': 'Empowering the next generation through quality education and opportunities',
                'points': ['Improve access to quality education for all children', 'Support vocational training programs',
                           'Create youth employment opportunities', 'Establish mentorship programs'],
                'order': 1
            },
            {
                'title': 'Women Empowerment',
                'icon': 'female',
                'description': "Advancing women's rights and opportunities in Kabale District",
                'points': ["Advocate for women's rights and opportunities", 'Support women-led businesses and cooperatives',
                           'Improve maternal and child healthcare', "Create platforms for women's voices"],
                'order': 2
            },
            {
                'title': 'Agriculture & Food Security',
                'icon': 'leaf',
                'description': 'Modernizing agriculture for sustainable food production',
                'points': ['Modernize farming practices and technology', 'Support agricultural cooperatives',
                           'Improve market access for farmers', 'Promote sustainable farming methods'],
                'order': 3
            },
            {
                'title': 'Infrastructure Development',
                'icon': 'road',
                'description': 'Building essential infrastructure for development',
                'points': ['Improve road networks and connectivity', 'Enhance healthcare facilities',
                           'Develop clean water projects', 'Expand electricity access'],
                'order': 4
            },
            {
                'title': 'Economic Development',
                'icon': 'chart-line',
                'description': 'Creating opportunities for economic growth',
                'points': ['Attract investment to Kabale District', 'Support small and medium enterprises',
                           'Develop tourism potential', 'Create job opportunities'],
                'order': 5
            },
            {
                'title': 'Community Security',
                'icon': 'shield-alt',
                'description': 'Ensuring safety and security for all residents',
                'points': ['Strengthen community policing', 'Address domestic violence issues',
                           'Promote peace and unity', 'Support vulnerable populations'],
                'order': 6
            },
        ]
        for item_data in manifesto_data:
            manifesto, created = ManifestoItem.objects.get_or_create(title=item_data['title'], defaults=item_data)
            if created:
                self.stdout.write(f'[OK] Manifesto item "{manifesto.title}" created')

        # Create Kabale features
        kabale_features_data = [
            {
                'title': 'Natural Beauty & Education',
                'icon': 'mountain',
                'description': "Blessed with stunning landscapes and fertile soils. Beyond farming, Kabale's story is one of education and transformation. Institutions like Kigezi College Butobere and Kabale University have become centers of hope.",
                'order': 1
            },
            {
                'title': 'Strong Community',
                'icon': 'users',
                'description': 'Kabale also teaches a lesson in unity and identity. The Bakiga people, known for their hard work and strength, carry a culture of resilience that inspires Uganda and Africa at large.',
                'order': 2
            },
            {
                'title': 'Strategic Location',
                'icon': 'map-marker-alt',
                'description': "Kabale District sits in a golden spot in southwestern Uganda, right next to Rwanda and close to the DRC. It is a gateway for trade, tourism, and culture.",
                'order': 3
            },
            {
                'title': 'Agricultural Potential',
                'icon': 'seedling',
                'description': "The people of Kabale mastered the art of terrace farming, carving steps into the mountainsides. Today, Kabale is recognized as Uganda's potato basket and a leader in sustainable farming.",
                'order': 4
            },
        ]
        for feature_data in kabale_features_data:
            feature, created = KabaleFeature.objects.get_or_create(title=feature_data['title'], defaults=feature_data)
            if created:
                self.stdout.write(f'[OK] Kabale feature "{feature.title}" created')

        # =====================================================================
        # News Articles
        # Uses update_or_create so that:
        #   - On first deploy  → articles are CREATED with images
        #   - On redeploys     → existing articles are UPDATED with the correct
        #                        featured_image path so images are always visible
        # Images live in media/news_images/ which is committed to the git repo
        # and is copied to the Railway volume on every startup via settings.py.
        # =====================================================================
        news_articles_data = [
            {
                'slug': 'the-lasting-case-for-aunt-enid',
                'defaults': {
                    'title': 'The Lasting Case for Aunt Enid',
                    'excerpt': 'Before she ever took her seat in Parliament, Hon. Enid Origumisiriza — fondly called Aunt Enid — had already written her story in the hearts of many.',
                    'content': (
                        'Long before the title "Honourable" was added before her name, Enid Origumisiriza was already '
                        'known in villages, homes, and marketplaces as a beacon of service. To the mothers who had once '
                        'struggled silently, she was the one who came with listening ears and practical solutions.\n\n'
                        'Her work began humbly — reaching out to families in need, supporting widows, and creating safe '
                        'spaces where women could learn skills and find empowerment. Enid believed that the strength of '
                        'a community is found in its women, and by uplifting them, she uplifted entire households.\n\n'
                        'For young people, Aunt Enid saw possibilities where others saw only barriers. She championed '
                        'entrepreneurial initiatives, teaching skills, instilling confidence, and opening doors to '
                        'opportunities.\n\n'
                        'Perhaps one of her most treasured legacies is the Children of the Word program. In it, she '
                        'created a space where children and teenagers could explore their God-given talents.\n\n'
                        'Ogu murundi ni Aunt Enid — this time, once again, it is Aunt Enid.'
                    ),
                    'category': 'leadership',
                    'location': 'Kabale District',
                    'published_date': dt(2025, 9, 25),
                    'is_featured': True,
                    'featured_image': 'news_images/aunt-enid-story.jpg',
                }
            },
            {
                'slug': 'president-museveni-historic-nomination',
                'defaults': {
                    'title': "President Museveni's Historic Nomination",
                    'excerpt': (
                        'Hon. Enid Origumisiriza Atuheire joined thousands of NRM supporters at Kololo to celebrate '
                        'the official nomination of H.E. President Yoweri Kaguta Museveni as the NRM presidential '
                        'candidate for the 2026 elections.'
                    ),
                    'content': (
                        'Hon. Enid Origumisiriza Atuheire joined thousands of NRM supporters at Kololo to celebrate '
                        'the official nomination of H.E. President Yoweri Kaguta Museveni as the NRM presidential '
                        'candidate for the 2026 elections — a historic moment of unity and strength.\n\n'
                        'The atmosphere was electric as H.E. President Museveni made a grand entrance. Draped in '
                        'yellow, party supporters from all corners of the country gathered in solidarity.\n\n'
                        "Hon. Enid's presence reaffirmed her commitment to the NRM's core values — peace, stability, "
                        'and inclusive development.\n\n'
                        '#NRM2026 #EnidForKabale #SteadyProgress #TogetherWeMove'
                    ),
                    'category': 'nrm_event',
                    'location': 'Kololo Independence Grounds',
                    'published_date': dt(2025, 9, 23),
                    'is_featured': True,
                    'featured_image': 'news_images/museveni-nomination.jpg',
                }
            },
            {
                'slug': 'clarification-on-false-reports-circulating-online',
                'defaults': {
                    'title': 'Clarification on False Reports Circulating Online',
                    'excerpt': (
                        'We wish to clarify that the information circulating on social media regarding the alleged '
                        'storming of Buhara Police Post by residents of Kiringa village is false and misleading.'
                    ),
                    'content': (
                        'We wish to clarify that the information circulating on social media regarding the alleged '
                        'storming of Buhara Police Post by residents of Kiringa village is false and misleading.\n\n'
                        'This claim is entirely false and appears to be a deliberate attempt to mislead the public '
                        'and discredit our team. At no point did Hon. Enid Origumisiriza Atuheire aka Aunt Enid get '
                        'involved in such activities.\n\n'
                        'We urge our supporters and the wider public to disregard such propaganda, and instead stand '
                        'firm in support of peaceful, honest politics.\n\n'
                        '#Owaboona #Omutashorora #EirakaRyaitu #AuntEnid'
                    ),
                    'category': 'clarification',
                    'location': 'Buhara, Kabale District',
                    'published_date': dt(2025, 9, 24),
                    'is_featured': True,
                    'featured_image': 'news_images/buhara-clarification.jpg',
                }
            },
            {
                'slug': 'successful-campaign-rally-in-kabale-town',
                'defaults': {
                    'title': 'Successful Campaign Rally in Kabale Town',
                    'excerpt': (
                        "Aunt Enid addressed thousands of supporters at the main square, sharing her vision for "
                        "Kabale District's future and listening to community concerns."
                    ),
                    'content': (
                        "Aunt Enid addressed thousands of supporters at the main square, sharing her vision for "
                        "Kabale District's future. The rally was a tremendous success with enthusiastic participation "
                        "from all age groups.\n\n"
                        "Key highlights included interactive Q&A sessions, presentation of the development plan, "
                        "recognition of local leaders, and launch of new community engagement initiatives.\n\n"
                        "Aunt Enid emphasized her commitment to transparent governance and sustainable development "
                        "that benefits all residents of Kabale District."
                    ),
                    'category': 'campaign',
                    'location': 'Kabale Town',
                    'published_date': dt(2025, 9, 24),
                    'is_featured': True,
                    'featured_image': 'news_images/campaign-rally.jpg',
                }
            },
            {
                'slug': 'women-empowerment-workshop-launched',
                'defaults': {
                    'title': 'Women Empowerment Workshop Launched',
                    'excerpt': (
                        'Aunt Enid launched a series of workshops aimed at empowering women entrepreneurs in '
                        'Kabale District with business skills and financial literacy.'
                    ),
                    'content': (
                        'Aunt Enid launched a series of workshops aimed at empowering women entrepreneurs in '
                        'Kabale District with business skills and financial literacy.\n\n'
                        'The workshops cover essential topics including business planning, financial management, '
                        'marketing, digital literacy, leadership, and access to microfinance.\n\n'
                        'Over 200 women from across Kabale District have already registered for the first phase. '
                        'Aunt Enid emphasized that empowering women strengthens entire communities.'
                    ),
                    'category': 'women_empowerment',
                    'location': 'Kabale District',
                    'published_date': dt(2025, 9, 24),
                    'is_featured': True,
                    'featured_image': 'news_images/women-empowerment.jpg',
                }
            },
            {
                'slug': 'youth-engagement-forum',
                'defaults': {
                    'title': 'Youth Engagement Forum',
                    'excerpt': (
                        'Aunt Enid met with youth leaders to discuss employment opportunities, education access, '
                        'and youth participation in community development.'
                    ),
                    'content': (
                        'Aunt Enid met with youth leaders to discuss employment opportunities, education access, '
                        "and youth participation in community development. The forum provided a platform for young "
                        "people to voice their concerns.\n\n"
                        "Key topics discussed included creating job opportunities, improving access to education and "
                        "vocational training, supporting youth entrepreneurship, and enhancing youth participation "
                        "in local governance.\n\n"
                        "Aunt Enid committed to establishing regular youth forums and creating a youth advisory "
                        "council to ensure young people's voices are heard in policy-making."
                    ),
                    'category': 'youth_development',
                    'location': 'Kabale District',
                    'published_date': dt(2025, 9, 24),
                    'is_featured': True,
                    'featured_image': 'news_images/youth-forum.jpg',
                }
            },
        ]

        for entry in news_articles_data:
            article, created = NewsArticle.objects.update_or_create(
                slug=entry['slug'],
                defaults=entry['defaults']
            )
            action = 'created' if created else 'updated (image assigned)'
            self.stdout.write(f'[OK] News article "{article.title}" {action}')

        # ==================== Project Categories ====================
        project_categories_data = [
            {'name': 'Women & Youth Empowerment', 'icon': 'female',     'order': 1,
             'description': 'Programs uplifting women and young people through skills training and economic opportunities.'},
            {'name': 'VSLAs & SACCOs',            'icon': 'piggy-bank', 'order': 2,
             'description': 'Support for Village Savings and Loans Associations and financial cooperatives.'},
            {'name': 'Health & Healthcare',        'icon': 'heartbeat',  'order': 3,
             'description': 'Maternal health initiatives, medical support, and healthcare access improvements.'},
            {'name': 'Agriculture & Tools',        'icon': 'seedling',   'order': 4,
             'description': 'Distribution of seeds, tools, and modern farming support to local farmers.'},
        ]
        categories_map = {}
        for cat_data in project_categories_data:
            cat, created = ProjectCategory.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
            categories_map[cat_data['name']] = cat
            if created:
                self.stdout.write(f'[OK] Project category "{cat.name}" created')

        # ==================== Impact Projects ====================
        import datetime
        impact_projects_data = [
            {
                'title': 'Women Business Skills Training - Kabale Town',
                'category_name': 'Women & Youth Empowerment',
                'excerpt': 'Over 200 women received hands-on business skills training including financial management, marketing, and leadership.',
                'description': 'Aunt Enid organized practical business skills workshops for women entrepreneurs across Kabale District. Participants received training in business planning, financial literacy, digital skills, and cooperative management.',
                'location': 'Kabale Town, Kabale District',
                'date_completed': datetime.date(2025, 8, 15),
                'beneficiaries': '200+ women entrepreneurs',
                'is_featured': True,
            },
            {
                'title': 'VSLA Seed Capital Support - Bufundi Sub-county',
                'category_name': 'VSLAs & SACCOs',
                'excerpt': 'Provided seed capital and training to 15 Village Savings and Loans Associations, enabling over 400 families to access affordable credit.',
                'description': 'Aunt Enid facilitated the strengthening of 15 VSLAs in Bufundi Sub-county. Each group received seed capital injections, governance training, and bookkeeping support.',
                'location': 'Bufundi Sub-county, Kabale District',
                'date_completed': datetime.date(2025, 7, 10),
                'beneficiaries': '400+ families across 15 VSLAs',
                'is_featured': True,
            },
            {
                'title': 'Sanitary Pad Distribution in Schools',
                'category_name': 'Health & Healthcare',
                'excerpt': 'Distributed sanitary pads to over 1,500 school girls across 12 schools, reducing absenteeism and keeping girls in class.',
                'description': 'Aunt Enid launched a campaign distributing sanitary pads to 1,500 school girls across 12 primary and secondary schools. The distribution was coupled with reproductive health education sessions.',
                'location': 'Various Schools, Kabale District',
                'date_completed': datetime.date(2025, 9, 1),
                'beneficiaries': '1,500+ school girls, 12 schools',
                'is_featured': True,
            },
            {
                'title': 'Irish Potato Seed Distribution - Rubanda',
                'category_name': 'Agriculture & Tools',
                'excerpt': 'Distributed certified Irish potato seeds and farming tools to 300 smallholder farmers to boost food production and incomes.',
                'description': "Aunt Enid supported 300 smallholder farming families with certified Irish potato seeds, hoes, and fertilizer. Farmers also received training on modern terrace farming, pest management, and market linkages.",
                'location': 'Rubanda, Kabale District',
                'date_completed': datetime.date(2025, 6, 20),
                'beneficiaries': '300 farming families',
                'is_featured': False,
            },
        ]

        for proj_data in impact_projects_data:
            cat_name = proj_data.pop('category_name')
            proj_data['category'] = categories_map.get(cat_name)
            project, created = ImpactProject.objects.get_or_create(title=proj_data['title'], defaults=proj_data)
            if created:
                self.stdout.write(f'[OK] Impact project "{project.title}" created')

        # ==================== Gallery Categories ====================
        gallery_categories_data = [
            {'name': 'Campaign Rallies',    'order': 1},
            {'name': 'Community Outreach',  'order': 2},
            {'name': 'Donation Drives',     'order': 3},
            {'name': 'Official Events',     'order': 4},
        ]
        for gcat_data in gallery_categories_data:
            gcat, created = GalleryCategory.objects.get_or_create(name=gcat_data['name'], defaults=gcat_data)
            if created:
                self.stdout.write(f'[OK] Gallery category "{gcat.name}" created')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with initial data!'))
        self.stdout.write('You can now run the development server with: python manage.py runserver')
        self.stdout.write('Admin access: Username: admin, Password: admin123')
