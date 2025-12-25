from rest_framework import serializers
from .models import *


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Serializer for site settings"""
    all_contact_emails = serializers.SerializerMethodField()
    all_contact_phones = serializers.SerializerMethodField()
    primary_email = serializers.SerializerMethodField()
    primary_phone = serializers.SerializerMethodField()
    
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'site_tagline', 'site_description', 
            # New multiple contact fields
            'contact_emails', 'contact_phones', 'all_contact_emails', 'all_contact_phones',
            'primary_email', 'primary_phone',
            # Legacy fields for backward compatibility
            'contact_email', 'contact_phone', 
            'address', 'social_facebook', 'social_instagram', 
            'social_twitter', 'business_hours',
            # Offers strip customization
            'offers_strip_color', 'offers_strip_gradient_color'
        ]
    
    def get_all_contact_emails(self, obj):
        """Get all contact emails including legacy field"""
        return obj.get_contact_emails()
    
    def get_all_contact_phones(self, obj):
        """Get all contact phones including legacy field"""
        return obj.get_contact_phones()
    
    def get_primary_email(self, obj):
        """Get the primary contact email"""
        return obj.get_primary_email()
    
    def get_primary_phone(self, obj):
        """Get the primary contact phone"""
        return obj.get_primary_phone()


class CarouselImageSerializer(serializers.ModelSerializer):
    """Serializer for carousel images"""
    imageUrl = serializers.SerializerMethodField()
    
    class Meta:
        model = CarouselImage
        fields = ['title', 'description', 'imageUrl']
    
    def get_imageUrl(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return ""


class LandingPageBgSerializer(serializers.ModelSerializer):
    """Serializer for landing page background"""
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = LandingPageBg
        fields = ['id', 'image', 'is_active']
    
    def get_image(self, obj):
        if obj.type == 'static':
            # Return single S3 image url
            if obj.static_image:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.static_image.url)
                return obj.static_image.url
            return ""
        else:
            # For carousel type, return the first active image
            # (You can modify this logic as needed)
            carousel_image = obj.carousel_images.filter(is_active=True).first()
            if carousel_image:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(carousel_image.image.url)
                return carousel_image.image.url
            return ""


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for team members"""
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'bio', 'image']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return ""


class PhilosophyHighlightSerializer(serializers.ModelSerializer):
    """Serializer for philosophy highlights"""
    
    class Meta:
        model = PhilosophyHighlight
        fields = ['title', 'description']


class AboutUsSerializer(serializers.ModelSerializer):
    """Serializer for About Us content"""
    team = serializers.SerializerMethodField()
    philosophy = serializers.SerializerMethodField()
    title1 = serializers.SerializerMethodField()
    title2 = serializers.SerializerMethodField()
    
    class Meta:
        model = AboutUs
        fields = ['desp1', 'desp2', 'team', 'philosophy', 'title1', 'title2']
    
    def get_team(self, obj):
        # Only return team for normal pages
        if obj.page_type == 'normal':
            team_members = TeamMember.objects.filter(is_active=True)
            return TeamMemberSerializer(team_members, many=True, context=self.context).data
        return []
    
    def get_philosophy(self, obj):
        # Only return philosophy for normal pages
        if obj.page_type == 'normal':
            highlights = PhilosophyHighlight.objects.filter(is_active=True)
            return {
                "title": obj.philosophy_title,
                "highlights": PhilosophyHighlightSerializer(highlights, many=True).data
            }
        return {}
    
    def get_title1(self, obj):
        # Only return for landing pages
        if obj.page_type == 'landing':
            image_url = ""
            if obj.title1_image:
                request = self.context.get('request')
                if request:
                    image_url = request.build_absolute_uri(obj.title1_image.url)
                else:
                    image_url = obj.title1_image.url
            
            return {
                "heading": obj.title1_heading,
                "desp1": obj.title1_desp1,
                "desp2": obj.title1_desp2,
                "image": image_url
            }
        return {}
    
    def get_title2(self, obj):
        # Only return for landing pages
        if obj.page_type == 'landing':
            image_url = ""
            if obj.title2_image:
                request = self.context.get('request')
                if request:
                    image_url = request.build_absolute_uri(obj.title2_image.url)
                else:
                    image_url = obj.title2_image.url
            
            return {
                "heading": obj.title2_heading,
                "desp1": obj.title2_desp1,
                "desp2": obj.title2_desp2,
                "image": image_url
            }
        return {}
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Clean up response based on page type
        if instance.page_type == 'normal':
            # Remove landing page fields
            data.pop('title1', None)
            data.pop('title2', None)
        else:
            # Remove normal page fields
            data.pop('desp1', None)
            data.pop('desp2', None)
            data.pop('team', None)
            data.pop('philosophy', None)
        
        return data


