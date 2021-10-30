import time
import os
import sqlite3


def get_domain_fromdb():
    domains = []
    conn = sqlite3.connect('data/main.db')
    c = conn.cursor()
    flag = c.execute("SELECT domain from INIT_TABLE where SUBFLAGSCAN=0")

    for row in flag:
        print(row[0])
        domains.append(row[0])
    conn.close()
    return domains


def flagdomainsacn(domain,subfinderpath):
    conn = sqlite3.connect('data/main.db')
    c = conn.cursor()
    sqlflag = "UPDATE INIT_TABLE set SUBFLAGSCAN= ? where DOMAIN = ?"
    sqlpath = "UPDATE INIT_TABLE set SUBFINDERPATH= ? where DOMAIN = ?"
    flag = c.execute(sqlflag, (1, domain))
    path = c.execute(sqlpath, (subfinderpath, domain))
    conn.commit()
    conn.close()


def subfinder(domain):
    timetxt = str(time.strftime("%Y%m%d_%H%M%S"))
    subfinderpath = "report/txt/subfinder_{}_{}.txt".format(domain, timetxt)

    flagdomainsacn(domain,subfinderpath)
    subfinder_com = "subfinder -d {} -all -o {}".format(domain, subfinderpath)
    os.system(subfinder_com)


def main():
    domainlist = get_domain_fromdb()
    for domain in domainlist:
        print(domain)
        subfinder(domain)


if __name__ == '__main__':
    main()
