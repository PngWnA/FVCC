#API processing
import requests, json, base64


# File IO & programming utils
import os, sys, multiprocessing
from itertools import chain

# ff(filter function) : meta -> {0, 1}
def ff(meta):
    print(". ", end='', flush=True)
    if not (meta["path"].endswith(".c") or meta["path"].endswith(".cpp")):
        return False
    star = json.loads(requests.get(meta["repository"]["url"], auth=('PngWnA', meta['token'])).text)["stargazers_count"]
    if star < 50:
        return False
    return meta


# search : target code x meta* x token -> list[json*]
def search(code, filetype, language, token):
    ''' 
    [Tactics]
    First, just get total_count of searched list.
    Second, get all list at the same time using multiprocessing (each pool can get 100 lists)
    '''

    search_endpoint = "https://api.github.com/search/code"
    query = "&".join([f"q={code}+in:{filetype}+language:{language}", 'page=1', 'per_page=1'])
    payload = "?".join([search_endpoint, query])

    response = requests.get(payload, auth=('PngWnA',token))
    count = json.loads(response.text)["total_count"]

    print(f"[*] Total count : {count}")

    fragment = (count // 100) + 1

    '''
    [Implementation]
    Should implement multiprocessing later...
    This pool method does not take lambda (since lambda cannot be pickled).
    '''

    #pool = multiprocessing.Pool(fragment)
    #result = pool.map(lambda page: requests.get(payload.replace('page=1', f'page={page}'), auth=('PngWnA',token)).text, range(1, fragment + 1))

    result = []
    for i in range(1, fragment+1):
        result.append(requests.get(payload.replace('page=1', f'page={i}').replace(f'per_page={i}', 'per_page=100'), auth=('PngWnA',token)).text)
        print(f"\r[*] Got {(i/fragment)*100}% <= {payload.replace('page=1', f'page={i}').replace(f'per_page={i}', 'per_page=100')}", end="")
    print("")

    result = list(map(lambda res: json.loads(res)["items"], result))
    result = list(chain(*result))

    return result

# get_content : json[repository] x token -> full code 
def get_code(data, token):
    code_endpoint = "https://api.github.com/repos"
    repository_name = data["repository"]["full_name"]
    path = data["path"]
    payload = "/".join([code_endpoint, repository_name, "contents", path])

    response = requests.get(payload, auth=("PngWnA", token))
    try:
        encoded = json.loads(response.text)["content"]
    except:
        print(response.text)
        return -1
    decoded = base64.b64decode(encoded).decode()
    return decoded

# save_codes : meta* x code* -> source_code*
def save_codes(items, codes):
   
    for idx in range(len(codes)):
        payload = "".join([items[idx]['repository']['full_name'].replace('/', '->'), str(codes[idx])])
        open(f"{items[idx]['name']}", "w+", encoding="utf=8").write(payload)

# main : token x sig -> file*
def main(argv):
    # Core parameters
    filetype = "file"
    language = "C"
    token = open(argv[1], "r").read()
    sig = __import__(argv[2].replace(".py", ""))
    dst = argv[3]

    # Make path
    if not os.path.exists(dst):
        os.mkdir(dst)
    os.chdir(f"./{dst}") 

    # Find source code clone
    for target in sig.dicts:
        print(f"[#{sig.dicts.index(target) + 1}/#{len(sig.dicts)}]  {target['name']}")
        print(f"\t Target : {target['vuln']}")

        if not os.path.exists(target["name"]):
            os.mkdir(target["name"])

        search_list = search(target["vuln"], filetype, language, token)
        for raw in search_list:
            raw['token'] = token

        pool = multiprocessing.Pool(16)
        possible_list = pool.map(ff, search_list)
        possible_list = list(filter(lambda x: x != False, possible_list))


        print (possible_list)
        print(f"[*] Search list reduced to : {len(search_list)} -> {len(possible_list)} ({len(possible_list) * 100 / len(search_list)}%)")

        exit()

        index = 0
        for candidate in possible_list:
            index += 1
            code = get_code(candidate, token)
            print(f"\r[*] Processing #{index}/#{len(possible_list)}", end="")
            try:
                if code == -1:
                    continue
                if target["patch"] in code:
                    continue
                open(f"{target['name']}/{candidate['repository']['full_name'].replace('/', '.')}.cpp", "w").write(code)
            except Exception as e:
                print("")
                print(f"ERROR OCCURED : {e}")
                exit()
    print("")
    print(f"\r[*] Possible list recuded to  #{len(possible_list)} -> #{len(os.listdir(target['name']))} ({len(os.listdir(target['name'])) * 100 /len(possible_list)})")
    return

if __name__ == "__main__":
    main(sys.argv)