from rest_framework import authentication, exceptions
from toolbox.slack.verify import verify_signature


class SlackSignedAuthentication(authentication.BaseAuthentication):
    """DRF custom authentication class.

    Verifies Slack API requests using signing secrets.

    Make sure `SLACK_SIGNING_SECRET` environment variable is set.
    """

    def authenticate(self, request):
        from django.contrib.auth.models import AnonymousUser

        if verify_signature(
            request.META.get("HTTP_X_SLACK_REQUEST_TIMESTAMP"),
            request.META.get("HTTP_X_SLACK_SIGNATURE"),
            request.body,
        ):
            return (AnonymousUser, None)
        raise exceptions.AuthenticationFailed("Unauthorized")
