
from django.contrib import admin
from .models import StaffExtra,StudentExtra,Book,LibraryHistory,LibrarianExtra
class StaffExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StaffExtra, StaffExtraAdmin)

class StudentExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentExtra, StudentExtraAdmin)
admin.site.register(Book)
class LibrarianHistoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(LibraryHistory,LibrarianHistoryAdmin)
admin.site.register(LibrarianExtra)