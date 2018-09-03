**目录**

[TOC]

无损（**lossless**）压缩算法以压缩和解压数据花费的时间来换取存储数据所需的空间，这样可以缓解存储能力不足的问题。`zlip` 和 `gzip` 提供了 `GNU` 的 `Zip` 库，另外 `bz2` 允许访问更新的 `bzip2` 格式。这些格式度处理数据流，而不考虑输入格式，并且提供了接口可以透明地读写压缩文件。可以使用这些模块压缩单个文件或数据源。

标准库还包括一些模块来管理归档格式，将多个文件合并到一个文件，从而将其作为一个单元来管理。 `tarfile` 读写 `UNIX` 磁盘归档格式，虽然老但是灵活性高而广泛应用。 `zipfile` 根据 `zip` 格式来处理文档，这种格式因为 `PC` 程序 `PKZIP` 而普及，现已由 `MS_DOS` 和 `Windows` 扩展开来——因其 `API` 的简单性和这种格式的可移植性而被广泛应用。

## 1. `zlib` —— `GNU` 的`zlib` 方式压缩

作用使用底层访问 `GNU` 的 `zilib` 压缩库，为 `GNU` 项目的 `zlib` 压缩库中很多函数提供了一个底层接口。

```python
"DEFLATED", "DEF_BUF_SIZE", "DEF_MEM_LEVEL", "MAX_WBITS", "ZLIB_RUNTIME_VERSION", "ZLIB_VERSION", "Z_BEST_COMPRESSION", "Z_BEST_SPEED", "Z_BLOCK", "Z_DEFAULT_COMPRESSION", "Z_DEFAULT_STRATEGY", "Z_FILTERED", "Z_FINISH", "Z_FIXED", "Z_FULL_FLUSH", "Z_HUFFMAN_ONLY", "Z_NO_COMPRESSION", "Z_NO_FLUSH", "Z_PARTIAL_FLUSH", "Z_RLE", "Z_SYNC_FLUSH", "Z_TREES", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "__version__", "adler32", "compress", "compressobj", "crc32", "decompress", "decompressobj", "error"
```

### 1.1 处理内存中的数据

使用 `zlib` 最简单的方法要求吧所有将要压缩或解压缩的数据存放在内存中。`compress` 和 `decompress` 函数接收一个子节序列作为参数，同时返回一个子节序列，下面就是示例：

```python
import zlib
import binascii

original_data = b'This is the original text.'
print('Original     :', len(original_data), original_data)

compressed = zlib.compress(original_data)
print('Compressed   :', len(compressed),
      binascii.hexlify(compressed))

decompressed = zlib.decompress(compressed)
print('Decompressed :', len(decompressed), decompressed)

# output
Original     : 26 b'This is the original text.'
Compressed   : 32 b'789c0bc9c82c5600a2928c5485fca2ccf4ccbcc41c8592d48a123d007f2f097e'
Decompressed : 26 b'This is the original text.'
```

上面的例子可以看出，对于少量数据的压缩比未压缩要大。因此实际的压缩结结果依赖于输入数据。下面的例子通过高亮输出 “*” 来突出显示哪些行的压缩数据比未压缩版本还会占用内存：

```python
import zlib

original_data = b'This is the original text.'

template = '{:>15}  {:>15}'
print(template.format('len(data)', 'len(compressed)'))
print(template.format('-' * 15, '-' * 15))

for i in range(5):
    data = original_data * i
    compressed = zlib.compress(data)
    highlight = '*' if len(data) < len(compressed) else ''		# 增强高亮表示
    print(template.format(len(data), len(compressed)), highlight)
    
# output
      len(data)  len(compressed)
---------------  ---------------
              0                8 *
             26               32 *
             52               35
             78               35
            104               36
```

`zlib` 支持几种不同的压缩级别，允许在计算成本和压缩空间之间取得平衡。默认压缩级别 `zlib.Z_DEFAULT_COMPRESSION` 为 `-1`，硬编码值对应于性能和压缩效果之间折衷。这当前对应于级别 `6`。等级 0 表示不压缩，等级 9 需要大量运行以产生最小的输出结果。下面的结果将说明给定的输入数据，在不同的等级情况下，可能得到同样的压缩数据量：

