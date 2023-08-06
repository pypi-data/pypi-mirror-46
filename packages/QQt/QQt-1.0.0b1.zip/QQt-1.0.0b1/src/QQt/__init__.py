# Copyright (c) 2012-2019 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib/

from . __config__ import * ; del __config__
from .__about__   import * ; del __about__

import sys
__import__(origin)
sys.modules[__name__] = sys.modules[origin]
for name, module in sys.modules.copy().items():
    if name.startswith(origin + "."):
        sys.modules[__name__ + name[len(origin):]] = sys.modules[name]
del origin, sys
