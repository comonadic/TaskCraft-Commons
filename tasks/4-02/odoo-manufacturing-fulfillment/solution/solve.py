"""Reference workflow, using the same XML-RPC API available to the contestant."""
import os,json,xmlrpc.client
from pathlib import Path
URL=os.environ.get('ODOO_URL','http://odoo:8069');DB='alecn';PW='admin';TAG='CN-SEED-01'
uid=xmlrpc.client.ServerProxy(URL+'/xmlrpc/2/common').authenticate(DB,'admin',PW,{})
api=xmlrpc.client.ServerProxy(URL+'/xmlrpc/2/object',allow_none=True)
def rpc(model,method,*args,**kwargs):
    try:return api.execute_kw(DB,uid,PW,model,method,list(args),kwargs)
    except xmlrpc.client.Fault as exc:
        # Some Odoo action methods return None after successfully committing.
        if 'cannot marshal None' in exc.faultString:return None
        raise
def search(model,domain,**kw):return rpc(model,'search',domain,**kw)
def read(model,ids,fields):return rpc(model,'read',ids,fields=fields)
def write(model,ids,values):return rpc(model,'write',ids,values)
def create(model,vals):return rpc(model,'create',vals)
def one(model,domain,**kw):return search(model,domain,limit=1,**kw)[0]
out=Path(os.environ.get('TASKCRAFT_ROOT','/app'))/'output';out.mkdir(parents=True,exist_ok=True)
statefile=out/'submission.json'
state=json.loads(statefile.read_text()) if statefile.exists() else {}
def save(**kwargs):
    state.update(kwargs);statefile.write_text(json.dumps(state,ensure_ascii=False,indent=2));print(list(kwargs),flush=True)

if 'products' not in state:
    cny=one('res.currency',[['name','=','CNY']],context={'active_test':False});eur=one('res.currency',[['name','=','EUR']],context={'active_test':False})
    write('res.currency',[cny,eur],{'active':True});write('res.company',[1],{'name':'青岚设备 '+TAG,'currency_id':cny})
    for curr,rate in [(cny,1),(eur,.125)]:create('res.currency.rate',{'name':'2020-01-01','currency_id':curr,'company_id':1,'rate':rate})
    accounts={code:one('account.account',[['code','=',code]]) for code in ['110100','110200','110300','110400','121000','211000']}
    income=one('account.account',[['account_type','=','income']]);expense=one('account.account',[['account_type','=','expense']]);stockjournal=one('account.journal',[['type','=','general']])
    category=create('product.category',{'name':TAG+' FIFO','property_cost_method':'fifo','property_valuation':'real_time','property_stock_journal':stockjournal,'property_stock_valuation_account_id':accounts['110100'],'property_stock_account_input_categ_id':accounts['110200'],'property_stock_account_output_categ_id':accounts['110300'],'property_stock_account_production_cost_id':accounts['110400'],'property_account_income_categ_id':income,'property_account_expense_categ_id':expense})
    products={}
    for code,cost in [('RM-A',150),('RM-B',50),('SUB',0),('KIT',0)]:
        products[code]=create('product.product',{'name':TAG+' '+code,'default_code':code,'type':'consu','is_storable':True,'tracking':'serial' if code=='KIT' else 'none','categ_id':category,'standard_price':cost,'list_price':1840 if code=='KIT' else cost,'taxes_id':[(6,0,[])],'supplier_taxes_id':[(6,0,[])]})
    supplier=create('res.partner',{'name':TAG+' 供应商','supplier_rank':1});customer=create('res.partner',{'name':TAG+' 客户','customer_rank':1})
    save(products=products,category=category,supplier=supplier,customer=customer,cny=cny,eur=eur,journal=stockjournal,expense=expense)
p=state['products']

