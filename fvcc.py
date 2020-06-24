import requests
import json
import base64
import os

# filter : code -> {0, 1}
def filter(code):
    return

# search : target code x language x token -> json[repositories]
def search(code, language, token):
    search_endpoint = "https://api.github.com/search/code"
    query = f"q={code}+in:file+language:{language}"
    payload = "?".join([search_endpoint, query])

    response = requests.get(payload, auth=('USERNAME',token))
    return json.loads(response.text)["items"]

# get_content : json[repository] -> full code 
def get_content(data, token):
    code_endpoint = "https://api.github.com/repos"
    repository_name = data["repository"]["full_name"]
    path = data["path"]
    payload = "/".join([code_endpoint, repository_name, "contents", path])

    response = requests.get(payload, auth=('USERNAME',token))
    try:
        encoded = json.loads(response.text)["content"]
    except:
        return -1
    decoded = base64.b64decode(encoded)
    return decoded.decode()

# get_contents : json* -> full code*
def get_contents(items, start, end, token):
    if end == None:
        end=len(items) - 1
    lst = []
    for item in items[start:end]:
        code = get_content(item, token)
        if code != -1:
            lst.append(code)
    return lst

# save_codes : meta* x code* -> source_code*
def save_codes(items, codes):
    if not os.path.exists("result"):
        os.mkdir("result")
    os.chdir("./result")    
    for idx in range(len(codes)):

        payload = "".join([items[idx]['repository']['full_name'].replace('/', '->'), str(codes[idx])])
        open(f"{items[idx]['name']}", "w+", encoding="utf=8").write(payload)


def main():
    # Core parameters
    filetype = "file"
    language = "C"
    code = """val = val*10 + code - '0';"""
    #code = """if (!FIELD_PICTURE && h->current_slice)"""
    token = "df53f7f74840e59bfcf76967bea5d5b379bd9fb7"
    print(f"[*] Start. \n    Target : {code}")

    # Find source code clone
    dump = search(code, language, token)
    print(f"[*] Total candidate : {len(dump)}")

    # Get full source code
    code_lists = get_contents(dump, 0, len(dump), token=token)
    print(f"[*] Done.")

    # Save candidate source codes
    print(f"[*] Saving...")
    save_codes(dump, code_lists)
    
    print(f"[*] Done.")

if __name__ == "__main__":
    main()