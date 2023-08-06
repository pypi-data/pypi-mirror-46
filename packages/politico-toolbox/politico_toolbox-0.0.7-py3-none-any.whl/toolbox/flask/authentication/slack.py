from time import time
from functools import wraps
from toolbox.slack.verify import verify_signature


def slack_signed(f):
    """Authentication decorator.

    Verifies Slack Events API requests using signing secrets.

    Make sure `SLACK_SIGNING_SECRET` environment variable is set.

    See details:

    - https://api.slack.com/docs/verifying-requests-from-slack
    - https://www.django-rest-framework.org/api-guide/authentication/

    Example:
        ```
        @app.route("events-api/", methods=["POST"])
        @slack_signed
        def events_api():
            # ...
        ```
    """
    from flask import request, Response

    @wraps(f)
    def decorated_function(*args, **kwargs):
        req_signature = request.headers.get("X-Slack-Signature")
        req_timestamp = request.headers.get("X-Slack-Request-Timestamp")

        # Check if timestamp is more than 5 minutes old
        if abs(time() - int(req_timestamp)) > 60 * 5:
            return Response("", status=403)

        if verify_signature(req_timestamp, req_signature, request.get_data()):
            return f(*args, **kwargs)

        return Response("", status=403)

    return decorated_function
