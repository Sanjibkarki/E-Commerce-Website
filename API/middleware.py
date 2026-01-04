import uuid
from django.utils.deprecation import MiddlewareMixin


class GuestIDMiddleware(MiddlewareMixin):
    """
    Middleware to assign a unique guest ID to anonymous users.
    Stores guest ID in session so it persists across requests.
    """
    GUEST_ID_SESSION_KEY = 'guest_id'

    def process_request(self, request):
        if not request.user.is_authenticated:
            # If user is not authenticated and has no guest_id, create one
            if self.GUEST_ID_SESSION_KEY not in request.session:
                request.session[self.GUEST_ID_SESSION_KEY] = str(uuid.uuid4())
            # Make guest_id accessible on request object for convenience
            request.guest_id = request.session[self.GUEST_ID_SESSION_KEY]
        else:
            # For authenticated users, don't set guest_id
            request.guest_id = None
        return None
