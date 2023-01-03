GPT_PROMPT = """
Generate a new magic card for the game Magic The Gathering:

Color: Green
Card Type: Creature
Card Name: Elvish Piper
Mana Cost: {3}{G}
Types: Creature — Elf Shaman
Card Text: {G}, {T}: You may put a creature card from your hand onto the battlefield.
Flavor Text: "From Gaea grew the world, and the world was silent. From Gaea grew the world's elves, and the world was silent no more." — Elvish teaching
P/T: 1/1

=============
Generate a new magic card for the game Magic The Gathering:

Color: Blue
Card Type: Creature
Card Name: Psychatog
Mana Cost: {1}{U}{B}
Types: Creature — Atog
Card Text: Discard a card: Psychatog gets +1/+1 until end of turn | Exile two cards from your graveyard: Psychatog gets +1/+1 until end of turn.
Flavor Text: n/a
P/T: 1/1

=============
Generate a new magic card for the game Magic The Gathering:

Color: n/a
Card Type: Artifact
Card Name: Black Lotus
Mana Cost: {0}
Types: Artifact
Card Text: {T}, Sacrifice Black Lotus: Add three mana of any one color.
Flavor Text: n/a
P/T: n/a

=============
Generate a new magic card for the game Magic The Gathering:

Color: Blue
Card Type: Creature
Card Name: Leviathan
Mana Cost: {5}{U}{U}{U}{U}
Types: Creature — Leviathan
Card Text: Trample | Leviathan enters the battlefield tapped and doesn't untap during your untap step. | At the beginning of your upkeep, you may sacrifice two Islands. If you do, untap Leviathan. | Leviathan can't attack unless you sacrifice two Islands. (This cost is paid as attackers are declared.)
Flavor Text: n/a
P/T: 10/10

=============
Generate a new magic card for the game Magic The Gathering:

Color: Black
Card Type: Creature
Card Name: Grim Draugr
Mana Cost: {2}{B}
Types: Snow Creature — Zombie Berserker
Card Text: {1}{S}: Grim Draugr gets +1/+0 and gains menace until end of turn. (It can't be blocked except by two or more creatures. {S} can be paid with one mana from a snow source.)
Flavor Text: "She was a ragged shadow of her living form, but she had lost none of her deadly prowess."
P/T: 3/2

=============
Generate a new magic card for the game Magic The Gathering:

Color: Red
Card Type: Sorcery
Card Name: Firebolt
Mana Cost: {R}
Types: Sorcery
Card Text: Firebolt deals 2 damage to any target. | Flashback {4}{R} (You may cast this card from your graveyard for its flashback cost. Then exile it.)
Flavor Text: "There’s more where that came from!"
P/T: n/a

=============
Generate a new magic card for the game Magic The Gathering:

Color: White
Card Type: Creature
Card Name: Crusading Knight
Mana Cost: {2}{W}{W}
Types: Creature — Human Knight
Card Text: Protection from black. | Crusading Knight gets +1/+1 for each Swamp your opponents control.
Flavor Text: "My only dream is to destroy the nightmares of others."
P/T: 2/2

=============
Generate a new magic card for the game Magic The Gathering:

Color: Green
Card Type: Creature
Card Name: Stone-Tongue Basilisk
Mana Cost: {4}{G}{G}{G}
Types: Creature — Basilisk
Card Text: Whenever Stone-Tongue Basilisk deals combat damage to a creature, destroy that creature at end of combat. | Threshold — As long as seven or more cards are in your graveyard, all creatures able to block Stone-Tongue Basilisk do so.
Flavor Text: n/a
P/T: 4/5

=============
Generate a new magic card for the game Magic The Gathering:

Color: Red
Card Type: Instant
Card Name: Reverberate
Mana Cost: {R}{R}
Types: Instant
Card Text: Copy target instant or sorcery spell. You may choose new targets for the copy.
Flavor Text: "Not bad, but I can think of a better use for that."
P/T: n/a

=============
Generate a new magic card for the game Magic The Gathering:

Color: n/a
Card Type: Land
Card Name: Cabal Coffers
Mana Cost: n/a
Types: Land
Card Text: {2}, {T}: Add {B} for each Swamp you control.
Flavor Text: "Deep within the Cabal's vault, the Mirari pulsed like a dead sun—and its darkness radiated across Otaria."
P/T: n/a

=============
Generate a new magic card for the game Magic The Gathering:

Color: Black
Card Type: Creature
Card Name: Crypt Ghast
Mana Cost: {3}{B}
Types: Creature — Spirit
Card Text: Extort (Whenever you cast a spell, you may pay {W/B}. If you do, each opponent loses 1 life and you gain that much life.) | Whenever you tap a Swamp for mana, add an additional {B}.
Flavor Text: n/a
P/T: 2/2

=============
Generate a new magic card for the game Magic The Gathering:

Color: Blue
Card Type: Enchantment
Card Name: Spreading Seas
Mana Cost: {1}{U}
Types: Enchantment — Aura
Card Text: Enchant land | When Spreading Seas enters the battlefield, draw a card. | Enchanted land is an Island.
Flavor Text: "Most inhabitants of Zendikar have given up on the idea of an accurate map."
P/T: n/a

=============
Generate a new magic card for the game Magic The Gathering:

Color: Blue
Card Type: Sorcery
Card Name: Preordain
Mana Cost: {U}
Types: Sorcery
Card Text: Scry 2, then draw a card. (To scry 2, look at the top two cards of your library, then put any number of them on the bottom of your library and the rest on top in any order.)
Flavor Text: n/a
P/T: n/a

=============
Generate a new magic card for the game Magic The Gathering:

Color: White
Card Type: Creature
Card Name: Mentor of the Meek
Mana Cost: {2}{W}
Types: Creature — Human Soldier
Card Text: Whenever another creature with power 2 or less enters the battlefield under your control, you may pay {1}. If you do, draw a card.
Flavor Text: "In these halls there is no pass or fail. Your true test comes with the first full moon."
P/T: 2/2

=============
Generate a new magic card for the game Magic The Gathering:

Color: my_color
Card Type: my_type
"""