import os

def create_init_file(directory):
    """为指定目录创建 __init__.py 文件（如果不存在的话）"""
    init_file_path = os.path.join(directory, '__init__.py')
    
    # 如果文件不存在，创建一个空的 __init__.py 文件
    if not os.path.exists(init_file_path):
        with open(init_file_path, 'w') as f:
            f.write('# This is an init file for the package\n')
        print(f"Created: {init_file_path}")
    else:
        print(f"Already exists: {init_file_path}")

def traverse_and_create_init_files(root_dir):
    """遍历指定目录及其子目录，创建所有目录的 __init__.py 文件"""
    for root, dirs, files in os.walk(root_dir):
        # 在每一个目录中（包括根目录）创建 __init__.py 文件
        create_init_file(root)

if __name__ == '__main__':
    # 设置根目录（你可以根据需要修改这个目录）
    root_directory = './proto'  # 修改为你的目标目录
    traverse_and_create_init_files(root_directory)