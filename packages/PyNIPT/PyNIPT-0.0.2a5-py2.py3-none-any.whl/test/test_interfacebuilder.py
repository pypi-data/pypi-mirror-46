# The script for checking the method in the InterfaceBuilder class is functioning

import pynipt as pn

# prjpath = '/Users/shlee419/Projects/dataset/3Drat_fMRI_2ses_2runs'
prjpath = '/Users/shlee419/Projects/JupyterNotebooks/05_STN-opto'
dset = pn.Bucket(prjpath)
# proc = pn.Processor(dset, 'A_PipelineTesting', logger=True)
#%%
proc = pn.Processor(dset, 'A_fMRI_Preprocessing', logger=True)


#%% input_method 1 test (group statistics)
msk_path = '/Users/shlee419/Projects/JupyterNotebooks/00_Templates/01_Rat/01_DukeUNC_190123/Rat_Paxinos_400um_Mask.nii.gz'

step = pn.InterfaceBuilder(proc)
step.init_step(title='GroupAnalysisTestStep', suffix='func', idx=6, subcode=0,
               mode='reporting')
step.set_input(label='input', input_path='050', method=1, join_modifier=dict(suffix="'[1]'"),
               filter_dict=dict(regex=r'sub-oSTN\d{3}_task-130Hz10mW_run-\d{2}$', ext='nii.gz'))
step.set_output(label='output', modifier='130Hz10mW_stim', ext='nii.gz')
step.set_var(label='mask', value=msk_path)
step.set_output(label='resid', suffix='_resid', ext='nii.gz')
step.set_var(label='temp_prefix', value='temporary')
step.set_temporary(label='tempdir', path_only=True)

#%%
print(step._input_set)
print(step._input_ref)
print(step._output_set)
print(step._temporary_set)
print(step._var_set)

#%%
step.set_cmd('3dttest++ -mask *[mask] '
             '-prefix *[output] -setA *[input] '
             '-resid *[resid] -tempdir *[tempdir] -prefix_clustsim *[temp_prefix] -ACF -CLUSTSIM')

#%%
step.run()

#%% static_input test
step = pn.InterfaceBuilder(proc)
step.init_step(title='StaticInputTest', suffix='func', idx=2, subcode=0,
               mode='processing')
step.set_input(label='input', input_path='func', method=0)
# set static input using first file of the filtered dset
step.set_static_input(label='static_input1', input_path='func')
# set static input using indexed file of the filtered dset
step.set_static_input(label='static_input2', input_path='func', idx=1)
# set static input using regex
step.set_static_input(label='static_input3', input_path='func',
                      filter_dict=dict(regex=r'.*run-02'))
step.set_output(label='output')

#%%
for label in step._input_set.keys():
    print(label)
    for path in step._input_set[label]:
        print('\t{}'.format(path))

#%% reset
proc.clear()
