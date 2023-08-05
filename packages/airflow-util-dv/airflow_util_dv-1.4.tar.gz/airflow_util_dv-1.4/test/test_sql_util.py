import time

from airflow_util_dv.sql_util import AirflowUtil


# def spool_csv(self, spool_path, data_path, data_type, sql_name, conn, daily_conn, system_type, database, ods_conn):


if __name__ == '__main__':
    airflow_util_dv = AirflowUtil()
    print(time.strftime('%Y.%m.%d %T', time.localtime(time.time())))

    airflow_util_dv.spool_csv('/Users/liuboxue/Desktop/',
                              '/Users/liuboxue/Desktop/',
                              'RTL1',
                              'test.sql',
                              'mysql/2wsx*IK<@10.20.202.184:3306/cbb',
                              '',
                              'RTL',
                              'MYSQL',
                              ''
                              )

    print(time.strftime('%Y.%m.%d %T', time.localtime(time.time())))
