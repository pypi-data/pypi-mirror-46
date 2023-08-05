#!/usr/bin/env python

"""
A minified version of ete3.parser.newick
"""

from __future__ import print_function
import re
import os
import six


# Regular expressions used for reading newick format
_ILEGAL_NEWICK_CHARS = r":;(),\[\]\t\n\r="
_NON_PRINTABLE_CHARS_RE = r"[\x00-\x1f]+"
_NHX_RE = r"\[&&NHX:[^\]]*\]"
_FLOAT_RE = r"\s*[+-]?\d+\.?\d*(?:[eE][-+]\d+)?\s*"
_NAME_RE = r"[^():,;]+?"

# default formats
FLOAT_FORMATTER = "%0.6g"
NAME_FORMATTER = "%s"
_ITERABLE_TYPES = set([list, set, tuple, frozenset])


# Allowed formats. This table is used to read and write newick using
# different convenctions. You can also add your own formats in an easy way.
#
#
# FORMAT: 
#   [[LeafAttr1, LeafAttr1Type, Strict?], 
#   [LeafAttr2, LeafAttr2Type, Strict?],
#   [InternalAttr1, InternalAttr1Type, Strict?], 
#   [InternalAttr2, InternalAttr2Type, Strict?]]
#
# Attributes are placed in the newick as follows:
#
# .... ,LeafAttr1:LeafAttr2)InternalAttr1:InternalAttr2 ...
#
#
#           /-A
# -NoName--|
#          |          /-B
#           \C-------|
#                    |          /-D
#                     \E-------|
#                               \-G
#
# Format 0 = (A:0.35,(B:0.72,(D:0.60,G:0.12)1.00:0.64)1.00:0.56);
# Format 1 = (A:0.35,(B:0.72,(D:0.60,G:0.12)E:0.64)C:0.56);
# Format 2 = (A:0.35,(B:0.72,(D:0.60,G:0.12)1.00:0.64)1.00:0.56);
# Format 3 = (A:0.35,(B:0.72,(D:0.60,G:0.12)E:0.64)C:0.56);
# Format 4 = (A:0.35,(B:0.72,(D:0.60,G:0.12)));
# Format 5 = (A:0.35,(B:0.72,(D:0.60,G:0.12):0.64):0.56);
# Format 6 = (A:0.35,(B:0.72,(D:0.60,G:0.12)E)C);
# Format 7 = (A,(B,(D,G)E)C);
# Format 8 = (A,(B,(D,G)));
# Format 9 = (,(,(,)));
# Format 10 = ((a[&Z=1,Y=2], b[&Z=1,Y=2]):1.0[&L=1,W=0], c[&Z=1,Y=2]):2.0[%L=1,W=1];"




NW_FORMAT = {
  0: [['name', str, True],  ["dist", float, True],    ['support', float, True],   ["dist", float, True]], # Flexible with support
  1: [['name', str, True],  ["dist", float, True],    ['name', str, True],      ["dist", float, True]], # Flexible with internal node names
  2: [['name', str, False], ["dist", float, False],   ['support', float, False],  ["dist", float, False]],# Strict with support values
  3: [['name', str, False], ["dist", float, False],   ['name', str, False],     ["dist", float, False]], # Strict with internal node names
  4: [['name', str, False], ["dist", float, False],   [None, None, False],        [None, None, False]],
  5: [['name', str, False], ["dist", float, False],   [None, None, False],        ["dist", float, False]],
  6: [['name', str, False], [None, None, False],      [None, None, False],        ["dist", float, False]],
  7: [['name', str, False], ["dist", float, False],   ["name", str, False],       [None, None, False]],
  8: [['name', str, False], [None, None, False],      ["name", str, False],       [None, None, False]],
  9: [['name', str, False], [None, None, False],      [None, None, False],        [None, None, False]], # Only topology with node names
  100: [[None, None, False],  [None, None, False],      [None, None, False],        [None, None, False]] # Only Topology
}


class NewickError(Exception):
    """Exception class designed for NewickIO errors."""
    def __init__(self, value):
        Exception.__init__(self, value)


