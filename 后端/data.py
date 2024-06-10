# 主要实现了文章管理
import os
from datetime import datetime
import pandas as pd
import shutil
import log_write

shared_datas_path = "shared_datas.xlsx"
unshared_datas_path = "unshared_datas.xlsx"

data_columns = [
        "Id", "Filename", "Address", "Editors ID List", "Creator ID",
        "Date", "Keywords", "Title", "Type", "Commentary File Address"
    ]

# 创建文件结构
if True:
    data_path = "./data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    shared_datas = "./data/shared_datas"
    if not os.path.exists(shared_datas):
        os.makedirs(shared_datas)
    unshared_datas = "./data/unshared_datas"
    if not os.path.exists(unshared_datas):
        os.makedirs(unshared_datas)
    commentary = "./data/commentary"
    if not os.path.exists(commentary):
        os.makedirs(commentary)


# 判断是否为管理员
def is_666(user_id, is_print=False):
    if is_print and query_document_by_id(user_id, "users.xlsx")["Authority"] == 666:
        print("尊敬的管理员，您好\n立即执行指令")
    return query_document_by_id(user_id, "users.xlsx")["Authority"] == 666


def query_document_by_id(id_, filename_):
    """
    根据文档的 ID 查询相应的其他列信息。
    :param id_: 文档的唯一标识符（ID）
    :param filename_: 存储文档信息的 Excel 文件路径
    :return: 一个包含文档信息的字典，如果没有找到，则返回 None
    """
    try:
        # 读取 Excel 文件
        df = pd.read_excel(filename_)
        # 检查是否存在该 ID
        if df.loc[df['Id'] == id_, 'Id'].values.size == 0:
            print(f"未找到 ID 为 {id_} 。")
            return None
        # 获取匹配的行
        document_info = df.loc[df['Id'] == id_].iloc[0].to_dict()
        return document_info
    except Exception as e:
        print(f"查询时发生错误：{e}")
        return None


def query_document_by_Filename(name_, filename_):
    """
    根据文档的 ID 查询相应的其他列信息。
    :param name_: 文档名（ID）
    :param filename_: 存储文档信息的 Excel 文件路径
    :return: 一个包含文档信息的字典，如果没有找到，则返回 None
    """
    try:
        # 读取 Excel 文件
        df = pd.read_excel(filename_)
        # 检查是否存在该 ID
        if df.loc[df['Filename'] == name_, 'Id'].values.size == 0:
            print(f"未找到 Filename 为 {name_} 。")
            return None
        # 获取匹配的行
        document_info = df.loc[df['Filename'] == name_].iloc[0].to_dict()
        return document_info
    except Exception as e:
        print(f"查询时发生错误：{e}")
        return None


def first_use(filename):
    df = pd.DataFrame(columns=data_columns)
    # 将Keywords和Editors ID List转换为字符串
    df["Keywords"] = df["Keywords"].apply(lambda x: ', '.join(x))
    df["Editors ID List"] = df["Editors ID List"].apply(lambda x: ', '.join(x))
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)


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


def check_data_name_exists(name, filename):
    df = pd.read_excel(filename)
    if df.loc[df['Filename'] == name, 'Id'].values.size > 0:
        return int(df.loc[df['Filename'] == name, 'Id'].values[0])
    else:
        return False


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


def new_document(user_id, name, data, filename=unshared_datas_path):
    # 检查文档名称是否已存在
    if check_data_name_exists(name, filename):
        print(f"文档名称 '{name}' 已存在。")
        return False
    # 创建文档的当前时间戳
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    current_time = str(current_time)
    # 创建文档的完整路径
    document_path = unshared_datas + "/" + f"{name}_{current_time}.txt"
    # 创建评论文件的完整路径
    commentary_path = commentary + "/" + f"{name}_{current_time}.xlsx"
    # 获取新文档的ID
    Id = get_id(filename)
    # 创建新文档的行数据
    row_data = [Id, name, document_path, [user_id], user_id, current_time, [], name, None, commentary_path]
    # 将新行数据追加到Excel文件
    add_row_to_excel(filename, row_data)
    # 写入文档数据到文件
    with open(document_path, 'w') as file:
        file.write(data)
    # 记录新文档创建的日志
    log_write.new_document(log_write.find_user_log(user_id), name)
    # 打印成功消息
    print(f"新文档 '{name}' 创建成功。")
    return True


