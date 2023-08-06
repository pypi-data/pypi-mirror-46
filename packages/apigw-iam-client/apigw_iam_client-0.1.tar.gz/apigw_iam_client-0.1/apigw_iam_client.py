from getpass import getuser
from six.moves.urllib.parse import urlparse

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests


class Client(object):
    
    def __init__(
            self, endpoint, role=None, profile=None, region=None,
            http=None, session=None, session_name=None):
        self.endpoint = endpoint.rstrip('/')
        self.role = role
        self.profile = profile
        self.region = region
        self.http = http or requests.Session()
        self.session = session or self.get_session()
        self.session_name = session_name

    def get(self, path, **kw):
        return self.http.get(
            "%s/%s" % (self.endpoint, path.lstrip('/')),
            auth=self.get_api_auth(),
            params=kw)

    def post(self, path, **kw):
        return self.http.post(
            "%s/%s" % (self.endpoint, path.lstrip('/')),
            json=kw, auth=self.get_api_auth())

    def get_api_auth(self):
        return SignatureAuth(
            self.session.get_credentials(),
            self.get_region(),
            "execute-api")

    def get_region(self):
        if self.region:
            return self.region
        p = urlparse(self.endpoint)
        if p.hostname.endswith('amazonaws.com'):
            self.region = p.hostname.split('.')[2]
            return self.region
        raise ValueError("Region must be explicitly passed for custom domains")
        
    def get_session(self, session_name=None):
        session = boto3.Session()
        if not self.role:
            return session
        
        sts = session.client('sts')
        result = sts.assume_role(
            RoleArn=self.role,
            RoleSessionName=session_name or getuser())['Credentials']

        return boto3.Session(
            aws_access_key_id=result['AccessKeyId'],
            aws_secret_access_key=result['SecretAccessKey'],
            aws_session_token=result['SessionToken'])


class SignatureAuth(requests.auth.AuthBase):
    """AWS V4 Request Signer for Requests.
    """

    def __init__(self, credentials, region, service):
        self.credentials = credentials
        self.region = region
        self.service = service

    def __call__(self, r):
        url = urlparse(r.url)
        path = url.path or '/'
        qs = url.query and '?%s' % url.query or ''
        safe_url = url.scheme + '://' + url.netloc.split(':')[0] + path + qs
        request = AWSRequest(
            method=r.method.upper(), url=safe_url, data=r.body)
        SigV4Auth(
            self.credentials, self.service, self.region).add_auth(request)
        r.headers.update(dict(request.headers.items()))
        return r
