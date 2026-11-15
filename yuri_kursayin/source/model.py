"""Task 1, variant 16 — six-link linkage (crank AB, coupler BC, rocker CD, rod CE, slider E on the vertical through D):
synthesis, positions, velocity & acceleration plans, sheet layout."""
import math

# ---------------- task data (variant 16) ----------------
TASK = 1
VARIANT = 16
DATA = dict(HE=85, L1=220, L2=200, lCD=190, n1=80, G2=180, G5=480, IS2=80, Fmax=77)
HE = DATA['HE']/1000; L1 = DATA['L1']/1000; L2 = DATA['L2']/1000
lCD = DATA['lCD']/1000; lCE = lCD; n1 = DATA['n1']
FMAX = DATA['Fmax']*100.0
BETA = 3.0            # chosen from 3..5 deg: DC0' deviates from the guide by beta
L1S = 110.0           # drawing length chosen for L1
MU = L1/L1S           # 0.002 m/mm
MUV = 0.008           # (m/s)/mm  -> pb ≈ 50 mm
MUA = 0.05            # (m/s^2)/mm
MUF = 200.0           # N/mm
NPOS = 8
CCW = True            # crank turns counter-clockwise (as in the example sheet: B0 -> 1 -> 2 -> 3 over the top)

# ---------------- helpers ----------------
def circ_int(c1, r1, c2, r2):
    dx, dy = c2[0]-c1[0], c2[1]-c1[1]; d = math.hypot(dx, dy)
    a = (r1*r1-r2*r2+d*d)/(2*d); h = math.sqrt(max(r1*r1-a*a, 0))
    ux, uy = dx/d, dy/d; px, py = c1[0]+a*ux, c1[1]+a*uy
    return (px-h*uy, py+h*ux), (px+h*uy, py-h*ux)
def sub(p, q): return (p[0]-q[0], p[1]-q[1])
def add(p, q): return (p[0]+q[0], p[1]+q[1])
def scl(p, s): return (p[0]*s, p[1]*s)
def mag(v): return math.hypot(v[0], v[1])
def cross_k(w, r): return (-w*r[1], w*r[0])
def solve2(a11, a12, a21, a22, b1, b2):
    det = a11*a22-a12*a21; return ((b1*a22-a12*b2)/det, (a11*b2-b1*a21)/det)
def ang(v): return math.degrees(math.atan2(v[1], v[0]))
def polar(c, r, a): return (c[0]+r*math.cos(math.radians(a)), c[1]+r*math.sin(math.radians(a)))

# ---------------- synthesis (drawing mm, D at origin, y up) ----------------
H = HE/MU; L2S = L2/MU; CD = lCD/MU; CE = CD
D = (0.0, 0.0); A = (L1S, -L2S)
# lower extreme: DC0' is beta from the guide (towards A); E0' straight below D, DE0' = 2·CD·cos(beta)
C0p = polar(D, CD, -90+BETA)
E0p = (0.0, 2*C0p[1])
E0 = (0.0, E0p[1]+H)                                 # upper extreme, H_E higher
GAM0 = math.degrees(math.acos(-E0[1]/(2*CD)))        # angle of DC0 from the guide
C0 = polar(D, CD, -90+GAM0)
PSI = GAM0-BETA
AC0 = math.dist(A, C0); AC0p = math.dist(A, C0p)
# C0 – folded (A between B0 and C0): BC − AB = AC0;  C0' – extended (B0' between A and C0'): AB + BC = AC0'
ABS = (AC0p-AC0)/2; BCS = (AC0p+AC0)/2
TH0 = ang(sub(A, C0))            # direction A -> B0 (away from C0)
TH0P = ang(sub(C0p, A))          # direction A -> B0'
B0 = polar(A, ABS, TH0); B0p = polar(A, ABS, TH0P)
SGN = 1 if CCW else -1
PHI_W = (SGN*(TH0P-TH0)) % 360; PHI_I = 360-PHI_W
AD = math.hypot(L1, L2)

W1 = math.pi*n1/30

def position(theta, Cprev):
    B = polar(A, ABS, theta)
    q1, q2 = circ_int(B, BCS, D, CD)
    C = q1 if math.dist(q1, Cprev) < math.dist(q2, Cprev) else q2
    E = (0.0, 2*C[1])                                # isosceles DCE (CE = CD), E on the guide x = 0
    S2 = ((B[0]+C[0])/2, (B[1]+C[1])/2)
    return dict(B=B, C=C, E=E, S2=S2, theta=theta)

