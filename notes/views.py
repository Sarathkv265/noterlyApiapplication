from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework import generics

from notes.models import User,Task

from notes.seializers import UserSerializer,TaskSerializer

from rest_framework.response import Response

from rest_framework import permissions,authentication

from notes.permissions import OwnerOnly


class UserCreationView(generics.CreateAPIView):
    
    serializer_class = UserSerializer
    
class TaskCeateListView(generics.ListCreateAPIView):
    
    serializer_class = TaskSerializer
    
    queryset = Task.objects.all()
    
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):                        # when creating task  serializer to identify the owner creating the  
        return serializer.save(owner=self.request.user)
    
    #def list(self, request, *args, **kwargs):
        
        #qs= Task.objects.filter(owner=request.user)
        
        #serializer_instance = TaskSerializer(qs,many = True)
        
        #return serializer_instance.
    def get_queryset(self):
        qs =Task.objects.filter(owner=self.request.user)
        
        if "category" in self.request.query_params:
            
            category_value = self.request.query_params.get("category")
            
            qs = qs.filter(category=category_value)
            
        if "priority" in self.request.query_params:
            
            prioeity_value = self.request.query_params.get("priority")
            
            qs = qs.filter(priority=prioeity_value)
            
        return qs
    
    
class TaskRetrieveUpdateDistroyView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Task.objects.all()
    
    serializer_class = TaskSerializer
    
    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    
    permission_classes = [OwnerOnly]
    
from django.db.models import Count
class TaskSummaryApiView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    authentication_classes=[authentication.TokenAuthentication]
    
    def get(self,request,*args,**kwargs):
        
        qs = Task.objects.filter(owner=request.user)
        
        category_summary = qs.values("category").annotate(count=Count("category"))
        status_summary = qs.values("status").annotate(count=Count("status"))
        priority_summary = qs.values("priority").annotate(count=Count("priority"))
        total_tasks = qs.count()
        
        context = {
            "category_summary":category_summary,
            "status_summary":status_summary,
            "priority_summary":priority_summary,
            "total_task":total_tasks
            }
        
        print(context)
        
        return Response(data=context)
    
class CategoryListView(APIView):
    
    def get(self,request,*args,**kwargs):
        
        categories = Task.category_choices
        
        st = {cat for tp in categories for cat in tp}
        
        return Response(data=st)
    
    
#token Authentication


