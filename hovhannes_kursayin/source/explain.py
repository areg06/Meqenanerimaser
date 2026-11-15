"""bacatrutyun.html: a from-zero explanation of task 1 (variant 13), in the same style as the other subject's explanation page.
Run:  python3 explain.py   → ../bacatrutyun.html"""
import math, os
import model as M
import calc as C
from model import S, sub, add, scl, mag, ang

P2 = M.PA_POS
v2 = C.vchain(P2); a2 = C.achain(P2)

def t(x, nd=1):
    """number for KaTeX: decimal comma, unicode minus"""
    s = f"{C.r(x, nd):.{nd}f}".replace('.', '{,}')
    return s
def h(x, nd=1):
    """number for plain text"""
    return f"{C.r(x, nd):.{nd}f}".replace('.', ',').replace('-', '−')

COL = dict(s1='#d9480f', s2='#2b8a3e', s3='#7048e8', s4='#1971c2', s5='#c2255c', muted='#555', line='#000', soft='#eef3ff')

def markers(pid):
    out = '<defs>'
    for k, c in COL.items():
        out += (f'<marker id="{pid}-{k}" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="7" markerHeight="7" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0.8 L10,5 L0,9.2 z" fill="{c}"/></marker>')
    return out + '</defs>'

def f2(v): return f'{v:.1f}'

# ---------------- figure 1: the mechanism in the thick position ----------------
def mech_svg():
    Y = lambda p: (p[0], 270 - p[1])
    P = M.POS[P2]
    A, D = S(M.A), S(M.D); B, Cc, E, S2 = (S(P[k]) for k in ('B', 'C', 'E', 'S2'))
    E0, E0p, C0, C0p = S(M.E0), S(M.E0p), S(M.C0), S(M.C0p)
    xg = D[0]
    def L(a, b, col, w=1.6, dash='', mk=None):
        a, b = Y(a), Y(b)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        m = f' marker-end="url(#m1-{mk})"' if mk else ''
        return f'<line x1="{f2(a[0])}" y1="{f2(a[1])}" x2="{f2(b[0])}" y2="{f2(b[1])}" stroke="{col}" stroke-width="{w}"{d}{m} stroke-linecap="round"/>'
    def arc(c, r, a0, a1, col, w=0.6, dash='3 2', n=40):
        pts = [Y((c[0]+r*math.cos(math.radians(a0+(a1-a0)*k/n)), c[1]+r*math.sin(math.radians(a0+(a1-a0)*k/n)))) for k in range(n+1)]
        return f'<polyline points="{" ".join(f"{f2(p[0])},{f2(p[1])}" for p in pts)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-dasharray="{dash}"/>'
    def T(p, s, size=7, col='#000', anchor='middle', weight='400', italic=False):
        p = Y(p); st = ' font-style="italic"' if italic else ''
        return f'<text x="{f2(p[0])}" y="{f2(p[1])}" font-size="{size}" fill="{col}" text-anchor="{anchor}" dominant-baseline="central" font-weight="{weight}"{st}>{s}</text>'
    def J(p, r=2.2):
        p = Y(p); return f'<circle cx="{f2(p[0])}" cy="{f2(p[1])}" r="{r}" fill="#fff" stroke="#000" stroke-width="1"/>'
    def num(p, k, col):
        q = Y(p); return (f'<circle cx="{f2(q[0])}" cy="{f2(q[1])}" r="5" fill="{col}"/>'
                          f'<text x="{f2(q[0])}" y="{f2(q[1])}" font-size="6.5" fill="#fff" text-anchor="middle" dominant-baseline="central" font-weight="700">{k}</text>')
    def ground(c, up):
        s = 1 if up else -1; q = Y(c)
        out = f'<path d="M{f2(q[0])} {f2(q[1])} L{f2(q[0]-4)} {f2(q[1]-s*7)} L{f2(q[0]+4)} {f2(q[1]-s*7)} Z" fill="#fff" stroke="#000" stroke-width="0.9"/>'
        out += f'<line x1="{f2(q[0]-7)}" y1="{f2(q[1]-s*7)}" x2="{f2(q[0]+7)}" y2="{f2(q[1]-s*7)}" stroke="#000" stroke-width="1.1"/>'
        for k in range(8):
            x = q[0]-6.5+k*1.8
            out += f'<line x1="{f2(x)}" y1="{f2(q[1]-s*7)}" x2="{f2(x-2)}" y2="{f2(q[1]-s*10)}" stroke="#000" stroke-width="0.6"/>'
        return out
    o = [f'<svg viewBox="2 0 246 258" role="img" aria-label="Մեխանիզմը {P2}-րդ դիրքում՝ օղակների համարներով">', markers('m1')]
    o.append(L((xg, E0[1]+10), (xg, E0p[1]-12), '#888', 0.7, '6 2 1 2'))             # slider guide
    o.append(T((xg+5, E0p[1]-12), 'yy', 6.5, '#555', 'start', italic=True))
    o.append(arc(D, M.CD, ang(sub(M.C0, M.D))+6, ang(sub(M.C0p, M.D))-6, '#999'))
    o.append(arc(A, M.ABS, 0, 360, '#999', n=72))
    q = [Y(D), Y(Cc), Y(E)]
    o.append(f'<polygon points="{" ".join(f"{f2(p[0])},{f2(p[1])}" for p in q)}" fill="{COL["s3"]}" fill-opacity=".09" stroke="none"/>')
    o.append(L(D, Cc, COL['s3'], 2.6)); o.append(L(D, E, COL['s3'], 0.7, '3 2'))
    o.append(L(A, B, COL['s1'], 2.8)); o.append(L(B, Cc, COL['s2'], 2.6)); o.append(L(Cc, E, COL['s4'], 2.6))
    rx = xg-3.5; o.append(L((rx, E0[1]+8), (rx, E0p[1]-8), '#000', 1.0))
    yy = E0[1]+6
    while yy > E0p[1]-8:
        o.append(L((rx, yy), (rx-3, yy-2.2), '#000', 0.5)); yy -= 3.1
    eq_ = Y(E); o.append(f'<rect x="{f2(eq_[0]-4)}" y="{f2(eq_[1]-6.5)}" width="8" height="13" fill="#fff" stroke="{COL["s5"]}" stroke-width="2"/>')
    o.append(ground(A, False)); o.append(ground(D, True))
    for p in (A, D, B, Cc, E): o.append(J(p))
    q = Y(S2); o.append(f'<circle cx="{f2(q[0])}" cy="{f2(q[1])}" r="1.8" fill="#000"/>')
    # ω1 arrow (counter-clockwise) around A
    pts = [(A[0]+11*math.cos(math.radians(a)), A[1]+11*math.sin(math.radians(a))) for a in range(130, 250, 10)]
    o.append(f'<polyline points="{" ".join(f"{f2(Y(p)[0])},{f2(Y(p)[1])}" for p in pts)}" fill="none" stroke="{COL["s1"]}" stroke-width="1.2" marker-end="url(#m1-s1)"/>')
    o.append(T(add(A, (-19, 2)), 'ω<tspan font-size="4.5" dy="1.5">1</tspan>', 7.5, COL['s1'], italic=True))
    # labels
    for p, s, d in ((A, 'A', (8, -4)), (D, 'D', (-7, 4)), (B, 'B', (4, 7)), (Cc, 'C', (-6, -5)), (E, 'E', (9, 5)), (S2, 'S₂', (0, 6))):
        o.append(T(add(p, d), s, 8, '#000', italic=True))
    for p, k, col in ((add(scl(add(A, B), 0.5), (9, 0)), 1, COL['s1']), (add(scl(add(B, Cc), 0.5), (0, -7)), 2, COL['s2']), (add(scl(add(D, Cc), 0.5), (8, 2)), 3, COL['s3']),
                      (add(scl(add(Cc, E), 0.5), (9, 0)), 4, COL['s4']), (add(E, (-17, 0)), 5, COL['s5'])):
        o.append(num(p, k, col))
    o.append(T((200, 30), f'մեխանիզմը {P2}-րդ (հաստ) դիրքում', 7, '#555'))
    o.append('</svg>')
    return ''.join(o)

# ---------------- figure 2: extreme positions ----------------
def extreme_svg():
    Y = lambda p: (p[0], 270 - p[1])
    A, D = S(M.A), S(M.D); C0, C0p, B0, B0p = (S(getattr(M, k)) for k in ('C0', 'C0p', 'B0', 'B0p'))
    def L(a, b, col, w=1.6, dash=''):
        a, b = Y(a), Y(b); d = f' stroke-dasharray="{dash}"' if dash else ''
        return f'<line x1="{f2(a[0])}" y1="{f2(a[1])}" x2="{f2(b[0])}" y2="{f2(b[1])}" stroke="{col}" stroke-width="{w}"{d} stroke-linecap="round"/>'
    def T(p, s, size=7, col='#000', anchor='middle', italic=False):
        p = Y(p); st = ' font-style="italic"' if italic else ''
        return f'<text x="{f2(p[0])}" y="{f2(p[1])}" font-size="{size}" fill="{col}" text-anchor="{anchor}" dominant-baseline="central"{st}>{s}</text>'
    def J(p, r=2):
        p = Y(p); return f'<circle cx="{f2(p[0])}" cy="{f2(p[1])}" r="{r}" fill="#fff" stroke="#000" stroke-width="1"/>'
    o = ['<svg viewBox="20 2 215 168" role="img" aria-label="Եզրային դիրքերը. ծալված և ձգված">']
    o.append(L(D, C0, '#999', 0.8, '3 2')); o.append(L(D, C0p, '#999', 0.8, '3 2'))
    # folded: B0-A-C0 (A between B0 and C0)
    o.append(L(C0, A, COL['s2'], 2.2)); o.append(L(A, B0, COL['s1'], 2.6))
    # stretched: A-B0'-C0'
    o.append(L(A, B0p, COL['s1'], 2.6)); o.append(L(B0p, C0p, COL['s2'], 2.2, '5 2'))
    for p in (A, D, C0, C0p, B0, B0p): o.append(J(p))
    for p, s, d in ((A, 'A', (2, -8)), (D, 'D', (-7, 3)), (C0, 'C₀', (7, 4)), (C0p, 'C₀′', (-8, -6)), (B0, 'B₀', (8, -4)), (B0p, 'B₀′', (0, 7))):
        o.append(T(add(p, d), s, 8, '#000', italic=True))
    o.append(T(add(scl(add(C0, A), 0.5), (4, 10)), f'AC₀ = BC − AB = {h(C.AC0)}', 7, COL['s2']))
    o.append(T(add(scl(add(C0p, A), 0.5), (0, -10)), f'AC₀′ = AB + BC = {h(C.AC0P)}', 7, COL['s2']))
    o.append('</svg>')
    return ''.join(o)

# ---------------- figure 3 / 4: plans of the thick position ----------------
def plan_svg(kind):
    if kind == 'v':
        pts = M.vplan(P2); k = 4.2; pid = 'mv'
        segs = [('p', 'b', 's1', 2.2, '', '⊥AB'), ('p', 'c', 's3', 2.2, '', '⊥CD'), ('b', 'c', 's2', 1.5, '', '⊥BC'),
                ('c', 'e', 's4', 1.5, '', '⊥CE'), ('p', 'e', 's5', 2.2, '', '∥ yy'), ('p', 's2', 's2', 1.1, '4 2', '')]
        names = dict(p='p (a, d)', b='b', c='c', e='e', s2='s₂')
        offs = dict(p=(16, -4), b=(-8, 6), c=(-7, -6), e=(9, 4), s2=(-9, 3))
        tri = []
    else:
        pts = M.aplan(P2); k = 2.5; pid = 'ma'
        segs = [('pi', 'b', 's1', 2.2, '', ''), ('b', 'n2', 's2', 1.4, '', ''), ('n2', 'c', 's2', 1.4, '', ''),
                ('pi', 'n3', 's3', 1.4, '', ''), ('n3', 'c', 's3', 1.4, '', ''), ('pi', 'c', 's3', 2.2, '', ''),
                ('c', 'n4', 's4', 1.4, '', ''), ('n4', 'e', 's4', 1.4, '', ''), ('pi', 'e', 's5', 2.2, '', ''), ('pi', 's2', 's2', 1.1, '4 2', '')]
        names = dict(pi='π (a, d)', b='b', n2='n₂', c='c', n3='n₃', e='e', n4='n₄', s2='s₂')
        offs = dict(pi=(-20, 4), b=(-8, 6), n2=(9, 6), c=(10, -1), n3=(-9, -3), e=(-8, -5), n4=(10, -3), s2=(10, 0))
        tri = [('b', 'c')]
    P = {n_: (p[0]*k, -p[1]*k) for n_, p in pts.items()}
    xs = [p[0] for p in P.values()]; ys = [p[1] for p in P.values()]
    x0, x1, y0, y1 = min(xs)-34, max(xs)+34, min(ys)-22, max(ys)+22
    o = [f'<svg viewBox="{f2(x0)} {f2(y0)} {f2(x1-x0)} {f2(y1-y0)}" style="max-width:{int((x1-x0)*1.9)}px" role="img">', markers(pid)]
    for a, b in tri:
        o.append(f'<line x1="{f2(P[a][0])}" y1="{f2(P[a][1])}" x2="{f2(P[b][0])}" y2="{f2(P[b][1])}" stroke="#999" stroke-width="0.8" stroke-dasharray="3 2"/>')
    for a, b, col, w, dash, lab in segs:
        A_, B_ = P[a], P[b]
        if math.dist(A_, B_) < 3: continue
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o.append(f'<line x1="{f2(A_[0])}" y1="{f2(A_[1])}" x2="{f2(B_[0])}" y2="{f2(B_[1])}" stroke="{COL[col]}" stroke-width="{w}"{d} marker-end="url(#{pid}-{col})"/>')
        if lab:
            mx, my = (A_[0]+B_[0])/2, (A_[1]+B_[1])/2; ux, uy = (B_[0]-A_[0]), (B_[1]-A_[1]); L_ = math.hypot(ux, uy)
            nx, ny = -uy/L_, ux/L_; rot = math.degrees(math.atan2(uy, ux))
            if rot > 90: rot -= 180
            if rot < -90: rot += 180
            o.append(f'<text x="{f2(mx+nx*6)}" y="{f2(my+ny*6)}" font-size="7" fill="#555" text-anchor="middle" dominant-baseline="central" transform="rotate({rot:.0f} {f2(mx+nx*6)} {f2(my+ny*6)})">{lab}</text>')
    for n_, p in P.items():
        o.append(f'<circle cx="{f2(p[0])}" cy="{f2(p[1])}" r="1.8" fill="#000"/>')
        dx, dy = offs[n_]
        o.append(f'<text x="{f2(p[0]+dx)}" y="{f2(p[1]+dy)}" font-size="9" text-anchor="middle" dominant-baseline="central" font-style="italic">{names[n_]}</text>')
    o.append('</svg>')
    return ''.join(o)

# ---------------- interactive rotator (end of the page) ----------------
def rotator_html():
    import json
    q = M.circ_int(M.B0, M.BCS, M.D, M.CD)
    br = 0 if math.dist(q[0], M.C0) < math.dist(q[1], M.C0) else 1
    K = dict(A=list(M.A), AB=M.ABS, BC=M.BCS, CD=M.CD, MU=M.MU, W1=M.W1, SGN=M.SGN,
             MUV=M.MUV, TH0=M.TH0, br=br, H=M.H, col=COL, P2=P2)
    return ROT_HTML.replace('ROT_CONST', json.dumps(K)).replace('@@MUVT@@', h(M.MUV, 3))

