dicts = [
    {"name":"CVE-2018-5268", "vuln":r"""m_signature = '\0' + String() + '\0' + String() + '\0' + String("\x0cjP  \r\n\x87\n");""", "patch":r"""static const unsigned char signature_[12] = { 0, 0, 0, 0x0c, 'j', 'P', ' ', ' ', 13, 10, 0x87, 10};"""}
]