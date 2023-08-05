import logging

from ketoclient.checkallowed import CheckAllowed
from ketoclient.checkallowed import NoCheck
from ketoclient.Properties import ENABLE_RBAC
from ketoclient.Properties import POLICY_MANAGEMENT_URL

logging.basicConfig(
       format = '%(thread)d - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)

if ENABLE_RBAC:
    checkAccess = CheckAllowed(POLICY_MANAGEMENT_URL).checkAccess

else:
    checkAccess = NoCheck().checkAccess

