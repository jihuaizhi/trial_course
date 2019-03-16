#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/20
# @Author  : jihuaizhi
"""
说明 ：

"""

import tkinter as tk
import json
import sqlite3
import os


def get_kjfx():
    """
    查询课件方向
    :return:
    """
    conn = sqlite3.connect(SQLITE3_DB)
    cursor = conn.cursor()
    cursor.execute(
        "select uuid,dict_data_name from sys_dict_data "
        "where dict_uuid='" + DICT_UUID + "' and parent_uuid=''")
    result_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return result_list


def get_kjfl(kjfx_uuid):
    """
    根据课件方向查询课件分类
    :param kjfx_uuid:
    :return:
    """
    conn = sqlite3.connect(SQLITE3_DB)
    cursor = conn.cursor()
    cursor.execute("select uuid,dict_data_name from sys_dict_data where parent_uuid='" + kjfx_uuid + "'")
    result_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return result_list


def create_course_form():
    """
    创建JSON表单UI界面初始化
    :return:
    """
    window = tk.Tk()
    # 设置窗口标题
    window.title("CZE-课件制作工具")
    # 设置窗口大小和左上角坐标位置
    window.geometry("600x500+200+200")

    # lab1 = tk.Label(window, text='OMG! this is TK!',  # 标签的文字
    #                 bg='green', font=('Arial', 12), width=15, height=2)  # 标签长宽
    lab1 = tk.Label(window, text='课件名称')
    lab1.grid(row=0, column=0)
    lab2 = tk.Label(window, text='课件类型')
    lab2.grid(row=1, column=0)
    lab3 = tk.Label(window, text='课件类别')
    lab3.grid(row=2, column=0)
    lab4 = tk.Label(window, text='课件难度')
    lab4.grid(row=3, column=0)
    lab5 = tk.Label(window, text='课件描述')
    lab5.grid(row=4, column=0)
    lab6 = tk.Label(window, text='课件方向')
    lab6.grid(row=5, column=0)
    lab7 = tk.Label(window, text='课件分类')
    lab7.grid(row=6, column=0)
    lab8 = tk.Label(window, text='课时数')
    lab8.grid(row=7, column=0)

    # 课件名称
    ent_kjmc = tk.Entry(window, show=None)
    ent_kjmc.grid(row=0, column=1)

    # 课件类型
    ent_kjlx = tk.Listbox(window, height=len(LIST_KJLX), exportselection=0)
    ent_kjlx.grid(row=1, column=1)
    for item in LIST_KJLX:
        ent_kjlx.insert('end', item[1])

    # 课件类别
    ent_kjlb = tk.Listbox(window, height=len(LIST_KJLB), exportselection=0)
    ent_kjlb.grid(row=2, column=1)
    for item in LIST_KJLB:
        ent_kjlb.insert('end', item[1])

    # 课件难度
    ent_kjnd = tk.Listbox(window, height=len(LIST_KJND), exportselection=0)
    ent_kjnd.grid(row=3, column=1)
    for item in LIST_KJND:
        ent_kjnd.insert('end', item[1])

    # 课件描述
    ent_kjms = tk.Text(window, show=None, height=3, width=30)
    ent_kjms.grid(row=4, column=1)

    # 课件方向
    ent_kjfx = tk.Listbox(window, height=4, exportselection=0)
    ent_kjfx.grid(row=5, column=1)
    for item in LIST_KJFX:
        ent_kjfx.insert('end', item[1])
    scr1 = tk.Scrollbar(window)
    ent_kjfx.configure(yscrollcommand=scr1.set)
    scr1['command'] = ent_kjfx.yview
    scr1.grid(row=5, column=2)

    # 课件分类
    ent_kjfl = tk.Listbox(window, height=4, exportselection=0)
    ent_kjfl.grid(row=6, column=1)
    # for item in LIST_KJFL:
    #     ent_kjfl.insert('end', item)
    scr2 = tk.Scrollbar(window)
    ent_kjfl.configure(yscrollcommand=scr1.set)
    scr2['command'] = ent_kjfl.yview
    scr2.grid(row=6, column=2)
    ent_kjfx.bind('<<ListboxSelect>>', func=handler_adaptor(fun_click_direction, conl=ent_kjfl))

    # 课时数
    ent_kjks = tk.Entry(window, show=None)
    ent_kjks.grid(row=7, column=1)

    ctl_lst = {}
    ctl_lst.update({'course_name': ent_kjmc})
    ctl_lst.update({'course_type': ent_kjlx})
    ctl_lst.update({'course_style': ent_kjlb})
    ctl_lst.update({'course_difficulty': ent_kjnd})
    ctl_lst.update({'course_description': ent_kjms})
    ctl_lst.update({'course_direction': ent_kjfx})
    ctl_lst.update({'course_direction_type': ent_kjfl})
    ctl_lst.update({'course_period': ent_kjks})

    btn_cerat = tk.Button(window, text='生成JSON', command=(lambda: fun_tk_submit(ctl_lst)))
    btn_cerat.grid(row=10, column=0, ipadx=10, padx=8, pady=2)
    btn_check = tk.Button(window, text='JSON文件校验', command=(lambda: fun_data_check()))
    btn_check.grid(row=10, column=1, ipadx=10, padx=8, pady=2)
    btn_close = tk.Button(window, text='关闭', command=(lambda: fun_close()))
    btn_close.grid(row=10, column=2, ipadx=10, padx=8, pady=2)

    window.mainloop()



