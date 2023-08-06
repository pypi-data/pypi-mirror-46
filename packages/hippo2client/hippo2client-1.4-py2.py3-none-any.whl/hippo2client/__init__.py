# -*- coding: utf-8 -*-
import sys

if sys.version_info < (3, 0):
    from hippo2client import Agent
    from hippo2client import MajorEntity
    from hippo2client import Meta
    from hippo2client import MetaTest
    from hippo2client import MetaTestResult
else:
    from hippo2client.hippo2client import Agent
    from hippo2client.hippo2client import MajorEntity
    from hippo2client.hippo2client import Meta
    from hippo2client.hippo2client import MetaTest
    from hippo2client.hippo2client import MetaTestResult


