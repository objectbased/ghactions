import hvac
import os

#print("::set-output name=value::test123")
os.system('echo "{value}={test123}" >> $GITHUB_OUTPUT')