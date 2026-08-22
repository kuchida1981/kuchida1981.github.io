#!/usr/bin/env python3
import sys
import re
from datetime import datetime, timezone, timedelta

def main():
    files = sys.argv[1:]
    if not files:
        print("No files specified for date correction.")
        return

    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    now_epoch = int(now.timestamp())
    now_iso = now.strftime('%Y-%m-%dT%H:%M:%S+09:00')

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f'Error reading {file_path}: {e}')
            continue

        match = re.search(r'(?m)^date:\s*[\x27\"]?([^\x27\n\"]*)[\x27\"]?', content)
        if not match:
            print(f'No date field found in {file_path}')
            continue

        date_str = match.group(1).strip()
        clean_date_str = date_str
        if clean_date_str.endswith('Z'):
            clean_date_str = clean_date_str[:-1] + '+00:00'
        clean_date_str = re.sub(r'\.[0-9]+', '', clean_date_str)

        try:
            dt = datetime.fromisoformat(clean_date_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            file_epoch = int(dt.timestamp())
        except Exception as e:
            print(f'Error parsing date \'{date_str}\' in {file_path}: {e}')
            continue

        if file_epoch <= now_epoch:
            new_content, count = re.subn(r'(?m)^date:\s*.*$', f'date: {now_iso}', content)
            if count > 0:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Corrected date in {file_path}: {date_str} -> {now_iso}')
                except Exception as e:
                    print(f'Error writing {file_path}: {e}')
            else:
                print(f'Failed to replace date in {file_path}')

if __name__ == "__main__":
    main()
