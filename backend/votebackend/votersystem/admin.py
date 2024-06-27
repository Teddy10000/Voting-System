from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import  Department, Course, Student, Election, Voter, VoterRegistration, Candidate, Vote
from account.models import User
# Register your models here.

# Register Department, Course, Student models
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_departments')
    list_filter = ('department',)
    search_fields = ('name',)

    def get_departments(self, obj):
        return ", ".join([str(d) for d in obj.department.all()])  # Join department names


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'level', 'course', 'age', 'department')
    search_fields = ('user__email', 'student_id', 'level', 'course__name', 'department__name')


# Register Election model with in-depth customization
@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date', 'status', 'managed_by', 'election_type', 'department', 'course')
    list_filter = ('election_type', 'status', 'department', 'course')
    search_fields = ('title', 'description', 'managed_by__user__username')

    readonly_fields = ('managed_by',)  # Make managed_by field read-only

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'department':
            if self.election_type == 'General':
                kwargs['queryset'] = Department.objects.none()  # Disable department selection for general elections
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == 'course':
            if self.election_type != 'Course':
                kwargs['queryset'] = Course.objects.none()  # Disable course selection for non-course elections
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        # Consider adding logic to restrict deletion of ongoing or past elections
        return True  # Allow deletion by default (modify as needed)


# Register Voter, VoterRegistration, Candidate, and Vote models

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_elections')  # Use a method to display election titles

    def get_elections(self, obj):
        return ", ".join([str(e) for e in obj.elections.all()])  # Join election titles

    search_fields = ('user__email', 'elections__title')

@admin.register(VoterRegistration)
class VoterRegistrationAdmin(admin.ModelAdmin):
    list_display = ('voter', 'election', 'registered_on')
    list_filter = ('voter', 'election')
    search_fields = ('voter__user__email', 'election__title')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('student', 'election', 'number_of_votes')
    list_filter = ('election',)
    search_fields = ('student__user__email', 'election__title')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'election', 'candidate', 'cast_on')
    list_filter = ('election',)
    search_fields = ('voter__user__username', 'election__title', 'candidate__student__user__username')