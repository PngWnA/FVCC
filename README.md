# FVCC
Find Vulnerable Code Clone

(Simple searching script using github API) 

## Argv
fvcc.py token sig.py dst

* fvcc.py : main pyton script
* token : github API token
* sig.py : dicts including [meta, vuln(code), patch(code)]
* dst : where candidate codes are saved

Note that vuln(code), patch(code) are one line string.

## Logic (pseudo)
```
for dict in sig.py
begin
    search_list <- github_search(dict[vuln code])
    for result in search_list
    begin
        if (vuln code in result) and (patch code not in result)
        begin
            code <- get_full_code(result)
            save(code)
        end
    end
end
```
