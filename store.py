#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@TIME        :  2021/10/13
@Author      :  YQZ
@Version     :  1.0
@Desc        :  Sqlite帮助类
"""
import sqlite3

from config import SQLITE_DB


class MyStore:
    def __init__(self):
        self.__db = SQLITE_DB
        self.__con = sqlite3.connect(self.__db)

    def create_sub_tree(self, cid, cname):
        data = [{'id': cid, 'name': cname}]
        cur = self.__con.cursor()
        sql = """
            select chapter_id,chapter_name from kg_course_data where p_chapter_id='%s'
        """ % cid
        cur.execute(sql)
        chs = cur.fetchall()
        for c in chs:
            sub_data = self.create_sub_tree(c[0], c[1])
            data.append(sub_data)
        return data

    def get_chapter_tree(self, course):
        """
        获取章节树， 以list返回
            [root, [sub tree], [sub tree], ...]
            每个节点: {“id":"chapter id", "name":"chapter name"}
        """
        data = [{'id': course, 'name': course}]
        cur = self.__con.cursor()
        sql = """
            SELECT chapter_id,chapter_name FROM kg_course_data where p_chapter_id='0' and course='%s'
        """ % course
        cur.execute(sql)
        chs = cur.fetchall()
        for c in chs:
            sub_data = self.create_sub_tree(c[0], c[1])
            data.append(sub_data)
        return data

    def get_chapter_rel_kp(self, course):
        """
        获取章节与知识点的关系
            [(chapter, kp),...]
        """
        data = []
        cur = self.__con.cursor()
        sql = """
                    SELECT chapter_id,chapter_name,kp_id,kp_name FROM kg_chapter_kp_data where course='%s'
        """ % course
        cur.execute(sql)
        chs = cur.fetchall()
        for c in chs:
            data.append(({"id": c[0], "name": c[1]}, {"id": c[2], "name": c[3]}))
        return data

    def get_kp_rel_kp(self, course):
        """
        获取知识点与知识点的关系
            [(kp, pre_kp),....]
        """
        data = []
        cur = self.__con.cursor()
        sql = """
                            SELECT kp_id,kp_name,p_kp_id,p_kp_name FROM kg_kp_kp_data where course='%s'
                """ % course
        cur.execute(sql)
        chs = cur.fetchall()
        for c in chs:
            data.append(({"id": c[0], "name": c[1]}, {"id": c[2], "name": c[3]}))
        return data


if __name__ == '__main__':
    data = MyStore().get_chapter_tree('初中数学七年级上册')
    # print(data)
    data = MyStore().get_chapter_rel_kp('初中数学七年级上册')
    print(data)
    data = MyStore().get_kp_rel_kp('初中数学七年级上册')
    # print(data)