def finish_picking(pid,quantities,serials=None):
    rpc('stock.picking','action_assign',[pid])
    moves=read('stock.move',read('stock.picking',[pid],['move_ids'])[0]['move_ids'],['product_id','product_uom_qty','move_line_ids','location_id','location_dest_id','product_uom'])
    for move in moves:
        product=move['product_id'][0];qty=quantities.get(product,0)
        if move['move_line_ids']:rpc('stock.move.line','unlink',move['move_line_ids'])
        lots=(serials or {}).get(product,[None]*int(qty))
        if lots and lots[0] is not None:
            for lot in lots:create('stock.move.line',{'move_id':move['id'],'picking_id':pid,'product_id':product,'product_uom_id':move['product_uom'][0],'location_id':move['location_id'][0],'location_dest_id':move['location_dest_id'][0],'lot_id':lot,'quantity':1,'picked':True})
        elif qty:create('stock.move.line',{'move_id':move['id'],'picking_id':pid,'product_id':product,'product_uom_id':move['product_uom'][0],'location_id':move['location_id'][0],'location_dest_id':move['location_dest_id'][0],'quantity':qty,'picked':True})
    result=rpc('stock.picking','button_validate',[pid])
    if isinstance(result,dict) and result.get('res_model')=='stock.backorder.confirmation':
        wid=create('stock.backorder.confirmation',{'pick_ids':[(6,0,[pid])]});rpc('stock.backorder.confirmation','process',[wid],context=result.get('context',{}))
    assert read('stock.picking',[pid],['state'])[0]['state']=='done',result

if 'purchase' not in state:
    po=create('purchase.order',{'partner_id':state['supplier'],'partner_ref':TAG,'currency_id':state['cny'],'order_line':[(0,0,{'product_id':p[c],'name':TAG+' '+c,'product_qty':q,'price_unit':price,'taxes_id':[(6,0,[])]}) for c,q,price in [('RM-A',10,150),('RM-B',20,50)]]})
    rpc('purchase.order','button_confirm',[po]);pid=read('purchase.order',[po],['picking_ids'])[0]['picking_ids'][0];finish_picking(pid,{p['RM-A']:2,p['RM-B']:4});save(purchase=po,receipt_first=pid)
if 'boms' not in state:
    def bom(code,parts):
        tmpl=read('product.product',[p[code]],['product_tmpl_id'])[0]['product_tmpl_id'][0]
        return create('mrp.bom',{'product_tmpl_id':tmpl,'product_id':p[code],'product_qty':1,'code':TAG+' '+code,'bom_line_ids':[(0,0,{'product_id':p[k],'product_qty':q}) for k,q in parts]})
    boms={'SUB':bom('SUB',[('RM-A',1),('RM-B',2)]),'KIT':bom('KIT',[('SUB',1),('RM-B',1)])}
    mo=create('mrp.production',{'product_id':p['SUB'],'product_qty':3,'bom_id':boms['SUB'],'origin':TAG});rpc('mrp.production','action_confirm',[mo]);snapshot=read('mrp.production',[mo],['reservation_state','components_availability_state','move_raw_ids'])[0];save(boms=boms,sub_mo=mo,shortage_snapshot=snapshot)
if 'receipt_second' not in state:
    pid=one('stock.picking',[['backorder_id','=',state['receipt_first']],['state','!=','done']]);finish_picking(pid,{p['RM-A']:8,p['RM-B']:16});save(receipt_second=pid)
if 'landed_cost' not in state:
    service=create('product.product',{'name':TAG+' 入库运输','type':'service','landed_cost_ok':True,'split_method_landed_cost':'by_current_cost_price','property_account_expense_id':state['expense']})
    lc=create('stock.landed.cost',{'picking_ids':[(6,0,[state['receipt_first'],state['receipt_second']])],'account_journal_id':state['journal'],'cost_lines':[(0,0,{'name':TAG+' 运费','product_id':service,'price_unit':1000,'split_method':'by_current_cost_price','account_id':state['expense']})]})
    rpc('stock.landed.cost','compute_landed_cost',[lc]);rpc('stock.landed.cost','button_validate',[lc]);save(landed_cost=lc)

