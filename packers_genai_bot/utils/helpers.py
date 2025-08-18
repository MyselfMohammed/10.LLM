# ---------------------- Misc Utilities ----------------------

import re                                           # For regular expression operations like removing Unicode characters

def strip_unicode(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

