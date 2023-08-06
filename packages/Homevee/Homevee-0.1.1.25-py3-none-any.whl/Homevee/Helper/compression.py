#!/usr/bin/python
# -*- coding: utf-8 -*-
import zlib


def compress_string(data: str) -> str:
    """
    Compresses the given data string
    :param data: the data string
    :return: the compresses string
    """
    deflate_compress = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    #zlib_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS)
    #gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)

    deflate_data = deflate_compress.compress(data) + deflate_compress.flush()
    #zlib_data = zlib_compress.compress(data) + zlib_compress.flush()
    #gzip_data = gzip_compress.compress(data) + gzip_compress.flush()

    return deflate_data

def decompress_string(data: str) -> str:
    """
    Decompresses the given compressed data string
    :param data: the compressed data string
    :return: the decompressed string
    """
    print(data)

    return zlib.decompress(data)