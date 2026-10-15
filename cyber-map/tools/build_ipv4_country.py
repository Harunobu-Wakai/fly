import sys, base64, json
src, codes, out = sys.argv[1:4]
rows=[]
for line in open(src):
    a,b,c=line.strip().split(',')
    rows.append((int(a),int(b),c))
rows.sort()
merged=[]  # (start, cc)
prev_end=-1
for a,b,c in rows:
    if a>prev_end+1: merged.append((prev_end+1,'ZZ'))
    if merged and merged[-1][1]==c and a==prev_end+1: pass
    else: merged.append((a,c))
    prev_end=max(prev_end,b)
merged.append((prev_end+1,'ZZ'))
ccs=sorted(set(c for _,c in merged)); idx={c:i for i,c in enumerate(ccs)}
buf=bytearray(); last=0
for s,c in merged:
    d=s-last; last=s
    while True:
        b=d&0x7f; d>>=7
        if d: buf.append(b|0x80)
        else: buf.append(b); break
    buf.append(idx[c])
num={}
for r in json.load(open(codes)):
    num[r[0]]=r[2]
num_map={c:num.get(c) for c in ccs if num.get(c)}
with open(out,'w') as f:
    f.write('// IPv4 -> country (ip-location-db geo-whois-asn-country, CC0). varint delta start + country index\n')
    f.write('window.IP_DB=%s;\n'%json.dumps({"n":len(merged),"cc":ccs,"num":num_map,"data":base64.b64encode(bytes(buf)).decode()}))
print(len(rows),len(merged),len(buf))
