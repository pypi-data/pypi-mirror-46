import os
import hmac
import hashlib


class MissingSigningSecret(Exception):
    """Error thrown if `SLACK_SIGNING_SECRET` environment variable is not set.
    """

    pass


def generate_signature(
    request_timestamp: str, request_body_bytestring: bytes
) -> str:
    """Generates a Slack request signature.

    Args:
        request_timestamp (str): Value of request's `X-Slack-Request-Timestamp`
            header.
        request_body_bytestring (bytes): Bytestring of the raw request body.

    Returns:
        str: Request hash signature

    """
    SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET", None)
    if not SIGNING_SECRET:
        raise MissingSigningSecret(
            "Must set SLACK_SIGNING_SECRET environment variable"
        )
    req = str.encode("v0:" + request_timestamp + ":") + request_body_bytestring
    request_hash = (
        "v0="
        + hmac.new(str.encode(SIGNING_SECRET), req, hashlib.sha256).hexdigest()
    )
    return request_hash


def verify_signature(
    request_timestamp: str, signature: str, request_body_bytestring: bytes
) -> bool:
    """Verifies a Slack request signature is valid.

    Args:
        request_timestamp (str): Value of request's `X-Slack-Request-Timestamp`
            header.
        signature (str):  Value of request's `X-Slack-Signature` header.
        request_body_bytestring (bytes): Bytestring of the raw request body.

    Returns:
        bool: Whether the request signature is valid
    """
    request_hash = generate_signature(
        request_timestamp, request_body_bytestring
    )
    return hmac.compare_digest(request_hash, signature)
