from flask import Flask, jsonify
import os,psycopg2
app=Flask(__name__)
def db():return psycopg2.connect(host=os.environ['DB_HOST'],dbname=os.environ['DB_NAME'],user=os.environ['DB_USER'],password=os.environ['DB_PASSWORD'],connect_timeout=3)
@app.get('/health')
@app.get('/api/health')
def health():
 try:
  with db() as c:
   with c.cursor() as q:q.execute('SELECT count(*) FROM orders');count=q.fetchone()[0]
  return jsonify(status='healthy',orders=count,market=os.environ.get('MARKET',''))
 except Exception as e:return jsonify(status='unhealthy',error=type(e).__name__),503
@app.get('/api/orders')
def orders():
 with db() as c:
  with c.cursor() as q:q.execute('SELECT id,amount_cny FROM orders ORDER BY id');rows=q.fetchall()
 return jsonify(orders=[{'id':x[0],'amount_cny':float(x[1])} for x in rows])
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
