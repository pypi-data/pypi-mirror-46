# Copyright (C) 2019  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import re

_EMPTY_AUTHOR = {'fullname': b'', 'name': None, 'email': None}

# https://github.com/jonschlinkert/author-regex
_author_regexp = r'([^<(]+?)?[ \t]*(?:<([^>(]+?)>)?[ \t]*(?:\(([^)]+?)\)|$)'


def parse_npm_package_author(author_str):
    """
    Parse npm package author string.

    It works with a flexible range of formats, as detailed below::

        name
        name <email> (url)
        name <email>(url)
        name<email> (url)
        name<email>(url)
        name (url) <email>
        name (url)<email>
        name(url) <email>
        name(url)<email>
        name (url)
        name(url)
        name <email>
        name<email>
        <email> (url)
        <email>(url)
        (url) <email>
        (url)<email>
        <email>
        (url)

    Args:
        author_str (str): input author string

    Returns:
        dict: A dict that may contain the following keys:
            * name
            * email
            * url

    """
    author = {}
    matches = re.findall(_author_regexp,
                         author_str.replace('<>', '').replace('()', ''),
                         re.M)
    for match in matches:
        if match[0].strip():
            author['name'] = match[0].strip()
        if match[1].strip():
            author['email'] = match[1].strip()
        if match[2].strip():
            author['url'] = match[2].strip()
    return author


def extract_npm_package_author(package_json):
    """
    Extract package author from a ``package.json`` file content and
    return it in swh format.

    Args:
        package_json (dict): Dict holding the content of parsed
            ``package.json`` file

    Returns:
        dict: A dict with the following keys:
            * fullname
            * name
            * email

    """

    def _author_str(author_data):
        if type(author_data) is dict:
            author_str = ''
            if 'name' in author_data:
                author_str += author_data['name']
            if 'email' in author_data:
                author_str += ' <%s>' % author_data['email']
            return author_str
        else:
            return author_data

    author_data = {}
    if 'author' in package_json:
        author_str = _author_str(package_json['author'])
        author_data = parse_npm_package_author(author_str)
    elif 'authors' in package_json and len(package_json['authors']) > 0:
        author_str = _author_str(package_json['authors'][0])
        author_data = parse_npm_package_author(author_str)

    name = author_data.get('name')
    email = author_data.get('email')

    fullname = None

    if name and email:
        fullname = '%s <%s>' % (name, email)
    elif name:
        fullname = name

    if not fullname:
        return _EMPTY_AUTHOR

    if fullname:
        fullname = fullname.encode('utf-8')

    if name:
        name = name.encode('utf-8')

    if email:
        email = email.encode('utf-8')

    return {'fullname': fullname, 'name': name, 'email': email}
