#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import glob


class Context(object):
    def __init__(self):
        self.classes = {}

    def add_node(self, node):
        if node.class_name:
            self.classes[node.class_name] = node

    def build_inheritance(self):
        for k, v in self.classes.iteritems():
            if v.super_class_name:
                v.super_class = self.classes[v.super_class_name]


class NodeType(object):
    TYPE_STRING = 'string'
    TYPE_INT = 'int'
    TYPE_FLOAT = 'float'
    TYPE_OBJECT = 'object'
    TYPE_ARRAY = 'array'
    TYPE_BOOL = 'bool'
    TYPE_NULL = 'null'  # This should not be used


class TreeNode(object):
    def __init__(self):
        self.children = []
        self.name = None
        self.type = None
        self.class_name = None
        self.super_class = None
        self.super_class_name = None

    def __str__(self):
        return '%s %s' % (self.name, self.type)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.type)

    def __repr__(self):
        return u'<TreeNode %s %s>' % (self.name, self.type)

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type


def parse_node(json_node, parent_node, context):
    if isinstance(json_node, list):
        parent_node.type = NodeType.TYPE_ARRAY
        for v in json_node:
            child = TreeNode()
            parse_node(v, child, context)
            parent_node.children.append(child)
            context.add_node(child)
    elif isinstance(json_node, dict):
        parent_node.type = NodeType.TYPE_OBJECT
        for k, v in json_node.iteritems():
            if k.startswith('__'):
                if k == '__class__':
                    parent_node.class_name = v
                elif k == '__super__':
                    parent_node.super_class_name = v
                continue
            child = TreeNode()
            child.name = k
            parse_node(v, child, context)
            parent_node.children.append(child)
            context.add_node(child)
    elif isinstance(json_node, bool):
        parent_node.type = NodeType.TYPE_BOOL
    elif isinstance(json_node, str):
        parent_node.type = NodeType.TYPE_STRING
    elif isinstance(json_node, unicode):
        parent_node.type = NodeType.TYPE_STRING
    elif isinstance(json_node, int):
        parent_node.type = NodeType.TYPE_INT
    elif isinstance(json_node, float):
        parent_node.type = NodeType.TYPE_FLOAT
    elif isinstance(json_node, None):
        parent_node.type = NodeType.TYPE_NULL


def get_generator(name):
    if name == 'objc':
        from json_to_model.generators import objc
        return objc
    return None
