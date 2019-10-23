__version__ = '0.5.0'

from .fcweb import (
    fcIndex, get, post, put, delete
)

from .right import (
    isLogin, getTokenFromHeader, getPayloadFromHeader, getDB, decode, updateToken, authRight, getBodyAsJson, getBodyAsStr, encodeToken
)

from .response import ResponseEntity

from .utils import pathMatch, createId

from .constant import *

from .connect import (
    getDB, getRedis, userCode2Session, guideCode2Session
)