class TreatmentClinicPricingSerializer(serializers.ModelSerializer):
    """Serializer for treatment pricing at specific clinics"""
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)
    clinic_id = serializers.IntegerField(source='clinic.id', read_only=True)
    
    class Meta:
        model = TreatmentClinicPricing
        fields = ['clinic_id', 'clinic_name', 'price', 'order', 'is_active']


class TreatmentItemSerializer(serializers.ModelSerializer):
    """Serializer for individual treatments"""
    image = serializers.SerializerMethodField()
    clinic_pricing = serializers.SerializerMethodField()
    
    class Meta:
        model = Treatment
        fields = ['id', 'name', 'duration', 'description', 'image', 'is_active', 'clinic_pricing']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return ""
    
    def get_clinic_pricing(self, obj):
        """Get pricing for all clinics where this treatment is available"""
        clinic_id = self.context.get('clinic_id')
        if clinic_id:
            # Filter pricing for specific clinic
            pricing = obj.clinic_pricing.filter(clinic_id=clinic_id, is_active=True)
        else:
            # Get all active pricing
            pricing = obj.clinic_pricing.filter(is_active=True)
        
        return TreatmentClinicPricingSerializer(pricing, many=True).data


class TreatmentLandingSerializer(serializers.ModelSerializer):
    """Serializer for treatments on landing page"""
    image = serializers.SerializerMethodField()
    clinic_pricing = serializers.SerializerMethodField()
    
    class Meta:
        model = Treatment
        fields = ['id', 'name', 'description', 'image', 'duration', 'clinic_pricing']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return ""
    
    def get_clinic_pricing(self, obj):
        """Get pricing for all clinics where this treatment is available"""
        clinic_id = self.context.get('clinic_id')
        if clinic_id:
            # Filter pricing for specific clinic
            pricing = obj.clinic_pricing.filter(clinic_id=clinic_id, is_active=True)
        else:
            # Get all active pricing
            pricing = obj.clinic_pricing.filter(is_active=True)
        
        return TreatmentClinicPricingSerializer(pricing, many=True).data


class TreatmentCategorySerializer(serializers.ModelSerializer):
    """Serializer for treatment categories"""
    items = TreatmentItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = TreatmentCategory
        fields = ['id', 'title', 'description', 'items']
    
    def get_items(self, obj):
        treatments = obj.items.filter(is_active=True)
        return TreatmentItemSerializer(treatments, many=True, context=self.context).data


class TreatmentFAQSerializer(serializers.ModelSerializer):
    """Serializer for treatment FAQs"""
    
    class Meta:
        model = TreatmentFAQ
        fields = ['question', 'answer']


class ResultSerializer(serializers.ModelSerializer):
    """Serializer for results"""
    before_image = serializers.SerializerMethodField()
    after_image = serializers.SerializerMethodField()
    is_featured = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    
    class Meta:
        model = Result
        fields = ['id', 'condition', 'duration', 'description', 'before_image', 'after_image', 'is_featured', 'created_at', 'is_active']
    
    def get_before_image(self, obj):
        if obj.before_image:
            # Check if it's an external URL (starts with http)
            if str(obj.before_image).startswith('http'):
                return str(obj.before_image)
            else:
                # It's an uploaded file, use Django's URL handling
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.before_image.url)
                return obj.before_image.url
        return ""
    
    def get_after_image(self, obj):
        if obj.after_image:
            # Check if it's an external URL (starts with http)
            if str(obj.after_image).startswith('http'):
                return str(obj.after_image)
            else:
                # It's an uploaded file, use Django's URL handling
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.after_image.url)
                return obj.after_image.url
        return ""


class ResultLandingSerializer(serializers.ModelSerializer):
    """Serializer for results on landing page"""
    before_image = serializers.SerializerMethodField()
    after_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Result
        fields = ['before_image', 'after_image']
    
    def get_before_image(self, obj):
        if obj.before_image:
            # Check if it's an external URL (starts with http)
            if str(obj.before_image).startswith('http'):
                return str(obj.before_image)
            else:
                # It's an uploaded file, use Django's URL handling
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.before_image.url)
                return obj.before_image.url
        return ""
    
    def get_after_image(self, obj):
        if obj.after_image:
            # Check if it's an external URL (starts with http)
            if str(obj.after_image).startswith('http'):
                return str(obj.after_image)
            else:
                # It's an uploaded file, use Django's URL handling
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.after_image.url)
                return obj.after_image.url
        return ""