ROT_HTML = r'''
  <div class="card" id="rotor">
    <h2>Պտտիր մեխանիզմը ինքդ</h2>
    <p>Բռնիր <b>B</b> կետը և պտտիր AB մղիչը: Մղիչը փոքր է, ուստի կարող ես քաշել սխեմայի ցանկացած տեղից. մղիչը կնայի դեպի մատդ (մկնիկը), A-ի շուրջը: Կարող ես նաև սեղմել «▶ Պտտել» կամ ընտրել 0–7 դիրքերից մեկը: Աջ կողմում արագությունների պլանն է նույն պահի համար, նույն μ<sub>v</sub> = @@MUVT@@ (մ/վ)/մմ մասշտաբով: Մանուշակագույն եռանկյունը (p, c, e) միշտ հավասարասրուն է (ce = pc), իսկ pe-ն միշտ ուղղաձիգ է. ստուգիր ցանկացած դիրքում:</p>
    <div class="rot">
      <div><svg id="rotMech" class="grab" role="img" aria-label="Մեխանիզմ"></svg><p class="cap">Մեխանիզմը (ω<sub>1</sub>-ը ժամացույցի սլաքի հակառակ ուղղությամբ)</p></div>
      <div><svg id="rotPlan" role="img" aria-label="Արագությունների պլան"></svg><p class="cap">Արագությունների պլանը (p-ն՝ բևեռը)</p></div>
    </div>
    <div class="rotctl">
      <button type="button" id="rotPlay">▶ Պտտել</button>
      <label><span>φ<sub>1</sub> = <b id="rotPhiTxt">0°</b></span><input type="range" id="rotPhi" min="0" max="360" step="0.5" value="0"></label>
    </div>
    <div class="rotctl" id="rotPos"><span>Դիրք՝</span></div>
    <div class="tbl"><table id="rotTab"></table></div>
  </div>
<script>
(function(){
const K = ROT_CONST, C = K.col, A = K.A, D = [0,0], R = Math.PI/180;
const ex = id => document.getElementById(id);
const mech = ex('rotMech'), plan = ex('rotPlan');
const nf = (x, d) => x.toFixed(d).replace('.', ',').replace('-', '−');
function cint(c1, r1, c2, r2){
  const dx = c2[0]-c1[0], dy = c2[1]-c1[1], d = Math.hypot(dx, dy);
  const a = (r1*r1-r2*r2+d*d)/(2*d), h = Math.sqrt(Math.max(r1*r1-a*a, 0));
  const ux = dx/d, uy = dy/d, px = c1[0]+a*ux, py = c1[1]+a*uy;
  return [[px-h*uy, py+h*ux], [px+h*uy, py-h*ux]];
}
function pos(phi){
  const t = (K.TH0+K.SGN*phi)*R, B = [A[0]+K.AB*Math.cos(t), A[1]+K.AB*Math.sin(t)];
  const Cp = cint(B, K.BC, D, K.CD)[K.br], E = [0, 2*Cp[1]];
  return {B, C:Cp, E};
}
function kin(P){
  const r = (p, q) => [(p[0]-q[0])*K.MU, (p[1]-q[1])*K.MU], ck = (w, v) => [-w*v[1], w*v[0]];
  const rAB = r(P.B, A), rCB = r(P.C, P.B), rCD = r(P.C, D), rEC = r(P.E, P.C);
  const VB = ck(K.SGN*K.W1, rAB);
  const a11 = -rCB[1], a12 = rCD[1], a21 = rCB[0], a22 = -rCD[0], b1 = -VB[0], b2 = -VB[1], det = a11*a22-a12*a21;
  const w2 = (b1*a22-a12*b2)/det, w3 = (a11*b2-b1*a21)/det;
  const VC = ck(w3, rCD), w4 = VC[0]/rEC[1], VEC = ck(w4, rEC);
  return {VB, VC, VEC, VE:[VC[0]+VEC[0], VC[1]+VEC[1]], w2, w3, w4};
}
// fixed view boxes over a full turn
let mb = [A[0], A[0], A[1], A[1]], pm = 0;
const grow = p => { mb[0] = Math.min(mb[0], p[0]); mb[1] = Math.max(mb[1], p[0]); mb[2] = Math.min(mb[2], p[1]); mb[3] = Math.max(mb[3], p[1]); };
for (let f = 0; f < 360; f += 2){
  const P = pos(f); [D, P.B, P.C, P.E].forEach(grow);
  const V = kin(P); [V.VB, V.VC, V.VE].forEach(v => pm = Math.max(pm, Math.hypot(v[0], v[1])/K.MUV));
}
const pad = 22;
mech.setAttribute('viewBox', `${mb[0]-pad} ${-mb[3]-pad} ${mb[1]-mb[0]+2*pad} ${mb[3]-mb[2]+2*pad}`);
const pr = pm+14; plan.setAttribute('viewBox', `${-pr} ${-pr} ${2*pr} ${2*pr}`);
const defs = '<defs>' + Object.keys(C).map(k => `<marker id="rm-${k}" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0.8 L10,5 L0,9.2 z" fill="${C[k]}"/></marker>`).join('') + '</defs>';
const Y = p => [p[0], -p[1]];
const ln = (a, b, col, w, dash, arrow) => { a = Y(a); b = Y(b);
  return `<line x1="${a[0].toFixed(2)}" y1="${a[1].toFixed(2)}" x2="${b[0].toFixed(2)}" y2="${b[1].toFixed(2)}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"${dash ? ` stroke-dasharray="${dash}"` : ''}${arrow ? ` marker-end="url(#rm-${arrow})"` : ''}/>`; };
const tx = (p, s, dx, dy, sz, col) => { p = Y(p); return `<text x="${(p[0]+dx).toFixed(1)}" y="${(p[1]+dy).toFixed(1)}" font-size="${sz||9}" fill="${col||'#000'}" text-anchor="middle" dominant-baseline="central" font-style="italic">${s}</text>`; };
const dot = (p, r, fill, stroke) => { p = Y(p); return `<circle cx="${p[0].toFixed(2)}" cy="${p[1].toFixed(2)}" r="${r}" fill="${fill}" stroke="${stroke||'#000'}" stroke-width="1"/>`; };
function ground(p){ const q = Y(p); let s = `<path d="M${q[0]},${q[1]} l-7,11 h14 z" fill="#fff" stroke="#000" stroke-width="1"/>`;
  for (let i = -8; i < 8; i += 3.5) s += `<line x1="${q[0]+i}" y1="${q[1]+11}" x2="${q[0]+i-3}" y2="${q[1]+15}" stroke="#000" stroke-width=".7"/>`; return s; }
// static background of the mechanism: B circle, 8 positions, slider guide
let bg = defs;
{ const a = Y(A); bg += `<circle cx="${a[0]}" cy="${a[1]}" r="${K.AB}" fill="none" stroke="#999" stroke-width=".7" stroke-dasharray="3 2"/>`; }
for (let i = 0; i < 8; i++){ const P = pos(45*i), u = [P.B[0]-A[0], P.B[1]-A[1]], L = Math.hypot(u[0], u[1]);
  bg += dot(P.B, 1.3, '#999', '#999') + tx([A[0]+u[0]/L*(K.AB+9), A[1]+u[1]/L*(K.AB+9)], i, 0, 0, 7, '#777'); }
bg += `<line x1="-6" y1="${-mb[3]-6}" x2="-6" y2="${-mb[2]+6}" stroke="#000" stroke-width=".8"/><line x1="6" y1="${-mb[3]-6}" x2="6" y2="${-mb[2]+6}" stroke="#000" stroke-width=".8"/>`;
bg += ground(A) + ground(D);
let phi = 0, playing = false, last = 0;
const posBox = ex('rotPos');
for (let i = 0; i < 8; i++){ const b = document.createElement('button'); b.type = 'button'; b.textContent = i; b.onclick = () => { stop(); set(45*i); }; posBox.appendChild(b); }
function draw(){
  const P = pos(phi), V = kin(P);
  let s = bg;
  s += `<polygon points="${[D, P.C, P.E].map(p => Y(p).map(v => v.toFixed(2)).join(',')).join(' ')}" fill="${C.s3}" fill-opacity=".12" stroke="none"/>`;
  s += ln(D, P.C, C.s3, 3) + ln(D, P.E, C.s3, .8, '3 2');
  s += ln(P.B, P.C, C.s2, 3) + ln(P.C, P.E, C.s4, 3) + ln(A, P.B, C.s1, 3.4);
  { const f = Y(P.E); s += `<rect x="${(f[0]-5).toFixed(2)}" y="${(f[1]-8).toFixed(2)}" width="10" height="16" fill="#fff" stroke="${C.s5}" stroke-width="2"/>`; }
  s += dot(A, 2.2, '#fff') + dot(D, 2.2, '#fff') + dot(P.C, 2.2, '#fff') + dot(P.E, 2.2, '#fff');
  s += dot(P.B, 6, C.s1, '#fff');
  s += tx(A, 'A', 0, -10) + tx(D, 'D', -11, -4) + tx(P.B, 'B', 11, -9, 10, C.s1) + tx(P.C, 'C', 10, -6) + tx(P.E, 'E', 14, 0);
  mech.innerHTML = s;
  // velocity plan, plan-mm = V / mu_v
  const m = v => [v[0]/K.MUV, v[1]/K.MUV], p = [0, 0], b = m(V.VB), c = m(V.VC), e = m(V.VE);
  let q = defs + `<polygon points="${[p, c, e].map(t => Y(t).map(v => v.toFixed(2)).join(',')).join(' ')}" fill="${C.s3}" fill-opacity=".15" stroke="#999" stroke-width=".7" stroke-dasharray="3 2"/>`;
  const vec = (a, z, col, w, dash) => Math.hypot(z[0]-a[0], z[1]-a[1]) > 2.5 ? ln(a, z, C[col], w, dash, col) : '';
  q += vec(b, c, 's2', 1.6) + vec(c, e, 's4', 1.6) + vec(p, b, 's1', 2.4) + vec(p, c, 's3', 2.4) + vec(p, e, 's5', 2.4);
  q += dot(p, 2, '#000') + tx(p, 'p', -8, 6);
  [[b, 'b'], [c, 'c'], [e, 'e']].forEach(([z, n]) => { const L = Math.hypot(z[0], z[1]) || 1; q += tx(z, n, z[0]/L*8, -z[1]/L*8, 10); });
  plan.innerHTML = q;
  // numbers
  const vl = v => Math.hypot(v[0], v[1]), pc = vl(c), ce = Math.hypot(e[0]-c[0], e[1]-c[1]);
  let rat = '—'; if (pc > 0.5) rat = nf(ce/pc, 3);
  const row = (k, mm, v) => `<tr><th scope="row">${k}</th><td>${mm}</td><td>${v}</td></tr>`;
  ex('rotTab').innerHTML = '<tr><th></th><th>պլանում, մմ</th><th>իրական</th></tr>'
    + row('V<sub>B</sub>', nf(vl(b), 1), nf(vl(V.VB), 3)+' մ/վ') + row('V<sub>C</sub>', nf(pc, 1), nf(vl(V.VC), 3)+' մ/վ')
    + row('V<sub>EC</sub>', nf(ce, 1), nf(vl(V.VEC), 3)+' մ/վ')
    + row('V<sub>E</sub>', nf(vl(e), 1), nf(vl(V.VE), 3)+' մ/վ '+(V.VE[1] < -1e-6 ? '↓' : V.VE[1] > 1e-6 ? '↑' : ''))
    + row('ω<sub>3</sub> / ω<sub>4</sub>', '', nf(V.w3, 2)+' / '+nf(V.w4, 2)+' վ⁻¹') + row('ce / pc', rat, 'պետք է լինի 1,000')
    + row('pe-ի հորիզոնական բաղադրիչը', nf(e[0], 2), 'պետք է լինի 0');
  ex('rotPhiTxt').textContent = nf(phi, 1).replace(',0', '')+'°';
  ex('rotPhi').value = phi;
  posBox.querySelectorAll('button').forEach((bt, i) => bt.classList.toggle('on', Math.abs(phi-45*i) < 0.6));
}
function set(f){ phi = ((f % 360)+360) % 360; draw(); }
function stop(){ playing = false; ex('rotPlay').textContent = '▶ Պտտել'; }
function tick(t){ if (!playing) return; if (last) set(phi + (t-last)*0.045); last = t; requestAnimationFrame(tick); }
ex('rotPlay').onclick = () => { if (playing) stop(); else { playing = true; last = 0; ex('rotPlay').textContent = '⏸ Կանգնեցնել'; requestAnimationFrame(tick); } };
ex('rotPhi').oninput = ev => { stop(); set(+ev.target.value); };
let drag = false;
function pt(ev){ const s = mech.createSVGPoint(); s.x = ev.clientX; s.y = ev.clientY; const p = s.matrixTransform(mech.getScreenCTM().inverse()); return [p.x, -p.y]; }
function toPhi(ev){ const p = pt(ev); set(K.SGN*(Math.atan2(p[1]-A[1], p[0]-A[0])/R - K.TH0)); }
mech.addEventListener('pointerdown', ev => { drag = true; stop(); mech.setPointerCapture(ev.pointerId); mech.classList.add('hold'); toPhi(ev); ev.preventDefault(); });
mech.addEventListener('pointermove', ev => { if (drag) toPhi(ev); });
const up = () => { drag = false; mech.classList.remove('hold'); };
mech.addEventListener('pointerup', up); mech.addEventListener('pointercancel', up);
set(45*K.P2);
})();
</script>
'''

