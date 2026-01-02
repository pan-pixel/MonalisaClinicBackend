from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import *


@admin.register(LandingPageBg)
class LandingPageBgAdmin(admin.ModelAdmin):
    list_display = ['type', 'is_active', 'created_at']
    list_filter = ['type', 'is_active']
    fieldsets = (
        ('General', {
            'fields': ('type', 'is_active')
        }),
        ('Static Image', {
            'fields': ('static_image', 'static_image_preview'),
            'description': 'Upload a single background image (only for static type)'
        }),
    )
    readonly_fields = ['static_image_preview']
    
    def static_image_preview(self, obj):
        if obj.static_image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 300px;" />', obj.static_image.url)
        return "No image"
    static_image_preview.short_description = "Image Preview"


class CarouselImageInline(admin.TabularInline):
    model = CarouselImage
    extra = 1
    fields = ['title', 'description', 'image', 'order', 'is_active']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'landing_bg', 'order', 'is_active']
    list_filter = ['is_active', 'landing_bg']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'order', 'is_active', 'image_preview']
    list_filter = ['is_active', 'role']
    search_fields = ['name', 'role']
    list_editable = ['order', 'is_active']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'role', 'bio')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px; border-radius: 50%;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Photo"


@admin.register(PhilosophyHighlight)
class PhilosophyHighlightAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['page_type', 'is_active', 'updated_at']
    list_filter = ['page_type', 'is_active']
    fieldsets = (
        ('Page Type', {
            'fields': ('page_type', 'is_active')
        }),
        ('Normal Page Content', {
            'fields': ('desp1', 'desp2', 'philosophy_title'),
            'description': 'Content for the regular About Us page'
        }),
        ('Landing Page - Section 1', {
            'fields': ('title1_heading', 'title1_desp1', 'title1_desp2', 'title1_image', 'title1_image_preview'),
            'description': 'First section for About Us on landing page'
        }),
        ('Landing Page - Section 2', {
            'fields': ('title2_heading', 'title2_desp1', 'title2_desp2', 'title2_image', 'title2_image_preview'),
            'description': 'Second section for About Us on landing page'
        }),
    )
    readonly_fields = ['title1_image_preview', 'title2_image_preview']
    
    def title1_image_preview(self, obj):
        if obj.title1_image:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.title1_image.url)
        return "No image"
    title1_image_preview.short_description = "Section 1 Image Preview"
    
    def title2_image_preview(self, obj):
        if obj.title2_image:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.title2_image.url)
        return "No image"
    title2_image_preview.short_description = "Section 2 Image Preview"


class TreatmentInline(admin.TabularInline):
    model = Treatment
    extra = 1
    fields = ['name', 'duration', 'is_featured', 'order', 'is_active']
    list_editable = ['order', 'is_active', 'is_featured']


class TreatmentBenefitInline(admin.TabularInline):
    model = TreatmentBenefit
    extra = 3
    fields = ['title', 'description', 'order', 'is_active']
    ordering = ['order']


class TreatmentStepInline(admin.TabularInline):
    model = TreatmentStep
    extra = 3
    fields = ['title', 'description', 'step_number', 'order', 'is_active']
    ordering = ['order', 'step_number']


@admin.register(TreatmentCategory)
class TreatmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'treatment_count']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    inlines = [TreatmentInline]
    
    def treatment_count(self, obj):
        return obj.items.count()
    treatment_count.short_description = "Treatments"


class TreatmentClinicPricingInline(admin.TabularInline):
    model = TreatmentClinicPricing
    extra = 1
    fields = ['clinic', 'price', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'duration', 'is_featured', 'order', 'is_active', 'image_preview', 'clinic_count']
    list_filter = ['category', 'is_featured', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active', 'is_featured']
    inlines = [TreatmentClinicPricingInline, TreatmentBenefitInline, TreatmentStepInline]
    fieldsets = (
        ('Category', {
            'fields': ('category',)
        }),
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Duration', {
            'fields': ('duration',)
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order', 'is_active')
        }),
    )
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image"
    
    def clinic_count(self, obj):
        return obj.clinic_pricing.filter(is_active=True).count()
    clinic_count.short_description = "Active Clinics"