```python
import zlib

input_data = b'Some repeated text.\n' * 1024
template = '{:>5}  {:>5}'

print(template.format('Level', 'Size'))
print(template.format('-----', '----'))

for i in range(0, 10):
    data = zlib.compress(input_data, i)
    print(template.format(i, len(data)))
    
# output
Level   Size
-----   ----
    0  20491
    1    172
    2    172
    3    172
    4     98
    5     98
    6     98
    7     98
    8     98
    9     98
```

### 1.2 增量压缩和解压

上面的内存中压缩方法存在一些缺点，主要是系统需要足够的内存，能够在内存中同时驻留未压缩和压缩版本，这样在真实世界的情况并不实用。因此需要采取另一种方法使用 `Compress` 和 `Decompress` 对象以增量方式处理数据，这样就不需要将整个数据集放在内存中。下面的例子中从一个纯文本文件读取小数据块，并传至 `compress` 函数。压缩器维护压缩数据的一个内部缓冲区。由于压缩算法依赖于校验和以及最小块大小，所以压缩器每次接收更多输入时可能并没有准备好返回数据。如果它没有准备好一个完整的压缩快，就会返回一个空串。所有数据都已输入时，`flush` 方法会强制压缩器结束最后一个快，并返回余下的压缩数据。

```python
import zlib
import binascii

compressor = zlib.compressobj(1)

with open('lorem.txt', 'rb') as input:
    while True:
        block = input.read(64)
        if not block:
            break
        compressed = compressor.compress(block)
        if compressed:
            print('Compressed: {}'.format(
                binascii.hexlify(compressed)))
        else:
            print('buffering...')
    remaining = compressor.flush()
    print('Flushed: {}'.format(binascii.hexlify(remaining)))
    
# output
Compressed: b'7801'
buffering...
buffering...
buffering...
buffering...
buffering...
Flushed: b'55904b6ac4400c44f73e451da0f129b20c2110c85e696b8c40ddedd167ce1f7915025a087daa9ef4be8c07e4f21c38962e834b800647435fd3b90747b2810eb9c4bbcc13ac123bded6e4bef1c91ee40d3c6580e3ff52aad2e8cb2eb6062dad74a89ca904cbb0f2545e0db4b1f2e01955b8c511cb2ac08967d228af1447c8ec72e40c4c714116e60cdef171bb6c0feaa255dff1c507c2c4439ec9605b7e0ba9fc54bae39355cb89fd6ebe5841d673c7b7bc68a46f575a312eebd220d4b32441bdc1b36ebf0aedef3d57ea4b26dd986dd39af57dfb05d32279de'
```

### 1.3 混合内容流

如果压缩和未压缩的数据需要混合在一起，还可以使用 `decompressobj()` 方法来返回 `Decompress` 类来处理。解压缩所有数据后，unused_data 属性会包含所有没有使用的数据，下面是具体的示例：

```python
import zlib

lorem = open('lorem.txt', 'rb').read()
compressed = zlib.compress(lorem)
combined = compressed + lorem

decompressor = zlib.decompressobj()
decompressed = decompressor.decompress(combined)

decompressed_matches = decompressed == lorem
print('Decompressed matches lorem:', decompressed_matches)

unused_matches = decompressor.unused_data == lorem
print('Unused data matches lorem :', unused_matches)

# output
Decompressed matches lorem: True
Unused data matches lorem : True
```

### 1.4 校验和——`checksum`

出了压缩和解压缩函数，zlib 还包括两个函数来计算数据的校验和，分别是 `adler32()` 和 `crc32()` 。这两者都不能认为是密码安全的，它们只是用于数据完整性验证。这两个函数都取相同相同的参数，包括一个数据串和一个可选值，这个值用作为校验和的一个起点。函数返回一个 32 位有符号整数值，可以作为一个新起点参数在传回到后续的调用

