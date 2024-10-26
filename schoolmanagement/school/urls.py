from django.urls import path
from school import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('',views.home_view,name=''),
    path('adminclick', views.adminclick_view),
    path('officestaffclick', views.officestaffclick_view),
    path('librariansclick', views.librariansclick_view),
    path('studentclick', views.studentclick_view),

# signuppp
   path('adminsignup', views.admin_signup_view),
   path('staffsignup', views.staff_signup_view),
   path('studentsignup', views.student_signup_view,name='studentsignup'),

# loginnn
   path('adminlogin', LoginView.as_view(template_name='school/adminlogin.html')),
   path('stafflogin', LoginView.as_view(template_name='school/stafflogin.html')),
   path('studentlogin', LoginView.as_view(template_name='school/studentlogin.html')),
   path('librarianlogin', LoginView.as_view(template_name='school/librarianlogin.html')),

   path('afterlogin', views.afterlogin_view,name='afterlogin'),

#    log outttttttt
   path('logout', views.logout_view),

# admin areaaaaa
   path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

# admin-staff-area
   path('admin-staff', views.admin_staff_view,name='admin-staff'),
   path('admin-add-staff', views.admin_add_staff_view,name='admin-add-staff'),
   path('admin-view-staff', views.admin_view_staff_view,name='admin-view-staff'),
   path('admin-approve-staff', views.admin_approve_staff_view,name='admin-approve-staff'),
   path('approve-staff/<int:pk>', views.approve_staff_view,name='approve-staff'),
   path('delete-staff/<int:pk>', views.delete_staff_view,name='delete-staff'),
   path('delete-staff-from-school/<int:pk>', views.delete_staff_from_school_view,name='delete-staff-from-school'),
   path('update-staff/<int:pk>', views.update_staff_view,name='update-staff'),
   path('admin-view-staff-salary', views.admin_view_staff_salary_view,name='admin-view-staff-salary'),

#    admin-student-area
    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-add-student', views.admin_add_student_view,name='admin-add-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('delete-student-from-school/<int:pk>', views.delete_student_from_school_view,name='delete-student-from-school'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('admin-approve-student', views.admin_approve_student_view,name='admin-approve-student'),
    path('approve-student/<int:pk>', views.approve_student_view,name='approve-student'),
    path('admin-view-student-fee', views.admin_view_student_fee_view,name='admin-view-student-fee'),

# librarian area
path('admin-librarian', views.admin_librarian_view, name='admin-librarian'),
path('admin-add-librarian', views.admin_add_librarian_view, name='admin-add-librarian'),
path('admin-view-librarian', views.admin_view_librarian_view, name='admin-view-librarian'),
path('delete-librarian/<int:pk>/', views.delete_librarian_view, name='delete-librarian'),
path('delete-librarian-from-school/<int:pk>', views.delete_librarian_from_school_view,name='delete-librarian-from-school'),
path('update-librarian/<int:pk>', views.update_librarian_view,name='update-librarian'),

# book area
path('admin-add-book', views.admin_add_book_view, name='admin-add-book'),
path('admin-view-book', views.admin_view_book_view, name='admin-view-book'),
path('delete-book/<int:pk>/', views.delete_book_view, name='admin_delete_book'),
path('delete-book-from-school/<int:pk>', views.delete_book_from_school_view,name='delete-book-from-school'),

# staff ariaa
    path('staff-dashboard', views.staff_dashboard_view,name='staff-dashboard'),

    
path('staff-student', views.staff_student_view,name='staff-student'),
path('staff-add-student', views.staff_add_student_view,name='staff-add-student'),
path('staff-view-student', views.staff_view_student_view,name='staff-view-student'),
path('staff-delete-student-from-school/<int:pk>', views.staff_delete_student_from_school_view,name='staff-delete-student-from-school'),
path('staff-delete-student/<int:pk>', views.staff_delete_student_view,name='staff-delete-student'),
path('staff-update-student/<int:pk>', views.staff_update_student_view,name='staff-update-student'),
path('staff-approve-student', views.staff_approve_student_view,name='staff-approve-student'),
path('approve-student/<int:pk>', views.approve_student_view,name='approve-student'),
path('staff-view-student-fee', views.staff_view_student_fee_view,name='staff-view-student-fee'),

# Librarian URLs
path('librarian-dashboard', views.librarian_dashboard_view, name='librarian-dashboard'),
path('librarian-student', views.librarian_student_view,name='librarian-student'),
path('librarian-view-library-history', views.librarian_view_library_history, name='librarian-view-library-history'),
path('librarian-add-book', views.librarian_add_book, name='librarian-add-book'),
path('delete-library-book-view/<int:pk>/', views.delete_library_book_view, name='delete-library-book-view'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
