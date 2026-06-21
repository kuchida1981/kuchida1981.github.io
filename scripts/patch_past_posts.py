import os
import glob

def main():
    posts_dir = "content/posts"
    # 自動生成された記事 (*-daily-news.md) を対象とする
    pattern = os.path.join(posts_dir, "**", "*-daily-news.md")
    
    files = glob.glob(pattern, recursive=True)
    print(f"Found {len(files)} potential files to patch.")
    
    patched_count = 0
    skipped_count = 0
    
    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # フロントマターの境界 (---) を特定
        # 最初の "---" と次の "---" の間がフロントマター
        parts = content.split("---", 2)
        if len(parts) >= 3:
            front_matter = parts[1]
            body = parts[2]
            
            # すでに author が設定されているかチェック
            if "author:" not in front_matter:
                # フロントマターを改行で分割
                lines = front_matter.splitlines()
                
                # 空行などを整理しつつ、末尾に author を追加
                # 最後の要素が空文字なら除外して綺麗に追加する
                if lines and lines[-1].strip() == "":
                    lines.pop()
                
                lines.append('author: "Ghost Writer"')
                
                # 再構築
                new_front_matter = "\n" + "\n".join(lines) + "\n"
                new_content = "---" + new_front_matter + "---" + body
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                
                patched_count += 1
            else:
                skipped_count += 1
        else:
            print(f"Warning: Invalid Front Matter format in {filepath}")
            
    print(f"Patch completed. Patched: {patched_count}, Skipped: {skipped_count}")

if __name__ == "__main__":
    main()
