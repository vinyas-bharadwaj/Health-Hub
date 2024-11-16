from django.shortcuts import get_object_or_404
import numpy as np
from rest_framework.permissions import IsAuthenticated
from .models import Patient, Doctor, Report
from .serializers import PatientSerializer, ReportSerializer, DoctorSerializer


# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientRegisterSerializer
from .schemas import user_list_docs

from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import tensorflow as tf
from PIL import Image
from django.core.files.storage import default_storage
from backend import settings
import os



class PredictView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response({"detail": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Load the uploaded image
        image = request.FILES['image']
        image = Image.open(image)

        # Load your pre-trained model (assuming it's a TensorFlow model)
        model_path = os.path.join(settings.BASE_DIR, 'model.h5')  # Path to your model
        model = tf.keras.models.load_model(model_path)

        # Preprocess the image to match the input size your model expects
        image = image.resize((224, 224))  # Example resize to 224x224
        image = np.array(image)  # Convert to NumPy array
        image = image / 255.0  # Normalize if necessary
        image = np.expand_dims(image, axis=0)  # Add batch dimension

        # Run prediction
        prediction = model.predict(image)

        # Return the prediction result (assuming binary classification)
        prediction_result = 'Malignant' if prediction[0][0] > 0.5 else 'Benign'
        
        return Response({
            'prediction': prediction_result,
            'confidence': prediction[0][0]
        })


@api_view(['GET'])
def doctor_count(request):
    # Count the number of doctors in the database
    count = Doctor.objects.count()
    
    # Return the count as a JSON response
    return JsonResponse({"doctor_count": count})

@api_view(['GET'])
def patient_count(request):
    count = Patient.objects.count()
    
    return JsonResponse({"patient_count": count})


class RegisterPatientView(APIView):
    @user_list_docs
    def post(self, request):
        print("-----------------")
        print(request.data)
        serializer = PatientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Patient registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterDoctorView(APIView):

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Doctor created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PatientListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        patients = Patient.objects.all()  # Query all Patient objects
        serializer = PatientSerializer(patients, many=True)  # Serialize the queryset
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class DoctorPatientsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, doctor_id):
        try:
            doctor = Doctor.objects.get(id=doctor_id)  # Fetch the doctor by ID
            patients = doctor.patients.all()  # Access the many-to-many relationship
            serializer = PatientSerializer(patients, many=True)  # Serialize patients
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
        
class DoctorDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            doctor = Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return Response({"detail": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)



class UserReportsView(APIView):
    def get(self, request, username):
        # Fetch the patient by username
        patient = get_object_or_404(Patient, username=username)
        # Fetch all reports associated with the patient
        reports = Report.objects.filter(patient=patient)
        # Serialize the reports
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    