```python
import zlib

data = open('lorem.txt', 'rb').read()

cksum = zlib.adler32(data)
print('Adler32: {:12d}'.format(cksum))
print('       : {:12d}'.format(zlib.adler32(data, cksum)))

cksum = zlib.crc32(data)
print('CRC-32 : {:12d}'.format(cksum))
print('       : {:12d}'.format(zlib.crc32(data, cksum)

# output
Adler32:   3542251998
       :    669447099
CRC-32 :   3038370516
       :   2870078631
```

### 1.5 压缩网络数据

下一个清单中的服务器使用流压缩器通过将压缩版本的文件写入用于与客户端通信的套接字来响应由文件名组成的请求。这里人为做了一些分块，以展示传递到 `compress()` 或 `decompress()` 的数据没有相应得到完整的压缩和未压缩输出块时，这个是一个缓冲行为。客户连接到套接字，并请求一个文件。然后循环接收压缩数据块。由于一个块可能未包含足够数据来完全解压缩，之前接受的剩余数据将与新数据结合，传递到解压缩器。解压缩数据时，会把它追加到一个缓冲区，处理循环结束时将与文件内容比较。

```python
# zlib_server.py
import zlib
import logging
import socketserver
import binascii

BLOCK_SIZE = 64


class ZlibRequestHandler(socketserver.BaseRequestHandler):

    logger = logging.getLogger('Server')

    def handle(self):
        compressor = zlib.compressobj(1)

        # Find out what file the client wants
        filename = self.request.recv(1024).decode('utf-8')
        self.logger.debug('client asked for: %r', filename)

        # Send chunks of the file as they are compressed
        with open(filename, 'rb') as input:
            while True:
                block = input.read(BLOCK_SIZE)
                if not block:
                    break
                self.logger.debug('RAW %r', block)
                compressed = compressor.compress(block)
                if compressed:
                    self.logger.debug(
                        'SENDING %r',
                        binascii.hexlify(compressed))
                    self.request.send(compressed)
                else:
                    self.logger.debug('BUFFERING')

        # Send any data being buffered by the compressor
        remaining = compressor.flush()
        while remaining:
            to_send = remaining[:BLOCK_SIZE]
            remaining = remaining[BLOCK_SIZE:]
            self.logger.debug('FLUSHING %r',
                              binascii.hexlify(to_send))
            self.request.send(to_send)
        return


if __name__ == '__main__':
    import socket
    import threading
    from io import BytesIO

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s: %(message)s',
    )
    logger = logging.getLogger('Client')

    # Set up a server, running in a separate thread
    address = ('localhost', 0)  # let the kernel assign a port
    server = socketserver.TCPServer(address, ZlibRequestHandler)
    ip, port = server.server_address  # what port was assigned?

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()

    # Connect to the server as a client
    logger.info('Contacting server on %s:%s', ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Ask for a file
    requested_file = 'lorem.txt'
    logger.debug('sending filename: %r', requested_file)
    len_sent = s.send(requested_file.encode('utf-8'))

    # Receive a response
    buffer = BytesIO()
    decompressor = zlib.decompressobj()
    while True:
        response = s.recv(BLOCK_SIZE)
        if not response:
            break
        logger.debug('READ %r', binascii.hexlify(response))

        # Include any unconsumed data when
        # feeding the decompressor.
        to_decompress = decompressor.unconsumed_tail + response
        while to_decompress:
            decompressed = decompressor.decompress(to_decompress)
            if decompressed:
                logger.debug('DECOMPRESSED %r', decompressed)
                buffer.write(decompressed)
                # Look for unconsumed data due to buffer overflow
                to_decompress = decompressor.unconsumed_tail
            else:
                logger.debug('BUFFERING')
                to_decompress = None

    # deal with data reamining inside the decompressor buffer
    remainder = decompressor.flush()
    if remainder:
        logger.debug('FLUSHED %r', remainder)
        buffer.write(remainder)

    full_response = buffer.getvalue()
    lorem = open('lorem.txt', 'rb').read()
    logger.debug('response matches file contents: %s',
                 full_response == lorem)

    # Clean up
    s.close()
    server.socket.close()
    
$ python3 zlib_server.py

Client: Contacting server on 127.0.0.1:53658
Client: sending filename: 'lorem.txt'
Server: client asked for: 'lorem.txt'
Server: RAW b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec\n'
Server: SENDING b'7801'
Server: RAW b'egestas, enim et consectetuer ullamcorper, lectusligula rutrum '
Server: BUFFERING
Server: RAW b'leo, a\nelementum elit tortor eu quam. Duis tincidunt nisi ut ant'
Server: BUFFERING
Server: RAW b'e. Nulla\nfacilisi. Sed tristique eros eu libero.Pellentesque ve'
Server: BUFFERING
Server: RAW b'l arcu. Vivamus\npurus orci, iaculis ac, suscipitsit amet, pulvi'
Client: READ b'7801'
Client: BUFFERING
Server: BUFFERING
Server: RAW b'nar eu,\nlacus.\n'
Server: BUFFERING
Server: FLUSHING b'55904b6ac4400c44f73e451da0f129b20c2110c85e696b8c40ddedd167ce1f7915025a087daa9ef4be8c07e4f21c38962e834b800647435fd3b90747b2810eb9'
Server: FLUSHING b'c4bbcc13ac123bded6e4bef1c91ee40d3c6580e3ff52aad2e8cb2eb6062dad74a89ca904cbb0f2545e0db4b1f2e01955b8c511cb2ac08967d228af1447c8ec72'
Client: READ b'55904b6ac4400c44f73e451da0f129b20c2110c85e696b8c40ddedd167ce1f7915025a087daa9ef4be8c07e4f21c38962e834b800647435fd3b90747b2810eb9'
Server: FLUSHING b'e40c4c714116e60cdef171bb6c0feaa255dff1c507c2c4439ec9605b7e0ba9fc54bae39355cb89fd6ebe5841d673c7b7bc68a46f575a312eebd220d4b32441bd'
Client: DECOMPRESSED b'Lorem ipsum dolor sit amet, consectetuer
adi'
Client: READ b'c4bbcc13ac123bded6e4bef1c91ee40d3c6580e3ff52aad2e8cb2eb6062dad74a89ca904cbb0f2545e0db4b1f2e01955b8c511cb2ac08967d228af1447c8ec72'
Client: DECOMPRESSED b'piscing elit. Donec\negestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a\nelementum elit tortor eu quam. Duis tinci'
Client: READ b'e40c4c714116e60cdef171bb6c0feaa255dff1c507c2c4439ec9605b7e0ba9fc54bae39355cb89fd6ebe5841d673c7b7bc68a46f575a312eebd220d4b32441bd'
Client: DECOMPRESSED b'dunt nisi ut ante. Nulla\nfacilisi. Sed tristique eros eu libero. Pellentesque vel arcu. Vivamus\npurus orci, iaculis ac'
Server: FLUSHING b'c1b36ebf0aedef3d57ea4b26dd986dd39af57dfb05d32279de'
Client: READ b'c1b36ebf0aedef3d57ea4b26dd986dd39af57dfb05d32279de'
Client: DECOMPRESSED b', suscipit sit amet, pulvinar eu,\nlacus.\n'
Client: response matches file contents: True
```

