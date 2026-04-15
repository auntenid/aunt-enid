from django.core.management.base import BaseCommand
from django.utils import timezone
from website.models import (
    NewsArticle, ManifestoItem, CoreValue, 
    KabaleFeature, SiteConfiguration
)


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
                'kabale_description': 'Kabale, often called the "Switzerland of Africa" because of its cool climate and rolling green hills, is a district that shows how resilience and determination can shape destiny. From the hills of Kabale comes a message: No matter how tough the environment, with resilience, unity, and vision, one can turn challenges into stepping stones toward greatness.',
                'footer_description': 'Empowering Kabale District through compassionate leadership and inclusive development.',
                'copyright_text': '2025 Aunt Enid Campaign. All rights reserved.',
            }
        )
        
        if created:
            self.stdout.write('✓ Site configuration created')
        else:
            self.stdout.write('✓ Site configuration already exists')

        # Create core values
        core_values_data = [
            {
                'title': 'Compassion',
                'icon': 'heart',
                'description': 'Leading with empathy and understanding',
                'order': 1
            },
            {
                'title': 'Integrity',
                'icon': 'handshake',
                'description': 'Transparent and accountable leadership',
                'order': 2
            },
            {
                'title': 'Inclusivity',
                'icon': 'users',
                'description': 'Representing all voices in our community',
                'order': 3
            },
            {
                'title': 'Innovation',
                'icon': 'lightbulb',
                'description': 'Creative solutions for our challenges',
                'order': 4
            }
        ]
        
        for value_data in core_values_data:
            value, created = CoreValue.objects.get_or_create(
                title=value_data['title'],
                defaults=value_data
            )
            if created:
                self.stdout.write(f'✓ Core value "{value.title}" created')

        # Create manifesto items
        manifesto_data = [
            {
                'title': 'Education & Youth Empowerment',
                'icon': 'graduation-cap',
                'description': 'Empowering the next generation through quality education and opportunities',
                'points': [
                    'Improve access to quality education for all children',
                    'Support vocational training programs',
                    'Create youth employment opportunities',
                    'Establish mentorship programs'
                ],
                'order': 1
            },
            {
                'title': 'Women Empowerment',
                'icon': 'female',
                'description': 'Advancing women\'s rights and opportunities in Kabale District',
                'points': [
                    'Advocate for women\'s rights and opportunities',
                    'Support women-led businesses and cooperatives',
                    'Improve maternal and child healthcare',
                    'Create platforms for women\'s voices'
                ],
                'order': 2
            },
            {
                'title': 'Agriculture & Food Security',
                'icon': 'leaf',
                'description': 'Modernizing agriculture for sustainable food production',
                'points': [
                    'Modernize farming practices and technology',
                    'Support agricultural cooperatives',
                    'Improve market access for farmers',
                    'Promote sustainable farming methods'
                ],
                'order': 3
            },
            {
                'title': 'Infrastructure Development',
                'icon': 'road',
                'description': 'Building essential infrastructure for development',
                'points': [
                    'Improve road networks and connectivity',
                    'Enhance healthcare facilities',
                    'Develop clean water projects',
                    'Expand electricity access'
                ],
                'order': 4
            },
            {
                'title': 'Economic Development',
                'icon': 'chart-line',
                'description': 'Creating opportunities for economic growth',
                'points': [
                    'Attract investment to Kabale District',
                    'Support small and medium enterprises',
                    'Develop tourism potential',
                    'Create job opportunities'
                ],
                'order': 5
            },
            {
                'title': 'Community Security',
                'icon': 'shield-alt',
                'description': 'Ensuring safety and security for all residents',
                'points': [
                    'Strengthen community policing',
                    'Address domestic violence issues',
                    'Promote peace and unity',
                    'Support vulnerable populations'
                ],
                'order': 6
            }
        ]
        
        for manifesto_data_item in manifesto_data:
            manifesto, created = ManifestoItem.objects.get_or_create(
                title=manifesto_data_item['title'],
                defaults=manifesto_data_item
            )
            if created:
                self.stdout.write(f'✓ Manifesto item "{manifesto.title}" created')

        # Create Kabale features
        kabale_features_data = [
            {
                'title': 'Natural Beauty & Education',
                'icon': 'mountain',
                'description': 'Blessed with stunning landscapes and fertile soils, Beyond farming, Kabale\'s story is one of education and transformation. Despite humble beginnings, the district has produced some of Uganda\'s finest leaders, entrepreneurs, and scholars, proving that greatness can rise from the hills. Institutions like Kigezi College Butobere and Kabale University have become centers of hope, nurturing young minds who dream far beyond their villages.',
                'order': 1
            },
            {
                'title': 'Strong Community',
                'icon': 'users',
                'description': 'Kabale also teaches a lesson in unity and identity. The Bakiga people, known for their hard work and strength, carry a culture of resilience that inspires Uganda and Africa at large. Their dances, energy, and determination are a reminder that no obstacle is too steep to climb.',
                'order': 2
            },
            {
                'title': 'Strategic Location',
                'icon': 'map-marker-alt',
                'description': 'Kabale District sits in a golden spot in southwestern Uganda, right next to Rwanda and close to the DRC. It is a gateway for trade, tourism, and culture. With its rolling green hills, cool climate, and Lake Bunyonyi\'s beauty, Kabale is not just Uganda\'s potato basket but also a door to international markets and world-class tourism. From here, roads lead to Rwanda, Burundi, and beyond—making Kabale a place where nature, culture, and opportunity meet.',
                'order': 3
            },
            {
                'title': 'Agricultural Potential',
                'icon': 'seedling',
                'description': 'Decades ago, Kabale was seen mainly as a remote highland area, difficult to access, with steep hills that made farming hard. But the people of Kabale refused to be limited by the land. Instead, they turned the challenge into strength. They mastered the art of terrace farming, carving steps into the mountainsides and making them bloom with Irish potatoes, sorghum, beans, and vegetables. Today, Kabale is recognized as Uganda\'s potato basket and a leader in sustainable farming.',
                'order': 4
            }
        ]
        
        for feature_data in kabale_features_data:
            feature, created = KabaleFeature.objects.get_or_create(
                title=feature_data['title'],
                defaults=feature_data
            )
            if created:
                self.stdout.write(f'✓ Kabale feature "{feature.title}" created')

        # Create news articles
        news_articles_data = [
            {
                'title': 'The Lasting Case for Aunt Enid',
                'slug': 'the-lasting-case-for-aunt-enid',
                'excerpt': 'Before she ever took her seat in Parliament, Hon. Enid Origumisiriza — fondly called Aunt Enid — had already written her story in the hearts of many. Through community projects, uplifting radio programs, and her tireless support for the needy, she gave hope where despair lingered.',
                'content': '''Long before the title "Honourable" was added before her name, Enid Origumisiriza was already known in villages, homes, and marketplaces as a beacon of service. To the mothers who had once struggled silently, she was the one who came with listening ears and practical solutions. To the youth wandering without direction, she was the one who saw not only their struggles but also their potential. And to children who thought their voices were too small to be heard, she was the one who whispered back: "Your gift matters."

Her work began humbly — reaching out to families in need, supporting widows, and creating safe spaces where women could learn skills and find empowerment. Enid believed that the strength of a community is found in its women, and by uplifting them, she uplifted entire households. Many small businesses that stand today carry her fingerprints, planted as seeds of encouragement and nurtured with guidance.

But her compassion was never limited to economic empowerment. On radio, her voice became a constant companion in homes. Through programs filled with encouragement, advice, and practical wisdom, she reached even those she could not meet physically. Listeners did not just hear a host — they heard a sister, a mentor, and a friend who cared deeply about their well-being.

For young people, Aunt Enid saw possibilities where others saw only barriers. She championed entrepreneurial initiatives, teaching skills, instilling confidence, and opening doors to opportunities. Each project she started was not just about financial gain but about dignity — giving young people the ability to dream bigger and to take charge of their own futures.

Perhaps one of her most treasured legacies is the Children of the Word program. In it, she created a space where children and teenagers could explore their God-given talents. Whether in singing, storytelling, sports, or leadership, she encouraged them to shine. To Enid, every child was a promise, and nurturing that promise was her sacred duty.

Her impact did not come with pomp or self-promotion. Instead, it came through selfless service, consistent presence, and genuine love for people. She gave, not because she had plenty, but because she believed that true abundance is measured by how many lives you touch.

Now, as she steps into greater responsibility in Parliament, the community looks back at her track record and forward with expectation. For they know that Aunt Enid is not a new leader — she is a trusted hand, a proven servant, a voice that has long spoken for the voiceless.

Ogu murundi ni Aunt Enid — this time, once again, it is Aunt Enid. And her story of compassion, leadership, and community progress is still being written.''',
                'category': 'leadership',
                'location': 'Kabale District',
                'published_date': timezone.datetime(2025, 9, 25),
                'is_featured': True
            },
            {
                'title': 'President Museveni\'s Historic Nomination',
                'slug': 'president-museveni-historic-nomination',
                'excerpt': 'Hon. Enid Origumisiriza Atuheire joined thousands of NRM supporters at Kololo to celebrate the official nomination of H.E. President Yoweri Kaguta Museveni as the NRM presidential candidate for the 2026 elections — a historic moment of unity, strength, and renewed commitment to Uganda\'s future.',
                'content': '''Hon. Enid Origumisiriza Atuheire joined thousands of NRM supporters at Kololo to celebrate the official nomination of H.E. President Yoweri Kaguta Museveni as the NRM presidential candidate for the 2026 elections — a historic moment of unity, strength, and renewed commitment to Uganda's future.

HON. ENID ORIGUMISIRIZA ATUHEIRE JOINED THOUSANDS TO WITNESS PRESIDENT MUSEVENI'S HISTORIC NOMINATION

Yesterday, Hon. Enid Origumisiriza Atuheire, the NRM flag bearer for Kabale District Woman Member of Parliament, joined thousands of jubilant supporters at Kololo Independence Grounds to witness a landmark moment in Uganda's political history.

The atmosphere was electric as H.E. President Yoweri Kaguta Museveni made a grand, signature entrance following his official nomination as NRM's presidential candidate for the 2026 General Elections.

Draped in yellow, party supporters from all corners of the country gathered in solidarity, waving flags and singing songs that echoed the strength and resilience of the National Resistance Movement (NRM). The celebration symbolized the party's enduring legacy and its unwavering vision for Uganda's continued transformation.

Hon. Enid Origumisiriza Atuheire's presence at Kololo reaffirmed her commitment to the NRM's core values — peace, stability, and inclusive development — and her unwavering support for the leadership of President Museveni, under whom Uganda has made remarkable progress since 1986.

As the nation gears up for the 2026 general elections, Hon. Enid stands firm with the people of Kabale and the NRM family, ready to deliver servant leadership, unity, and progress.

#NRM2026
#EnidForKabale
#SteadyProgress
#TogetherWeMove''',
                'category': 'nrm_event',
                'location': 'Kololo Independence Grounds',
                'published_date': timezone.datetime(2025, 9, 23),
                'is_featured': True
            },
            {
                'title': 'Clarification on False Reports Circulating Online',
                'slug': 'clarification-on-false-reports-circulating-online',
                'excerpt': 'We wish to clarify that the information circulating on social media regarding the alleged storming of Buhara Police Post by residents of Kiringa village is false and misleading.',
                'content': '''We wish to clarify that the information circulating on social media regarding the alleged storming of Buhara Police Post by residents of Kiringa village is false and misleading.

CLARIFICATION ON FALSE REPORTS CIRCULATING ONLINE

We have taken note of a misleading article currently circulating on social media under the headline: "Residents Storm Buhara Police Post, Secure Release of Arrested Village Leader."

This claim is entirely false and appears to be a deliberate attempt to mislead the public, cause unnecessary alarm, and discredit our team. At no point did any Hon. Enid Origumisiriza Atuheire aka Aunt Enid get involved in such activities. All activities and engagements by our team and supporters have remained peaceful, lawful, and grounded in respect for due process.

We are aware that such misinformation is part of an ongoing pattern of intimidation, targeted against our team — a pattern that has included bullying, threats, and attempts to sow division within the community. Despite these provocations, we have chosen a path of discipline, unity, and focus on the bigger picture: representing the will of the people in the upcoming general elections.

Let it be clear: we are not shaken. The people know the truth, and they know who stands for transparency, development, and genuine leadership.

We urge our supporters and the wider public to disregard such propaganda, and instead stand firm in support of peaceful, honest politics. We remain committed to engaging voters with respect, listening to their concerns, and building a leadership that is inclusive and people-centered.

Let us rise above falsehoods — and walk forward, together, with truth and integrity.

#Owaboona
#Omutashorora
#EirakaRyaitu
#AuntEnid''',
                'category': 'clarification',
                'location': 'Buhara, Kabale District',
                'published_date': timezone.datetime(2025, 9, 24),
                'is_featured': True
            },
            {
                'title': 'Successful Campaign Rally in Kabale Town',
                'slug': 'successful-campaign-rally-in-kabale-town',
                'excerpt': 'Aunt Enid addressed thousands of supporters at the main square, sharing her vision for Kabale District\'s future and listening to community concerns.',
                'content': '''Aunt Enid addressed thousands of supporters at the main square, sharing her vision for Kabale District's future and listening to community concerns. The rally was a tremendous success with enthusiastic participation from all age groups.

The event showcased Aunt Enid's commitment to inclusive development and her deep understanding of the district's needs. Supporters from across Kabale came together to hear her plans for education, healthcare, infrastructure, and economic development.

Key highlights of the rally included:

• Interactive Q&A sessions with community members
• Presentation of the comprehensive development plan
• Recognition of local leaders and community champions
• Launch of new community engagement initiatives

The rally demonstrated the strong support for Aunt Enid's candidacy and her vision for a prosperous Kabale District. The energy and enthusiasm of the crowd reflected the community's readiness for positive change and development.

Aunt Enid emphasized her commitment to transparent governance, community participation, and sustainable development that benefits all residents of Kabale District.

The successful rally marks another milestone in Aunt Enid's campaign to represent the people of Kabale District with integrity, dedication, and a clear vision for the future.''',
                'category': 'campaign',
                'location': 'Kabale Town',
                'published_date': timezone.datetime(2025, 9, 24),
                'is_featured': True
            },
            {
                'title': 'Women Empowerment Workshop Launched',
                'slug': 'women-empowerment-workshop-launched',
                'excerpt': 'Aunt Enid launched a series of workshops aimed at empowering women entrepreneurs in Kabale District with business skills and financial literacy.',
                'content': '''Aunt Enid launched a series of workshops aimed at empowering women entrepreneurs in Kabale District with business skills and financial literacy. The initiative represents a significant step forward in promoting gender equality and economic empowerment.

The workshops cover essential topics including:

• Business planning and strategy development
• Financial management and budgeting
• Marketing and customer relations
• Digital literacy and online business
• Leadership and communication skills
• Access to funding and microfinance

Over 200 women from across Kabale District have already registered for the first phase of workshops, demonstrating the strong demand for such programs in the community.

Aunt Enid emphasized that empowering women is not just about individual success, but about strengthening entire communities and driving sustainable development. When women have access to education, resources, and opportunities, everyone benefits.

The workshops are designed to be practical and hands-on, with real-world applications that participants can immediately implement in their businesses and daily lives.

This initiative aligns with Aunt Enid's broader vision of inclusive development that ensures no one is left behind, particularly women who have historically faced barriers to economic participation.

The program includes mentorship opportunities, networking events, and ongoing support to ensure long-term success for participants.''',
                'category': 'women_empowerment',
                'location': 'Kabale District',
                'published_date': timezone.datetime(2025, 9, 24),
                'is_featured': True
            },
            {
                'title': 'Youth Engagement Forum',
                'slug': 'youth-engagement-forum',
                'excerpt': 'Aunt Enid met with youth leaders to discuss employment opportunities, education access, and youth participation in community development.',
                'content': '''Aunt Enid met with youth leaders to discuss employment opportunities, education access, and youth participation in community development. The forum provided a platform for young people to voice their concerns and share their vision for Kabale District's future.

Key topics discussed included:

• Creating more job opportunities for young people
• Improving access to quality education and vocational training
• Supporting youth entrepreneurship and innovation
• Enhancing youth participation in local governance
• Addressing challenges faced by young people in rural areas
• Promoting digital literacy and technology skills

The forum highlighted the critical role that young people play in driving development and innovation. Aunt Enid emphasized her commitment to creating an environment where youth can thrive and contribute meaningfully to society.

Participants shared their experiences and challenges, providing valuable insights into the needs and aspirations of young people in Kabale District. The discussion revealed a strong desire for:

• Better infrastructure and connectivity
• Access to modern technology and digital resources
• Support for creative and innovative projects
• Opportunities for skills development and training
• Platforms for youth leadership and civic engagement

Aunt Enid committed to establishing regular youth forums and creating a youth advisory council to ensure that young people's voices are heard in policy-making and development planning.

The forum concluded with concrete action plans for youth development initiatives, including mentorship programs, skills training workshops, and support for youth-led community projects.''',
                'category': 'youth_development',
                'location': 'Kabale District',
                'published_date': timezone.datetime(2025, 9, 24),
                'is_featured': True
            }
        ]
        
        for article_data in news_articles_data:
            article, created = NewsArticle.objects.get_or_create(
                slug=article_data['slug'],
                defaults=article_data
            )
            if created:
                self.stdout.write(f'✓ News article "{article.title}" created')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with initial data!')
        )
        self.stdout.write('You can now run the development server with: python manage.py runserver')
        self.stdout.write('Admin access: Username: admin, Password: admin123')
