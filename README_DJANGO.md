# Aunt Enid Campaign - Django Web Application

A dynamic Django web application for Enid Origumisiriza Atuheire (Aunt Enid), an aspiring Woman Member of Parliament for Kabale District 2026-2031. This application converts the original static HTML website into a fully dynamic, content-manageable Django application.

## 🌟 Features

### Dynamic Content Management
- **News Articles**: Create, edit, and manage news articles through Django admin
- **Manifesto Items**: Dynamic manifesto sections with customizable content
- **Core Values**: Manageable core values section
- **Kabale Features**: Dynamic Kabale District information
- **Site Configuration**: Centralized site-wide settings management
- **Contact Messages**: Contact form submissions management

### Admin Interface
- **Django Admin**: Full-featured admin interface for content management
- **User-friendly**: Easy-to-use interface for non-technical users
- **Media Management**: Upload and manage images through admin
- **Content Organization**: Categorized and organized content management

### Technical Features
- **Responsive Design**: Mobile-first responsive design
- **SEO Optimized**: Meta tags, Open Graph, Twitter Cards, Sitemap
- **Security**: CSRF protection, input validation, secure headers
- **Performance**: Optimized queries, static file serving
- **Database**: SQLite for development, easily configurable for production

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 5.0+
- Pillow (for image handling)

### Installation

1. **Clone/Download the project**
   ```bash
   # The project is already set up in your current directory
   cd "C:\Users\matsi\Documents\trial\official aunt enid"
   ```

2. **Install dependencies**
   ```bash
   pip install django pillow
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Populate initial data**
   ```bash
   python manage.py populate_data
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/
   - Admin credentials: Username: `admin`, Password: `admin123`

## 📁 Project Structure

```
aunt_enid_campaign/
├── aunt_enid_campaign/          # Django project settings
│   ├── __init__.py
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
├── website/                     # Main Django app
│   ├── models.py                # Database models
│   ├── views.py                 # View functions
│   ├── urls.py                  # App URL patterns
│   ├── admin.py                 # Admin configuration
│   ├── forms.py                 # Form definitions
│   ├── context_processors.py   # Template context processors
│   └── management/
│       └── commands/
│           └── populate_data.py # Data population command
├── templates/                   # Django templates
│   └── website/
│       ├── base.html           # Base template
│       ├── home.html           # Homepage
│       ├── article_detail.html # Article detail page
│       ├── contact.html        # Contact page
│       ├── news_list.html      # News listing
│       ├── about.html          # About page
│       ├── manifesto.html      # Manifesto page
│       ├── kabale.html         # Kabale District page
│       ├── sitemap.xml         # XML sitemap
│       └── robots.txt          # Robots.txt
├── static/                     # Static files
│   ├── css/
│   │   └── styles.css          # Main stylesheet
│   ├── js/
│   │   ├── script.js           # Main JavaScript
│   │   └── security.js         # Security features
│   └── images/                 # Static images
├── media/                      # User uploaded files
├── manage.py                   # Django management script
└── db.sqlite3                  # SQLite database
```

## 🎛️ Admin Interface

### Accessing Admin
1. Go to http://127.0.0.1:8000/admin/
2. Login with username: `admin`, password: `admin123`

### Managing Content

#### News Articles
- **Create**: Add new news articles with title, content, images
- **Edit**: Modify existing articles
- **Categories**: Organize articles by category
- **Featured**: Mark articles as featured for homepage display
- **Publishing**: Control publication status and dates

#### Site Configuration
- **Site Information**: Update site name, taglines, descriptions
- **Contact Info**: Manage phone, email, location details
- **Social Media**: Update social media links
- **Content**: Modify about section, manifesto descriptions

#### Manifesto Items
- **Add Items**: Create new manifesto points
- **Icons**: Choose from predefined FontAwesome icons
- **Order**: Set display order
- **Points**: Add bullet points for each manifesto item