## 2. `gzip` ——读写 GNU Zip 文件

作用是读写 gzip 文件，它为 GNU zip 文件提供了一个了类文件的借口，它使用 zlib 来压缩和解压缩数据。

```python
"FCOMMENT", "FEXTRA", "FHCRC", "FNAME", "FTEXT", "GzipFile", "READ", "WRITE", "_GzipReader", "_PaddedFile", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_compression", "_test", "builtins", "compress", "decompress", "io", "open", "os", "struct", "sys", "time", "write32u", "zlib"
```

### 2.1 写压缩文件

模块级函数方法 `open()` 穿件类文件的类 GzipFile 的一个实例，它提供了读写数据的常用方法。如果需要将数据写至一个压缩的文件，需要使用 `wb` 模式打开文件。下面的例子中，使用来自 `io` 模块的 `TextIOWrapper` 包装了 `GzipFile`，能够将 Unicode 文本编码成适用压缩的字节。

```python
# gzip_write.py
import gzip
import io
import os

outfilename = 'example.txt.gz'
with gzip.open(outfilename, 'wb') as output:
    with io.TextIOWrapper(output, encoding='utf-8') as enc:
        enc.write('Contents of the example file go here.\n')

print(outfilename, 'contains', os.stat(outfilename).st_size,
      'bytes')
os.system('file -b --mime {}'.format(outfilename))

# output
application/x-gzip; charset=binary
example.txt.gz contains 75 bytes
```

