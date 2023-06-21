import hvac
import os

#print("::set-output name=value::test123")
#os.system('echo "{value}={test123}" >> $GITHUB_OUTPUT')

name = 'token'
value = 'test123'
with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    print(f'{name}={value}', file=fh)