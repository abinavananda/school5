from django.shortcuts import render,redirect,reverse
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book
from django.views.decorators.http import require_POST
from .models import LibraryHistory
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail

def home_view(request):
    return render(request,'school/index.html')

#for signup/login as admin
def adminclick_view(request):
    return render(request,'school/adminclick.html')

#for s signup/login as staff
def officestaffclick_view(request):
    return render(request,'school/officestaffclick.html')

#for s signup/login as librariansclicks
def librariansclick_view(request):
    return render(request,'school/librariansclick.html')


#for s signup/login as student
def studentclick_view(request):
    return render(request,'school/studentclick.html')


# admin signup

def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'school/adminsignup.html',{'form':form})



def student_signup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'school/studentsignup.html',context=mydict)



def staff_signup_view(request):
    form1=forms.StaffUserForm()
    form2=forms.StaffExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StaffUserForm(request.POST)
        form2=forms.StaffExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_Staff_group = Group.objects.get_or_create(name='STAFF')
            my_Staff_group[0].user_set.add(user)

        return HttpResponseRedirect('stafflogin')
    return render(request,'school/staffsignup.html',context=mydict)




#for checking user is techer , student or admin, librarian
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_staff(user):
    return user.groups.filter(name='STAFF').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()
def is_librarian(user):
    return user.groups.filter(name='LIBRARIAN').exists()

def logout_view(request):
    return render(request,'school/index.html')



