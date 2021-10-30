#!/usr/bin/python
import sqlite3


def getrecode():

    resultlist = []

    with open("recode.txt", "r", encoding="utf-8") as f:
        baselist = f.read().split("[")

    for i in range(1, len(baselist)):
        prolist = baselist[i].split("]\n")
        resultlist.append(prolist)

    return resultlist


def create_init_table():

    recodelist = getrecode()
    conn = sqlite3.connect('data/main.db')
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE INIT_TABLE (NAME TEXT NOT NULL,DOMAIN TEXT NOT NULL,SUBFLAGSCAN INT NOT NULL,SUBFINDERPATH TEXT NOT NULL,HTTPXFLAGSCAN INT NOT NULL,HTTPXJSONPATH TEXT NOT NULL,HTTPXCSVPATH TEXT NOT NULL,HTTPXJSONTODBFLAG INT NOT NULL);""")
    except:
        pass
    try:
        c.execute("""CREATE TABLE HTTPX_TABLE (DOMAIN TEXT NOT NULL,URL TEXT NOT NULL,TITLE TEXT NOT NULL,WEBSERVER TEXT NOT NULL,HOST TEXT NOT NULL,NUCLEIFLAG INT NOT NULL);""")
    except:
        pass

    try:
        c.execute("""CREATE TABLE NUCLEI_TABLE (SCANTIME TEXT NOT NULL,HTTPXURLPATH TEXT NOT NULL,NECLEIRESULTPATH TEXT NOT NULL,NUCLEIFLAG INT NOT NULL);""")
    except:
        pass

    for rcode in recodelist:
        name = rcode[0]
        for domain in rcode[1].rstrip().split("\n"):
            print(name,domain)

            flag = len(list(c.execute("SELECT DOMAIN from INIT_TABLE where domain='{}'".format(domain))))
            if flag:
                pass
            else:
                sql = "INSERT INTO INIT_TABLE (NAME,DOMAIN,SUBFLAGSCAN,SUBFINDERPATH,HTTPXFLAGSCAN,HTTPXJSONPATH,HTTPXCSVPATH,HTTPXJSONTODBFLAG) VALUES (?,?,?,?,?,?,?,?)"
                c.execute(sql,[name,domain,0,"NOTSCAN",0,"NOTSCAN","NOTSCAN",0])

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_init_table()