def upgrade_document(user_id, name, data):
    message = False
    document_id = -1
    for path in [unshared_datas_path, shared_datas_path, False]:
        if not path:
            if message:
                print(message)
            return False
        df = pd.read_excel(path)
        # 检查文档是否存在
        if df.loc[df['Filename'] == name, 'Id'].values.size == 0:
            continue
        # 获取文档的ID
        document_id = df.loc[df['Filename'] == name, 'Id'].values[0]
        # 获取文档的编辑者列表
        editors_id_list = df.loc[df['Id'] == document_id, 'Editors ID List'].values[0]
        # 检查用户是否有修改权限
        if not is_666(user_id):
            if str(user_id) not in editors_id_list:
                message = f"用户 '{user_id}' 没有权限修改文档 '{name}'。"
                continue
        break
    # 获取文档的完整路径
    document_path = df.loc[df['Id'] == document_id, 'Address'].values[0]
    with open(document_path, 'w') as file:
        file.write(data)
    log_write.update_document(log_write.find_user_log(user_id), name)
    print(f"文档 '{name}' 已成功更新。")
    return True


def delete_document(user_id, name):
    message = False
    document_id = -1
    for path in [unshared_datas_path, shared_datas_path, False]:
        if not path:
            if message:
                print(message)
            return False
        df = pd.read_excel(path)
        # 检查文档是否存在
        if df.loc[df['Filename'] == name, 'Id'].values.size == 0:
            continue
        # 获取文档的ID
        document_id = df.loc[df['Filename'] == name, 'Id'].values[0]
        # 获取文档的编辑者列表
        editors_id_list = df.loc[df['Id'] == document_id, 'Editors ID List'].values[0]
        # 检查用户是否有修改权限
        if not is_666(user_id):
            if str(user_id) not in editors_id_list:
                message = f"用户 '{user_id}' 没有权限修改文档 '{name}'。"
                continue
        break
    document_path = df.loc[df['Id'] == document_id, 'Address'].values[0]
    # 删除文件系统中的文档
    try:
        os.remove(document_path)
    except OSError as e:
        print(f"删除文件时发生错误：{e}")
        return False
    # 更新数据库中的记录（从Excel文件中删除对应的行）
    try:
        df.drop(df[df['Id'] == document_id].index, inplace=True)
        df.to_excel(path, index=False)
    except Exception as e:
        print(f"更新数据库时发生错误：{e}")
        return False
    log_write.delete_document(log_write.find_user_log(user_id), name)
    # 打印成功消息
    print(f"文档 '{name}' 已成功删除。")
    return True


def make_document_public(user_id, document_name):
    # 读取私有和共享数据的Excel文件
    df_unshared = pd.read_excel(unshared_datas_path)
    df_shared = pd.read_excel(shared_datas_path)
    # 检查文档是否存在于私有数据中
    if df_unshared.loc[df_unshared['Filename'] == document_name, 'Id'].values.size == 0:
        print(f"文档 '{document_name}' 不存在于私有数据中。")
        return False
    # 获取文档的ID
    document_id = df_unshared.loc[df_unshared['Filename'] == document_name, 'Id'].values[0]
    # 验证用户权限（用户ID是文档的创建者）
    creator_id = df_unshared.loc[df_unshared['Id'] == document_id, 'Creator ID'].values[0]
    if str(user_id) != str(creator_id):
        print(f"用户 '{user_id}' 没有权限公开文档 '{document_name}'。")
        return False
    # 获取文档和评论文件的完整路径
    document_path = df_unshared.loc[df_unshared['Id'] == document_id, 'Address'].values[0]
    # 创建共享数据的行数据，并更新文件路径
    shared_row_data = df_unshared.loc[df_unshared['Id'] == document_id].copy()
    shared_row_data['Address'] = os.path.join(shared_datas, os.path.basename(document_path))
    # 删除私有数据中的文档记录
    df_unshared.drop(df_unshared.index[document_id - 1], inplace=True)
    df_unshared.to_excel(unshared_datas_path, index=False)
    # 将行数据添加到共享数据中
    df_shared = pd.concat([df_shared, shared_row_data], ignore_index=True)
    df_shared.to_excel(shared_datas_path, index=False)
    # 移动文件到共享文件夹
    shutil.move(document_path, shared_row_data['Address'].values[0])
    # 记录日志
    log_path = log_write.find_user_log(user_id)  # 假设这个函数返回正确的日志文件路径
    log_write.log_make_document_public(log_path, document_name)
    # 打印成功消息
    print(f"文档 '{document_name}' 已成功公开。")
    return True


if not os.path.exists(shared_datas_path):
    first_use(shared_datas_path)
if not os.path.exists(unshared_datas_path):
    first_use(unshared_datas_path)

if __name__ == "__main__":
    new_document(1, "filename1", "filename1: this is unshared_datas")
    upgrade_document(1, "filename1", "filename1: this is upgraded unshared_datas")
    make_document_public(1, "filename1")
    delete_document(1, "filename1")
