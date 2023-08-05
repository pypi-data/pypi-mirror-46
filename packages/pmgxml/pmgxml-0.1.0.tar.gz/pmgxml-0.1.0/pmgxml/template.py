import re
from anytree import Node, LevelOrderIter
from .helper import coalesce

def tokenize(s, tokens):
    t = ''
    i = 0
    j = len(s)
    while i < j:
        token_found = False
        for tok in tokens:
            if i < j-len(tok) and s[i:i+len(tok)] == tok:
                token_found = True
                yield t
                t = ''
                yield tok
                i += len(tok)
                break
        if not token_found:
            t += s[i]
            i += 1
    if len(t) > 0:
        yield t

def parse_to_tree(tokens, include_filler=False):
    root = Node("root", content='', type='NULL')
    stack = [root]
    for i in range(len(tokens)):
        t = tokens[i]
        if t == '[<':
            stack.append(Node(i, parent=stack[-1], content='', type='NULL'))
            if include_filler:
                Node(i, parent=stack[-1], content=t, type='LBRACK')
        elif t == '>]':
            if include_filler:
                Node(i, parent=stack[-1], content=t, type='RBRACK')
            stack.pop()
        else:
            m = re.match(r'^([^\:]*?)\:(.*)$', t, re.DOTALL)
            if m is None:
                if i > 0 and i < len(tokens)-1 and tokens[i-1] == '[<' and tokens[i+1] == '>]':
                    Node(i, parent=stack[-1], content=t, type='NAME')
                else:
                    Node(i, parent=stack[-1], content=t, type='TEXT')
            else:
                assert len(m.groups()) == 2
                if i > 0 and tokens[i-1] == '[<':
                    Node(i, parent=stack[-1], content=m.group(1), type='PATH')
                    if include_filler:
                        Node(i, parent=stack[-1], content=':', type='COLON')
                    Node(i, parent=stack[-1], content=m.group(2), type='TEXT')
                else:
                    Node(i, parent=stack[-1], content=t, type='TEXT')
    assert len(stack) == 1
    return root

def get_tree_for_template(template):
    tokens = list(tokenize(template, ['[<', '>]']))
    tree = parse_to_tree(tokens, True)
    assert template == ''.join(map(lambda t: t.content, tree.descendants))

    tree = parse_to_tree(tokens)
    for n in LevelOrderIter(tree):
        if len(n.children) > 1 and n.children[0].type == 'PATH':
            setattr(n, 'xpath', n.children[0].content)
            n.type = 'FOREACH'
            n.children[0].parent = None
        if n.type == 'NULL' and len(n.children) == 1 and n.children[0].type == 'NAME':
            n.content = n.children[0].content
            n.xpath = n.children[0].content
            n.type = 'REPLACE'
            n.children[0].parent = None
    setattr(tree, 'xpath', '/')
    for n in tree.descendants:
        assert n.type in ['TEXT', 'FOREACH', 'REPLACE']

    return tree

def walk_subtree(tree, xml, result=[], escape_function=None):
    for n in tree.children:
        if n.type == 'FOREACH':
            for x in xml.xpath(n.xpath):
                walk_subtree(n, x, result, escape_function)
        elif n.type == 'REPLACE':
            newtext = xml.xpath(n.xpath)[0].text
            if escape_function is not None:
                newtext = escape_function(newtext)
            result.append(newtext)
        elif n.type == 'TEXT':
            result.append(n.content)
        else:
            assert False, 'Invalid node type: {}'.format(n.type)
    return result

def apply_xml_to_template(template, xml, escape_function=None):
    tree = get_tree_for_template(template)
    result = ''.join(map(lambda s: str(coalesce(s, '')),
                     walk_subtree(tree, xml, result=[], escape_function=escape_function)))
    return result
