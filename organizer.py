import os
import shutil
import argparse
from datetime import datetime
import logging

logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# 定义常见文件类型对应的文件夹
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
    "Music": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
}

def get_category(file_name):
    """根据文件扩展名返回分类文件夹名称"""
    ext = os.path.splitext(file_name)[1].lower()
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Others"

def organize_files(folder, dry_run=True):
    """按类型整理文件"""
    for root, dirs, files in os.walk(folder):
        # 避免整理已经创建的分类文件夹
        if os.path.abspath(root) != os.path.abspath(folder):
            continue
        for file in files:
            category = get_category(file)
            src_path = os.path.join(root, file)
            dest_folder = os.path.join(folder, category)
            dest_path = os.path.join(dest_folder, file)

            if dry_run:
                msg = f"DRY-RUN: {src_path} -> {dest_path}"
                print(msg)
                logging.info(msg)

            else:
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(src_path, dest_path)
                msg = f'Moved: {src_path} -> {dest_path}'
                print(msg)
                logging.info(msg)

def organize_by_date(folder, dry_run=True):
    """按文件修改日期（YYYY-MM）整理"""
    for root, dirs, files in os.walk(folder):
        if os.path.abspath(root) != os.path.abspath(folder):
            continue

        for file in files:
            src_path = os.path.join(root, file)

            # 获取文件修改时间
            mtime = os.path.getmtime(src_path)
            date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m")

            dest_folder = os.path.join(folder, date_str)
            dest_path = os.path.join(dest_folder, file)

            if dry_run:
                msg = f"DRY-RUN: {src_path} -> {dest_path}"
                print(msg)
                logging.info(msg)
            else:
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(src_path, dest_path)
                msg = f"Moved: {src_path} -> {dest_path}"
                print(msg)
                logging.info(msg)


def main():
    parser = argparse.ArgumentParser(description="Auto File Organizer")
    parser.add_argument('--src', required=True, help='Folder to organize')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without moving files')
    parser.add_argument(
        '--by',
        choices=['type', 'date'],
        default='type',
        help='Organize files by type or date'
    )
    args = parser.parse_args()
    folder_path = args.src
    logging.info(f"Start organizing folder: {folder_path} (by={args.by}, dry_run={args.dry_run})")
    if not os.path.exists(folder_path):
        print(f"错误：路径 {folder_path} 不存在")
        return

    print(f"正在整理 {folder_path}（dry-run={args.dry_run}）")
    if args.by == 'type':
        organize_files(folder_path, dry_run=args.dry_run)
    elif args.by == 'date':
        organize_by_date(folder_path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()