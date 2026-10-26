import html, json, random, threading, time
from pathlib import Path

OUT = Path(__file__).resolve().parent / "generated_html"
OUT.mkdir(parents=True, exist_ok=True)

def make_html(filename, title, kind, events, actors, description):
    # Events are captured during the actual threaded run and embedded in the generated page.
    payload = json.dumps(events, ensure_ascii=False).replace("</", "<\\/")
    actor_payload = json.dumps(actors, ensure_ascii=False)
    page = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TITLE_PLACEHOLDER</title><style>
:root{color-scheme:dark;--bg:#0b1220;--panel:#121d30;--line:#293a53;--text:#edf4ff;--muted:#9fb0c8;--green:#42d392;--amber:#ffcc66;--red:#ff758f;--blue:#75b7ff}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at top,#172844,var(--bg) 65%);color:var(--text);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1120px;margin:auto;padding:28px 18px 50px}h1{font-size:clamp(1.6rem,4vw,2.5rem);margin:0 0 6px}.sub{color:var(--muted);max-width:850px}.top{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap}.pill{border:1px solid var(--line);border-radius:99px;padding:6px 11px;color:var(--muted);font-size:12px}.panel{background:linear-gradient(145deg,#142139,#101929);border:1px solid var(--line);border-radius:18px;padding:18px;margin-top:18px;box-shadow:0 12px 30px #0002}.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.btn{background:#203551;color:var(--text);border:1px solid #385574;border-radius:10px;padding:9px 14px;cursor:pointer;font-weight:650}.btn.primary{background:#1f7b5a;border-color:#36a77b}.btn:disabled{opacity:.45;cursor:not-allowed}input[type=range]{width:min(350px,65vw);accent-color:var(--green)}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-top:14px}.stat{padding:12px;background:#0c1626;border:1px solid var(--line);border-radius:12px}.stat small{display:block;color:var(--muted)}.stat strong{font-size:1.1rem}.actors{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-top:14px}.actor{background:#0c1626;border:1px solid var(--line);border-radius:14px;padding:14px;min-height:116px;transition:all .25s}.actor.active{border-color:var(--green);box-shadow:0 0 0 1px #42d39244,0 0 22px #42d39214}.actor.wait{border-color:var(--amber)}.actor .name{font-weight:750;font-size:1rem}.state{display:inline-block;margin-top:9px;padding:4px 8px;border-radius:99px;background:#25354b;color:var(--muted);font-size:12px}.state.eating,.state.writing,.state.reading{background:#124a38;color:#8ef0c2}.state.waiting,.state.hungry{background:#51401f;color:#ffdb8d}.state.thinking,.state.idle{background:#263c5a;color:#b8d8ff}.resource-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin-top:12px}.resource{padding:11px;border:1px solid var(--line);border-radius:10px;text-align:center;background:#0c1626}.resource.owned{border-color:var(--red);background:#351c2a}.resource.free{border-color:#386b58}.timeline{max-height:280px;overflow:auto;border:1px solid var(--line);border-radius:12px;margin-top:12px}.event{display:grid;grid-template-columns:52px 1fr;gap:10px;padding:9px 12px;border-bottom:1px solid #243249;font-size:13px}.event:last-child{border-bottom:0}.event.current{background:#1b3445}.idx{color:var(--muted);font-variant-numeric:tabular-nums}.foot{color:var(--muted);font-size:12px;margin-top:14px}code{color:#a9d3ff}
</style></head><body><main><div class="top"><div><h1>TITLE_PLACEHOLDER</h1><div class="sub">DESCRIPTION_PLACEHOLDER</div></div><span class="pill">Generated from this program's execution trace</span></div>
<div class="panel"><div class="controls"><button class="btn primary" id="play">▶ Play</button><button class="btn" id="step">Step →</button><button class="btn" id="reset">↺ Reset</button><label class="pill">Speed <input id="speed" type="range" min="1" max="10" value="5"> <span id="speedLabel">5×</span></label><span class="pill" id="counter">Event 0 / 0</span></div><input id="scrub" type="range" min="0" max="0" value="0" style="width:100%;margin-top:14px"></div>
<div class="panel"><h2 style="margin:0">Live state</h2><div id="stats" class="stats"></div><div id="actors" class="actors"></div><div id="resources" class="resource-grid"></div></div>
<div class="panel"><div class="top"><h2 style="margin:0">Execution timeline</h2><span class="pill" id="currentLabel">Ready</span></div><div id="timeline" class="timeline"></div><div class="foot">This replay uses state/event records collected while the synchronization program ran. The animation is a view of that run, not a separately scripted algorithm.</div></div>
</main><script>
const events=EVENTS_PLACEHOLDER, actors=ACTORS_PLACEHOLDER, kind='KIND_PLACEHOLDER';
let pos=0,timer=null; const $=id=>document.getElementById(id);
function stateAt(i){return events.slice(0,i+1).reduce((s,e)=>{if(e.actor && s.actors[e.actor]!==undefined)s.actors[e.actor]=e.state||e.action||s.actors[e.actor];if(e.resource && s.resources[e.resource]!==undefined)s.resources[e.resource]=e.owner||'Free';s.last=e;return s},{actors:Object.fromEntries(actors.map(a=>[a,'Idle'])),resources:kind==='dining'?Object.fromEntries(['Fork 1','Fork 2','Fork 3','Fork 4'].map(f=>[f,'Free'])):{'Shared resource':'Available'},last:null});}
function render(i){pos=Math.max(0,Math.min(events.length-1,i));const e=events[pos]||{};const s=stateAt(pos);$('counter').textContent=`Event ${events.length?pos+1:0} / ${events.length}`;$('scrub').value=pos;$('currentLabel').textContent=e.message||'Ready';
let activeReaders=Object.values(s.actors).filter(v=>v==='Reading').length;let writer=Object.values(s.actors).some(v=>v==='Writing');
$('stats').innerHTML=(kind==='dining'?[['Eating now',Object.values(s.actors).filter(v=>v==='Eating').length],['Hungry / waiting',Object.values(s.actors).filter(v=>v==='Hungry'||v==='Waiting').length],['Forks in use',Object.values(s.resources).filter(v=>v!=='Free').length]]:[['Active readers',activeReaders],['Writer active',writer?'Yes':'No'],['Shared resource',writer?'Write locked':activeReaders?'Read shared':'Available']]).map(x=>`<div class="stat"><small>${x[0]}</small><strong>${x[1]}</strong></div>`).join('');
$('actors').innerHTML=actors.map(a=>{let st=s.actors[a]||'Idle';let cls=['Eating','Reading','Writing'].includes(st.toLowerCase().replace(/^./,c=>c.toUpperCase()))?'active':(['Hungry','Waiting'].includes(st)?'wait':'');return `<div class="actor ${cls}"><div class="name">${a}</div><div class="state ${st.toLowerCase()}">${st}</div></div>`}).join('');
$('resources').innerHTML=Object.entries(s.resources).map(([r,o])=>`<div class="resource ${o==='Free'||o==='Available'?'free':'owned'}"><strong>${r}</strong><div style="color:var(--muted);font-size:12px;margin-top:4px">${o==='Free'?'Available':o==='Available'?'Available':'Held by '+o}</div></div>`).join('');
$('timeline').innerHTML=events.map((ev,j)=>`<div class="event ${j===pos?'current':''}"><span class="idx">${String(j+1).padStart(2,'0')}</span><span>${ev.message}</span></div>`).join('');let cur=$('timeline').children[pos];if(cur)cur.scrollIntoView({block:'nearest'});
$('step').disabled=pos>=events.length-1;}
function stop(){if(timer){clearTimeout(timer);timer=null}$('play').textContent='▶ Play'}function tick(){if(pos>=events.length-1){stop();return}render(pos+1);timer=setTimeout(tick,Math.max(120,1100-Number($('speed').value)*95))}
$('play').onclick=()=>{if(timer){stop()}else{if(pos>=events.length-1)render(0);$('play').textContent='❚❚ Pause';tick()}};$('step').onclick=()=>{stop();render(pos+1)};$('reset').onclick=()=>{stop();render(0)};$('scrub').oninput=e=>{stop();render(Number(e.target.value))};$('speed').oninput=e=>$('speedLabel').textContent=e.target.value+'×';$('scrub').max=Math.max(0,events.length-1);render(0);
</script></body></html>'''
    page = page.replace('TITLE_PLACEHOLDER', html.escape(title)).replace('DESCRIPTION_PLACEHOLDER', html.escape(description)).replace('EVENTS_PLACEHOLDER', payload).replace('ACTORS_PLACEHOLDER', actor_payload).replace('KIND_PLACEHOLDER', kind)
    path=OUT/filename
    path.write_text(page, encoding='utf-8')
    print(f"HTML simulation written: {path}")

def record_factory(events, lock):
    def record(message, actor=None, state=None, resource=None, owner=None, action=None):
        item={"message":message}
        if actor is not None:item["actor"]=actor
        if state is not None:item["state"]=state
        if resource is not None:item["resource"]=resource
        if owner is not None:item["owner"]=owner
        if action is not None:item["action"]=action
        with lock: events.append(item)
    return record