def kinematics(P):
    rAB = scl(sub(P['B'], A), MU); rCB = scl(sub(P['C'], P['B']), MU); rCD = scl(sub(P['C'], D), MU)
    rEC = scl(sub(P['E'], P['C']), MU)
    W = SGN*W1
    VB = cross_k(W, rAB)
    w2, w3 = solve2(-rCB[1], rCD[1], rCB[0], -rCD[0], -VB[0], -VB[1])
    VC = cross_k(w3, rCD); VCB = cross_k(w2, rCB)
    w4 = VC[0]/rEC[1]; VEC = cross_k(w4, rEC); VE = add(VC, VEC)
    VS2 = scl(add(VB, VC), 0.5)
    aB = scl(rAB, -W1*W1)
    rhs = sub(scl(rCD, -w3*w3), sub(aB, scl(rCB, w2*w2)))
    e2, e3 = solve2(-rCB[1], rCD[1], rCB[0], -rCD[0], rhs[0], rhs[1])
    aCBn = scl(rCB, -w2*w2); aCBt = cross_k(e2, rCB); aCDn = scl(rCD, -w3*w3); aCDt = cross_k(e3, rCD)
    aC = add(aCDn, aCDt)
    aECn = scl(rEC, -w4*w4); e4 = (aC[0]+aECn[0])/rEC[1]; aECt = cross_k(e4, rEC)
    aE = add(add(aC, aECn), aECt); aS2 = scl(add(aB, aC), 0.5)
    return dict(VB=VB, VC=VC, VCB=VCB, VE=VE, VEC=VEC, VS2=VS2, w2=w2, w3=w3, w4=w4,
                aB=aB, aCBn=aCBn, aCBt=aCBt, aCDn=aCDn, aCDt=aCDt, aC=aC, aECn=aECn, aECt=aECt,
                aE=aE, aS2=aS2, e2=e2, e3=e3, e4=e4)

POS = []; _Cp = C0
for i in range(NPOS):
    P = position(TH0+SGN*360.0/NPOS*i, _Cp); _Cp = P['C']
    P['K'] = kinematics(P); P['i'] = i
    P['sE'] = E0[1]-P['E'][1]
    POS.append(P)
POS0P = position(TH0P, C0p)
def working(i): return 0 < SGN*((POS[i]['theta']-TH0)*SGN % 360) < PHI_W   # between B0 and B0' (slider goes down)

# transmission angle over a full turn
GAMMA_MIN = 180.0; CE_INC_MAX = 0.0; _Cp = C0
for k in range(3600):
    P = position(TH0+SGN*0.1*k, _Cp); _Cp = P['C']
    u = sub(P['B'], P['C']); v = sub(D, P['C'])
    g = math.degrees(math.acos(max(-1, min(1, (u[0]*v[0]+u[1]*v[1])/(mag(u)*mag(v))))))
    GAMMA_MIN = min(GAMMA_MIN, g, 180-g)
    CE_INC_MAX = max(CE_INC_MAX, math.degrees(math.asin(abs(P['C'][0])/CE)))

# ---------------- F_re diagram (shape digitised from the task sheet: starts at ≈0.4·H_E, max near 0.85·H_E) ----------------
FRE_PTS = [(0.0, 0.0), (0.40, 0.0), (0.48, 0.42), (0.60, 0.71), (0.73, 0.89), (0.85, 1.0), (0.94, 0.97), (1.0, 0.88)]
def _pchip_slopes(xs, ys):
    n = len(xs); h = [xs[i+1]-xs[i] for i in range(n-1)]; dl = [(ys[i+1]-ys[i])/h[i] for i in range(n-1)]
    m = [0.0]*n; m[0] = dl[0]; m[-1] = dl[-1]
    for i in range(1, n-1):
        if dl[i-1]*dl[i] <= 0: m[i] = 0.0
        else:
            w1 = 2*h[i]+h[i-1]; w2 = h[i]+2*h[i-1]; m[i] = (w1+w2)/(w1/dl[i-1]+w2/dl[i])
    return m
