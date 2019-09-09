import urllib.request

def download_file(url, file_name):
    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')

    file_size = int(u.info()['Content-Length'])

    print('Downloading: {}\nInto: {}'.format(url, file_name))

    file_size_dl = 0
    block_sz = 8192
    last_status = -1

    while 1:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = 'Bytes: {}/{} [{:.2f}%]'.format(file_size_dl, file_size, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)

        if status != last_status:
            print(status, end='\r')
            last_status = status

    print()
    f.close()