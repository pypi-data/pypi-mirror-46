import lxml

XML_ESCAPE = {
    '"': '&quot;',
    "'": '&apos;',
    '<': '&lt;',
    '>': '&gt;',
    '&': '&amp;',
    '#': '&#x23;'
}

def mass_replace(s, replace_vars):
    if s is None:
        return s
    if not isinstance(replace_vars, dict):
        raise Exception('replace_vars must be a dict.')
    for v in replace_vars.keys():
        s = s.replace(v, replace_vars[v])
    return s

def coalesce(*arg):
    for el in arg:
        if el is not None:
            return el
    return None

def escape(s):
    return mass_replace(s, XML_ESCAPE)

def remove_attributes(element, kill_attrs):
    for a in element.attrib:
        if a in kill_attrs:
            del element.attrib[a]

def remove_all_attributes_but(element, keep_attrs):
    for a in element.attrib:
        if a not in keep_attrs:
            del element.attrib[a]

def readxmlfile(path):
    return lxml.objectify.fromstring(open(path, 'rb').read(),
                                     parser=lxml.objectify.makeparser(remove_comments=True))

def writexmlfile(path, body):
    tree = lxml.etree.ElementTree(body)
    tree.write(path, xml_declaration=True, encoding='UTF-8')
