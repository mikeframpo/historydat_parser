
from __future__ import print_function
import sys

#TODO: 
# * make a new variable to print out the file optionally
# * parse the game names and manufacturers, put this in a datatype  
# * fail if an unexpected state occurs

class Game:

    def __init__(self, systems, romnames):
        self.systems = systems
        self.romnames = romnames

class HistDatParser:

    _verbose = True
    _echo_file = False

    _known_systems = {
        'snes': 'Super Nintendo',
        'nes': 'Nintendo Entertainment System',
        'info': 'Unknown game system',
        'gba': 'Gameboy Advance',
        'n64': 'Nintendo 64',
        'gbcolor': 'Gameboy Color',
        'sg1000': 'Sega Game 1000',
        'cpc_cass': 'Amstrad CPC (Cassette)',
        'cpc_flop': 'Amstrad CPC (Floppy)',
        'bbca_cas': 'BBC Micro A (Cassette)',
        'megadriv': 'Sega Megadrive',
        'channelf': 'Fairchild Channel F',
        'a7800': 'Atari 7800',
        'a2600': 'Atari 2600',
        'crvision': '',
        'cdi': '',
        'coleco': '',
        'neogeo': '',
        'scv': '',
        'pcecd': '',
        'msx2_cart': '',
        'sms': '',
        'neocd': '',
        'vc4000': '',
        'studio2': '',
        'pce': '',
        'saturn,': '',
        'sat_cart': '',
        'aquarius': '',
        'gamegear': '',
        'coco_cart': '',
        'xegs': '',
        'x68k_flop': '',
        'gameboy': '',
        'alice32': '',
        'a5200': '',
        'a800': '',
        'advision': '',
        'c64_cart': '',
        'c64_flop': '',
        'mac_flop': '',
        'mac_hdd': '',
        'arcadia': '',
        'apfm1000': '',
        'apple2gs': '',
        'famicom_flop': '',
        'intv': '',
        'alice90': '',
        'lynx': '',
        'msx1_cart': '',
        'megacd': '',
        'megacdj': ''
    }

    _unknown_systems = set()

    def __init__(self, filename):
        self.datfile = open(filename)
        self._games_by_gamekey = {}
        self._parse()

    TOKEN_GAMEID, TOKEN_BIO, TOKEN_END = range(3)

    def _parse_token(self, line):
        parsed = None
        if line[0] is '$':
            line = line[1:]
            if line.strip() == 'end':
                parsed = [self.TOKEN_END]
            elif line.strip() == 'bio':
                parsed = [self.TOKEN_BIO]
            else:
                eqIdx = line.find('=')
                if eqIdx is not -1:
                    systemsline = line[0:eqIdx]
                    parsed = []
                    parsed.append(self.TOKEN_GAMEID)
                    systems = systemsline.split(',')
                    for system in systems:
                        try:
                            self._known_systems.has_key(system)
                        except ValueError:
                            self._unknown_systems.add(system)
                    parsed.append(systems)
                    line = line[eqIdx + 1:]
                    romnames = line.split(',')
                    romnames = [rom for rom in romnames if len(rom) > 0]
                    parsed.append(romnames)
            
        return parsed

    STATE_END, STATE_GAME, STATE_BIO = range(3)

    def _parse(self):
        state = self.STATE_END
        for line in self.datfile:
            if self._echo_file:
                print(line, end='')
            parsed = self._parse_token(line)
            if state is self.STATE_END:
                if parsed is not None:
                    if parsed[0] is self.TOKEN_GAMEID:
                        self._add_game(parsed)
                        state = self.STATE_GAME
                    elif parsed[0] is self.TOKEN_END:
                        continue
                    else:
                        raise Exception('Expected a new system after $end')
            elif state is self.STATE_GAME:
                if parsed is not None:
                    if parsed[0] is self.TOKEN_BIO:
                        state = self.STATE_BIO
            elif state is self.STATE_BIO:
                if parsed is not None:
                    if parsed[0] is self.TOKEN_END:
                        state = self.STATE_END
            else:
                raise Exception('Unexpected parse state')
        if len(self._unknown_systems) > 0:
            print("Found unknown game systems:")
            for system in self._unknown_systems:
                print(system)

    def _get_gamekey(self, system, romname):
        return '{0}_{1}'.format(system, romname)

    def _add_game(self, parsed):
        assert parsed[0] is HistDatParser.TOKEN_GAMEID
        assert len(parsed[1]) > 0
        assert len(parsed[2]) > 0
        systems = parsed[1]
        romnames = parsed[2]
        game = Game(systems, romnames)
        for system in systems:
            for romname in romnames:
                key = self._get_gamekey(system, romname)
                self._games_by_gamekey[key] = game

    def get_game(self, system, romname):
        key = self._get_gamekey(system, romname)
        if self._games_by_gamekey.has_key(key):
            return self._games_by_gamekey[key]
        return None

if __name__ == '__main__':
    filename = sys.argv[1]
    parser = HistDatParser(filename)

