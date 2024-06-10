# 实现了用户注册，登录
from datetime import datetime
import pandas as pd
import log_write
import os

user_path = 'users.xlsx'
user_columns = [
    "Id", "Username", "Password", "Authority", "Log"
]


def first_use(filename=user_path):
    df = pd.DataFrame(columns=user_columns)
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)


# 定义一个函数来检查用户名是否已存在
def check_username_exists(username, filename_=user_path):
    df = pd.read_excel(filename_)
    if df.loc[df['Username'] == username, 'Id'].values.size > 0:
        return int(df.loc[df['Username'] == username, 'Id'].values[0])
    else:
        return False


def get_id(xlsx_file):
    try:
        # 读取Excel文件
        df = pd.read_excel(xlsx_file)

        # 确保至少有一行数据
        if df.empty:
            return 1

        # 获取第一列的所有值
        first_column = df.iloc[:, 0]
        return first_column.max() + 1
    except Exception as e:
        print(f"读取Excel文件时发生错误：{e}")
        return None


# 用户注册
def register(username, password, filename_=user_path):
    if check_username_exists(username):
        print("该用户名已被注册，请选择其他用户名。")
        return False
    else:
        # 将新用户数据保存到Excel文件
        Id = str(get_id(filename_))
        Authority = "0"
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        current_time = str(current_time)
        Log = f"./log/{Id}_{current_time}.xlsx"
        log_write.log_create(Log, current_time, username, password)
        user_data = pd.DataFrame([[Id, username, password, Authority, Log]], columns=user_columns)
        df = pd.read_excel(filename_)
        df = pd.concat([df, user_data], ignore_index=True)
        df.to_excel(filename_, index=False)
        print("注册成功！")
        return True


# 用户登录
def login(username, password, filename_=user_path):
    df = pd.read_excel(filename_)
    id_ = check_username_exists(username, filename_='users.xlsx')
    try:
        if password == str(df.loc[df['Id'] == id_, 'Password'].values[0]):
            print("登录成功！")
            xlsx_path = df.loc[df['Id'] == id_, 'Log'].values[0]
            log_write.login(xlsx_path)
            return int(df.loc[df['Username'] == username, 'Id'].values[0])
        else:
            print("用户名或密码错误，请重试。")
            return False
    except Exception as e:
        print("用户名不存在，请重试。")
        return False

# 用户信息修改
def update_user_info(user_id, column_name, new_value, filename_=user_path):
    try:
        column_name = str(column_name)
        # 读取现有的Excel文件
        df = pd.read_excel(filename_)

        # 检查列名是否存在
        if column_name not in df.columns:
            print(f"列名 '{column_name}' 不存在于Excel文件中。")
            return False

        # 确保用户ID是数字
        user_id = int(user_id)
        # 更新找到的用户ID对应的列信息
        df.loc[df['Id'] == user_id, column_name] = str(new_value)
        # 将更新后的DataFrame保存回Excel文件
        df.to_excel(filename_, index=False)

        log_write.update_user_info(log_write.find_user_log(user_id), f"upgrade {column_name}")
        print("用户信息已更新。")
        return True
    except Exception as e:
        print(f"更新用户信息时发生错误：{e}")
        return False


def show_user_details(user_id):
    from data import query_document_by_id
    result = query_document_by_id(user_id, user_path)
    print(result)


if not os.path.exists(user_path):
    first_use(user_path)
