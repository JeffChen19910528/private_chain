#!/bin/bash

# 文件名作为脚本的第一个参数
FILES="password.txt"

# 定义一个函数来显示文件的当前内容
display_file_content() {
    echo "当前文件内容："
    nl -ba "$FILES"  # nl命令用于添加行号并打印文件内容
    echo "----------------------------"
}

# 检查文件是否存在，如果不存在，则创建
if [ ! -f "$FILES" ]; then
    echo "文件不存在，创建新文件：$FILES"
    touch "$FILES"
fi

# 显示初始内容
display_file_content

# 定义一个函数用于删除指定行号的内容
delete_line() {
    sed -i "${1}d" "$FILES"
}

# 指定文件夹路径
DIR_PATH="$PWD/data/keystore"

# 初始化地址数组和地址到文件路径的映射
declare -a ADDRESS_ARRAY
declare -A ADDRESS_TO_FILE_MAP

# 检查文件夹是否存在
if [ ! -d "$DIR_PATH" ]; then
    echo "文件夹不存在: $DIR_PATH"
    exit 1
fi

# 读取文件夹中的每个JSON文件
for FILE in "$DIR_PATH"/*; do
    # 使用jq工具读取每个JSON文件中的address值
    ADDRESS=$(jq -r '.address' "$FILE" 2>/dev/null)

    # 检查地址是否非空
    if [ -n "$ADDRESS" ] && [ "$ADDRESS" != "null" ]; then
        ADDRESS_ARRAY+=("$ADDRESS")
        ADDRESS_TO_FILE_MAP["$ADDRESS"]="$FILE"
    fi
done

# 显示所有读取的地址值
echo "所有读取的地址值："
for i in "${!ADDRESS_ARRAY[@]}"; do
    echo "$((i + 1))) ${ADDRESS_ARRAY[$i]}"
done

# 提示用户输入要删除的地址代号
read -p "请输入要删除的地址代号: " INDEX
let INDEX=INDEX-1

# 验证输入是否为数字和在有效范围内
if ! [[ $INDEX =~ ^[0-9]+$ ]] || [[ "$INDEX" -lt 0 || "$INDEX" -ge "${#ADDRESS_ARRAY[@]}" ]]; then
    echo "请输入一个有效的地址代号。"
    exit 1
fi

# 获取要删除的文件路径
DELETE_FILE="${ADDRESS_TO_FILE_MAP["${ADDRESS_ARRAY[$INDEX]}"]}"

# 删除文件
if [ -n "$DELETE_FILE" ]; then
    echo "正在删除文件: $DELETE_FILE"
    rm "$DELETE_FILE"
    echo "文件已删除。"
else
    echo "未找到与选择的地址相关联的文件。"
fi

# 调用函数删除指定行号的内容
delete_line $((INDEX + 1))

# 最后，再次显示文件的最终内容
display_file_content
echo "更新完成。"
./init.sh
