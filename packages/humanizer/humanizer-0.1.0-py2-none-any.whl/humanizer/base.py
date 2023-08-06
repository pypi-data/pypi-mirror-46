
# encoding: utf-8

# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()

import mybad


# =========================================
#       ERRORS
# --------------------------------------

class HumanizerError(mybad.Error):
    pass


# =========================================
#       CLASSES
# --------------------------------------

class Humanizer(object):

    @classmethod
    def default(klass):
        if not hasattr(klass, 'instance') or klass.instance is None:
            klass.instance = klass()

        return klass.instance


# =========================================
#       EXPORTS
# --------------------------------------

__all__ = [
    'HumanizerError',
    'Humanizer',
]