# ---------------- page ----------------
D_ = M.DATA
DE0P = C.r(2*M.CD*math.cos(math.radians(M.BETA))); DE0 = C.r(DE0P - M.H)
COSG = DE0/(2*C.r(M.CD)); GAM = C.r(math.degrees(math.acos(COSG)), 1)
GL = C.LAB + M.AD; GR = C.LBC + M.lCD
R = dict(
    MUL=t(M.MU, 5).rstrip('0'), L1S=t(M.L1S, 0), H=t(M.H, 1), L2S=t(M.L2S, 1), CD=t(M.CD, 1), DE0P=t(DE0P), DE0=t(DE0), DE2CD=t(2*M.CD, 1), COSG=t(COSG, 4), GAM=t(GAM),
    AC0=t(C.AC0), AC0P=t(C.AC0P), SUM=t(C.AC0+C.AC0P), BC=t(C.BC), AB=t(C.AB), LAB=t(C.LAB, 4), LBC=t(C.LBC, 4),
    PSI=t(M.PSI), PHIW=t(M.PHI_W), PHII=t(M.PHI_I), K=t(M.PHI_W/M.PHI_I, 2), GMIN=t(M.GAMMA_MIN), GL=t(GL, 4), GR=t(GR, 4), AD=t(M.AD, 4),
    W1=t(C.W1, 3), VB=t(C.VB, 3), VB4=t(C.VB4, 4), MUV=t(M.MUV, 3), MUA=t(M.MUA, 2), AB_ACC=t(C.AB_ACC, 3), PB=t(C.PB), PIB=t(C.PIB),
    pc=t(v2['pc']), bc=t(v2['bc']), ce=t(v2['ce']), pe=t(v2['pe']), ps2=t(v2['ps2']),
    VC=t(v2['VC'], 3), VCB=t(v2['VCB'], 3), VEC=t(v2['VEC'], 3), VE=t(v2['VE'], 3), VS2=t(v2['VS2'], 3),
    w2=t(v2['w2'], 2), w3=t(v2['w3'], 2), w4=t(v2['w4'], 2),
    aCBn=t(a2['aCBn'], 3), aCDn=t(a2['aCDn'], 3), aECn=t(a2['aECn'], 3), bn2=t(a2['bn2']), pin3=t(a2['pin3']), cn4=t(a2['cn4']),
    n2c=t(a2['n2c']), n3c=t(a2['n3c']), n4e=t(a2['n4e']), pic=t(a2['pic']), pie=t(a2['pie']), pis2=t(a2['pis2']),
    aCBt=t(a2['aCBt'], 3), aCDt=t(a2['aCDt'], 3), aECt=t(a2['aECt'], 3), aC=t(a2['aC'], 3), aE=t(a2['aE'], 3), aS2=t(a2['aS2'], 3),
    e2=t(a2['e2'], 1), e3=t(a2['e3'], 1), e4=t(a2['e4'], 1),
    G2=str(D_['G2']), G5=str(D_['G5']), FMAX=str(int(M.FMAX)), YMAXF=t(C.FRE_MAX_MM), MUF=t(M.MUF, 0), L1=t(M.L1, 2), HE=t(M.HE, 3), L2=t(M.L2, 3), LCD=t(M.lCD, 3),
    N1=str(D_['n1']), IS2R=str(D_['IS2']), IS2SI=t(D_['IS2']/1000, 2),
)
TXT = dict(hpc=h(v2['pc']), hVC=h(v2['VC'], 3), hpe=h(v2['pe']), hVE=h(v2['VE'], 3), hVB=h(C.VB, 3), hAB=h(C.AB), hBC=h(C.BC),
           hPSI=h(M.PSI), hGMIN=h(M.GAMMA_MIN), hW1=h(C.W1, 3), hMUV=h(M.MUV, 3), hMUA=h(M.MUA, 2), haE=h(a2['aE'], 3), hw3=h(v2['w3'], 2),
           hbn2=h(a2['bn2']), hbc=h(v2['bc']), hVCB=h(v2['VCB'], 3), hw2=h(v2['w2'], 2), hN1=str(D_['n1']), hHE=h(M.HE*1000, 0), hLCD=h(D_['lCD'], 0),
           hPB=h(C.PB), hPIB=h(C.PIB), hDE0P=h(DE0P), hGAM=h(GAM),
           hWR=f'{[i for i in range(8) if M.working(i)][0]}–{[i for i in range(8) if M.working(i)][-1]}',
           hFMAX=h(M.FMAX, 0), hFRE0=h(M.fre_shape(0.40), 2))

from mpgraph import mp_graph, PROJ_SVG
_m2 = C.MP[P2]; _m4 = C.MP[4]
JMX = max(range(9), key=lambda j: abs(C.MP[j]['M'])); _mx = C.MP[JMX]
def _sg(x): return ('+' if x > 0 else '') + h(x)
R.update(KM=t(C.KM, 7), ys2=t(_m2['ys2']), pe2=t(_m2['pe']), Fr2=t(_m2['Fr'], 0), t2=t(_m2['t2'], 2), t5=t(_m2['t5'], 2), tr=t(_m2['tr'], 2),
         M2=t(_m2['M']), MMAX=t(C.MP_MAX), MUM=t(C.MU_M, 2), MUPHI=t(C.MU_PHI, 3), MPY=str(C.MP_YMAX))
TXT.update(hsE1=h(M.POS[1]['sE']/M.H, 2), hys2=h(_m2['ys2']), hpe2=h(_m2['pe']), hFr2=h(_m2['Fr'], 0), hM2=h(_m2['M']), hM4=h(_m4['M']), hpe4=h(_m4['pe']),
           hJMX=str(JMX), hMMX=h(_mx['M']), hM3=h(C.MP[3]['M']), hMP2=h(C.MP[2]['M']))
from graf import a4_sheet, A4_CSS
import sheet as SH
R.update(A4CSS=SH.SHEET_CSS + A4_CSS, K20=t(20/C.OP, 2), OP=str(C.OP), MUA_G=t(C.MU_A, 2), AR8=t(C.AR[8]), AR8P=t(-C.AR[8]), ACYC=t(C.A_CYCLE, 0), AOV=t(C.A_CYCLE/(2*3.14)),
         YMM=t(C.YMM), MM=t(C.M_M), DEMAX=t(C.DE_MAX*C.MU_A), DEMIN=t(C.DE_MIN*C.MU_A), DERANGE=t(C.DE_RANGE))
TXT.update(YMIDTXT=', '.join(f'{k}–{k+1}: {h(C.YMID[k])}' for k in range(8)), AM3=h(C.AM[3]), DE3=h(C.DE[3]), JMAX=str(C.J_MAX), JMIN=str(C.J_MIN),
           AR3S=('+ ' if C.AR[3] > 0 else '− ') + h(abs(C.AR[3])))
AROWS = ''.join(f'<tr{" class=hl" if j in (C.J_MAX, C.J_MIN) else ""}><td>{j}</td><td>{h(C.YMID[j-1]) if j else ""}</td><td>{h(C.AR[j])}</td><td>{h(C.AM[j])}</td><td>{h(C.DE[j])}</td><td>{h(C.DE[j]*C.MU_A)}</td></tr>' for j in range(9))
MPROWS = ''.join(f'<tr{" class=hl" if j == P2 else ""}><td>{j}</td><td>{_sg(x["ys2"])}</td><td>{h(x["pe"])}</td><td>{x["a5"]}°</td><td>{h(x["Fr"],0)}</td><td>{h(x["M"])}</td><td>{h(x["Mmm"])}</td></tr>' for j, x in enumerate(C.MP))

from graf4 import a3_sheet4
_ip = C.IP; _i2 = _ip[P2]
R.update(IM2=t(C.M2, 2), IM5=t(C.M5, 2), IIS2=t(C.IS2, 2), GACC=str(C.G_ACC), IVS2=t(_i2['VS2'], 3), IW2=t(_i2['w2'], 2), IVE=t(_i2['VE'], 3),
         IA=t(_i2['a'], 5), IB=t(_i2['b'], 5), IFF=t(_i2['f'], 5), IT2=t(_i2['t2'], 6), ITW=t(_i2['tw'], 6), IT5=t(_i2['t5'], 6), II2=t(_i2['I'], 5),
         IMAX=t(C.IP_MAX, 5), IMUI=t(C.MU_I*1e4, 3), IYMAX=str(C.IP_YMAX))
TXT.update(hJIMAX=str(C.J_IMAX), hIS2=h(C.IS2, 2))
IPROWS = ''.join(f'<tr{" class=hl" if j == C.J_IMAX else ""}><td>{j}</td><td>{h(x["a"],5)}</td><td>{h(x["b"],5)}</td><td>{h(x["f"],5)}</td><td>{h(x["I"],5)}</td><td>{h(x["Imm"])}</td></tr>' for j, x in enumerate(_ip))

vel_rows = ''
for i in range(8):
    c = C.vchain(i)
    vel_rows += (f'<tr{" class=hl" if i == P2 else ""}><td>{i}</td><td>{h(c["VC"],3)}</td><td>{h(c["VEC"],3)}</td><td>{h(c["VE"],3)} {c["VEs"]}</td>'
                 f'<td>{h(c["w2"],2)} {c["w2s"]}</td><td>{h(c["w3"],2)} {c["w3s"]}</td><td>{h(c["w4"],2)} {c["w4s"]}</td></tr>')

