#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@TIME        :  2021/10/13
@Author      :  YQZ
@Version     :  1.0
@Desc        :  Neo4j图数据库帮助类
                课程节点： label: course   attributes: id, name， subject, grade, term(学期)
                章节节点： label: chapter    attribute: id, name
                知识点: label: kp  attribute: id, name
                关系：  part (子集),  include (包含),  after 在(知识点)之后
"""
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import config

LABEL_COURSE = "课程"
LABEL_CHAPTER = "章节"
LABEL_KP = "知识点"
REL_PART = "部分"
REL_INCLUDE = "包含"
REL_AFTER = "前导"


class MyGraph:
    def __init__(self):
        self.__graph = Graph("bolt://{0}:{1}".format(config.NEO4J_HOST, config.NEO4J_PORT),
                             auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))

    def create_node(self, p_label, p_attrs):
        """
        创建节点
        """
        q_str = "_.id='" + p_attrs['id'] + "'"
        matcher = NodeMatcher(self.__graph)
        if matcher.match(p_label).where(q_str).first() is None:
            node = Node(p_label, **p_attrs)
            return self.__graph.create(node)
        return None

    def match_node(self, p_label, p_attrs):
        """
        匹配
        """
        q_str = "_.id='" + p_attrs['id'] + "'"
        return NodeMatcher(self.__graph).match(p_label).where(q_str).first()

    def create_relationship(self, p_label1, p_attrs1, p_label2, p_attrs2, p_rel_name):
        """
        创建关系
        """
        node1 = self.match_node(p_label1, p_attrs1)
        node2 = self.match_node(p_label2, p_attrs2)
        if node1 is None or node2 is None:
            return False
        return self.__graph.create(Relationship(node1, p_rel_name, node2))

    def create_course(self, course_id, course_name):
        attrs = {"id": course_id, "name": course_name}
        return self.create_node(LABEL_COURSE, attrs)

    def create_chapter(self, chapter_id, chapter_name):
        attrs = {"id": chapter_id, "name": chapter_name}
        return self.create_node(LABEL_CHAPTER, attrs)

    def create_kp(self, kp_id, kp_name):
        attrs = {"id": kp_id, "name": kp_name}
        return self.create_node(LABEL_KP, attrs)

    def create_course_rel_chapter(self, course, chapter_id):
        node_course = self.match_node(LABEL_COURSE, {"id": course})
        node_chapter = self.match_node(LABEL_CHAPTER, {"id": chapter_id})
        if node_course is None or node_chapter is None:
            return False
        return self.__graph.create(Relationship(node_course, REL_PART, node_chapter))

    def create_chapter_rel_chapter(self, cid1, cid2):
        node1 = self.match_node(LABEL_CHAPTER, {"id": cid1})
        node2 = self.match_node(LABEL_CHAPTER, {"id": cid2})
        if node1 is None or node2 is None:
            return False
        return self.__graph.create(Relationship(node1, REL_PART, node2))

    def create_chapter_rel_kp(self, chapter_id, kp_id):
        node_chapter = self.match_node(LABEL_CHAPTER, {"id": chapter_id})
        node_kp = self.match_node(LABEL_KP, {"id": kp_id})
        if node_chapter is None or node_kp is None:
            return False
        return self.__graph.create(Relationship(node_chapter, REL_INCLUDE, node_kp))

    def create_kp_rel_kp(self, kp1, kpname1, kp2, kpname2):
        node1 = self.match_node(LABEL_KP, {"id": kp1})
        node2 = self.match_node(LABEL_KP, {"id": kp2})
        if node1 is None:
            self.create_kp(kp1, kpname1)
            node1 = self.match_node(LABEL_KP, {"id": kp1})
        if node2 is None:
            self.create_kp(kp2, kpname2)
            node2 = self.match_node(LABEL_KP, {"id": kp2})
        return self.__graph.create(Relationship(node1, REL_AFTER, node2))
