# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['delta']

package_data = \
{'': ['*']}

install_requires = \
['diff-match-patch>=20181111.0,<20181112.0']

extras_require = \
{'html': ['lxml>=4.3,<5.0', 'cssutils>=1.0,<2.0']}

setup_kwargs = {
    'name': 'quill-delta',
    'version': '1.0.0',
    'description': 'Python port of the quill.js delta library that enables operational transformation with aditional functionality for rendering html',
    'long_description': '\n# Delta (Python Port)\n\nPython port of the javascript Delta library for QuillJS: https://github.com/quilljs/delta\n\nSome basic pythonizing has been done, but mostly it works exactly like the above library.\n\nThere is no other python specific documentation at this time, sorry.  Please see the tests\nfor reference examples.\n\n# Rendering HTML in Python\n\nThis library includes a module `delta.html` that renders html from an operation list,\nallowing you to render Quill Delta operations in full from a Python server.\n\nFor example:\n\n    from delta import html\n\n    ops = [ \n        { "insert":"Quill\\nEditor\\n\\n" },\n        { "insert": "bold",\n          "attributes": {"bold": True}},\n        { "insert":" and the " },\n        { "insert":"italic",\n          "attributes": { "italic": True }},\n        { "insert":"\\n\\nNormal\\n" },\n    ]\n\n    html.render(ops)\n\nResult (line formatting added for readability):\n    \n    <p>Quill</p>\n    <p>Editor</p>\n    <p><br></p>\n    <p><strong>bold</strong> and the <em>italic</em></p>\n    <p><br></p>\n    <p>Normal</p>\n\n[See test_html.py](tests/test_html.py) for more examples.\n\n# Developing\n\n## Tests\n\n    > python setup.py test\n\nor \n\n    > py.test\n\n',
    'author': 'Brantley Harris',
    'author_email': 'brantley@forge.works',
    'url': 'https://github.com/forgeworks/delta-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