@admin.register(TreatmentClinicPricing)
class TreatmentClinicPricingAdmin(admin.ModelAdmin):
    list_display = ['treatment', 'clinic', 'price', 'order', 'is_active']
    list_filter = ['is_active', 'clinic', 'treatment__category']
    search_fields = ['treatment__name', 'clinic__name', 'price']
    list_editable = ['price', 'order', 'is_active']
    fieldsets = (
        ('Treatment & Clinic', {
            'fields': ('treatment', 'clinic')
        }),
        ('Pricing', {
            'fields': ('price',)
        }),
        ('Display Options', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(TreatmentBenefit)
class TreatmentBenefitAdmin(admin.ModelAdmin):
    list_display = ['treatment', 'title', 'order', 'is_active']
    list_filter = ['is_active', 'treatment']
    search_fields = ['title', 'description', 'treatment__name']
    list_editable = ['order', 'is_active']


@admin.register(TreatmentStep)
class TreatmentStepAdmin(admin.ModelAdmin):
    list_display = ['treatment', 'title', 'step_number', 'order', 'is_active']
    list_filter = ['is_active', 'treatment']
    search_fields = ['title', 'description', 'treatment__name']
    list_editable = ['order', 'is_active']


@admin.register(TreatmentFAQ)
class TreatmentFAQAdmin(admin.ModelAdmin):
    list_display = ['question_short', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']
    
    def question_short(self, obj):
        return obj.question[:100] + "..." if len(obj.question) > 100 else obj.question
    question_short.short_description = "Question"


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['condition', 'duration', 'is_featured', 'is_active', 'created_at', 'images_preview']
    list_filter = ['is_featured', 'is_active', 'created_at']
    search_fields = ['condition', 'description']
    list_editable = ['is_featured', 'is_active']
    fieldsets = (
        ('Case Information', {
            'fields': ('condition', 'duration', 'description')
        }),
        ('Before & After Images', {
            'fields': ('before_image', 'before_preview', 'after_image', 'after_preview')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order', 'is_active')
        }),
    )
    readonly_fields = ['before_preview', 'after_preview']
    
    def before_preview(self, obj):
        if obj.before_image:
            return format_html('<img src="{}" style="max-height: 150px;" />', obj.before_image.url)
        return "No image"
    before_preview.short_description = "Before Image Preview"
    
    def after_preview(self, obj):
        if obj.after_image:
            return format_html('<img src="{}" style="max-height: 150px;" />', obj.after_image.url)
        return "No image"
    after_preview.short_description = "After Image Preview"
    
    def images_preview(self, obj):
        html = ""
        if obj.before_image:
            html += f'<img src="{obj.before_image.url}" style="max-height: 60px; margin-right: 5px;" title="Before" />'
        if obj.after_image:
            html += f'<img src="{obj.after_image.url}" style="max-height: 60px;" title="After" />'
        return format_html(html) if html else "No images"
    images_preview.short_description = "Images"


@admin.register(SkinConcern)
class SkinConcernAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'icon_preview']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Icon', {
            'fields': ('icon', 'icon_preview')
        }),
        ('Content', {
            'fields': ('treatments', 'products', 'results')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
    readonly_fields = ['icon_preview']
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="max-height: 60px;" />', obj.icon.url)
        return "No icon"
    icon_preview.short_description = "Icon"


@admin.register(LandingFAQ)
class LandingFAQAdmin(admin.ModelAdmin):
    list_display = ['question_short', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']
    
    def question_short(self, obj):
        return obj.question[:100] + "..." if len(obj.question) > 100 else obj.question
    question_short.short_description = "Question"


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'icon']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'icon')
        }),
        ('Display Options', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def get_queryset(self, request):
        # Show active benefits first, then inactive ones
        return super().get_queryset(request).order_by('-is_active', 'order')
    
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValueError as e:
            # Add a friendly error message if trying to activate more than 4 benefits
            from django.contrib import messages
            messages.error(request, str(e))
            if not change:  # If it's a new object, don't save it
                return


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'clinic', 'email', 'phone', 'preferred_date', 'preferred_time', 'status', 'created_at']
    list_filter = ['clinic', 'status', 'preferred_date', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'clinic__name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Clinic Selection', {
            'fields': ('clinic',)
        }),
        ('Client Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Appointment Details', {
            'fields': ('preferred_date', 'preferred_time', 'treatment_interest', 'message')
        }),
        ('Status & Notes', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']
    
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_confirmed.short_description = "Mark selected appointments as confirmed"
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_completed.short_description = "Mark selected appointments as completed"
    
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_cancelled.short_description = "Mark selected appointments as cancelled"


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    fields = ['image', 'caption', 'order']
    

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'is_featured', 'views_count', 'created_at', 'image_preview']
    list_filter = ['is_published', 'is_featured', 'created_at', 'author']
    search_fields = ['title', 'content', 'tags']
    list_editable = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'image_preview']
    inlines = [BlogImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'excerpt')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Featured Image', {
            'fields': ('featured_image', 'image_preview')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description', 'tags', 'read_time'),
            'classes': ('collapse',)
        }),
        ('Publication Settings', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Statistics & Timestamps', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 80px;" />', obj.featured_image.url)
        return "No image"
    image_preview.short_description = "Featured Image Preview"
    
    actions = ['mark_published', 'mark_unpublished', 'mark_featured', 'mark_unfeatured']
    
    def mark_published(self, request, queryset):
        queryset.update(is_published=True)
    mark_published.short_description = "Mark selected blogs as published"
    
    def mark_unpublished(self, request, queryset):
        queryset.update(is_published=False)
    mark_unpublished.short_description = "Mark selected blogs as unpublished"
    
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_featured.short_description = "Mark selected blogs as featured"
    
    def mark_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)
    mark_unfeatured.short_description = "Remove selected blogs from featured"


