from rest_framework import generics,permissions
from votersystem.models import Department, Course , Student , VoterRegistration,Candidate , Vote , Election , Voter 
from rest_framework.permissions import IsAdminUser , BasePermission
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from .serializers import (VoteSerializer, ElectionSerializer,CandidateCreateSerializer,VoterListSerializer, VoterUpdateSerializer ,CandidateListSerializer, CandidateUpdateSerializer, VoterCreateSerializer, VoterCreateSerializer, VoterRegistrationSerializer,
    DepartmentCreateSerializer, DepartmentListSerializer, DepartmentUpdateSerializer, StudentUpdateSerializer,
    CourseCreateSerializer, CourseListSerializer, CourseUpdateSerializer,StudentCreateSerializer,StudentListSerializer
)
from rest_framework.response import Response


from rest_framework_simplejwt.tokens import RefreshToken

class StudentCreateViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer
    permission_classes = [permissions.IsAdminUser]
    def get_queryset(self):
        queryset = super().get_queryset()  # Get the base queryset
        department = self.request.query_params.get('department', None)
        course = self.request.query_params.get('course', None)
        level = self.request.query_params.get('level', None)

        # Filter by department (if provided)
        if department:
            queryset = queryset.filter(department__name=department)

        # Filter by course (if provided)
        if course:
            queryset = queryset.filter(courses__name=course)  # Assuming a ManyToManyField relationship

        # Filter by level (if provided)
        if level:
            queryset = queryset.filter(level=level)

        return queryset

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner or an admin
        return obj.user == request.user or request.user.is_staff

class StudentUpdateView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        # Allow only the student or admin to access the student's data
        if self.request.user.is_staff:
            return Student.objects.all()
        return Student.objects.filter(user=self.request.user)

# CANDIDATES FOR ELECTION CREATEVIEW
class CandidateCreateView(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class CandidateListView(generics.ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateListSerializer
    permission_classes = [permissions.IsAuthenticated]

class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CandidateUpdateSerializer
        return CandidateListSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_object(self):
        obj = super().get_object()
        if self.request.method not in ['PUT', 'PATCH', 'DELETE'] and self.request.user != obj.student.user:
            raise PermissionDenied("You do not have permission to view or edit this candidate.")
        return obj


#DEPARTMENTAL VIEWSET
class DepartmentCreateView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentCreateSerializer
    permission_classes = [IsAdminUser]


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentListSerializer


class DepartmentUpdateView(generics.UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentUpdateSerializer

    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # Specific filtering logic can be added here if necessary
        return Department.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Add custom validation or logic here if necessary

        self.perform_update(serializer)

        return Response(serializer.data)
    

    #COURSE  VIEWS 

class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAdminUser]

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

class CourseUpdateView(generics.UpdateAPIView):
    serializer_class = CourseUpdateSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # Specific filtering logic can be added here if necessary
        return Course.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Add custom validation or logic here if necessary

        self.perform_update(serializer)

        return Response(serializer.data)
    



#ELECTION VIEWSET
class ElectionCreateView(generics.CreateAPIView):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(managed_by=self.request.user)
class ElectionListView(generics.ListAPIView):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [permissions.AllowAny]

class ElectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


 ## VOTERREGISTRATION VIEWSET THAT TAKES CARE OF THE VOTER REGISTRATION
class VoterRegistrationViewSet(viewsets.ModelViewSet):
    queryset = VoterRegistration.objects.all()
    serializer_class = VoterRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        voter = self.request.user.voter
        serializer.save(voter=voter)



##VOTER VIEWSET

class VoterCreateView(generics.CreateAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'voter'):
            raise ValidationError("You are already registered as a voter.")
        serializer.save(user=user)

class VoterListView(generics.ListAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterListSerializer
    permission_classes = [permissions.IsAdminUser]


class VoterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voter.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return VoterUpdateSerializer
        return VoterListSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_object(self):
        obj = super().get_object()
        if self.request.method not in ['PUT', 'PATCH', 'DELETE'] and self.request.user != obj.user:
            raise PermissionDenied("You do not have permission to view this voter's details.")
        return obj

## VOTE VIEWSETS
class VoteCreateView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        election = serializer.validated_data['election']

        # Check if user is eligible to vote in this election
        if not self.check_user_eligibility(election):
            return Response({'error': 'You are not eligible to vote in this election'}, status=status.HTTP_403_FORBIDDEN)

        # Additional checks (optional):
        # - Check if user has already voted in this election (if applicable)
        # - Check if voting period is still open

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['voter'] = self.request.user.voter.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ListVoteView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(voter=self.request.user.voter)
    
class RetrieveVoteView(generics.RetrieveAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(voter=self.request.user.voter)

class DeleteVoteView(generics.DestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(voter=self.request.user.voter)
    

## PASS FOR SUPERUSER IS TED