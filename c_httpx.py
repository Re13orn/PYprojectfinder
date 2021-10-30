import sqlite3
import json
import time
import os


def get_something_fromdb(obj,flag):
    result = []
    conn = sqlite3.connect('data/main.db')
    c = conn.cursor()
    flag = c.execute("SELECT domain,{} from INIT_TABLE where {}=0".format(obj,flag))
    for row in flag:
        result.append([row[0],row[1]])
    conn.close()
    return result

def flaghttpxsacn(domain,httpxjsonpath,httpxcsvpath):
    conn = sqlite3.connect('data/main.db')
    c = conn.cursor()
    sqlflag = "UPDATE INIT_TABLE set HTTPXFLAGSCAN= ? where DOMAIN = ?"
    sqljsonpath = "UPDATE INIT_TABLE set HTTPXJSONPATH= ? where DOMAIN = ?"
    sqlcsvpath = "UPDATE INIT_TABLE set HTTPXCSVPATH= ? where DOMAIN = ?"
    flag = c.execute(sqlflag, (1, domain))
    path = c.execute(sqljsonpath, (httpxjsonpath, domain))
    path = c.execute(sqlcsvpath, (httpxcsvpath, domain))
    conn.commit()
    conn.close()


def jsoncontenttodb(jsonfilepath):
    conn = sqlite3.connect('data/main.db')
    c = conn.cursor()
    sqlflag = "UPDATE INIT_TABLE set HTTPXJSONTODBFLAG= ? where HTTPXJSONPATH = ?"

    sql = "INSERT INTO HTTPX_TABLE (DOMAIN,URL,TITLE,WEBSERVER,HOST,NUCLEIFLAG) VALUES (?,?,?,?,?,?)"

    with open(jsonfilepath,newline='') as jsonfile:
        for line in jsonfile.readlines():
            jsd = json.loads(line)
            domain = jsd["input"]
            url = jsd["url"]
            try:
                title=jsd["title"]
            except:
                title="notitle"
            try:
                webserver = jsd["webserver"]
            except:
                webserver = "noserver"
            host = jsd["host"]

            savedb = c.execute(sql,(domain,url,title,webserver,host,0))
    sqlflagdb = c.execute(sqlflag, (1,jsonfilepath))
    conn.commit()
    conn.close()


def httpx(domain,subfinderpath):

    timetxt = str(time.strftime("%Y%m%d_%H%M%S"))
    httpx_csvpath = "report/csv/httpx_{}_{}.csv".format(domain, timetxt)
    httpx_jsonpath = "report/json/httpx_{}_{}.json".format(domain, timetxt)
    flaghttpxsacn(domain,httpx_jsonpath,httpx_csvpath)
    httpx_csv = "cat {} | httpx -csv -o {}".format(subfinderpath, httpx_csvpath)
    httpx_json = "cat {} | httpx -json -o {}".format(subfinderpath, httpx_jsonpath)

    os.system(httpx_json)
    os.system(httpx_csv)


def main():
    scriptpath = os.path.split(os.path.realpath(__file__))[0]
    domain_path_list = get_something_fromdb("SUBFINDERPATH","HTTPXFLAGSCAN")
    for domain_path in domain_path_list:
        httpx(domain_path[0],domain_path[1])

    domain_httpxjsonpath_list = get_something_fromdb("HTTPXJSONPATH","HTTPXJSONTODBFLAG")
    for domain_httpxjsonpath in domain_httpxjsonpath_list:
        jsoncontenttodb(domain_httpxjsonpath[1])


if __name__ == '__main__':
    main()