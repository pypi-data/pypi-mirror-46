from datetime import timedelta

from ipware.ip import get_ip

from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext as _

from .exception import ThrottlingException
from .models import InputLoggedRequest


class ThrottlingValidator:

    def __init__(self, timeframe, throttle_at, description):
        self.timeframe = timeframe
        self.throttle_at = throttle_at
        self.description = description

    def validate(self, request):
        if not getattr(settings, 'TURN_OFF_THROTTLING', False) and not self._validate(request):
            raise ThrottlingException(self.description)

    def _validate(self, request):
        raise NotImplemented

    def __repr__(self):
        return '<{} (timeframe={}, throttle_at={}, description={})>'.format(
            self.__class__.__name__, self.timeframe, self.throttle_at, self.description
        )


class PerRequestThrottlingValidator(ThrottlingValidator):

    def __init__(self, timeframe, throttle_at, description=_('Slow down')):
        super(PerRequestThrottlingValidator, self).__init__(timeframe, throttle_at, description)

    def _validate(self, request):
        count_same_requests = InputLoggedRequest.objects.filter(
            ip=get_ip(request), path=request.path,
            request_timestamp__gte=timezone.now() - timedelta(seconds=self.timeframe),
            method=request.method.upper()).count()
        return count_same_requests <= self.throttle_at


class UnsuccessfulLoginThrottlingValidator(ThrottlingValidator):

    def __init__(self, timeframe, throttle_at, description=_('Too many login attempts')):
        super(UnsuccessfulLoginThrottlingValidator, self).__init__(timeframe, throttle_at, description)

    def _validate(self, request):
        count_same_requests = InputLoggedRequest.objects.filter(
            ip=get_ip(request), path=request.path,
            request_timestamp__gte=timezone.now() - timedelta(seconds=self.timeframe),
            type=InputLoggedRequest.UNSUCCESSFUL_LOGIN_REQUEST).count()
        return count_same_requests <= self.throttle_at


class SuccessfulLoginThrottlingValidator(ThrottlingValidator):

    def __init__(self, timeframe, throttle_at, description=_('You are logged too much times')):
        super(SuccessfulLoginThrottlingValidator, self).__init__(timeframe, throttle_at, description)

    def _validate(self, request):
        count_same_requests = InputLoggedRequest.objects.filter(
            ip=get_ip(request), path=request.path,
            request_timestamp__gte=timezone.now() - timedelta(seconds=self.timeframe),
            type=InputLoggedRequest.SUCCESSFUL_LOGIN_REQUEST).count()
        return count_same_requests <= self.throttle_at
