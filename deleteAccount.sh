#!/bin/bash

# 文件名作為腳本的第一個參數
FILES="password.txt"

# 检查文件是否存在
if [ ! -f "$FILES" ]; then
    echo "文件不存在，创建新文件：$FILES"
    touch "$FILES"
fi

# 定义一个函数来显示文件的当前内容
display_file_content() {
    echo "当前文件内容："
    nl -ba "$FILES"  # nl命令用于添加行号并打印文件内容
    echo "----------------------------"
}

# 定义一个函数用于删除指定行号的内容
delete_line() {
    local line_number="$1"
    let line_number=line_number+1
    
    if [[ ! -f "$FILES" ]]; then
        echo "錯誤：檔案 '$FILES' 不存在。"
        return 1
    fi
    sed -i "${line_number}d" "$FILES"
}

# 指定資料夾路徑
DIR_PATH="$PWD"/data/keystore

# 初始化地址陣列和地址到文件路徑的映射
declare -a ADDRESS_ARRAY
declare -A ADDRESS_TO_FILE_MAP

# 檢查資料夾是否存在
if [ ! -d "$DIR_PATH" ]; then
    echo "資料夾不存在: $DIR_PATH"
    exit 1
fi

# 讀取資料夾中的每個JSON文件
for FILE in "$DIR_PATH"/*; do
    # 檢查文件是否為正常的文件
    if [ ! -f "$FILE" ]; then
        echo "跳過非正常文件: $FILE"
        continue
    fi

    # 使用jq工具讀取每個JSON檔案中的address值
    ADDRESS=$(jq -r '.address' "$FILE")
    
    # 檢查地址是否非空
    if [ ! -z "$ADDRESS" ] && [ "$ADDRESS" != "null" ]; then
        # 將地址添加到地址陣列中
        ADDRESS_ARRAY+=("$ADDRESS")
        # 將地址和文件路徑關聯起來
        ADDRESS_TO_FILE_MAP["$ADDRESS"]="$FILE"
    fi
done

# 顯示地址陣列
display_file_content
echo "所有讀取的地址值："
for i in "${!ADDRESS_ARRAY[@]}"; do
    echo "$((i+1))) ${ADDRESS_ARRAY[$i]}"
done

# 提示用戶輸入要刪除的地址代號
read -p "請輸入要刪除的地址代號: " INDEX

# 計算實際索引值
let INDEX=INDEX-1

# 驗證輸入
if [[ "$INDEX" -lt 0 || "$INDEX" -ge "${#ADDRESS_ARRAY[@]}" ]]; then
    echo "錯誤：請輸入一個有效的地址代號。"
    exit 1
fi

# 獲取要刪除的文件路徑
DELETE_FILE="${ADDRESS_TO_FILE_MAP["${ADDRESS_ARRAY[$INDEX]}"]}"

# 刪除文件
if [ -n "$DELETE_FILE" ]; then
    echo "正在刪除文件: $DELETE_FILE"
    rm "$DELETE_FILE"
    echo "文件已刪除。"
else
    echo "未找到與選擇的地址相關聯的文件。"
fi

 # 检查输入是否为数字
if ! [[ $INDEX =~ ^[0-9]+$ ]]; then
    echo "请输入有效的行号。"
    exit 1
fi
# 调用函数删除指定行号的内容
delete_line $INDEX
# 最后，再次显示文件的最终内容
display_file_content
echo "更新完成。"
./init.sh