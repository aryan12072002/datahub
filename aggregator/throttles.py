# aggregator/throttles.py
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# Custom throttle for anonymous users
class AnonBurstRateThrottle(AnonRateThrottle):
    rate = '10/min'  # anonymous users can hit 10 requests per minute

# Custom throttle for authenticated users
class UserBurstRateThrottle(UserRateThrottle):
    rate = '30/min'  # logged-in users can hit 30 requests per minute
