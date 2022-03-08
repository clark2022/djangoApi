import redis

pool = redis.ConnectionPool(host='47.102.133.25', port=6379,password='@Sum1990')

r = redis.Redis(connection_pool=pool)
r.set('foo', 'Bar')
print(r.get('foo'))

