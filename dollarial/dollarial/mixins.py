from django.contrib.auth.mixins import AccessMixin


class ClerkRequiredMixin(AccessMixin):
    """Verify that the current user is clerk."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if (not hasattr(request.user, 'clerk')
                or request.user.clerk is None
                or not request.user.clerk.is_employee) \
                and not request.user.is_staff:
            self.raise_exception = True
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin(AccessMixin):
    """Verify that the current user is clerk."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_staff:
            self.raise_exception = True
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
