from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import models
from .models import *
from .serializers import *


class LandingPageBgAPIView(generics.RetrieveAPIView):
    """API view for landing page background image or carousel"""
    serializer_class = LandingPageBgSerializer
    
    def get_object(self):
        return get_object_or_404(LandingPageBg, is_active=True)


@api_view(['GET'])
def about_us_api(request):
    """API view for About Us content with isLanding parameter"""
    is_landing = request.query_params.get('isLanding', 'false').lower() == 'true'
    
    page_type = 'landing' if is_landing else 'normal'
    
    try:
        about_us = AboutUs.objects.get(page_type=page_type, is_active=True)
        serializer = AboutUsSerializer(about_us, context={'request': request})
        return Response(serializer.data)
    except AboutUs.DoesNotExist:
        # If landing page doesn't exist, fallback to normal page
        if page_type == 'landing':
            try:
                about_us = AboutUs.objects.get(page_type='normal', is_active=True)
                serializer = AboutUsSerializer(about_us, context={'request': request})
                return Response(serializer.data)
            except AboutUs.DoesNotExist:
                return Response(
                    {"error": "No About Us content found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": f"About Us content for {page_type} page not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET'])
def treatments_api(request):
    """API view for treatments with isLanding parameter and optional clinic filter"""
    is_landing = request.query_params.get('isLanding', 'false').lower() == 'true'
    clinic_id = request.query_params.get('clinic_id', None)
    
    if is_landing:
        # Return featured treatments for landing page
        treatments = Treatment.objects.filter(is_active=True, is_featured=True)
        if clinic_id:
            treatments = treatments.filter(clinic_id=clinic_id)
        serializer = TreatmentLandingSerializer(treatments, many=True, context={'request': request})
        return Response(serializer.data)
    else:
        # Return treatment categories with items for normal page
        categories = TreatmentCategory.objects.filter(is_active=True).prefetch_related('items')
        
        result = []
        for category in categories:
            treatments = category.items.filter(is_active=True)
            if clinic_id:
                treatments = treatments.filter(clinic_id=clinic_id)
            
            if treatments.exists():  # Only include categories that have treatments
                category_data = {
                    "id": category.id,
                    "title": category.title,
                    "description": category.description,
                    "items": TreatmentItemSerializer(treatments, many=True, context={'request': request}).data
                }
                result.append(category_data)
        
        return Response(result)


class TreatmentFAQAPIView(generics.ListAPIView):
    """API view for treatment FAQs"""
    serializer_class = TreatmentFAQSerializer
    queryset = TreatmentFAQ.objects.filter(is_active=True)


@api_view(['GET'])
def results_api(request):
    """API view for results with isLanding parameter"""
    is_landing = request.query_params.get('isLanding', 'false').lower() == 'true'
    
    if is_landing:
        # Return one featured result for landing page
        try:
            result = Result.objects.filter(is_active=True, is_featured=True).first()
            if result:
                serializer = ResultLandingSerializer(result, context={'request': request})
                return Response(serializer.data)
            else:
                # Fallback to any result if no featured result exists
                result = Result.objects.filter(is_active=True).first()
                if result:
                    serializer = ResultLandingSerializer(result, context={'request': request})
                    return Response(serializer.data)
                else:
                    return Response({"beforeImage": "", "afterImage": ""})
        except Result.DoesNotExist:
            return Response({"beforeImage": "", "afterImage": ""})
    else:
        # Return all results for normal page
        results = Result.objects.filter(is_active=True)
        serializer = ResultSerializer(results, many=True, context={'request': request})
        return Response(serializer.data)


class SkinConcernsAPIView(generics.ListAPIView):
    """API view for skin concerns"""
    serializer_class = SkinConcernSerializer
    queryset = SkinConcern.objects.filter(is_active=True)


class LandingFAQAPIView(generics.ListAPIView):
    """API view for landing page FAQs"""
    serializer_class = LandingFAQSerializer
    queryset = LandingFAQ.objects.filter(is_active=True)


class WhyChooseUsAPIView(generics.ListAPIView):
    """API view for Why Choose Us benefits"""
    serializer_class = WhyChooseUsSerializer
    queryset = WhyChooseUs.objects.filter(is_active=True)


class AppointmentCreateAPIView(generics.CreateAPIView):
    """API view for creating appointment bookings"""
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        
        return Response(
            {
                "message": "Appointment request submitted successfully. We will contact you soon.",
                "appointment_id": appointment.id
            },
            status=status.HTTP_201_CREATED
        )


class ContactMessageCreateAPIView(generics.CreateAPIView):
    """API view for creating contact messages"""
    serializer_class = ContactMessageSerializer
    queryset = ContactMessage.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        
        return Response(
            {
                "message": "Your message has been sent successfully. We will get back to you soon.",
                "message_id": message.id
            },
            status=status.HTTP_201_CREATED
        )


# Blog Views
class BlogListCreateAPIView(generics.ListCreateAPIView):
    """API view for listing and creating blog posts"""
    
    def get_queryset(self):
        queryset = Blog.objects.filter(is_published=True)
        
        # Filter by featured
        is_featured = self.request.query_params.get('featured', None)
        if is_featured is not None:
            if is_featured.lower() == 'true':
                queryset = queryset.filter(is_featured=True)
        
        # Filter by tags
        tags = self.request.query_params.get('tags', None)
        if tags:
            queryset = queryset.filter(tags__icontains=tags)
        
        # Search in title and content
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | models.Q(content__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BlogListSerializer
        return BlogCreateUpdateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blog = serializer.save()
        
        return Response(
            {
                "message": "Blog post created successfully.",
                "blog_id": blog.id,
                "slug": blog.slug
            },
            status=status.HTTP_201_CREATED
        )


class BlogDetailAPIView(generics.RetrieveUpdateAPIView):
    """API view for retrieving and updating individual blog posts"""
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Blog.objects.filter(is_published=True)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BlogDetailSerializer
        return BlogCreateUpdateSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Increment view count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        blog = serializer.save()
        
        return Response(
            {
                "message": "Blog post updated successfully.",
                "blog_id": blog.id,
                "slug": blog.slug
            }
        )


# Treatment Detail View
@api_view(['GET'])
def treatment_detail_api(request, treatment_id):
    """API view for detailed treatment information"""
    try:
        treatment = Treatment.objects.get(id=treatment_id, is_active=True)
        serializer = TreatmentDetailSerializer(treatment, context={'request': request})
        return Response(serializer.data)
    except Treatment.DoesNotExist:
        return Response(
            {"error": "Treatment not found"},
            status=status.HTTP_404_NOT_FOUND
        )


# Clinic Views
@api_view(['GET'])
def clinics_api(request):
    """API view for clinics list"""
    clinics = Clinic.objects.filter(is_active=True)
    serializer = ClinicListSerializer(clinics, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def clinic_detail_api(request, clinic_id):
    """API view for clinic detail"""
    try:
        clinic = get_object_or_404(Clinic, id=clinic_id, is_active=True)
        serializer = ClinicDetailSerializer(clinic, context={'request': request})
        return Response(serializer.data)
    except Clinic.DoesNotExist:
        return Response(
            {"error": "Clinic not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def clinic_treatments_api(request, clinic_id):
    """API view for treatments specific to a clinic"""
    try:
        clinic = get_object_or_404(Clinic, id=clinic_id, is_active=True)
        treatments = Treatment.objects.filter(clinic=clinic, is_active=True).order_by('order', 'name')
        serializer = TreatmentItemSerializer(treatments, many=True, context={'request': request})
        
        return Response({
            'clinic': {
                'id': clinic.id,
                'name': clinic.name,
                'city': clinic.city
            },
            'treatments': serializer.data
        })
    except Clinic.DoesNotExist:
        return Response(
            {"error": "Clinic not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def clinic_offers_api(request, clinic_id):
    """API view for offers specific to a clinic"""
    try:
        clinic = get_object_or_404(Clinic, id=clinic_id, is_active=True)
        offers = Offer.objects.filter(clinic=clinic, is_active=True).order_by('order', '-created_at')
        serializer = OfferSerializer(offers, many=True, context={'request': request})
        
        return Response({
            'clinic': {
                'id': clinic.id,
                'name': clinic.name,
                'city': clinic.city
            },
            'offers': serializer.data
        })
    except Clinic.DoesNotExist:
        return Response(
            {"error": "Clinic not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def offers_api(request):
    """API view for all active offers"""
    clinic_id = request.query_params.get('clinic_id', None)
    
    offers = Offer.objects.filter(is_active=True)
    if clinic_id:
        offers = offers.filter(clinic_id=clinic_id)
    
    offers = offers.order_by('order', '-created_at')
    serializer = OfferSerializer(offers, many=True, context={'request': request})
    return Response(serializer.data)


# Site Settings View
@api_view(['GET'])
def site_settings_api(request):
    """API view for site settings"""
    try:
        site_settings = SiteSettings.objects.first()
        if site_settings:
            serializer = SiteSettingsSerializer(site_settings)
            return Response(serializer.data)
        else:
            # Return default values if no settings exist
            return Response({
                "site_name": "Monalisa Wellness",
                "site_tagline": "Skin Clinic",
                "site_description": "Expert skincare treatments and products that transform your skin and enhance your natural beauty.",
                "contact_email": "info@monalisaclinic.com",
                "contact_phone": "092891 57655",
                "address": "Delhi & Gurugram\nMultiple Locations",
                "social_facebook": "",
                "social_instagram": "",
                "social_twitter": "",
                "business_hours": "Monday - Sunday: Open Daily\nCloses at: 7:30 PM\nCall for specific timings"
            })
    except Exception as e:
        return Response(
            {"error": "Failed to fetch site settings"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Additional utility views
@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({"status": "OK", "message": "Monalisa Wellness API is running"})


@api_view(['GET'])
def api_endpoints(request):
    """List all available API endpoints"""
    endpoints = {
        "Landing Page Background": "/api/landing-bg/",
        "About Us": "/api/about-us/ (add ?isLanding=true for landing page)",
        "Treatments": "/api/treatments/ (add ?isLanding=true for featured treatments)",
        "Treatment Detail": "/api/treatments/{id}/",
        "Treatment FAQs": "/api/treatments/faq/",
        "Blog List & Create": "/api/blogs/ (GET: list, POST: create)",
        "Blog Detail & Update": "/api/blogs/{slug}/ (GET: detail, PUT/PATCH: update)",
        "Results": "/api/results/ (add ?isLanding=true for featured result)",
        "Skin Concerns": "/api/skin-concerns/",
        "Landing Page FAQs": "/api/landing/faq/",
        "Why Choose Us": "/api/why-choose-us/",
        "Clinics List": "/api/clinics/",
        "Clinic Detail": "/api/clinics/{id}/",
        "Book Appointment": "/api/appointments/ (POST)",
        "Contact Message": "/api/contact/ (POST)",
        "Site Settings": "/api/site-settings/",
        "Health Check": "/api/health/",
        "API Endpoints": "/api/endpoints/",
    }
    return Response(endpoints)
