import re
from django import forms
from django.shortcuts import render


class MyForm(forms.Form):
    no_of_students = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Number Of Students...'}))
    no_of_branches = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Number Of Branches...'}))
    branches = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Branches(eg:comps extc it)...'}))
    classroom_capacity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Classroom Capacity...'}))


def index(request):
    counter = 0
    classroom = 1
    students = 0
    classroomBranch = dict()  # All branches of a class
    classroomRollNo = dict()  # All roll nos of a class
    form = MyForm(request.POST or None)
    if form.is_valid():
        noOfStudents = form.cleaned_data['no_of_students']
        branches = form.cleaned_data['branches']
        branches = re.split(' ', branches) # spliting spaces between branches
        classroomCapacity = form.cleaned_data['classroom_capacity']
        for i in range(1, noOfStudents + 1):
            for branch in branches:
                if students < noOfStudents:
                    if classroom not in classroomRollNo:
                        classroomRollNo[classroom] = list()
                        classroomRollNo[classroom].append(i)
                    else:
                        classroomRollNo[classroom].append(i)
                    if classroom not in classroomBranch:
                        classroomBranch[classroom] = list()
                        classroomBranch[classroom].append(branch)
                    else:
                        classroomBranch[classroom].append(branch)
                    students += 1
                    counter += 1
                    if counter == classroomCapacity and students < noOfStudents:
                        counter = 0
                        classroom += 1
                else:
                    break
        return render(request, 'list.html',
                      {'branches': classroomBranch, 'rollnos': classroomRollNo}) # passing output of program to list.html
    return render(request, 'index.html', {"form": form}) # displaying form on index page
