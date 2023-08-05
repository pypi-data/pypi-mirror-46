"""
@author : puranjan

Keto Client PROPERTIES
"""
import os


if 'POLICY_MANAGEMENT_URL' in os.environ:
    POLICY_MANAGEMENT_URL = os.environ['POLICY_MANAGEMENT_URL']
else:
    POLICY_MANAGEMENT_URL = 'http://localhost:4466'

if 'ENABLE_RBAC' in os.environ:
    ENABLE_RBAC = os.environ['ENABLE_RBAC']
else:
    ENABLE_RBAC = False