通过传入一个不同压缩级别的参数，可以控制压缩的量——这里的压缩量值的的压缩比。其中有效的压缩级别为 0 到 9，值越小压缩越快，压缩程度越小。需要注意，压缩后数据大小变化不仅取决于压缩级别，而且还取决于输入数据

```python
import gzip
import io
import os
import hashlib


def get_hash(data):
    return hashlib.md5(data).hexdigest()


data = open('lorem.txt', 'r').read() * 1024
cksum = get_hash(data.encode('utf-8'))


print('Level  Size        Checksum')
print('-----  ----------  ---------------------------------')
print('data   {:>10}  {}'.format(len(data), cksum))

for i in range(0, 10):
    filename = 'compress-level-{}.gz'.format(i)
    with gzip.open(filename, 'wb', compresslevel=i) as output:
        with io.TextIOWrapper(output, encoding='utf-8') as enc:
            enc.write(data)
    size = os.stat(filename).st_size
    cksum = get_hash(open(filename, 'rb').read())
    print('{:>5d}  {:>10d}  {}'.format(i, size, cksum))
    
# output
Level  Size        Checksum
-----  ----------  ---------------------------------
data       754688  e4c0f9433723971563f08a458715119c
    0      754793  ced7189c324eb73a8388492a9024d391
    1        9846  5356d357f23e0d5b6d85e920929f0e43
    2        8267  8ce46bce238edc095e47e941cebad93d
    3        8227  91662517459db94a744671a6b4295b67
    4        4167  ad304e3aec585640de9f14306fb32083
    5        4167  4381a5d6dff4dd2746387f20411dcfcd
    6        4167  ef3a05112ea382abb53bc4a5bee3a52a
    7        4167  4723a253d1dc8ddecd4ff7b7adf0bc0b
    8        4167  0e1aeba7bdc39f0007039f130d9a28b2
    9        4167  eccf47c4c4f1cca3274e57a1b9b9ddd2
```

GzipFile 实例还包括一个 `writelines()` 方法，可以用来写一个字符串序列，其与常规文件一样，输入行要包含一个换行符。

```python
import gzip
import io
import itertools
import os

with gzip.open('example_lines.txt.gz', 'wb') as output:
    with io.TextIOWrapper(output, encoding='utf-8') as enc:
        enc.writelines(
            itertools.repeat('The same line, over and over.\n',
                             10)
        )

os.system('gzcat example_lines.txt.gz')


# output
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
```

### 2.2 读压缩数据

从压缩的数据读取回数据，可以使用二进制读模式（`rb`）打开文件，这样可以避免对航尾结束字符完成基于文本的转换。读文件时，还可以用 `seek`进行定位，只读取部分数据。这个例子读取上一节中 `gzip_write.py` 写的文件，在解压缩后使用`TextIOWrapper` 解码文本。

```python
import gzip
import io

with gzip.open('example.txt.gz', 'rb') as input_file:
    with io.TextIOWrapper(input_file, encoding='utf-8') as dec:
        print(dec.read())
        
# output
Contents of the example file go here.


# 下面的例子是使用 seek 来定位文件
import gzip

with gzip.open('example.txt.gz', 'rb') as input_file:
    print('Entire file:')
    all_data = input_file.read()
    print(all_data)

    expected = all_data[5:15]

    # rewind to beginning
    input_file.seek(0)

    # move ahead 5 bytes
    input_file.seek(5)
    print('Starting at position 5 for 10 bytes:')
    partial = input_file.read(10)
    print(partial)

    print()
    print(expected == partial)
    
# output
Entire file:
b'Contents of the example file go here.\n'
Starting at position 5 for 10 bytes:
b'nts of the'

True
```