def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_staff(request.user):
        accountapproval=models.StaffExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('staff-dashboard')
        else:
            return render(request,'school/staff_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
    elif is_librarian(request.user):
        accountapproval=models.LibrarianExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('librarian-dashboard')
        else:
            return render(request,'school/librarian_wait_for_approval.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    staffcount=models.StaffExtra.objects.all().filter(status=True).count()
    pendingstaffcount=models.StaffExtra.objects.all().filter(status=False).count()

    studentcount=models.StudentExtra.objects.all().filter(status=True).count()
    pendingstudentcount=models.StudentExtra.objects.all().filter(status=False).count()

    staffsalary=models.StaffExtra.objects.filter(status=True).aggregate(Sum('salary'))
    pendingstaffsalary=models.StaffExtra.objects.filter(status=False).aggregate(Sum('salary'))

    studentfee=models.StudentExtra.objects.filter(status=True).aggregate(Sum('fee',default=0))
    pendingstudentfee=models.StudentExtra.objects.filter(status=False).aggregate(Sum('fee'))

 

    #aggregate function return dictionary so fetch data from dictionay
    mydict={
        'staffcount':staffcount,
        'pendingstaffcount':pendingstaffcount,

        'studentcount':studentcount,
        'pendingstudentcount':pendingstudentcount,

        'staffsalary':staffsalary['salary__sum'],
        'pendingstaffsalary':pendingstaffsalary['salary__sum'],

        'studentfee':studentfee['fee__sum'],
        'pendingstudentfee':pendingstudentfee['fee__sum'],

    }

    return render(request,'school/admin_dashboard.html',context=mydict)



#for staff sectionnnnnnnn by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_staff_view(request):
   return render(request,'school/admin_staff.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_staff_view(request):
    form1=forms.StaffUserForm()
    form2=forms.StaffExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StaffUserForm(request.POST)
        form2=forms.StaffExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_staff_group = Group.objects.get_or_create(name='STAFF')
            my_staff_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-staff')
    return render(request,'school/admin_add_staff.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_staff_view(request):
    staff=models.StaffExtra.objects.all().filter(status=True)
    return render(request,'school/admin_view_staff.html',{'staff':staff})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_staff_view(request):
    staff=models.StaffExtra.objects.all().filter(status=False)
    return render(request,'school/admin_approve_staff.html',{'staff':staff})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_staff_view(request,pk):
    staff=models.StaffExtra.objects.get(id=pk)
    staff.status=True
    staff.save()
    return redirect(reverse('admin-approve-staff'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_staff_view(request,pk):
    staff=models.StaffExtra.objects.get(id=pk)
    user=models.User.objects.get(id=staff.user_id)
    user.delete()
    staff.delete()
    return redirect('admin-approve-staff')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_staff_from_school_view(request,pk):
    staff=models.StaffExtra.objects.get(id=pk)
    user=models.User.objects.get(id=staff.user_id)
    user.delete()
    staff.delete()
    return redirect('admin-view-staff')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_staff_view(request,pk):
    staff=models.StaffExtra.objects.get(id=pk)
    user=models.User.objects.get(id=staff.user_id)

    form1=forms.StaffUserForm(instance=user)
    form2=forms.StaffExtraForm(instance=staff)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.StaffUserForm(request.POST,instance=user)
        form2=forms.StaffExtraForm(request.POST,instance=staff)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-staff')
    return render(request,'school/admin_update_staff.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_staff_salary_view(request):
    staff=models.StaffExtra.objects.all()
    return render(request,'school/admin_view_staff_salary.html',{'staff':staff})



#for student by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'school/admin_student.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request,'school/admin_add_student.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=True)
    return render(request,'school/admin_view_student.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentExtraForm(request.POST,instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-student')
    return render(request,'school/admin_update_student.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=False)
    return render(request,'school/admin_approve_student.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    students=models.StudentExtra.objects.get(id=pk)
    students.status=True
    students.save()
    return redirect(reverse('admin-approve-student'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_fee_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'school/admin_view_student_fee.html',{'students':students})


#for staff  LOGIN    SECTIONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_dashboard_view(request):
    staffdata=models.StaffExtra.objects.all().filter(status=True,user_id=request.user.id)
    mydict={
        'salary':staffdata[0].salary,
        'mobile':staffdata[0].mobile,
        'date':staffdata[0].joindate,
    }
    return render(request,'school/staff_dashboard.html',context=mydict)

#for student by stFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_student_view(request):
    return render(request,'school/staff_student.html')


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_add_student_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('staff-student')
    return render(request,'school/staff_add_student.html',context=mydict)


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_view_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=True)
    return render(request,'school/staff_view_student.html',{'students':students})


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_delete_student_from_school_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('staff-view-student')


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_delete_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('staff-approve-student')


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_update_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentExtraForm(request.POST,instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('staff-view-student')
    return render(request,'school/staff_update_student.html',context=mydict)



@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_approve_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=False)
    return render(request,'school/staff_approve_student.html',{'students':students})


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def approve_student_view(request,pk):
    students=models.StudentExtra.objects.get(id=pk)
    students.status=True
    students.save()
    return redirect(reverse('staff-approve-student'))


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_view_student_fee_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'school/staff_view_student_fee.html',{'students':students})



# admin on librariannnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_librarian_view(request):
    return render(request, 'school/admin_librarian.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_librarian_view(request):
    form1 = forms.LibrarianUserForm()
    form2 = forms.LibrarianExtraForm()
    if request.method == 'POST':
        form1 = forms.LibrarianUserForm(request.POST)
        form2 = forms.LibrarianExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            librarian_extra = form2.save(commit=False)
            librarian_extra.user = user
            librarian_extra.status = True
            librarian_extra.save()

            librarian_group = Group.objects.get_or_create(name='LIBRARIAN')
            librarian_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-librarian')
    return render(request, 'school/admin_add_librarian.html', {'form1': form1, 'form2': form2})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_librarian_view(request):
    librarians = models.LibrarianExtra.objects.all().filter(status=True)
    return render(request, 'school/admin_librarian_view.html', {'librarians': librarians})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_librarian_view(request, pk):
    librarian = models.LibrarianExtra.objects.get(id=pk)
    user = models.User.objects.get(id=librarian.user_id)
    user.delete()
    librarian.delete()
    return redirect('admin-view-librarian')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_librarian_from_school_view(request,pk):
    librarian=models.LibrarianExtra.objects.get(id=pk)
    user=models.User.objects.get(id=librarian.user_id)
    user.delete()
    librarian.delete()
    return redirect('admin-view-librarian')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_librarian_view(request,pk):
    librarian=models.LibrarianExtra.objects.get(id=pk)
    user=models.User.objects.get(id=librarian.user_id)

    form1=forms.LibrarianUserForm(instance=user)
    form2=forms.LibrarianExtraForm(instance=librarian)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.LibrarianUserForm(request.POST,instance=user)
        form2=forms.LibrarianExtraForm(request.POST,instance=librarian)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-librarian')
    return render(request,'school/admin_update_librarian.html',context=mydict)

# add book by adminnnnnnnnnnnnnnnnnn


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_book_view(request):
    form = forms.BookForm()
    if request.method == 'POST':
        form = forms.BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-view-book')
    context = {'form': form}
    return render(request, 'school/admin_add_book.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_book_view(request):
    books = models.Book.objects.all() 
    context = {'books': books}
    return render(request, 'school/admin_view_book.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_book_view(request, pk):
    book = get_object_or_404(Book, id=pk)
    if book:
        book.delete()
        messages.success(request, 'Book deleted successfully.')
    return redirect('admin-view-book')  

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_book_from_school_view(request,pk):
    book=models.Book.objects.get(id=pk)
    user=models.User.objects.get(id=book.user_id)
    user.delete()
    book.delete()
    return redirect('admin-view-book')


# librarian areaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

@login_required(login_url='librarianlogin')
@user_passes_test(is_librarian)
def librarian_dashboard_view(request):
    librariandata=models.LibrarianExtra.objects.all().filter(status=True,user_id=request.user.id)
    mydict={
       
        'mobile':librariandata[0].mobile,
       
    }
    return render(request, 'school/librarian_dashboard.html',context=mydict)


@login_required(login_url='librarianlogin')
@user_passes_test(is_librarian)
def librarian_student_view(request):
    return render(request,'school/librarian_student.html')


@login_required(login_url='librarianlogin')
@user_passes_test(is_librarian)
def librarian_add_book(request):
    form = forms.LibraryHistoryForm()
    if request.method == 'POST':
        form = forms.LibraryHistoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('librarian-view-library-history')
    context = {'form': form}
    return render(request, 'school/librarian_add_book.html', context)

@login_required(login_url='librarianlogin')
@user_passes_test(is_librarian)
def librarian_view_library_history(request):
    library = models.LibraryHistory.objects.all() 
    context = {'library': library}
    return render(request, 'school/librarian_view_library_history', context)


@require_POST 
def delete_library_book_view(request, pk):
    library_history_entry = get_object_or_404(LibraryHistory, pk=pk)


    library_history_entry.delete()
    messages.success(request, 'Library record deleted successfully.')
    return redirect('librarian-view-library-history') 

