import numpy as np
from scipy.optimize import minimize
rng=np.random.default_rng(0)
J=np.array([[0,-1],[1,0.]])
print("C1 skew diffusive coupling: eig(-d I - g K) real parts for g in", [0.1,1,10,100])
d=0.5
K=np.zeros((4,4));K[:2,:2]=J;K[2:,2:]=2*J
for g in [0.1,1,10,100]:
    print(g, np.round(np.linalg.eigvals(-d*np.eye(4)-g*K).real.max(),3), "DC transfer (dI+gK)^-1 gK dist to I:", np.round(np.linalg.norm(np.linalg.solve(d*np.eye(4)+g*K,g*K)-np.eye(4),2),4))
print("C2 skew forcing x'=-d x + g J u, circular u=(cos wt, sin wt): steady x is u rotated 90deg = u delayed quarter period")
w=1.0;g=1.0
# steady state: x = g/(d+iw) * J u in complex form; check lagged corr
t=np.linspace(0,200,200001);dt=t[1]-t[0]
u=np.stack([np.cos(w*t),np.sin(w*t)],1);x=np.zeros_like(u)
for k in range(1,len(t)):x[k]=x[k-1]+dt*(-d*x[k-1]+g*J@u[k-1])
s=len(t)//2
def cc(lag):
    L=int(lag/dt);a=u[s:len(t)-L];b=x[s+L:]
    return np.sum(a*b)/np.sqrt(np.sum(a*a)*np.sum(b*b))
lags=np.linspace(0,2*np.pi,64);c=[cc(l) for l in lags]
print(" zero-lag copy corr",round(cc(0),3)," max lagged corr",round(max(c),3),"at lag",round(lags[int(np.argmax(c))],2))
# reversible u: independent OU channels
u2=np.zeros((len(t),2));x2=np.zeros_like(u2)
for k in range(1,len(t)):
    u2[k]=u2[k-1]-dt*u2[k-1]+np.sqrt(dt)*rng.standard_normal(2)
    x2[k]=x2[k-1]+dt*(-d*x2[k-1]+g*J@u2[k-1])
def cc2(L):
    a=u2[s:len(t)-L] if L>=0 else u2[s-L:];b=x2[s+L:] if L>=0 else x2[s:len(t)+L]
    return np.sum(a*b)/np.sqrt(np.sum(a*a)*np.sum(b*b))
print(" reversible OU partner: same-channel corr at lags -2..2 s:",[round(cc2(int(l/dt)),3) for l in [-2,-1,0,1,2]])
print("C3 two skew stages in series: J @ J.T =",(J@J.T).tolist(), " (identity: copy).  J@J =",(J@J).tolist()," (anti-copy)")
print("C4 strictly upper-triangular N (n=6): min copy defect ||(N - I)Q|| on 2-dim U vs norm bound B")
n=6;iu=np.triu_indices(n,1)
def defect(p,B):
    N=np.zeros((n,n));N[iu]=p[:len(iu[0])]
    nn=np.linalg.norm(N,2)
    if nn>B:N*=B/nn
    Q,_=np.linalg.qr(p[len(iu[0]):].reshape(n,2))
    return np.linalg.norm((N-np.eye(n))@Q,2)
for B in [0.5,1,2,5,20,100]:
    best=min(minimize(defect,rng.standard_normal(len(iu[0])+2*n)*B,args=(B,),method='Nelder-Mead',options={'maxiter':20000,'xatol':1e-8,'fatol':1e-10}).fun for _ in range(12))
    print(" B",B," min defect",round(best,4))
print("C5 trace theorem: A with tr A>=0, random traceless K, any g: is -?(A - gK) ever Hurwitz?")
cnt=0
for _ in range(20000):
    A=rng.standard_normal((4,4));A-=np.eye(4)*(np.trace(A)/4); A+=np.eye(4)*0.0  # tr A = 0
    K=rng.standard_normal((4,4));K-=np.eye(4)*np.trace(K)/4
    g=10**rng.uniform(-2,3)
    if np.linalg.eigvals(A-g*K).real.max()<0:cnt+=1
print(" Hurwitz count (should be 0):",cnt)
cnt=0
for _ in range(20000):
    A=rng.standard_normal((4,4));A-=np.eye(4)*(np.trace(A)/4+0.3)
    K=rng.standard_normal((4,4));K-=np.eye(4)*np.trace(K)/4
    g=10**rng.uniform(-2,3)
    if np.linalg.eigvals(A-g*K).real.max()<0:cnt+=1
print(" same but tr A = -1.2 (dissipative): Hurwitz count",cnt,"/20000")
print("C4b explicit: two 3-chains, N=B*blockdiag(J3,J3), E=B^-2 corners -> eigenvalue 1 of geometric multiplicity 2; defect on that 2-d U")
for B in [2,5,20,100]:
    J3=np.diag([1.,1],1);N=np.zeros((6,6));N[:3,:3]=B*J3;N[3:,3:]=B*J3
    E=np.zeros((6,6));E[2,0]=E[5,3]=B**-2.
    w,V=np.linalg.eig(N+E);idx=np.argsort(abs(w-1))[:2];Q,_=np.linalg.qr(V[:,idx].real)
    print(" B",B," ||N||",round(np.linalg.norm(N,2),1)," defect",round(np.linalg.norm((N-np.eye(6))@Q,2),5))
print("C6 twisted equivariance: random G-equivariant maps with rho=chi*pi (Z2 mirror, chi=-1)")
# face R^6: channels (L1,R1,L2,R2,L3,R3); mirror M swaps L/R; self rep = -M
M=np.zeros((6,6))
for i in range(3):M[2*i,2*i+1]=M[2*i+1,2*i]=1
worst=np.inf
for _ in range(2000):
    W1=rng.standard_normal((16,6))*10**rng.uniform(-1,2);W2=rng.standard_normal((6,16))
    def phi(u):  # symmetrise: Phi(u) = 1/2[f(u) - M f(Mu)] is equivariant with Phi(Mu) = -M Phi(u)
        f=lambda v:W2@np.tanh(W1@v+0.3)
        return 0.5*(f(u)-M@f(M@u))
    u=rng.standard_normal(6);c=10**rng.uniform(-1,1)
    lhs=np.linalg.norm(phi(u)-c*u)+np.linalg.norm(phi(M@u)-c*M@u);worst=min(worst,lhs/(2*c*np.linalg.norm(u)))
print(" min over 2000 random maps of [e(u)+e(Mu)]/(2c|u|) (theorem: >=1):",round(worst,4))
# linear: distance from Hom_G to cI
T=rng.standard_normal((6,6));R=0.5*(T- M@T@M)  # Reynolds onto {T M = -M T}
print(" Reynolds check T M + M T = 0:",np.allclose(R@M,-M@R)," trace of any twisted intertwiner:",round(np.trace(R),12))
