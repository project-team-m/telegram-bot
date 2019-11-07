import pypyodbc

mySQLServer = ''
myDataBase = 'BDBot'

mydb = pypyodbc.connect(
  'Driver=(SQL Server);'
  'Server=' + mySQLServer + ';'
  'DataBase' + myDataBase + ';')

cursor = mydb.cursor()

Query = ("""
  SELECT
  FROM
  WHERE
""")

cursor.execute(Query)
result = cursor.fetchall()