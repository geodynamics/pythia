from opal.conf import settings

if settings.USE_I18N:
    from trans_real import *
else:
    from trans_null import *

del settings
