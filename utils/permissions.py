# -*- coding: utf-8 -*-
from rest_framework import permissions
#from guardian.core import ObjectPermissionChecker

class IsOwnerAndReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to read it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        print('permission checked')
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        print('object permission checked')
        # if request.method in permissions.SAFE_METHODS:
        #     # the obj is specialzed for the diagnostic reports and ect. It needs practitioner to be a Foreignkey
        #     return obj.practitioner.user == request.user
        # return False
        return True

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to read it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        return obj.practitioner.user == request.user


# class ToBeTransferred(permissions.BasePermission):
#     """
#         Object-level permission to only allow owners of an object to read it.
#         Assumes the model instance has an `owner` attribute.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         checker = ObjectPermissionChecker(request.user)
#         return checker.has_perm('can_read', obj.practitioner.user)