### 2.3 处理流

GzipFile 类可以用来包装其他类型的数据流，使它们也可以压缩。通过一个套接字或者一个现有的文件句柄传输数据时，这会很有用。另外还可以使用 BytesIO 缓冲区被用于压缩数据。使用 GzipFIle 而不是 zlib 的一个好处是 GzipFile 支持文件 API。不过，当重新读取先压缩的数据时，需要像 `read()` 显示传递一个长度数值。如果没有这个长度，会导致一个 CRC 错误，这个可能是 BytesIO 报告 EOF 之前会返回一个空字符串。当处理压缩数据流时，可以在数据前添加一个整数作为前缀，表示要读取的具体数据量，或者使用 zlib 中的增量解压缩 API。

```python
import gzip
from io import BytesIO
import binascii

uncompressed_data = b'The same line, over and over.\n' * 10
print('UNCOMPRESSED:', len(uncompressed_data))
print(uncompressed_data)

buf = BytesIO()
with gzip.GzipFile(mode='wb', fileobj=buf) as f:
    f.write(uncompressed_data)

compressed_data = buf.getvalue()
print('COMPRESSED:', len(compressed_data))
print(binascii.hexlify(compressed_data))

inbuffer = BytesIO(compressed_data)
with gzip.GzipFile(mode='rb', fileobj=inbuffer) as f:
    reread_data = f.read(len(uncompressed_data))

print('\nREREAD:', len(reread_data))
print(reread_data)


# output
UNCOMPRESSED: 300
b'The same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\n'
COMPRESSED: 51
b'1f8b080022caae5a02ff0bc94855284ecc4d55c8c9cc4bd551c82f4b2d5248cc4b0133f4b8424665916401d3e717802c010000'

REREAD: 300
b'The same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\nThe same line, over and over.\n'
```

## 3. `bz2`——`bzip2` 压缩

作用是完成 bzip2 压缩，`bz2` 模块是 bzip2 库的接口，用于压缩数据以进行存储或传输。提供了三种API：

- “一次性” 压缩/解压缩功能，用于操作大堆数据
- 用于处理数据流的迭代压缩/解压缩对象
- 类似文件的类，支持与未压缩文件一样的读写

```python
"BZ2Compressor", "BZ2Decompressor", "BZ2File", "RLock", "_MODE_CLOSED", "_MODE_READ", "_MODE_WRITE", "__all__", "__author__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_builtin_open", "_compression", "compress", "decompress", "io", "open", "os", "warnings"
```

### 3.1 内存中一次性操作

使用 bz2 最简单的方法是将所有压缩或解压缩的数据加载到内存中，然后使用 `compress()` 和 `decompress()` 来完成转换。压缩数据包含非 ASCII 字符，所以在打印之前需要先转换为**十六进制模式**。下面的示例中演示了用法

```python
import bz2
import binascii

original_data = b'This is the original text.'
print('Original     : {} bytes'.format(len(original_data)))
print(original_data)

print()
compressed = bz2.compress(original_data)
print('Compressed   : {} bytes'.format(len(compressed)))
hex_version = binascii.hexlify(compressed)
for i in range(len(hex_version) // 40 + 1):
    print(hex_version[i * 40:(i + 1) * 40])

print()
decompressed = bz2.decompress(compressed)
print('Decompressed : {} bytes'.format(len(decompressed)))
print(decompressed)

# output
Original     : 26 bytes
b'This is the original text.'

Compressed   : 62 bytes
b'425a683931415926535916be35a6000002938040'
b'01040022e59c402000314c000111e93d434da223'
b'028cf9e73148cae0a0d6ed7f17724538509016be'
b'35a6'

Decompressed : 26 bytes
b'This is the original text.'
```

对于短文本，压缩版本的长度可能大大超过原版本。具体的结果取决于输入数据。

