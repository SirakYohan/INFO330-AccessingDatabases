import sqlite3
import sys

conn = sqlite3.connect("/Users/sirak/Documents/INFO-330/INFO330-AccessingDatabases/pokemon.sqlite")
cursor = conn.cursor()

# All the "against" column suffixes:
against_types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    num = sys.argv[i]
    cursor.execute("SELECT pokemon.name, type.name \
                    FROM pokemon \
                    JOIN pokemon_type ON pokemon.id = pokemon_type.pokemon_id \
                    JOIN type ON type.id = pokemon_type.type_id \
                    WHERE pokemon.pokedex_number = ?", (num,))
    results = cursor.fetchall()
    if len(results) == 0:
        print(f"Pokemon with pokedex number {num} not found.")
        continue
    types = [row[1] for row in results]
    pokemon = {'name': results[0][0], 'types': types}
    team.append(pokemon)


for i, p in enumerate(team):
    strengths = []
    weaknesses = []
    resulting = cursor.execute("SELECT against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, \
                        against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, \
                        against_normal, against_poison, against_psychic, against_rock, against_steel, against_water \
                        FROM against")
    resulting = cursor.fetchone()
    for j, type_word in enumerate(against_types):
        column_index = j
        if resulting is not None:
            if resulting[column_index] > 1:
                weaknesses.append(type_word)
            elif resulting[column_index] < 1:
                strengths.append(type_word)
    print(f"Analyzing {i}")
    print(f"{p['name']} ({' '.join(p['types'])}) is strong against {strengths} but weak against {weaknesses}")

# You will need to write the SQL, extract the results, and compare
# Remember to look at those "against_NNN" column values; greater than 1
# means the Pokemon is strong against that type, and less than 1 means
# the Pokemon is weak against that type


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

