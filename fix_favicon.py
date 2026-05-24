import glob, re

files = glob.glob('*.html')
updated = 0

PATTERN = re.compile(r'<link rel="icon"[^>]*/>')
NEW_TAG = '<link rel="icon" href="favicon.svg?v=2" type="image/svg+xml"/>'

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    # Debug: show what icon tag looks like in this file
    found = PATTERN.findall(content)
    if found:
        print(f'  found in {f}: {found[0][:60]}')
        new_content = PATTERN.sub(NEW_TAG, content)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        updated += 1
    elif 'favicon' in content:
        # Show the line with favicon so we can debug
        for line in content.splitlines():
            if 'favicon' in line.lower():
                print(f'  DEBUG {f}: {repr(line[:80])}')
                break

print(f'Done — {updated} files updated')