HTML = r'''<!doctype html>
<html lang="hy">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Առաջադրանք №1 բացատրություն</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\(',right:'\\)',display:false}],strict:false});"></script>
<style>
  :root{
    color-scheme: light;
    --bg:#ffffff; --card:#ffffff; --ink:#000000; --muted:#444444; --border:#cfd6e3;
    --pen:#1d3a8a; --accent:#b4232c; --soft:#eef3ff; --warn-bg:#fff6e5; --warn:#9a5b00;
    --ok-bg:#eaf7ee; --ok:#1e7a3c;
    --s1:#d9480f; --s2:#2b8a3e; --s3:#7048e8; --s4:#1971c2; --s5:#c2255c; --line:#000000;
  }
  *{box-sizing:border-box}
  body{margin:0; background:var(--bg); color:var(--ink); font:17px/1.65 "Noto Sans Armenian","Segoe UI",system-ui,sans-serif}
  .page{max-width:900px; margin:0 auto; padding:32px 16px 72px}
  h1{font-size:2rem; margin:0 0 6px; color:var(--pen)}
  .lead{color:var(--muted); margin:0 0 26px}
  h2{font-size:1.35rem; margin:0 0 12px; color:var(--pen)}
  h3{font-size:1.08rem; margin:18px 0 6px}
  .card{background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px 22px; margin:0 0 22px}
  .toc a{color:var(--pen)}
  .toc ol{margin:6px 0 0; padding-left:22px}
  .tip,.warn,.write{border-radius:8px; padding:10px 14px; margin:12px 0}
  .tip{background:var(--soft); border-left:4px solid var(--pen)}
  .warn{background:var(--warn-bg); border-left:4px solid var(--warn)}
  .write{background:var(--ok-bg); border-left:4px solid var(--ok)}
  .write::before{content:"✍ Տետրում գրիր. "; font-weight:700; color:var(--ok)}
  table{border-collapse:collapse; width:100%; font-size:.95rem}
  th,td{border:1px solid var(--border); padding:6px 9px; text-align:left; vertical-align:top}
  th{background:var(--soft)}
  tr.hl td{background:#fff3bf; font-weight:600}
  .tbl{overflow-x:auto}
  .mpbox{max-width:640px;margin:10px 0}.mpbox svg{display:block;width:100%;height:auto;font-family:"STIX Two Text",serif}
  .mpg .ax,.projg .ax{stroke:#444;stroke-width:.35;fill:none}.mpg .ar{fill:#444}.mpg .gr{stroke:#cfd6e3;stroke-width:.3;stroke-dasharray:1.2 1}
  .mpg .cv{fill:none;stroke:var(--pen);stroke-width:.8}.mpg .dt,.projg .dt{fill:var(--pen)}.mpg .tk{font-size:4px;text-anchor:middle;fill:#444}
  .mpg .lb,.projg .lb{font-size:5px;font-style:italic}.mpg .sb{font-size:3.4px}.mpg .dm{stroke:var(--accent);stroke-width:.3}.mpg .dmt{font-size:3.8px;fill:var(--accent)}.mpg .dmt.c{text-anchor:middle}
  .a4box{max-width:560px;margin:10px auto}.a4box svg{margin:0}
  .a3box{margin:10px 0}.a3box svg{display:block;width:100%;height:auto;margin:0}
  @@A4CSS@@
  .projbox{max-width:460px;margin:10px 0}.projbox svg{display:block;width:100%;height:auto}
  .projg .cap{font-size:5px;fill:#444}.projg .vc{stroke:var(--pen);stroke-width:1}.projg .pj{stroke:#777;stroke-width:.4;stroke-dasharray:1.5 1}
  .projg .hl{stroke:var(--accent);stroke-width:1.6}.projg .hlt{font-size:4.2px;fill:var(--accent)}.projg .g2{stroke:var(--ok);stroke-width:.9}.projg .ar2{fill:var(--ok)}
  .katex-display{overflow-x:auto; overflow-y:hidden; padding:2px 0}
  svg{max-width:100%; height:auto; display:block; margin:8px auto}
  svg text{font-family:inherit}
  .chip{display:inline-block; padding:0 8px; border-radius:10px; color:#fff; font-weight:600; font-size:.9rem}
  .c1{background:var(--s1)} .c2{background:var(--s2)} .c3{background:var(--s3)} .c4{background:var(--s4)} .c5{background:var(--s5)}
  .flow{display:flex; flex-wrap:wrap; gap:6px; align-items:center; margin:10px 0}
  .flow span.box{border:1px solid var(--border); background:var(--soft); border-radius:8px; padding:4px 10px; font-size:.93rem}
  .flow span.arr{color:var(--muted)}
  .cap{font-size:.88rem; color:var(--muted); text-align:center; margin:2px 0 10px}
  .two{display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px; align-items:start}
  ol li, ul li{margin:4px 0}
  .rot{display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px; align-items:start}
  .rot svg{width:100%; max-height:440px; touch-action:none; user-select:none; -webkit-user-select:none}
  .rot svg.grab{cursor:grab} .rot svg.grab.hold{cursor:grabbing}
  .rotctl{display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:8px 0}
  .rotctl label{display:flex; gap:8px; align-items:center; flex:1 1 220px}
  .rotctl input[type=range]{flex:1; min-width:120px}
  .rotctl button{font:inherit; font-size:.95rem; padding:4px 12px; border:1px solid var(--border); border-radius:8px; background:var(--soft); color:var(--pen); cursor:pointer}
  .rotctl button.on{background:var(--pen); color:#fff}
</style>
</head>
<body>
<div class="page">
  <h1>Առաջադրանք №1 — բացատրություն զրոյից</h1>
  <p class="lead">Մեխանիզմների և մեքենաների տեսություն, տարբերակ 13: Այս էջը միայն <b>հասկանալու</b> համար է: Տետրում գրվող մաքուր լուծումը, A3 թերթերի կոորդինատները և քայլերի ստուգաթերթը մյուս էջերում են (<a href="TMM_Variant13.html">Աշխատանքը</a> և <a href="tetr.html">Տետրում գրելու</a>՝ էջ 10–22): Կանաչ «✍» դաշտերը ցույց են տալիս, թե բացատրության որ մասը տետրի որ տողին է վերաբերում:</p>

  <div class="card toc">
    <h2>Բովանդակություն</h2>
    <ol>
      <li><a href="#task">Ինչի՞ մասին է խնդիրը</a></li>
      <li><a href="#scheme">Ինչպես կարդալ սխեման</a></li>
      <li><a href="#data">Տրված տվյալները և բոլոր նշանակումները</a></li>
      <li><a href="#ideas">Չորս գաղափար, որոնց վրա կանգնած է ամեն ինչ</a></li>
      <li><a href="#s1">Քայլ 1 — մասշտաբը և գծագրային երկարությունները</a></li>
      <li><a href="#s2">Քայլ 2 — եզրային դիրքերը, AB-ն և BC-ն</a></li>
      <li><a href="#s3">Քայլ 3 — 8 դիրքերի պլանը</a></li>
      <li><a href="#s4">Քայլ 4 — B կետի արագությունը և μ<sub>v</sub>-ն</a></li>
      <li><a href="#s5">Քայլ 5 — արագությունների պլանի կառուցումը</a></li>
      <li><a href="#s6">Քայլ 6 — թվերը, ω-ները և դրանց ուղղությունը</a></li>
      <li><a href="#s7">Քայլ 7 — արագացումների պլանը (դիրք 3)</a></li>
      <li><a href="#s8">Քայլ 8 — բերված մոմենտը և նրա գրաֆիկը</a></li>
      <li><a href="#s9">Քայլ 9 — աշխատանքների և կինետիկ էներգիայի աճի գրաֆիկները</a></li>
      <li><a href="#s10">Քայլ 10 — բերված իներցիայի մոմենտը</a></li>
      <li><a href="#fre">F<sub>re</sub> գրաֆիկը և թերթերը</a></li>
      <li><a href="#assume">Ենթադրություններ — ճշտիր դասախոսի մոտ</a></li>
      <li><a href="#check">Ստուգաթերթ և տարածված սխալներ</a></li>
      <li><a href="#rotor">Պտտիր մեխանիզմը ինքդ</a></li>
    </ol>
  </div>

  <div class="card" id="task">
    <h2>1. Ինչի՞ մասին է խնդիրը</h2>
    <p>Պատկերացրու մամլիչ կամ դրոշմող մեքենա: Էլեկտրաշարժիչը հավասարաչափ պտտում է <b>կռունկը</b> (կարճ լծակ)՝ րոպեում @@hN1@@ պտույտ: Մեզ պետք է, որ <b>սողնակը</b> (դանակ, դրոշմ) շարժվի <b>վեր ու վար</b> ուղղաձիգ ուղղորդով՝ @@hHE@@ մմ ընթացքով: Պտույտը ետ ու առաջ շարժման վերածելու համար օգտագործում են <b>լծակավոր մեխանիզմ</b>. քո մեխանիզմն ունի 5 շարժական օղակ (գումարած անշարժ «հիմքը»):</p>
    <p>Առաջադրանքում պետք է անել երեք բան.</p>
    <ol>
      <li><b>Սինթեզ</b> (§1). գտնել կռունկի և շարժաթևի <b>երկարությունները</b>, որոնք տրված չեն, և գծել մեխանիզմը 8 դիրքում:</li>
      <li><b>Արագություններ</b> (§2). յուրաքանչյուր դիրքում գտնել կետերի արագությունները և օղակների անկյունային արագությունները՝ <b>արագությունների պլանի</b> օգնությամբ:</li>
      <li><b>Արագացումներ</b> (§3). մեկ՝ 3-րդ (հաստ) դիրքի համար գտնել արագացումները՝ <b>արագացումների պլանով</b>:</li>
    </ol>
    <p>Ինչու՞ է սա պետք: Հաջորդ բաժնում (ուժային հաշվարկ) իներցիայի ուժերը հաշվվում են <i>F</i> = <i>m</i>·<i>a</i>-ով, ուստի առանց արագացումների հնարավոր չէ իմանալ, թե ինչ ուժեր են ազդում օղակների վրա: Իսկ թափանիվի հաշվարկին պետք են արագությունները բոլոր դիրքերում:</p>
    <div class="tip">«Պլանը» ուղղակի <b>վեկտորային գծագիր</b> է. արագությունները (կամ արագացումները) գծում ենք սլաքներով մասշտաբով, և հավասարումը լուծում ենք <b>երկրաչափորեն</b>՝ քանոնով և անկյունաչափով, առանց եռանկյունաչափության:</div>
  </div>

  <div class="card" id="scheme">
    <h2>2. Ինչպես կարդալ սխեման</h2>
    <p>Ահա քո մեխանիզմը 3-րդ (հաստ) դիրքում, իսկական համամասնություններով (A3 թերթի կոորդինատներից): Յուրաքանչյուր օղակ ունի իր գույնը. նույն գույները կտեսնես պլաններում:</p>
    @@MECH@@
    <div class="tbl">
    <table>
      <tr><th>Օղակ</th><th>Անվանում</th><th>Ինչպես է շարժվում</th></tr>
      <tr><td><span class="chip c1">1</span> AB</td><td><b>կռունկ</b></td><td>լրիվ պտտվում է A-ի շուրջը, հավասարաչափ (ω<sub>1</sub> = const), ժամացույցի սլաքի հակառակ ուղղությամբ (↺)</td></tr>
      <tr><td><span class="chip c2">2</span> BC</td><td><b>շարժաթև</b></td><td>բարդ (հարթ-զուգահեռ) շարժում. B-ն գնում է շրջանով, C-ն՝ աղեղով: S<sub>2</sub>-ը նրա մեջտեղն է (զանգվածի կենտրոն)</td></tr>
      <tr><td><span class="chip c3">3</span> CD</td><td><b>ճոճաթև (լծակ)</b></td><td><b>Ճոճվում</b> է D-ի շուրջը՝ լրիվ չպտտվելով</td></tr>
      <tr><td><span class="chip c4">4</span> CE</td><td><b>շարժաթև</b></td><td>բարդ շարժում. C-ն գնում է աղեղով, E-ն՝ ուղիղ գծով: <b>CE = CD</b></td></tr>
      <tr><td><span class="chip c5">5</span> E</td><td><b>սողնակ</b></td><td>համընթաց շարժում ուղղաձիգ <i>yy</i> ուղղորդով (D-ով անցնող ուղղաձիգ)</td></tr>
      <tr><td>0</td><td>հենարան (դարակ)</td><td>անշարժ. A և D հոդերը, ուղղորդը: Գծագրում նշվում են շտրիխավորված եռանկյունիներով</td></tr>
    </table>
    </div>
    <h3>Շարժման ճանապարհը</h3>
    <div class="flow">
      <span class="box">Շարժիչ</span><span class="arr">→</span>
      <span class="box"><span class="chip c1">1</span> կռունկը պտտվում է</span><span class="arr">→</span>
      <span class="box"><span class="chip c2">2</span> BC-ն հրում/քաշում է C-ն</span><span class="arr">→</span>
      <span class="box"><span class="chip c3">3</span> CD-ն ճոճվում է D-ի շուրջը</span><span class="arr">→</span>
      <span class="box"><span class="chip c4">4</span> CE-ն հրում է E-ն</span><span class="arr">→</span>
      <span class="box"><span class="chip c5">5</span> սողնակը վեր-վար</span>
    </div>
    <p>Մեխանիզմը կազմված է երկու մասից. <b>ABCD քառօղակ</b> (կռունկ-ճոճաթևային), որը պտույտը դարձնում է ճոճում, և <b>CE շարժաթևը սողնակի հետ</b>, որը ճոճումը դարձնում է ուղղագիծ շարժում: Դրա համար էլ հաշվարկը միշտ գնում է նույն հերթականությամբ՝ <b>B → C → E</b>:</p>
    <div class="tip">Քանի որ CE = CD և E-ն D-ով անցնող ուղղաձիգի վրա է, DCE եռանկյունը <b>միշտ հավասարասրուն է</b>, և E-ն գտնվում է D-ից ուղիղ ներքև՝ ճիշտ C-ի բարձրության կրկնապատիկ խորությամբ: Սա շատ կարևոր է, այն կօգնի և՛ գծելիս, և՛ պլաններում:</div>
  </div>

  <div class="card" id="data">
    <h2>3. Տրված տվյալները</h2>
    <p>Դու առաջադրանքի աղյուսակի №13 տողն ես.</p>
    <div class="tbl">
    <table>
      <tr><th>Նշանակում</th><th>Արժեք</th><th>Ինչ է նշանակում</th></tr>
      <tr><td>\(H_E\)</td><td>@@hHE@@ մմ = @@HE@@ մ</td><td>սողնակի <b>ընթացքը</b>՝ ամենավերին և ամենաներքին դիրքերի տարբերությունը</td></tr>
      <tr><td>\(L_1\)</td><td>310 մմ</td><td>A և D հոդերի <b>հորիզոնական</b> հեռավորությունը</td></tr>
      <tr><td>\(L_2\)</td><td>265 մմ</td><td>A և D հոդերի <b>ուղղաձիգ</b> հեռավորությունը</td></tr>
      <tr><td>\(l_{CD}\)</td><td>@@hLCD@@ մմ</td><td>ճոճաթևի երկարությունը (նույնն է \(l_{CE}\)-ի)</td></tr>
      <tr><td>\(n_1\)</td><td>@@hN1@@ պտ/ր</td><td>կռունկի պտուտաթիվը</td></tr>
      <tr><td>\(G_2,\ G_5,\ I_{S_2},\ F_{re}^{max}\)</td><td>@@G2@@ Ն, @@G5@@ Ն, @@IS2R@@, @@FMAX@@ Ն</td><td>կշիռներ, իներցիայի մոմենտ, օգտակար դիմադրության ուժ. <b>կինեմատիկային պետք չեն</b>. G₂, G₅, F<sub>re</sub>-ն պետք են բերված մոմենտի համար (Քայլ 8), I<sub>S₂</sub>-ը՝ Քայլ 10-ում</td></tr>
    </table>
    </div>
    <p>Լրացուցիչ պայմաններ. \(l_{CE} = l_{CD} = @@LCD@@\) մ, \(l_{BS_2} = 0{,}5\,l_{BC}\), \(\beta = 3°\div5°\) (ընդունում ենք 3°):</p>
    <h3>Մյուս տառերը, որոնց կհանդիպես</h3>
    <div class="tbl">
    <table>
      <tr><th>Նշանակում</th><th>Իմաստը</th></tr>
      <tr><td>\(\mu_l\) («մյու»)</td><td><b>երկարությունների մասշտաբ</b>, մ/մմ. գծագրի 1 մմ-ը քանի մետր է իրականում</td></tr>
      <tr><td>\(\mu_v,\ \mu_a\)</td><td>արագությունների ((մ/վ)/մմ) և արագացումների ((մ/վ²)/մմ) մասշտաբները</td></tr>
      <tr><td>աստղանիշ՝ \(AB^*\), \(H_E^*\)</td><td>նույն երկարությունը <b>գծագրի վրա</b>, մմ-ով</td></tr>
      <tr><td>\(p\), \(\pi\)</td><td>արագությունների և արագացումների պլանի <b>բևեռը</b>՝ «զրոյական» կետը. անշարժ կետերը (A, D) պլանում ընկնում են այստեղ</td></tr>
      <tr><td>փոքրատառ \(b, c, e, s_2\)</td><td>մեխանիզմի B, C, E, S₂ կետերի «պատկերները» պլանում. \(pc\) հատվածը = \(V_C\)-ն մասշտաբով</td></tr>
      <tr><td>\(V_{CB}\), \(V_{EC}\)</td><td>C-ի <b>հարաբերական</b> արագությունը B-ի նկատմամբ, E-ինը՝ C-ի նկատմամբ</td></tr>
      <tr><td>\(\omega_2, \omega_3, \omega_4\)</td><td>օղակների անկյունային արագությունները, վ⁻¹ (= ռադ/վ)</td></tr>
      <tr><td>\(a^n,\ a^t\)</td><td>արագացման <b>նորմալ</b> (կենտրոնաձիգ) և <b>շոշափող</b> բաղադրիչներ</td></tr>
      <tr><td>\(n_2, n_3, n_4\)</td><td>արագացումների պլանի օժանդակ կետեր՝ նորմալ բաղադրիչի ծայրը</td></tr>
      <tr><td>\(\varepsilon_2, \varepsilon_3, \varepsilon_4\)</td><td>անկյունային արագացումները, վ⁻²</td></tr>
    </table>
    </div>
  </div>

  <div class="card" id="ideas">
    <h2>4. Չորս գաղափար, որոնց վրա կանգնած է ամեն ինչ</h2>
    <h3>Գաղափար 1. մասշտաբ</h3>
    <p>Ցանկացած ֆիզիկական մեծություն թղթի վրա դառնում է հատված. <b>իրական = գծագրային × μ</b>, և հակառակը՝ <b>գծագրային = իրական / μ</b>: Սա միակ բանաձևն է, որ պետք է անգիր հիշել. մնացածը դրա կիրառություններն են:</p>
    <h3>Գաղափար 2. պտտվող կետի արագությունը</h3>
    <p>Եթե կետը պտտվում է կենտրոնի շուրջը \(l\) շառավղով, նրա արագությունը</p>
    $$V = \omega\cdot l,\qquad \vec V \perp \text{շառավղին}$$
    <p>Ինչպես անվի եզրը. արագությունը միշտ շոշափող է շրջանին, այսինքն ուղղահայաց շառավղին: Այս պատճառով տետրում ամենուր գրված է «⊥AB», «⊥CD», «⊥CE»:</p>
    <h3>Գաղափար 3. երկու կետ մեկ օղակի վրա</h3>
    <p>Եթե B-ն և C-ն մեկ կոշտ ձողի ծայրերն են, C-ի արագությունը = B-ի արագություն + C-ի պտույտը B-ի շուրջը.</p>
    $$\vec V_C = \vec V_B + \vec V_{CB},\qquad \vec V_{CB}\perp BC$$
    <p>Վեկտորային հավասարումը հարթության վրա = <b>երկու</b> թվային հավասարում, ուստի կարող ենք գտնել <b>երկու</b> անհայտ: Դրա համար տետրում հավասարման տակ գծում ենք «Մեծ. / ուղղ.» աղյուսակը. «+» = հայտնի է, «−» = անհայտ: Եթե «−»-երը ճիշտ երկուսն են, հավասարումը լուծվում է:</p>
    <h3>Գաղափար 4. հավասարասրուն եռանկյունը DCE</h3>
    <p>Քանի որ \(CE = CD\) և E-ն D-ով անցնող ուղղաձիգի վրա է, E-ի կոորդինատները C-ի միջոցով են՝ \(E = (0,\ 2y_C)\): Սրանից արագությունների համար հետևում է հետաքրքիր բան. \(V_E\)-ն ուղղաձիգ է, ուստի նրա հորիզոնական բաղադրիչը զրո է.</p>
    $$-(\omega_3+\omega_4)\,y_C = 0\quad\Rightarrow\quad \omega_4 = -\omega_3,\qquad V_{EC} = \omega_4\,l_{CE} = -\omega_3\,l_{CD}\ \Rightarrow\ |V_{EC}| = |V_C|$$
    <p>Այսինքն՝ <b>ce = pc</b> (արագությունների պլանում pce եռանկյունը նույնպես հավասարասրուն է), \(\omega_4\)-ը մեծությամբ հավասար է \(\omega_3\)-ին, բայց հակառակ ուղղությամբ, և \(pe\)-ն միշտ ուղղաձիգ է: Սա լավ ինքնաստուգում է:</p>
  </div>

  <div class="card" id="s1">
    <h2>Քայլ 1 — Մասշտաբը և գծագրային երկարությունները</h2>
    <h3>Գաղափարը</h3>
    <p>Իրական մեխանիզմը մոտ կես մետր է, իսկ թերթը՝ 42 սմ: Պետք է փոքրացնել: \(L_1 = @@L1@@\) մ հեռավորությունը որոշում ենք գծել <b>@@L1S@@ մմ</b> (կլոր թիվ, որ մեխանիզմը լավ տեղավորվի). մնացած բոլոր երկարությունները հետևում են դրանից:</p>
    $$\mu_l = \frac{L_1}{L_1^*} = \frac{@@L1@@}{@@L1S@@} = @@MUL@@\ \text{մ/մմ}$$
    <p>Հիմա յուրաքանչյուր իրական երկարություն բաժանում ենք \(\mu_l\)-ի.</p>
    $$H_E^* = \frac{@@HE@@}{@@MUL@@} = @@H@@\ \text{մմ},\quad L_2^* = \frac{@@L2@@}{@@MUL@@} = @@L2S@@\ \text{մմ},\quad CD^* = CE^* = \frac{@@LCD@@}{@@MUL@@} = @@CD@@\ \text{մմ}$$
    <div class="tip"><b>Ինքնաստուգում.</b> \(CE^*\)-ը և \(CD^*\)-ը նույն թիվն են, քանի որ \(l_{CE} = l_{CD}\):</div>
    <div class="write">էջ 10–11. \(\mu_l\), \(H_E^*\), \(L_2^*\), \(CD^* = CE^*\) տողերը:</div>
  </div>

  <div class="card" id="s2">
    <h2>Քայլ 2 — Եզրային դիրքերը, AB-ն և BC-ն</h2>
    <h3>Գաղափարը</h3>
    <p>\(l_{AB}\)-ն և \(l_{BC}\)-ն տրված չեն: Դրանք պետք է ընտրել այնպես, որ սողնակը վեր-վար շարժվի <b>ճիշտ @@hHE@@ մմ</b>: Գաղտնիքը <b>եզրային դիրքերն</b> են. սողնակը կանգ է առնում ու ետ դառնում այն պահին, երբ կռունկը և շարժաթևը <b>մեկ ուղղի վրա</b> են:</p>
    <h3>ա) Սողնակի և ճոճաթևի եզրային դիրքերը</h3>
    <ol>
      <li><b>Ստորին դիրք.</b> DC-ն ուղղաձիգից շեղում ենք β = 3° → C₀′: Քանի որ DCE-ն հավասարասրուն է, E-ն D-ից ուղիղ ներքև է, և \(DE_0' = 2\cdot CD^*\cdot\cos\beta = 2\cdot@@CD@@\cdot\cos3° = @@DE0P@@\) մմ → E₀′ (ամենացածր կետը):</li>
      <li><b>Վերին դիրք.</b> E₀′-ից բարձրանում ենք \(H_E^*\) = @@H@@ մմ → E₀, \(DE_0 = @@DE0@@\) մմ: E₀-ից \(CE^*\) = @@CD@@ մմ աղեղը հատում է C-ի հետագիծը → C₀:</li>
      <li>DC₀-ն ուղղաձիգից շեղված է γ անկյունով. \(\cos\gamma = DE_0/(2\,CD^*) = @@DE0@@/@@DE2CD@@ = @@COSG@@\), \(\gamma = @@GAM@@°\):</li>
    </ol>
    <p>Ճոճաթևի ճոճման անկյունը՝ \(\psi = \angle C_0DC_0' = \gamma - \beta = @@GAM@@° - 3° = @@PSI@@°\):</p>
    <h3>բ) Ինչու՞ են կռունկը և շարժաթևը մեկ ուղղի վրա</h3>
    @@EXTREME@@
    <p class="cap">Եզրային դիրքերում A, B, C կետերը մեկ ուղղի վրա են. C₀-ում՝ «ծալված» (A-ն B₀-ի և C₀-ի միջև), C₀′-ում՝ «ձգված»:</p>
    <p>Երբ C-ն հասնում է իր ամենամոտ կետին (C₀), A-ն ընկնում է B-ի և C-ի միջև, «ծալված». \(AC_0 = BC - AB\): Երբ C-ն ամենահեռու կետում է (C₀′), AB-ն և BC-ն մեկ գծով «ձգված» են. \(AC_0' = AB + BC\): Գծագրից չափում ենք \(AC_0\) և \(AC_0'\) ու լուծում ենք համակարգը.</p>
    $$\begin{cases} BC - AB = @@AC0@@ \\ AB + BC = @@AC0P@@ \end{cases}\quad\Rightarrow\quad 2\cdot BC = @@SUM@@$$
    $$BC = @@BC@@\ \text{մմ},\qquad AB = @@AC0P@@ - @@BC@@ = @@AB@@\ \text{մմ}$$
    <p>Հավասարումները <b>գումարում</b> ենք (AB-ն կրճատվում է), դրա համար տետրում համակարգի կողքին գրված է «±»:</p>
    $$l_{AB} = AB\cdot\mu_l = @@AB@@\cdot@@MUL@@ = @@LAB@@\ \text{մ},\qquad l_{BC} = @@BC@@\cdot@@MUL@@ = @@LBC@@\ \text{մ}$$
    <div class="warn">Ստուգում. @@AB@@ + @@BC@@ = @@AC0P@@ ✔ և @@BC@@ − @@AB@@ = @@AC0@@ ✔: Քո չափած \(AC_0\)-ն կարող է 0,5 մմ-ով տարբերվել, դա նորմալ է. պարզապես նույն երկու տողը հաշվիր քո թվերով:</div>
    <div class="tip"><b>Ստուգում, որ կռունկը լրիվ կպտտվի</b> (Գրասհոֆի պայման). \(l_{AB} + l_{AD} = @@LAB@@ + @@AD@@ = @@GL@@ &lt; l_{BC} + l_{CD} = @@GR@@\) ✔ (\(l_{AD} = \sqrt{L_1^2 + L_2^2}\)): Փոխանցման ամենափոքր անկյունը՝ \(\gamma_{min} \approx @@GMIN@@°\), այսինքն մեխանիզմը չի «խրվում»:</div>
    <div class="write">էջ 11. DE₀′, DE₀, γ, ψ տողերը, «±» համակարգը ընդհանուր տեսքով (B₀C₀ − AB₀ = AC₀…), հետո թվերով, 2·BC, BC, AB, \(l_{AB}\), \(l_{BC}\):</div>
  </div>

  <div class="card" id="s3">
    <h2>Քայլ 3 — 8 դիրքերի պլանը</h2>
    <p>Մեխանիզմը շարժման մեջ ուսումնասիրելու համար «լուսանկարում» ենք 8 պահ: Կռունկի շրջանագիծը (\(R = AB^* = @@AB@@\) մմ) B₀-ից սկսած բաժանում ենք <b>8 հավասար մասի</b> (45°-ական)՝ ժամացույցի սլաքի հակառակ ուղղությամբ: Ամեն Bᵢ-ի համար կարկինով.</p>
    <div class="flow">
      <span class="box">Bᵢ</span><span class="arr">→ R = BC* →</span>
      <span class="box">Cᵢ (C-ի աղեղի վրա)</span><span class="arr">→ R = CE* →</span>
      <span class="box">Eᵢ (ուղղորդի վրա)</span>
    </div>
    <p>Բոլոր դիրքերը գծում ենք բարակ, իսկ <b>3-րդը՝ հաստ</b>. դա այն դիրքն է, որի համար անում ենք արագացումների պլանը: 0-րդ դիրքը (B₀) մեռյալ դիրքն է, սողնակը ամենավերևում է:</p>
    <div class="tip">Կռունկը B₀-ից B₀′ պտտվում է \(@@PHIW@@°\) (սողնակը իջնում է՝ <b>աշխատանքային ընթացք</b>), վերադարձին՝ \(@@PHII@@°\) (<b>պարապ ընթացք</b>): \(K = @@PHIW@@/@@PHII@@ = @@K@@ &gt; 1\). պարապ ընթացքն ավելի արագ է: 1, 2, 3, 4 դիրքերը աշխատանքային են, 5, 6, 7-ը՝ պարապ:</div>
    <div class="write">տետրում այս քայլի համար հաշվարկ չկա, միայն թերթ 1-ի գծագիրն է: Գծելու բոլոր քայլերը նշվող վանդակներով՝ <code>TMM_Variant13.html</code>-ում:</div>
  </div>

  <div class="card" id="s4">
    <h2>Քայլ 4 — B կետի արագությունը և \(\mu_v\)-ն</h2>
    <h3>Գաղափարը</h3>
    <p>B-ն միակ կետն է, որի արագությունն <b>անմիջապես</b> հայտնի է. նա պտտվում է A-ի շուրջը հայտնի ω<sub>1</sub>-ով (Գաղափար 2): Նախ պտ/ր-ը դարձնում ենք ռադ/վ (1 պտույտ = 2π, 1 րոպե = 60 վ).</p>
    $$\omega_1 = \frac{2\pi n_1}{60} = \frac{\pi n_1}{30} = \frac{3{,}1416\cdot@@N1@@}{30} = @@W1@@\ \text{վ}^{-1}$$
    $$V_B = \omega_1\cdot l_{AB} = @@W1@@\cdot@@LAB@@ = @@VB@@\ \text{մ/վ},\qquad \vec V_B\perp AB$$
    <p>Կռունկը պտտվում է հավասարաչափ, ուստի \(V_B\)-ն <b>բոլոր 8 դիրքերում նույնն է</b>. փոխվում է միայն ուղղությունը:</p>
    <h3>Մասշտաբը</h3>
    <p>Ընտրում ենք \(\mu_v = @@MUV@@\) (մ/վ)/մմ, որ \(V_B\)-ն պլանում լինի մոտ 50 մմ սլաք:</p>
    $$pb = \frac{V_B}{\mu_v} = \frac{@@VB4@@}{@@MUV@@} = @@PB@@\ \text{մմ}$$
    <p>Այսինքն պլանի 1 մմ-ը = @@hMUV@@ մ/վ: Ցանկացած հատված պլանում բազմապատկում ես այս թվով ու ստանում արագություն:</p>
    <div class="write">էջ 11. \(V_B\)-ի տողը և «\(\vec V_B\perp AB\) (\(\omega_1\)-ի ուղղությամբ)»: Էջ 12, կետ 5. \(\mu_v\)-ն և pb-ն:</div>
  </div>

  <div class="card" id="s5">
    <h2>Քայլ 5 — Արագությունների պլանի կառուցումը (դիրք 3-ի օրինակով)</h2>
    @@VPLAN@@
    <p class="cap">Դիրք 3-ի արագությունների պլանը. գույները նույնն են, ինչ սխեմայում:</p>
    <h3>ա) b կետը</h3>
    <p>Թղթի վրա ընտրում ենք p բևեռը: Նրանից տանում ենք <b>pb = @@PB@@ մմ ⊥ AB</b>, ω<sub>1</sub>-ի պտույտի կողմը: A-ն և D-ն անշարժ են, ուստի նրանց պատկերները (a, d) ընկնում են p-ում:</p>
    <h3>բ) c կետը — հավասարում (1)</h3>
    $$\vec V_C = \vec V_B + \vec V_{CB}$$
    <div class="tbl">
    <table>
      <tr><th></th><th>\(\vec V_C\)</th><th>\(\vec V_B\)</th><th>\(\vec V_{CB}\)</th></tr>
      <tr><td>Մեծ.</td><td>− (անհայտ)</td><td>+ (@@hVB@@ մ/վ)</td><td>− (անհայտ)</td></tr>
      <tr><td>ուղղ.</td><td>+ (⊥CD, C-ն պտտվում է D-ի շուրջը)</td><td>+ (⊥AB)</td><td>+ (⊥BC)</td></tr>
    </table>
    </div>
    <p>Երկու անհայտ (երկու «−») → լուծվում է: Երկրաչափորեն. <b>b-ով</b> տանում ենք ուղիղ ⊥BC (\(V_{CB}\)-ի ուղղությունը), <b>p-ով</b>՝ ուղիղ ⊥CD (\(V_C\)-ի ուղղությունը, քանի որ D-ն p-ում է): Դրանց <b>հատումը c կետն է</b>: Վերջ. չափում ենք pc-ն և bc-ն:</p>
    <h3>գ) e կետը — հավասարում (2)</h3>
    $$\vec V_E = \vec V_C + \vec V_{EC}$$
    <div class="tbl">
    <table>
      <tr><th></th><th>\(\vec V_E\)</th><th>\(\vec V_C\)</th><th>\(\vec V_{EC}\)</th></tr>
      <tr><td>Մեծ.</td><td>− (անհայտ)</td><td>+ (pc)</td><td>− (անհայտ)</td></tr>
      <tr><td>ուղղ.</td><td>+ (∥ yy, ուղղաձիգ)</td><td>+ (⊥CD)</td><td>+ (⊥CE)</td></tr>
    </table>
    </div>
    <p>E-ն սահում է միայն ուղղաձիգ ուղղորդով, ուստի \(\vec V_E\)-ի ուղղությունը հայտնի է (∥ yy), իսկ \(\vec V_{EC}\)-ինը՝ ⊥CE: Երկու անհայտ → լուծվում է: <b>c-ով</b> տանում ենք ուղիղ ⊥CE, <b>p-ով</b>՝ ուղղաձիգ: Հատումը <b>e կետն է</b>:</p>
    <h4>Ինչու՞ է ce = pc</h4>
    <p>Գաղափար 4-ից՝ \(\omega_4 = -\omega_3\) և \(l_{CE} = l_{CD}\), ուստի \(V_{EC} = V_C\), այսինքն \(ce = pc\): Պլանում pce եռանկյունը հավասարասրուն է. e-ն p-ի ուղղաձիգի վրա է և c-ից նույն հեռավորության վրա, ինչ p-ն: Սա լավ ստուգում է. չափիր ce-ն, այն պետք է հավասար լինի pc-ին:</p>
    <div class="tip"><b>Ինքնաստուգում.</b> \(V_C = pc\cdot\mu_v = @@pc@@\cdot@@MUV@@ = @@VC@@\) մ/վ, \(\omega_3 = @@VC@@/@@LCD@@ = @@w3@@\) վ<sup>−1</sup>, իսկ \(V_{EC} = ce\cdot\mu_v = @@ce@@\cdot@@MUV@@ = @@VEC@@\) մ/վ ✔, \(\omega_4 = @@VEC@@/@@LCD@@ = @@w4@@\) վ<sup>−1</sup> ✔:</div>
    <h3>դ) s₂ կետը</h3>
    <p>S₂-ը BC-ի մեջտեղում է, ուստի s₂-ը <b>bc հատվածի մեջտեղում է</b> (\(bs_2 = cs_2\)): ps₂-ը չափում ենք:</p>
    <div class="warn"><b>Մեռյալ դիրքը (0).</b> A, B, C մեկ ուղղի վրա են, ուստի ⊥AB և ⊥BC ուղիղները համընկնում են, և c-ն ընկնում է p-ի վրա. \(V_C = V_E = V_{EC} = 0\), \(bc = pb = @@PB@@\) մմ, s₂-ը pb-ի մեջտեղում: Պլանը պարզապես մեկ սլաք է: Սա սխալ չէ. սողնակն այդ պահին կանգնած է ու շրջվում է:</div>
    <div class="write">էջ 11–12. հավասարումներ (1), (2)՝ իրենց «Մեծ./ուղղ.» աղյուսակներով, ce = pc նշումը և կետ 4-ը (\(bs_2 = cs_2\)):</div>
  </div>

  <div class="card" id="s6">
    <h2>Քայլ 6 — Թվերը, ω-ները և դրանց ուղղությունը</h2>
    <p>Պլանից չափում ենք հատվածները (մմ) և բազմապատկում \(\mu_v\)-ով (դիրք 3).</p>
    $$V_C = pc\cdot\mu_v = @@pc@@\cdot@@MUV@@ = @@VC@@\ \text{մ/վ}\qquad V_{EC} = ce\cdot\mu_v = @@ce@@\cdot@@MUV@@ = @@VEC@@\ \text{մ/վ}$$
    $$V_E = pe\cdot\mu_v = @@pe@@\cdot@@MUV@@ = @@VE@@\ \text{մ/վ}\qquad V_{S_2} = ps_2\cdot\mu_v = @@ps2@@\cdot@@MUV@@ = @@VS2@@\ \text{մ/վ}$$
    $$V_{CB} = bc\cdot\mu_v = @@bc@@\cdot@@MUV@@ = @@VCB@@\ \text{մ/վ}$$
    <h3>Անկյունային արագությունները</h3>
    <p>Գաղափար 2-ը «հակառակ»՝ \(\omega = V/l\): Օղակի պտույտը տալիս է <b>հարաբերական</b> արագությունը (կամ անշարժ կետի նկատմամբ արագությունը).</p>
    $$\omega_2 = \frac{V_{CB}}{l_{BC}} = \frac{@@VCB@@}{@@LBC@@} = @@w2@@\ \text{վ}^{-1}$$
    $$\omega_3 = \frac{V_C}{l_{CD}} = \frac{@@VC@@}{@@LCD@@} = @@w3@@,\quad \omega_4 = \frac{V_{EC}}{l_{CE}} = \frac{@@VEC@@}{@@LCD@@} = @@w4@@\ \text{վ}^{-1}$$
    <h3>Ինչպես գտնել պտույտի ուղղությունը (↻ թե ↺)</h3>
    <ol>
      <li>Պլանից վերցրու հարաբերական արագության սլաքը, օրինակ՝ \(\vec V_{CB}\) (b-ից c):</li>
      <li>Մտովի տեղափոխիր այն մեխանիզմի <b>C</b> կետ:</li>
      <li>Նայիր, թե ինչ կողմ է այն «պտտում» C-ն B-ի շուրջը. դա \(\omega_2\)-ի ուղղությունն է:</li>
    </ol>
    <p>\(\omega_3\)-ի համար՝ \(\vec V_C\)-ն (p-ից c) դնում ես C-ում ու նայում D-ի շուրջը, \(\omega_4\)-ի համար՝ \(\vec V_{EC}\)-ն (c-ից e) դնում ես E-ում ու նայում C-ի շուրջը:</p>
    <h3>Բոլոր 8 դիրքերը</h3>
    <div class="tbl">
    <table>
      <tr><th>i</th><th>\(V_C\), մ/վ</th><th>\(V_{EC}\)</th><th>\(V_E\)</th><th>\(\omega_2\), վ⁻¹</th><th>\(\omega_3\)</th><th>\(\omega_4\)</th></tr>
      @@VROWS@@
    </table>
    </div>
    <div class="tip"><b>Ինչ է ցույց տալիս աղյուսակը.</b> 1–4 դիրքերում \(V_E\)-ն ↓ է (սողնակը իջնում է՝ աշխատանքային ընթացք), 5–7-ում՝ ↑: 0-ում և մոտ 4-ում (ներքևի եզր) \(V_E \approx 0\): \(\omega_3\)-ը փոխում է նշանը 4-ի և 5-ի միջև. ճոճաթևը շրջվում է: \(\omega_4\)-ը մեծությամբ միշտ հավասար է \(\omega_3\)-ին՝ հակառակ նշանով: Եթե քո աղյուսակում նույն օրինաչափությունը կա, պլանները ճիշտ են:</div>
    <div class="write">էջ 12–13. կետ 6-ի տողերը դիրք 3-ի համար, \(\omega_2, \omega_3, \omega_4\), իսկ էջ 13-ի աղյուսակում՝ բոլոր 8 տողերը (մյուս դիրքերի հաշվարկը՝ «13ա» ներդիրում):</div>
  </div>

  <div class="card" id="s7">
    <h2>Քայլ 7 — Արագացումների պլանը (դիրք 3)</h2>
    <h3>Գաղափարը</h3>
    <p>Պտտվող կետի արագացումն ունի երկու մաս.</p>
    <ul>
      <li><b>նորմալ</b> \(a^n = \omega^2\cdot l\)՝ ուղղված դեպի պտտման <b>կենտրոնը</b> (այն «թեքում» է արագությունը): Հաշվվում է, քանի որ ω-ն արդեն գիտենք §2-ից:</li>
      <li><b>շոշափող</b> \(a^t = \varepsilon\cdot l\)՝ ⊥ շառավղին (այն փոխում է արագության <b>մեծությունը</b>): Անհայտ է, որովհետև ε-ն չգիտենք:</li>
    </ul>
    <p>Ուստի յուրաքանչյուր հավասարումում հարաբերական արագացումը բաժանվում է երկու սլաքի՝ հայտնի \(a^n\) և անհայտ մեծությամբ \(a^t\):</p>
    @@APLAN@@
    <p class="cap">Դիրք 3-ի արագացումների պլանը (πb = @@hPIB@@ մմ): n₂, n₃, n₄՝ նորմալ բաղադրիչների ծայրերը:</p>
    <h3>ա) B կետը</h3>
    $$a_B^t = \varepsilon_1\cdot l_{AB} = \frac{d\omega_1}{dt}\cdot l_{AB} = 0\ \ (\omega_1 = \text{const})$$
    $$a_B = a_B^n = \omega_1^2\cdot l_{AB} = @@W1@@^2\cdot@@LAB@@ = @@AB_ACC@@\ \text{մ/վ}^2,\ \ B\to A$$
    $$\mu_a = @@MUA@@\ \frac{\text{մ/վ}^2}{\text{մմ}},\qquad \pi b = \frac{a_B}{\mu_a} = \frac{@@AB_ACC@@}{@@MUA@@} = @@PIB@@\ \text{մմ}$$
    <h3>բ) c կետը — հավասարումներ (1), (2), (3)</h3>
    <p>C-ն գրում ենք <b>երկու</b> կողմից. որպես BC-ի կետ և որպես CD-ի կետ, ու հավասարեցնում.</p>
    $$\vec a_B + \vec a_{CB}^n + \vec a_{CB}^t = \vec a_{CD}^n + \vec a_{CD}^t$$
    $$a_{CB}^n = \omega_2^2\, l_{BC} = @@w2@@^2\cdot@@LBC@@ = @@aCBn@@\ \text{մ/վ}^2 \Rightarrow bn_2 = \frac{@@aCBn@@}{@@MUA@@} = @@bn2@@\ \text{մմ}\ \ (C\to B)$$
    $$a_{CD}^n = \omega_3^2\, l_{CD} = @@w3@@^2\cdot@@LCD@@ = @@aCDn@@\ \text{մ/վ}^2 \Rightarrow \pi n_3 = \frac{@@aCDn@@}{@@MUA@@} = @@pin3@@\ \text{մմ}\ \ (C\to D)$$
    <p><b>Կառուցում.</b> b-ից bn₂ ∥ BC (C-ից B կողմ), n₂-ով՝ ուղիղ ⊥BC: π-ից πn₃ ∥ CD (C-ից D կողմ), n₃-ով՝ ուղիղ ⊥CD: <b>Հատումը c-ն է</b>: Նույն տրամաբանությունը, ինչ արագություններում, միայն յուրաքանչյուր կողմում մի սլաք ավել:</p>
    <h3>գ) e կետը — հավասարում (4)</h3>
    $$\vec a_E = \vec a_C + \vec a_{EC}^n + \vec a_{EC}^t$$
    <p>\(a_E\)-ի ուղղությունը հայտնի է (∥ yy), \(a_{EC}^t\)-ինը՝ ⊥CE, իսկ \(a_{EC}^n\)-ը ուղղված է E-ից C: Քանի որ \(\omega_4^2 l_{CE} = \omega_3^2 l_{CD}\), ունենք \(a_{EC}^n = a_{CD}^n\).</p>
    $$a_{EC}^n = \omega_4^2\, l_{CE} = @@w4@@^2\cdot@@LCD@@ = @@aECn@@\ \text{մ/վ}^2 \Rightarrow cn_4 = \frac{@@aECn@@}{@@MUA@@} = @@cn4@@\ \text{մմ}\ \ (E\to C)$$
    <p><b>Կառուցում.</b> <b>c</b> կետից (ոչ թե e-ից) տանում ենք cn₄ ∥ CE (E-ից C կողմ), n₄-ով՝ ուղիղ ⊥CE, π-ով՝ ուղղաձիգ: Հատումը <b>e</b> կետն է: s₂-ը bc-ի միջնակետն է:</p>
    <h3>դ) Թվերը</h3>
    $$a_C = \pi c\cdot\mu_a = @@pic@@\cdot@@MUA@@ = @@aC@@,\qquad a_E = \pi e\cdot\mu_a = @@pie@@\cdot@@MUA@@ = @@aE@@\ \text{մ/վ}^2$$
    $$a_{S_2} = \pi s_2\cdot\mu_a = @@pis2@@\cdot@@MUA@@ = @@aS2@@\ \text{մ/վ}^2$$
    $$a_{CB}^t = n_2c\cdot\mu_a = @@n2c@@\cdot@@MUA@@ = @@aCBt@@\ \text{մ/վ}^2$$
    $$a_{CD}^t = n_3c\cdot\mu_a = @@n3c@@\cdot@@MUA@@ = @@aCDt@@,\qquad a_{EC}^t = n_4e\cdot\mu_a = @@n4e@@\cdot@@MUA@@ = @@aECt@@\ \text{մ/վ}^2$$
    $$\varepsilon_2 = \frac{a_{CB}^t}{l_{BC}} = @@e2@@,\qquad \varepsilon_3 = \frac{a_{CD}^t}{l_{CD}} = @@e3@@,\qquad \varepsilon_4 = \frac{a_{EC}^t}{l_{CE}} = @@e4@@\ \text{վ}^{-2}$$
    <div class="tip"><b>Ինչու՞ է bn₂-ը գրեթե զրո (@@hbn2@@ մմ).</b> 3-րդ դիրքում bc = @@hbc@@ մմ փոքր է (\(V_{CB}\) = @@hVCB@@ մ/վ, \(\omega_2\) = @@hw2@@ վ⁻¹), ուստի \(a_{CB}^n = \omega_2^2 l_{BC}\)-ն շատ փոքր է, և n₂-ը գրեթե համընկնում է b-ի հետ: Սա կառուցման սխալ չէ: Նույն պատճառով \(a_{EC}^n = a_{CD}^n\), \(cn_4 = \pi n_3\):</div>
    <div class="tip"><b>Ֆիզիկական ստուգում.</b> 3-րդ դիրքում սողնակը իջնում է (\(V_E\) ↓), իսկ \(a_E\)-ն = @@haE@@ մ/վ² ուղղված է <b>վեր</b>. սողնակը արգելակվում է, քանի որ մոտենում է ներքևի եզրին: Տրամաբանական է ✔:</div>
    <div class="write">էջ 14–16. \(a_B\)-ն (\(a_B^t = 0\)-ի բացատրությամբ), (1), (2), (3) հավասարումները աղյուսակներով, \(\mu_a\)-ն և πb-ն, \(bn_2, \pi n_3\), (4)-ը, \(cn_4\), հետո բոլոր \(a\)-երն ու \(\varepsilon\)-երը:</div>
  </div>

  <div class="card" id="s8">
    <h2>Քայլ 8 — Բերված մոմենտը և նրա գրաֆիկը</h2>
    <h3>Ինչու է սա պետք</h3>
    <p>Մեխանիզմի վրա ազդում են երեք արտաքին ուժ՝ \(G_2\) (շարժաթևի կշիռը), \(G_5\) (սողնակի կշիռը) և \(F_r\) (օգտակար դիմադրությունը): Դրանք կիրառված են տարբեր օղակների և շարժվում են տարբեր արագություններով: Հաջորդ բաժիններում (թափանիվ) հարմար է այս ամենը փոխարինել <b>մեկ մոմենտով</b>, որը կիրառված է կռունկի վրա: Այդ պայմանական մոմենտը կոչվում է <b>բերված մոմենտ</b> \(M_P\):</p>
    <div class="tip"><b>Սահմանումը (դասախոսի ձևակերպմամբ).</b> Բերված մոմենտը բերման օղակի (1 կռունկի) վրա կիրառված պայմանական մոմենտ է, որի հզորությունը ժամանակի ցանկացած պահի հավասար է մեխանիզմի օղակների վրա ազդող արտաքին ուժերի հզորությունների հանրահաշվական գումարին:</div>
    <h3>Ինչու հզորություն, ոչ թե աշխատանք</h3>
    <p>Աշխատանքը ուժ × տեղափոխություն է, բայց յուրաքանչյուր օղակի տեղափոխությունը դժվար է իմանալ: Հզորությունը <b>ուժ × արագություն</b> է, իսկ արագություններն արդեն ունենք 8 պլաններից: \(M_P\)-ն ուղղում ենք \(\omega_1\)-ի կողմը, ուստի նրա հզորությունը պարզապես \(M_P\cdot\omega_1\) է.</p>
    $$M_P\cdot\omega_1 = G_2 V_{S_2}\cos\alpha_2 + G_5 V_E\cos\alpha_5 + F_r V_E\cos 180°$$
    $$M_P = G_2\frac{V_{S_2}\cos\alpha_2}{\omega_1} + G_5\frac{V_E\cos\alpha_5}{\omega_1} - F_r\frac{V_E}{\omega_1}$$
    <p>Ուժի հզորությունը <b>դրական</b> է, եթե ուժը օգնում է շարժմանը (անկյունը սուր է), և <b>բացասական</b>, եթե խանգարում է (անկյունը բութ է):</p>
    <h3>ա) G<sub>5</sub>. սողնակի կշիռը</h3>
    <p>Սողնակը շարժվում է ուղղաձիգ, իսկ կշիռը միշտ ներքև է: Երբ սողնակն <b>իջնում է</b> (1–4 դիրքեր), \(\alpha_5 = 0°\), կշիռը «օգնում» է (+): Երբ <b>բարձրանում է</b> (5–7), \(\alpha_5 = 180°\), կշիռը խանգարում է (−): Մեթոդականի օրինակում այս անդամը չկա, որովհետև այնտեղ սողնակը հորիզոնական է շարժվում (\(\cos 90° = 0\)): <b>Մեզ մոտ այն կա</b>:</p>
    <h3>բ) F<sub>r</sub>. օգտակար դիմադրությունը</h3>
    <p>Սա այն ուժն է, որը մեխանիզմը պետք է հաղթահարի: Այն ազդում է միայն աշխատանքային ընթացքում և միշտ ուղղված է շարժմանը հակառակ՝ վեր, մինչդեռ \(V_E\)-ը ներքև է: Դրա համար \(\cos 180° = -1\), և բանաձևում վերջին անդամը մինուսով է:</p>
    <p>Ամեն դիրքի \(F_r\)-ը կարդում ենք թերթ 1-ի F<sub>re</sub> գրաֆիկից. չափում ենք օրդինատը \(y_j\) (մմ) և բազմապատկում մասշտաբով \(\mu_F = F_{re}^{max}/y_{max} = @@FMAX@@/@@YMAXF@@ = @@MUF@@\) Ն/մմ:</p>
    <div class="warn"><b>1-ին դիրքում \(F_r = 0\).</b> 1-ը աշխատանքային ընթացքի մաս է, բայց սողնակը դեռ քիչ է իջել (@@hsE1@@·H<sub>E</sub>), իսկ ուժը սկսվում է մոտ 0,40·H<sub>E</sub>-ից: Ուստի \(F_r \ne 0\) միայն <b>2, 3, 4</b> դիրքերում:</div>
    <h3>գ) G<sub>2</sub>. ps₂·cos α₂-ը՝ առանց անկյունը չափելու</h3>
    <p>\(\alpha_2\)-ը \(G_2\)-ի (ներքև) և \(V_{S_2}\)-ի (պլանում ps₂ սլաքի) միջև անկյունն է: Այն կարելի է չափել անկյունաչափով, բայց դասախոսը խորհուրդ է տալիս ավելի պարզ ձև.</p>
    <ol>
      <li>Պլանում p-ով տար ուղղաձիգ գիծ:</li>
      <li>s₂ կետից իջեցրու ուղղահայաց այդ գծին. ստացվում է ուղղանկյուն եռանկյուն:</li>
      <li>Ուղղաձիգի վրայի էջը հենց \(ps_2\cdot\cos\alpha_2\)-ն է: Չափիր այն քանոնով (մմ):</li>
      <li>Նշանը. եթե այդ էջը p-ից <b>ներքև</b> է (անկյունը սուր է), գրիր «+», եթե <b>վերև</b> է (անկյունը բութ է)՝ «−»:</li>
    </ol>
    @@PROJ@@
    <h3>դ) Ամեն ինչ միլիմետրերով</h3>
    <p>Ամեն արագություն հավասար է պլանի հատվածի և \(\mu_v\)-ի արտադրյալին: Տեղադրելով՝ բոլոր անդամներում հայտնվում է նույն \(\mu_v/\omega_1\) արտադրիչը.</p>
    $$\frac{\mu_v}{\omega_1} = \frac{@@MUV@@}{@@W1@@} = @@KM@@\ \frac{\text{մ}}{\text{մմ}}$$
    $$M_P = @@KM@@\cdot\big[\,@@G2@@\cdot(ps_2\cos\alpha_2) \pm @@G5@@\cdot pe - F_r\cdot pe\,\big]$$
    <p><b>Օրինակ՝ դիրք 3</b> (ps₂·cos α₂ = @@hys2@@ մմ, pe = @@hpe2@@ մմ, F<sub>r</sub> = @@hFr2@@ Ն).</p>
    $$M_{P3} = @@KM@@\cdot\big[@@G2@@\cdot(@@ys2@@) + @@G5@@\cdot @@pe2@@ - @@Fr2@@\cdot @@pe2@@\big] = @@t2@@ + @@t5@@ - @@tr@@ = @@M2@@\ \text{Ն}\cdot\text{մ}$$
    <p>Տես՝ կշիռների անդամները մի քանի Ն·մ են, իսկ \(F_r\)-ինը՝ հարյուրավոր: Դրա համար աշխատանքային ընթացքում մոմենտը մեծ է և բացասական:</p>
    <div class="tbl"><table>
      <tr><th>j</th><th>ps₂·cos α₂, մմ</th><th>pe, մմ</th><th>α₅</th><th>F<sub>r</sub>, Ն</th><th>M<sub>P</sub>, Ն·մ</th><th>գծագրում, մմ</th></tr>
      @@MPROWS@@
    </table></div>
    <div class="tip"><b>Ինքնաստուգում (դասախոսից).</b> 2, 3, 4 դիրքերում \(M_P\)-ն բացասական է, մոդուլով մեծագույնը՝ 2-րդ կամ 3-րդ դիրքում, մնացածում՝ փոքր (դրական կամ բացասական): Մեզ մոտ՝ @@hMMX@@ Ն·մ @@hJMX@@-րդ դիրքում ✔ (3-րդում՝ @@hM3@@): 4-րդում մոմենտը փոքր է (@@hM4@@), որովհետև սողնակը գրեթե կանգնած է (pe = @@hpe4@@ մմ):</div>
    <h3>ե) Գրաֆիկը</h3>
    <p>\(|M_P|_{max}\)-ը ներկայացնում ենք 70–80 մմ-ով (վերցնում ենք @@MPY@@), իսկ կռունկի լրիվ պտույտը՝ 160 մմ-ով (8 դիրք × 20 մմ).</p>
    $$\mu_M = \frac{|M_P|_{max}}{@@MPY@@} = \frac{@@MMAX@@}{@@MPY@@} = @@MUM@@\ \frac{\text{Ն}\cdot\text{մ}}{\text{մմ}},\qquad \mu_\varphi = \frac{2\pi}{160} = \frac{2\cdot3{,}14}{160} = @@MUPHI@@\ \frac{\text{ռադ}}{\text{մմ}}$$
    $$(M_P)_j^{\text{գծ}} = \frac{M_{Pj}}{\mu_M}\quad(\text{իր նշանով})$$
    <div class="mpbox">@@MPG@@</div>
    <p class="cap">Գրաֆիկը քո թվերով: Թղթի վրա այն կառուցվում է A4 միլիմետրական թերթի վրա. տես <a href="#s9">Քայլ 9-ը</a>:</p>
    <div class="warn"><b>Զգույշ.</b> F<sub>re</sub> կորը թվայնացված է առաջադրանքի թերթի նկարից (մոտավոր): Եթե քո գծած գրաֆիկից չափված \(y_j\)-ն տարբերվի, վերահաշվիր 2–4 տողերը: Մեթոդականի 37-րդ էջի աղյուսակը մի արտագրիր. այնտեղ F<sub>r</sub>·V/ω₁ սյունակը մեկ տողով շեղված է:</div>
    <div class="write">էջ 17–18. §4 վերնագիրը, հզորությունների հավասարությունը, \(M_P\)-ի բանաձևը, \(\alpha_5\)-ի և \(F_r\)-ի բացատրությունը, \(\mu_F\), \(\mu_v/\omega_1\), դիրք 3-ի հաշվարկը, աղյուսակը, \(\mu_M\), \(\mu_\varphi\) և գծագրական չափերը:</div>
  </div>

  <div class="card" id="s9">
    <h2>Քայլ 9 — Աշխատանքների և կինետիկ էներգիայի աճի գրաֆիկները</h2>
    <h3>Ինչու է սա պետք</h3>
    <p>Թափանիվը հաշվելու համար պետք է իմանալ, թե կռունկի մեկ պտույտի ընթացքում մեքենայի կինետիկ էներգիան որքանով է տատանվում: Բերված մոմենտը ուժ չէ, մոմենտ է. նրա աշխատանքը ստանալու համար պետք է այն <b>ինտեգրել</b> ըստ պտտման անկյան: Սա անում ենք գրաֆիկորեն (դասախոսի եղանակով):</p>
    <h3>Ինչու է գրաֆիկական ինտեգրումն աշխատում</h3>
    <p>Աշխատանքը մոմենտի գրաֆիկի տակ մնացած մակերեսն է. \(A=\int M_P\,d\varphi\): Մեկ միջակայքում (20 մմ) կորը փոխարինում ենք նրա <b>միջնակետի</b> օրդինատով \(y_m\): Բևեռից P մինչև \((0,\,y_m)\) կետը տարված ճառագայթի թեքությունը \(y_m/OP\) է. եթե նրան զուգահեռ անցնենք 20 մմ դեպի աջ, կբարձրանանք \(y_m\cdot 20/OP\)-ով: Հենց դա էլ \(y_m\)-ին համապատասխանող մակերեսն է՝ արտահայտված նոր մասշտաբով: Քանի որ ինտեգրալը <b>գումարում</b> է մակերեսները, յուրաքանչյուր հաջորդ զուգահեռը սկսվում է նախորդի վերջից.</p>
    $$y_{j'} = y_{(j-1)'} + y_{m}\cdot\frac{20}{OP} = y_{(j-1)'} + y_m\cdot @@K20@@$$
    <p>Մասշտաբը ստանում ենք «միավորների հաշվարկով». մեկ մմ օրդինատը A գրաֆիկում հավասար է \(\mu_M\)-ին (մոմենտ) × \(\mu_\varphi\)-ին (անկյուն) × \(OP\)-ին (բևեռային հեռավորություն).</p>
    $$\mu_A = \mu_M\cdot\mu_\varphi\cdot OP = @@MUM@@\cdot@@MUPHI@@\cdot@@OP@@ = @@MUA_G@@\ \frac{\text{Ջ}}{\text{մմ}}$$
    <h3>Մեր թվերը</h3>
    <p>Միջնակետերի օրդինատները (մմ, վեր՝ +) 0–1, … 7–8 միջակայքերի համար. @@YMIDTXT@@: Շղթան \(0 \to 1' \to \dots \to 8'\) տալիս է \(y_{8'} = @@AR8@@\) մմ (A<sub>r</sub> բացասական է. դիմադրության ուժերը աշխատանք են «խլում»): Աշխատանքը ցիկլում՝</p>
    $$A_r = |y_{8'}|\cdot\mu_A = @@AR8P@@\cdot@@MUA_G@@ = @@ACYC@@\ \text{Ջ}$$
    <h3>Ինչու է A<sub>m</sub> ուղիղ և վերջանում 8″-ում</h3>
    <p>Շարժիչի մոմենտը \(M_m\) հաստատուն է, ուստի \(A_m = M_m\cdot\varphi\) աճում է <b>գծայնորեն</b>: Մեքենան աշխատում է կայուն՝ մեկ ցիկլից հետո նրա արագությունը կրկնվում է, ուստի կինետիկ էներգիան չի փոխվում, այսինքն՝ ցիկլում \(A_m + A_r = 0\): Դրա համար 8-ից <b>վեր</b> դնում ենք \(|y_{8'}|\)՝ ստանում ենք 8″, իսկ 0-ն 8″-ի հետ միացնող ուղիղը A<sub>m</sub>-ն է:</p>
    <h3>Ինչ է ΔE-ն</h3>
    <p>\(\Delta E = A_m + A_r\) կինետիկ էներգիայի աճն է ցանկացած դիրքում (մեթոդականում՝ ΔT): Դրական է, երբ շարժիչը տալիս է ավելին, քան «տանում» է դիմադրությունը՝ թափանիվը արագանում է, բացասական է՝ դանդաղում: Գրաֆիկում՝ \(y_{\Delta E}=y_{A_m}+y_{A_r}\) (օր.՝ \(j=3\)՝ @@AM3@@ @@AR3S@@ = @@DE3@@ մմ), իրական արժեքը՝ \(y\cdot\mu_A\):</p>
    <div class="tbl"><table>
      <tr><th>j</th><th>y<sub>մ</sub></th><th>y<sub>Ar</sub></th><th>y<sub>Am</sub></th><th>y<sub>ΔE</sub>, մմ</th><th>ΔE, Ջ</th></tr>
      @@AROWS@@
    </table></div>
    <h3>M<sub>m</sub>-ը գրաֆիկից</h3>
    <p>A<sub>m</sub>-ի ուղիղը բարձրանում է \(|y_{8'}|\) մմ-ով 160 մմ-ի վրա, ուստի նրա թեքությունը \(|y_{8'}|/160\) է: Ճառագայթի կանոնով՝ թեքություն = \(y/OP\). P-ից A<sub>m</sub>-ին զուգահեռ ճառագայթը M առանցքի վրա կտրում է \(y_{M_m}=|y_{8'}|\cdot OP/160\) հատվածը, իսկ հորիզոնական գիծը այդ բարձրության վրա \(M_m\)-ն է (սա ինտեգրման հակադարձ քայլն է): Մեզ մոտ՝</p>
    $$M_m = y_{M_m}\cdot\mu_M = @@YMM@@\cdot@@MUM@@ = @@MM@@\ \text{Ն·մ}$$
    <div class="tip"><b>Ինքնաստուգում.</b> \(A/2\pi = @@ACYC@@/6{,}28 = @@AOV@@\) Ն·մ ≈ \(M_m\) ✔: Այսինքն՝ գրաֆիկորեն ստացված մոմենտը համընկնում է ցիկլում կատարված աշխատանքի միջինին:</div>
    <p><b>Հետագայում.</b> \(\Delta E_{max}-\Delta E_{min} = @@DEMAX@@-(@@DEMIN@@) = @@DERANGE@@\) Ջ (j = @@JMAX@@ և j = @@JMIN@@ դիրքերում) պետք կգա թափանիվի հաշվարկում:</p>
    <div class="a4box">@@A4G@@</div>
    <p class="cap">A4 թերթը քո թվերով (1 մմ = 1 մմ): Ֆայլերը՝ <a href="chertej_A4_graf.pdf">PDF</a>, <a href="chertej_A4_graf.png">PNG</a>:</p>
    <div class="warn"><b>Զգույշ.</b> Միջնակետերի օրդինատները կարդում ես քո գծած կորից, ուստի ±1 մմ տարբերությունը նորմալ է. այդ դեպքում շղթան, A<sub>m</sub>-ը, ΔE-ն և M<sub>m</sub>-ը վերահաշվիր նույն բանաձևերով:</div>
    <div class="write">էջ 19–20. §5 վերնագիրը, OP, \(\mu_A\), միջնակետերի օրդինատները, \(y_{j'}\) շղթան, A<sub>m</sub>-ի ուղիղը, ΔE աղյուսակը, A, \(M_m\), \(\Delta E_{max}-\Delta E_{min}\):</div>
  </div>

  <div class="card" id="s10">
    <h2>Քայլ 10 — Բերված իներցիայի մոմենտը</h2>
    <h3>Ինչու է սա պետք</h3>
    <p>Թափանիվը հաշվելու համար պետք է իմանալ ոչ միայն, թե ինչպես է փոխվում էներգիան (Քայլ 9), այլ նաև, թե <b>որքան «իներտ» է ամբողջ մեքենան</b>: Բայց մեխանիզմի օղակները շարժվում են տարբեր արագություններով՝ կռունկը պտտվում է, շարժաթևը «պտտվում և սահում է», սողնակը միայն շարժվում է վեր ու վար: Ամեն օղակի իներցիան առանձին հաշվելու փոխարեն ամբողջ մեխանիզմը փոխարինում ենք <b>մեկ պայմանական օղակով</b>՝ կռունկով:</p>
    <div class="tip"><b>Սահմանումը (դասախոսի ձևով).</b> Բերված իներցիայի մոմենտ \(I_P\)-ն բերման օղակի (կռունկի) պայմանական իներցիայի մոմենտ է, որի կինետիկ էներգիան \(I_P\omega_1^2/2\) ամեն պահի հավասար է ամբողջ մեխանիզմի կինետիկ էներգիային:</div>
    <h3>Օղակների կինետիկ էներգիաները</h3>
    <ul>
      <li><b>Կռունկ 1.</b> արդեն բերման օղակն է, դրա իներցիան այստեղ չի հաշվվում (առաջադրանքում տրված չէ):</li>
      <li><b>Շարժաթև 2 (BC).</b> հարթ շարժում. պտույտ ծանրության կենտրոնի շուրջը՝ \(I_{S_2}\omega_2^2/2\), գումարած համընթաց շարժում S<sub>2</sub> կետի արագությամբ՝ \(m_2V_{S_2}^2/2\):</li>
      <li><b>Սողնակ 5.</b> միայն համընթաց. \(m_5V_E^2/2\) (մեր տարբերակում սողնակի կետը E-ն է):</li>
    </ul>
    <h3>Արտածումը</h3>
    $$I_P\frac{\omega_1^2}{2} = m_2\frac{V_{S_2}^2}{2} + I_{S_2}\frac{\omega_2^2}{2} + m_5\frac{V_E^2}{2}$$
    <p>Բազմապատկում ենք 2-ով և բաժանում \(\omega_1^2\)-ի վրա.</p>
    $$I_P = m_2\left(\frac{V_{S_2}}{\omega_1}\right)^2 + I_{S_2}\left(\frac{\omega_2}{\omega_1}\right)^2 + m_5\left(\frac{V_E}{\omega_1}\right)^2$$
    <p>Նոր չափում պետք չէ. \(V_{S_2} = ps_2\cdot\mu_v\), \(\omega_2 = V_{CB}/l_{BC}\), \(V_E = pe\cdot\mu_v\) արդեն կան Քայլ 5–6-ի աղյուսակներում: Միակ անհայտը \(I_P\)-ն է:</p>
    <h3>Մեր թվերը</h3>
    <p>Զանգվածները՝ \(m = G/g\), դասախոսն ասաց վերցնել \(g = @@GACC@@\) մ/վ²; \(I_{S_2}\)՝ աղյուսակի արժեքը ×10⁻³.</p>
    $$m_2 = \frac{@@G2@@}{@@GACC@@} = @@IM2@@\ \text{կգ},\quad m_5 = \frac{@@G5@@}{@@GACC@@} = @@IM5@@\ \text{կգ},\quad I_{S_2} = @@IS2R@@\cdot10^{-3} = @@IIS2@@\ \text{կգ·մ}^2,\quad \omega_1 = @@W1@@\ \text{վ}^{-1}$$
    <p><b>Օրինակ՝ դիրք 3</b> (\(V_{S_2} = @@IVS2@@\) մ/վ, \(\omega_2 = @@IW2@@\) վ⁻¹, \(V_E = @@IVE@@\) մ/վ).</p>
    $$I_{P3} = @@IM2@@\cdot@@IA@@ + @@IIS2@@\cdot@@IB@@ + @@IM5@@\cdot@@IFF@@ = @@IT2@@ + @@ITW@@ + @@IT5@@ \approx @@II2@@\ \text{կգ·մ}^2$$
    <div class="tbl"><table>
      <tr><th>j</th><th>(V<sub>S₂</sub>/ω₁)²</th><th>(ω₂/ω₁)²</th><th>(V<sub>E</sub>/ω₁)²</th><th>I<sub>P</sub>, կգ·մ²</th><th>գծագրում, մմ</th></tr>
      @@IPROWS@@
    </table></div>
    <h3>Ինչու է առավելագույնը պարապ ընթացքում</h3>
    <p>\(I_P\) մեծ է այնտեղ, որտեղ օղակները արագ են շարժվում (անդամները արագությունների քառակուսիներ են): Պարապ ընթացքը (դիրքեր 5–7) ավելի արագ է, քան աշխատանքայինը, ուստի տրամաբանորեն առավելագույնը այնտեղ է: Մեզ մոտ՝ <b>j = @@hJIMAX@@</b>-ում, \(I_{P\,max} = @@IMAX@@\) կգ·մ²: Եթե քո չափումներով մի փոքր այլ դիրք ստացվի, գրիր այն, ինչ ստացել ես:</p>
    <div class="warn"><b>Երկու նշում.</b> 1) Մեթոդականի օրինակում \(g = 9{,}8\), իսկ դասախոսն ասաց վերցնել 10. վերցրել ենք 10: 2) \(I_{S_2}\)-ի միավորը լուսանկարում վատ էր երևում. դասախոսն ասաց ×10⁻³, այսինքն՝ @@hIS2@@ կգ·մ²:</div>
    <h3>Գրաֆիկը և ինչու է այն շրջված</h3>
    <p>\(I_{P\,max}\)-ը ներկայացնում ենք @@IYMAX@@ մմ-ով, φ-ն՝ 160 մմ-ով (ինչպես նախորդ գրաֆիկներում).</p>
    $$\mu_I = \frac{I_{P\,max}}{@@IYMAX@@} = \frac{@@IMAX@@}{@@IYMAX@@} = @@IMUI@@\cdot10^{-4}\ \frac{\text{կգ·մ}^2}{\text{մմ}},\qquad (I_P)_j^{\text{գծ}} = \frac{I_{Pj}}{\mu_I}$$
    <p>Գրաֆիկը գծում ենք <b>90°-ով շրջված</b> (մեթոդականի նկ. 14). \(I_P\)-ի առանցքը հորիզոնական է, φ-ինը՝ ուղղաձիգ՝ ներքև, 20 մմ-ը մեկ դիրքի համար: Շրջում ենք, որովհետև հաջորդ քայլում φ-ն «արտաքսվելու» է. \(\Delta T(\varphi)\)-ից և \(I_P(\varphi)\)-ից կստացվի մեկ գրաֆիկ \(\Delta T(I_P)\) (էներգիա–զանգված դիագրամ), որից էլ որոշվում է թափանիվը: Այդ քայլը դասախոսը դեռ չի բացատրել, ուստի թերթի վրա դրա համար ազատ տեղ է թողնված:</p>
    <div class="a3box">@@A3G@@</div>
    <p class="cap">Թերթ 4-ը քո թվերով (A3, 1 մմ = 1 մմ): Աջում՝ \(I_P(\varphi)\), ձախում՝ \(\Delta T(\varphi)\) (= ΔE): Ֆայլերը՝ <a href="chertej_A3_4.pdf">PDF</a>, <a href="chertej_A3_4.png">PNG</a>:</p>
    <div class="write">էջ 21–22. §6 վերնագիրը, էներգիաների հավասարությունը և \(I_P\)-ի բանաձևը, \(m_2, m_5, I_{S_2}, \omega_1\), դիրք 3-ի հաշվարկը, աղյուսակ 4, \(\mu_I\), \(\mu_\varphi\) և գծագրական չափերը:</div>
  </div>

  <div class="card" id="fre">
    <h2>F<sub>re</sub> գրաֆիկը և թերթերը</h2>
    <h3>F<sub>re</sub> գրաֆիկը</h3>
    <p>Սա <b>օգտակար դիմադրության ուժն</b> է՝ այն, ինչ սողնակը «հաղթահարում է» (օրինակ՝ մետաղը դրոշմելիս): Այն գործում է <b>միայն աշխատանքային ընթացքում</b> (սողնակը իջնում է) և ուղղված է շարժմանը հակառակ: Գրաֆիկի ձևը արտագծում ես առաջադրանքի թերթից՝ S<sub>E</sub> առանցքը դնելով ուղղորդին զուգահեռ, որ յուրաքանչյուր Eᵢ-ից հորիզոնական գծով անմիջապես կարդաս F<sub>re</sub>-ն: Մասշտաբը՝ \(\mu_F = @@FMAX@@/@@YMAXF@@ = @@MUF@@\) Ն/մմ: Կինեմատիկային պետք չէ, բայց ամեն դիրքի F<sub>r</sub>-ը պետք է <a href="#s8">բերված մոմենտի</a> համար:</p>
    <h3>Ինչ կա ամեն թերթում</h3>
    <div class="two">
      <div class="tip"><b>Թերթ 1.</b> դիրքերի պլանը (8 դիրք, 3-րդը՝ հաստ), եզրային դիրքերի կառուցումը, L₁*, L₂*, H<sub>E</sub>* չափերը, F<sub>re</sub> գրաֆիկը և դիրք 3-ի <b>արագացումների պլանը</b>:</div>
      <div class="tip"><b>Թերթ 2.</b> <b>8 արագությունների պլան</b>, 4 × 2 վանդակներում (վերևում՝ 0–3, ներքևում՝ 4–7), բոլորը նույն μ<sub>v</sub>-ով և pb = @@hPB@@ մմ:</div>
    </div>
  </div>

  <div class="card" id="assume">
    <h2>Ենթադրություններ — սրանք ճշտիր դասախոսի մոտ</h2>
    <div class="tbl">
    <table>
      <tr><th>Ինչ</th><th>Ընդունված</th><th>Կփոխի՞ արդյունքը</th></tr>
      <tr><td>β անկյունը</td><td>3° (թույլատրված 3°÷5°)</td><td>Այո, մի փոքր. կփոխվեն եզրային դիրքերը, AB-ն, BC-ն և բոլոր թվերը: Եթե դասախոսն այլ β ասի, ամեն ինչ պետք է վերահաշվել:</td></tr>
      <tr><td>Կռունկի պտույտի ուղղությունը</td><td>ժամացույցի սլաքի հակառակ (↺)</td><td>Եթե սխեմայում հակառակն է, պլանները կլինեն «հայելային», իսկ աշխատանքային ու պարապ ընթացքները՝ տեղերով փոխված:</td></tr>
      <tr><td>μ<sub>v</sub> և μ<sub>a</sub></td><td>@@hMUV@@ և @@hMUA@@ (pb = @@hPB@@, πb = @@hPIB@@ մմ)</td><td>Ոչ. փոխվում է միայն պլանի չափը, արագություններն ու արագացումները նույնն են:</td></tr>
      <tr><td>Հաստ (արագացումների) դիրքը</td><td>3-րդ</td><td>Եթե այլ դիրք պահանջվի, բոլոր դիրքերի արագացումները արդեն կան <code>TMM_Variant13.html</code>-ի աղյուսակներում:</td></tr>
      <tr><td>\(I_{S_2}\)-ի միավորը</td><td>@@IS2R@@·10⁻³ = @@IS2SI@@ կգ·մ² (դասախոսն ասաց ×10⁻³)</td><td>Կինեմատիկայի համար ոչ, Քայլ 10-ի համար՝ այո:</td></tr>
      <tr><td>F<sub>re</sub> կորի ձևը</td><td>թվայնացված է առաջադրանքի թերթի նկարից (սկիզբը՝ ≈ 0,40·H<sub>E</sub>, առավելագույնը՝ ≈ 0,85·H<sub>E</sub>)</td><td>Կինեմատիկայի համար ոչ. բերված մոմենտի 2–4 դիրքերում՝ մոտավոր:</td></tr>
    </table>
    </div>
  </div>

  <div class="card" id="check">
    <h2>Ստուգաթերթ և տարածված սխալներ</h2>
    <h3>Տետրի հերթականությունը (ինչպես նմուշում)</h3>
    <ol>
      <li>էջ 10. տվյալների աղյուսակ, պայմաններ 1–5, §1-ի վերնագիր, \(\mu_l\), \(H_E^*\), \(L_2^*\)</li>
      <li>էջ 11. \(CD^*\), ψ, «±» համակարգը, AB, BC, \(l_{AB}, l_{BC}\), §2. \(V_B\), հավասարում (1)</li>
      <li>էջ 12. (2) հավասարում \(V_E\)-ի համար, \(bs_2 = cs_2\), \(\mu_v\), կետ 6 (դիրք 3)</li>
      <li>էջ 13. \(\omega_3, \omega_4\) և 8 դիրքերի աղյուսակը (+ «13ա» ներդիր)</li>
      <li>էջ 14–16. §3. արագացումներ դիրք 3-ի համար</li>
      <li>էջ 17–18. §4. բերված մոմենտ, աղյուսակ, \(\mu_M\), \(\mu_\varphi\), գծագրական չափեր</li>
      <li>էջ 19–20. §5. աշխատանքների և ΔE-ի գրաֆիկները</li>
      <li>էջ 21–22. §6. բերված իներցիայի մոմենտ, աղյուսակ 4, \(\mu_I\)</li>
    </ol>
    <p>Յուրաքանչյուր տողի համար՝ <b>բանաձև → տեղադրված թվեր → արդյունք՝ միավորով</b>:</p>
    <h3>Ստուգումներ, որոնք ապացուցում են, որ ճիշտ ես արել</h3>
    <ul>
      <li>\(BC - AB = AC_0\) և \(AB + BC = AC_0'\) (@@BC@@ − @@AB@@ = @@AC0@@, @@AB@@ + @@BC@@ = @@AC0P@@)</li>
      <li>Գծագրում սողնակի ընթացքը ճիշտ @@H@@ մմ է (= \(H_E^*\))</li>
      <li>Բոլոր 8 պլաններում pb = @@hPB@@ մմ, և pb ⊥ համապատասխան AB-ին</li>
      <li>\(ce = pc\) և pe-ն ուղղաձիգ բոլոր դիրքերում</li>
      <li>0-րդ դիրքում c, e ≡ p</li>
      <li>\(V_E\)-ն ↓ 1–4 դիրքերում, ↑ 5–7-ում</li>
      <li>\(a_E\)-ն 3-րդ դիրքում ուղղված է վեր (արգելակում)</li>
      <li>\(M_P < 0\) 2, 3, 4 դիրքերում, \(|M_P|_{max}\)-ը՝ 2-րդ կամ 3-րդ դիրքում, մյուսներում՝ փոքր</li>
    </ul>
    <h3>Տարածված սխալներ</h3>
    <ul>
      <li>\(V_C\)-ն տանել ⊥BC՝ ⊥CD-ի փոխարեն: C-ն պտտվում է <b>D</b>-ի շուրջը, ուստի \(\vec V_C\perp CD\), իսկ ⊥BC-ն հարաբերական \(\vec V_{CB}\)-ի ուղղությունն է:</li>
      <li>e-ն գտնել c-ից ⊥CE-ով, բայց p-ից ուղղաձիգի փոխարեն թեք գիծ տանել. \(V_E\)-ն միշտ ∥ yy է:</li>
      <li>Նորմալ արագացումը տանել սխալ կողմ. \(a^n\)-ը միշտ դեպի <b>կենտրոն</b> է՝ C→B, C→D, E→C:</li>
      <li>Արագացումների պլանում n₄-ը դնել e-ից. այն c-ից է (\(\vec a_E = \vec a_C + \dots\)):</li>
      <li>Մոռանալ, որ \(a_B^t = 0\) (ω<sub>1</sub> = const), և փնտրել ε<sub>1</sub>:</li>
      <li>Տարբեր դիրքերի պլանները գծել տարբեր μ<sub>v</sub>-ով. բոլորը նույն @@hMUV@@-ով են:</li>
      <li>Միավորներ. ω-ն վ⁻¹ (ռադ/վ), ε-ն՝ վ⁻², արագացումները՝ մ/վ²:</li>
      <li>§4-ում մոռանալ G<sub>5</sub>-ի անդամը (մեթոդականի օրինակում այն չկա, մեզ մոտ՝ կա) կամ նրա նշանը պարապ ընթացքում (−):</li>
      <li>F<sub>r</sub> դնել 1-ին կամ 5–7 դիրքերում. այն ≠ 0 միայն 2, 3, 4-ում:</li>
      <li>ps₂·cos α₂-ի նշանը. p-ից վերև եղած պրոյեկցիան գրվում է մինուսով:</li>
    </ul>
  </div>
@@ROTATOR@@
</div>
</body>
</html>
'''

out = HTML
for k, v_ in R.items(): out = out.replace(f'@@{k}@@', v_)
for k, v_ in TXT.items(): out = out.replace(f'@@{k}@@', v_)
out = (out.replace('@@MECH@@', mech_svg()).replace('@@EXTREME@@', extreme_svg())
          .replace('@@VPLAN@@', plan_svg('v')).replace('@@APLAN@@', plan_svg('a')).replace('@@VROWS@@', vel_rows).replace('@@ROTATOR@@', rotator_html())
          .replace('@@AROWS@@', AROWS).replace('@@A4G@@', a4_sheet()).replace('@@A3G@@', a3_sheet4()).replace('@@IPROWS@@', IPROWS).replace('@@MPROWS@@', MPROWS).replace('@@MPG@@', mp_graph()).replace('@@PROJ@@', '<div class="projbox">' + PROJ_SVG + '</div>'))
assert '@@' not in out, out[out.index('@@')-40:out.index('@@')+40]
HERE = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(HERE, '..', 'bacatrutyun.html'), 'w').write(out)
print('written', len(out))
