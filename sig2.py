dicts = [
    {"name":"CVE-2017-7866", "vuln":r"""static int decode_zbuf(AVBPrint *bp, const uint8_t *data,""", "patch":r"""av_bprint_get_buffer(bp, 2, &buf, &buf_size);"""}
]