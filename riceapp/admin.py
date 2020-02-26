from django.contrib import admin
from .models import *
# Register your models here.

# class RiceBlastAdmin(admin.AdminSite):
    # site_header = 'Rice Blast'

admin.site.site_header = 'Rice Blast'

admin.site.register(RiceBlastLab)
admin.site.register(People)
admin.site.register(Field)
admin.site.register(Isolate)
admin.site.register(RiceGenotype)
admin.site.register(PathotypingResults)
admin.site.register(VcgGroup)
admin.site.register(DNASequence)
admin.site.register(VCGTest)
admin.site.register(Protocol)
admin.site.register(RiceGBS)