def set_float_format(formatter):
    """
    Set the conversion format used to represent float distances and support
    values in the newick representation of trees.

    For example, use set_float_format('%0.32f') to specify 32 decimal numbers
    when exporting node distances and bootstrap values.

    Scientific notation (%e) or any other custom format is allowed. The
    formatter string should not contain any character that may break newick
    structure (i.e.: ":;,()")
    """
    global FLOAT_FORMATTER
    FLOAT_FORMATTER = formatter
    #DIST_FORMATTER = ":"+FLOAT_FORMATTER



def format_node(
    node, 
    node_type, 
    format,
    dist_formatter=None,
    support_formatter=None,
    name_formatter=None):
    """
    Used when writing newick...
    """

    # use default formatters unless specified
    if dist_formatter is None: 
        dist_formatter = FLOAT_FORMATTER
    if support_formatter is None: 
        support_formatter = FLOAT_FORMATTER
    if name_formatter is None: 
        name_formatter = NAME_FORMATTER

    # apply formatting to leaves or nodes
    if node_type == "leaf":
        container1 = NW_FORMAT[format][0][0]  # name
        container2 = NW_FORMAT[format][1][0]  # dists
        converterFn1 = NW_FORMAT[format][0][1]
        converterFn2 = NW_FORMAT[format][1][1]
        flexible1 = NW_FORMAT[format][0][2]
    else:
        container1 = NW_FORMAT[format][2][0]  # support/name
        container2 = NW_FORMAT[format][3][0]  # dist
        converterFn1 = NW_FORMAT[format][2][1]
        converterFn2 = NW_FORMAT[format][3][1]
        flexible1 = NW_FORMAT[format][2][2]

    if converterFn1 == str:
        try:
            FIRST_PART = re.sub("["+_ILEGAL_NEWICK_CHARS+"]", "_", \
                                  str(getattr(node, container1)))
            if not FIRST_PART and container1 == 'name' and not flexible1:
                FIRST_PART = "NoName"
        except (AttributeError, TypeError):
            FIRST_PART = "?"
        FIRST_PART = name_formatter %FIRST_PART
    elif converterFn1 is None:
        FIRST_PART = ""
    else:
        try:
            #FIRST_PART =  "%0.6f" %(converterFn2(getattr(node, container1)))
            FIRST_PART = support_formatter %(converterFn2(getattr(node, container1)))
        except (ValueError, TypeError):
            FIRST_PART = "?"


    if converterFn2 == str:
        try:
            SECOND_PART = ":"+re.sub("["+_ILEGAL_NEWICK_CHARS+"]", "_", \
                                  str(getattr(node, container2)))
        except (ValueError, TypeError):
            SECOND_PART = ":?"
    elif converterFn2 is None:
        SECOND_PART = ""
    else:
        try:
            #SECOND_PART = ":%0.6f" %(converterFn2(getattr(node, container2)))
            SECOND_PART = ":%s" %(dist_formatter %(converterFn2(getattr(node, container2))))
        except (ValueError, TypeError):
            SECOND_PART = ":?"

    return "%s%s" %(FIRST_PART, SECOND_PART)



def read_newick(newick, root_node=None, format=0):
    """ 
    Reads a newick tree from either a string or a file, and returns
    an ETE tree structure.

    A previously existent node object can be passed as the root of the
    tree, which means that all its new children will belong to the same
    class as the root (This allows to work with custom TreeNode objects).

    You can also take advantage from this behaviour to concatenate
    several tree structures.
    """

    ## check newick type as a string or filepath, Toytree parses urls to str's
    if isinstance(newick, six.string_types):   
        if os.path.exists(newick):
            if newick.endswith('.gz'):
                import gzip
                nw = gzip.open(newick).read()
            else:
                nw = open(newick, 'rU').read()
        else:
            nw = newick

        ## get re matcher for testing newick formats
        matcher = compile_matchers(formatcode=format)
        nw = nw.strip()      

        # it is a TreeNode already?  
        if not nw.startswith('(') and nw.endswith(';'):
            return _read_node_data(nw[:-1], root_node, "single", matcher, format)

        # it is text
        elif not nw.startswith('(') or not nw.endswith(';'):
            raise NewickError('Unexisting tree file or Malformed newick tree structure.')
        else:
            return _read_newick_from_string(nw, root_node, matcher, format)
    else:
        raise NewickError("'newick' argument must be either a filename or a newick string.")



