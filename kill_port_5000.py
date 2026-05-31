import os
output = os.popen('netstat -a -n -o | findstr :5000').read()
for line in output.splitlines():
    if 'LISTENING' in line:
        pid = line.strip().split()[-1]
        print(f"Killing PID {pid}")
        os.system(f'taskkill /f /pid {pid}')
