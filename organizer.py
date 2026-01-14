# organizer.py
import os
import argparse

def list_files(folder):
    """列出指定文件夹及子文件夹里的所有文件"""
    for root, dirs, files in os.walk(folder):
        for file in files:
            print(os.path.join(root, file))

def main():
    parser = argparse.ArgumentParser(description="Auto File Organizer")
    parser.add_argument('--src', required=True, help='Folder to organize')
    args = parser.parse_args()

    folder_path = args.src
    if not os.path.exists(folder_path):
        print(f"错误：路径 {folder_path} 不存在")
        return

    print(f"正在列出 {folder_path} 中的所有文件：")
    list_files(folder_path)

if __name__ == "__main__":
    main()
