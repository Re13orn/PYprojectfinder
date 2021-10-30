import time
import os
import sqlite3


def get_urlpath_fromdb():
    urllist = []
    conn = sqlite3.connect('data/main.db')
    c = conn.cursor()
    flag = c.execute("SELECT URL from HTTPX_TABLE where NUCLEIFLAG=0")
    for row in flag:
        urllist.append(row[0])

    timetxt = str(time.strftime("%Y%m%d_%H%M%S"))
    httpxurlscanpath = "report/txt/httpx_{}.txt".format(timetxt)
    sqlnucleiflag = "UPDATE HTTPX_TABLE set NUCLEIFLAG = ? where URL = ?"


    with open(httpxurlscanpath,"w") as f:
        for url in urllist:
            dosqlnucleiflag = c.execute(sqlnucleiflag,(1,url))
            f.write(url+"\n")

    conn.commit()
    conn.close()
    return httpxurlscanpath

def flagnucleisacn(scantime,httpxurlpath,necleiresultpath):
    conn = sqlite3.connect('data/main.db')
    c = conn.cursor()

    sql = "INSERT INTO NUCLEI_TABLE (SCANTIME,HTTPXURLPATH,NECLEIRESULTPATH,NUCLEIFLAG) VALUES (?,?,?,?)"
    c.execute(sql,(scantime,httpxurlpath,necleiresultpath,1))
    conn.commit()
    conn.close()


def nuclei(httpxurlpath):

    scantime = str(time.strftime("%Y%m%d_%H%M%S"))
    necleiresultpath = "report/txt/neclei_{}.txt".format(scantime)
    nuclei_com = "cat {} | nuclei -o {}".format(httpxurlpath, necleiresultpath)
    flagnucleisacn(scantime, httpxurlpath, necleiresultpath)
    os.system(nuclei_com)


def main():

    httpxurlpath = get_urlpath_fromdb()
    nuclei(httpxurlpath)


if __name__ == '__main__':
    main()