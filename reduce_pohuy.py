import os
import random
import re

unique_variations = [
    "похуй",
    "пахую",
    "похуи",
    "похуйй",
    "поохуй",
    "пхуй",
    "пахуи",
    "похую",
    "пхй",
    "похй",
    "пахю",
    "пахууй"
]

def clean_comments(content):
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        sline = line.strip()
        # Find any line that starts with // or #, but ignore Django template comments {# ... #} if they somehow exist 
        # (though we only injected // and #)
        if sline.startswith('//') or sline.startswith('#'):
            # Check if this line is likely our trash line (contains "пох" or "пах" or "пх" or "ху" etc.)
            continue
        cleaned_lines.append(line)
        
    return cleaned_lines

base_dir = r"c:\Users\nereal\Desktop\Программы\project_zeta"

files_to_touch = []
for root, dirs, files in os.walk(base_dir):
    if 'venv' in root or '.git' in root or '__pycache__' in root:
        continue
    for file in ['simulator.html', 'views.py', 'lobby.html', 'models.py']:
        if file in files:
            files_to_touch.append(os.path.join(root, file))

# First, clean all files
file_content_map = {}
for path in files_to_touch:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            cleaned_lines = clean_comments(content)
            # Remove empty lines that were created by comment removal (optional)
            
            # just store the lines
            file_content_map[path] = cleaned_lines
    except Exception as e:
        pass

# Now we have exactly 12 variations. We want to place them randomly across the files.
random.shuffle(unique_variations)

# Distribute them
available_spots = []
for path, lines in file_content_map.items():
    ext = '.py' if path.endswith('.py') else '.js'
    prefix = "# " if ext == '.py' else "// "
    
    # Find "complex" spots
    for i, line in enumerate(lines):
        sline = line.strip()
        if sline == "": continue
        indent = len(line) - len(line.lstrip())
        
        is_complex = False
        if ext == '.py':
            if indent >= 8 and (sline.startswith('if ') or sline.startswith('for ') or sline.startswith('try:')):
                is_complex = True
        else:
            if indent >= 12 and (sline.startswith('if ') or sline.startswith('for') or sline.startswith('function')):
                is_complex = True
                
        if is_complex:
            available_spots.append((path, i, indent, prefix))

# Pick exactly 12 random spots (or as many as we have available)
spots_to_use = random.sample(available_spots, min(len(unique_variations), len(available_spots)))

insertions = {} # path -> { line_index : prefix + text }
for idx, spot in enumerate(spots_to_use):
    path, line_idx, indent, prefix = spot
    if path not in insertions:
        insertions[path] = {}
    insertions[path][line_idx] = " " * indent + prefix + unique_variations[idx]

# Write back
for path, lines in file_content_map.items():
    final_lines = []
    
    for i, line in enumerate(lines):
        if i in insertions.get(path, {}):
            final_lines.append(insertions[path][i])
        final_lines.append(line)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(final_lines))
    print(f"Updated {path} with {len(insertions.get(path, {}))} comments")

print("Done")
