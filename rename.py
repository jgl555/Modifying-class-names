#!/usr/bin/env python
#coding=utf-8
import os,sys

# 需要修改的类名前缀(需要替换)
pre_str = 'aaa'
# 新的类名前缀(需要替换)
pre_to_str = 'bb'
# 搜寻以下文件类型(自己需要替换)
suf_set = ('.h', '.m', '.xib', '.storyboard', '.mm', '.pch','.swift')
# 项目路径(需要替换)
project_path = '/Users/jgl/app'
# 项目配置文件路径(需要替换)(显示包内容 app.xcodeproj)
pbxpro_path = '/Users/jgl/app/app.xcodeproj/app.pbxproj'


# 文件重命名函数，返回新的文件名
def file_rename(file_path):
    root_path = os.path.split(file_path)[0]     # 文件目录
    root_name = os.path.split(file_path)[1]     # 文件名包含扩展名
    filename = os.path.splitext(root_name)[0];  # 文件名
    filetype = os.path.splitext(root_name)[1];  # 文件扩展名

    new_path = os.path.join(root_path, filename.replace(pre_str, pre_to_str) + filetype)    # 拼接新路径
    os.renames(file_path, new_path)             # 文件重命名
    return filename.replace(pre_str, pre_to_str)

# 定义一个字典 key=旧类名 value=新类名
needModifyDic = {}

# 遍历文件，符合规则的进行重命名
for (root, dirs, files) in os.walk(project_path):
    for file_name in files:
        if file_name.startswith((pre_str,)) and file_name.endswith(suf_set):
            old_name = os.path.splitext(file_name)[0]
            new_name = file_rename(os.path.join(root, file_name))
            needModifyDic[old_name] = new_name

# 遍历文件，在文件中更换新类名的引用
print(needModifyDic)
for (root, dirs, files) in os.walk(project_path):
    for file_name in files:
        if file_name.endswith(suf_set):
            print('-----fileName-------' + file_name)
            with open(os.path.join(root, file_name), 'r+') as f:
                print('========fileName========' + file_name)
                s0 = f.read()
                f.close()
                for key in needModifyDic:
                    if key in s0:
                        with open(os.path.join(root, file_name), 'r+') as f4:
                            s1 = f4.read().replace(key, needModifyDic[key])
                            print(key + ' ------> ' + needModifyDic[key])
                            f4.seek(0)
                            f4.write(s1)
                            f4.truncate()
                            f4.close()
# 替换配置文件中的类名
for key in needModifyDic:
    with open(pbxpro_path, 'r+') as f:
        s0 = f.read()
        f.close()
        if key in s0:
            with open(pbxpro_path, 'r+') as f2:
                s = f2.read().replace(key, needModifyDic[key])
                f2.seek(0)
                f2.write(s)
                f2.truncate()
                f2.close()