```python
import bz2

original_data = b'This is the original text.'

fmt = '{:>15}  {:>15}'
print(fmt.format('len(data)', 'len(compressed)'))
print(fmt.format('-' * 15, '-' * 15))

for i in range(5):
    data = original_data * i
    compressed = bz2.compress(data)
    print(fmt.format(len(data), len(compressed)), end='')
    print('*' if len(data) < len(compressed) else '')
    
# output
      len(data)  len(compressed)
---------------  ---------------
              0               14*
             26               62*
             52               68*
             78               70
            104               72
```

### 3.2 增量压缩和解压缩

在内存中压缩的方法，存在明显缺点导致这种方法在实际中不实用。另种方法是使用 BZ2Decompressor 和 BZ2Compressor 对象来进行增量方式处理数据，从而不必对整个数据集都放在内存中。这里的例子从一个纯文本文件读取小数据块，将它传至 `compress()`。压缩器维护压缩数据的一个内部缓冲区，由于压缩算法取决于校验和以及最小块大小，所以压缩器每次接受更懂输入时可能并没有准本好返回数据。如果它没有准备好一个完整的压缩块，会返回一个空字符串。所有数据都已经输入时，`flush()` 方法将强制压缩器结束最后一个数据块，并返回雨下的压缩数据。

```python
import bz2
import binascii
import io

compressor = bz2.BZ2Compressor()

with open('lorem.txt', 'rb') as input:
    while True:
        block = input.read(64)
        if not block:
            break
        compressed = compressor.compress(block)
        if compressed:
            print('Compressed: {}'.format(
                binascii.hexlify(compressed)))
        else:
            print('buffering...')
    remaining = compressor.flush()
    print('Flushed: {}'.format(binascii.hexlify(remaining)))
    
    
# output
buffering...
buffering...
buffering...
buffering...
Flushed: b'425a6839314159265359ba83a48c000014d5800010400504052fa7fe003000ba9112793d4ca789068698a0d1a341901a0d53f4d1119a8d4c9e812d755a67c10798387682c7ca7b5a3bb75da77755eb81c1cb1ca94c4b6faf209c52a90aaa4d16a4a1b9c167a01c8d9ef32589d831e77df7a5753a398b11660e392126fc18a72a1088716cc8dedda5d489da410748531278043d70a8a131c2b8adcd6a221bdb8c7ff76b88c1d5342ee48a70a12175074918'
```

### 3.3 混合内容流

压缩和未压缩数据混合在一起的情况，使用 BZ2Decompressor 解压缩所有数据之后，unused_data 属性会包含所有未用的数据

```python
import bz2

lorem = open('lorem.txt', 'rt').read().encode('utf-8')
compressed = bz2.compress(lorem)
combined = compressed + lorem

decompressor = bz2.BZ2Decompressor()
decompressed = decompressor.decompress(combined)

decompressed_matches = decompressed == lorem
print('Decompressed matches lorem:', decompressed_matches)

unused_matches = decompressor.unused_data == lorem
print('Unused data matches lorem :', unused_matches)

# output
Decompressed matches lorem: True
Unused data matches lorem : True
```

### 3.4 写压缩文件

可以使用 BZ2File 读写 bzip2 压缩文件，使用常用的方法读写数据。当需要往压缩文件内写入数据时，先将其以 `'wb'` 模式打开。下例子中用来自 `io`  模块的  `TextIOWrapper` 包装了 `BZ2File`使其能够把 Unicode 字符编码为字节码，以适应后续的压缩过程。

```python
import bz2
import io
import os

data = 'Contents of the example file go here.\n'

with bz2.BZ2File('example.bz2', 'wb') as output:
    with io.TextIOWrapper(output, encoding='utf-8') as enc:
        enc.write(data)

os.system('file example.bz2')

# output
example.bz2: bzip2 compressed data, block size = 900k
```

