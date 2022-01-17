#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@TIME        :  2021/10/13
@Author      :  YQZ
@Version     :  1.0
@Desc        :  
"""

from graph import MyGraph
from store import MyStore


class KGBuilder:
    def __init__(self):
        self.graph = MyGraph()
        self.db = MyStore()

    def create_kg(self, course):
        tree = self.db.get_chapter_tree(course)
        self.graph.create_course(tree[0]["id"], tree[0]["name"])
        for i in range(1, len(tree)):
            self.__create_chapter_graph(tree[i])
            self.graph.create_course_rel_chapter(tree[0]["id"], tree[i][0]["id"])
        self.__create_chapter_kp(course)
        self.__create_kp_rel(course)

    def __create_chapter_graph(self, tree):
        self.graph.create_chapter(tree[0]["id"], tree[0]["name"])
        for i in range(1, len(tree)):
            self.__create_chapter_graph(tree[i])
            self.graph.create_chapter_rel_chapter(tree[0]["id"], tree[i][0]["id"])

    def __create_chapter_kp(self, course):
        data = self.db.get_chapter_rel_kp(course)
        for item in data:
            if item[1]["id"] is not None and item[1]["name"] is not None:
                self.graph.create_kp(item[1]["id"], item[1]["name"])
                self.graph.create_chapter_rel_kp(item[0]["id"], item[1]["id"])

    def __create_kp_rel(self, course):
        data = self.db.get_kp_rel_kp(course)
        for item in data:
            self.graph.create_kp_rel_kp(item[0]["id"], item[0]["name"], item[1]["id"], item[1]["name"])


if __name__ == '__main__':
    KGBuilder().create_kg("初中数学七年级上册")
