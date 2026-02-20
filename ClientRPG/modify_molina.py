import pickle
import shutil
import os

def update_molina():
    file_path = 'Char configs/Molina.pkl'
    if not os.path.exists(file_path):
        print("Molina.pkl not found!")
        return

    # Backup before altering
    shutil.copyfile(file_path, file_path + '.backup2')

    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    
    # Init pets if none exist
    if "pets" not in data:
        data["pets"] = []
    
    # Create pets
    spider_desc = """Spider (João-com-braço)
Tiny beast, unaligned

Aa. -4
Pcn. 1 (1d4 - 1)
Speed. 20ft., climb 20ft.
Body 5 (-5) senses 16 (+6) mind 1 (−9) soul 6 (-4) vitality -1 
Skills. Stealth +10
Senses. Darkvision 30ft, passive perception +0
Challenge 0 (10 xp)

Spider climb. The spider can climb difficult surfaces, including upside down on ceilings, without needing to make a check.

Web sense. While in contact with a web, the spider knows the exact location of any other creature in contact with the same web.

Web walker. The spider ignores movement restrictions caused by webbing.

Undesired hitchhiker. The spider can occupy another creature's space and vice versa. The spider has advantage (anterior type) on stealth checks as long as it remains stationary on a creature's body."""

    salamander_desc = """Giant salamander (Come-bosta jr.)
Small-medium beast, unaligned
Aa -2
Pcn 7 (2d6) 
Speed 40 ft., Climb 15 ft., Burrow 5 ft.
Body senses mind soul vitality
13 (3) 10 (0) 3 (-7) 6 (-4) 0
Damage vulnerability. The giant salamander has vulnerability to fire damage. 
Senses passive perception 9
Languages
Challenge 0 (10 xp)
Amphibious. The giant salamander can breathe air and water.
Amphibious climb. The giant salamander can climb difficult surfaces, including upside down on ceilings, without needing to make a check.
Dry skin. The giant salamander has to keep its skin moist or it will take one level of exhaustion for each half hour it remains in a dry climate unattended. It takes about twice the amount of water that a medium creature needs to keep the salamander hydrated, and another creature have to spend an action roughly every half hour to moisten the salamander's skin if no body of waters where the salamander can douse itself are nearby. In extremely hot and dry climates (such as the elemental plane of fire), the DM might rule that the salamander needs even more water and attention."""

    # Note: Description is the 7th element in the tuple
    spider = (
        'Spider (João-com-braço)',
        'Tiny beast',
        '1', '1',
        '-4', '20ft/climb20',
        spider_desc
    )
    
    salamander = (
        'Giant salamander (Come-bosta jr.)',
        'Small-Medium',
        '7', '7',
        '-2', '40/15cl/5bw',
        salamander_desc
    )
    
    data["pets"] = [spider, salamander]
    
    # Init features if none exist
    if "features" not in data:
        data["features"] = []
        
    # Create features
    sorcery_pts = (
        'Sorcery Points',
        '4', '4', 'LR',
        'Convert shards to sorcery points: expend shards to regain double amount of sorcery points. Convert sorcery points to shards: expend 3 sorcery points to regain one shard.',
        False
    )
    
    metamagic_quickened = (
        'Metamagic: Quickened Spell',
        '', '', '-',
        'When you cast a spell that has a casting time of 1 action, you can spend 2 sorcery points to change the casting time to 1 bonus action for this casting.',
        False
    )
    
    metamagic_subtle = (
        'Metamagic: Subtle Spell',
        '', '', '-',
        'Spend 1 sorcery point to cast a spell without somatic, verbal, or Material components (excluding consumed/costly). Can be used even if another metamagic option was already used.',
        False
    )
    
    metamagic_heightened = (
        'Metamagic: Heightened Spell',
        '', '', '-',
        'Spend 2 sorcery points to give one target of the spell disadvantage (anterior type) on its saving throws made against the spell.',
        False
    )
    
    data["features"].extend([sorcery_pts, metamagic_quickened, metamagic_subtle, metamagic_heightened])
    
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)
    
    print("Molina updated successfully! Please tell the user to reload the character.")

if __name__ == "__main__":
    update_molina()
