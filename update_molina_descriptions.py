import pickle
import os

file_path = r"ClientRPG/Char configs/Molina.pkl"

# Mapping of Feature Name -> Full Description
# Extracted from the provided text content
full_descriptions = {
    "Telepathic Channel": """Your alien influence gives you the ability to touch the minds of other creatures. You can create a channel to communicate telepathically with one creature you can see within 30 feet of you (no action required). If connected in this way, you lose the channel as soon as the creature leaves your sight. If you have expanded at least 1 minute familiarizing yourself with the creature and expend one action to mentally concentrate, the range becomes 120 ft., and you just need to know their general direction instead of having direct sight. If, in this case, the creature moves considerably from the spot you originally guessed, you lose the channel, unless you know where it moved. Either way, the creature doesn’t know the origin of the voice in its head.
1 foot of stone, 1 inch of common metal, a thin sheet of lead, or 3 feet of wood block the communication but not the channel itself, and contact can be made as soon as the creature leaves the blocked area, as long as you keep track of its location.
As an action, you grant the creature the ability to respond until the start of your next turn. Neither of you gain the ability to understand the other’s language, and you can’t link with a creature that doesn’t know any language.""",

    "Obscurus Arcana": """Your mental and physical conditioning allow you to conceal your spellcasting and spells from others. You learn the mage hand cantrip. When you cast mage hand, you can make the spectral hand invisible. Controlling its movement still takes an action, but special timings (free actions, reactions and bonus actions...) carry to your mage hand.
Additionally, the current contents of your spellbook, as well as any spells you learn by gaining wizard levels, are committed to memory. Your memory is considered a spellbook.
You can also befuddle a creature's mind with nothing but a gesture. As an action, you can force up to your effective wizard level (5) creatures you can see within 30 feet of you to make a mind saving throw. On a failed save, you can force the creature to forget a single aspect of a conversation, observation or encounter it had in the past 10 minutes.""",

    "Mimic Trait": """You gain an uncanny ability to mimic other people. As an action, you gain one trait of your choice from the following list that a humanoid you can see within 60 feet possesses (even if they only possess it temporarily):
- One special sense, such as darkvision or tremorsense.
- One movement speed, such as a swim or climb speed.
- One aspect, knowledge field, tool or instrument proficiency.
- One damage resistance.
- Their accent, verbal ticks and mannerisms.
You can keep this trait as long as you are within 60 feet of the target, or until you use this feature again.""",

    "Master Simulator": """You have become a master of crafting and controlling simulacra. Casting the simulacrum spell and repairing damaged simulacra requires half as much time and gold. You can have up to two active duplicates created by the simulacrum spell at one time.""",

    "Arcane Recovery": """You have learned to regain some of your magical energy by studying your spellbook. When you finish a short rest, you can regain shards. The maximum amount is equal to roundup(effective wizard level/2). Your count for keeping track of saturation for total shard outputs of 5 or less whose combined values (of shards) are less or equal to the amount of shards you regained decreases by 1.
Once you use this feature, you can't do so again until you finish a long rest.""",

    "Sorcery Points": """You have sorcery points equal to your effective sorcerer level. You regain all spent sorcery points when you finish a long rest.
Converting shards to sorcery points: On your turn, you can expend shards and regain double the amount of sorcery points (no action required).
Converting sorcery points to shards: On your turn, you can expend 3 sorcery points and regain one shard (no action required).""",

    "Rebel Kinship": """You are part of a network of fellow dissidents. Although you may not always agree on the methods of dissent with your fellow members, they are willing to create distractions in public, provide safe passage, and inform you of the patrol routes of guards, the military and other law enforcement.
Dissidents also have a foot in a varied assortment of spheres of society, as they need the assistant of everyone they can get their hands on for their cause.""",

    "Lupine Mask": """While wearing this dark ceramic mask, you have advantage (anterior type) on awareness checks relying on hearing and smell, as well as on Animal Handling checks made to interact with wolves and other canines.""",

    "Bag of Holding": """(Disguised as a small coco hat)
This bag has an interior space considerably larger than its outside dimensions, roughly 2 feet in diameter at the mouth and 4 feet deep. The bag can hold up to 500 pounds, not exceeding a volume of 64 cubic feet. The bag weighs 15 pounds, regardless of its contents.""",

    "Stonespeaker Crystal": """(10 charges) (attunement)
Created by the stone giant librarians of Gravenhollow, this nineteen-inch-long shard of quartz grants you advantage (anterior type) on Investigation checks while it is on your person.
The crystal has 10 charges. While holding it, you can use an action to expend charges to cast: comprehend languages (1), speak with animals (2), speak with dead (4), speak with plants (3), or stone tell (3).
Regains 1d6 + 4 expended charges daily at dawn.""",

    "Innate Expertise": """Your natural magic blooms through your actions. Choose two of your aspect proficiencies. You gain expertise with them, which means your proficiency bonus is doubled for any ability check you make that uses either of the chosen proficiencies.""",

    "Metamagic": """You gain the ability to twist your spells to suit your needs.
Current Options:
- Quickened Spell: Spend 2 SP to change casting time 1 action -> 1 bonus action.
- Subtle Spell: Spend 1 SP to cast without V/S components (unless material consumable/costly).
- Heightened Spell: Spend 2 SP to give one target disadvantage on the first saving throw."""
}

if os.path.exists(file_path):
    try:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        
        if "features" in data:
            updated_count = 0
            # Iterate through existing features and update description if we have a full text version
            # Structure is list of tuples: (Name, Cur, Max, Reset, Desc)
            new_features_list = []
            for i, feat in enumerate(data["features"]):
                name = feat[0]
                # Check for exact or partial match
                new_desc = None
                if name in full_descriptions:
                    new_desc = full_descriptions[name]
                
                if new_desc:
                    # Construct new tuple (immutable)
                    new_feat = (feat[0], feat[1], feat[2], feat[3], new_desc)
                    new_features_list.append(new_feat)
                    updated_count += 1
                else:
                    new_features_list.append(feat)
            
            data["features"] = new_features_list
            
            with open(file_path, "wb") as f:
                pickle.dump(data, f)
                
            print(f"Updated descriptions for {updated_count} features.")
            
    except Exception as e:
        print(f"Error updating descriptions: {e}")
else:
    print(f"File not found: {file_path}")
