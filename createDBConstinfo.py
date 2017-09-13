#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-9-13 11:18
# @Author  : Alan
# @Site    : 
# @File    : createDBConstinfo.py
# @Software: PyCharm Community Edition

import psycopg2.extras

# 数据库连接参数
# conn = psycopg2.connect(database="test", user="postgres", password="longrise", host="localhost", port="5434")
conn = psycopg2.connect(database="ACC_DEV", user="postgres", password="longrise", host="192.168.7.212", port="54320")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute("select * from pg_tables where schemaname='public';")
tables = cur.fetchall()  # 数据库中所有表
print(tables)
with open('DBconstinfo.java', 'w', encoding='utf8') as f:
    f.write('public class DBconstinfo{\n')
    for table in tables:
        tableName = table['tablename']
        cur.execute("SELECT * FROM pg_description WHERE objoid=\'"+tableName+"\'::regclass AND objsubid = \'0\';")
        descs = cur.fetchall()
        if descs:
            tableDesc = descs[0]['description']
            f.write('/*************************' + tableDesc + ' start************************************/\n')
            f.write('    /**' + tableDesc + '*/\n')
        else:
            f.write('/*************************' + tableName + '表 start************************************/\n')
            f.write('    /**' + tableName + '表*/\n')
        f.write('    public static final String TABLE_' + tableName.upper() + '=\"' + tableName + '\";\n')
        cur.execute("SELECT col.column_name,des.description "
                    + "FROM information_schema.columns col LEFT JOIN pg_description des "
                    + " ON col.table_name::regclass = des.objoid "
                    + "AND col.ordinal_position = des.objsubid "
                    + "WHERE table_name=\'" + tableName + "\' "
                    + "ORDER BY ordinal_position;"
                    )
        # cur.execute("select * from information_schema.columns where table_name = '" + tablename + "';")
        columns = cur.fetchall()  # 表中所有字段
        print(columns)
        for column in columns:
            columnName = column['column_name']
            columnDesc = column['description']
            if columnDesc is None:
                f.write('    /**' + columnName + '*/\n')
            else:
                f.write('    /**' + columnDesc + '*/\n')
            f.write('    public static final String ' + tableName.upper() + '_' + columnName.upper() + '=\"'
                    + columnName + '\";\n')
        f.write('/***************************** end************************************/\n\n')
    f.write('}')
