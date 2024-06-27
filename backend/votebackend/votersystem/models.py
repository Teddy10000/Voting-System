from django.db import models
from django.db import models
from account.models import User
from django.utils import timezone
from rest_framework.exceptions import ValidationError

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ManyToManyField(Department)  # This defines the relationship

    def __str__(self):
        return self.name



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    level = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()
    
class Election(models.Model):
    ELECTION_TYPES = [
        ('General', 'General'),
        ('Departmental', 'Departmental'),
        ('Course', 'Course'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    managed_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    election_type = models.CharField(max_length=20, choices=ELECTION_TYPES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('End date must be after start date.')
        if self.election_type == 'Departmental' and not self.department:
            raise ValidationError('Department must be specified for departmental elections.')
        if self.election_type == 'Course' and not self.course:
            raise ValidationError('Course must be specified for course-specific elections.')
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Voter(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    elections = models.ManyToManyField(Election, through='VoterRegistration')

    def __str__(self):
        return self.user.email
    
class VoterRegistration(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'election')
        
class Candidate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    number_of_votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.student.user.get_full_name()} in {self.election.title}'
    

class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    cast_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'election')