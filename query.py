
#made by -prakhar gupta

import csv, sqlite3
import pandas as pd

#Number of nodes
db = sqlite3.connect("san_jose.db")
c = db.cursor()
QUERY = '''SELECT count(*)as num from nodes;
'''
c.execute(QUERY)
node = c.fetchall()[0]
print "Number of Node",node

#Number of ways
c = db.cursor()
QUERY = '''SELECT count(*)as num from ways;
'''
c.execute(QUERY)
way = c.fetchall()[0]
print "Number of ways",way

#No of unique users
c = db.cursor()
QUERY = '''SELECT COUNT(DISTINCT(user)) from (select user from nodes UNION ALL select user from ways);

'''
c.execute(QUERY)
duser = c.fetchall()[0]
print "No of unique users",duser

#Top 10 contributers
c = db.cursor()
QUERY = '''SELECT user,count(user)  from (select user from nodes UNION ALL select user from ways)
group by user
order by  count(user) desc
limit 10;
'''
c.execute(QUERY) 
top = c.fetchall()
dt=pd.DataFrame(top)
print "Top 10 contributers"
print (dt)

#Common Fast Food Chains in San Jose
c = db.cursor()
query= '''SELECT value,COUNT(*) FROM nodes_tags WHERE value='Starbucks'or value="McDonald's" or value='Taco Bell'
or value='Subway' or value ='Burger King' group by value ;'''
c.execute(query)
row=c.fetchall()
df=pd.DataFrame(row)
print "Common Fast Food Chains in San Jose"
print (df)

#Top 5 amenities  available in San Jose
c = db.cursor()
QUERY = '''SELECT value,count(*)as num from (select value,key from nodes_tags  UNION ALL select value,key from ways_tags)
where key='amenity'
group by value
order by num desc
limit 5;
'''
c.execute(QUERY)
rows = c.fetchall()
  
d = pd.DataFrame(rows)
print "Top 5 amenities  available in San Jose "
print (d)






