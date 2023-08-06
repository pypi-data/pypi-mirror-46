# pylint: disable-msg=W0622
"""cubicweb-comment packaging information"""

modname = 'comment'
distname = "cubicweb-%s" % modname

numversion = (1, 14, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = "Logilab"
author_email = "contact@logilab.fr"
web = 'http://www.cubicweb.org/project/%s' % distname
description = "commenting system for the CubicWeb framework"
classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]

__depends__ = {'cubicweb': '>= 3.24.0'}