class SkinConcernSerializer(serializers.ModelSerializer):
    """Serializer for skin concerns"""
    icon = serializers.SerializerMethodField()
    
    class Meta:
        model = SkinConcern
        fields = ['id', 'title', 'description', 'icon', 'treatments', 'products', 'results']
    
    def get_icon(self, obj):
        if obj.icon:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.icon.url)
            return obj.icon.url
        return ""


class LandingFAQSerializer(serializers.ModelSerializer):
    """Serializer for landing page FAQs"""
    
    class Meta:
        model = LandingFAQ
        fields = ['question', 'answer']


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for clinic offers"""
    image = serializers.SerializerMethodField()
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)
    is_valid = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Offer
        fields = [
            'id', 'header', 'description', 'image', 'clinic_name', 
            'valid_from', 'valid_until', 'is_featured', 'is_valid', 'days_remaining'
        ]
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return ""


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for appointment bookings"""
    
    class Meta:
        model = Appointment
        fields = [
            'clinic', 'first_name', 'last_name', 'email', 'phone',
            'preferred_date', 'preferred_time', 'treatment_interest', 'message'
        ]
    
    def create(self, validated_data):
        appointment = Appointment.objects.create(**validated_data)
        
        # Send email notification to owner
        from django.core.mail import send_mail
        from django.conf import settings
        
        try:
            clinic_name = appointment.clinic.name if appointment.clinic else 'No clinic specified'
            subject = f"New Appointment Request - {appointment.full_name} at {clinic_name}"
            message = f"""
            New appointment request received:
            
            Clinic: {clinic_name}
            Name: {appointment.full_name}
            Email: {appointment.email}
            Phone: {appointment.phone}
            Preferred Date: {appointment.preferred_date}
            Preferred Time: {appointment.preferred_time}
            Treatment Interest: {appointment.treatment_interest}
            Message: {appointment.message}
            
            Please log in to the admin panel to manage this appointment.
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.OWNER_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            # Log the error but don't fail the appointment creation
            print(f"Failed to send email notification: {e}")
        
        return appointment


class BlogImageSerializer(serializers.ModelSerializer):
    """Serializer for blog images"""
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'caption', 'order']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return ""


class BlogListSerializer(serializers.ModelSerializer):
    """Serializer for blog list view"""
    featured_image = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author', 'featured_image',
            'tags_list', 'read_time', 'views_count', 'created_at', 'updated_at'
        ]
    
    def get_featured_image(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return ""
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()


class BlogDetailSerializer(serializers.ModelSerializer):
    """Serializer for blog detail view"""
    featured_image = serializers.SerializerMethodField()
    images = BlogImageSerializer(many=True, read_only=True)
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'author', 'featured_image',
            'images', 'tags_list', 'read_time', 'views_count', 'meta_title',
            'meta_description', 'created_at', 'updated_at'
        ]
    
    def get_featured_image(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return ""
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()


class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating blog posts"""
    
    class Meta:
        model = Blog
        fields = [
            'title', 'slug', 'content', 'excerpt', 'author', 'featured_image',
            'is_published', 'is_featured', 'meta_title', 'meta_description',
            'tags', 'read_time'
        ]
        extra_kwargs = {
            'slug': {'required': False}
        }
    
    def validate_slug(self, value):
        # Check for slug uniqueness excluding current instance
        instance_id = self.instance.id if self.instance else None
        if Blog.objects.filter(slug=value).exclude(id=instance_id).exists():
            raise serializers.ValidationError("A blog with this slug already exists.")
        return value


class TreatmentBenefitSerializer(serializers.ModelSerializer):
    """Serializer for treatment benefits"""
    
    class Meta:
        model = TreatmentBenefit
        fields = ['title', 'description']


class TreatmentStepSerializer(serializers.ModelSerializer):
    """Serializer for treatment steps"""
    
    class Meta:
        model = TreatmentStep
        fields = ['title', 'description', 'step_number']


class TreatmentCategoryDetailSerializer(serializers.ModelSerializer):
    """Serializer for category details in treatment"""
    class Meta:
        model = TreatmentCategory
        fields = ['id', 'title', 'description']


class TreatmentDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed treatment view"""
    category = TreatmentCategoryDetailSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    benefits = serializers.SerializerMethodField()
    steps = serializers.SerializerMethodField()
    clinic_pricing = serializers.SerializerMethodField()
    
    class Meta:
        model = Treatment
        fields = [
            'id', 'name', 'category', 'duration', 'description',
            'image', 'is_featured', 'order', 'is_active', 'benefits', 'steps', 'clinic_pricing'
        ]
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return ""
    
    def get_benefits(self, obj):
        """Get benefits specific to this treatment"""
        benefits = obj.benefits.filter(is_active=True)
        return TreatmentBenefitSerializer(benefits, many=True).data
    
    def get_steps(self, obj):
        """Get steps specific to this treatment"""
        steps = obj.steps.filter(is_active=True)
        return TreatmentStepSerializer(steps, many=True).data
    
    def get_clinic_pricing(self, obj):
        """Get pricing for all clinics where this treatment is available"""
        clinic_id = self.context.get('clinic_id')
        if clinic_id:
            # Filter pricing for specific clinic
            pricing = obj.clinic_pricing.filter(clinic_id=clinic_id, is_active=True)
        else:
            # Get all active pricing
            pricing = obj.clinic_pricing.filter(is_active=True)
        
        return TreatmentClinicPricingSerializer(pricing, many=True).data


class WhyChooseUsSerializer(serializers.ModelSerializer):
    """Serializer for Why Choose Us benefits"""
    
    class Meta:
        model = WhyChooseUs
        fields = ['id', 'title', 'description', 'icon', 'order']


class TestimonialSerializer(serializers.ModelSerializer):
    """Serializer for testimonials (Google review screenshots)"""
    screenshot = serializers.SerializerMethodField()
    
    class Meta:
        model = Testimonial
        fields = ['id', 'screenshot', 'reviewer_name', 'review_text', 'rating', 'order', 'is_active', 'created_at']
    
    def get_screenshot(self, obj):
        if obj.screenshot:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.screenshot.url)
            return obj.screenshot.url
        return ""


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for contact messages"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
    
    def create(self, validated_data):
        message = ContactMessage.objects.create(**validated_data)
        
        # Send email notification to owner
        from django.core.mail import send_mail
        from django.conf import settings
        
        try:
            subject = f"New Contact Message - {message.subject}"
            email_message = f"""
            New contact message received:
            
            Name: {message.name}
            Email: {message.email}
            Subject: {message.subject}
            Message: {message.message}
            
            Please log in to the admin panel to respond to this message.
            """
            
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.OWNER_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            # Log the error but don't fail the message creation
            print(f"Failed to send email notification: {e}")
        
        return message


class ClinicImageSerializer(serializers.ModelSerializer):
    """Serializer for clinic gallery images"""
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ClinicImage
        fields = ['id', 'image', 'caption', 'order']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return ""


class ClinicTeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for clinic team members"""
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ClinicTeamMember
        fields = ['id', 'name', 'role', 'bio', 'image', 'order']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return ""


class ClinicListSerializer(serializers.ModelSerializer):
    """Serializer for clinic list view"""
    main_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Clinic
        fields = [
            'id', 'name', 'specialization', 'address', 'city', 'phone', 'email',
            'rating', 'reviews_count', 'reviews_text', 'business_hours', 'hours_note',
            'main_image', 'google_maps_url'
        ]
    
    def get_main_image(self, obj):
        if obj.main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.main_image.url)
            return obj.main_image.url
        return ""


class ClinicDetailSerializer(serializers.ModelSerializer):
    """Serializer for clinic detail view"""
    main_image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    team_members = serializers.SerializerMethodField()
    treatments = serializers.SerializerMethodField()
    offers = serializers.SerializerMethodField()
    
    class Meta:
        model = Clinic
        fields = [
            'id', 'name', 'specialization', 'description', 'address', 'city',
            'phone', 'email', 'rating', 'reviews_count', 'reviews_text',
            'business_hours', 'hours_note', 'main_image', 'google_maps_url', 
            'map_embed_url', 'images', 'team_members', 'treatments', 'offers'
        ]
    
    def get_main_image(self, obj):
        if obj.main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.main_image.url)
            return obj.main_image.url
        return ""
    
    def get_images(self, obj):
        images = obj.images.filter(is_active=True)
        return ClinicImageSerializer(images, many=True, context=self.context).data
    
    def get_team_members(self, obj):
        team_members = obj.team_members.filter(is_active=True)
        return ClinicTeamMemberSerializer(team_members, many=True, context=self.context).data
    
    def get_treatments(self, obj):
        # Get treatments that have pricing for this clinic
        from .models import Treatment
        treatments = Treatment.objects.filter(
            clinic_pricing__clinic=obj, 
            clinic_pricing__is_active=True,
            is_active=True
        ).prefetch_related('clinic_pricing__clinic').distinct().order_by('order', 'name')
        return TreatmentItemSerializer(treatments, many=True, context=self.context).data
    
    def get_offers(self, obj):
        offers = obj.offers.filter(is_active=True).order_by('order', '-created_at')
        return OfferSerializer(offers, many=True, context=self.context).data 