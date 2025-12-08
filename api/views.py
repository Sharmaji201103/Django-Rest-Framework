from django.shortcuts import render,get_object_or_404
# from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer,EmployeeSerializer,ImportSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


from django.http import Http404

from rest_framework.views import APIView
from employees.models import Employee

from rest_framework import mixins,generics,viewsets

from blogs.models import Blog,Comment
from blogs.serializers import BlogSerializer,CommentSerializer
from .paginations import CustomPaginaton
from .filters import EmployeeFilter


from rest_framework.parsers import MultiPartParser,FormParser
from exceldata.models import DataImport
import pandas as pd

@api_view(['GET','POST'])
def studentsView(request):
    if request.method=='GET':
        students=Student.objects.all()
        serializer=StudentSerializer(students,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method=='POST':
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','PUT','DELETE'])
def studentDetailView(request,id):
    try:
        student=Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        serializer=StudentSerializer(student)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method=='PUT':
        serializer=StudentSerializer(student,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# class Employees(APIView):
#     def get(self,request):
#         employees=Employee.objects.all()
#         serializer=EmployeeSerializer(employees,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
#     def post(self,request):
#         serializer=EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
# class EmployeeDetail(APIView):
#     def get_object(self,id):
#         try:
#             return Employee.objects.get(id=id)
#         except Employee.DoesNotExist:
#             raise Http404
        
#     def get(self,request,id):
#         employee=self.get_object(id)
#         serializer=EmployeeSerializer(employee)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
#     def put(self,request,id):
#         employee=self.get_object(id)
#         serializer=EmployeeSerializer(employee,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
#     def delete(self,request,id):
#         employee=self.get_object(id)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


"""  

# Mixins
class Employees(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    
    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)
    
class EmployeeDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    
    def get(self,request,pk):
        return self.retrieve(request,pk)
    
    def put(self,request,pk):
        return self.update(request,pk)
    
    def delete(self,request,pk):
        return self.destroy(request,pk)
        
"""

""" 
#Generics
class Employees(generics.ListCreateAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    lookup_field='pk'
    
"""



#ViewSets
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    pagination_class=CustomPaginaton
    filterset_class=EmployeeFilter
    
""" 
    def list(self,request):
        queryset=Employee.objects.all()
        serializer=EmployeeSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer=EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        employee=get_object_or_404(Employee,pk=pk)
        serializer=EmployeeSerializer(employee)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def update(self,request,pk=None):
        employee=get_object_or_404(Employee,pk=pk)
        serializer=EmployeeSerializer(employee,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk=None):
        employee=get_object_or_404(Employee,pk=pk)
        employee.delete()
        return request(status=status.HTTP_204_NO_CONTENT)
"""

#Blogs
class BlogsView(generics.ListCreateAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    
class CommentsView(generics.ListCreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    
class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    lookup_field='pk'
    
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comment=Comment.objects.all()
    serializer_class=CommentSerializer
    lookup_field='pk'
    
    
    
class ImportAPIView(APIView):
    serializer_class=ImportSerializer
    parser_classes=[MultiPartParser,FormParser]
    
    def post(self,request):
        try:
            data=request.FILES
            serializer=self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status':False,
                    'message':'Provide a valid file'
                },status=status.HTTP_400_BAD_REQUEST)
            excel_file=data.get('file')
            df=pd.read_excel(excel_file,sheet_name=0)
            dataimports=[]
            for index,row in df.iterrows():
                first_name=row['FirstName']
                last_name=row['LastName']
                email=row['Email']
                dataimport=DataImport.objects.filter(email=email)
                if dataimport.exists():
                    continue
                else:
                    dataimport=DataImport(
                        first_name=first_name,
                        last_name=last_name,
                        email=email
                    )
                    dataimports.append(dataimport)
            DataImport.objects.bulk_create(dataimports)
            return Response({
                'status':True,
                'message':"Profile imported successfully"
            },status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'status':False,
                'message':'We could not complete the import process.'
            },status=status.HTTP_400_BAD_REQUEST)
            
class ExportAPIView(APIView):
    def post(self,request):
        try:
            dataexport=DataImport.objects.all()
            df=pd.DataFrame.from_records(dataexport.values(),exclude=['date_created'])
            df.to_excel('ProfileExport.xlsx',index=False)
            return Response({
                'status':True,
                'message':'Profile exported successfully'
            },status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'status':False,
                'message':'We could not complete the export process.'
            },status=status.HTTP_400_BAD_REQUEST)