def finish_mo(mo,qty,lot=None):
    vals={'qty_producing':qty}
    if lot:vals['lot_producing_id']=lot
    write('mrp.production',[mo],vals);rpc('mrp.production','action_assign',[mo])
    for move in read('stock.move',read('mrp.production',[mo],['move_raw_ids'])[0]['move_raw_ids'],['product_uom_qty']):write('stock.move',[move['id']],{'quantity':move['product_uom_qty'],'picked':True})
    r=rpc('mrp.production','button_mark_done',[mo]);assert read('mrp.production',[mo],['state'])[0]['state']=='done',r
if 'manufactured' not in state:
    finish_mo(state['sub_mo'],3);mos=[];lots=[]
    for i in range(1,4):
        lot=create('stock.lot',{'name':f'SSK-{i:04d}','product_id':p['KIT'],'company_id':1});mo=create('mrp.production',{'product_id':p['KIT'],'product_qty':1,'bom_id':state['boms']['KIT'],'origin':TAG});rpc('mrp.production','action_confirm',[mo]);finish_mo(mo,1,lot);mos.append(mo);lots.append(lot)
    save(manufactured=mos,lots=lots)
if 'sale' not in state:
    plist=create('product.pricelist',{'name':TAG+' EUR','currency_id':state['eur']})
    sale=create('sale.order',{'partner_id':state['customer'],'client_order_ref':TAG,'pricelist_id':plist,'order_line':[(0,0,{'product_id':p['KIT'],'name':TAG+' KIT','product_uom_qty':3,'price_unit':230,'tax_id':[(6,0,[])]})]});rpc('sale.order','action_confirm',[sale]);pid=read('sale.order',[sale],['picking_ids'])[0]['picking_ids'][0];finish_picking(pid,{p['KIT']:2},{p['KIT']:state['lots'][:2]});second=one('stock.picking',[['backorder_id','=',pid]]);finish_picking(second,{p['KIT']:1},{p['KIT']:state['lots'][2:]});save(sale=sale,delivery_first=pid,delivery_second=second)
if 'invoices' not in state:
    line=read('sale.order',[state['sale']],['order_line'])[0]['order_line'][0];invoices=[];payments=[];bank=one('account.journal',[['type','=','bank']])
    paymentline=read('account.journal',[bank],['inbound_payment_method_line_ids'])[0]['inbound_payment_method_line_ids'][0]
    outstanding=one('account.account',[['code','=','101403']]);write('account.payment.method.line',[paymentline],{'payment_account_id':outstanding})
    for qty in [2,1]:
        invoice=create('account.move',{'move_type':'out_invoice','partner_id':state['customer'],'currency_id':state['eur'],'invoice_origin':TAG,'ref':TAG,'invoice_date':'2025-01-15','invoice_line_ids':[(0,0,{'product_id':p['KIT'],'name':TAG+' KIT','quantity':qty,'price_unit':230,'tax_ids':[(6,0,[])],'sale_line_ids':[(6,0,[line])]})]});rpc('account.move','action_post',[invoice])
        context={'active_model':'account.move','active_ids':[invoice]};wiz=create('account.payment.register',{'journal_id':bank,'payment_method_line_id':paymentline,'payment_date':'2025-01-15','amount':qty*230,'currency_id':state['eur']},) if False else rpc('account.payment.register','create',{'journal_id':bank,'payment_method_line_id':paymentline,'payment_date':'2025-01-15','amount':qty*230,'currency_id':state['eur']},context=context)
        rpc('account.payment.register','action_create_payments',[wiz],context=context);invoices.append(invoice)
    save(invoices=invoices,payments=search('account.payment',[['partner_id','=',state['customer']]]))
if 'return_picking' not in state:
    context={'active_id':state['delivery_first'],'active_ids':[state['delivery_first']],'active_model':'stock.picking'}
    wizard=rpc('stock.return.picking','create',{'picking_id':state['delivery_first']},context=context)
    lines=read('stock.return.picking',[wizard],['product_return_moves'])[0]['product_return_moves']
    for line in lines:write('stock.return.picking.line',[line],{'quantity':1})
    result=rpc('stock.return.picking','action_create_returns',[wizard],context=context);pid=result['res_id'];finish_picking(pid,{p['KIT']:1},{p['KIT']:[state['lots'][1]]});save(return_picking=pid)
