import os
import re

# すべてのUIファイルを取得
files_to_fix = [
    "ui/wifi_card.py",
    "ui/add_wifi_dialog.py"
]

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 正しくないパターンを修正
    content = re.sub(r'"wifi"_FIND', '"wifi_find"', content)
    content = re.sub(r'"edit"', '"edit"', content)  # すでに正しい
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"修正しました: {filepath}")

print("完了！")
