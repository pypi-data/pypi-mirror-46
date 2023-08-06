from itertools import groupby
import numpy as np

def create_decoder(unit_path):

    unit = read_unit(unit_path)
    model = Decoder(unit)
    return model

def read_unit(unit_path):
    # load unit from units.txt

    unit_to_id = dict()

    unit_to_id['<blk>'] = 0

    for line in open(str(unit_path), 'r', encoding='utf-8'):
        unit, idx = line.split()

        unit_to_id[unit] = int(idx)

    unit = Unit(unit_to_id)
    return unit

def write_unit(unit, unit_path):

    w = open(str(unit_path), 'w', encoding='utf-8')
    for i in range(1, len(unit.id_to_unit)):
        u = unit.id_to_unit[i]
        w.write(u+' '+str(i)+'\n')

    w.close()

class Unit:

    def __init__(self, unit_to_id):

        self.unit_to_id = unit_to_id
        self.id_to_unit = {}

        assert '<blk>' in self.unit_to_id and self.unit_to_id['<blk>'] == 0

        for unit, idx in self.unit_to_id.items():
            self.id_to_unit[idx] = unit

    def __str__(self):
        return '<Unit: ' + str(len(self.unit_to_id)) + ' elems>'

    def __repr__(self):
        return self.__str__()


    def __len__(self):
        return len(self.unit_to_id)


    def get_id(self, unit):

        # handle special units
        if unit == ' ':
            unit = '<space>'

        assert unit in self.unit_to_id, 'unit '+unit+'is not in '+str(self.unit_to_id)
        return self.unit_to_id[unit]

    def get_ids(self, units):
        """
        get index for a word list
        :param words:
        :return:
        """

        return [self.get_id(unit) for unit in units]

    def get_unit(self, id):
        assert id >= 0 and id in self.id_to_unit

        unit = self.id_to_unit[id]

        # handle special units
        if unit == '<space>':
            unit = ' '

        return unit

    def get_units(self, ids):
        """
        get unit from ids

        :param ids: elem_id list
        :return: a list of unit
        """

        return [self.get_unit(id) for id in ids]

class Decoder:

    def __init__(self, unit):
        self.unit = unit

    def initialize(self):
        return

    def decode_label(self, logits, blank_factor=1.0, add_space=True, no_remove=False):

        # to make if comparision shorter
        decoded_seq = []

        blank_id = 0

        for t in range(len(logits)):

            logit = logits[t]
            logit[0] /= blank_factor

            arg_max = np.argmax(logit)
            decoded_seq.append(arg_max)

            #print(arg_max)
        if no_remove:
            cleaned_decoded_seq = decoded_seq
        else:
            ids = [x[0] for x in groupby(decoded_seq)]
            cleaned_decoded_seq = [x for x in filter(lambda x: x != blank_id, ids)]

        return cleaned_decoded_seq


    def decode_phone(self, logits, blank_factor=1.0, add_space=True, no_remove=False):

        cleaned_decoded_seq = self.decode_label(logits, blank_factor, add_space, no_remove)

        if add_space:
            return ' '.join(self.unit.get_units(cleaned_decoded_seq))
        else:
            return ''.join(self.unit.get_units(cleaned_decoded_seq))

