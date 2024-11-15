from django.shortcuts import get_object_or_404
from .models import Patient, Doctor, Report
from .serializers import PatientSerializer, ReportSerializer

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientRegisterSerializer
from .schemas import user_list_docs

class RegisterPatientView(APIView):
    
    @user_list_docs
    def post(self, request):
        print(request.data)
        serializer = PatientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Patient registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PatientListView(APIView):
    def get(self, request):
        patients = Patient.objects.all()  # Query all Patient objects
        serializer = PatientSerializer(patients, many=True)  # Serialize the queryset
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class DoctorPatientsView(APIView):
    def get(self, request, doctor_id):
        try:
            doctor = Doctor.objects.get(id=doctor_id)  # Fetch the doctor by ID
            patients = doctor.patients.all()  # Access the many-to-many relationship
            serializer = PatientSerializer(patients, many=True)  # Serialize patients
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
        

class UserReportsView(APIView):
    def get(self, request, username):
        # Fetch the patient by username
        patient = get_object_or_404(Patient, username=username)
        # Fetch all reports associated with the patient
        reports = Report.objects.filter(patient=patient)
        # Serialize the reports
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    