def _read_newick_from_string(nw, root_node, matcher, formatcode):
    """ Reads a newick string in the New Hampshire format. """
    if nw.count('(') != nw.count(')'):
        raise NewickError('Parentheses do not match. Broken tree structure?')

    # white spaces and separators are removed
    nw = re.sub("[\n\r\t]+", "", nw)

    current_parent = None
    # Each chunk represents the content of a parent node, and it could contain
    # leaves and closing parentheses.
    # We may find:
    # leaf, ..., leaf,
    # leaf, ..., leaf))),
    # leaf)), leaf, leaf))
    # leaf))
    # ) only if formatcode == 100

    for chunk in nw.split("(")[1:]:
        # If no node has been created so far, this is the root, so use the node.
        current_parent = root_node if current_parent is None else current_parent.add_child()

        subchunks = [ch.strip() for ch in chunk.split(",")]
        # We should expect that the chunk finished with a comma (if next chunk
        # is an internal sister node) or a subchunk containing closing parenthesis until the end of the tree.
        #[leaf, leaf, '']
        #[leaf, leaf, ')))', leaf, leaf, '']
        #[leaf, leaf, ')))', leaf, leaf, '']
        #[leaf, leaf, ')))', leaf), leaf, 'leaf);']
        if subchunks[-1] != '' and not subchunks[-1].endswith(';'):
            raise NewickError('Broken newick structure at: %s' %chunk)

        # lets process the subchunks. Every closing parenthesis will close a
        # node and go up one level.
        for i, leaf in enumerate(subchunks):
            if leaf.strip() == '' and i == len(subchunks) - 1:
                continue # "blah blah ,( blah blah"
            closing_nodes = leaf.split(")")

            # first part after splitting by ) always contain leaf info
            _read_node_data(closing_nodes[0], current_parent, "leaf", matcher, formatcode)

            # next contain closing nodes and data about the internal nodes.
            if len(closing_nodes)>1:
                for closing_internal in closing_nodes[1:]:
                    closing_internal =  closing_internal.rstrip(";")
                    # read internal node data and go up one level
                    _read_node_data(closing_internal, current_parent, "internal", matcher, formatcode)
                    current_parent = current_parent.up
    return root_node



def _parse_extra_features(node, NHX_string):
    """ 
    Reads node's extra data form its NHX string. NHX uses this
    format:  [&&NHX:prop1=value1:prop2=value2] 
    """
    NHX_string = NHX_string.replace("[&&NHX:", "")
    NHX_string = NHX_string.replace("]", "")
    for field in NHX_string.split(":"):
        try:
            pname, pvalue = field.split("=")
        except ValueError as e:
            raise NewickError('Invalid NHX format %s' % field)
        node.add_feature(pname, pvalue)



def compile_matchers(formatcode):
    """
    Tests newick string against format types? and makes a re.compile.
    Compiles a re matcher for checking newick formats
    """
    matchers = {}
    for node_type in ["leaf", "single", "internal"]:
        if node_type == "leaf" or node_type == "single":
            container1 = NW_FORMAT[formatcode][0][0]
            container2 = NW_FORMAT[formatcode][1][0]
            converterFn1 = NW_FORMAT[formatcode][0][1]
            converterFn2 = NW_FORMAT[formatcode][1][1]
            flexible1 = NW_FORMAT[formatcode][0][2]
            flexible2 = NW_FORMAT[formatcode][1][2]
        else:
            container1 = NW_FORMAT[formatcode][2][0]
            container2 = NW_FORMAT[formatcode][3][0]
            converterFn1 = NW_FORMAT[formatcode][2][1]
            converterFn2 = NW_FORMAT[formatcode][3][1]
            flexible1 = NW_FORMAT[formatcode][2][2]
            flexible2 = NW_FORMAT[formatcode][3][2]

        if converterFn1 == str:
            FIRST_MATCH = "("+_NAME_RE+")"
        elif converterFn1 == float:
            FIRST_MATCH = "("+_FLOAT_RE+")"
        elif converterFn1 is None:
            FIRST_MATCH = '()'

        if converterFn2 == str:
            SECOND_MATCH = "(:"+_NAME_RE+")"
        elif converterFn2 == float:
            SECOND_MATCH = "(:"+_FLOAT_RE+")"
        elif converterFn2 is None:
            SECOND_MATCH = '()'

        if flexible1 and node_type != 'leaf':
            FIRST_MATCH += "?"
        if flexible2:
            SECOND_MATCH += "?"

        matcher_str = r'^\s*%s\s*%s\s*(%s)?\s*$' % (FIRST_MATCH, SECOND_MATCH, _NHX_RE)
        compiled_matcher = re.compile(matcher_str)
        matchers[node_type] = [container1, container2, converterFn1, converterFn2, compiled_matcher]

    return matchers



