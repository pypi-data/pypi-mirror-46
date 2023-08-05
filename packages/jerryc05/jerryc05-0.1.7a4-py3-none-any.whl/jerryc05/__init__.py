L='.'
K=print
__version__='0.1.7a4'
import urllib.request as D
try:
	K(end='Checking for updates...\r')
	with D.urlopen('https://pypi.org/pypi/jerryc05/json',timeout=1)as E:
		import json;F=json.loads(E.read());C=F['info']['version'];G=C.split(L);A=__version__.split(L);B=A[-1]
		for (H,I) in enumerate(B):
			if I.isalpha():A.remove(B);A.append(f"{int(B[:H])-0.5}");break
		if A<G:import jerryc05.mod_parser as J;colored_text=J.colored_text;colored_text(f'New version {C} is available!!!\nUpgrade using command "pip3 install -U jerryc05".\n','yellow')
except OSError:K('')