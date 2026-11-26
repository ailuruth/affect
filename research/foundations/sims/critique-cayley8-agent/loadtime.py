import time,io,contextlib,os,sys
t0=time.time()
P8="/home/user/affect/research/foundations/sims/design-g8/checks.py"
src=open(P8).read()
head,body=src.split("BODY = r'''",1)
body=body.split("'''",1)[0]
body=body.split("# =========================================================== J31")[0]
G={"__name__":"g8","__file__":P8}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(head,"g8head","exec"),G)
print("head",time.time()-t0,flush=True)
G7=G["G7"]
exec(compile(body,"g8body","exec"),G7)
print("body",time.time()-t0)
