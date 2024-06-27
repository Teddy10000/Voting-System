"""
URL configuration for votebackend project.

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
from django.urls import path , include
from .serializers import StudentUpdateSerializer
from .views import (StudentUpdateView, StudentListView,
    StudentCreateViewSet,
    DepartmentCreateView,
    DepartmentListView,
    DepartmentUpdateView,
    CourseCreateView,
    VoterCreateView, VoterListView, VoterDetailView,
    CourseListView,
    CourseUpdateView, )
from account import urls
from .views import VoteCreateView, CandidateCreateView, CandidateListView, CandidateDetailView , ElectionListView, ElectionDetailView, ElectionCreateView, ListVoteView, RetrieveVoteView, DeleteVoteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include(urls)),
        #STUDENT ENDPOINTS
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/create/', StudentCreateViewSet.as_view({'post': 'create'}), name='student-create'),
    path('students/<int:pk>/', StudentUpdateView.as_view(), name='student-detail'),


    path('candidates/', CandidateListView.as_view(), name='candidate-list'),
    path('candidates/create/', CandidateCreateView.as_view(), name='candidate-create'),
    path('candidates/<int:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),
      
      # Department endpoints
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('departments/create/', DepartmentCreateView.as_view(), name='department-create'),
    path('departments/<int:pk>/', DepartmentUpdateView.as_view(), name='department-detail'),

    # Course endpoints
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/', CourseUpdateView.as_view(), name='course-detail'),

    path('elections/', ElectionListView.as_view(), name='election-list'),
    path('elections/<int:pk>/', ElectionDetailView.as_view(), name='election-detail'),
    path('elections/create/', ElectionCreateView.as_view(), name='election-create'),


    path('votes/', VoteCreateView.as_view(), name='create-vote'),
    path('votes/list/', ListVoteView.as_view(), name='list-votes'),
    path('votes/<int:pk>/', RetrieveVoteView.as_view(), name='retrieve-vote'),
    path('votes/<int:pk>/delete/', DeleteVoteView.as_view(), name='delete-vote'),

    path('voters/', VoterListView.as_view(), name='voter-list'),
    path('voters/create/', VoterCreateView.as_view(), name='voter-create'),
    path('voters/<int:pk>/', VoterDetailView.as_view(), name='voter-detail'),
]
