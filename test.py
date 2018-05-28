import fuzzy

names = [ 'Catherine', 'Katherine', 'Katarina', 'Johnathan', 'Jonathan', 'John', 'Teresa', 'Theresa', 'Smith', 'Smyth', 'Jessica', 'Joshua']
soundex = fuzzy.Soundex(1)
for n in names:
    print n
    print soundex(n)
