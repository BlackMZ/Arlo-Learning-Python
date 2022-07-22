import sqlparse

if __name__ == '__main__':
    sql = 'select id, NAME, age, address       from oms_order d where d.id = 1 order by id desc'
    # sql = 'insert into       oms_order    (\'id\') values (\'dd\')'
    # sql = 'select * rom oms_order;  '
    # sql = 'drop table drop table'
    # sql = 'delete from oms_order d where d.id = 1'
    # sql = 'create table abc (    "id" char(24));'
    # sql = 'DROP TABLE IF EXISTS "public"."db_operation_log";'
    # sql = 'DROP TABLE IF EXISTS "public"."db_operation_log";'
    # sql = 'update asset_info    set id = \'dd\'   where id = \'c\';'
    # sqlparse.split(sql)

    standard_sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
    # print(standard_sql)
    parsed_sql = sqlparse.parse(standard_sql)[0]
    tokens = parsed_sql.tokens
    for i in range(0, tokens.__len__()):
        print(tokens[i])