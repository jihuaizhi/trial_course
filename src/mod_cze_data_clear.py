#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# python 3.7.2
# @Time    : 2019/3/16
# @Author  : jihuaizhi
# @Desc    : CZE平台历史数据清理程序,依据数据库中的记录,清理课件,CTF,AWD,靶场的文本类文件,视频类文件


import mysql.connector
from mysql.connector import errorcode
import shutil
import sys
import os
import csv


def fun_copy_data():
    try:
        """数据库连接信息"""
        mydb = mysql.connector.connect(
            host="10.0.0.2",  # 数据库主机地址
            port="3306",
            user="root",  # 数据库用户名
            passwd="root",  # 数据库密码
            database="fusion_platform"
        )
        # 打开数据库,以字典格式返回
        mycursor = mydb.cursor(dictionary=True)
        # 执行查询
        # storage_path="/storage/Uploads/TRIAL/"
        # new_storage_path="/storage_new/Uploads/TRIAL/"
        storage_path = sys.path[0] + "/old_path/"
        new_storage_path = sys.path[0] + "/new_path/"

        mycursor.execute("select uuid,course_name from trial_course")
        myresult = mycursor.fetchall()
        if os.path.exists('copy_log.csv'):
            os.remove('copy_log.csv')
        with open('copy_log.csv', 'a', encoding='utf-8', newline='') as csvfile:
            write_csv = csv.writer(csvfile)
            for row in myresult:
                old_dir = storage_path + row['uuid']
                new_dir = new_storage_path + row['uuid']
                # print("原文件夹:", old_dir)
                # print("新文件夹:", new_dir)
                if os.path.exists(new_dir):
                    print("目标文件夹已经存在数据! ", new_dir, row['uuid'])
                    write_csv.writerow(["ERR:目标文件夹已经存在数据!跳过复制! ", new_dir, row['uuid']])
                    continue
                if not os.path.exists(old_dir):
                    # 课件原附件文件夹不存在
                    print("源文件夹不存在! ", old_dir, row['uuid'])
                    write_csv.writerow(["ERR:源文件夹不存在!未能复制! ", old_dir, row['uuid']])
                    continue
                    # 输出错误信息到文件
                print(["复制文件夹! ", old_dir, row['uuid']])
                write_csv.writerow(["复制文件夹! ", old_dir, row['uuid']])
                shutil.copytree(old_dir, new_dir)



    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        mydb.close()



def fun_check_data():
    try:
        """数据库连接信息"""
        mydb = mysql.connector.connect(
            host="10.0.0.2",  # 数据库主机地址
            port="3306",
            user="root",  # 数据库用户名
            passwd="root",  # 数据库密码
            database="fusion_platform"
        )
        # 打开数据库,以字典格式返回
        mycursor = mydb.cursor(dictionary=True)
        # 执行查询
        mycursor.execute("select uuid,course_name from trial_course")
        myresult = mycursor.fetchall()

        if os.path.exists('check_log.csv'):
            os.remove('check_log.csv')
        with open('check_log.csv', 'a', encoding='utf-8', newline='') as csvfile:
            write_csv = csv.writer(csvfile)
            write_csv.writerow(["课件UUID", "课件名称", "视频数量", "视频文件数量",
                                "文档数量", "文档文件数量", "附件数量", "附件文件数量", "拓扑数据", "虚拟机"])
            for row_course in myresult:
                row_data=[]
                row_data.append(row_course['uuid'])
                row_data.append(row_course['course_name'])

                #校验视频数据
                print('课件UUID:', row_course['uuid'], '课件名称', row_course['course_name'])
                mycursor.execute(
                    "select uuid,video_name,video_path "
                    "from trial_video where course_uuid='" + row_course['uuid'] + "'")
                rst = mycursor.fetchall()
                row_data.append(len(rst))
                if len(rst) > 0:
                    video_count=0
                    for row_video in rst:
                        if os.path.exists(row_video['video_path']):
                            video_count+=1
                    row_data.append(video_count)
                else:
                    row_data.append(0)



                write_csv.writerow(row_data)






    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        mydb.close()


# 启动调试方法
if __name__ == '__main__':
    # fun_copy_data()
    fun_check_data()