if 'refund' not in state:
    credit=create('account.move',{'move_type':'out_refund','partner_id':state['customer'],'currency_id':state['eur'],'invoice_origin':TAG,'ref':TAG+' 退回SSK-0002，服务费30EUR不退','invoice_date':'2025-01-16','reversed_entry_id':state['invoices'][0],'invoice_line_ids':[(0,0,{'product_id':p['KIT'],'name':TAG+' 退货扣除服务费','quantity':1,'price_unit':200,'tax_ids':[(6,0,[])]})]});rpc('account.move','action_post',[credit]);save(refund=credit)
if 'subcontract_receipt' not in state:
    partner=create('res.partner',{'name':TAG+' 校准分包商','supplier_rank':1})
    raw=create('product.product',{'name':TAG+' RM-C','default_code':'RM-C','type':'consu','is_storable':True,'categ_id':state['category'],'standard_price':20,'taxes_id':[(6,0,[])],'supplier_taxes_id':[(6,0,[])]})
    calibrated=create('product.product',{'name':TAG+' SC','default_code':'SC','type':'consu','is_storable':True,'tracking':'serial','categ_id':state['category'],'taxes_id':[(6,0,[])],'supplier_taxes_id':[(6,0,[])]})
    po=create('purchase.order',{'partner_id':state['supplier'],'partner_ref':TAG+' 分包原料','order_line':[(0,0,{'product_id':raw,'name':TAG+' RM-C','product_qty':5,'price_unit':20,'taxes_id':[(6,0,[])]})]});rpc('purchase.order','button_confirm',[po]);pid=read('purchase.order',[po],['picking_ids'])[0]['picking_ids'][0];finish_picking(pid,{raw:5})
    subloc=read('res.partner',[partner],['property_stock_subcontractor'])[0]['property_stock_subcontractor'][0];stock=one('stock.location',[['complete_name','=','WH/Stock']]);internal=one('stock.picking.type',[['code','=','internal']])
    resupply=create('stock.picking',{'picking_type_id':internal,'location_id':stock,'location_dest_id':subloc,'partner_id':partner,'origin':TAG,'move_ids':[(0,0,{'name':TAG+' 分包供料','product_id':raw,'product_uom_qty':3,'product_uom':1,'location_id':stock,'location_dest_id':subloc})]});rpc('stock.picking','action_confirm',[resupply]);finish_picking(resupply,{raw:3})
    tmpl=read('product.product',[calibrated],['product_tmpl_id'])[0]['product_tmpl_id'][0];bom=create('mrp.bom',{'product_tmpl_id':tmpl,'product_id':calibrated,'type':'subcontract','subcontractor_ids':[(6,0,[partner])],'code':TAG+' 校准分包','bom_line_ids':[(0,0,{'product_id':raw,'product_qty':1})]})
    po2=create('purchase.order',{'partner_id':partner,'partner_ref':TAG+' 分包','order_line':[(0,0,{'product_id':calibrated,'name':TAG+' SC','product_qty':3,'price_unit':50,'taxes_id':[(6,0,[])]})]});rpc('purchase.order','button_confirm',[po2]);pid2=read('purchase.order',[po2],['picking_ids'])[0]['picking_ids'][0];lots=[create('stock.lot',{'name':f'CS-{i:04d}','product_id':calibrated,'company_id':1}) for i in range(1,4)];finish_picking(pid2,{calibrated:3},{calibrated:lots});save(subcontract_receipt=pid2,subcontract_resupply=resupply,subcontract_bom=bom,subcontract_pos=[po,po2],subcontract_products={'RM-C':raw,'SC':calibrated})
