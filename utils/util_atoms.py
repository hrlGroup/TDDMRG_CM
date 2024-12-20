
from pyscf import gto




ATOM_DATA = (
(  '1', 'h', 'hydrogen'),
(  '2', 'he', 'helium'),
(  '3', 'li', 'lithium'),
(  '4', 'be', 'beryllium'),
(  '5', 'b', 'boron'),
(  '6', 'c', 'carbon'),
(  '7', 'n', 'nitrogen'),
(  '8', 'o', 'oxygen'),
(  '9', 'f', 'fluorine'),
( '10', 'ne', 'neon'),
( '11', 'na', 'sodium', 'natrium'),
( '12', 'mg', 'magnesium'),
( '13', 'al', 'aluminum'),
( '14', 'si', 'silicon'),
( '15', 'p', 'phosphorus'),
( '16', 's', 'sulfur'),
( '17', 'cl', 'chlorine'),
( '18', 'ar', 'argon'),
( '19', 'k', 'potassium', 'kalium'),
( '20', 'ca', 'calcium'),
( '21', 'sc', 'scandium'),
( '22', 'ti', 'titanium'),
( '23', 'v', 'vanadium'),
( '24', 'cr', 'chromium'),
( '25', 'mn', 'manganese'),
( '26', 'fe', 'iron', 'ferrum'),
( '27', 'co', 'cobalt'),
( '28', 'ni', 'nickel'),
( '29', 'cu', 'copper', 'cuprum'),
( '30', 'zn', 'zinc'),
( '31', 'ga', 'gallium'),
( '32', 'ge', 'germanium'),
( '33', 'as', 'arsenic'),
( '34', 'se', 'selenium'),
( '35', 'br', 'bromine'),
( '36', 'kr', 'krypton'),
( '37', 'rb', 'rubidium'),
( '38', 'sr', 'strontium'),
( '39', 'y', 'yttrium'),
( '40', 'zr', 'zirconium'),
( '41', 'nb', 'niobium'),
( '42', 'mo', 'molybdenum'),
( '43', 'tc', 'technetium'),
( '44', 'ru', 'ruthenium'),
( '45', 'rh', 'rhodium'),
( '46', 'pd', 'palladium'),
( '47', 'ag', 'silver'),
( '48', 'cd', 'cadmium'),
( '49', 'in', 'indium'),
( '50', 'sn', 'tin', 'stannum'),
( '51', 'sb', 'antimony'),
( '52', 'te', 'tellurium'),
( '53', 'i', 'iodine'),
( '54', 'xe', 'xenon'),
( '55', 'cs', 'cesium'),
( '56', 'ba', 'barium'),
( '57', 'la', 'lanthanum'),
( '58', 'ce', 'cerium'),
( '59', 'pr', 'praseodymium'),
( '60', 'nd', 'neodymium'),
( '61', 'pm', 'promethium'),
( '62', 'sm', 'samarium'),
( '63', 'eu', 'europium'),
( '64', 'gd', 'gadolinium'),
( '65', 'tb', 'terbium'),
( '66', 'dy', 'dysprosium'),
( '67', 'ho', 'holmium'),
( '68', 'er', 'erbium'),
( '69', 'tm', 'thulium'),
( '70', 'yb', 'ytterbium'),
( '71', 'lu', 'lutetium'),
( '72', 'hf', 'hafnium'),
( '73', 'ta', 'tantalum'),
( '74', 'w', 'tungsten'),
( '75', 're', 'rhenium'),
( '76', 'os', 'osmium'),
( '77', 'ir', 'iridium'),
( '78', 'pt', 'platinum'),
( '79', 'au', 'gold', 'aurum'),
( '80', 'hg', 'mercury'),
( '81', 'tl', 'thallium'),
( '82', 'pb', 'lead', 'plumbum'),
( '83', 'bi', 'bismuth'),
( '84', 'po', 'polonium'),
( '85', 'at', 'astatine'),
( '86', 'rn', 'radon'),
( '87', 'fr', 'francium'),
( '88', 'ra', 'radium'),
( '89', 'ac', 'actinium'),
( '90', 'th', 'thorium'),
( '91', 'pa', 'protactinium'),
( '92', 'u', 'uranium'),
( '93', 'np', 'neptunium'),
( '94', 'pu', 'plutonium'),
( '95', 'am', 'americium'),
( '96', 'cm', 'curium'),
( '97', 'bk', 'berkelium'),
( '98', 'cf', 'californium'),
( '99', 'es', 'einsteinium'),
('100', 'fm', 'fermium'),
('101', 'md', 'mendelevium'),
('102', 'no', 'nobelium'),
('103', 'lr', 'lawrencium'),
('104', 'rf', 'rutherfordium'),
('105', 'db', 'dubnium'),
('106', 'sg', 'seaborgium'),
('107', 'bh', 'bohrium'),
('108', 'hs', 'hassium'),
('109', 'mt', 'meitnerium'),
('110', 'ds', 'darmstadtium'),
('111', 'rg', 'roentgenium'),
('112', 'cn', 'copernicium'),
('113', 'nh', 'nihonium'),
('114', 'fl', 'flerovium'),
('115', 'mc', 'moscovium'),
('116', 'lv', 'livermorium'),
('117', 'ts', 'tennessine'),
('118', 'og', 'oganesson')
)


########################################################
def get_nuc_charge(atom):
    for i in range(0,len(ATOM_DATA)):
        if str(atom).lower() in ATOM_DATA[i]:
            return int(ATOM_DATA[i][0])
    raise ValueError(f'The element {atom} of atom_list is not a recognized atom.')
########################################################


########################################################
def get_tot_nuc_charge(atom_list):
    nq = 0.0
    for a in atom_list:
        nq = nq + get_nuc_charge(a)
    return nq
########################################################


########################################################
def extract_atoms(s):
    lines = s.split(';')
    a = []
    i = 0
    for l in lines:
        w = l.split()
        if len(w) != 0: a = a + [w[0]]
        i += 1
    return a
########################################################


########################################################
def mole(logbook):
    nelCore = 2 * logbook['nCore']
    tot_nq = get_tot_nuc_charge(extract_atoms(logbook['atoms']))
    charge = tot_nq - nelCore - logbook['nelCAS']
    mol = gto.M(atom=logbook['atoms'], basis=logbook['basis'],
                ecp=logbook['ecp'], symmetry=logbook['group'],
                charge=charge, spin=logbook['twos'])
    return mol
########################################################
