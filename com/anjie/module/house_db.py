import sqlite3

# 标题
title = "";
# 房子请求链接
url = "";
# 房子类型
house_type = ""
# 销售类型、出租类型
sale_type = ""
# 精装修等
level = ""
# 楼层
floor_number = ""
# 房子所在地
area_name = ""
# 具体地址
addr = ""
# 联系人
user = ""
# 补充
supplement = ""
price = "";
unit = "";
def createTable():
    conn = sqlite3.connect('anjie.db');
    curs = conn.cursor();
    curs.execute('''
        CREATE TABLE  IF NOT EXISTS user_table(
          id VARCHAR(255) PRIMARY KEY,
          title VARCHAR(255),
          url VARCHAR(255),
          house_type VARCHAR(255),
          level VARCHAR(255),
          floor_number VARCHAR(255),
          title VARCHAR(255),
          title VARCHAR(255),
        )
        ''');
    # 关闭Cursor:
    curs.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()


def insertOneData():
    conn = sqlite3.connect('anjie.db');
    curs = conn.cursor();
    u = User();
    u.id = -1;
    u.name = "anjie";
    curs.execute('INSERT INTO user_table (id, name) VALUES (?, ?)', [u.id, u.name]);
    curs.close()
    # 通过rowcount获得插入的行数:
    print('插入了%d 条数据' % curs.rowcount)
    conn.commit()
    conn.close()


def insertManyData():
    conn = sqlite3.connect('anjie.db');
    curs = conn.cursor();
    u = None;
    for i in range(10):
        u = User();
        u.id = i;
        u.name = "anjie"+str(i);
        curs.execute('INSERT INTO user_table (id, name) VALUES (?, ?)', [u.id, u.name]);

    curs.close()
    # 通过rowcount获得插入的行数:
    conn.commit()
    conn.close()


def selectData():
    conn = sqlite3.connect('anjie.db');
    curs = conn.cursor();
    curs.execute('SELECT * FROM user_table');
    print(curs.fetchall())
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # createTable();
    # insertOneData()
    # insertManyData();
    # selectData();

    conn = sqlite3.connect('anjie.db');
    curs = conn.cursor();
    curs.execute('SELECT * FROM user_table');
    print(curs.fetchone())
    print(curs.fetchmany())
    print(curs.fetchmany(size=2))
    curs.arraysize=1
    print(curs.fetchmany())
    print(curs.fetchall())
    conn.commit()
    conn.close()

