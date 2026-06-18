from django.contrib import admin
from .models import Complaint,ComplaintSupport
from users.models import User


def formfield_for_foreignkey(self, db_field, request, **kwargs):
    obj_id = request.resolver_match.kwargs.get("object_id")

    if obj_id:
        complaint = Complaint.objects.get(pk=obj_id)

        if db_field.name == "assignedOfficer":
            kwargs["queryset"] = User.objects.filter(
                role="officer",
                department=complaint.department
            )

        elif db_field.name == "assignedWorker":
            kwargs["queryset"] = User.objects.filter(
                role="worker",
                department=complaint.department
            )

    return super().formfield_for_foreignkey(
        db_field, request, **kwargs
    )

admin.site.register(Complaint)
admin.site.register(ComplaintSupport)