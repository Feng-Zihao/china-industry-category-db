
# -*- coding: utf-8 -*-

import csv
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#li = map(lambda x: x.decode('utf-8'), row)
#for l in li:
#    print l
"""
{code: code,
 name: ' ',
 children: {

 
}
"""
class CategoryNode(object):
    def __init__(self, code, name):
        self.code = code
        self.name = name.strip()
        self.children = {}  # <code: category>
    
    def appendChild(self, child):
        self.children[child.code] = child
        child.parent = self

    def __repr__(self):
        return '<%s, %s>' % (self.code, self.name.decode('utf-8'))


def detectLevel(row):
    for i in range(5):
        if row[i].encode('hex') != 'e38080':
            return i

root_category = CategoryNode('root', 'root')
current_level = -1


node = root_category
with open('n10191379.csv') as f:
    r = csv.reader(f, delimiter=',')
    for row in r:
        if len(row) != 5:
            print 'error in the file'
            sys.exit(-1)
        level = detectLevel(row)
        child = CategoryNode(code=row[level], name=row[4])
        if level > 3:
            print 'bug'
            sys.exit(-1)
        if level < current_level:
            while (current_level >= level):
                node = node.parent
                current_level -= 1
            #print '<', current_level
        if level > current_level:
            node.appendChild(child)
            node = child
            current_level += 1
            #print '>', current_level
        elif level == current_level:
            node.appendChild(child)
            #print '==', current_level



def printCategoryTree(node, level=-1):
    if level != -1:
        row = [' '] * 5
        row[level] = node.code
        row[4] = node.name
        print ','.join(row)
    for key in node.children:
        printCategoryTree(node.children[key], level+1)
        #print node.children[key].name


#printCategoryTree(root_category)


print """
/* The following part is generated by a program.
 * DON'T modify that except for the indent format.
 */

function getIndustryCategoryDict() {
    return \
""",

def generateJavascript(node):
    print '{',
    for key in node.children:
        child = node.children[key]
        print "'%s': {'code': '%s', 'name': '%s', 'children': " % \
              (key, child.code, child.name),
        generateJavascript(child)
    print '}',

generateJavascript(root_category)


print """
}

/** This is the end of the generated part */
"""
