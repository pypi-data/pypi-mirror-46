L=print
J='RESET_ALL'
C='RESET'
def colored_text(text,fore=C,back=C,style=J):
	V='BLACK';U='WHITE';T='CYAN';S='MAGENTA';R='BLUE';Q='YELLOW';P='GREEN';O='RED';I='';F=style;E=back;D=fore;D=D.upper();E=E.upper();F=F.upper();import colorama as G;G.init(autoreset=True);A=G.Fore;K={O:A.RED,P:A.GREEN,Q:A.YELLOW,R:A.BLUE,S:A.MAGENTA,T:A.CYAN,U:A.WHITE,V:A.BLACK,C:A.RESET}
	if E==C and F==J:L(f"{K.get(D.upper(),'')}{text}");return
	B=G.Back;M={O:B.RED,P:B.GREEN,Q:B.YELLOW,R:B.BLUE,S:B.MAGENTA,T:B.CYAN,U:B.WHITE,V:B.BLACK,C:B.RESET};H=G.Style;N={'DIM':H.DIM,'NORMAL':H.NORMAL,'BRIGHT':H.BRIGHT,J:H.RESET_ALL};L(f"{N.get(F.upper(),'')}{K.get(D.upper(),'')}{M.get(E.upper(),'')}{text}")