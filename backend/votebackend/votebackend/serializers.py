from rest_framework import serializers
from account.serializers import UserCreateSerializer , UserListSerializer
from votersystem.models import Student , Course , Department , Election , VoterRegistration , Vote , Candidate , Voter
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken

## THIS IS A STUDENT SERIALIZER 
class StudentCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Student
        fields = ('user', 'student_id', 'level', 'course', 'age', 'department')

    '''  def validate_student_id(self, value):
        # Add logic to validate the student ID according to the year of admission
        # For example, ensure the ID matches a specific format
        # Example: 2024XXXX where XXXX is a unique number
        if not value.startswith('2024'):
            raise serializers.ValidationError("Student ID must start with the year of admission (e.g., 2024).")
        return value '''

    def validate_user_email(self, email):
        # Add logic to ensure the email matches the school's email format
        if not email.endswith('@ruc.edu'):
            raise serializers.ValidationError("Email must be a valid school email address.")
        return email 

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        self.validate_user_email(user_data['email'])
        user = UserCreateSerializer.create(UserCreateSerializer(), validated_data=user_data)
        student, created = Student.objects.update_or_create(user=user, **validated_data)
        return student
    
  

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        token = RefreshToken.for_user(instance.user)
        representation['token'] = {
            'refresh': str(token),
            'access': str(token.access_token),
        }
        return representation

class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'level', 'course', 'age', 'department']
        depth = 1


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['age']

    def update(self, instance, validated_data):
        # Only update the fields specified in the serializer (age in this case)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance




###DEPARTMENT SERIALIZERS
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('name',)

class DepartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

    def create(self, validated_data):
        return Department.objects.create(**validated_data)
    
class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class DepartmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance



#COURSE SERIALIZERS 

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name',)

class CourseCreateSerializer(serializers.ModelSerializer):
    departments = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), many=True)

    class Meta:
        model = Course
        fields = ['name', 'departments']

    def create(self, validated_data):
        departments_data = validated_data.pop('departments')
        course = Course.objects.create(**validated_data)
        course.departments.set(departments_data)
        return course
    
class CourseListSerializer(serializers.ModelSerializer):
    departments = DepartmentListSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'departments']
class CourseUpdateSerializer(serializers.ModelSerializer):
    departments = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), many=True)

    class Meta:
        model = Course
        fields = ['name', 'departments']

    def update(self, instance, validated_data):
        departments_data = validated_data.pop('departments', None)
        instance.name = validated_data.get('name', instance.name)

        if departments_data is not None:
            instance.departments.set(departments_data)

        instance.save()
        return instance





class StudentListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    course = CourseSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Student
        fields = ('user', 'student_id', 'level', 'course', 'department')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Customize the representation if needed, for example:
        # representation['course_name'] = representation.pop('course')['name']
        # representation['department_name'] = representation.pop('department')['name']
        return representation
    

#CANDIDATES SERIALIZERS
class CandidateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['student', 'election']

    def validate(self, data):
        # Check if the student is already a candidate in the same election
        if Candidate.objects.filter(student=data['student'], election=data['election']).exists():
            raise serializers.ValidationError("This student is already a candidate in this election.")
        return data

    def create(self, validated_data):
        candidate = Candidate.objects.create(**validated_data)
        return candidate
    
class CandidateListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    election_title = serializers.CharField(source='election.title', read_only=True)

    class Meta:
        model = Candidate
        fields = ['id', 'student_name', 'election_title', 'number_of_votes']


class CandidateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['number_of_votes']

##ELECTION SERIALIZERS
class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'status', 'managed_by', 'election_type', 'department', 'course']

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        if data['election_type'] == 'Departmental' and not data.get('department'):
            raise serializers.ValidationError("Department must be specified for departmental elections.")
        if data['election_type'] == 'Course' and not data.get('course'):
            raise serializers.ValidationError("Course must be specified for course-specific elections.")
        return data



##VOTER REGISTRATION SERIALIERS
class VoterRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoterRegistration
        fields = ['voter', 'election', 'registered_on']

    def validate(self, data):
        election = data['election']
        voter = data['voter']

        if election.status != 'Active':
            raise serializers.ValidationError("Cannot register for an inactive election.")
        
        if election.election_type == 'Departmental' and voter.user.student.department != election.department:
            raise serializers.ValidationError("Voter is not eligible for this departmental election.")
        
        if election.election_type == 'Course' and voter.user.student.course != election.course:
            raise serializers.ValidationError("Voter is not eligible for this course-specific election.")

        return data


#VOTE SERIALIZERS  
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['voter', 'election', 'candidate', 'cast_on']
        read_only_fields = ['cast_on']

    def validate(self, data):
        voter = data['voter']
        election = data['election']
        candidate = data['candidate']

        # Check if the voter is registered for the election
        if not VoterRegistration.objects.filter(voter=voter, election=election).exists():
            raise serializers.ValidationError("Voter is not registered for this election.")
        
        # Ensure the voter has not already voted in this election
        if Vote.objects.filter(voter=voter, election=election).exists():
            raise serializers.ValidationError("Voter has already cast a vote in this election.")
        
        # Ensure the candidate is running in this election
        if not Candidate.objects.filter(id=candidate.id, election=election).exists():
            raise serializers.ValidationError("The selected candidate is not running in this election.")
        
        return data
    
##VOTER SERIALIZER

class VoterCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Voter
        fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserCreateSerializer.create(UserCreateSerializer(), validated_data=user_data)
        voter, created = Voter.objects.update_or_create(user=user)
        return voter
    

class VoterListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Voter
        fields = ['id', 'user_email']


class VoterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['id']