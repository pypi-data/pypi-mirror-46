"""Chem structure reader

This module contains functions that extract data from JSON files for
compatibility with the Dash bio Molecule2dViewer component."""

import json

import numpy as np

from periodictable import elements


_elements = {el.number: el.symbol for el in elements}


def get_distance(p1, p2):
    return 20.0*np.round(np.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] -
                                                           p2['y'])**2), 2)


def read_structure(
        file_path='',
        data_string=''
):
    """Read a file in JSON format, either from a file or from a string of
    raw data.

    :param (string) file_path: The full path to the JSON file (can be
                               relative or absolute).
    :param (string) data_string: A string corresponding to the JSON file.

    :rtype (dict[list]): A dictionary containing the atoms and bonds
                         in the file.
    """

    # ensure we are only given one file specification
    if file_path and data_string:
        raise Exception(
            "Please specify either a file path or a \
            string of data."
        )

    if not file_path and not data_string:
        raise Exception(
            'no'
        )

    structural_info = {}

    if file_path:
        with open(file_path, 'r') as f:
            structural_info = json.loads(f.read())
    else:
        structural_info = json.loads(data_string)

    structure = structural_info['PC_Compounds'][0]

    try:
        atoms = [
            {'id': atm[0],
             'atom': atm[1]}
            for atm in list(zip(
                    structure['atoms']['aid'],
                    [_elements[int(el)] for el in structure['atoms']['element']]
            ))
        ]
    except Exception:
        atoms = []

    bonds = [
        {'id': int(bnd[0]),
         'source': int(bnd[1]),
         'target': int(bnd[2]),
         'bond': int(bnd[3]),
         'strength': 1}
        for bnd in list(zip(
                [i+1 for i in range(len(structure['bonds']['aid1']))],
                structure['bonds']['aid1'],
                structure['bonds']['aid2'],
                structure['bonds']['order']
        ))
    ]

    pos = {
        i: {
            'x': structure['coords'][0]['conformers'][0]['x'][structure['coords'][0]['aid'].index(i)],
            'y': structure['coords'][0]['conformers'][0]['y'][structure['coords'][0]['aid'].index(i)],
        } for i in structure['coords'][0]['aid']
    }

    for bnd in bonds:
        bnd['distance'] = get_distance(pos[bnd['source']], pos[bnd['target']])

    residue = {
        'nodes': atoms,
        'links': bonds
    }
    return residue
