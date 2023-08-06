from time import time
from rest_framework import authentication, exceptions
from toolbox.slack.verify import verify_signature


class SlackSignedAuthentication(authentication.BaseAuthentication):
    """DRF custom authentication class.

    Verifies Slack Events API requests using signing secrets.

    Make sure `SLACK_SIGNING_SECRET` environment variable is set.

    See details:

    - https://api.slack.com/docs/verifying-requests-from-slack
    - https://www.django-rest-framework.org/api-guide/authentication/

    Example:
        ```
        class MyAPI(APIView):
            authentication_classes = (SlackSignedAuthentication,)
        ```
    """

    def authenticate(self, request):
        from django.contrib.auth.models import AnonymousUser

        req_timestamp = request.META.get("HTTP_X_SLACK_REQUEST_TIMESTAMP")
        req_signature = request.META.get("HTTP_X_SLACK_SIGNATURE")

        # Check if timestamp is more than 5 minutes old
        if abs(time() - int(req_timestamp)) > 60 * 5:
            raise exceptions.AuthenticationFailed("Unauthorized")

        if verify_signature(req_timestamp, req_signature, request.body):
            return (AnonymousUser, None)
        raise exceptions.AuthenticationFailed("Unauthorized")
