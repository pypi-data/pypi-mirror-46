B=print
import sys,jerryc05,jerryc05.mod_12306.__main__
def main(args=None):
	A=args;C=sys.argv
	if A:A[:0]=C
	else:A=C
	D=jerryc05.__version__
	if len(A)<2 or A[1]=='':B('No argument specified! I donno what to do, my flend!\n                                  .. .vr\n                                qBMBBBMBMY\n                               8BBBBBOBMBMv   叫你不给参数!\n                             iMBMM5vOY:BMBBv     不给参数！？\n             .r,             OBM;   .: rBBBBBY\n             vUL             7BB   .;7. LBMMBBM.\n            .@Wwz.           :uvir .i:.iLMOMOBM..\n             vv::r;             iY. ...rv,@arqiao.\n              Li. i:             v:.::::7vOBBMBL..\n              ,i7: vSUi,         :M7.:.,:u08OP. .\n                .N2k5u1ju7,..     BMGiiL7   ,i,i.\n                 :rLjFYjvjLY7r::.  ;v  vr... rE8q;.:,,\n                751jSLXPFu5uU@jerryc05.,1vjY2E89Yuzero.\n                BB:FMu rkM8Eq0PFjF15FZ0Xu15F25uuLuu25Gi.\n              ivSvvXL    :v58ZOGZXF2UUkFSFkU1u125uUJUUZ,\n            :@kevensun.      ,iY20GOXSUXkSuS2F5XXkUX5SEv.\n        .:i0BMBMBBOOBMUi;,        ,;8PkFP5NkPXkFqPEqqkZu.\n      .rqMqBBMOMMBMBBBM .           @kexianli.S11kFSU5q5\n    .7BBOi1L1MM8BBBOMBB..,          8kqS52XkkU1Uqkk1kUEJ\n    .;MBZ;iiMBMBMMOBBBu ,           1OkS1F1X5kPP112F51kU\n      .rPY  OMBMBBBMBB2 ,.          rME5SSSFk1XPqFNkSUPZ,.\n             ;;JuBML::r:.:.,,        SZPX0SXSP5kXGNP15UBr.\n                 L,    :@huhao.      :MNZqNXqSqXk2E0PSXPE .\n             viLBX.,,v8Bj. i:r7:,     2Zkqq0XXSNN0NOXXSXOU\n           :r2. rMBGBMGi .7Y, 1i::i   vO0PMNNSXXEqPYSecbone.\n           .i1r. .jkY,    vE. iY....  20Fq0q5X5F1S2F22uuv1M;')
	elif A[1]=='12306':jerryc05.mod_12306.__main__.main(A[2:])
	elif A[1]=='-v':B(D)
	else:B(f"Argument {A[1]} unsupported. Contact support?")
	return
if __name__=='__main__':main()