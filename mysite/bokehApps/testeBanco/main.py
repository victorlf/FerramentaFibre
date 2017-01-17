import sys
import sqlite3


conn = sqlite3.connect('/home/victor/db.sqlite3')

Tab1 = "Tab1"
Tab2 = "Tab2"
Tab3 = "Tab3"
Tab4 = "Tab4"
tabCount = 0
nomeTabela = ""
params = []

lines = open("/home/victor/myDatabase.sq3")
sqls = list()

for sql in lines:
    # Assim pula linhas indesejadas
    if sql.startswith("CREATE") or sql.startswith("INSERT"):
        if sql.startswith("CREATE"):
        #    cells = sql.split()
        #    #print cells
        #    for i, cell in enumerate(cells):
        #        if cell == "TABLE":
        #           cells[i+1] = nomeTabela
        #   sql = ""
        #    for cell in cells:
        #        sql += cell + " "
        #    sqls.append(sql)
            tabCount += 1
            if tabCount == 1:
                nomeTabela = Tab1
            elif tabCount == 2:
                nomeTabela = Tab2
            elif tabCount == 3:
                nomeTabela = Tab3
            elif tabCount == 4:
                nomeTabela = Tab4

        elif sql.startswith("INSERT"):
            cells = sql.split()
            # print cells
            for i, cell in enumerate(cells):
                if cell == "INTO":
                    cells[i + 1] = nomeTabela
                elif cell.startswith("VALUES"):
                    cellValue = cell.replace("VALUES", "")
                    cellValue = cellValue.replace(";", "")
                    cellValue = cellValue.replace("(", "")
                    cellValue = cellValue.replace(")", "")
                    temp = cellValue.split(",")
                    tup = ()
                    for val in temp:
                        temp2 = (val,)
                        tup = tup + temp2
                    params.append(tup)
                    cells[i] = "VALUES(?,?,?,?,?,?,?,?,?,?,?);"
            #print cells
            sql = ""
            for cell in cells:
                sql += cell + " "
            sqls.append(sql)



for sql in sqls:
    print sql

#for param in params:
#    print param
#conn.execute(sqls[0])
#conn.execute('''CREATE TABLE SENDERS (NAME TEXT PRIMARY KEY, ID INTEGER UNIQUE);''')
#conn.commit()
#conn.close()d??