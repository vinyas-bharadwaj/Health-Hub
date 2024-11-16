"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import RegisterPatientView, PatientListView, DoctorPatientsView, RegisterDoctorView, DoctorDetailView, doctor_count, patient_count, PredictView


router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/schema/', SpectacularAPIView.as_view(), name="schema"),
    path('api/docs/schema/ui', SpectacularSwaggerView.as_view()),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/create/", RegisterPatientView.as_view(), name='register'),
    path('api/users/', PatientListView.as_view(), name='patient-list'),
    path('api/users/count', patient_count, name="patient-count"),
    path('api/doctor/<int:pk>/', DoctorDetailView.as_view(), name='get-doctor'),
    path('api/doctor/<int:doctor_id>/patients/', DoctorPatientsView.as_view(), name='doctor-patients'),
    path('api/doctor/create/', RegisterDoctorView.as_view(), name='create-doctor'),
    path('api/doctor/count', doctor_count, name="doctor-count"),
    path('api/predict/', PredictView.as_view())
] + router.urls


