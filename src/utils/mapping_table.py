# -*- coding: utf-8 -*-
# @Time    : 2024/05/06 15:54:12
# @Author  : DannyDong
# @File    : mapping_table.py
# @Describe: 映射表

# 用于解析学生信息批量上传数据
UPLOAD_STUDENT_MAPPING_TABLE = {
    '学号': 'student_id',
    '学生姓名': 'name',
    '登录账号': 'username',
    '登录密码': 'password',
    '性别': 'gender',
    '是否激活': 'is_active',
    '电话': 'phone',
    '邮箱': 'email'
}

# 用于将单个字典中的中文字段名映射为英文字段名
def translate_fields(record, mapping):
    return { mapping.get(key, key): value for key, value in record.items() }


if __name__ == '__main__':
    pass
