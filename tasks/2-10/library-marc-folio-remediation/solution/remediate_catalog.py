import argparse,csv,json,unicodedata,xml.etree.ElementTree as E
from pathlib import Path
def run(case,out):
 out.mkdir(parents=True,exist_ok=True);tree=E.parse(case/'records.xml');root=tree.getroot();authority=json.loads((case/'authority.json').read_text());matches=json.loads((case/'folio_matches.json').read_text());policy=json.loads((case/'policy.json').read_text());decisions=[];changes=[];plans=[]
 for record in root.findall('record'):
  rid=record.find("controlfield[@tag='001']").text;edits=[]
  def field(tag,code):return record.find(f"datafield[@tag='{tag}']/subfield[@code='{code}']")
  title=field('245','a');new=unicodedata.normalize('NFKC',title.text).strip().rstrip('/').strip()
  if new!=title.text:title.text=new;edits.append('title')
  lang=field('041','a')
  if lang.text=='chi':lang.text='zho';edits.append('language')
  author=field('100','a')
  if author.text in authority:author.text=authority[author.text];edits.append('authority')
  isbn=field('020','a');new=isbn.text.replace('-','').replace(' ','')
  if isbn.text!=new:isbn.text=new;edits.append('isbn')
  link=field('856','u')
  if link.text.startswith('http://'):link.text='https://'+link.text[7:];edits.append('url')
  branch=field('949','a').text;ms=matches.get(isbn.text,[])
  decision='quarantine' if branch not in policy['valid_branches'] else 'review' if len(ms)>1 else 'create' if not ms else 'skip_protected' if ms[0]['protected'] else 'overlay'
  target=ms[0]['instance_id'] if len(ms)==1 else ''
  decisions.append({'record_id':rid,'decision':decision,'target_instance':target});changes.append({'record_id':rid,'changes':edits});plans.append({'record_id':rid,'action':decision,'instance_id':target,'branch':branch})
 tree.write(out/'remediated_records.xml',encoding='utf-8',xml_declaration=True)
 with (out/'overlay_decisions.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['record_id','decision','target_instance']);w.writeheader();w.writerows(decisions)
 (out/'folio_import_plan.json').write_text(json.dumps(plans,ensure_ascii=False,indent=2))
 qa={'records':len(decisions),'decision_counts':{k:sum(x['decision']==k for x in decisions) for k in ['quarantine','review','create','skip_protected','overlay']},'changes':changes}
 (out/'qa_report.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));(out/'remediation_summary.md').write_text('# 编目修复摘要\n\n'+json.dumps(qa['decision_counts'],ensure_ascii=False)+'\n依据题设馆藏政策统一修复题名、语种、作者、ISBN和链接；不自动覆盖有歧义或受保护记录。')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--case-dir',type=Path,required=True);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();run(a.case_dir,a.output_dir)
