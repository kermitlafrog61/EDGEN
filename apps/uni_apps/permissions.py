from rest_framework.permissions import BasePermission

from .university.models import University


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if view.request.method == 'POST':
            user = request.user
            university = University.objects.get(pk=view.kwargs.get('id'))

            return bool(
                user.is_authenticated and
                user in university.owners.all()
            )
        return True

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            request.user in obj.university.owners.all()
        )


class IsStudentOrOwner(BasePermission):
    def has_permission(self, request, view):
        if view.action in ('create', 'list'):
            user = request.user
            university = University.objects.get(pk=view.kwargs.get('id'))
            return bool(
                user.is_authenticated and
                (user in university.students.all() or
                user in university.owners.all())
            )
        return True
    
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            (request.user in obj.university.owners.all() or
            request.user in obj.university.students.all())
        )
