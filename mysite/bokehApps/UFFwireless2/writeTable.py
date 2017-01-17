import sys
import sqlite3


#conn = sqlite3.connect('/home/victor/mysite/db.sqlite3')

def insereTabela(arquivo):
    params = []
    #medicoes = "wireless_experiment_iperf_victor"

    #lines = open("/home/victor/myDatabase.sq3")
    lines = open("/home/victor/mysite/bokehApps/UFGwireless2/banco/" + arquivo)
    tup = ()
    for line in lines:
        # Assim pula linhas indesejadas
        if line.startswith("INSERT INTO \"iperf_transfer\""):
            cells = line.split()
            # print cells
            for i, cell in enumerate(cells):
                if cell.startswith("VALUES"):
                    cellValue = cell.replace("VALUES", "")
                    cellValue = cellValue.replace(";", "")
                    cellValue = cellValue.replace("(", "")
                    cellValue = cellValue.replace(")", "")
                    temp = cellValue.split(",")
                    for val in temp:
                        temp2 = (val,)
                        tup = tup + temp2
                    params.append(tup)
                    tup = ()
                    cells[i] = "VALUES(?,?,?,?,?,?,?,?,?,?,?);"
            #print cells

    #return params

    #for param in params:
    #    print str(param)+"\n"

    conn = sqlite3.connect('/home/victor/mysite/db.sqlite3')
    sql = "INSERT INTO IPERF_TRANSFER  (OML_TUPLE_ID, OML_SENDER_ID, OML_SEQ, OML_TS_CLIENT, OML_TS_SERVER, PID, CONNECTION_ID , BEGIN_INTERVAL, END_INTERVAL, SIZE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? ,?)"
    i = 1
    for param in params:
        conn.execute(sql, param)
        print i
        i += 1
    conn.commit()
    conn.close()

# for param in params:
#     print param
