import re

#%%
command = r'test *[asdasd] *[asdaaa] {{}}'

prefix, surfix = '*[', ']'
raw_prefix = ''.join([r'\{}'.format(chr) for chr in prefix])
raw_surfix = ''.join([r'\{}'.format(chr) for chr in surfix])

# The text
p = re.compile(r"{0}[^{0}{1}]+{1}".format(raw_prefix, raw_surfix))
place_holders = set([obj[len(prefix):-len(surfix)] for obj in p.findall(command)])

p = re.compile(r"{}({}){}".format(raw_prefix,'|'.join(place_holders), raw_surfix))
new_command = p.sub(r'{\1}', command)
#%%
print(new_command.encode())
#%%
new_command.encode().format(asdasd='test', asdaaa='pass')