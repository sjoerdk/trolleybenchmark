import os

def du(path):
    """Bytes in path quick, linux only"""
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += du(entry.path)
    return total


def format_bytes(size, split=False):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    if split:
        return size, power_labels[n]
    else:
        return f'{size:.2f}{power_labels[n]}'

