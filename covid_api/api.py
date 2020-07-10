from rest_framework.settings import api_settings
from django.conf import settings
from rest_framework.throttling import UserRateThrottle
from django.core.exceptions import ImproperlyConfigured

class StaffRateThrottle(UserRateThrottle):
    """
    Limits the rate of API calls that may be made by a given user.
    The user id will be used as a unique cache key if the user is
    authenticated.  For anonymous requests, the IP address of the request will
    be used.
    """
    def allow_request(self, request, view):
        # We can only determine the scope once we're called by the view.
        self.scope = getattr(view, self.scope, None)

        # If a view does not have a `throttle_scope` always allow the request
        if not self.scope:
            return True

        if request.user.is_staff:
            return True

        # Determine the allowed request rate as we normally would during
        # the `__init__` call.
        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)

        # We can now proceed as normal.
        return super().allow_request(request, view)

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        self.rate = self.get_rate(self)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

    def get_rate(self, request=None):
        """
        Determine the string representation of the allowed request rate.
        """
        if not getattr(self, 'scope', None):
            msg = ("You must set either `.scope` or `.rate` for '%s' throttle" %
                   self.__class__.__name__)
            raise ImproperlyConfigured(msg)
        
        throttle_rates = api_settings.DEFAULT_THROTTLE_RATES

        try:
            return throttle_rates[self.scope]
        except KeyError:
            msg = "No default throttle rate set for '%s' scope" % self.scope
            raise ImproperlyConfigured(msg)

class ByMinuteRateThrottle(StaffRateThrottle):
    scope = 'minute'


class ByHourRateThrottle(StaffRateThrottle):
    scope = 'hour'


class ByDayRateThrottle(StaffRateThrottle):
    scope = 'day'