@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ['blog', 'caption', 'order', 'image_preview']
    list_filter = ['blog']
    search_fields = ['blog__title', 'caption']
    list_editable = ['order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image Preview"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    actions = ['mark_read', 'mark_unread']
    
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_read.short_description = "Mark selected messages as read"
    
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_unread.short_description = "Mark selected messages as unread"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_tagline', 'site_description')
        }),
        ('Contact Information - Multiple Contacts', {
            'fields': ('contact_emails', 'contact_phones', 'all_emails_display', 'all_phones_display'),
            'description': 'Add multiple contact emails and phone numbers as JSON arrays. Example: ["email1@domain.com", "email2@domain.com"]'
        }),
        ('Contact Information - Legacy (Single)', {
            'fields': ('contact_email', 'contact_phone'),
            'classes': ('collapse',),
            'description': 'Legacy single contact fields - will be automatically included in the multiple contacts above'
        }),
        ('Location & Business Hours', {
            'fields': ('address', 'business_hours'),
            'description': 'For business hours, use format like "Monday-Friday: 9:00 AM - 7:30 PM" to avoid formatting issues'
        }),
        ('Social Media', {
            'fields': ('social_facebook', 'social_instagram', 'social_twitter')
        }),
        ('Offers Strip Customization', {
            'fields': ('offers_strip_color', 'offers_strip_gradient_color', 'offers_strip_preview'),
            'description': 'Customize the color of the promotional offers strip at the top of the website. Use hex color codes (e.g., #DC2626 for red, #1F2937 for dark gray). If gradient color is left blank, a darker shade will be auto-generated.'
        }),
    )
    readonly_fields = ['all_emails_display', 'all_phones_display', 'offers_strip_preview']
    
    def all_emails_display(self, obj):
        """Display all contact emails in a readable format"""
        if obj:
            emails = obj.get_contact_emails()
            if emails:
                formatted_emails = "<br>".join([f"• {email}" for email in emails])
                return format_html(f"<div style='padding: 10px; background: #f8f9fa; border-radius: 4px;'><strong>All Contact Emails:</strong><br>{formatted_emails}</div>")
            return format_html("<em>No contact emails found</em>")
        return ""
    all_emails_display.short_description = "All Contact Emails (Combined)"
    
    def all_phones_display(self, obj):
        """Display all contact phone numbers in a readable format"""
        if obj:
            phones = obj.get_contact_phones()
            if phones:
                formatted_phones = "<br>".join([f"• {phone}" for phone in phones])
                return format_html(f"<div style='padding: 10px; background: #f8f9fa; border-radius: 4px;'><strong>All Contact Phones:</strong><br>{formatted_phones}</div>")
            return format_html("<em>No contact phone numbers found</em>")
        return ""
    all_phones_display.short_description = "All Contact Phones (Combined)"
    
    def offers_strip_preview(self, obj):
        """Display a preview of the offers strip color"""
        if obj:
            main_color = obj.offers_strip_color or '#DC2626'
            gradient_color = obj.offers_strip_gradient_color or '#B91C1C'
            return format_html(
                '<div style="padding: 15px; background: linear-gradient(to right, {}, {}, {}); '
                'border-radius: 4px; color: white; text-align: center; font-weight: bold; margin-top: 10px;">'
                'Offers Strip Preview<br>'
                '<small style="opacity: 0.9;">Main: {} | Gradient: {}</small>'
                '</div>',
                main_color, gradient_color, main_color,
                main_color, gradient_color
            )
        return ""
    offers_strip_preview.short_description = "Color Preview"
    
    def get_form(self, request, obj=None, **kwargs):
        """Customize the form to add help text and better widget for JSON fields"""
        form = super().get_form(request, obj, **kwargs)
        
        # Add help text for JSON fields
        if 'contact_emails' in form.base_fields:
            form.base_fields['contact_emails'].help_text = (
                'Enter email addresses as a JSON array. Example: '
                '["info@monalisaclinic.com", "support@monalisaclinic.com", "appointments@monalisaclinic.com"]'
            )
            form.base_fields['contact_emails'].widget.attrs['rows'] = 3
            
        if 'contact_phones' in form.base_fields:
            form.base_fields['contact_phones'].help_text = (
                'Enter phone numbers as a JSON array. Example: '
                '["+91-92891-57655", "+91-98765-43210", "+91-11-1234-5678"]'
            )
            form.base_fields['contact_phones'].widget.attrs['rows'] = 3
            
        if 'business_hours' in form.base_fields:
            form.base_fields['business_hours'].help_text = (
                'Use complete time format to avoid display issues. Example: '
                '"Monday-Friday: 9:00 AM - 7:30 PM\\nSaturday-Sunday: 10:00 AM - 6:00 PM\\nCall for specific timings"'
            )
            form.base_fields['business_hours'].widget.attrs['rows'] = 4
        
        # ColorField automatically provides a color picker widget, so we just need to add help text
        if 'offers_strip_color' in form.base_fields:
            form.base_fields['offers_strip_color'].help_text = (
                'Click the color box to open a color picker. Default: #DC2626 (red)'
            )
            
        if 'offers_strip_gradient_color' in form.base_fields:
            form.base_fields['offers_strip_gradient_color'].help_text = (
                'Optional: Click the color box to pick a gradient color. If left blank, a darker shade of the main color will be auto-generated.'
            )
        
        return form
    
    def save_model(self, request, obj, form, change):
        """Override save to ensure proper migration of legacy fields"""
        # Auto-migrate legacy fields if new fields are empty
        if hasattr(obj, 'contact_email') and obj.contact_email and not obj.contact_emails:
            obj.contact_emails = [obj.contact_email]
        if hasattr(obj, 'contact_phone') and obj.contact_phone and not obj.contact_phones:
            obj.contact_phones = [obj.contact_phone]
        
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        # Prevent adding multiple instances
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False


