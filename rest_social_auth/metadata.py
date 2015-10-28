from django.http import Http404
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.metadata import SimpleMetadata


class SocialRestAuthViewMetadata(SimpleMetadata):

    def determine_actions(self, request, view):
        """
        For generic class based views we return information about
        the fields that are accepted for 'PUT' and 'POST' methods.
        """
        actions = {}
        for method in set(['PUT', 'POST']) & set(view.allowed_methods):
            try:
                # Test global permissions
                if hasattr(view, 'check_permissions'):
                    view.check_permissions(view.request)
                # Test object permissions
                if method == 'PUT' and hasattr(view, 'get_object'):
                    view.get_object()
            except (APIException, PermissionDenied, Http404):
                pass
            else:
                # If user has appropriate permissions for the view, include
                # appropriate metadata about the fields that should be supplied.
                serializer = view.get_serializer_in()
                actions[method] = self.get_serializer_info(serializer)
        return actions