_xs = [p[0] for p in FRE_PTS]; _ys = [p[1] for p in FRE_PTS]; _ms = _pchip_slopes(_xs, _ys)
def fre_shape(s):
    s = max(0.0, min(1.0, s))
    for i in range(len(_xs)-1):
        if _xs[i] <= s <= _xs[i+1]:
            hh = _xs[i+1]-_xs[i]; t = (s-_xs[i])/hh
            h00 = 2*t**3-3*t**2+1; h10 = t**3-2*t**2+t; h01 = -2*t**3+3*t**2; h11 = t**3-t**2
            return max(0.0, h00*_ys[i]+h10*hh*_ms[i]+h01*_ys[i+1]+h11*hh*_ms[i+1])
    return 0.0

# ---------------- sheet layout (mm, origin = bottom-left corner of the grid) ----------------
GRID_W, GRID_H = 380, 270
XD, YD = 34.0, 258.0
def S(p): return (XD+p[0], YD+p[1])
PA_POS = 3                                                    # working position (as in the example sheet)
PA = (290.0, 165.0)                                           # acceleration-plan pole (sheet 1)
DIAG_X = 74.0                                                 # S_E axis of the F_re diagram
L1_DIM_Y = 44.0; L2_DIM_X = 222.0; HE_DIM_X = 22.0

def vplan(i):
    K = POS[i]['K']; s = 1/MUV
    return dict(p=(0.0, 0.0), b=scl(K['VB'], s), c=scl(K['VC'], s), e=scl(K['VE'], s), s2=scl(K['VS2'], s))
def aplan(i):
    K = POS[i]['K']; s = 1/MUA
    b = scl(K['aB'], s); c = scl(K['aC'], s)
    return dict(pi=(0.0, 0.0), b=b, n2=add(b, scl(K['aCBn'], s)), c=c, n3=scl(K['aCDn'], s),
                n4=add(c, scl(K['aECn'], s)), e=scl(K['aE'], s), s2=scl(K['aS2'], s))

# sheet 2: the 8 velocity plans, 4 per row, each centred in its cell
V2_COLS = (50.0, 143.0, 236.0, 329.0); V2_ROWS = (196.0, 78.0)
def _plan_center(i):
    pts = list(vplan(i).values()); xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return ((min(xs)+max(xs))/2, (min(ys)+max(ys))/2)
PV2 = {}
VLBL = {(3, 's2'): (5.0, -4.5), (3, 'b'): (-3.5, -3.5), (3, 'c'): (-3.4, 2.4), (4, 's2'): (-3.6, 0.0), (7, 'c'): (3.4, 2.8), (7, 's2'): (4.4, -0.4), (7, 'b'): (3.4, -3.6), (5, 'p'): (-5.5, 0.0)}                                                     # hand-placed labels where points crowd: {(i, key): (dx, dy)}
for _i in range(NPOS):
    _c = _plan_center(_i); _cx = V2_COLS[_i % 4]; _cy = V2_ROWS[_i // 4]
    PV2[_i] = (round(_cx-_c[0], 1), round(_cy-_c[1], 1))

if __name__ == '__main__':
    print(f"mu={MU} H*={H:.3f} L2*={L2S:.3f} CD*={CD:.3f}")
    print(f"C0={C0} C0'={C0p} E0={E0} E0'={E0p} gam0={GAM0:.3f} psi={PSI:.3f}")
    print(f"AC0={AC0:.3f} AC0'={AC0p:.3f} AB*={ABS:.3f} BC*={BCS:.3f} phiW={PHI_W:.3f} gamma_min={GAMMA_MIN:.2f} CEinc={CE_INC_MAX:.2f}")
    print('W1', W1, 'VB', W1*ABS*MU, 'aB', W1**2*ABS*MU)
    for P in POS:
        K = P['K']
        print(P['i'], working(P['i']), f"th={P['theta']:.1f} sE={P['sE']:.2f} s={P['sE']/H:.3f} fre={fre_shape(P['sE']/H):.3f}",
              f"VE={K['VE'][1]:+.4f} aE={K['aE'][1]:+.3f} w3={K['w3']:+.3f} e3={K['e3']:+.2f}")
    for i in range(NPOS): print('v', i, 'pole', PV2[i], {k: tuple(round(c, 1) for c in p) for k, p in vplan(i).items()})
    print('a3', {k: tuple(round(c, 1) for c in p) for k, p in aplan(3).items()})
    print('sheet D', S(D), 'A', S(A), 'E0', S(E0), "E0'", S(E0p), 'C0', S(C0), "C0'", S(C0p))
