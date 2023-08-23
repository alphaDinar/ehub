from django.contrib import admin
from .models import Scheme,Image,Passage,Video,Pdf,Slide,Meeting

class ImageTable(admin.TabularInline):
    model = Image
class PassageTable(admin.TabularInline):
    model = Passage
class VideoTable(admin.TabularInline):
    model = Video

class SchemeAdmin(admin.ModelAdmin):
    readonly_fields = ['time_started','time_completed']
    list_display = ('course','topic','date_created')
    inlines = [ImageTable,PassageTable,VideoTable]
    class Meta:
        model = Scheme


admin.site.register(Scheme,SchemeAdmin)
admin.site.register(Image)
admin.site.register(Passage)
admin.site.register(Video)
admin.site.register(Pdf)
admin.site.register(Slide)


from .models import RecentScheme

admin.site.register(RecentScheme)

admin.site.register(Meeting)