def _read_node_data(subnw, current_node, node_type, matcher, formatcode):
    """
    Reads a leaf node from a subpart of the original newicktree 
    """

    if node_type == "leaf" or node_type == "single":
        if node_type == "leaf":
            node = current_node.add_child()
        else:
            node = current_node
    else:
        node = current_node

    subnw = subnw.strip()
    
    if not subnw and node_type == 'leaf' and formatcode != 100:
        raise NewickError('Empty leaf node found')
    elif not subnw:
        return

    container1, container2, converterFn1, converterFn2, compiled_matcher = matcher[node_type]
    data = re.match(compiled_matcher, subnw)
    if data:
        data = data.groups()
        # This prevents ignoring errors even in flexible nodes:
        if subnw and data[0] is None and data[1] is None and data[2] is None:
            raise NewickError("Unexpected newick format '%s'" %subnw)

        if data[0] is not None and data[0] != '':
            node.add_feature(container1, converterFn1(data[0].strip()))

        if data[1] is not None and data[1] != '':
            node.add_feature(container2, converterFn2(data[1][1:].strip()))

        if data[2] is not None \
                and data[2].startswith("[&&NHX"):
            _parse_extra_features(node, data[2])
    else:
        raise NewickError("Unexpected newick format '%s' " %subnw[0:50])
    return



def write_newick(rootnode, 
    features=None, 
    format=1, 
    format_root_node=True,
    is_leaf_fn=None, 
    dist_formatter=None,
    support_formatter=None,
    name_formatter=None):
    """ 
    Iteratively export a tree structure and returns its NHX
    representation. 
    """
    newick = []
    leaf = is_leaf_fn if is_leaf_fn else lambda n: not bool(n.children)
    for postorder, node in rootnode.iter_prepostorder(is_leaf_fn=is_leaf_fn):

        # what is this...
        if postorder:
            newick.append(")")
            if node.up is not None or format_root_node:
                newick.append(format_node(node, "internal", format,
                                          dist_formatter=dist_formatter,
                                          support_formatter=support_formatter,
                                          name_formatter=name_formatter))
                newick.append(_get_features_string(node, features))

        # versus this?
        else:
            if node is not rootnode and node != node.up.children[0]:
                newick.append(",")

            if leaf(node):
                safe_name = re.sub("["+_ILEGAL_NEWICK_CHARS+"]", "_", \
                               str(getattr(node, "name")))
                newick.append(format_node(node, "leaf", format,
                              dist_formatter=dist_formatter,
                              support_formatter=support_formatter,
                              name_formatter=name_formatter))
                newick.append(_get_features_string(node, features))
            else:
                newick.append("(")

    newick.append(";")
    return ''.join(newick)



def _get_features_string(self, features=None):
    """ 
    Generates the extended newick string NHX with extra data about a node.
    """
    string = ""
    if features is None:
        features = []
    elif features == []:
        features = self.features

    for pr in features:
        if hasattr(self, pr):
            raw = getattr(self, pr)
            
            # convert to a string
            if type(raw) in _ITERABLE_TYPES:
                raw = '|'.join([str(i) for i in raw])
            elif type(raw) == dict:
                raw = '|'.join(
                    ["{}-{}".format(i, j) for (i, j) in raw.items()]
                )
                # map(lambda x,y: "%s-%s" %(x, y), six.iteritems(raw)))
            elif type(raw) == str:
                pass
            else:
                raw = str(raw)

            value = re.sub("[" + _ILEGAL_NEWICK_CHARS + "]", "_", raw)
            if string != "":
                string += ":"
            string += r"%s=%s" % (pr, str(value))
    if string != "":
        string = "[&&NHX:" + string + "]"

    return string
