import sys

class HistDatParser:

    _warnings = True

    _systems = (
        'snes',
        'nes',
        'info',
        'gba',
        'n64',
        'gbcolor',
        'sg1000',
        'cpc_cass',
        'cpc_flop',
        'bbca_cas',
        'megadriv'
    )

    def __init__(self, filename):
        self.datfile = open(filename)
        self._parse()

    TOKEN_SYSTEM, TOKEN_BIO, TOKEN_END = range(3)

    def _parse_token(self, line):
        if line[0] is '$':
            parsed = []
            line = line[1:]
            if line.strip() == 'end':
                parsed.append(self.TOKEN_END)
            elif line.strip() == 'bio':
                parsed.append(self.TOKEN_BIO)
            else:
                eqIdx = line.find('=')
                if eqIdx < 0:
                    raise Exception(
                        'Expected \'=\' in line: {0}'.format(line))
                system = line[0:eqIdx]
                parsed.append(self.TOKEN_SYSTEM)
                try:
                    self._systems.index(system)
                except ValueError:
                    if self._warnings:
                        print('System: {0} is unexpected type.'.format(system))
                parsed.append(system)
                line = line[eqIdx + 1:]
                romnames = line.split(',')
                romnames = [rom for rom in romnames if len(rom) > 0]
                parsed.append(romnames)
            
        return None

    STATE_END, STATE_GAME, STATE_BIO = range(3)

    def _parse(self):
        state = self.STATE_END
        for line in self.datfile:
            parsed = self._parse_token(line)
            if state is self.STATE_END:
                if parsed is not None:
                    if parsed[0] is self.TOKEN_SYSTEM:
                        self._add_system(parsed)
                        state = self.STATE_GAME
                    else:
                        raise Exception('Expected a new system after $end')
            elif state is self.STATE_GAME:
                if parsed is not None:
                    if parsed[0] is self.TOKEN_BIO:
                        state = self.STATE_BIO
            elif state is self.STATE_BIO:
                #TODO: parse title and append bio information to game
                pass
            else:
                raise Exception('Unexpected parse state')

    def _add_system(self, parsed):
        #TODO: add this to a dictionary or something
        pass

if __name__ == '__main__':
    filename = sys.argv[1]
    parser = HistDatParser(filename)