def handler_adaptor(fun, **kwds):
    """
    事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧
    :param fun:
    :param kwds:
    :return:
    """
    return lambda event, fun1=fun, kwds1=kwds: fun(event, **kwds)


def fun_click_direction(event, conl):
    """
    方向下拉框级联选择事件
    :param event:
    :param conl:
    :return:
    """
    w = event.widget
    direction_uuid = LIST_KJFX[w.curselection()[0]][0]
    global LIST_KJFL
    LIST_KJFL = get_kjfl(direction_uuid)
    conl.delete(0, 'end')
    for item in LIST_KJFL:
        conl.insert('end', item[1])


def fun_close():
    """关闭窗口,退出程序"""
    exit("GoodBye!!!")  # 抛出SystemExit异常. 一般在交互式shell中退出时使用


def fun_tk_submit(ctl_lst):
    """
    校验数据合法性
    :param ctl_lst: 表单输入数据
    :return: 输出JSON文件
    """
    # 输入校验检查结果
    check_flag = True

    # 校验课件名称
    course_name = ctl_lst['course_name'].get()

    if len(course_name) == 0:
        print("数据错误：课件名称不能为空")
        check_flag = False

    if len(course_name) > 50:
        print("数据错误：课件名称长度超50")
        check_flag = False

    # 校验课件类型
    course_type = ''
    if len(ctl_lst['course_type'].curselection()) == 0:
        print("数据错误：课件类型不能为空")
        check_flag = False
    else:
        course_type = LIST_KJLX[ctl_lst['course_type'].curselection()[0]][0]

    # 校验课件类别
    course_style = ''
    if len(ctl_lst['course_style'].curselection()) == 0:
        print("数据错误：课件类别不能为空")
        check_flag = False
    else:
        course_style = LIST_KJLB[ctl_lst['course_style'].curselection()[0]][0]

    # 校验课件难度
    course_difficulty = ''
    if len(ctl_lst['course_difficulty'].curselection()) == 0:
        print("数据错误：课件难度不能为空")
        check_flag = False
    else:
        course_difficulty = LIST_KJND[ctl_lst['course_difficulty'].curselection()[0]][0]

    # 校验课件描述
    course_description = ctl_lst['course_description'].get(0.0, 'end')

    if len(course_description) == 0:
        print("数据错误：课件描述不能为空")
        check_flag = False

    if len(course_description) > 255:
        print("数据错误：课件描述长度超255")
        check_flag = False

    # 校验课件方向
    course_direction_uuid = ''
    if len(ctl_lst['course_direction'].curselection()) == 0:
        print("数据错误：课件方向不能为空")
        check_flag = False
    else:
        course_direction_uuid = LIST_KJFX[ctl_lst['course_direction'].curselection()[0]][0]

    # 校验课件分类
    course_direction_type_uuid = ''
    if len(ctl_lst['course_direction_type'].curselection()) == 0:
        print("数据错误：课件分类不能为空")
        check_flag = False
    else:
        course_direction_type_uuid = LIST_KJFL[ctl_lst['course_direction_type'].curselection()[0]][0]

    # 校验课件课时
    course_period = ctl_lst['course_period'].get()
    print(course_period.isdigit())

    if not course_period.isdigit():
        print("数据错误：课件课时必须为整数")
        check_flag = False

    if course_period.isdigit() and (int(course_period) > 100 or int(course_period) <= 0):
        print("数据错误：课件课时必须大于0 小于100小时")
        check_flag = False

    if not check_flag:
        print("数据校验：数据校验未通过，请修改数据重试!!!!!!!!!!!!")
        print('------------------------------------------------------------')
        # return

    print('数据校验通过，开始创建json文件！')
    print('------------------------------------------------------------')

    json_data = {}
    json_data.update({"uuid": ""})
    json_data.update({"course_built": 1})
    json_data.update({"course_name": course_name})
    json_data.update({"course_type": course_type})
    json_data.update({"course_style": course_style})
    json_data.update({"course_status": 1})
    json_data.update({"course_difficulty": course_difficulty})
    json_data.update({"course_description": course_description})
    json_data.update({"course_direction_uuid": course_direction_uuid})
    json_data.update({"course_direction_type_uuid": course_direction_type_uuid})
    json_data.update({"course_period": course_period})

    fun_creat_json(json_data)