if 'dropship' not in state:
    item=create('product.product',{'name':TAG+' ACC','default_code':'ACC','type':'consu','is_storable':True,'categ_id':state['category'],'taxes_id':[(6,0,[])],'supplier_taxes_id':[(6,0,[])]});dt=one('stock.picking.type',[['code','=','dropship']])
    po=create('purchase.order',{'partner_id':state['supplier'],'partner_ref':TAG+' 直运','picking_type_id':dt,'dest_address_id':state['customer'],'order_line':[(0,0,{'product_id':item,'name':TAG+' ACC','product_qty':3,'price_unit':80,'taxes_id':[(6,0,[])]})]});rpc('purchase.order','button_confirm',[po]);pid=read('purchase.order',[po],['picking_ids'])[0]['picking_ids'][0];finish_picking(pid,{item:3});save(dropship=pid,dropship_po=po,dropship_product=item)
if 'scrap' not in state:
    stock=one('stock.location',[['complete_name','=','WH/Stock']]);scraploc=one('stock.location',[['scrap_location','=',True]])
    scrap=create('stock.scrap',{'product_id':p['RM-B'],'scrap_qty':1,'product_uom_id':1,'location_id':stock,'scrap_location_id':scraploc,'origin':TAG+' 盘点报废'});rpc('stock.scrap','action_validate',[scrap])
    po=create('purchase.order',{'partner_id':state['supplier'],'partner_ref':TAG+' 报废补购','order_line':[(0,0,{'product_id':p['RM-B'],'name':TAG+' RM-B补购','product_qty':1,'price_unit':50,'taxes_id':[(6,0,[])]})]});rpc('purchase.order','button_confirm',[po]);pid=read('purchase.order',[po],['picking_ids'])[0]['picking_ids'][0];finish_picking(pid,{p['RM-B']:1});save(scrap=scrap,replacement_po=po)

def pay_and_reconcile(invoice,amount,currency):
    # Reconcile the bank's outstanding lines, so Odoo records Paid, not In Payment.
    bank=one('account.journal',[['type','=','bank']]);move=read('account.move',[invoice],['move_type','partner_id'])[0];incoming=move['move_type']=='out_invoice';method=read('account.journal',[bank],['inbound_payment_method_line_ids' if incoming else 'outbound_payment_method_line_ids'])[0]['inbound_payment_method_line_ids' if incoming else 'outbound_payment_method_line_ids'][0]
    account=one('account.account',[['code','=','101403' if incoming else '101404']]);write('account.payment.method.line',[method],{'payment_account_id':account});context={'active_model':'account.move','active_ids':[invoice]}
    residual=read('account.move',[invoice],['amount_residual'])[0]['amount_residual']
    if residual>.001:
        wiz=rpc('account.payment.register','create',{'journal_id':bank,'payment_method_line_id':method,'payment_date':'2025-01-20','amount':residual,'currency_id':currency},context=context);rpc('account.payment.register','action_create_payments',[wiz],context=context)
    payments=search('account.payment',[['partner_id','=',move['partner_id'][0]],['state','in',['in_process','paid']],['currency_id','=',currency]])
    for payment in read('account.payment',payments,['move_id']):
        if not payment['move_id']:continue
        lines=rpc('account.move.line','search_read',[['move_id','=',payment['move_id'][0]],['account_id','=',account],['reconciled','=',False]],fields=['balance','amount_currency','currency_id','partner_id'])
        for line in lines:
            bankacct=read('account.journal',[bank],['default_account_id'])[0]['default_account_id'][0];reconcilemove=create('account.move',{'move_type':'entry','journal_id':bank,'date':'2025-01-20','ref':TAG+' 银行核销','line_ids':[(0,0,{'name':TAG,'account_id':account,'partner_id':move['partner_id'][0],'currency_id':currency,'amount_currency':-line['amount_currency'],'debit':max(0,-line['balance']),'credit':max(0,line['balance'])}),(0,0,{'name':TAG,'account_id':bankacct,'currency_id':currency,'amount_currency':line['amount_currency'],'debit':max(0,line['balance']),'credit':max(0,-line['balance'])})]});rpc('account.move','action_post',[reconcilemove]);other=one('account.move.line',[['move_id','=',reconcilemove],['account_id','=',account]]);rpc('account.move.line','reconcile',[line['id'],other])
