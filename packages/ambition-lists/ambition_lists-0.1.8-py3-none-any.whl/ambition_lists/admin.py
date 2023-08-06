from django.contrib import admin

from .admin_site import ambition_lists_admin
from .models import Antibiotic, Day14Medication, Medication, Neurological
from .models import Symptom, OtherDrug, AbnormalResultsReason
from .models import CXRType, InfiltrateLocation, MissedDoses, ArvRegimens


@admin.register(Antibiotic, site=ambition_lists_admin)
class AntibioticAdmin(admin.ModelAdmin):
    pass


@admin.register(Day14Medication, site=ambition_lists_admin)
class Day14MedicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Medication, site=ambition_lists_admin)
class MedicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Neurological, site=ambition_lists_admin)
class NeurologicalAdmin(admin.ModelAdmin):
    pass


@admin.register(Symptom, site=ambition_lists_admin)
class SymptomAdmin(admin.ModelAdmin):
    pass


@admin.register(OtherDrug, site=ambition_lists_admin)
class OtherDrugAdmin(admin.ModelAdmin):
    pass


@admin.register(AbnormalResultsReason, site=ambition_lists_admin)
class AbnormalResultsReasonAdmin(admin.ModelAdmin):
    pass


@admin.register(CXRType, site=ambition_lists_admin)
class CXRTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(InfiltrateLocation, site=ambition_lists_admin)
class InfiltrateLocationAdmin(admin.ModelAdmin):
    pass


@admin.register(MissedDoses, site=ambition_lists_admin)
class MissedDosesAdmin(admin.ModelAdmin):
    pass


@admin.register(ArvRegimens, site=ambition_lists_admin)
class ArvRegimensAdmin(admin.ModelAdmin):
    pass
