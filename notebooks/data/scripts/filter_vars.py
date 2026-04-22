import json
import sys

path = sys.argv[1]
outpath = sys.argv[2]

with open(path) as f:
    data = json.load(f)

vars = data.get('variables', [])
keywords = ['income', 'debt', 'loan', 'credit', 'borrow', 'saving', 'expenditure',
            'wage', 'earn', 'spend', 'asset', 'liab', 'repay', 'default', 'grant',
            'salary', 'payment', 'financial', 'bank', 'interest', 'overdraft', 'card']

matches = []
for v in vars:
    label = (v.get('label') or '').lower()
    name = (v.get('name') or '').lower()
    if any(k in label or k in name for k in keywords):
        matches.append({
            'name': v.get('name'),
            'label': v.get('label'),
            'group': v.get('var_grp_name', '')
        })

result = {'total_vars': data.get('total', len(vars)), 'matched': len(matches), 'variables': matches}
with open(outpath, 'w') as f:
    json.dump(result, f, indent=2)
print(f"Matched {len(matches)} of {data.get('total', len(vars))} variables")
