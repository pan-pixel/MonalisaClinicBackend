from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone
from colorfield.fields import ColorField
import json


class LandingPageBg(models.Model):
    """Model for landing page background image or carousel"""
    TYPE_CHOICES = [
        ('static', 'Static Image'),
        ('carousel', 'Image Carousel'),
    ]
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='static')
    static_image = models.ImageField(upload_to='landing/bg/', blank=True, null=True,
                                   help_text="Single background image for landing page")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Landing Page Background"
        verbose_name_plural = "Landing Page Backgrounds"
    
    def __str__(self):
        return f"Landing Page {self.type.title()} - {'Active' if self.is_active else 'Inactive'}"


class CarouselImage(models.Model):
    """Model for carousel images"""
    landing_bg = models.ForeignKey(LandingPageBg, on_delete=models.CASCADE, related_name='carousel_images')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='landing/carousel/')
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class TeamMember(models.Model):
    """Model for team members"""
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} - {self.role}"


class PhilosophyHighlight(models.Model):
    """Model for philosophy highlights"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class AboutUs(models.Model):
    """Model for About Us content"""
    PAGE_TYPE_CHOICES = [
        ('normal', 'Normal Page'),
        ('landing', 'Landing Page'),
    ]
    
    page_type = models.CharField(max_length=10, choices=PAGE_TYPE_CHOICES, default='normal')
    
    # Normal page fields
    desp1 = models.TextField(blank=True, help_text="First description paragraph")
    desp2 = models.TextField(blank=True, help_text="Second description paragraph")
    philosophy_title = models.CharField(max_length=200, blank=True)
    
    # Landing page fields
    title1_heading = models.CharField(max_length=200, blank=True)
    title1_desp1 = models.TextField(blank=True)
    title1_desp2 = models.TextField(blank=True)
    title1_image = models.ImageField(upload_to='about/landing/', blank=True, null=True)
    
    title2_heading = models.CharField(max_length=200, blank=True)
    title2_desp1 = models.TextField(blank=True)
    title2_desp2 = models.TextField(blank=True)
    title2_image = models.ImageField(upload_to='about/landing/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About Us Content"
        verbose_name_plural = "About Us Content"
    
    def __str__(self):
        return f"About Us - {self.page_type.title()} Page"


class TreatmentCategory(models.Model):
    """Model for treatment categories"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Treatment Category"
        verbose_name_plural = "Treatment Categories"
    
    def __str__(self):
        return self.title


class TreatmentBenefit(models.Model):
    """Model for treatment benefits"""
    treatment = models.ForeignKey('Treatment', on_delete=models.CASCADE, related_name='benefits')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Treatment Benefit"
        verbose_name_plural = "Treatment Benefits"
    
    def __str__(self):
        return f"{self.treatment.name} - {self.title}"


class TreatmentStep(models.Model):
    """Model for treatment process steps (What to Expect)"""
    treatment = models.ForeignKey('Treatment', on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=200)
    description = models.TextField()
    step_number = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'step_number']
        verbose_name = "Treatment Step"
        verbose_name_plural = "Treatment Steps"
    
    def __str__(self):
        return f"{self.treatment.name} - Step {self.step_number}: {self.title}"


