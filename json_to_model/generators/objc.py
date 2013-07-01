#!/usr/bin/python
# -*- coding: utf-8 -*-

import inflector
from json_to_model.parser import NodeType
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
        return '%s *' % english.classify(node.super_class.class_name)
    return result


def gen_code(pathname, context):
    header_content = []
    source_content = []
    env = Environment(loader=PackageLoader('generators', 'templates'))
    header_template = env.get_template('header.h')
    for class_name, clazz in context.classes.iteritems():
        original_name = class_name
        class_name = english.classify(original_name)
        properties = []
        for attribute in clazz.children:
            properties.append({
                'class_name': get_property_type(context, attribute),
                'name': english.variablize(attribute.name),
                'retain_type': retain_map[attribute.type],
            })

        super_name = english.classify(clazz.super_class.class_name) if clazz.super_class else 'NSObject'
        print header_template.render(class_name=class_name, super_name=super_name, properties=properties)
