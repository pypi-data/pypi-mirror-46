
import pynipt as pn
from miresi import SSH

client = SSH()
client.connect_by_idx(5)

pipe = pn.Pipeline('/data/TestFolder/3Drat_fMRI_1ses', client=client)
#%%

from paralexe import Executor

cmd = '''awk '{print $1" "$2}' /Users/shlee419/Projects/JupyterNotebooks/02_mPFC-DBS/Results/UNCCH_CAMRI/500_OneSampleTTest-1samp_IL010Hz/1samp_IL010Hz_resid.ACFparam.txt'''
exc = Executor(cmd)
exc.execute()
print(exc.stdout.read())
print(exc.stderr.read())