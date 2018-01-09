def index(spieler, position):
    return abs(spieler*31 - position)

def nachbarn(position):
    if position < 8:
        return None, None
    direkt = 23-position
    return direkt, 15-direkt

def start_spielfeld():
    return [
        2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 0, 0, 0, 0,
        0, 0, 0, 0, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2,
    ]

def zeichne_spielfeld_reihe(reihe, spielfeld):
    unterer_index = reihe*8
    zahlen = ["{:^4}".format(spielfeld[i]) for i in xrange(unterer_index, unterer_index+8)]
    if reihe in (1, 2):
        zahlen.reverse()
    print "|" + "|".join(zahlen) + "|"

def zeichne_spielfeld(spielfeld):
    print "-"*41
    for reihe in xrange(3, -1, -1):
        zeichne_spielfeld_reihe(reihe, spielfeld)
        print "-"*41

def gueltig(spieler, position, spielfeld):
    return position.isdigit() and int(position) < 16 and spielfeld[index(spieler, int(position))] > 1

def zug(spieler, position, spielfeld, take_aside=True):
    spielfeld = spielfeld[:]
    spielfeld_index = index(spieler, position)
    steine = spielfeld[spielfeld_index]
    if steine < 2:
        raise ValueError("Wir brauchen mehr als 2 Steine")
    spielfeld[spielfeld_index] = 0

    for i in xrange(steine):
        spielfeld_index = index(spieler, (position + i + 1) % 16)
        spielfeld[spielfeld_index] += 1

    position = (position + steine) % 16

    steine = spielfeld[spielfeld_index]
    if steine == 1:
        return spielfeld
    if take_aside:
        anderer_spieler = (spieler + 1) % 2
        position0, position1 = nachbarn(position)
        if position0 is not None:
            i0, i1 = index(anderer_spieler, position0), index(anderer_spieler, position1)
            if spielfeld[i0]:
                steine += (spielfeld[i0] + spielfeld[i1])
                spielfeld[i0] = 0
                spielfeld[i1] = 0
    spielfeld[spielfeld_index] = steine
    return zug(spieler, position, spielfeld, take_aside)

def spiel():
    import sys

    spielzug = 0
    spielfeld = start_spielfeld()
    zeichne_spielfeld(spielfeld)
    while 1:
        spieler = spielzug % 2
        input = "U:" if spieler == 0 else "O:"
        position = raw_input(input)
        if position == 'q':
            sys.exit()
        while not gueltig(spieler, position, spielfeld):
            print "Bitte Zahl zwischen 0 und 15 eingeben! (Mindestens 2 Steine auf Feld)"
            position = raw_input(input)
        spielfeld = zug(spieler, int(position), spielfeld, spielzug > 1)
        zeichne_spielfeld(spielfeld)
        if max(spielfeld[:15]) < 2:
            print "Spieler O hat gewonnen"
            sys.exit()
        elif max(spielfeld[16:]) < 2:
            print "Spieler U hat gewonnen"
            sys.exit()
        spielzug += 1

if __name__ == '__main__':
    spiel()
