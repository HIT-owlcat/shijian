from user import *
from data import *
from commentary import *


# 用户注册及登录
def main():
    while True:
        print("\n文章管理系统")
        print("1. 注册")
        print("2. 登录")
        print("3. 退出")
        choice = input("请选择一个操作：")

        if choice == '1':
            username = input("输入用户名：")
            password = input("输入密码：")
            register(username, password)
        elif choice == '2':
            username = input("输入用户名：")
            password = input("输入密码：")
            user_id_ = login(username, password)
            if user_id_:
                print("user_id:", user_id_)
                action1(user_id_)
        elif choice == '3':
            break
        else:
            print("无效的输入，请重新选择。")


# 登录后用户操作
def action1(user_id):
    while True:
        print("\n请选择一个操作:")
        print("0. 查看个人信息")
        print("1. 修改个人信息")
        print("2. 查看共享文章")
        print("3. 查看私有文章")
        print("4. 创建新文章")
        print("5. 修改文章")
        print("6. 删除文章")
        print("7. 公开文章")
        print("8. 退出")
        choice = input("请输入您的选择：")
        if choice == '0':
            # 查看个人信息
            show_user_details(user_id)
        elif choice == '1':
            # 修改个人信息
            column_name = input("请输入修改类别：")
            new_value = input("请输入修改结果：")
            update_user_info(user_id, column_name, new_value, filename_=user_path)
        elif choice == '2':
            # 查看共享文章
            # todo 待完善
            df = pd.read_excel(shared_datas_path)
            # print(df)
            data_reading = input("请输入想要查看的文章：")
            reading_details = query_document_by_Filename(data_reading, shared_datas_path)
            if not reading_details:
                continue
            reading_path = reading_details["Address"]
            reading_id = reading_details["Id"]
            with open(reading_path, 'r', encoding='utf-8') as file:
                # 读取文件内容
                content = file.read()
                # 打印文件内容
                print(content)
            action2(user_id, reading_id)
        elif choice == '3':
            # 查看私有文章
            # todo 待完善
            df = pd.read_excel(unshared_datas_path)
            # print(df)
            data_reading = input("请输入想要查看的文章：")
            reading_details = query_document_by_Filename(data_reading, unshared_datas_path)
            if not reading_details:
                continue
            reading_path = reading_details["Address"]
            reading_id = reading_details["Id"]
            with open(reading_path, 'r', encoding='utf-8') as file:
                # 读取文件内容
                content = file.read()
                # 打印文件内容
                print(content)
        elif choice == '4':
            # 创建新文件 默认不公开
            filename = input("输入文件的名称：")
            data = input("输入文件内容：")
            new_document(user_id, filename, data)
        elif choice == '5':
            # 修改文件
            filename = input("输入文件的名称：")
            data = input("输入文件内容：")
            new_document(user_id, filename, data)
            upgrade_document(user_id, filename, data)
        elif choice == '6':
            # 删除文章
            filename = input("输入文件的名称：")
            delete_document(user_id, filename)
            """elif choice == '2':
                # 添加评论
                file_id = int(input("输入要评论的共享文件的ID："))
                comment = input("输入您的评论：")
                add_comment(file_id, user_id, comment)
            elif choice == '3':
                # 读取评论
                file_id = int(input("输入要读取评论的共享文件的ID："))
                read_comments(file_id)"""
        elif choice == "7":
            # 公开文章
            filename = input("输入文件的名称：")
            make_document_public(user_id, filename)
        elif choice == '8':
            # 退出
            print("退出操作。")
            break
        else:
            print("无效的输入，请重新选择。")


# 阅读共享文件操作
def action2(user_id, reading_id):
    while True:
        print("\n请选择一个操作:")
        print("0. 查看评论")
        print("1. 添加评论")
        print("2. 退出")
        choice = input("请输入您的选择：")
        if choice == '0':
            # 查看评论
            read_comments(reading_id)
        elif choice == '1':
            # 添加评论
            comment = input("请输入评论：")
            add_comment(reading_id, user_id, comment)
        elif choice == '2':
            # 退出
            print("退出操作。")
            break
        else:
            print("无效的输入，请重新选择。")


if __name__ == "__main__":
    main()