# Clinic Admin Configuration
class ClinicImageInline(admin.TabularInline):
    model = ClinicImage
    extra = 1
    fields = ['image', 'caption', 'order', 'is_active', 'image_preview']
    readonly_fields = ['image_preview']
    ordering = ['order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


class ClinicTeamMemberInline(admin.TabularInline):
    model = ClinicTeamMember
    extra = 1
    fields = ['name', 'role', 'bio', 'image', 'order', 'is_active']
    ordering = ['order']


class OfferInline(admin.TabularInline):
    model = Offer
    extra = 1
    fields = ['header', 'valid_from', 'valid_until', 'is_active', 'is_featured', 'order']
    list_editable = ['order', 'is_active', 'is_featured']


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone', 'rating', 'is_active', 'order', 'main_image_preview']
    list_filter = ['is_active', 'city']
    search_fields = ['name', 'city', 'specialization']
    list_editable = ['order', 'is_active']
    inlines = [ClinicImageInline, ClinicTeamMemberInline, OfferInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'specialization', 'description')
        }),
        ('Location & Contact', {
            'fields': ('address', 'city', 'phone', 'email')
        }),
        ('Rating & Reviews', {
            'fields': ('rating', 'reviews_count', 'reviews_text')
        }),
        ('Business Hours', {
            'fields': ('business_hours', 'hours_note')
        }),
        ('Main Image', {
            'fields': ('main_image', 'main_image_preview')
        }),
        ('Maps & Directions', {
            'fields': ('google_maps_url', 'map_embed_url')
        }),
        ('Display Options', {
            'fields': ('order', 'is_active')
        }),
    )
    readonly_fields = ['main_image_preview', 'created_at', 'updated_at']
    
    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.main_image.url)
        return "No image"
    main_image_preview.short_description = "Main Image Preview"