同样在该模块中，通过传入一个 `compresslevel` 参数可以选择调用不同的压缩级别。该参数可取值范围为 `1` 到 `9` 的闭区间。取值越小，则压缩速度越快，压缩幅度越低。取值越大则速度越慢、幅度越大，最大值可以将文件压缩至一个上限。

```python
import bz2
import io
import os

data = open('lorem.txt', 'r', encoding='utf-8').read() * 1024
print('Input contains {} bytes'.format(
    len(data.encode('utf-8'))))

for i in range(1, 10):
    filename = 'compress-level-{}.bz2'.format(i)
    with bz2.BZ2File(filename, 'wb', compresslevel=i) as output:
        with io.TextIOWrapper(output, encoding='utf-8') as enc:
            enc.write(data)
    os.system('cksum {}'.format(filename))
    
# output
3018243926 8771 compress-level-1.bz2
1942389165 4949 compress-level-2.bz2
2596054176 3708 compress-level-3.bz2
1491394456 2705 compress-level-4.bz2
1425874420 2705 compress-level-5.bz2
2232840816 2574 compress-level-6.bz2
447681641 2394 compress-level-7.bz2
3699654768 1137 compress-level-8.bz2
3103658384 1137 compress-level-9.bz2
Input contains 754688 bytes

# 此外它还有一个 writelines 方法用于写入字符串的序列
import bz2
import io
import itertools
import os

data = 'The same line, over and over.\n'

with bz2.BZ2File('lines.bz2', 'wb') as output:
    with io.TextIOWrapper(output, encoding='utf-8') as enc:
        enc.writelines(itertools.repeat(data, 10))

os.system('bzcat lines.bz2')

# output
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
The same line, over and over.
```

### 3.5 读取压缩文件

从已经压缩的文件中读取数据，需要使用 `'rb'` 模式进行打开。它会以字符串形式从 `read()` 方法中返回。

```python
import bz2
import io

with bz2.BZ2File('example.bz2', 'rb') as input:
    with io.TextIOWrapper(input, encoding='utf-8') as dec:
        print(dec.read())
        
# output
Contents of the example file go here.

# 使用 seek
import bz2
import contextlib

with bz2.BZ2File('example.bz2', 'rb') as input:
    print('Entire file:')
    all_data = input.read()
    print(all_data)

    expected = all_data[5:15]

    # rewind to beginning
    input.seek(0)

    # move ahead 5 bytes
    input.seek(5)
    print('Starting at position 5 for 10 bytes:')
    partial = input.read(10)
    print(partial)

    print()
    print(expected == partial)
    
# output
Entire file:
b'Contents of the example file go here.\n'
Starting at position 5 for 10 bytes:
b'nts of the'

True
```

### 3.6 读写 Unicode 数据

前面的例子直接使用 `BZ2File` 来读写压缩文件，并使用 `io.TextIOWrapper` 来管理 Unicode 文本的编解码，必要时使用 `bz2.open()` 来避免这些额外的步骤，可以通过设置 `io.TextIOWrapper` 来自动处理编码解码。`open()` 方法返回的文件句柄可以用 `seek()` 方法来移动指针，但务必小心，因为这移动的是 *字节* 而不是 *字符*，而且有可能会被移动到一个字符的中间

```python
import bz2
import os

data = 'Character with an åccent.'

with bz2.open('example.bz2', 'wt', encoding='utf-8') as output:
    output.write(data)

with bz2.open('example.bz2', 'rt', encoding='utf-8') as input:
    print('Full file: {}'.format(input.read()))

# Move to the beginning of the accented character.
with bz2.open('example.bz2', 'rt', encoding='utf-8') as input:
    input.seek(18)
    print('One character: {}'.format(input.read(1)))

# Move to the middle of the accented character.
with bz2.open('example.bz2', 'rt', encoding='utf-8') as input:
    input.seek(19)
    try:
        print(input.read(1))
    except UnicodeDecodeError:
        print('ERROR: failed to decode')
        
# output
Full file: Character with an åccent.
One character: å
ERROR: failed to decode
```



## 参考

- <http://www.zlib.net/> – Home page for zlib library.
- <http://www.zlib.net/manual.html> – Complete zlib documentation