if 'vendor_bills' not in state:
    bills=[]
    for po in [state['purchase']]+state['subcontract_pos']+[state['dropship_po'],state['replacement_po']]:
        order=read('purchase.order',[po],['order_line','partner_id'])[0];lines=[]
        for line in read('purchase.order.line',order['order_line'],['product_id','product_qty','price_unit','name']):lines.append((0,0,{'product_id':line['product_id'][0],'name':line['name'],'quantity':line['product_qty'],'price_unit':line['price_unit'],'purchase_line_id':line['id'],'tax_ids':[(6,0,[])]}))
        bill=create('account.move',{'move_type':'in_invoice','partner_id':order['partner_id'][0],'invoice_date':'2025-01-18','ref':TAG,'currency_id':state['cny'],'invoice_line_ids':lines});rpc('account.move','action_post',[bill]);pay_and_reconcile(bill,0,state['cny']);bills.append(bill)
    freight=create('account.move',{'move_type':'in_invoice','partner_id':state['supplier'],'invoice_date':'2025-01-18','ref':TAG+' 运费','currency_id':state['cny'],'invoice_line_ids':[(0,0,{'name':TAG+' 运费','account_id':state['expense'],'quantity':1,'price_unit':1000,'tax_ids':[(6,0,[])]})]});rpc('account.move','action_post',[freight]);pay_and_reconcile(freight,1000,state['cny']);bills.append(freight)
    for invoice in state['invoices']+[state['refund']]:pay_and_reconcile(invoice,0,state['eur'])
    save(vendor_bills=bills)
if 'expense_sheet' not in state:
    groups=search('res.groups',[['name','in',['Analytic Accounting','Show Full Accounting Features']]])
    write('res.users',[uid],{'groups_id':[(4,x) for x in groups]})
    employee=create('hr.employee',{'name':TAG+' 合成员工'});plan=create('account.analytic.plan',{'name':TAG+' 项目'});analytic=create('account.analytic.account',{'name':TAG,'plan_id':plan});product=create('product.product',{'name':TAG+' 差旅报销','type':'service','can_be_expensed':True,'property_account_expense_id':state['expense'],'supplier_taxes_id':[(6,0,[])]})
    bank=one('account.journal',[['type','=','bank']]);method=read('account.journal',[bank],['outbound_payment_method_line_ids'])[0]['outbound_payment_method_line_ids'][0]
    expense=create('hr.expense',{'name':TAG+' 苏州差旅','employee_id':employee,'product_id':product,'total_amount_currency':123.45,'currency_id':state['cny'],'payment_mode':'company_account','analytic_distribution':{str(analytic):100},'tax_ids':[(6,0,[])]})
    sheet=create('hr.expense.sheet',{'name':TAG+' 报销单','employee_id':employee,'expense_line_ids':[(6,0,[expense])],'payment_method_line_id':method});rpc('hr.expense.sheet','action_submit_sheet',[sheet]);rpc('hr.expense.sheet','action_approve_expense_sheets',[sheet]);rpc('hr.expense.sheet','action_sheet_move_post',[sheet]);save(expense_sheet=sheet,expense=expense,analytic=analytic)
(out/'workflow_report.md').write_text('# 合成业务执行报告\n\n已在原生Odoo以FIFO自动估值完成两次收货、两级BOM、缺料后补货、序列制造、2+1交付、EUR收款、退货与部分退款。缺料快照：'+json.dumps(state['shortage_snapshot'],ensure_ascii=False)+'。\n运输成本1000元已在两次采购入库上按当前成本比例60%/40%分摊，A600、B400；运费在制造前入账。退款200EUR与退回SSK-0002对应，30EUR服务费未退。另完成真实分包供料和CS序列收货、供应商直运、1件B报废和补购、6张供应商发票、银行核销和带项目分摊的差旅。凭证和数量以数据库为准。\n')
print('WORKFLOW COMPLETE',flush=True)