@admin.register(ClinicImage)
class ClinicImageAdmin(admin.ModelAdmin):
    list_display = ['clinic', 'caption', 'order', 'is_active', 'image_preview']
    list_filter = ['is_active', 'clinic']
    search_fields = ['clinic__name', 'caption']
    list_editable = ['order', 'is_active']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(ClinicTeamMember)
class ClinicTeamMemberAdmin(admin.ModelAdmin):
    list_display = ['clinic', 'name', 'role', 'order', 'is_active', 'image_preview']
    list_filter = ['is_active', 'clinic', 'role']
    search_fields = ['clinic__name', 'name', 'role']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('clinic', 'name', 'role', 'bio')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px; border-radius: 50%;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Photo"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['reviewer_name', 'rating', 'order', 'is_active', 'user_image_preview', 'screenshot_preview', 'created_at']
    list_filter = ['is_active', 'rating', 'created_at']
    search_fields = ['reviewer_name', 'review_text']
    list_editable = ['order', 'is_active', 'rating']
    fieldsets = (
        ('User Information', {
            'fields': ('user_image', 'user_image_preview', 'reviewer_name'),
            'description': 'Upload a profile picture of the reviewer (optional)'
        }),
        ('Review Screenshot', {
            'fields': ('screenshot', 'screenshot_preview'),
            'description': 'Upload a screenshot of the Google review'
        }),
        ('Review Details (Optional - for SEO)', {
            'fields': ('review_text', 'rating'),
            'classes': ('collapse',),
            'description': 'Optional details for SEO and accessibility. The screenshot will be displayed primarily.'
        }),
        ('Display Options', {
            'fields': ('order', 'is_active')
        }),
    )
    readonly_fields = ['screenshot_preview', 'user_image_preview', 'created_at']
    
    def screenshot_preview(self, obj):
        if obj.screenshot:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.screenshot.url
            )
        return "No screenshot"
    screenshot_preview.short_description = "Screenshot Preview"
    
    def user_image_preview(self, obj):
        if obj.user_image:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 150px; border-radius: 50%; box-shadow: 0 2px 8px rgba(0,0,0,0.1); object-fit: cover;" />',
                obj.user_image.url
            )
        return "No user image"
    user_image_preview.short_description = "User Image Preview"


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['header', 'clinic', 'valid_from', 'valid_until', 'is_active', 'is_featured', 'order', 'days_remaining_display', 'image_preview']
    list_filter = ['clinic', 'is_active', 'is_featured', 'valid_from', 'valid_until']
    search_fields = ['header', 'description', 'clinic__name']
    list_editable = ['is_active', 'is_featured', 'order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('clinic', 'header', 'description')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order', 'is_active')
        }),
    )
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image"
    
    def days_remaining_display(self, obj):
        if obj.is_valid:
            days = obj.days_remaining
            if days > 0:
                return format_html('<span style="color: green;">{} days left</span>', days)
            else:
                return format_html('<span style="color: orange;">Last day</span>')
        else:
            return format_html('<span style="color: red;">Expired</span>')
    days_remaining_display.short_description = "Status"


# Custom admin interface styling
def admin_media_js():
    return format_html("""
    <script>
        django.jQuery(document).ready(function($) {
            // Add custom styling for better admin interface
            $('body').addClass('monalisa-admin');
        });
    </script>
    <style>
        .monalisa-admin .module h2, 
        .monalisa-admin .module caption, 
        .monalisa-admin .inline-group h2 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .monalisa-admin .button, 
        .monalisa-admin input[type=submit], 
        .monalisa-admin input[type=button], 
        .monalisa-admin .submit-row input, 
        .monalisa-admin a.button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
        }
        .monalisa-admin .button:hover, 
        .monalisa-admin input[type=submit]:hover, 
        .monalisa-admin input[type=button]:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
    </style>
    """)

# Add custom CSS/JS to admin
admin.site.media = admin_media_js
