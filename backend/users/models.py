from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Patient(AbstractUser):
    pass

class Report(models.Model):
    image = models.ImageField(upload_to='reports/')  # Save images to 'reports/' directory
    patient = models.ForeignKey(Patient, related_name="reports", on_delete=models.CASCADE, default=1)  # One-to-Many with Patient

    def __str__(self):
        return f"Report {self.id} for {self.patient.username}"


class Doctor(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    patients = models.ManyToManyField(Patient, related_name="doctors")

    def __str__(self):
        return self.username

