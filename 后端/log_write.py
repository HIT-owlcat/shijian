# 用户操作数据记录
from datetime import datetime
import pandas as pd
import os

user_path = 'users.xlsx'


def find_user_log(user_id, filename_=user_path):
    df = pd.read_excel(filename_)
    xlsx_path = df.loc[df['Id'] == user_id, 'Log'].values[0]
    return xlsx_path


def add_row_to_excel(xlsx_file, row_data, column_names=None, is_print=False):
    try:
        # 读取现有的Excel文件
        df = pd.read_excel(xlsx_file)

        # 如果没有提供列名，使用现有DataFrame的列名
        if column_names is None:
            column_names = df.columns

        # 创建一个新的DataFrame，包含要添加的行数据
        new_row_df = pd.DataFrame([row_data], columns=column_names)

        # 将新行数据追加到现有DataFrame
        df = pd.concat([df, new_row_df], ignore_index=True)

        # 将更新后的DataFrame保存回Excel文件
        df.to_excel(xlsx_file, index=False)
        if is_print:
            print("行数据已添加。")
    except Exception as e:
        if is_print:
            print(f"添加行时发生错误：{e}")


def log_create(xlsx_file, current_time, username, password):
    os.makedirs(os.path.dirname(xlsx_file), exist_ok=True)
    log_data = pd.DataFrame([[current_time, "REGISTER", f"username:{username}, password:{password}"]],
                            columns=['Time', 'Operation', 'Details'])
    log_data.to_excel(xlsx_file, index=False)


def login(xlsx_path):
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_add = [current_time, 'login', '']
    add_row_to_excel(xlsx_path, data_to_add)


def update_user_info(xlsx_path, details):
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_add = [current_time, 'new_document', f'name:{details}']
    add_row_to_excel(xlsx_path, data_to_add)


def new_document(xlsx_path, name):
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_add = [current_time, 'new_document', f'filename:{name}']
    add_row_to_excel(xlsx_path, data_to_add)


def update_document(xlsx_path, name):
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_add = [current_time, 'update', f'filename:{name}']
    add_row_to_excel(xlsx_path, data_to_add)


def delete_document(xlsx_path, name):
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_add = [current_time, 'delete', f'filename:{name}']
    add_row_to_excel(xlsx_path, data_to_add)


def log_make_document_public(xlsx_path, document_name):
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_add = [current_time, 'make public', f'document: {document_name}']
    add_row_to_excel(xlsx_path, data_to_add)


def log_add_commentary(xlsx_path, document_name, details):
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_add = [current_time, 'add_commentary', f'document: {document_name} commentary: {details}']
    add_row_to_excel(xlsx_path, data_to_add)
