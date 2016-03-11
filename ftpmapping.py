#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
ftpmapping.py - The-awesome-ftpmapping-script
"""
import os
import optparse
import ftplib

LOCATION_NONE     = 'NONE'
LOCATION_MID      = 'MID'
LOCATION_MID_GAP  = 'MID_GAP'
LOCATION_TAIL     = 'TAIL'
LOCATION_TAIL_GAP = 'TAIL_GAP'
 
Notations = {
    LOCATION_NONE: '',
    LOCATION_MID: '├─',
    LOCATION_MID_GAP: '│  ',
    LOCATION_TAIL: '└─',
    LOCATION_TAIL_GAP: '    '
}
 
class Line(object):
    def __init__(self, name, size, is_dir):
        self.name = name
        self.size = size
        self.is_dir = is_dir


 
class Node(object):
    def __init__(self, name, depth, parent=None, location=LOCATION_NONE):
        self.name = name
        self.depth = depth
        self.parent = parent
        self.location = location
        self.children = []
 
    def __str__(self):
        sections = [self.name.decode('gbk').encode('utf-8')]
        parent = self.has_parent()
        if parent:
            if self.is_tail():
                sections.insert(0, Notations[LOCATION_TAIL])
            else:
                sections.insert(0, Notations[LOCATION_MID])
            self.__insert_gaps(self, sections)
        return ''.join(sections)
 
    def __insert_gaps(self, node, sections):
        parent = node.has_parent()
        # parent exists and parent's parent is not the root node
        if parent and parent.has_parent():
            if parent.is_tail():
                sections.insert(0, Notations[LOCATION_TAIL_GAP])
            else:
                sections.insert(0, Notations[LOCATION_MID_GAP])
            self.__insert_gaps(parent, sections)
 
    def has_parent(self):
        return self.parent
 
    def has_children(self):
        return self.children
 
    def add_child(self, node):
        self.children.append(node)
 
    def is_tail(self):
        return self.location == LOCATION_TAIL
 
 

class Tree(object):
    def __init__(self, treetype):
        self.nodes = []
        self.treetype = treetype
 
    def debug_print(self):
        for node in self.nodes:
            print(str(node) + '/')
    def write2file(self, filename):
        try:
            with open(filename, 'w') as fp:
                fp.writelines(str(node) + '/\n'
                              for node in self.nodes)
        except IOError as e:
            print(e)
            return False
        return True
    
    def resolve_lines(self, line):
        seprate = line.split()
        resolved_name = [ value for key,value in enumerate(seprate) if key >7]
        name = ''
        for key,value in enumerate(resolved_name):
            name = name + ' ' + value
        name = name.strip().decode('gbk').encode('gbk')
        if name == '.' or name == '..':
            pass
        else:
            size = seprate[-5].decode('gbk')
            proper = seprate[0].decode('gbk')
            is_dir = True if proper.upper().startswith('D') else False
            line = Line(name, size, is_dir)
            self.entries.append(line)
    
    def build(self, path):
        self.__build(path, 0, None, LOCATION_NONE)
 
    def __build(self, path, depth, parent, location):
        name = os.path.basename(path)

        node = Node(name, depth, parent, location)

        self.add_node(node)
        if parent:
            parent.add_child(node)
        
        self.entries = []
        
        try:
            _ftp_ctx.connection.retrlines('LIST', callback = self.resolve_lines)
        except:
            _ftp_ctx.init()
            _ftp_ctx.connection.retrlines('LIST', callback = self.resolve_lines)
        
        
        end_index = len(self.entries) - 1
        
        # keey dir entry ahead for generating order of nodes of the tree
        def dir_bubble(x,y):
            if(x.is_dir):
                return -1
            else:
                return 1
        self.entries = sorted(self.entries, dir_bubble)
    

        for i, entry in enumerate(self.entries):
            if entry.is_dir is True:
                childpath = os.path.join(path, entry.name)
                # print chardet.detect(childpath)
                try:
                    _ftp_ctx.connection.cwd(childpath)
                except:
                    try:
                        _ftp_ctx.init()
                        _ftp_ctx.connection.cwd(childpath)
                    except:
                        with open('error.log', 'a') as f:
                            f.write(childpath+"\n")
                        # continue the process
                        return

                location = LOCATION_TAIL if i == end_index else LOCATION_MID
                self.__build(childpath, depth + 1, node, location)
            elif self.treetype == 'file':
                location = LOCATION_TAIL if i == end_index else LOCATION_MID
                # indicate the current node(dic) as parent
                file_node = Node(entry.name, depth, node, location)
                self.add_node(file_node)
            
 
    def add_node(self, node):
        self.nodes.append(node)
 
 
def _parse_args():
    parser = optparse.OptionParser()
    parser.add_option(
        '--path', dest='path', action='store', type='string',
        default='/', help='the path used to generate the tree [default: %default]')
    parser.add_option(
        '-o', '--out', dest='file', action='store', type='string',
        help='specify a filename or file to store the generated tree [default: pathname.trees]')
    parser.add_option(
        '-u', '--username', dest='username', action='store', type='string',
        default='anonymous', help='the username used to connect to the ftp server [default: anonymous]')
    parser.add_option(
        '-p', '--password', dest='password', action='store', type='string',
        default='anonymous', help='the password used to connect to the ftp server [default: anonymous]')
    parser.add_option(
        '-s', '--server', dest='server', action='store', type='string',
    help='the ftp server address')
    parser.add_option(
        '-t', '--type', dest='treetype', action='store', type='string',
        default='folder', help='tree type, leave it default for folder-only.It map and generate the tree contained files when passing \'file\'. [default: folder]')

    options, args = parser.parse_args()
    # positional arguments are ignored
    return options
 
class _FTPCtx():
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.connection = ftplib.FTP(self.server, self.username, self.password)
    def init(self):
        self.connection = ftplib.FTP(self.server, self.username, self.password)
        
        
 
def main():
    options = _parse_args()
    path = options.path
    username = options.username
    password = options.password
    server = options.server
    treetype = options.treetype
    # keep ftp context
    global _ftp_ctx
    _ftp_ctx = _FTPCtx(server, username, password)
    tree = Tree(treetype)
    tree.build(path)
    tree.debug_print()
    if options.file:
        filename = options.file
    else:
        name = server
        filename = '%s.tree' % name
    result = tree.write2file(filename)
    print('write tree to file `%s` %s' % (filename, 'successfully' if result else 'failed'))
    return 0 if result else 1
 
if __name__ == '__main__':
    import sys
    sys.exit(main())

