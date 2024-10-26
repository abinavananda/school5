from django import forms
from django.contrib.auth.models import User
from .models import LibraryHistory, StudentExtra, Book
from . import models

#for admin
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']


#for student related form
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['roll','cl','mobile','fee','status']




#for Staff related form
class StaffUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class StaffExtraForm(forms.ModelForm):
    class Meta:
        model=models.StaffExtra
        fields=['salary','mobile','status']

# forms.py
class LibrarianUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

class LibrarianExtraForm(forms.ModelForm):
    class Meta:
        model = models.LibrarianExtra
        fields = ['mobile', 'status']



class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ['title', 'author', 'published_date']

class LibraryHistoryForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=StudentExtra.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select Student'
        }),
        empty_label="Select Student"
    )
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select Book'
        }),
        empty_label="Select Book"
    )

    class Meta:
        model = LibraryHistory
        fields = ['student', 'book', 'borrow_date', 'return_date']
        widgets = {
            'borrow_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Borrow Date',
                'type': 'date'
            }),
            'return_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Return Date',
                'type': 'date'
            }),
        }