#### Core Values & Kabale Features
- **Manage**: Add, edit, or remove core values and Kabale features
- **Order**: Control display order
- **Icons**: Select appropriate icons

## 🔧 Configuration

### Settings (aunt_enid_campaign/settings.py)
- **DEBUG**: Set to False for production
- **ALLOWED_HOSTS**: Add your domain for production
- **SECRET_KEY**: Change for production (keep secret!)
- **DATABASES**: Configure for your database
- **STATIC/MEDIA**: Configure file serving

### Environment Variables (Recommended for Production)
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## 📱 Content Management

### Adding News Articles
1. Go to Admin → News Articles → Add
2. Fill in:
   - Title
   - Slug (auto-generated from title)
   - Excerpt (short description)
   - Content (full article)
   - Category
   - Location
   - Featured Image (optional)
   - Publication settings

### Updating Site Information
1. Go to Admin → Site Configuration
2. Update:
   - Site name and taglines
   - Contact information
   - Social media links
   - About section content
   - Kabale District information

### Managing Manifesto
1. Go to Admin → Manifesto Items
2. Add/edit items with:
   - Title and description
   - Icon selection
   - Bullet points list
   - Display order

## 🚀 Deployment

### Production Checklist
- [ ] Set DEBUG = False
- [ ] Update SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up production database
- [ ] Configure static/media file serving
- [ ] Set up SSL certificate
- [ ] Configure email settings
- [ ] Set up backup strategy

### Recommended Hosting Platforms
- **Heroku**: Easy Django deployment
- **DigitalOcean**: VPS with Django
- **AWS**: Scalable cloud hosting
- **PythonAnywhere**: Django-specific hosting

### Static Files for Production
```bash
python manage.py collectstatic
```

## 🔒 Security Features

- **CSRF Protection**: Built-in Django CSRF protection
- **Input Validation**: Form validation and sanitization
- **Secure Headers**: XSS protection, content type options
- **Admin Security**: Secure admin interface
- **File Upload Security**: Image validation and size limits

## 📊 SEO Features

- **Meta Tags**: Dynamic meta descriptions and titles
- **Open Graph**: Social media sharing optimization
- **Twitter Cards**: Twitter sharing optimization
- **Sitemap**: Automatic XML sitemap generation
- **Robots.txt**: Search engine crawling instructions
- **URL Structure**: SEO-friendly URLs with slugs

## 🎨 Customization

### Styling
- Edit `static/css/styles.css` for styling changes
- Maintains original design with NRM colors (green/yellow)
- Responsive design for all devices

### Templates
- Modify templates in `templates/website/`
- Base template for consistent layout
- Individual page templates for specific content

### JavaScript
- `static/js/script.js`: Main functionality
- `static/js/security.js`: Security features
- Share functionality and mobile navigation

## 📞 Support

### Technical Support
- Email: matsikojohnsonf@gmail.com
- Phone: +256 705 357 149

### Documentation
- Django Documentation: https://docs.djangoproject.com/
- Django Admin: https://docs.djangoproject.com/en/stable/ref/contrib/admin/

## 🔄 Migration from Static Site

The Django application includes all content from the original static website:
- ✅ All news articles migrated
- ✅ Manifesto content preserved
- ✅ About section maintained
- ✅ Contact information updated
- ✅ Images and styling preserved
- ✅ Social media links maintained

## 📈 Future Enhancements

### Potential Features
- **Newsletter**: Email subscription system
- **Events**: Event management and calendar
- **Gallery**: Photo gallery management
- **Donations**: Online donation system
- **Volunteers**: Volunteer registration
- **Analytics**: Google Analytics integration
- **Multi-language**: Support for local languages

---

**Built with ❤️ for Aunt Enid's Campaign**

*Empowering communities, building futures, and creating lasting positive change for the people of Kabale District through dynamic, modern web technology.*

---

**Last Updated**: September 25, 2025  
**Version**: Django v1.0  
**Status**: ✅ Ready for Production
