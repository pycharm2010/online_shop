from rest_framework.exceptions import Throttled
from rest_framework.throttling import UserRateThrottle

from rest_framework.throttling import UserRateThrottle


class PostLikeThrottle(UserRateThrottle):
    scope = "post_like"
    THROTTLE_RATES = {
        "post_like": "6/min",
    }


