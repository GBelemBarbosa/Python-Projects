import pickle

def view_molina():
    try:
        with open('Char configs/Molina.pkl', 'rb') as f:
            data = pickle.load(f)
        print("Features format:", data.get("features", [])[:2])
        print("Pets format:", data.get("pets", [])[:2])
    except Exception as e:
        print(e)

if __name__ == "__main__":
    view_molina()