class Treatment(models.Model):
    """Model for individual treatments"""
    category = models.ForeignKey(TreatmentCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    duration = models.CharField(max_length=50, help_text="e.g., '60 minutes', '1-2 hours'")
    description = models.TextField()
    image = models.ImageField(upload_to='treatments/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Featured on landing page")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class TreatmentClinicPricing(models.Model):
    """Model for treatment pricing at specific clinics"""
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='clinic_pricing')
    clinic = models.ForeignKey('Clinic', on_delete=models.CASCADE, related_name='treatment_pricing')
    price = models.CharField(max_length=50, help_text="e.g., '$150', 'From $100'")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order for this clinic")
    
    class Meta:
        ordering = ['order', 'clinic__name']
        unique_together = ['treatment', 'clinic']  # Ensure one pricing per treatment-clinic combination
        verbose_name = "Treatment Clinic Pricing"
        verbose_name_plural = "Treatment Clinic Pricing"
    
    def __str__(self):
        return f"{self.treatment.name} - {self.clinic.name} - {self.price}"


class TreatmentFAQ(models.Model):
    """Model for treatment FAQs"""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Treatment FAQ"
        verbose_name_plural = "Treatment FAQs"
    
    def __str__(self):
        return self.question[:100]


class Result(models.Model):
    """Model for treatment results"""
    condition = models.CharField(max_length=200, help_text="Skin condition treated")
    duration = models.CharField(max_length=100, help_text="Treatment duration or timeline")
    description = models.TextField()
    result_image = models.ImageField(upload_to='results/', help_text="Result image showing treatment outcome")
    is_featured = models.BooleanField(default=False, help_text="Featured on landing page")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Result: {self.condition}"


class SkinConcern(models.Model):
    """Model for skin concerns"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to='skin_concerns/icons/', help_text="Icon for the concern")
    treatments = models.TextField(help_text="Related treatments information")
    products = models.TextField(help_text="Recommended products information")
    results = models.TextField(help_text="Expected results information")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class LandingFAQ(models.Model):
    """Model for landing page FAQs"""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Landing Page FAQ"
        verbose_name_plural = "Landing Page FAQs"
    
    def __str__(self):
        return self.question[:100]


class Appointment(models.Model):
    """Model for appointment bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    clinic = models.ForeignKey('Clinic', on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        ),
    ])
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    treatment_interest = models.CharField(max_length=200, blank=True,
                                        help_text="Treatment they're interested in")
    message = models.TextField(blank=True, help_text="Additional message or concerns")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Admin notes
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        clinic_name = self.clinic.name if self.clinic else 'No Clinic'
        return f"Appointment: {self.first_name} {self.last_name} - {clinic_name} - {self.preferred_date}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class ContactMessage(models.Model):
    """Model for general contact messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class Blog(models.Model):
    """Model for blog posts"""
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True, help_text="Short description of the blog post")
    author = models.CharField(max_length=100, default="Monalisa Wellness")
    featured_image = models.ImageField(upload_to='blog/featured/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Featured on landing page")
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO meta title")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    read_time = models.PositiveIntegerField(default=5, help_text="Estimated read time in minutes")
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        if not self.excerpt:
            # Auto-generate excerpt from content (first 150 characters)
            self.excerpt = self.content[:150] + "..." if len(self.content) > 150 else self.content
        super().save(*args, **kwargs)
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class BlogImage(models.Model):
    """Model for additional blog images"""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"Image for {self.blog.title}"


class WhyChooseUs(models.Model):
    """Model for Why Choose Us benefits"""
    ICON_CHOICES = [
        ('clock', 'Clock (Years of Experience)'),
        ('award', 'Award (Personalized Plans)'),
        ('zap', 'Zap (Advanced Technology)'),
        ('heart', 'Heart (Proven Results)'),
        ('shield', 'Shield'),
        ('star', 'Star'),
        ('users', 'Users'),
        ('check-circle', 'Check Circle'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default='clock')
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Why Choose Us Benefit"
        verbose_name_plural = "Why Choose Us Benefits"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Check if there are already 4 active items (excluding current instance)
            active_count = WhyChooseUs.objects.filter(is_active=True).exclude(pk=self.pk).count()
            if active_count >= 4:
                raise ValueError("Only 4 'Why Choose Us' benefits can be active at the same time.")
        super().save(*args, **kwargs)


class Clinic(models.Model):
    """Model for clinic locations"""
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=300, help_text="Services offered")
    description = models.TextField(help_text="Detailed description of the clinic")
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    reviews_count = models.PositiveIntegerField(default=0)
    reviews_text = models.CharField(max_length=100, default="Google reviews")
    
    # Business hours
    business_hours = models.CharField(max_length=100, default="Open Daily - Closes 7:30 PM")
    hours_note = models.CharField(max_length=100, default="Call for specific timings")
    
    # Main image for listing
    main_image = models.ImageField(upload_to='clinics/main/')
    
    # Map and directions
    google_maps_url = models.URLField(help_text="Google Maps link for directions")
    map_embed_url = models.URLField(blank=True, help_text="Google Maps embed URL")
    
    # Status and ordering
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Clinic"
        verbose_name_plural = "Clinics"
    
    def __str__(self):
        return self.name


class ClinicImage(models.Model):
    """Model for clinic gallery images"""
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='clinics/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Clinic Image"
        verbose_name_plural = "Clinic Images"
    
    def __str__(self):
        return f"{self.clinic.name} - Image {self.order}"


class ClinicTeamMember(models.Model):
    """Model for clinic team members"""
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='clinics/team/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Clinic Team Member"
        verbose_name_plural = "Clinic Team Members"
    
    def __str__(self):
        return f"{self.clinic.name} - {self.name}"


class SiteSettings(models.Model):
    """Model for general site settings"""
    site_name = models.CharField(max_length=100, default="Monalisa Wellness")
    site_tagline = models.CharField(max_length=200, blank=True)
    site_description = models.TextField(blank=True)
    
    # Multiple contact information stored as JSON arrays
    contact_emails = models.JSONField(
        default=list, 
        blank=True,
        help_text="List of contact email addresses as JSON array. Example: [\"info@example.com\", \"support@example.com\"]"
    )
    contact_phones = models.JSONField(
        default=list, 
        blank=True,
        help_text="List of contact phone numbers as JSON array. Example: [\"+1-555-0123\", \"+1-555-0124\"]"
    )
    
    # Legacy fields for backward compatibility (will be deprecated)
    contact_email = models.EmailField(blank=True, help_text="Legacy field - use contact_emails instead")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Legacy field - use contact_phones instead")
    
    address = models.TextField(blank=True)
    social_facebook = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    business_hours = models.TextField(
        blank=True, 
        help_text="Business hours information. Use full format like 'Monday-Friday: 9:00 AM - 7:30 PM' to avoid formatting issues."
    )
    
    # Offers strip customization
    offers_strip_color = ColorField(
        default="#DC2626",
        help_text="Color for the offers strip banner. Default: #DC2626 (red)"
    )
    offers_strip_gradient_color = ColorField(
        default="#B91C1C",
        blank=True,
        help_text="Optional gradient color for the offers strip. If left blank, will use a darker shade of the main color."
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('Only one SiteSettings instance is allowed')
        
        # Auto-migrate legacy fields to new JSON fields if they exist and new fields are empty
        if self.contact_email and not self.contact_emails:
            self.contact_emails = [self.contact_email]
        if self.contact_phone and not self.contact_phones:
            self.contact_phones = [self.contact_phone]
            
        return super().save(*args, **kwargs)
    
    def get_contact_emails(self):
        """Get all contact emails (from both new and legacy fields)"""
        emails = []
        if self.contact_emails:
            emails.extend(self.contact_emails)
        if self.contact_email and self.contact_email not in emails:
            emails.append(self.contact_email)
        return emails
    
    def get_contact_phones(self):
        """Get all contact phone numbers (from both new and legacy fields)"""
        phones = []
        if self.contact_phones:
            phones.extend(self.contact_phones)
        if self.contact_phone and self.contact_phone not in phones:
            phones.append(self.contact_phone)
        return phones
    
    def get_primary_email(self):
        """Get the primary (first) contact email"""
        emails = self.get_contact_emails()
        return emails[0] if emails else None
    
    def get_primary_phone(self):
        """Get the primary (first) contact phone"""
        phones = self.get_contact_phones()
        return phones[0] if phones else None
    
    def add_contact_email(self, email):
        """Add a new contact email"""
        if not self.contact_emails:
            self.contact_emails = []
        if email not in self.contact_emails:
            self.contact_emails.append(email)
            
    def add_contact_phone(self, phone):
        """Add a new contact phone"""
        if not self.contact_phones:
            self.contact_phones = []
        if phone not in self.contact_phones:
            self.contact_phones.append(phone)
    
    def remove_contact_email(self, email):
        """Remove a contact email"""
        if self.contact_emails and email in self.contact_emails:
            self.contact_emails.remove(email)
            
    def remove_contact_phone(self, phone):
        """Remove a contact phone"""
        if self.contact_phones and phone in self.contact_phones:
            self.contact_phones.remove(phone)


class Testimonial(models.Model):
    """Model for Google review testimonials (screenshots)"""
    screenshot = models.ImageField(
        upload_to='testimonials/',
        help_text="Screenshot of the Google review"
    )
    user_image = models.ImageField(
        upload_to='testimonials/users/',
        blank=True,
        null=True,
        help_text="Profile picture of the reviewer (optional)"
    )
    reviewer_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name of the reviewer (optional, for SEO)"
    )
    review_text = models.TextField(
        blank=True,
        help_text="Text content of the review (optional, for SEO and accessibility)"
    )
    rating = models.PositiveIntegerField(
        default=5,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Rating out of 5 stars"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this testimonial should be displayed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        name = self.reviewer_name or "Anonymous"
        return f"{name} - {self.rating} stars"


class Offer(models.Model):
    """Model for clinic-specific offers"""
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='offers')
    header = models.CharField(max_length=200, help_text="Offer headline/title")
    description = models.TextField(help_text="Detailed description of the offer")
    image = models.ImageField(upload_to='offers/', help_text="Offer promotional image")
    
    # Offer validity
    valid_from = models.DateField(help_text="Offer start date")
    valid_until = models.DateField(help_text="Offer end date")
    
    # Display options
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Featured offer on clinic page")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
    
    def __str__(self):
        return f"{self.clinic.name} - {self.header}"
    
    @property
    def is_valid(self):
        """Check if offer is currently valid"""
        today = timezone.now().date()
        return self.valid_from <= today <= self.valid_until
    
    @property
    def days_remaining(self):
        """Get number of days remaining for the offer"""
        today = timezone.now().date()
        if today > self.valid_until:
            return 0
        return (self.valid_until - today).days
