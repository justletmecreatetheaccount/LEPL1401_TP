"""
Mission 4: ADN
Effectuée en binome (Theo Daron, Vlad Doniga)
Vous êtes le meilleur tuteur <3 (ça vaut un point bonus non ?)

Nous n'avons pas inclus de code faisant usage des fonctions au lancement du programme parce que ce n'était pas demandé.
(De plus, hormis des données bidons nous n'aurions rien pu mettre _Kappa_ )

(Les commentaires dans le code sont en anglais pour plus de style )

Bisous.

"""
def is_adn(s):
    adn_chars = set(["a","c","g","t"])
    for x in s:
        if not x.lower() in adn_chars:
            return False
    return True if len(s) > 0 else False

def positions(string, pattern):
    result = []
    pattern_pointer = 0 #pattern_pointer is the index in the pattern of what we are looking for 
    pos = 0
    while pos < len(string):
        # Retrieving characters we are looking at
        char = string[pos]
        lookfor = pattern[pattern_pointer]
        
        # Check if the character matchs the pattern
        if char.lower() == lookfor.lower():
            pattern_pointer += 1
        
        # If the previous char matched but not the current one
        # We have to check if the current one match the first
        # char of the pattern
        elif pattern_pointer > 0:
            pattern_pointer = 0
            pos = pos - pattern_pointer - 1
        
        # Checking if we matched a number of char equal to length of the pattern
        # If its True, then we have a full match !
        if pattern_pointer == len(pattern):
            presence_index = pos - pattern_pointer + 1 #The +1 is because the presence_index have to be the index of the first char and not the char before
            result.append(presence_index)
            
            # Resetting position to match chained pattern
            # Like this one
            # pattern: aa
            # string: AAA
            # There's two match in this one. That's why we are taking pos back
            pos = presence_index
            pattern_pointer = 0
        
        pos += 1
    return result

def distance_h(string1, string2):
    string1 = string1.lower()
    string2 = string2.lower()
    if len(string2) != len(string1): 
        return None
    d = 0
    for (index, x) in enumerate(string1):
        d += 0 if string2[index] == x else 1
    return d
        
def distances_matrice(l):
    result = []
    for line in l:
        line_array = []
        for line2 in l:
            line_array.append(distance_h(line, line2))
        result.append(line_array)
    return result