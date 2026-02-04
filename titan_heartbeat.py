import time, os, subprocess, shutil
WATCH = r'C:\Monolith\Actions'
ARCHIVE = r'C:\Monolith\Memory\Archive'
TRASH = r'C:\Monolith\Memory\Trash'

print('--- TITAN ENGINE ONLINE ---')
while True:
    for f in os.listdir(WATCH):
        path = os.path.join(WATCH, f)
        if os.path.isfile(path) and not f.startswith('.'):
            print(f'[EXECUTING] {f}')
            try:
                if f.endswith('.py'): subprocess.run(['python', path], check=True)
                elif f.endswith('.ps1'): subprocess.run(['powershell', '-File', path], check=True)
                elif f.endswith('.js'): subprocess.run(['node', path], check=True)
                shutil.move(path, os.path.join(ARCHIVE, f))
                print('[SUCCESS]')
            except Exception as e:
                print(f'[ERROR] {e}')
                shutil.move(path, os.path.join(TRASH, f))
    time.sleep(2)
