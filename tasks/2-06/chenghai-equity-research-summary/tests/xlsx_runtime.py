"""Small OOXML adapter for benchmark runtime, preserving authored template styles.

The authoring pipeline creates templates with artifact-tool. This dependency-free
runtime helper fills those templates inside offline Linux task environments.
"""
import zipfile
import xml.etree.ElementTree as E

NS='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
E.register_namespace('',NS)


def fill_xlsx(template,target,values,formulas=None):
    formulas=formulas or {}
    with zipfile.ZipFile(template) as src,zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            raw=src.read(info.filename)
            if info.filename=='xl/worksheets/sheet1.xml':
                root=E.fromstring(raw); data=root.find('{'+NS+'}sheetData')
                for addr,val in values.items():
                    rownum=''.join(c for c in addr if c.isdigit())
                    row=next((r for r in data if r.attrib.get('r')==rownum),None)
                    if row is None:row=E.SubElement(data,'{'+NS+'}row',{'r':rownum})
                    cell=next((c for c in row if c.attrib.get('r')==addr),None)
                    if cell is None:cell=E.SubElement(row,'{'+NS+'}c',{'r':addr})
                    for child in list(cell):cell.remove(child)
                    cell.attrib.pop('t',None)
                    if addr in formulas:
                        E.SubElement(cell,'{'+NS+'}f').text=formulas[addr].lstrip('=')
                        E.SubElement(cell,'{'+NS+'}v').text=str(val)
                    elif isinstance(val,bool):
                        cell.set('t','b');E.SubElement(cell,'{'+NS+'}v').text='1' if val else '0'
                    elif isinstance(val,(int,float)):
                        E.SubElement(cell,'{'+NS+'}v').text=str(val)
                    else:
                        cell.set('t','inlineStr');s=E.SubElement(cell,'{'+NS+'}is');E.SubElement(s,'{'+NS+'}t').text=str(val)
                for row in data:row[:]=sorted(row,key=lambda c:col_index(c.attrib['r']))
                data[:]=sorted(data,key=lambda r:int(r.attrib['r']))
                raw=E.tostring(root,encoding='utf-8',xml_declaration=True)
            dst.writestr(info,raw)


def col_index(addr):
    n=0
    for c in addr:
        if c.isalpha():n=n*26+ord(c.upper())-64
    return n


def read_xlsx(path):
    with zipfile.ZipFile(path) as z:
        shared=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            for si in E.fromstring(z.read('xl/sharedStrings.xml')):
                shared.append(''.join(n.text or '' for n in si.iter('{'+NS+'}t')))
        out={};formulas={}
        root=E.fromstring(z.read('xl/worksheets/sheet1.xml'))
        for c in root.iter('{'+NS+'}c'):
            address=c.attrib['r'];t=c.attrib.get('t');v=c.find('{'+NS+'}v');f=c.find('{'+NS+'}f')
            if f is not None:formulas[address]=f.text
            if t=='inlineStr':val=''.join(n.text or '' for n in c.iter('{'+NS+'}t'))
            elif v is None or v.text is None:val=None
            elif t=='s':val=shared[int(v.text)]
            elif t=='b':val=v.text=='1'
            elif t in ['str','e']:val=v.text
            else:
                try:val=float(v.text)
                except ValueError:val=v.text
            out[address]=val
        return out,formulas
