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







## 参考

- <http://www.zlib.net/> – Home page for zlib library.
- <http://www.zlib.net/manual.html> – Complete zlib documentation