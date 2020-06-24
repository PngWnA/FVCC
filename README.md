# FVCC
Find Vulnerable Code Clone

## Argv
fvcc.py sig.py dst

* fvcc.py : main pyton script.
* sig.py : lists including [vuln code, patch code]
* dst : where candidate codes are saved.

## Logic (pseudo)
```
for list in sig.py
begin
    search_list <- github_search(vuln code)
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