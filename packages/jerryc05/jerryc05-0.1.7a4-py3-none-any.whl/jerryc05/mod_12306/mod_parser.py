H=open
G=str
def station_name(station_name_js='station_name.js',station_name_py='station_name.py'):
	P='@';O="'";N='utf-8';E=[]
	with H(station_name_js,encoding=N)as I:
		B=I.read();A=B.find(O)
		if A==-1:raise SystemError('Parsing js failed: "=" not found in "station_name.js"')
		A+=1
		if B[A]==P:A+=1
		J=B.find(O,A);K=B[A:J].split(P)
		for C in K:E.append(C.split('|'))
		import operator as L;E.sort(key=L.itemgetter(4))
	with H(station_name_py,'w',encoding=N)as D:
		D.write('def parse(s):\n\tx=((');F='a'
		for C in E:
			M=C[4][0]
			while M!=F:D.write('),\n(');F=chr(ord(F)+1)
			D.write(f"{tuple(C)},\n")
		D.write('))\n\tr=[]\n\tfor _ in x[ord(s[0])-97]:\n\t\tif s in _[4] or s in _[3]:\n\t\t\tr.append(_)\n\treturn r')
def ticket_count(num):
	A=num
	if A=='':return'\\'
	if A=='无':return'0'
	if A=='有':return' 20+'
	else:return A