#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os.path
import inflector
from json_to_model.parser import NodeType, TreeNode
from jinja2 import Environment, PackageLoader

type_map = {
    NodeType.TYPE_ARRAY: 'NSArray *',
    NodeType.TYPE_BOOL: 'BOOL',
    NodeType.TYPE_INT: 'NSInteger',
    NodeType.TYPE_FLOAT: 'CGFloat',
    NodeType.TYPE_STRING: 'NSString *',
}

retain_map = {
    NodeType.TYPE_OBJECT: 'strong',
    NodeType.TYPE_ARRAY: 'strong',
    NodeType.TYPE_BOOL: 'assign',
    NodeType.TYPE_INT: 'assign',
    NodeType.TYPE_FLOAT: 'assign',
    NodeType.TYPE_STRING: 'copy',
}

english = inflector.English()


def get_property_type(context, node):
    result = type_map.get(node.type, None)
    if result is None:
        return '%s *' % english.classify(node.class_name)
    return result


def get_property_name(context, node):
    name = english.variablize(node.name)
    if name != 'id':
        return name
    else:
        return 'ID'


def get_type_of_first_obj_in_array(context, node):
    if node.type == NodeType.TYPE_ARRAY:
        if len(node.children) > 0:
            return get_property_type(context, node.children[0])
    return None


def property_is_inherited(context, node, property):
    c = node.super_class
    found = False
    while c is not None:
        found = property in c.children
        c = c.super_class
    return found


def gen_code(pathname, context):
    env = Environment(loader=PackageLoader('json_to_model.generators', 'templates'))
    header_template = env.get_template('header.h')
    source_template = env.get_template('source.m')
    for class_name, clazz in context.classes.iteritems():
        original_name = class_name
        class_name = english.classify(original_name)
        properties = []
        includes = set()
        for node in clazz.children:
            if property_is_inherited(context, clazz, node):
                continue
            properties.append({
                'type': get_property_type(context, node),
                'name': get_property_name(context, node),
                'original_name': node.name,
                'retain_type': retain_map[node.type],
                'children_type': get_type_of_first_obj_in_array(context, node)
            })
            if node.class_name:
                includes.add(get_property_type(context, node))
            if node.children:
                if node.children[0].class_name:
                    includes.add(get_property_type(context, node.children[0]))

        super_name = english.classify(clazz.super_class.class_name) if clazz.super_class else 'NSObject'
        if super_name != 'NSObject':
            includes.add(super_name)

        with open(os.path.join(pathname, '%s.h' % class_name), 'wb') as f:
            f.write(header_template.render(time=time.ctime(), class_name=class_name, super_name=super_name, properties=properties, includes=includes))
        with open(os.path.join(pathname, '%s.m' % class_name), 'wb') as f:
            f.write(source_template.render(time=time.ctime(), class_name=class_name, super_name=super_name, properties=properties))
