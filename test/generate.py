with open('large1/test', 'wb') as f:
    for i in range(10 ** 3):
        f.write(b"\0" * 1000)

with open('large2/test', 'wb') as f:
    for i in range(10 ** 3):
        f.write(b"\0" * 1000)