def fun_creat_json(json_data):
    """
    将表单数据写入JSON文件
    :param json_data:
    :return:
    """

    json_string = json.dumps(json_data, ensure_ascii=False, indent=4)
    print(json_string)
    with open("data.json", "w", encoding="utf-8") as f:
        print(json_string, file=f)


def check_course_form():
    """
    数据校验表单
    :return:
    """
    window = tk.Tk()
    # 设置窗口标题
    window.title("CZE-课件数据检查工具")
    # 设置窗口大小和左上角坐标位置
    window.geometry("600x500+200+200")

    lab1 = tk.Label(window, text='校验信息', bg='white')
    lab1.grid(row=0, column=0, ipadx=200, ipady=50, padx=10, pady=10)

    btn_close = tk.Button(window, text='数据校验', command=(lambda: fun_data_check()))
    btn_close.grid(row=1, column=0, ipadx=100, padx=10, pady=10)

    window.mainloop()

    pass


def fun_data_check():
    """
    检查JSON文件数据格式
    :return:
    """
    # 判断JSON文件是否存在
    if not os.path.isfile("data3.json"):
        print("文件错误:JSON文件不存在")
        return

    # 校验json格式并读取JSON数据
    try:
        with open('data.json', 'r', encoding="utf-8") as f:
            course_data = json.load(f)
    except ValueError:
        print("json格式错误:json文件内容格式错误,请检查json格式是否正确")
        return

    if 'uuid' in course_data and 'course_built' in course_data \
            and 'course_name' in course_data \
            and 'course_type' in course_data \
            and 'course_style' in course_data \
            and 'course_status' in course_data \
            and 'course_difficulty' in course_data \
            and 'course_description' in course_data \
            and 'course_direction_uuid' in course_data \
            and 'course_direction_type_uuid' in course_data \
            and 'course_period' in course_data:
        pass
    else:
        print("文件定义错误：课件基本信息定义错误,请检查配置项")
        return

    if course_data['course_style'] == 1:
        if not ('doc_name' in course_data and 'doc_path' in course_data):
            print("文件定义错误：文件型课件信息定义错误,请检查配置项")
            return

    if course_data['course_style'] == 2:
        if not ('video_name' in course_data and 'video_path' in course_data):
            print("文件定义错误：视频型课件信息定义错误,请检查配置项")
            return

    if course_data['course_style'] == 3:
        if not ('exp_name' in course_data and 'exp_video_name' in course_data
                and 'exp_video_path' in course_data
                and 'exp_doc_name' in course_data
                and 'exp_doc_path' in course_data
                and 'exp_enclosure_name' in course_data
                and 'exp_enclosure_path' in course_data
                and 'exp_images' in course_data):
            print("文件定义错误：虚拟机型课件信息定义错误,请检查配置项")
            return
        for item in course_data['exp_images']:
            if 'image_file' not in item:
                print("文件定义错误：虚拟机信息定义错误,请检查配置项")
                return

    check_flag = True

    # 校验课件名称
    if len(course_data['course_name']) <= 0 or len(course_data['course_name']) > 50:
        print("数据错误：课件名称不能为空,长度超50")
        check_flag = False

    # 校验课件类型
    if course_data['course_type'] not in [item[0] for item in LIST_KJLX]:
        print("数据错误：课件类型错误")
        check_flag = False

    # 校验课件类别
    if course_data['course_style'] not in [item[0] for item in LIST_KJLB]:
        print("数据错误：课件类别错误")
        check_flag = False

    # 校验课件难度
    if course_data['course_difficulty'] not in [item[0] for item in LIST_KJND]:
        print("数据错误：课件难度错误")
        check_flag = False

    # 校验课件描述
    if len(course_data['course_description']) <= 0 or len(course_data['course_description']) > 255:
        print("数据错误：课件描述长度不能为空 小于255")
        check_flag = False

    # 校验课件方向
    if course_data['course_direction_uuid'] not in [item[0] for item in LIST_KJFX]:
        print("数据错误：课件方向错误")
        check_flag = False

    # 校验课件分类
    kjfl = get_kjfl(course_data['course_direction_uuid'])
    if course_data['course_direction_type_uuid'] not in [item[0] for item in kjfl]:
        print("数据错误：课件分类错误")
        check_flag = False

    # 校验课件课时
    course_period = course_data['course_period']
    if type(course_period) != int:
        print("数据错误：课件课时必须为整数")
        check_flag = False
    elif(course_period) > 100 or int(course_period) <= 0:
        print("数据错误：课件课时必须大于0 小于100小时")
        check_flag = False

    # 校验文件类课件
    if course_data['course_style'] == 1:
        if course_data['doc_name'] == '':
            print("数据错误：文件型课件文件名称不能为空")
            check_flag = False
        if not os.path.isfile(course_data['doc_path']):
            print("数据错误：文件型课件文件不存在")
            check_flag = False

    # 校验视频类课件
    if course_data['course_style'] == 2:
        if course_data['video_name'] == '':
            print("数据错误：视频型课件文件名称不能为空")
            check_flag = False

        if not os.path.isfile(course_data['video_path']):
            print("数据错误：视频型课件文件不存在")
            check_flag = False

    # 校验虚拟机类课件
    if course_data['course_style'] == 3:
        if not os.path.isfile(course_data['exp_video_path']):
            print("数据错误：实验视频文件不存在")
            check_flag = False
        if not os.path.isfile(course_data['exp_doc_path']):
            print("数据错误：实验手册文件不存在")
            check_flag = False
        if not os.path.isfile(course_data['exp_enclosure_path']):
            print("数据错误：实验附件文件不存在")
            check_flag = False
        for item in course_data['exp_images']:
            if item['image_file'] =='':
                print("文件定义错误：虚拟机镜像不能为空,请检查配置项")
                check_flag = False
            elif not os.path.isfile(item['image_file']):
                print("文件定义错误：虚拟机镜像文件不存在,请检查配置项")
                check_flag = False


    if not check_flag:
        print("数据校验：数据校验未通过，请修改数据重试!!!!!!!!!!!!")
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    else:
        print('数据校验通过!!!')
        print('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')



LIST_KJLX = [[1, '教学类'], [2, '实训类']]
LIST_KJLB = [[1, '文本型'], [2, '视频型'], [3, '虚拟机型']]
LIST_KJND = [[1, '1星'], [2, '2星'], [3, '3星'], [4, '4星'], [5, '5星']]
# 本地数据库文件名
SQLITE3_DB = 'sqlite3.db'
# 课件方向字典表UUID
DICT_UUID = '85349680-b49e-11e8-b3c3-994915e7tre'
LIST_KJFX = get_kjfx()
LIST_KJFL = []




if __name__ == '__main__':
    # create_course_form()
    check_course_form()
