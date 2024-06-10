# 评论操作
import os
from datetime import datetime
import pandas as pd
import log_write

shared_datas_path = "shared_datas.xlsx"
user_path = 'users.xlsx'


def query_document_by_id(id_, filename_):
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


def create_comment_file(comment_file_path):
    if os.path.exists(comment_file_path):
        return
    # 确保评论文件的目录存在
    os.makedirs(os.path.dirname(comment_file_path), exist_ok=True)

    # 创建一个空的DataFrame作为评论文件
    comment_df = pd.DataFrame(columns=["Comment Time", "Username", "Comment Content"])

    # 将空的DataFrame保存为Excel文件
    with pd.ExcelWriter(comment_file_path, engine='openpyxl') as writer:
        comment_df.to_excel(writer, index=False)
    print(f"评论文件已创建在：{comment_file_path}")


def add_comment(file_id_, user_id_, comment_content):
    comment_file_path = query_document_by_id(file_id_, shared_datas_path)["Commentary File Address"]
    if not os.path.exists(comment_file_path):
        create_comment_file(comment_file_path)
    # 创建评论记录
    comment_record = {
        "Comment Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Username": query_document_by_id(user_id_, user_path)["Username"],
        "Comment Content": comment_content
    }

    # 读取现有的评论文件
    comment_df = pd.read_excel(comment_file_path)

    # 将新评论添加到DataFrame
    new_comment_df = pd.DataFrame([comment_record])
    comment_df = pd.concat([comment_df, new_comment_df], ignore_index=True)

    # 将更新后的DataFrame保存回Excel文件
    with pd.ExcelWriter(comment_file_path, engine='openpyxl') as writer:
        comment_df.to_excel(writer, index=False)
    log_write.log_add_commentary(log_write.find_user_log(user_id_),
                                 comment_file_path.split("_")[0].split("/")[-1], comment_content)
    print("评论已成功添加。")


def read_comments(file_id_):
    try:
        comment_file_path = query_document_by_id(file_id_, shared_datas_path)["Commentary File Address"]
        # 读取评论文件
        comment_df = pd.read_excel(comment_file_path)

        # 打印所有评论
        if comment_df.empty:
            print("没有找到任何评论。")
        else:
            for index, row in comment_df.iterrows():
                print(f"时间：{row['Comment Time']}, 用户名：{row['Username']}, 评论内容：{row['Comment Content']}")
    except Exception as e:
        print(f"读取评论时发生错误：{e}")


def main():
    # 登录成功后已经获取user_id
    user_id = 1
    file_id = 1
    # 用户添加评论
    add_comment(file_id, user_id, '这是一个很有用的文件！')
    # 读取并显示所有评论
    read_comments(file_id)


if __name__ == "__main__":
    main()
