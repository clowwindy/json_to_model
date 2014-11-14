#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os.path
import inflector
from json_to_model.parser import NodeType
from jinja2 import Environment, PackageLoader

type_map = {
    NodeType.TYPE_ARRAY: 'Array',
    NodeType.TYPE_BOOL: 'Bool',
    NodeType.TYPE_INT: 'Int',
    NodeType.TYPE_FLOAT: 'Double',
    NodeType.TYPE_STRING: 'String?',
}

defaults_map = {
    NodeType.TYPE_ARRAY: '[]',
    NodeType.TYPE_BOOL: 'false',
    NodeType.TYPE_INT: '0',
    NodeType.TYPE_FLOAT: '0.0',
    NodeType.TYPE_STRING: 'nil',
}

english = inflector.English()

name_table = {
    'id': 'ID',
    'description': 'descriptionData'
}


def get_property_type(context, node):
    result = type_map.get(node.type, None)
    if result is None:
        return '%s' % english.classify(node.class_name)
    if result == 'Array':
        return '%s<%s>' % (result,
                           get_type_of_first_obj_in_array(context, node))
    return result


def get_property_default_value(context, node):
    result = defaults_map.get(node.type, None)
    if result is None:
        return 'nil'
    return result


def get_property_name(context, node):
    name = english.variablize(node.name)
    if name in name_table:
        return name_table[name]
    return name


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
    env = Environment(loader=PackageLoader('json_to_model.generators',
                                           'templates'))
    source_template = env.get_template('swift.swift')
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
                'default_value': get_property_default_value(context, node),
                'original_name': node.name,
                'children_type': get_type_of_first_obj_in_array(context, node)
            })
            if node.class_name:
                includes.add(get_property_type(context, node))
            if node.children:
                if node.children[0].class_name:
                    includes.add(get_property_type(context, node.children[0]))

        super_name = english.classify(clazz.super_class.class_name)\
            if clazz.super_class else 'NSObject'
        if super_name != 'NSObject':
            includes.add(super_name)

        with open(os.path.join(pathname, '%s.swift' % class_name), 'wb') as f:
            f.write(source_template.render(time=time.ctime(),
                                           class_name=class_name,
                                           super_name=super_name,
                                           properties=properties))
