import pymysql
if __name__ == '__main__':
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='lbx152913',
        db='airflow'
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = 'select * from dag'
    # sql = 'select * from userinfo where user=%s and pwd=%s' #查询
    # sql = 'select * from userinfo where user="%s" and pwd="%s"' % (user, pwd) #该方法不安全，要使用PYMYSQL模表导入。
    # sql = 'insert into userinfo (user,pwd) value (%s,%s)'  #增加
    # sql = 'update userinfo set user=%s where user=%s'  #更改
    # sql = 'delete from userinfo where user=%s and pwd=%s' #删除

    # print(sql)
    # rows = cursor.execute(sql, (user, pwd))
    # rows = cursor.executemany(sql, [('sly1', '123'), ('sly2', '123'), ('sly3', '123')])
    rows = cursor.execute(sql)
    print(rows)

    cursor.scroll(1, mode='absolute')
    print(cursor.fetchone())
    # cursor.scroll(2, mode='relative')
    print('this is fetch one...')
    print(cursor.fetchmany(2))
    print('this is fetch many....')
    print(cursor.fetchall())
    print('this is fetch all...')
    print(rows)

    conn.commit()

    cursor.close()
    conn.close()