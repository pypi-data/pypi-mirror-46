"""
Verifying requests from Slack <https://api.slack.com/docs/verifying-requests-from-slack>
"""
import hmac
import hashlib

import flask


def verify(slack_signing_secret: str, request: flask.Request) -> bool:
    """Return if the request is verified.
    
    slack_signing_secret: Signing Secret from Slack.
    request: flask.Request object from flask.
    """
    # Retrive request body.
    # And transform bytes to string inorder to be used with format string.
    request_body = request.get_data().decode("utf-8") 
    
    # Retrive the X-Slack-Request-Timestamp header on the HTTP request, and the body of the request.
    timestamp = request.headers['X-Slack-Request-Timestamp']
    
    # Calculate our signature.
    sig_basestring = f"v0:{timestamp}:{request_body}".encode('utf-8')
    hashed = hmac.new(
        slack_signing_secret.encode('utf-8'), 
        sig_basestring, 
        digestmod=hashlib.sha256
    ).hexdigest()
    my_signature = f"v0={hashed}"
    
    # Signature from incoming request headers.
    slack_signature = request.headers['X-Slack-Signature']
    
    return hmac.compare_digest(my_signature, slack_signature)
