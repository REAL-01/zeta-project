import os
import random

used_comments = set()

bases = ["похуй", "пахую", "похую", "пахуй", "пох", "пхуй", "пахуи", "похуи"]
mid = ["ваще", "и так", "типа", "ну", "вообще", "абсолютно", "кста", "жестко", ""]
ends = ["сойдет", "работает", "пашет", "катит", "прокатит", "пойдет", "хуярит", "крутится", ""]
punct = ["", "!", "!!", "...", "..", " 111", " азаз", " лол", " кек", " бля"]

def generate_unique():
    while True:
        b = random.choice(bases)
        m = random.choice(mid)
        e = random.choice(ends)
        p = random.choice(punct)
        
        # Add random character repetitions for bad grammar
        if random.random() < 0.3: b = b.replace('у', 'уу' * random.randint(1, 3))
        if random.random() < 0.3: b = b.replace('о', 'оо' * random.randint(1, 3))
        if random.random() < 0.3: e = e.replace('е', 'ее' * random.randint(1, 3))
        
        parts = [b]
        if m: parts.append(m)
        if e: parts.append(e)
        
        phrase = " ".join(parts) + p
        if phrase not in used_comments:
            used_comments.add(phrase)
            return phrase

def process_file(content, ext):
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        sline = line.strip()
        if sline.startswith('//') or sline.startswith('#'):
            # Check if it is one of our "pohuy" comments
            if 'похуй' in sline or 'пахую' in sline or 'сойдет' in sline or 'работает' in sline:
                indent = len(line) - len(line.lstrip())
                prefix = "# " if ext == '.py' else "// "
                new_lines.append(" " * indent + prefix + generate_unique())
                continue
        new_lines.append(line)
        
    return '\n'.join(new_lines)


base_dir = r"c:\Users\nereal\Desktop\Программы\project_zeta"

count = 0
for root, dirs, files in os.walk(base_dir):
    if 'venv' in root or '.git' in root or '__pycache__' in root:
        continue
    for file in files:
        if file in ['simulator.html', 'views.py', 'lobby.html', 'models.py']:
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                orig = content
                ext = '.py' if file.endswith('.py') else '.js'
                content = process_file(content, ext)
                
                if content != orig:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated {path}")
                    count += 1
            except Exception as e:
                pass
print(f"Done, replaced comments with {len(used_comments)} unique variations.")
