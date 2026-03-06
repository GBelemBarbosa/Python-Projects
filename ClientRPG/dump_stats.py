import pickle, json
data = pickle.load(open('Char configs/Molina.pkl','rb'))
out = {
    'STATS': data.get('stats'),
    'SAVES': data.get('saves'),
    'COMBAT': data.get('combat'),
    'ASPECTS': {k: v for k, v in data.get('aspects').items()},
    'LEVEL': data.get('level'),
    'CLASS': data.get('class')
}
with open('out.json', 'w') as f: json.dump(out, f, indent=2)
