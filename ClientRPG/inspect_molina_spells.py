import pickle
import docx

def inspect():
    with open('Char configs/Molina.pkl', 'rb') as f:
        data = pickle.load(f)
    print("Spell format sample:")
    if 'spells' in data and len(data['spells']) > 0:
        s = data['spells'][0]
        print(s)
        print("Length:", len(s))
    else:
        print("No spells found.")

    print("\nDocx format sample (first 10 paragraphs of Cantrips):")
    try:
        doc = docx.Document('Cantrips.docx')
        for i, p in enumerate(doc.paragraphs[:10]):
            print(f"{i}: {p.text}")
    except Exception as e:
        print("Error reading docx:", e)

if __name__ == "__main__":
    inspect()
