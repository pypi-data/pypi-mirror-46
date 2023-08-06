# !/usr/bin/python3
"""
PDB Parser (pdb_eda.pdbParser)
-------------------------------------------------------

This module provides methods to read and parse the PDB format files and returns PDB objects.
Format details of PDB can be found in ftp://ftp.wwpdb.org/pub/pdb/doc/format_descriptions/Format_v33_Letter.pdf.
"""
import re
import numpy as np


def readPDBfile(filename, mode='lite'):
    """
    Creates :class:`pdb_eda.pdbParser.PDBentry` object from file name.

    :param str filename: The name of a PDB formated file.
    """
    with open(filename, "r") as fileHandle:
        return parse(fileHandle, mode)


def parse(handle, mode='lite'):
    """
    Creates :class:`pdb_eda.pdbParser.PDBentry` object from file handle object.

    :param handle: The file handle of a PDB formated file.
    :param str mode: Whether of not to parse all the atoms, default as 'lite' (not parse).
    """
    atoms = []
    rotationMats = []
    orthoMat = []
    modelCount = 0
    pdbid = date = method = resolution = rValue = rFree = program = spaceGroup = 0
    for record in handle.readlines():
        if mode == 'lite' and record.startswith('ATOM'):
            break
        elif record.startswith('HEADER'):
            date = record[57: 57+2].strip()
            pdbid = record[62: 62+4].strip()
        elif record.startswith('EXPDTA'):
            method = record[6: 6+30]
            method = method.strip().replace(' ', '_')
        elif record.startswith('REMARK   2 RESOLUTION'):
            match = re.search('RESOLUTION.(.+)ANGSTROMS', record)
            if match:
                resolution = match.group(1).strip()
        elif record.startswith('REMARK   3   R VALUE'):
            match = re.search('^REMARK   3   R VALUE            \(WORKING SET\) : (.+)$', record)
            if match:
                rValue = match.group(1).strip()
        elif record.startswith('REMARK   3   FREE R VALUE'):
            match = re.search('^REMARK   3   FREE R VALUE                     : (.+)$', record)
            if match:
                rFree = match.group(1).strip()
        elif record.startswith('REMARK   3   PROGRAM'):
            match = re.search('^REMARK   3   PROGRAM     : (.+)$', record)
            if match:
                program = match.group(1).strip().replace(' ', '_')
        elif record.startswith('MODEL'):
            modelCount += 1
            if modelCount > 1: break
        elif record.startswith('REMARK 290 SYMMETRY OPERATORS FOR SPACE GROUP:'):
            match = re.search('^REMARK 290 SYMMETRY OPERATORS FOR SPACE GROUP: (.+)$', record)
            if match:
                spaceGroup = match.group(1).strip().replace(' ', '_')
        elif record.startswith('REMARK 290   SMTRY'):
            match = re.search('^REMARK 290   SMTRY(.+)$', record)
            if match:
                items = match.group(1).split()
                if len(rotationMats) < int(items[1]):
                    rotationMats.append(np.zeros((3, 4)))
                rotationMats[int(items[1])-1][int(items[0])-1] = [float(i) for i in items[2:6]]
        elif record.startswith('SCALE1     '):
            match = re.search('^SCALE1     (.+)$', record)
            if match:
                orthoMat.append(match.group(1).split())
        elif record.startswith('SCALE2     '):
            match = re.search('^SCALE2     (.+)$', record)
            if match:
                orthoMat.append(match.group(1).split())
        elif record.startswith('SCALE3     '):
            match = re.search('^SCALE3     (.+)$', record)
            if match:
                orthoMat.append(match.group(1).split())
        elif record.startswith('ATOM') or record.startswith('HETATM'):
            keyValues = {'record': record,
                         'recordType': record[0: 0+6],
                         'serial': record[6: 6+5],
                         'atomName': record[12: 12+4],
                         'alternateLocation': record[16: 16+1],
                         'residueName': record[17: 17+3],
                         'chainID': record[21: 21+1],
                         'residueNumber': record[22: 22+4],
                         'x': record[30: 30+8],
                         'y': record[38: 38+8],
                         'z': record[46: 46+8],
                         'occupancy': record[54: 54+6],
                         'bFactor': record[60: 60+6],
                         'element': record[76: 76+2]}

            keyValues = {key: value.strip() for (key, value) in keyValues.items()}
            atoms.append(Atom(keyValues))

    orthoMat = np.array(orthoMat, dtype='float64')
    header = PDBheader(pdbid, date, method, resolution, rValue, rFree, program, spaceGroup, rotationMats, orthoMat)
    return PDBentry(header, atoms)


