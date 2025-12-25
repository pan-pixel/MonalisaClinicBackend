from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Utility endpoints
    path('health/', views.health_check, name='health_check'),
    path('endpoints/', views.api_endpoints, name='api_endpoints'),
    
    # Landing page background
    path('landing-bg/', views.LandingPageBgAPIView.as_view(), name='landing_bg'),
    
    # About us endpoints
    path('about-us/', views.about_us_api, name='about_us'),
    
    # Treatment endpoints
    path('treatments/', views.treatments_api, name='treatments'),
    path('treatments/categories/', views.treatment_categories_api, name='treatment_categories'),
    path('treatments/categories/nav/', views.treatment_categories_nav_api, name='treatment_categories_nav'),
    path('treatments/<int:treatment_id>/', views.treatment_detail_api, name='treatment_detail'),
    path('treatments/faq/', views.TreatmentFAQAPIView.as_view(), name='treatment_faq'),
    
    # Clinic endpoints
    path('clinics/', views.clinics_api, name='clinics_list'),
    path('clinics/<int:clinic_id>/', views.clinic_detail_api, name='clinic_detail'),
    path('clinics/<int:clinic_id>/treatments/', views.clinic_treatments_api, name='clinic_treatments'),
    path('clinics/<int:clinic_id>/offers/', views.clinic_offers_api, name='clinic_offers'),
    
    # Offers endpoints
    path('offers/', views.offers_api, name='offers_list'),
    
    # Blog endpoints
    path('blogs/', views.BlogListCreateAPIView.as_view(), name='blog_list_create'),
    path('blogs/<slug:slug>/', views.BlogDetailAPIView.as_view(), name='blog_detail'),
    
    # Results endpoints
    path('results/', views.results_api, name='results'),
    
    # Skin concerns endpoint
    path('skin-concerns/', views.SkinConcernsAPIView.as_view(), name='skin_concerns'),
    
    # Landing page FAQ
    path('landing/faq/', views.LandingFAQAPIView.as_view(), name='landing_faq'),
    
    # Why Choose Us
    path('why-choose-us/', views.WhyChooseUsAPIView.as_view(), name='why_choose_us'),
    
    # Appointment booking
    path('appointments/', views.AppointmentCreateAPIView.as_view(), name='appointment_create'),
    
    # Contact message
    path('contact/', views.ContactMessageCreateAPIView.as_view(), name='contact_create'),
    
    # Testimonials
    path('testimonials/', views.TestimonialAPIView.as_view(), name='testimonials'),
    
    # Site settings
    path('site-settings/', views.site_settings_api, name='site_settings'),
] 