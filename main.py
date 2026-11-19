import os,json,urllib.request,time,base64
B=[];S=0;ep=0
D=base64.b64decode("ZGRkZGRkZGQoKCgoKCgoKB4eHh4eHh4eFBQUFBQUFBQKCgoKCgoKCgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKFBQUFAoACh4yMjIyHgoUMjxBQTwyFBQ3QUZGQTcUFBQyPEFBPDcUAAoUFBQUCh4oKCgoKCgeKDIyMjIyMigoMjIyMjIyKCg3NzIyNzcoKDIyMjIyMigoNzcyMjc3KCgyMjIyMjIoHigoKCgoKB4yMjIyMjIyMjc8PDw8PDctMjIyMjIyLS0yMjIyMjItNzw8RktGPDc3PDxGS0Y8Ny0yMjIyMjItMjIyMjIyMjIeKCgtLSgoHigyMjIyMjIoKDIyMjIyMigtMjIyMjIyLS0yMjIyMjItKDIyLS0oKB4oMjItLSgoHh4oKC0tKCgeFAoKAAAKChQUCgoAAAoKFBQKCgAACgoUFAoKAAAKChQUCgoAAAoKFBQKCgAACgoUFAoKAAAKChQAChQeHhQKAAoUHigoHhQKFB4oMjIoHhQeKDIyMjIoHh4oMjIyMigeFB4oMjIoHhQKFB4oKB4UCgAKFB4eFAoA")
P,D=D[:64],D[64:]
K=D[:64];D=D[64:]
B=D[:64];D=D[64:]
R=D[:64];D=D[64:]
Q=D[:64];D=D[64:]
M=D[:64];D=D[64:]
E=D[:64]
def sq(f,r):return(r<<4)+f
def on_board(s):return 0<=s<128 and(s&0x88)==0
def pc(p):return p&8
def pt(p):return p&7
def Eval(b):
 s=0
 for i in range(128):
  p=b[i]
  if not p:continue
  t=p&7
  c=1 if pc(p)==0 else -1
  if t==1:
   p1=(i>>4)*8+(i&7)
   v=100+P[p1] if c==1 else P[((i^112)>>4)*8+((i^112)&7)]
  elif t==2:
   p1=(i>>4)*8+(i&7)
   v=320+K[p1] if c==1 else K[((i^112)>>4)*8+((i^112)&7)]
  elif t==3:
   p1=(i>>4)*8+(i&7)
   v=330+B[p1] if c==1 else B[((i^112)>>4)*8+((i^112)&7)]
  elif t==4:
   p1=(i>>4)*8+(i&7)
   v=500+R[p1] if c==1 else R[((i^112)>>4)*8+((i^112)&7)]
  elif t==5:
   p1=(i>>4)*8+(i&7)
   v=900+Q[p1] if c==1 else Q[((i^112)>>4)*8+((i^112)&7)]
  elif t==6:
   ph=min(1,int(sum(1 for x in b if x&7 in [4,5])))
   p1=(i>>4)*8+(i&7)
   ks=(ph>0.5)*2+(ph<0.5)*1
   km=M[p1] if ph>0.5 else E[p1]
   v=km+ks*2 if c==1 else -km-ks*2
  else:v=0
 return s if S==0 else -s
def Gen(b):
 m=[]
 for i in range(128):
  p=b[i]
  if not p or pc(p)!=S:continue
  t=pt(p)
  if t==1:
   d=16 if S==0 else -16;to=i+d
   if on_board(to)and not b[to]:
    if(S==0and i<24)or(S==1and i>=96):m+=(i,to,0),
    t2=i+2*d
    if on_board(t2)and not b[t2]:m+=(i,t2,0),
   for cd in[d+1,d-1]:
    to=i+cd
    if on_board(to)and(to&0x88)==0:
     if b[to]and pc(b[to])!=S:
      if(S==0and to>=112)or(S==1and to<16):m+=(i,to,5),(i,to,4),(i,to,3),(i,to,2)
      else:m+=(i,to,0),
     elif to==ep:m+=(i,to,0),
  elif t==2:
   for d in[31,33,14,-14,-31,-33,-18,18]:
    to=i+d
    if on_board(to)and(b[to]==0 or pc(b[to])!=S):m+=(i,to,0),
  elif t==3:
   for d in[15,-15,17,-17]:
    to=i
    while True:
     to+=d
     if not on_board(to):break
     if b[to]:
      if pc(b[to])!=S:m+=(i,to,0),
      break
     m+=(i,to,0),
  elif t==4:
   for d in[16,-16,1,-1]:
    to=i
    while True:
     to+=d
     if not on_board(to):break
     if b[to]:
      if pc(b[to])!=S:m+=(i,to,0),
      break
     m+=(i,to,0),
  elif t==5:
   for d in[16,-16,1,-1,15,-15,17,-17]:
    to=i
    while True:
     to+=d
     if not on_board(to):break
     if b[to]:
      if pc(b[to])!=S:m+=(i,to,0),
      break
     m+=(i,to,0),
  elif t==6:
   for d in[16,-16,1,-1,15,-15,17,-17]:
    to=i+d
    if on_board(to)and(b[to]==0 or pc(b[to])!=S):m+=(i,to,0)
 return m
def Mv(b,m):
 global S
 fr,to,promo=m
 p=b[fr];cap=b[to]
 b[to]=p if not promo else(p&8)|promo
 b[fr]=0
 if p&7==1and abs(fr-to)==32:pass
 if promo:b[to]=(p&8)|promo
 S^=8
def Um(b,m,cap):
 global S
 fr,to,promo=m
 p=b[to]
 b[fr]=p if not promo else(p&8)|1
 b[to]=cap
 S^=8
def Sr():
 m=Gen(B)
 if not m:return None
 best=None;best_s=-99999
 for mv in m:
  Mv(B,mv)
  score=-99999
  for mv2 in Gen(B):
   Mv(B,mv2)
   t=-Eval(B)
   if t>score:score=t
   Um(B,mv2,0)
  Um(B,mv,0)
  if score>best_s:best_s=score;best=mv
 return best
def Init():
 global B,S
 B=[0]*128;S=0
 B[sq(0,0)]=4;B[sq(1,0)]=2;B[sq(2,0)]=3;B[sq(3,0)]=5;B[sq(4,0)]=6;B[sq(5,0)]=3;B[sq(6,0)]=2;B[sq(7,0)]=4
 for f in range(8):B[sq(f,1)]=1
 for f in range(8):B[sq(f,6)]=9
 B[sq(0,7)]=12;B[sq(1,7)]=10;B[sq(2,7)]=11;B[sq(3,7)]=13;B[sq(4,7)]=14;B[sq(5,7)]=11;B[sq(6,7)]=10;B[sq(7,7)]=12
init = Init
sr = Sr
make_move = Mv
undo_move = Um
eval = Eval
