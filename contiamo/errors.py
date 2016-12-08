# Exceptions
import sys


class ContiamoError(Exception):

  def __init__(self, message=None, http_body=None, http_status=None,
         json_body=None, headers=None):
    super().__init__(message)

    if http_body and hasattr(http_body, 'decode'):
      try:
        http_body = http_body.decode('utf-8')
      except BaseException:
        http_body = ('<Could not decode body as utf-8. '
                     'Please report to support@contiamo.com>')

    self._message = message
    self.http_body = http_body
    self.http_status = http_status
    self.json_body = json_body
    self.headers = headers or {}
    # self.request_id = self.headers.get('request-id', None)

  def __unicode__(self):
    # if self.request_id is not None:
    #   msg = self._message or "<empty message>"
    #   return u"Request {0}: {1}".format(self.request_id, msg)
    # else:
    return self._message

  if sys.version_info > (3, 0):
    def __str__(self):
      return self.__unicode__()
  else:
    def __str__(self):
      return unicode(self).encode('utf-8')


class APIConnectionError(ContiamoError):
  pass

class AuthenticationError(ContiamoError):
  pass

class APIError(ContiamoError):
  pass

class InvalidRequestError(ContiamoError):
  pass
