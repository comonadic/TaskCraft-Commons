import os,sys,json,xmlrpc.client
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from support import *
g=Grade();TAG='CN-SEED-01';url=os.environ.get('ODOO_URL','http://odoo:8069')
try:
    uid=xmlrpc.client.ServerProxy(url+'/xmlrpc/2/common').authenticate('alecn','admin','admin',{})
    api=xmlrpc.client.ServerProxy(url+'/xmlrpc/2/object',allow_none=True)
    def rpc(model,method,*args,**kw):return api.execute_kw('alecn',uid,'admin',model,method,list(args),kw)
    def rows(model,domain,fields):return rpc(model,'search_read',domain,fields=fields)
    products={r['default_code']:r['id'] for r in rows('product.product',[['name','ilike',TAG]],['default_code'])}
    assert {'RM-A','RM-B','SUB','KIT','RM-C','SC','ACC'}<=set(products)
    assert rows('sale.order',[['client_order_ref','=',TAG],['state','=','sale']],['name'])
    assert isinstance(read_json(OUTPUT/'submission.json'),dict)
except Exception:
    g.check('业务状态及提交入口硬门槛',1,lambda:0);g.finish();sys.exit(0)
p=products
def close(a,b):return abs(float(a)-float(b))<.01
def fifo():
    prod=rows('product.product',[['id','in',[p[x] for x in ['RM-A','RM-B','SUB','KIT']]]],['cost_method','valuation']);company=rows('res.company',[['id','=',1]],['currency_id'])[0]
    return all(x['cost_method']=='fifo' and x['valuation']=='real_time' for x in prod) and company['currency_id'][1]=='CNY'
g.check('人民币与FIFO自动估值',.05,fifo)
def landed():
    costs=rows('stock.landed.cost',[['state','=','done']],['valuation_adjustment_lines','account_move_id']);sums={p['RM-A']:0,p['RM-B']:0}
    for c in costs:
        if not c['account_move_id']:continue
        for v in rows('stock.valuation.adjustment.lines',[['id','in',c['valuation_adjustment_lines']]],['product_id','additional_landed_cost']):
            if v['product_id'][0] in sums:sums[v['product_id'][0]]+=v['additional_landed_cost']
    return close(sums[p['RM-A']],600) and close(sums[p['RM-B']],400)
g.check('实际成本分摊600/400',.1,landed)
def manufactured():
    mos=rows('mrp.production',[['origin','ilike',TAG],['state','=','done']],['product_id','product_qty','bom_id','move_raw_ids']);tot={p['SUB']:0,p['KIT']:0}
    for m in mos:
        if m['product_id'][0] in tot:tot[m['product_id'][0]]+=m['product_qty']
    return all(close(q,3) for q in tot.values()) and len(mos)>=2
g.check('两级真实制造完成',.1,manufactured)
def pickings():
    orders=rows('sale.order',[['client_order_ref','=',TAG]],['picking_ids']);picks=rows('stock.picking',[['id','in',orders[0]['picking_ids']],['state','=','done']],['backorder_id','picking_type_code','move_line_ids']);qty=[]
    for pick in picks:
        if pick['picking_type_code']=='outgoing':qty.append(sum(r['quantity'] for r in rows('stock.move.line',[['id','in',pick['move_line_ids']],['product_id','=',p['KIT']]],['quantity'])))
    return sorted(qty)==[1,2] and any(x['backorder_id'] for x in picks)
g.check('2+1实际交付与欠单',.08,pickings)
def invoices():
    inv=rows('account.move',[['invoice_origin','ilike',TAG],['move_type','=','out_invoice'],['state','=','posted']],['amount_total','currency_id','payment_state','amount_residual'])
    return all(any(close(x['amount_total'],target) and x['currency_id'][1]=='EUR' and x['payment_state']=='paid' and close(x['amount_residual'],0) for x in inv) for target in [460,230])
g.check('两张EUR发票已付款核销',.1,invoices)
def refunds():
    inv=rows('account.move',[['invoice_origin','ilike',TAG],['move_type','=','out_refund'],['state','=','posted']],['amount_total','currency_id','payment_state','reversed_entry_id'])
    return any(close(x['amount_total'],200) and x['currency_id'][1]=='EUR' and x['payment_state']=='paid' and bool(x['reversed_entry_id']) for x in inv)
g.check('200EUR已付退款及原发票关联',.07,refunds)
def stock():
    for code,expected in [('RM-A',7),('RM-B',11),('SUB',0),('KIT',1),('RM-C',2),('SC',3),('ACC',0)]:
        quants=rows('stock.quant',[['product_id','=',p[code]],['location_id.usage','=','internal']],['quantity','location_id']);total=sum(x['quantity'] for x in quants)
        if not close(total,expected):return 0
    lot=rows('stock.lot',[['name','=','SSK-0002'],['product_id','=',p['KIT']]],['id'])
    return bool(lot) and close(sum(x['quantity'] for x in rows('stock.quant',[['lot_id','=',lot[0]['id']],['location_id.complete_name','=','WH/Stock']],['quantity'])),1)
g.check('最终库存与退回序列位置',.12,stock)
def subcontract():
    lots=rows('stock.lot',[['product_id','=',p['SC']]],['name']);moves=rows('stock.move',[['product_id','=',p['RM-C']],['state','=','done']],['location_id','location_dest_id','quantity']);sub=rows('mrp.production',[['product_id','=',p['SC']],['state','=','done']],['product_qty'])
    return {x['name'] for x in lots}=={'CS-0001','CS-0002','CS-0003'} and close(sum(x['product_qty'] for x in sub),3) and any(close(x['quantity'],3) and 'Subcontract' in x['location_dest_id'][1] for x in moves)
g.check('分包供料、制造与CS序列',.09,subcontract)
def dropship():
    moves=rows('stock.move',[['product_id','=',p['ACC']],['state','=','done'],['location_id.usage','=','supplier'],['location_dest_id.usage','=','customer']],['quantity'])
    return close(sum(x['quantity'] for x in moves),3)
g.check('供应商直运3件',.05,dropship)
def scrap():
    scraps=rows('stock.scrap',[['product_id','=',p['RM-B']],['state','=','done']],['scrap_qty']);pos=rows('purchase.order',[['partner_ref','ilike',TAG+' 报废补购'],['state','=','purchase']],['order_line'])
    return close(sum(x['scrap_qty'] for x in scraps),1) and any(any(close(l['product_qty'],1) and l['product_id'][0]==p['RM-B'] for l in rows('purchase.order.line',[['id','in',o['order_line']]],['product_qty','product_id'])) for o in pos)
g.check('真实报废与额外补购',.05,scrap)
def bills():
    b=rows('account.move',[['ref','ilike',TAG],['move_type','=','in_invoice'],['state','=','posted'],['payment_state','=','paid']],['amount_total'])
    totals=[round(x['amount_total'],2) for x in b];targets=[2500,100,150,240,50,1000]
    return all(x in totals for x in targets) and len(b)>=6
g.check('六张供应商发票已付',.07,bills)
def expense():
    es=rows('hr.expense',[['name','ilike',TAG]],['total_amount','state','analytic_distribution','sheet_id'])
    return any(close(x['total_amount'],123.45) and x['state']=='done' and x['analytic_distribution'] for x in es)
g.check('差旅报销与分析账户',.07,expense)
g.check('中文操作报告与记录索引',.05,lambda:len((OUTPUT/'workflow_report.md').read_text())>100 and len(read_json(OUTPUT/'submission.json'))>=10)
g.finish()