class PDBentry:
    """:class:`pdb_eda.pdbParser.PDBentry` class that stores the :class:`pdb_eda.pdbParser.PDBheader` and/or :class:`pdb_eda.pdbParser.Atom` class."""

    def __init__(self, header, atoms):
        """:class:`pdb_eda.pdbParser.PDBentry` initializer. """
        self.header = header
        self.atoms = atoms

    def calcSymmetryAtoms(self, checkList):
        xs = sorted([i[0] for i in checkList])
        ys = sorted([i[1] for i in checkList])
        zs = sorted([i[2] for i in checkList])

        allAtoms = []
        oMat = np.linalg.inv(self.header.orthoMat[:, 0:3])
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for k in [-1, 0, 1]:
                    for r in range(len(self.header.rotationMats)):
                        if i == 0 and j == 0 and k == 0 and r == 0:
                            continue
                        else:
                            rMat = self.header.rotationMats[r]
                            otMat = np.dot(oMat, [i, j, k])
                            atoms = [symAtom(atom) for atom in self.atoms]
                            for x in atoms:
                                x.coord = np.dot(rMat[:, 0:3], x.coord) + rMat[:, 3] + otMat

                            ## test if the symmetry atoms are within the range of the checkList
                            inRangeAtoms = [x for x in atoms if xs[0] - 5 <= x.coord[0] <= xs[-1] + 5 and ys[0] - 5 <= x.coord[1] <= ys[-1] + 5 and zs[0] - 5 <= x.coord[2] <= zs[-1] + 5]

                        if len(inRangeAtoms):
                            for x in inRangeAtoms:
                                x.symmetry = [i, j, k, r]
                            allAtoms.extend(inRangeAtoms)

        return allAtoms


class PDBheader:
    """:class:`pdb_eda.pdbParser.PDBheader` that stores information about PDB header."""

    def __init__(self, PDBid, date, method, resolution, rValue, rFree, program, spaceGroup, rotationMats, orthoMat):
        """:class:`pdb_eda.pdbParser.PDBheader` initializer.

        :param str pdbid: PDB id.:param str pdbid: PDB id.
        :param str date: PDB structure publish date.
        :param str method: Experiment method, i.e. X-ray, NMR, etc.
        :param float resolution: Structure resolution if applicable.
        :param float rValue: Structure's R value.
        :param float rFree: Structure's R free value.
        :param str program: Software for acquiring the structure.
        :param str spaceGroup: Structure's space group if applicable.
        :param list rotationMats: Structure's rotation matrix and translation matrix if applicable.

        """
        self.pdbid = PDBid
        self.date = date
        self.method = method
        self.resolution = resolution
        self.rValue = rValue
        self.rFree = rFree
        self.program = program
        self.spaceGroup = spaceGroup
        self.rotationMats = rotationMats
        self.orthoMat = orthoMat


class Atom:
    """:class:`pdb_eda.pdbParser.Atom` that stores information about PDB atoms."""

    def __init__(self, keyValues):
        """
        :class:`pdb_eda.pdbParser.Atom` initializer.

        :param dict keyValues: Key value pairs for atom information.
        """
        self.record = keyValues['record']
        self.recordType = keyValues['recordType']
        self.serial = int(keyValues['serial'])
        self.atomName = keyValues['atomName']
        self.alternateLocation = keyValues['alternateLocation']
        self.residueName = keyValues['residueName']
        self.chainID = keyValues['chainID']
        self.residueNumber = int(keyValues['residueNumber'])
        self.x = float(keyValues['x'])
        self.y = float(keyValues['y'])
        self.z = float(keyValues['z'])
        self.coord = np.array([self.x, self.y, self.z])
        self.occupancy = float(keyValues['occupancy'])
        self.bFactor = float(keyValues['bFactor'])
        self.element = keyValues['element']


class symAtom:
    """A wrapper class to the `pdbParser.atom` class,
    delegate all BioPDB atom class method and data member except having its own symmetry and coordination """

    def __init__(self, atom):
        """
        `pdb_eda.densityAnalysis.symAtom` initializer.

        :param atom: `BioPDB.atom` object.
        """
        self.atom = atom
        self.coord = atom.coord
        self.symmetry = []

    def __getattr__(self, attr):
        return getattr(self.atom, attr)

