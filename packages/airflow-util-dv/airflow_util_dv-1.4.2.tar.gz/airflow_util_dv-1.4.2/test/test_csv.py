import cx_Oracle
import xlrd


def get_data(xlsx_path, conn):
    r"""
        获取xslx中的名
    :return:
    """
    data = xlrd.open_workbook(xlsx_path)
    table = data.sheet_by_index(0)
    for row in range(1, table.nrows):
        table_name = table.cell(row, 0).value
        try:
            sql = "SELECT COLUMN_NAME FROM dba_tab_columns WHERE OWNER = 'K_ODS' AND TABLE_NAME='%s'" % table_name
            columns = get_result(conn, sql)
            colunm_str = ','.join(str(i[0]) for i in columns)
            result_sql = "(select " + str(colunm_str) + " from k_ods." + str(table_name) + ") minus ( select " \
                         + str(colunm_str) + " from odsb_admin." + str(table_name).replace('ODS1_', "ODSB1_") + ")"
            result = get_result(conn, result_sql)
            if len(result) > 0:
                pass
            else:
                with open(str("/Users/liuboxue/Desktop/result.txt"), mode='a', encoding='utf-8') as f:
                    f.write(str(table_name) + '\n')
                    f.close()
        except Exception as e:
            print(str(table_name))
            pass


def get_result(conn, sql):
    r"""
    get result
    :param conn:
    :param sql:
    :return:
    """
    try:
        connnection = cx_Oracle.connect(conn)
        cursor = connnection.cursor()
        sql = sql
        cursor.execute(sql)
        connnection.commit()
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(e)


if __name__ == '__main__':
    xlsx_path = '/Users/liuboxue/Desktop/ods_table.xlsx'
    conn = 'k_ods/WrnN9Szg@10.20.201.216:1521/DDMUATDB'
    get_data(xlsx_path, conn)
