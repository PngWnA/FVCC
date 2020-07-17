dicts = [
    {"name":"CVE-2018-13785", "vuln":r"""(png_ptr->width * png_ptr->channels * (png_ptr->bit_depth > 8? 2: 1)""", "patch":r"""idat_limit = PNG_UINT_31_MAX;"""}
]