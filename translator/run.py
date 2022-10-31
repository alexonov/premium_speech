import subprocess
import json
from pprint import pprint

word = 'money'

result = subprocess.Popen(f'node main.js {word}', shell=True, stdout=subprocess.PIPE)

print('RESULT:')
pprint(json.loads(result.stdout.read()))