##
# File:    DictMethodRunnerHelper.py
# Author:  J. Westbrook
# Date:    18-Aug-2018
# Version: 0.001 Initial version
#
# Updates:
#  4-Sep-2018 jdw add methods to construct entry and entity identier categories.
# 10-Sep-2018 jdw add method for citation author aggregation
# 22-Sep-2018 jdw add method assignAssemblyCandidates()
# 27-Oct-2018 jdw add method consolidateAccessionDetails()
# 30-Oct-2018 jdw add category methods addChemCompRelated(), addChemCompInfo(),
#                 addChemCompDescriptor()
# 10-Nov-2018 jdw add addChemCompSynonyms(), addChemCompTargets(), filterBlockByMethod()
# 12-Nov-2018 jdw add InChIKey matching in addChemCompRelated()
# 15-Nov-2018 jdw add handling for antibody misrepresentation of multisource organisms
# 28-Nov-2018 jdw relax constraints on the production of rcsb_entry_info
#  1-Dec-2018 jdw add ncbi source and host organism info
# 11-Dec-2018 jdw add addStructRefSeqEntityIds and buildEntityPolySeq
# 10-Jan-2019 jdw better handle initialization in filterBlockByMethod()
# 11-Jan-2019 jdw revise classification in assignAssemblyCandidates()
# 16-Feb-2019 jdw add buildContainerEntityInstanceIds()
# 19-Feb-2019 jdw add internal method __addPdbxValidateAsymIds() to add cardinal identifiers to
#                 pdbx_validate_* categories
# 28-Feb-2019 jdw change criteria for adding rcsb_chem_comp_container_identiers to work with ion definitions
# 11-Mar-2019 jdw replace taxonomy file handling with calls to TaxonomyUtils()
# 11-Mar-2019 jdw add EC lineage using EnzymeDatabaseUtils()
# 17-Mar-2019 jdw add support for entity subcategory rcsb_macromolecular_names_combined
# 23-Mar-2019 jdw change criteria chem_comp collection criteria to _chem_comp.pdbx_release_status
# 25-Mar-2019 jdw remap merged taxons and adjust exception handling for taxonomy lineage generation
#  7-Apr-2019 jdw add CathClassificationUtils and CathClassificationUtils and sequence difference type counts
# 25-Apr-2019 jdw For source and host organism add ncbi_parent_scientific_name
#                 add rcsb_entry_info.deposited_modeled_polymer_monomer_count and
#                     rcsb_entry_info.deposited_unmodeled_polymer_monomer_count,
#  1-May-2019 jdw add support for _rcsb_entry_info.deposited_polymer_monomer_count,
#                   _rcsb_entry_info.polymer_entity_count_protein,
#                   _rcsb_entry_info.polymer_entity_count_nucleic_acid,
#                   _rcsb_entry_info.polymer_entity_count_nucleic_acid_hybrid,
#                   _rcsb_entry_info.polymer_entity_count_DNA,
#                   _rcsb_entry_info.polymer_entity_count_RNA,
#                   _rcsb_entry_info.nonpolymer_ligand_entity_count
#                   _rcsb_entry_info.selected_polymer_entity_types
#                   _rcsb_entry_info.polymer_entity_taxonomy_count
#                   _rcsb_entry_info.assembly_count
#                    add categories rcsb_entity_instance_domain_scop and rcsb_entity_instance_domain_cath
#  4-May-2019 jdw extend content in categories rcsb_entity_instance_domain_scop and rcsb_entity_instance_domain_cath
# 13-May-2019 jdw add rcsb_entry_info.deposited_polymer_entity_instance_count and deposited_nonpolymer_entity_instance_count
#                 add entity_poly.rcsb_non_std_monomer_count and rcsb_non_std_monomers
# 15-May-2019 jdw add _rcsb_entry_info.na_polymer_entity_types update enumerations for _rcsb_entry_info.selected_polymer_entity_types
# 19-May-2019 jdw add method __getStructConfInfo()
#
##
"""
This helper class implements external method references in the RCSB dictionary extension.

All data accessors and structures here refer to dictionary category and attribute names.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import datetime
import functools
import itertools
import logging
import re
from collections import Counter

from mmcif.api.DataCategory import DataCategory

from rcsb.db.helpers.DictMethodRunnerHelperBase import DictMethodRunnerHelperBase
from rcsb.utils.ec.EnzymeDatabaseUtils import EnzymeDatabaseUtils
from rcsb.utils.io.MarshalUtil import MarshalUtil
from rcsb.utils.struct.CathClassificationUtils import CathClassificationUtils
from rcsb.utils.struct.ScopClassificationUtils import ScopClassificationUtils
from rcsb.utils.taxonomy.TaxonomyUtils import TaxonomyUtils

logger = logging.getLogger(__name__)


def cmp_elements(lhs, rhs):
    return 0 if (lhs[-1].isdigit() or lhs[-1] in ['R', 'S']) and rhs[0].isdigit() else -1


class DictMethodRunnerHelper(DictMethodRunnerHelperBase):
    """ Helper class implements external method references in the RCSB dictionary extension.

    """
    # Dictionary of current standard monomers -
    monDict3 = {
        "ALA": "A",
        "ARG": "R",
        "ASN": "N",
        "ASP": "D",
        "ASX": "B",
        "CYS": "C",
        "GLN": "Q",
        "GLU": "E",
        "GLX": "Z",
        "GLY": "G",
        "HIS": "H",
        "ILE": "I",
        "LEU": "L",
        "LYS": "K",
        "MET": "M",
        "PHE": "F",
        "PRO": "P",
        "SER": "S",
        "THR": "T",
        "TRP": "W",
        "TYR": "Y",
        "VAL": "V",
        "PYL": "O",
        "SEC": "U",
        "DA": "A",
        "DC": "C",
        "DG": "G",
        "DT": "T",
        "DU": "U",
        "DI": "I",
        "A": "A",
        "C": "C",
        "G": "G",
        "I": "I",
        "N": "N",
        "T": "T",
        "U": "U",
        # "UNK": "X",
        #         "MSE":"M",
        # ".": "."
    }

    def __init__(self, **kwargs):
        """
        Args:
            **kwargs: (dict)  Placeholder for future key-value arguments

        """
        super(DictMethodRunnerHelper, self).__init__(**kwargs)
        self._thing = kwargs.get("thing", None)
        #
        self.__drugBankMappingFilePath = kwargs.get("drugBankMappingFilePath", None)
        self.__drugBankMappingDict = {}
        #
        self.__csdModelMappingFilePath = kwargs.get("csdModelMappingFilePath", None)
        self.__csdModelMappingDict = {}
        #
        self.__taxonomyDataPath = kwargs.get("taxonomyDataPath", None)
        self.__taxU = None
        #
        self.__enzymeDataPath = kwargs.get("enzymeDataPath", None)
        self.__ecU = None
        #
        self.__siftsMappingFilePath = kwargs.get("siftsMappingFilePath", None)
        self.__siftsMappingDict = {}
        #
        self.__structDomainDataPath = kwargs.get("structDomainDataPath", None)
        self.__scopU = None
        self.__cathU = None
        #
        self.__wsPattern = re.compile(r"\s+", flags=re.UNICODE | re.MULTILINE)
        self.__workPath = kwargs.get("workPath", None)
        logger.debug("Dictionary method helper init")
        #
        #
        self.__re_non_digit = re.compile(r'[^\d]+')
        #
        # Entry specifoc cache initialization for instance type and atom counts -
        #
        self.__cacheEntryId = None
        self.__instanceD = None
        self.__atomSiteCountD = None
        #

    def echo(self, msg):
        logger.info(msg)

    def setDatablockId(self, dataContainer, catName, atName, **kwargs):
        try:
            val = dataContainer.getName()
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=[atName]))
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii in range(numRows):
                cObj.setValue(val, atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def setLoadDateTime(self, dataContainer, catName, atName, **kwargs):
        try:
            val = dataContainer.getProp('load_date')
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=[atName]))
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii in range(numRows):
                cObj.setValue(val, atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def setLocator(self, dataContainer, catName, atName, **kwargs):
        try:
            val = dataContainer.getProp('locator')
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=[atName]))
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii in range(numRows):
                cObj.setValue(val, atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def setRowIndex(self, dataContainer, catName, atName, **kwargs):
        try:
            if not dataContainer.exists(catName):
                # exit if there is no category to index
                return False
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii, iRow in enumerate(range(numRows), 1):
                # Note - we set the integer value as a string  -
                cObj.setValue(str(ii), atName, iRow)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def __addPdbxValidateAsymIds(self, dataContainer, asymMapD, npAuthAsymMapD):
        """ Internal method to insert Asym_id's into the following categories:

                _pdbx_validate_close_contact.rcsb_label_asym_id_1
                _pdbx_validate_close_contact.rcsb_label_asym_id_2
                _pdbx_validate_symm_contact.rcsb_label_asym_id_1
                _pdbx_validate_symm_contact.rcsb_label_asym_id_2
                _pdbx_validate_rmsd_bond.rcsb_label_asym_id_1
                _pdbx_validate_rmsd_bond.rcsb_label_asym_id_2
                _pdbx_validate_rmsd_angle.rcsb_label_asym_id_1
                _pdbx_validate_rmsd_angle.rcsb_label_asym_id_2
                _pdbx_validate_rmsd_angle.rcsb_label_asym_id_3
                _pdbx_validate_torsion.rcsb_label_asym_id
                _pdbx_validate_peptide_omega.rcsb_label_asym_id_1
                _pdbx_validate_peptide_omega.rcsb_label_asym_id_2
                _pdbx_validate_chiral.rcsb_label_asym_id
                _pdbx_validate_planes.rcsb_label_asym_id
                _pdbx_validate_planes_atom.rcsb_label_asym_id
                _pdbx_validate_main_chain_plane.rcsb_label_asym_id
                _pdbx_validate_polymer_linkage.rcsb_label_asym_id_1
                _pdbx_validate_polymer_linkage.rcsb_label_asym_id_2
        """
        #
        mD = {'pdbx_validate_close_contact': [('auth_asym_id_1', 'auth_seq_id_1', 'rcsb_label_asym_id_1'), ('auth_asym_id_2', 'auth_seq_id_2', 'rcsb_label_asym_id_2')],
              'pdbx_validate_symm_contact': [('auth_asym_id_1', 'auth_seq_id_1', 'rcsb_label_asym_id_1'), ('auth_asym_id_2', 'auth_seq_id_2', 'rcsb_label_asym_id_2')],
              'pdbx_validate_rmsd_bond': [('auth_asym_id_1', 'auth_seq_id_1', 'rcsb_label_asym_id_1'), ('auth_asym_id_2', 'auth_seq_id_2', 'rcsb_label_asym_id_2')],
              'pdbx_validate_rmsd_angle': [('auth_asym_id_1', 'auth_seq_id_1', 'rcsb_label_asym_id_1'), ('auth_asym_id_2', 'auth_seq_id_2', 'rcsb_label_asym_id_2'), ('auth_asym_id_3', 'auth_seq_id_3', 'rcsb_label_asym_id_3')],
              'pdbx_validate_torsion': [('auth_asym_id', 'auth_seq_id', 'rcsb_label_asym_id')],
              'pdbx_validate_peptide_omega': [('auth_asym_id_1', 'auth_seq_id_1', 'rcsb_label_asym_id_1'), ('auth_asym_id_2', 'auth_seq_id_2', 'rcsb_label_asym_id_2')],
              'pdbx_validate_chiral': [('auth_asym_id', 'auth_seq_id', 'rcsb_label_asym_id')],
              'pdbx_validate_planes': [('auth_asym_id', 'auth_seq_id', 'rcsb_label_asym_id')],
              'pdbx_validate_planes_atom': [('auth_asym_id', 'auth_seq_id', 'rcsb_label_asym_id')],
              'pdbx_validate_main_chain_plane': [('auth_asym_id', 'auth_seq_id', 'rcsb_label_asym_id')],
              'pdbx_validate_polymer_linkage': [('auth_asym_id_1', 'auth_seq_id_1', 'rcsb_label_asym_id_1'), ('auth_asym_id_2', 'auth_seq_id_2', 'rcsb_label_asym_id_2')],
              'pdbx_distant_solvent_atoms': [('auth_asym_id', 'auth_seq_id', 'rcsb_label_asym_id')]}
        #
        # polymer lookup
        authAsymD = {}
        for asymId, d in asymMapD.items():
            if d['entity_type'].lower() in ['polymer', 'branched']:
                authAsymD[(d['auth_asym_id'], '?')] = asymId
        #
        # non-polymer lookup
        #
        logger.debug("%s authAsymD %r" % (dataContainer.getName(), authAsymD))
        for (authAsymId, seqId), d in npAuthAsymMapD.items():
            if d['entity_type'].lower() not in ['polymer', 'branched']:
                authAsymD[(authAsymId, seqId)] = d['asym_id']

        #
        for catName, mTupL in mD.items():
            if not dataContainer.exists(catName):
                continue
            cObj = dataContainer.getObj(catName)
            for ii in range(cObj.getRowCount()):
                for mTup in mTupL:
                    if cObj.hasAttribute(mTup[0]) and cObj.hasAttribute(mTup[1]):
                        authVal = cObj.getValue(mTup[0], ii)
                        authSeqId = cObj.getValue(mTup[1], ii)
                        #
                        # logger.debug("%s %4d authAsymId %r authSeqId %r" % (catName, ii, authVal, authSeqId))
                        #
                        if (authVal, authSeqId) in authAsymD:
                            if not cObj.hasAttribute(mTup[2]):
                                cObj.appendAttribute(mTup[2])
                            cObj.setValue(authAsymD[(authVal, authSeqId)], mTup[2], ii)
                        elif (authVal, '?') in authAsymD:
                            if not cObj.hasAttribute(mTup[2]):
                                cObj.appendAttribute(mTup[2])
                            cObj.setValue(authAsymD[(authVal, '?')], mTup[2], ii)

                        else:
                            if authVal not in ['.']:
                                logger.error("%s %s missing mapping auth asymId %s" % (dataContainer.getName(), catName, authVal))
                    else:
                        logger.error("%s %s missing required attributes %s %s" % (dataContainer.getName(), catName, mTup[0], mTup[1]))

        return True

    def aggregateCitationAuthors(self, dataContainer, catName, atName, **kwargs):
        try:
            if not dataContainer.exists(catName) or not dataContainer.exists('citation_author'):
                return False
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            citIdL = cObj.getAttributeValueList('id')
            #
            tObj = dataContainer.getObj('citation_author')
            #
            citIdL = list(set(citIdL))
            tD = {}
            for ii, citId in enumerate(citIdL):
                tD[citId] = tObj.selectValuesWhere('name', citId, 'citation_id')
            for ii in range(cObj.getRowCount()):
                citId = cObj.getValue('id', ii)
                cObj.setValue('|'.join(tD[citId]), atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def buildContainerEntryIds(self, dataContainer, catName, **kwargs):
        """
        Build:

        loop_
        _rcsb_entry_container_identifiers.entry_id
        _rcsb_entry_container_identifiers.entity_ids
        _rcsb_entry_container_identifiers.polymer_entity_ids_polymer
        _rcsb_entry_container_identifiers.non-polymer_entity_ids
        _rcsb_entry_container_identifiers.assembly_ids
        ...
        """
        try:
            if not dataContainer.exists('entry'):
                return False
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id', 'entity_ids', 'polymer_entity_ids',
                                                                              'non-polymer_entity_ids', 'assembly_ids']))
            #
            cObj = dataContainer.getObj(catName)

            tObj = dataContainer.getObj('entry')
            entryId = tObj.getValue('id', 0)
            cObj.setValue(entryId, 'entry_id', 0)
            #
            tObj = dataContainer.getObj('entity')
            entityIdL = tObj.getAttributeValueList('id')
            cObj.setValue(','.join(entityIdL), 'entity_ids', 0)
            #
            #
            pIdL = tObj.selectValuesWhere('id', 'polymer', 'type')
            tV = ','.join(pIdL) if pIdL else '?'
            cObj.setValue(tV, 'polymer_entity_ids', 0)

            npIdL = tObj.selectValuesWhere('id', 'non-polymer', 'type')
            tV = ','.join(npIdL) if npIdL else '?'
            cObj.setValue(tV, 'non-polymer_entity_ids', 0)
            #
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            assemblyIdL = tObj.getAttributeValueList('id') if tObj else []
            tV = ','.join(assemblyIdL) if assemblyIdL else '?'
            cObj.setValue(tV, 'assembly_ids', 0)

            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def buildContainerEntityIds(self, dataContainer, catName, **kwargs):
        """
        Build:

        loop_
        _rcsb_entity_container_identifiers.entry_id
        _rcsb_entity_container_identifiers.entity_id
        #
        _rcsb_entity_container_identifiers.asym_ids
        _rcsb_entity_container_identifiers.auth_asym_ids
        #
        _rcsb_entity_container_identifiers.nonpolymer_comp_id
        _rcsb_entity_container_identifiers.chem_comp_monomers
        ...
        """
        try:
            if not (dataContainer.exists('entry') and dataContainer.exists('entity')):
                return False
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id', 'entity_id', 'asym_ids',
                                                                              'auth_asym_ids', 'chem_comp_monomers', 'nonpolymer_comp_id']))
            #
            cObj = dataContainer.getObj(catName)

            psObj = dataContainer.getObj('pdbx_poly_seq_scheme')
            npsObj = dataContainer.getObj('pdbx_nonpoly_scheme')
            #
            tObj = dataContainer.getObj('entry')
            entryId = tObj.getValue('id', 0)
            cObj.setValue(entryId, 'entry_id', 0)
            #
            tObj = dataContainer.getObj('entity')
            entityIdL = tObj.getAttributeValueList('id')
            #
            for ii, entityId in enumerate(entityIdL):
                cObj.setValue(entryId, 'entry_id', ii)
                cObj.setValue(entityId, 'entity_id', ii)
                eType = tObj.getValue('type', ii)
                asymIdL = []
                authAsymIdL = []
                ccMonomerL = []
                ccLigandL = []
                if eType == 'polymer' and psObj:
                    asymIdL = psObj.selectValuesWhere('asym_id', entityId, 'entity_id')
                    authAsymIdL = psObj.selectValuesWhere('pdb_strand_id', entityId, 'entity_id')
                    ccMonomerL = psObj.selectValuesWhere('mon_id', entityId, 'entity_id')
                elif npsObj:
                    asymIdL = npsObj.selectValuesWhere('asym_id', entityId, 'entity_id')
                    authAsymIdL = npsObj.selectValuesWhere('pdb_strand_id', entityId, 'entity_id')
                    ccLigandL = npsObj.selectValuesWhere('mon_id', entityId, 'entity_id')
                    logger.debug("entityId %r ligands %r" % (entityId, set(ccLigandL)))
                #
                if asymIdL:
                    cObj.setValue(','.join(list(set(asymIdL))).strip(), 'asym_ids', ii)
                if authAsymIdL:
                    cObj.setValue(','.join(list(set(authAsymIdL))).strip(), 'auth_asym_ids', ii)
                if ccMonomerL:
                    cObj.setValue(','.join(list(set(ccMonomerL))).strip(), 'chem_comp_monomers', ii)
                else:
                    cObj.setValue('?', 'chem_comp_monomers', ii)
                if ccLigandL:
                    cObj.setValue(','.join(set(ccLigandL)).strip(), 'nonpolymer_comp_id', ii)
                else:
                    cObj.setValue('?', 'nonpolymer_comp_id', ii)

            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def buildContainerEntityInstanceIds(self, dataContainer, catName, **kwargs):
        """
        Build:

        loop_
        _rcsb_entity_instance_container_identifiers.entry_id
        _rcsb_entity_instance_container_identifiers.entity_id
        _rcsb_entity_instance_container_identifiers.entity_type
        _rcsb_entity_instance_container_identifiers.asym_id
        _rcsb_entity_instance_container_identifiers.auth_asym_id
        _rcsb_entity_instance_container_identifiers.comp_id
        _rcsb_entity_instance_container_identifiers.auth_seq_id


            loop_
            _pdbx_poly_seq_scheme.asym_id
            _pdbx_poly_seq_scheme.entity_id
            _pdbx_poly_seq_scheme.seq_id
            _pdbx_poly_seq_scheme.mon_id
            _pdbx_poly_seq_scheme.ndb_seq_num
            _pdbx_poly_seq_scheme.pdb_seq_num
            _pdbx_poly_seq_scheme.auth_seq_num
            _pdbx_poly_seq_scheme.pdb_mon_id
            _pdbx_poly_seq_scheme.auth_mon_id
            _pdbx_poly_seq_scheme.pdb_strand_id
            _pdbx_poly_seq_scheme.pdb_ins_code
            _pdbx_poly_seq_scheme.hetero
            A 1 1  MET 1  1  ?  ?   ?   A . n
            A 1 2  ALA 2  2  ?  ?   ?   A . n

            loop_
            _pdbx_nonpoly_scheme.asym_id
            _pdbx_nonpoly_scheme.entity_id
            _pdbx_nonpoly_scheme.mon_id
            _pdbx_nonpoly_scheme.ndb_seq_num
            _pdbx_nonpoly_scheme.pdb_seq_num
            _pdbx_nonpoly_scheme.auth_seq_num
            _pdbx_nonpoly_scheme.pdb_mon_id
            _pdbx_nonpoly_scheme.auth_mon_id
            _pdbx_nonpoly_scheme.pdb_strand_id
            _pdbx_nonpoly_scheme.pdb_ins_code
            H 3 ADP 1  105 105 ADP ADP A .
            I 3 ADP 1  101 101 ADP ADP B .
            J 4 MG  1  66  1   MG  MG  B .
            K 3 ADP 1  102 102 ADP ADP C .
        ...
        """
        try:
            if not (dataContainer.exists('entry') and dataContainer.exists('entity')):
                return False
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id', 'entity_id', 'entity_type', 'asym_id', 'auth_asym_id', 'comp_id', 'auth_seq_id']))
            #
            cObj = dataContainer.getObj(catName)
            #
            eObj = dataContainer.getObj('entity')
            eD = {}
            for ii in range(eObj.getRowCount()):
                entityId = eObj.getValue('id', ii)
                entityType = eObj.getValue('type', ii)
                eD[entityId] = entityType
            #

            psObj = dataContainer.getObj('pdbx_poly_seq_scheme')
            npsObj = dataContainer.getObj('pdbx_nonpoly_scheme')
            #
            tObj = dataContainer.getObj('entry')
            entryId = tObj.getValue('id', 0)

            cObj.setValue(entryId, 'entry_id', 0)
            #
            asymD = {}
            npAuthAsymD = {}
            if psObj is not None:
                for ii in range(psObj.getRowCount()):
                    asymId = psObj.getValue('asym_id', ii)
                    if asymId in asymD:
                        continue
                    entityId = psObj.getValue('entity_id', ii)
                    authAsymId = psObj.getValue('pdb_strand_id', ii)
                    asymD[asymId] = {'entry_id': entryId, 'entity_id': entityId, 'entity_type': eD[entityId],
                                     'asym_id': asymId, 'auth_asym_id': authAsymId, 'comp_id': '?', 'auth_seq_id': '?'}
                    #
            if npsObj is not None:
                for ii in range(npsObj.getRowCount()):
                    asymId = npsObj.getValue('asym_id', ii)

                    entityId = npsObj.getValue('entity_id', ii)
                    authAsymId = npsObj.getValue('pdb_strand_id', ii)
                    resNum = npsObj.getValue('pdb_seq_num', ii)
                    monId = npsObj.getValue('mon_id', ii)
                    if asymId not in asymD:
                        asymD[asymId] = {'entry_id': entryId, 'entity_id': entityId, 'entity_type': eD[entityId],
                                         'asym_id': asymId, 'auth_asym_id': authAsymId, 'comp_id': monId, 'auth_seq_id': '?'}
                    npAuthAsymD[(authAsymId, resNum)] = {'entry_id': entryId, 'entity_id': entityId, 'entity_type': eD[entityId],
                                                         'asym_id': asymId, 'auth_asym_id': authAsymId, 'comp_id': monId, 'auth_seq_id': resNum}

            # JDW TODO MAKE npsObj extended mapping !
            #
            for ii, ky in enumerate(sorted(asymD)):
                for k, v in asymD[ky].items():
                    cObj.setValue(v, k, ii)

            ok = self.__addPdbxValidateAsymIds(dataContainer, asymD, npAuthAsymD)
            return ok
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def __expandOperatorList(self, operExpression):
        """
        Operation expressions may have the forms:

                (1)        the single operation 1
                (1,2,5)    the operations 1, 2, 5
                (1-4)      the operations 1,2,3 and 4
                (1,2)(3,4) the combinations of operations
                           3 and 4 followed by 1 and 2 (i.e.
                           the cartesian product of parenthetical
                           groups applied from right to left)
        """

        rL = []
        opCount = 1
        try:
            if operExpression.find('(') < 0:
                opL = [operExpression]
            else:
                opL = [t.strip().strip('(').rstrip(')') for t in re.findall(r'\(.*?\)', operExpression)]
            #
            for op in opL:
                teL = []
                tL = op.split(',')
                for t in tL:
                    trngL = t.split('-')
                    if len(trngL) == 2:
                        rngL = [str(r) for r in range(int(trngL[0]), int(trngL[1]) + 1)]
                    else:
                        rngL = trngL
                    teL.extend(rngL)
                rL.append(teL)
                opCount *= len(teL)

        except Exception as e:
            logger.exception("Failing parsing %r with %s" % (operExpression, str(e)))
        #
        if len(rL) < 1:
            opCount = 0
        return opCount, rL

    def __getAssemblyComposition(self, dataContainer):
        """ Return assembly composition by entity and instance type counts.

            Example -
                loop_
                _pdbx_struct_assembly.id
                _pdbx_struct_assembly.details
                _pdbx_struct_assembly.method_details
                _pdbx_struct_assembly.oligomeric_details
                _pdbx_struct_assembly.oligomeric_count
                1 'complete icosahedral assembly'                ? 180-meric      180
                2 'icosahedral asymmetric unit'                  ? trimeric       3
                3 'icosahedral pentamer'                         ? pentadecameric 15
                4 'icosahedral 23 hexamer'                       ? octadecameric  18
                5 'icosahedral asymmetric unit, std point frame' ? trimeric       3
                #
                loop_
                _pdbx_struct_assembly_gen.assembly_id
                _pdbx_struct_assembly_gen.oper_expression
                _pdbx_struct_assembly_gen.asym_id_list
                1 '(1-60)'           A,B,C
                2 1                  A,B,C
                3 '(1-5)'            A,B,C
                4 '(1,2,6,10,23,24)' A,B,C
                5 P                  A,B,C
                #
        """
        #
        instanceD = self.__getInstanceTypes(dataContainer)
        instanceTypeD = instanceD['instanceTypeD'] if 'instanceTypeD' in instanceD else {}
        instancePolymerTypeD = instanceD['instancePolymerTypeD'] if 'instancePolymerTypeD' in instanceD else {}
        instEntityD = instanceD['instEntityD'] if 'instEntityD' in instanceD else {}
        epTypeD = instanceD['epTypeD'] if 'epTypeD' in instanceD else {}
        eTypeD = instanceD['eTypeD'] if 'eTypeD' in instanceD else {}
        epTypeFilteredD = instanceD['epTypeFilteredD'] if 'epTypeFilteredD' in instanceD else {}
        #
        atomSiteCountD = self.__getQualifiedAtomSiteInfo(dataContainer, instanceTypeD)
        instAtomCount = atomSiteCountD['instanceAtomCountD'] if 'instanceAtomCountD' in atomSiteCountD else {}
        instModeledMonomerCount = atomSiteCountD['instanceModeledMonomerCountD'] if 'instanceModeledMonomerCountD' in atomSiteCountD else {}
        instUnmodeledMonomerCount = atomSiteCountD['instanceUnmodeledMonomerCountD'] if 'instanceUnmodeledMonomerCountD' in atomSiteCountD else {}
        #
        # -------------------------
        assemblyInstanceCountByTypeD = {}
        assemblyAtomCountByTypeD = {}
        assemblyAtomCountD = {}
        assemblyModeledMonomerCountD = {}
        assemblyUnmodeledMonomerCountD = {}
        # Pre-generation (source instances)
        assemblyInstanceD = {}
        # Post-generation (gerated instances)
        assemblyInstanceGenD = {}
        assemblyInstanceCountByPolymerTypeD = {}
        assemblyPolymerInstanceCountD = {}
        assemblyPolymerClassD = {}
        #
        assemblyEntityCountByPolymerTypeD = {}
        assemblyEntityCountByTypeD = {}
        # --------------
        #
        try:
            if dataContainer.exists('pdbx_struct_assembly_gen'):
                tObj = dataContainer.getObj('pdbx_struct_assembly_gen')
                for ii in range(tObj.getRowCount()):
                    assemblyId = tObj.getValue('assembly_id', ii)
                    # Initialize instances count
                    if assemblyId not in assemblyInstanceCountByTypeD:
                        assemblyInstanceCountByTypeD[assemblyId] = {eType: 0 for eType in ['polymer', 'non-polymer', 'branched', 'macrolide', 'water']}
                    if assemblyId not in assemblyAtomCountByTypeD:
                        assemblyAtomCountByTypeD[assemblyId] = {eType: 0 for eType in ['polymer', 'non-polymer', 'branched', 'macrolide', 'water']}
                    if assemblyId not in assemblyModeledMonomerCountD:
                        assemblyModeledMonomerCountD[assemblyId] = 0
                    if assemblyId not in assemblyUnmodeledMonomerCountD:
                        assemblyUnmodeledMonomerCountD[assemblyId] = 0
                    if assemblyId not in assemblyAtomCountD:
                        assemblyAtomCountD[assemblyId] = 0
                    #
                    opExpression = tObj.getValue('oper_expression', ii)
                    opCount, opL = self.__expandOperatorList(opExpression)
                    tS = tObj.getValue('asym_id_list', ii)
                    asymIdList = [t.strip() for t in tS.strip().split(',')]
                    assemblyInstanceD.setdefault(assemblyId, []).extend(asymIdList)
                    assemblyInstanceGenD.setdefault(assemblyId, []).extend(asymIdList * opCount)
                    #
                    logger.debug("%s assembly %r opExpression %r opCount %d opL %r" % (dataContainer.getName(), assemblyId, opExpression, opCount, opL))
                    logger.debug("%s assembly %r length asymIdList %r" % (dataContainer.getName(), assemblyId, len(asymIdList)))
                    #
                    for eType in ['polymer', 'non-polymer', 'branched', 'macrolide', 'water']:
                        iList = [asymId for asymId in asymIdList if asymId in instanceTypeD and instanceTypeD[asymId] == eType]
                        assemblyInstanceCountByTypeD[assemblyId][eType] += len(iList) * opCount
                        #
                        atCountList = [instAtomCount[asymId] for asymId in asymIdList if asymId in instanceTypeD and instanceTypeD[asymId] == eType and asymId in instAtomCount]
                        assemblyAtomCountByTypeD[assemblyId][eType] += sum(atCountList) * opCount
                        assemblyAtomCountD[assemblyId] += sum(atCountList) * opCount
                        #
                    #
                    modeledMonomerCountList = [instModeledMonomerCount[asymId]
                                               for asymId in asymIdList if asymId in instanceTypeD and instanceTypeD[asymId] == 'polymer' and asymId in instModeledMonomerCount]
                    assemblyModeledMonomerCountD[assemblyId] += sum(modeledMonomerCountList) * opCount
                    #
                    unmodeledMonomerCountList = [instUnmodeledMonomerCount[asymId]
                                                 for asymId in asymIdList if asymId in instanceTypeD and instanceTypeD[asymId] == 'polymer' and asymId in instUnmodeledMonomerCount]
                    assemblyUnmodeledMonomerCountD[assemblyId] += sum(unmodeledMonomerCountList) * opCount

                #
                assemblyInstanceCountByPolymerTypeD = {}
                assemblyPolymerInstanceCountD = {}
                assemblyPolymerClassD = {}
                #
                assemblyEntityCountByPolymerTypeD = {}
                assemblyEntityCountByTypeD = {}
                #
                # Using the generated list of instance assembly components ...
                for assemblyId, asymIdList in assemblyInstanceGenD.items():
                    # ------
                    #  Instance polymer composition
                    pInstTypeList = [instancePolymerTypeD[asymId] for asymId in asymIdList if asymId in instancePolymerTypeD]
                    pInstTypeD = Counter(pInstTypeList)
                    assemblyInstanceCountByPolymerTypeD[assemblyId] = {pType: 0 for pType in ['Protein', 'DNA', 'RNA', 'NA-hybrid', 'Other']}
                    assemblyInstanceCountByPolymerTypeD[assemblyId] = {pType: pInstTypeD[pType] for pType in ['Protein', 'DNA', 'RNA', 'NA-hybrid', 'Other'] if pType in pInstTypeD}
                    assemblyPolymerInstanceCountD[assemblyId] = len(pInstTypeList)
                    #
                    logger.debug("%s assemblyId %r pInstTypeD %r" % (dataContainer.getName(), assemblyId, pInstTypeD.items()))

                    # -------------
                    # Entity and polymer entity composition
                    #
                    entityIdList = list(set([instEntityD[asymId] for asymId in asymIdList if asymId in instEntityD]))
                    pTypeL = [epTypeD[entityId] for entityId in entityIdList if entityId in epTypeD]
                    #
                    polymerCompClass, subsetCompClass, naCompClass, _ = self.__getPolymerComposition(pTypeL)
                    assemblyPolymerClassD[assemblyId] = {'polymerCompClass': polymerCompClass, 'subsetCompClass': subsetCompClass, 'naCompClass': naCompClass}
                    #
                    logger.debug("%s assemblyId %s polymerCompClass %r subsetCompClass %r naCompClass %r pTypeL %r" %
                                 (dataContainer.getName(), assemblyId, polymerCompClass, subsetCompClass, naCompClass, pTypeL))

                    pTypeFilteredL = [epTypeFilteredD[entityId] for entityId in entityIdList if entityId in epTypeFilteredD]
                    #
                    pEntityTypeD = Counter(pTypeFilteredL)
                    assemblyEntityCountByPolymerTypeD[assemblyId] = {pType: 0 for pType in ['Protein', 'DNA', 'RNA', 'NA-hybrid', 'Other']}
                    assemblyEntityCountByPolymerTypeD[assemblyId] = {pType: pEntityTypeD[pType]
                                                                     for pType in ['Protein', 'DNA', 'RNA', 'NA-hybrid', 'Other'] if pType in pEntityTypeD}
                    #
                    eTypeL = [eTypeD[entityId] for entityId in entityIdList if entityId in eTypeD]
                    entityTypeD = Counter(eTypeL)
                    assemblyEntityCountByTypeD[assemblyId] = {eType: 0 for eType in ['polymer', 'non-polymer', 'branched', 'macrolide', 'water']}
                    assemblyEntityCountByTypeD[assemblyId] = {eType: entityTypeD[eType]
                                                              for eType in ['polymer', 'non-polymer', 'branched', 'macrolide', 'water'] if eType in entityTypeD}
                    #
                    # ---------------
                    #
            #
            logger.debug("%s assemblyInstanceCountByTypeD %r" % (dataContainer.getName(), assemblyInstanceCountByTypeD.items()))
            logger.debug("%s assemblyAtomCountByTypeD %r" % (dataContainer.getName(), assemblyAtomCountByTypeD.items()))
            logger.debug("%s assemblyAtomCountD %r" % (dataContainer.getName(), assemblyAtomCountD.items()))
            logger.debug("%s assemblyModeledMonomerCountD %r" % (dataContainer.getName(), assemblyModeledMonomerCountD.items()))
            logger.debug("%s assemblyUnmodeledMonomerCountD %r" % (dataContainer.getName(), assemblyUnmodeledMonomerCountD.items()))
            logger.debug("%s assemblyPolymerClassD %r" % (dataContainer.getName(), assemblyPolymerClassD.items()))
            logger.debug("%s assemblyPolymerInstanceCountD %r" % (dataContainer.getName(), assemblyPolymerInstanceCountD.items()))
            logger.debug("%s assemblyInstanceCountByPolymerTypeD %r" % (dataContainer.getName(), assemblyInstanceCountByPolymerTypeD.items()))
            logger.debug("%s assemblyEntityCountByPolymerTypeD %r" % (dataContainer.getName(), assemblyEntityCountByPolymerTypeD.items()))
            logger.debug("%s assemblyEntityCountByTypeD %r" % (dataContainer.getName(), assemblyEntityCountByTypeD.items()))
            #
            rD = {'assemblyInstanceCountByTypeD': assemblyInstanceCountByTypeD,
                  'assemblyAtomCountByTypeD': assemblyAtomCountByTypeD,
                  'assemblyAtomCountD': assemblyAtomCountD,
                  'assemblyModeledMonomerCountD': assemblyModeledMonomerCountD,
                  'assemblyUnmodeledMonomerCountD': assemblyUnmodeledMonomerCountD,
                  'assemblyInstanceCountByPolymerTypeD': assemblyInstanceCountByPolymerTypeD,
                  'assemblyPolymerInstanceCountD': assemblyPolymerInstanceCountD,
                  'assemblyPolymerClassD': assemblyPolymerClassD,
                  'assemblyEntityCountByPolymerTypeD': assemblyEntityCountByPolymerTypeD,
                  'assemblyEntityCountByTypeD': assemblyEntityCountByTypeD
                  }
        except Exception as e:
            logger.exception("Failing %s with %s" % (dataContainer.getName(), str(e)))
        return rD

    def addAssemblyInfo(self, dataContainer, catName, **kwargs):
        """ Build rcsb_assembly_info category.
        """
        try:
            if not (dataContainer.exists('entry') and dataContainer.exists('pdbx_struct_assembly')):
                return False
            logger.debug("%s beginning for %s" % (dataContainer.getName(), catName))
            # Create the new target category rcsb_assembly_info
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id',
                                                                              'assembly_id',
                                                                              'polymer_atom_count',
                                                                              'nonpolymer_atom_count',
                                                                              'branched_atom_count',
                                                                              'solvent_atom_count',
                                                                              'atom_count',
                                                                              'modeled_polymer_monomer_count',
                                                                              'unmodeled_polymer_monomer_count',
                                                                              'polymer_monomer_count',
                                                                              'polymer_composition',
                                                                              'selected_polymer_entity_types',
                                                                              'na_polymer_entity_types',
                                                                              'polymer_entity_instance_count',
                                                                              'nonpolymer_entity_instance_count',
                                                                              'branched_entity_instance_count',
                                                                              'solvent_entity_instance_count',
                                                                              'polymer_entity_instance_count_protein',
                                                                              'polymer_entity_instance_count_nucleic_acid',
                                                                              'polymer_entity_instance_count_DNA',
                                                                              'polymer_entity_instance_count_RNA',
                                                                              'polymer_entity_instance_count_nucleic_acid_hybrid',
                                                                              'polymer_entity_count',
                                                                              'nonpolymer_entity_count',
                                                                              'branched_entity_count',
                                                                              'solvent_entity_count',
                                                                              'polymer_entity_count_protein',
                                                                              'polymer_entity_count_nucleic_acid',
                                                                              'polymer_entity_count_DNA',
                                                                              'polymer_entity_count_RNA',
                                                                              'polymer_entity_count_nucleic_acid_hybrid']))
            #
            #
            logger.debug("%s beginning for %s" % (dataContainer.getName(), catName))
            #
            # Get assembly comp details -
            #
            rD = self.__getAssemblyComposition(dataContainer)
            #
            cObj = dataContainer.getObj(catName)

            tObj = dataContainer.getObj('entry')
            entryId = tObj.getValue('id', 0)
            #
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            assemblyIdL = tObj.getAttributeValueList('id')
            #
            #
            for ii, assemblyId in enumerate(assemblyIdL):
                cObj.setValue(entryId, 'entry_id', ii)
                cObj.setValue(assemblyId, 'assembly_id', ii)
                #
                d = rD['assemblyAtomCountByTypeD'][assemblyId]
                num = d['polymer'] if 'polymer' in d else 0
                cObj.setValue(num, 'polymer_atom_count', ii)

                num = d['non-polymer'] if 'non-polymer' in d else 0
                cObj.setValue(num, 'nonpolymer_atom_count', ii)

                num = d['water'] if 'water' in d else 0
                cObj.setValue(num, 'solvent_atom_count', ii)

                num = d['branched'] if 'branched' in d else 0
                cObj.setValue(num, 'branched_atom_count', ii)

                num = rD['assemblyAtomCountD'][assemblyId]
                cObj.setValue(num, 'atom_count', ii)
                #
                num1 = rD['assemblyModeledMonomerCountD'][assemblyId]
                num2 = rD['assemblyUnmodeledMonomerCountD'][assemblyId]
                cObj.setValue(num1, 'modeled_polymer_monomer_count', ii)
                cObj.setValue(num2, 'unmodeled_polymer_monomer_count', ii)
                cObj.setValue(num1 + num2, 'polymer_monomer_count', ii)
                #
                d = rD['assemblyPolymerClassD'][assemblyId]
                cObj.setValue(d['polymerCompClass'], 'polymer_composition', ii)
                cObj.setValue(d['subsetCompClass'], 'selected_polymer_entity_types', ii)
                cObj.setValue(d['naCompClass'], 'na_polymer_entity_types', ii)
                #
                d = rD['assemblyInstanceCountByTypeD'][assemblyId]
                num = d['polymer'] if 'polymer' in d else 0
                cObj.setValue(num, 'polymer_entity_instance_count', ii)
                #
                num = d['non-polymer'] if 'non-polymer' in d else 0
                cObj.setValue(num, 'nonpolymer_entity_instance_count', ii)
                #
                num = d['branched'] if 'branched' in d else 0
                cObj.setValue(num, 'branched_entity_instance_count', ii)
                #
                num = d['water'] if 'water' in d else 0
                cObj.setValue(num, 'solvent_entity_instance_count', ii)
                #
                d = rD['assemblyInstanceCountByPolymerTypeD'][assemblyId]
                num = d['Protein'] if 'Protein' in d else 0
                cObj.setValue(num, 'polymer_entity_instance_count_protein', ii)
                num1 = d['DNA'] if 'DNA' in d else 0
                cObj.setValue(num1, 'polymer_entity_instance_count_DNA', ii)
                num2 = d['RNA'] if 'RNA' in d else 0
                cObj.setValue(num2, 'polymer_entity_instance_count_RNA', ii)
                cObj.setValue(num1 + num2, 'polymer_entity_instance_count_nucleic_acid', ii)
                num = d['NA-hybrid'] if 'NA-hybrid' in d else 0
                cObj.setValue(num, 'polymer_entity_instance_count_nucleic_acid_hybrid', ii)
                #
                d = rD['assemblyEntityCountByPolymerTypeD'][assemblyId]
                num = d['Protein'] if 'Protein' in d else 0
                cObj.setValue(num, 'polymer_entity_count_protein', ii)
                num1 = d['DNA'] if 'DNA' in d else 0
                cObj.setValue(num1, 'polymer_entity_count_DNA', ii)
                num2 = d['RNA'] if 'RNA' in d else 0
                cObj.setValue(num2, 'polymer_entity_count_RNA', ii)
                cObj.setValue(num1 + num2, 'polymer_entity_count_nucleic_acid', ii)
                num = d['NA-hybrid'] if 'NA-hybrid' in d else 0
                cObj.setValue(num, 'polymer_entity_count_nucleic_acid_hybrid', ii)
                #
                d = rD['assemblyEntityCountByTypeD'][assemblyId]
                num = d['polymer'] if 'polymer' in d else 0
                cObj.setValue(num, 'polymer_entity_count', ii)
                #
                num = d['non-polymer'] if 'non-polymer' in d else 0
                cObj.setValue(num, 'nonpolymer_entity_count', ii)
                #
                num = d['branched'] if 'branched' in d else 0
                cObj.setValue(num, 'branched_entity_count', ii)
                #
                num = d['water'] if 'water' in d else 0
                cObj.setValue(num, 'solvent_entity_count', ii)
            #
            return
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def buildContainerAssemblyIds(self, dataContainer, catName, **kwargs):
        """
        Build:

        loop_
        _rcsb_assembly_container_identifiers.entry_id
        _rcsb_assembly_container_identifiers.assembly_id
        ...


        """
        try:
            if not (dataContainer.exists('entry') and dataContainer.exists('pdbx_struct_assembly')):
                return False
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id', 'assembly_id']))
            #
            cObj = dataContainer.getObj(catName)

            tObj = dataContainer.getObj('entry')
            entryId = tObj.getValue('id', 0)
            cObj.setValue(entryId, 'entry_id', 0)
            #
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            assemblyIdL = tObj.getAttributeValueList('id')
            for ii, assemblyId in enumerate(assemblyIdL):
                cObj.setValue(entryId, 'entry_id', ii)
                cObj.setValue(assemblyId, 'assembly_id', ii)

            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def addDepositedAssembly(self, dataContainer, catName, **kwargs):
        """ Add the deposited coordinates as a separate assembly labeled as 'deposited'.

        """
        try:
            if not dataContainer.exists('struct_asym'):
                return False
            if not dataContainer.exists('pdbx_struct_assembly'):
                dataContainer.append(DataCategory('pdbx_struct_assembly', attributeNameList=['id', 'details', 'method_details',
                                                                                             'oligomeric_details', 'oligomeric_count',
                                                                                             'rcsb_details', 'rcsb_candidate_assembly']))
            if not dataContainer.exists('pdbx_struct_assembly_gen'):
                dataContainer.append(DataCategory('pdbx_struct_assembly_gen', attributeNameList=['assembly_id', 'oper_expression', 'asym_id_list', 'ordinal']))

            if not dataContainer.exists('pdbx_struct_oper_list'):
                row = ['1', 'identity operation', '1_555', 'x, y, z', '1.0000000000', '0.0000000000', '0.0000000000',
                       '0.0000000000', '0.0000000000', '1.0000000000', '0.0000000000', '0.0000000000',
                       '0.0000000000', '0.0000000000', '1.0000000000', '0.0000000000']
                atList = ['id', 'type', 'name', 'symmetry_operation', 'matrix[1][1]', 'matrix[1][2]', 'matrix[1][3]',
                          'vector[1]', 'matrix[2][1]', 'matrix[2][2]', 'matrix[2][3]', 'vector[2]',
                          'matrix[3][1]', 'matrix[3][2]', 'matrix[3][3]', 'vector[3]']
                dataContainer.append(DataCategory('pdbx_struct_oper_list', attributeNameList=atList, rowList=[row]))

            #
            logger.debug("Add deposited assembly for %s" % dataContainer.getName())
            cObj = dataContainer.getObj('struct_asym')
            asymIdL = cObj.getAttributeValueList('id')
            logger.debug("AsymIdL %r" % asymIdL)
            #
            # Ordinal is added by subsequent attribure-level method.
            tObj = dataContainer.getObj('pdbx_struct_assembly_gen')
            rowIdx = tObj.getRowCount()
            tObj.setValue('deposited', 'assembly_id', rowIdx)
            tObj.setValue('1', 'oper_expression', rowIdx)
            tObj.setValue(','.join(asymIdL), 'asym_id_list', rowIdx)
            #
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            rowIdx = tObj.getRowCount()
            tObj.setValue('deposited', 'id', rowIdx)
            tObj.setValue('deposited_coordinates', 'details', rowIdx)
            #
            for atName in ['oligomeric_details', 'method_details', 'oligomeric_count']:
                if tObj.hasAttribute(atName):
                    tObj.setValue('?', atName, rowIdx)
            #
            #
            #
            logger.debug("Full row is %r" % tObj.getRow(rowIdx))
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def filterAssemblyDetails(self, dataContainer, catName, atName, **kwargs):
        """ Filter _pdbx_struct_assembly.details -> _pdbx_struct_assembly.rcsb_details
            with a more limited vocabulary -

                'author_and_software_defined_assembly'
                'author_defined_assembly'
                'software_defined_assembly'

        """
        mD = {'author_and_software_defined_assembly': 'author_and_software_defined_assembly',
              'author_defined_assembly': 'author_defined_assembly',
              'complete icosahedral assembly': 'author_and_software_defined_assembly',
              'complete point assembly': 'author_and_software_defined_assembly',
              'crystal asymmetric unit': 'software_defined_assembly',
              'crystal asymmetric unit, crystal frame': 'software_defined_assembly',
              'details': 'software_defined_assembly',
              'helical asymmetric unit': 'software_defined_assembly',
              'helical asymmetric unit, std helical frame': 'software_defined_assembly',
              'icosahedral 23 hexamer': 'software_defined_assembly',
              'icosahedral asymmetric unit': 'software_defined_assembly',
              'icosahedral asymmetric unit, std point frame': 'software_defined_assembly',
              'icosahedral pentamer': 'software_defined_assembly',
              'pentasymmetron capsid unit': 'software_defined_assembly',
              'point asymmetric unit': 'software_defined_assembly',
              'point asymmetric unit, std point frame': 'software_defined_assembly',
              'representative helical assembly': 'author_and_software_defined_assembly',
              'software_defined_assembly': 'software_defined_assembly',
              'trisymmetron capsid unit': 'software_defined_assembly',
              'deposited_coordinates': 'software_defined_assembly'}
        #
        try:
            if not dataContainer.exists('pdbx_struct_assembly'):
                return False

            logger.debug("Filter assembly details for %s" % dataContainer.getName())
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            if not tObj.hasAttribute(atName):
                tObj.appendAttribute(atName)
            #
            for iRow in range(tObj.getRowCount()):
                details = tObj.getValue('details', iRow)
                if details in mD:
                    tObj.setValue(mD[details], 'rcsb_details', iRow)
                else:
                    tObj.setValue('software_defined_assembly', 'rcsb_details', iRow)
                logger.debug("Full row is %r" % tObj.getRow(iRow))
            return True
        except Exception as e:
            logger.exception("For %s %s failing with %s" % (catName, atName, str(e)))
        return False

    def assignAssemblyCandidates(self, dataContainer, catName, atName, **kwargs):
        """ Flag candidate biological assemblies as 'author_defined_assembly' ad author_and_software_defined_assembly'

        """
        mD = {'author_and_software_defined_assembly': 'author_and_software_defined_assembly',
              'author_defined_assembly': 'author_defined_assembly',
              'complete icosahedral assembly': 'author_and_software_defined_assembly',
              'complete point assembly': 'author_and_software_defined_assembly',
              'crystal asymmetric unit': 'software_defined_assembly',
              'crystal asymmetric unit, crystal frame': 'software_defined_assembly',
              'details': 'software_defined_assembly',
              'helical asymmetric unit': 'software_defined_assembly',
              'helical asymmetric unit, std helical frame': 'software_defined_assembly',
              'icosahedral 23 hexamer': 'software_defined_assembly',
              'icosahedral asymmetric unit': 'software_defined_assembly',
              'icosahedral asymmetric unit, std point frame': 'software_defined_assembly',
              'icosahedral pentamer': 'software_defined_assembly',
              'pentasymmetron capsid unit': 'software_defined_assembly',
              'point asymmetric unit': 'software_defined_assembly',
              'point asymmetric unit, std point frame': 'software_defined_assembly',
              'representative helical assembly': 'author_and_software_defined_assembly',
              'software_defined_assembly': 'software_defined_assembly',
              'trisymmetron capsid unit': 'software_defined_assembly',
              'deposited_coordinates': 'software_defined_assembly'}
        #
        eD = {k: True for k in ['crystal asymmetric unit', 'crystal asymmetric unit, crystal frame', 'helical asymmetric unit',
                                'helical asymmetric unit, std helical frame', 'icosahedral 23 hexamer', 'icosahedral asymmetric unit',
                                'icosahedral asymmetric unit, std point frame', 'icosahedral pentamer', 'pentasymmetron capsid unit',
                                'point asymmetric unit', 'point asymmetric unit, std point frame', 'trisymmetron capsid unit',
                                'deposited_coordinates', 'details']}
        try:
            if not dataContainer.exists('pdbx_struct_assembly'):
                return False

            tObj = dataContainer.getObj('pdbx_struct_assembly')
            if not tObj.hasAttribute(atName):
                tObj.appendAttribute(atName)
            #
            for iRow in range(tObj.getRowCount()):
                details = tObj.getValue('details', iRow)
                if details in mD and details not in eD:
                    tObj.setValue('Y', 'rcsb_candidate_assembly', iRow)
                else:
                    tObj.setValue('N', 'rcsb_candidate_assembly', iRow)
                logger.debug("Full row is %r" % tObj.getRow(iRow))

            #
            numAssemblies = tObj.getRowCount()
            logger.debug("Assembly count is %d" % numAssemblies)
            if dataContainer.exists('rcsb_entry_info'):
                eiObj = dataContainer.getObj('rcsb_entry_info')
                eiObj.setValue(numAssemblies, 'assembly_count', 0)
            #
            #
            return True
        except Exception as e:
            logger.exception("For %s %s failing with %s" % (catName, atName, str(e)))
        return False

    def __getAttribList(self, sObj, atTupL):
        atL = []
        atSL = []
        if sObj:
            for (atS, at) in atTupL:
                if sObj.hasAttribute(atS):
                    atL.append(at)
                    atSL.append(atS)
        return atSL, atL

    def __normalizeCsvToList(self, entryId, colL, separator=','):
        """ Normalize a row containing some character delimited fields.

            Expand list of uneven lists into unifornm list of lists.
            Only two list lengths are logically supported: 1 and second
            maximum length.

            returns: list of expanded rows or the original input.

        """
        tcL = []
        countL = []
        for col in colL:
            cL = [t.strip() for t in col.split(separator)]
            tcL.append(cL)
            countL.append(len(cL))
        #
        tL = list(set(countL))
        if len(tL) == 1 and tL[0] == 1:
            return [colL]
        # Report pathological cases ...
        if (len(tL) > 2) or (tL[0] != 1 and len(tL) == 2):
            logger.error("%s integrated source data inconsistent %r colL" % (entryId, colL))
            return [colL]
        #
        # Expand the columns with uniform length
        #
        icL = []
        maxL = tL[1]
        for tc in tcL:
            if len(tc) == 1:
                tc = tc * maxL
            icL.append(tc)
        #
        logger.debug("%s icL %r" % (entryId, icL))
        # Convert back to a row list
        #
        iRow = 0
        rL = []
        for iRow in range(maxL):
            row = []
            for ic in icL:
                row.append(ic[iRow])
            rL.append(row)

        return rL

    def filterSourceOrganismDetails(self, dataContainer, catName, **kwargs):
        """  Select relevant source and host organism details from primary data categories.

        Build:
            loop_
            _rcsb_entity_source_organism.entity_id
            _rcsb_entity_source_organism.pdbx_src_id
            _rcsb_entity_source_organism.source_type
            _rcsb_entity_source_organism.scientific_name
            _rcsb_entity_source_organism.common_name
            _rcsb_entity_source_organism.ncbi_taxonomy_id
            _rcsb_entity_source_organism.provenance_code
            _rcsb_entity_source_organism.beg_seq_num
            _rcsb_entity_source_organism.end_seq_num
            _rcsb_entity_source_organism.taxonomy_lineage_id
            _rcsb_entity_source_organism.taxonomy_lineage_name
            _rcsb_entity_source_organism.taxonomy_lineage_depth
            1 1 natural 'Homo sapiens' human 9606  'PDB Primary Data' 1 202 . . .
            # ... abbreviated


            loop_
            _rcsb_entity_host_organism.entity_id
            _rcsb_entity_host_organism.pdbx_src_id
            _rcsb_entity_host_organism.scientific_name
            _rcsb_entity_host_organism.common_name
            _rcsb_entity_host_organism.ncbi_taxonomy_id
            _rcsb_entity_host_organism.provenance_code
            _rcsb_entity_host_organism.beg_seq_num
            _rcsb_entity_host_organism.end_seq_num
            _rcsb_entity_host_organism.taxonomy_lineage_id
            _rcsb_entity_host_organism.taxonomy_lineage_name
            _rcsb_entity_host_organism.taxonomy_lineage_depth
                        1 1 'Escherichia coli' 'E. coli' 562  'PDB Primary Data' 1 102 .  . .
            # ... abbreviated

            And two related items -

            _entity.rcsb_multiple_source_flag
            _entity.rcsb_source_part_count

        """
        #
        hostCatName = 'rcsb_entity_host_organism'
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            if catName == hostCatName:
                logger.debug("Skipping method for %r %r" % (dataContainer.getName(), catName))
                return True
            #
            # if there is no source information then exit
            if not (dataContainer.exists('entity_src_gen') or dataContainer.exists('entity_src_nat') or dataContainer.exists('pdbx_entity_src_syn')):
                return False
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entity_id',
                                                                              'pdbx_src_id',
                                                                              'source_type',
                                                                              'scientific_name',
                                                                              'common_name',
                                                                              'ncbi_taxonomy_id',
                                                                              'beg_seq_num',
                                                                              'end_seq_num',
                                                                              'provenance_code',
                                                                              'ncbi_scientific_name',
                                                                              'ncbi_parent_scientific_name',
                                                                              'ncbi_common_names',
                                                                              'taxonomy_lineage_id',
                                                                              'taxonomy_lineage_name',
                                                                              'taxonomy_lineage_depth']))
            #
            if not dataContainer.exists(hostCatName):
                dataContainer.append(DataCategory(hostCatName, attributeNameList=['entity_id',
                                                                                  'pdbx_src_id',
                                                                                  'scientific_name',
                                                                                  'common_name',
                                                                                  'ncbi_taxonomy_id',
                                                                                  'beg_seq_num',
                                                                                  'end_seq_num',
                                                                                  'provenance_code',
                                                                                  'ncbi_scientific_name',
                                                                                  'ncbi_parent_scientific_name',
                                                                                  'ncbi_common_names',
                                                                                  'taxonomy_lineage_id',
                                                                                  'taxonomy_lineage_name',
                                                                                  'taxonomy_lineage_depth']))

            #
            if not self.__taxU:
                self.__taxU = TaxonomyUtils(taxDirPath=self.__taxonomyDataPath)
            cObj = dataContainer.getObj(catName)
            hObj = dataContainer.getObj(hostCatName)
            #
            s1Obj = dataContainer.getObj('entity_src_gen')
            atHTupL = [('entity_id', 'entity_id'),
                       ('pdbx_host_org_scientific_name', 'scientific_name'),
                       ('pdbx_host_org_common_name', 'common_name'),
                       ('pdbx_host_org_ncbi_taxonomy_id', 'ncbi_taxonomy_id'),
                       ('pdbx_src_id', 'pdbx_src_id'),
                       ('pdbx_beg_seq_num', 'beg_seq_num'),
                       ('pdbx_end_seq_num', 'end_seq_num')]
            atHSL, atHL = self.__getAttribList(s1Obj, atHTupL)
            #
            at1TupL = [('entity_id', 'entity_id'),
                       ('pdbx_gene_src_scientific_name', 'scientific_name'),
                       ('gene_src_common_name', 'common_name'),
                       ('pdbx_gene_src_ncbi_taxonomy_id', 'ncbi_taxonomy_id'),
                       ('pdbx_src_id', 'pdbx_src_id'),
                       ('pdbx_beg_seq_num', 'beg_seq_num'),
                       ('pdbx_end_seq_num', 'end_seq_num')]
            at1SL, at1L = self.__getAttribList(s1Obj, at1TupL)
            #
            s2Obj = dataContainer.getObj('entity_src_nat')
            at2TupL = [('entity_id', 'entity_id'),
                       ('pdbx_organism_scientific', 'scientific_name'),
                       ('nat_common_name', 'common_name'),
                       ('pdbx_ncbi_taxonomy_id', 'ncbi_taxonomy_id'),
                       ('pdbx_src_id', 'pdbx_src_id'),
                       ('pdbx_beg_seq_num', 'beg_seq_num'),
                       ('pdbx_end_seq_num', 'end_seq_num')
                       ]
            at2SL, at2L = self.__getAttribList(s2Obj, at2TupL)
            #
            s3Obj = dataContainer.getObj('pdbx_entity_src_syn')
            at3TupL = [('entity_id', 'entity_id'),
                       ('organism_scientific', 'scientific_name'),
                       ('organism_common_name', 'common_name'),
                       ('ncbi_taxonomy_id', 'ncbi_taxonomy_id'),
                       ('pdbx_src_id', 'pdbx_src_id'),
                       ('beg_seq_num', 'beg_seq_num'),
                       ('end_seq_num', 'end_seq_num')]
            at3SL, at3L = self.__getAttribList(s3Obj, at3TupL)
            #
            eObj = dataContainer.getObj('entity')
            entityIdL = eObj.getAttributeValueList('id')
            pCode = 'PDB Primary Data'
            #
            partCountD = {}
            srcL = []
            hostL = []
            for entityId in entityIdL:
                partCountD[entityId] = 1
                eL = []
                tf = False
                if s1Obj:
                    sType = 'genetically engineered'
                    vL = s1Obj.selectValueListWhere(at1SL, entityId, 'entity_id')
                    if vL:
                        for v in vL:
                            eL.append((entityId, sType, at1L, v))
                        logger.debug("%r entity %r - %r" % (sType, entityId, vL))
                        partCountD[entityId] = len(eL)
                        srcL.extend(eL)
                        tf = True
                    #
                    vL = s1Obj.selectValueListWhere(atHSL, entityId, 'entity_id')
                    if vL:
                        for v in vL:
                            hostL.append((entityId, sType, atHL, v))
                        logger.debug("%r entity %r - %r" % (sType, entityId, vL))
                    if tf:
                        continue

                if s2Obj:
                    sType = 'natural'
                    vL = s2Obj.selectValueListWhere(at2SL, entityId, 'entity_id')
                    if vL:
                        for v in vL:
                            eL.append((entityId, sType, at2L, v))
                        logger.debug("%r entity %r - %r" % (sType, entityId, vL))
                        partCountD[entityId] = len(eL)
                        srcL.extend(eL)
                        continue

                if s3Obj:
                    sType = 'synthetic'
                    vL = s3Obj.selectValueListWhere(at3SL, entityId, 'entity_id')
                    if vL:
                        for v in vL:
                            eL.append((entityId, sType, at3L, v))
                        logger.debug("%r entity %r - %r" % (sType, entityId, vL))
                        partCountD[entityId] = len(eL)
                        srcL.extend(eL)
                        continue

            iRow = 0
            entryTaxIdD = {}
            for (entityId, sType, atL, tv) in srcL:
                ii = atL.index('ncbi_taxonomy_id') if 'ncbi_taxonomy_id' in atL else -1
                if ii > 0 and len(tv[ii].split(',')) > 1:
                    tvL = self.__normalizeCsvToList(dataContainer.getName(), tv)
                    ii = atL.index('pdbx_src_id') if 'pdbx_src_id' in atL else -1
                    for jj, row in enumerate(tvL, 1):
                        row[ii] = str(jj)
                    partCountD[entityId] = len(tvL)
                else:
                    tvL = [tv]
                for v in tvL:
                    cObj.setValue(sType, 'source_type', iRow)
                    cObj.setValue(pCode, 'provenance_code', iRow)
                    for ii, at in enumerate(atL):
                        cObj.setValue(v[ii], at, iRow)
                        # if at == 'ncbi_taxonomy_id' and v[ii] and v[ii] not in ['.', '?'] and v[ii].isdigit():
                        if at == 'ncbi_taxonomy_id' and v[ii] and v[ii] not in ['.', '?']:
                            taxId = int(self.__re_non_digit.sub('', v[ii]))
                            taxId = self.__taxU.getMergedTaxId(taxId)
                            cObj.setValue(str(taxId), 'ncbi_taxonomy_id', iRow)
                            entryTaxIdD[taxId] = entryTaxIdD[taxId] + 1 if taxId in entryTaxIdD else 1
                            #
                            sn = self.__taxU.getScientificName(taxId)
                            if sn:
                                cObj.setValue(sn, 'ncbi_scientific_name', iRow)
                            #
                            psn = self.__taxU.getParentScientificName(taxId)
                            if psn:
                                cObj.setValue(psn, 'ncbi_parent_scientific_name', iRow)
                            #
                            cnL = self.__taxU.getCommonNames(taxId)
                            if cnL:
                                cObj.setValue(';'.join(list(set(cnL))), 'ncbi_common_names', iRow)
                            # Add lineage -
                            linL = self.__taxU.getLineageWithNames(taxId)
                            if linL is not None:
                                cObj.setValue(';'.join([str(tup[0]) for tup in linL]), 'taxonomy_lineage_depth', iRow)
                                cObj.setValue(';'.join([str(tup[1]) for tup in linL]), 'taxonomy_lineage_id', iRow)
                                cObj.setValue(';'.join([str(tup[2]) for tup in linL]), 'taxonomy_lineage_name', iRow)
                            else:
                                logger.warning("%s taxId %r lineage %r" % (dataContainer.getName(), taxId, linL))

                    logger.debug("%r entity %r - UPDATED %r %r" % (sType, entityId, atL, v))
                    iRow += 1
            #
            iRow = 0
            for (entityId, sType, atL, tv) in hostL:
                ii = atL.index('ncbi_taxonomy_id') if 'ncbi_taxonomy_id' in atL else -1
                if ii > 0 and len(tv[ii].split(',')) > 1:
                    tvL = self.__normalizeCsvToList(dataContainer.getName(), tv)
                    ii = atL.index('pdbx_src_id') if 'pdbx_src_id' in atL else -1
                    for jj, row in enumerate(tvL, 1):
                        row[ii] = str(jj)
                    partCountD[entityId] = len(tvL)
                else:
                    tvL = [tv]
                for v in tvL:
                    hObj.setValue(pCode, 'provenance_code', iRow)
                    for ii, at in enumerate(atL):
                        hObj.setValue(v[ii], at, iRow)
                        #  if at == 'ncbi_taxonomy_id' and v[ii] and v[ii] not in ['.', '?'] and v[ii].isdigit():
                        if at == 'ncbi_taxonomy_id' and v[ii] and v[ii] not in ['.', '?']:
                            taxId = int(self.__re_non_digit.sub('', v[ii]))
                            taxId = self.__taxU.getMergedTaxId(taxId)
                            hObj.setValue(str(taxId), 'ncbi_taxonomy_id', iRow)
                            sn = self.__taxU.getScientificName(taxId)
                            if sn:
                                hObj.setValue(sn, 'ncbi_scientific_name', iRow)
                            #
                            psn = self.__taxU.getParentScientificName(taxId)
                            if psn:
                                hObj.setValue(psn, 'ncbi_parent_scientific_name', iRow)
                            #
                            cnL = self.__taxU.getCommonNames(taxId)
                            if cnL:
                                hObj.setValue(';'.join(list(set(cnL))), 'ncbi_common_names', iRow)
                            # Add lineage -
                            linL = self.__taxU.getLineageWithNames(taxId)
                            if linL is not None:
                                hObj.setValue(';'.join([str(tup[0]) for tup in linL]), 'taxonomy_lineage_depth', iRow)
                                hObj.setValue(';'.join([str(tup[1]) for tup in linL]), 'taxonomy_lineage_id', iRow)
                                hObj.setValue(';'.join([str(tup[2]) for tup in linL]), 'taxonomy_lineage_name', iRow)
                            else:
                                logger.warning("%s taxId %r lineage %r" % (dataContainer.getName(), taxId, linL))
                    logger.debug("%r entity %r - UPDATED %r %r" % (sType, entityId, atL, v))
                    iRow += 1
            if 0:
                iRow = 0
                for (entityId, sType, atL, v) in hostL:
                    hObj.setValue(pCode, 'provenance_code', iRow)
                    for ii, at in enumerate(atL):
                        hObj.setValue(v[ii], at, iRow)
                        if at == 'ncbi_taxonomy_id' and v[ii] and v[ii] not in ['.', '?'] and v[ii].isdigit():
                            taxId = int(v[ii])
                            sn = self.__taxU.getScientificName(taxId)
                            if sn:
                                hObj.setValue(sn, 'ncbi_scientific_name', iRow)
                            cnL = self.__taxU.getCommonNames(taxId)
                            if cnL:
                                hObj.setValue(';'.join(list(set(cnL))), 'ncbi_common_names', iRow)
                    logger.debug("%r entity %r - UPDATED %r %r" % (sType, entityId, atL, v))
                    iRow += 1
            # -------------------------------------------------------------------------
            # Update entity attributes
            #    _entity.rcsb_multiple_source_flag
            #    _entity.rcsb_source_part_count
            for atName in ['rcsb_source_part_count', 'rcsb_multiple_source_flag']:
                if not eObj.hasAttribute(atName):
                    eObj.appendAttribute(atName)
            #
            for ii in range(eObj.getRowCount()):
                entityId = eObj.getValue('id', ii)
                cFlag = 'Y' if partCountD[entityId] > 1 else 'N'
                eObj.setValue(partCountD[entityId], 'rcsb_source_part_count', ii)
                eObj.setValue(cFlag, 'rcsb_multiple_source_flag', ii)

            logger.debug("Entry taxonomy count is %d" % len(entryTaxIdD))
            if dataContainer.exists('rcsb_entry_info'):
                eiObj = dataContainer.getObj('rcsb_entry_info')
                eiObj.setValue(len(entryTaxIdD), 'polymer_entity_taxonomy_count', 0)
            #
            return True
        except Exception as e:
            logger.exception("In %s for %s failing with %s" % (dataContainer.getName(), catName, str(e)))
        return False

    def consolidateAccessionDetails(self, dataContainer, catName, **kwargs):
        """  Consolidate accession details into a single object.

             _rcsb_accession_info.entry_id                1ABC
             _rcsb_accession_info.status_code             REL
             _rcsb_accession_info.deposit_date            2018-01-11
             _rcsb_accession_info.initial_release_date    2018-03-23
             _rcsb_accession_info.major_revision          1
             _rcsb_accession_info.minor_revision          2
             _rcsb_accession_info.revision_date           2018-10-25


            #

            _pdbx_database_status.entry_id                        3OQP
            _pdbx_database_status.deposit_site                    RCSB
            _pdbx_database_status.process_site                    RCSB
            _pdbx_database_status.recvd_initial_deposition_date   2010-09-03
            _pdbx_database_status.status_code                     REL
            _pdbx_database_status.status_code_sf                  REL
            _pdbx_database_status.status_code_mr                  ?
            _pdbx_database_status.status_code_cs                  ?
            _pdbx_database_status.pdb_format_compatible           Y
            _pdbx_database_status.methods_development_category    ?
            _pdbx_database_status.SG_entry                        Y
            #
            loop_
            _pdbx_audit_revision_history.ordinal
            _pdbx_audit_revision_history.data_content_type
            _pdbx_audit_revision_history.major_revision
            _pdbx_audit_revision_history.minor_revision
            _pdbx_audit_revision_history.revision_date
            1 'Structure model' 1 0 2010-10-13
            2 'Structure model' 1 1 2011-07-13
            3 'Structure model' 1 2 2011-07-20
            4 'Structure model' 1 3 2014-11-12
            5 'Structure model' 1 4 2017-10-25
            #
        """
        ##
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            #
            # if there is incomplete accessioninformation then exit
            if not (dataContainer.exists('pdbx_database_status') or dataContainer.exists('pdbx_audit_revision_history')):
                return False
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id',
                                                                              'status_code',
                                                                              'deposit_date',
                                                                              'initial_release_date',
                                                                              'major_revision',
                                                                              'minor_revision',
                                                                              'revision_date']))
            #
            cObj = dataContainer.getObj(catName)
            #
            tObj = dataContainer.getObj('pdbx_database_status')
            entryId = tObj.getValue('entry_id', 0)
            statusCode = tObj.getValue('status_code', 0)
            depositDate = tObj.getValue('recvd_initial_deposition_date', 0)
            #
            cObj.setValue(entryId, 'entry_id', 0)
            cObj.setValue(statusCode, 'status_code', 0)
            cObj.setValue(depositDate, 'deposit_date', 0)
            #
            tObj = dataContainer.getObj('pdbx_audit_revision_history')
            nRows = tObj.getRowCount()
            # Assuming the default sorting order from the release module -
            releaseDate = tObj.getValue('revision_date', 0)
            minorRevision = tObj.getValue('minor_revision', nRows - 1)
            majorRevision = tObj.getValue('major_revision', nRows - 1)
            revisionDate = tObj.getValue('revision_date', nRows - 1)
            cObj.setValue(releaseDate, 'initial_release_date', 0)
            cObj.setValue(minorRevision, 'minor_revision', 0)
            cObj.setValue(majorRevision, 'major_revision', 0)
            cObj.setValue(revisionDate, 'revision_date', 0)
            #
            return True
        except Exception as e:
            logger.exception("In %s for %s failing with %s" % (dataContainer.getName(), catName, str(e)))
        return False

    def __fetchDrugBankMapping(self, filePath, workPath='.'):
        """

        """
        if self.__drugBankMappingDict:
            return self.__drugBankMappingDict
        rD = {}
        try:
            if not filePath:
                return rD
            mU = MarshalUtil(workPath=workPath)
            rD = mU.doImport(filePath, format="json")
            logger.debug("Fetching DrugBank mapping length %d" % len(rD))
            self.__drugBankMappingDict = rD
            return rD
        except Exception as e:
            logger.exception("For %s failing with %s" % (filePath, str(e)))
        return rD

    def __fetchCsdModelMapping(self, filePath, workPath='.'):
        """

        """
        if self.__csdModelMappingDict:
            return self.__csdModelMappingDict
        rD = {}
        try:
            if not filePath:
                return rD
            mU = MarshalUtil(workPath=workPath)
            rD = mU.doImport(filePath, format="json")
            logger.debug("Fetching CSD model length %d" % len(rD))
            self.__csdModelMappingDict = rD
            return rD
        except Exception as e:
            logger.exception("For %s failing with %s" % (filePath, str(e)))
        return rD

    def addChemCompRelated(self, dataContainer, catName, **kwargs):
        """

        Example:

             loop_
             _rcsb_chem_comp_related.comp_id
             _rcsb_chem_comp_related.ordinal
             _rcsb_chem_comp_related.resource_name
             _rcsb_chem_comp_related.resource_accession_code
             _rcsb_chem_comp_related.related_mapping_method
             ATP 1 DrugBank DB00171 'assigned by resource'
        """
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            # Exit if source categories are missing
            if not (dataContainer.exists('chem_comp_atom') and dataContainer.exists('chem_comp_bond')):
                return False

            #
            dbD = self.__fetchDrugBankMapping(self.__drugBankMappingFilePath, workPath=self.__workPath)
            #
            ccId = dataContainer.getName()
            #
            dbMapD = dbD['id_map']
            inKeyD = dbD['inchikey_map']
            logger.debug("inKeyD length is %d" % len(inKeyD))
            dbId = None
            mType = None
            #
            if dataContainer.exists('rcsb_chem_comp_descriptor'):
                ccIObj = dataContainer.getObj('rcsb_chem_comp_descriptor')

                if ccIObj.hasAttribute('InChIKey'):
                    inky = ccIObj.getValue('InChIKey', 0)
                    logger.debug("inKeyD length is %d testing %r" % (len(inKeyD), inky))
                    if inky in inKeyD:
                        logger.debug("Matching inchikey for %s" % ccId)
                        dbId = inKeyD[inky][0]['drugbank_id']
                        mType = 'matching InChIKey'
            #

            if not dbId and dbMapD and dataContainer.getName() in dbMapD:
                dbId = dbMapD[ccId]["drugbank_id"]
                mType = 'assigned by resource'
                logger.debug("Matching db assignment for %s" % ccId)

            if dbId:
                #
                if dataContainer.exists('rcsb_chem_comp_container_identifiers'):
                    tObj = dataContainer.getObj('rcsb_chem_comp_container_identifiers')
                    if not tObj.hasAttribute('drugbank_id'):
                        tObj.appendAttribute('drugbank_id')
                    tObj.setValue(dbId, 'drugbank_id', 0)

                #
                if not dataContainer.exists(catName):
                    dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                                  'ordinal',
                                                                                  'resource_name',
                                                                                  'resource_accession_code',
                                                                                  'related_mapping_method']))
                wObj = dataContainer.getObj(catName)
                logger.debug("Using DrugBank mapping length %d" % len(dbMapD))
                rL = wObj.selectIndices('DrugBank', 'resource_name')
                if rL:
                    ok = wObj.removeRows(rL)
                    if not ok:
                        logger.debug("Error removing rows in %r %r" % (catName, rL))
                iRow = wObj.getRowCount()
                wObj.setValue(ccId, 'comp_id', iRow)
                wObj.setValue(iRow + 1, 'ordinal', iRow)
                wObj.setValue('DrugBank', 'resource_name', iRow)
                wObj.setValue(dbId, 'resource_accession_code', iRow)
                wObj.setValue(mType, 'related_mapping_method', iRow)
            #
            #
            csdMapD = self.__fetchCsdModelMapping(self.__csdModelMappingFilePath, workPath=self.__workPath)
            self.__csdModelMappingDict = csdMapD
            #
            if csdMapD and dataContainer.getName() in csdMapD:
                if not dataContainer.exists(catName):
                    dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                                  'ordinal',
                                                                                  'resource_name',
                                                                                  'resource_accession_code',
                                                                                  'related_mapping_method']))
                wObj = dataContainer.getObj(catName)
                self.__csdModelMappingDict = csdMapD
                logger.debug("Using CSD model mapping length %d" % len(csdMapD))
                ccId = dataContainer.getName()
                dbId = csdMapD[ccId][0]["db_code"]
                rL = wObj.selectIndices('CCDC/CSD', 'resource_name')
                if rL:
                    ok = wObj.removeRows(rL)
                    if not ok:
                        logger.debug("Error removing rows in %r %r" % (catName, rL))
                iRow = wObj.getRowCount()
                wObj.setValue(ccId, 'comp_id', iRow)
                wObj.setValue(iRow + 1, 'ordinal', iRow)
                wObj.setValue('CCDC/CSD', 'resource_name', iRow)
                wObj.setValue(dbId, 'resource_accession_code', iRow)
                wObj.setValue('assigned by PDB', 'related_mapping_method', iRow)
            #

            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def addChemCompTargets(self, dataContainer, catName, **kwargs):
        """

        Example:
             loop_
             _rcsb_chem_comp_target.comp_id
             _rcsb_chem_comp_target.ordinal
             _rcsb_chem_comp_target.name
             _rcsb_chem_comp_target.interaction_type
             _rcsb_chem_comp_target.target_actions
             _rcsb_chem_comp_target.organism_common_name
             _rcsb_chem_comp_target.reference_database_name
             _rcsb_chem_comp_target.reference_database_accession_code
             _rcsb_chem_comp_target.provenance_code
             ATP 1 "O-phosphoseryl-tRNA(Sec) selenium transferase" target cofactor Human UniProt Q9HD40 DrugBank

        DrugBank target info:
        {
            "type": "target",
            "name": "Alanine--glyoxylate aminotransferase 2, mitochondrial",
            "organism": "Human",
            "actions": [
               "cofactor"
            ],
            "known_action": "unknown",
            "uniprot_ids": "Q9BYV1"
         },

        """
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            # Exit if source categories are missing
            if not (dataContainer.exists('chem_comp_atom') and dataContainer.exists('chem_comp_bond')):
                return False

            #
            dbD = self.__fetchDrugBankMapping(self.__drugBankMappingFilePath, workPath=self.__workPath)
            dbMapD = dbD['id_map']
            #
            ccId = dataContainer.getName()
            if dbMapD and ccId in dbMapD and 'target_interactions' in dbMapD[ccId]:
                #
                # Create the new target category
                if not dataContainer.exists(catName):
                    dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                                  'ordinal',
                                                                                  'name',
                                                                                  'interaction_type',
                                                                                  'target_actions',
                                                                                  'organism_common_name',
                                                                                  'reference_database_name',
                                                                                  'reference_database_accession_code',
                                                                                  'provenance_code']))
                wObj = dataContainer.getObj(catName)
                logger.debug("Using DrugBank mapping length %d" % len(dbMapD))
                rL = wObj.selectIndices('DrugBank', 'provenance_code')
                if rL:
                    ok = wObj.removeRows(rL)
                    if not ok:
                        logger.debug("Error removing rows in %r %r" % (catName, rL))
                #
                iRow = wObj.getRowCount()
                iRow = wObj.getRowCount()
                for tD in dbMapD[ccId]['target_interactions']:
                    wObj.setValue(ccId, 'comp_id', iRow)
                    wObj.setValue(iRow + 1, 'ordinal', iRow)
                    wObj.setValue(tD['name'], 'name', iRow)
                    wObj.setValue(tD['type'], 'interaction_type', iRow)
                    if 'actions' in tD and len(tD['actions']) > 0:
                        wObj.setValue(';'.join(tD['actions']), 'target_actions', iRow)
                    if 'organism' in tD:
                        wObj.setValue(tD['organism'], 'organism_common_name', iRow)
                    if 'uniprot_ids' in tD:
                        wObj.setValue('UniProt', 'reference_database_name', iRow)
                        wObj.setValue(tD['uniprot_ids'], 'reference_database_accession_code', iRow)
                    wObj.setValue('DrugBank', 'provenance_code', iRow)
                    iRow += 1

            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def addChemCompInfo(self, dataContainer, catName, **kwargs):
        """
        Example:
             _rcsb_chem_comp_info.comp_id                 BNZ
             _rcsb_chem_comp_info.atom_count              12
             _rcsb_chem_comp_info.atom_count_chiral        0
             _rcsb_chem_comp_info.bond_count              12
             _rcsb_chem_comp_info.bond_count_aromatic      6
             _rcsb_chem_comp_info.atom_count_heavy         6
        """
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            # Exit if source categories are missing
            if not dataContainer.exists('chem_comp'):
                return False
            ccObj = dataContainer.getObj('chem_comp')
            if not ccObj.hasAttribute('pdbx_release_status'):
                return False
            ccId = ccObj.getValue('id', 0)
            #
            # Create the new target category
            #
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                              'atom_count',
                                                                              'atom_count_heavy',
                                                                              'atom_count_chiral',
                                                                              'bond_count',
                                                                              'bond_count_aromatic'
                                                                              ]))
            # -------
            cN = 'rcsb_chem_comp_container_identifiers'
            if not dataContainer.exists(cN):
                dataContainer.append(DataCategory(cN, attributeNameList=['comp_id']))
            idObj = dataContainer.getObj(cN)
            idObj.setValue(ccId, 'comp_id', 0)
            #
            # -------
            wObj = dataContainer.getObj(catName)
            #
            numAtoms = 0
            numAtomsHeavy = 0
            numAtomsChiral = 0
            try:
                cObj = dataContainer.getObj('chem_comp_atom')
                numAtoms = cObj.getRowCount()
                numAtomsHeavy = 0
                numAtomsChiral = 0
                for ii in range(numAtoms):
                    el = cObj.getValue('type_symbol', ii)
                    if el != 'H':
                        numAtomsHeavy += 1
                    chFlag = cObj.getValue('pdbx_stereo_config', ii)
                    if chFlag != 'N':
                        numAtomsChiral += 1
            except Exception:
                logger.warning("Missing chem_comp_atom category for %s" % ccId)
                numAtoms = 0
                numAtomsHeavy = 0
                numAtomsChiral = 0
            #
            wObj.setValue(ccId, 'comp_id', 0)
            wObj.setValue(numAtoms, 'atom_count', 0)
            wObj.setValue(numAtomsChiral, 'atom_count_chiral', 0)
            wObj.setValue(numAtomsHeavy, 'atom_count_heavy', 0)
            #
            #  ------
            numBonds = 0
            numBondsAro = 0
            try:
                cObj = dataContainer.getObj('chem_comp_bond')
                numBonds = cObj.getRowCount()
                numBondsAro = 0
                for ii in range(numAtoms):
                    aroFlag = cObj.getValue('pdbx_aromatic_flag', ii)
                    if aroFlag != 'N':
                        numBondsAro += 1
            except Exception:
                pass
            #
            wObj.setValue(numBonds, 'bond_count', 0)
            wObj.setValue(numBondsAro, 'bond_count_aromatic', 0)
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def addChemCompDescriptor(self, dataContainer, catName, **kwargs):
        """
        Parse the pdbx_chem_comp_descriptor category and extract SMILES/CACTVS and InChI descriptors -

        loop_
        _pdbx_chem_comp_descriptor.comp_id
        _pdbx_chem_comp_descriptor.type
        _pdbx_chem_comp_descriptor.program
        _pdbx_chem_comp_descriptor.program_version
        _pdbx_chem_comp_descriptor.descriptor
        ATP SMILES           ACDLabs              10.04 "O=P(O)(O)OP(=O)(O)OP(=O)(O)OCC3OC(n2cnc1c(ncnc12)N)C(O)C3O"
        ATP SMILES_CANONICAL CACTVS               3.341 "Nc1ncnc2n(cnc12)[C@@H]3O[C@H](CO[P@](O)(=O)O[P@@](O)(=O)O[P](O)(O)=O)[C@@H](O)[C@H]3O"
        ATP SMILES           CACTVS               3.341 "Nc1ncnc2n(cnc12)[CH]3O[CH](CO[P](O)(=O)O[P](O)(=O)O[P](O)(O)=O)[CH](O)[CH]3O"
        ATP SMILES_CANONICAL "OpenEye OEToolkits" 1.5.0 "c1nc(c2c(n1)n(cn2)[C@H]3[C@@H]([C@@H]([C@H](O3)CO[P@@](=O)(O)O[P@](=O)(O)OP(=O)(O)O)O)O)N"
        ATP SMILES           "OpenEye OEToolkits" 1.5.0 "c1nc(c2c(n1)n(cn2)C3C(C(C(O3)COP(=O)(O)OP(=O)(O)OP(=O)(O)O)O)O)N"
        ATP InChI            InChI                1.03  "InChI=1S/C10H16N5O13P3/c11-8-5-9(13-2-12-8)15(3- ...."
        ATP InChIKey         InChI                1.03  ZKHQWZAMYRWXGA-KQYNXXCUSA-N

        To produce -
             _rcsb_chem_comp_descriptor.comp_id                 ATP
             _rcsb_chem_comp_descriptor.SMILES                  'Nc1ncnc2n(cnc12)[CH]3O[CH](CO[P](O)(=O)O[P](O)(=O)O[P](O)(O)=O)[CH](O)[CH]3O'
             _rcsb_chem_comp_descriptor.SMILES_stereo           'Nc1ncnc2n(cnc12)[C@@H]3O[C@H](CO[P@](O)(=O)O[P@@](O)(=O)O[P](O)(O)=O)[C@@H](O)[C@H]3O'
             _rcsb_chem_comp_descriptor.InChI                   'InChI=1S/C10H16N5O13P3/c11-8-5-9(13-2-12-8)15(3-14-5)10-7(17)6(16)4(26-10)1-25 ...'
             _rcsb_chem_comp_descriptor.InChIKey                'ZKHQWZAMYRWXGA-KQYNXXCUSA-N'
        """
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            # Exit if source categories are missing
            if not (dataContainer.exists('chem_comp') and dataContainer.exists('pdbx_chem_comp_descriptor')):
                return False
            #
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                              'SMILES',
                                                                              'SMILES_stereo',
                                                                              'InChI',
                                                                              'InChIKey']))
            #
            wObj = dataContainer.getObj(catName)
            ccIObj = dataContainer.getObj('pdbx_chem_comp_descriptor')
            iRow = 0
            ccId = ''
            for ii in range(ccIObj.getRowCount()):
                ccId = ccIObj.getValue('comp_id', ii)
                nm = ccIObj.getValue('descriptor', ii)
                prog = ccIObj.getValue('program', ii)
                typ = ccIObj.getValue('type', ii)
                #
                if typ == 'SMILES_CANONICAL' and prog == "CACTVS":
                    wObj.setValue(nm, 'SMILES_stereo', iRow)
                elif typ == 'SMILES' and prog == "CACTVS":
                    wObj.setValue(nm, 'SMILES', iRow)
                elif typ == 'InChI' and prog == "InChI":
                    wObj.setValue(nm, 'InChI', iRow)
                elif typ == 'InChIKey' and prog == "InChI":
                    wObj.setValue(nm, 'InChIKey', iRow)
            #
            wObj.setValue(ccId, 'comp_id', iRow)
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def addChemCompSynonyms(self, dataContainer, catName, **kwargs):
        """
             loop_
                 _rcsb_chem_comp_synonyms.comp_id
                 _rcsb_chem_comp_synonyms.ordinal
                 _rcsb_chem_comp_synonyms.name
                 _rcsb_chem_comp_synonyms.provenance_code
                    ATP 1 "adenosine 5'-(tetrahydrogen triphosphate)"  'PDB Reference Data'
                    ATP 2 "Adenosine 5'-triphosphate"  'PDB Reference Data'
                    ATP 3 Atriphos  DrugBank
                    ATP 4 Striadyne DrugBank

            loop_
            _pdbx_chem_comp_identifier.comp_id
            _pdbx_chem_comp_identifier.type
            _pdbx_chem_comp_identifier.program
            _pdbx_chem_comp_identifier.program_version
            _pdbx_chem_comp_identifier.identifier
            ATP "SYSTEMATIC NAME" ACDLabs              10.04
            ;adenosine 5'-(tetrahydrogen triphosphate)
            ;
            ATP "SYSTEMATIC NAME" "OpenEye OEToolkits" 1.5.0
             "[[(2R,3S,4R,5R)-5-(6-aminopurin-9-yl)-3,4-dihydroxy-oxolan-2-yl]methoxy-hydroxy-phosphoryl] phosphono hydrogen phosphate"
            #

        """
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            if not (dataContainer.exists('chem_comp') and dataContainer.exists('pdbx_chem_comp_identifier')):
                return False
            #
            #
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                              'ordinal',
                                                                              'name',
                                                                              'provenance_code']))
            else:
                # remove the rowlist -
                pass
            #
            wObj = dataContainer.getObj(catName)
            #
            # Get all of the names relevant names from the definition -
            #
            iRow = 0
            provCode = 'PDB Reference Data'
            ccObj = dataContainer.getObj('chem_comp')
            ccId = ccObj.getValue('id', 0)
            ccName = ccObj.getValue('name', 0)
            ccSynonymL = []
            if ccObj.hasAttribute('pdbx_synonyms'):
                ccSynonymL = str(ccObj.getValue('pdbx_synonyms', 0)).split(';')
            #
            wObj.setValue(ccId, 'comp_id', iRow)
            wObj.setValue(ccName, 'name', iRow)
            wObj.setValue(iRow + 1, 'ordinal', iRow)
            wObj.setValue(provCode, 'provenance_code', iRow)
            iRow += 1
            for nm in ccSynonymL:
                if nm in ['?', '.']:
                    continue
                wObj.setValue(ccId, 'comp_id', iRow)
                wObj.setValue(nm, 'name', iRow)
                wObj.setValue(iRow + 1, 'ordinal', iRow)
                wObj.setValue(provCode, 'provenance_code', iRow)
                iRow += 1
            #
            ccIObj = dataContainer.getObj('pdbx_chem_comp_identifier')
            for ii in range(ccIObj.getRowCount()):
                nm = ccIObj.getValue('identifier', ii)
                prog = ccIObj.getValue('program', ii)
                wObj.setValue(ccId, 'comp_id', iRow)
                wObj.setValue(nm, 'name', iRow)
                wObj.setValue(iRow + 1, 'ordinal', iRow)
                wObj.setValue(prog, 'provenance_code', iRow)
                iRow += 1
            #
            dbD = self.__fetchDrugBankMapping(self.__drugBankMappingFilePath, workPath=self.__workPath)
            dbMapD = dbD['id_map']
            #
            if dbMapD and ccId in dbMapD and 'aliases' in dbMapD[ccId]:
                iRow = wObj.getRowCount()
                for nm in dbMapD[ccId]['aliases']:
                    wObj.setValue(ccId, 'comp_id', iRow)
                    wObj.setValue(nm, 'name', iRow)
                    wObj.setValue(iRow + 1, 'ordinal', iRow)
                    wObj.setValue('DrugBank', 'provenance_code', iRow)
                    iRow += 1

            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))

        return False

    def __getPolymerComposition(self, polymerTypeList):
        """
        polymerTypeList contains entity_poly.type and entity_branch.type values:

        Current polymer type list:
             'polypeptide(D)'
             'polypeptide(L)'
             'polydeoxyribonucleotide'
             'polyribonucleotide'
             'polysaccharide(D)'
             'polysaccharide(L)'
             'polydeoxyribonucleotide/polyribonucleotide hybrid'
             'cyclic-pseudo-peptide'
             'peptide nucleic acid'
             'other'
             "other type pair (polymer type count = 2)"
             "other composition (polymer type count >= 3)"
        Current branch type list:
             'oligosaccharide'

        Output composition classes:

            'homomeric protein' 'single protein entity'
            'heteromeric protein' 'multiple protein entities'
            'DNA' 'DNA entity/entities only'
            'RNA' 'RNA entity/entities only'
            'NA-hybrid' 'DNA/RNA hybrid entity/entities only'
            'protein/NA' 'Both protein and nucleic acid polymer entities'
            'DNA/RNA' 'Both DNA and RNA polymer entities'
            'oligosaccharide' 'One of more oligosaccharide entities'
            'protein/oligosaccharide' 'Both protein and oligosaccharide entities'
            'NA/oligosaccharide' 'Both NA and oligosaccharide entities'
            'other' 'Neither an individual protein, nucleic acid polymer nor oligosaccharide entity'
            'other type pair' 'Other combinations of 2 polymer types'
            'other type composition' 'Other combinations of 3 or more polymer types'

        And selected types -
            'Protein (only)' 'protein entity/entities only'
            'Nucleic acid (only)' 'DNA, RNA or NA-hybrid entity/entities only'
            'Protein/NA' 'Both protein and nucleic acid (DNA, RNA, or NA-hybrid) polymer entities'
            'Other' 'Another polymer type composition'

        And selected NA types -
            'DNA (only)' 'DNA entity/entities only'
            'RNA (only)' 'RNA entity/entities only'
            'NA-hybrid (only)' 'NA-hybrid entity/entities only'
            'DNA/RNA (only)' 'Both DNA and RNA polymer entities only'
            'Other' 'Another polymer type composition'
        """

        compClass = 'other'
        # get type counts
        cD = {}
        for polymerType in polymerTypeList:
            if polymerType in ['polypeptide(D)', 'polypeptide(L)']:
                cD['protein'] = cD['protein'] + 1 if 'protein' in cD else 1
            elif polymerType in ['polydeoxyribonucleotide']:
                cD['DNA'] = cD['DNA'] + 1 if 'DNA' in cD else 1
            elif polymerType in ['polyribonucleotide']:
                cD['RNA'] = cD['RNA'] + 1 if 'RNA' in cD else 1
            elif polymerType in ['polydeoxyribonucleotide/polyribonucleotide hybrid']:
                cD['NA-hybrid'] = cD['NA-hybrid'] + 1 if 'NA-hybrid' in cD else 1
            elif polymerType in ['oligosaccharide']:
                cD['oligosaccharide'] = cD['oligosaccharide'] + 1 if 'oligosaccharide' in cD else 1
            else:
                cD['other'] = cD['other'] + 1 if 'other' in cD else 1
        #
        if len(cD) == 1:
            ky = list(cD.keys())[0]
            if 'protein' in cD:
                if cD['protein'] == 1:
                    compClass = 'homomeric protein'
                else:
                    compClass = 'heteromeric protein'
            elif ky in ['DNA', 'RNA', 'NA-hybrid', 'oligosaccharide', 'other']:
                compClass = ky
        elif len(cD) == 2:
            if 'protein' in cD:
                if ('DNA' in cD) or ('RNA' in cD) or ('NA-hybrid' in cD):
                    compClass = 'protein/NA'
                elif 'oligosaccharide' in cD:
                    compClass = 'protein/oligosaccharide'
            elif 'DNA' in cD and 'RNA' in cD:
                compClass = 'DNA/RNA'
            elif 'oligosaccharide' in cD and ('RNA' in cD or 'DNA' in cD):
                compClass = 'NA/oligosaccharide'
            else:
                compClass = "other type pair"
        elif len(cD) == 3:
            if 'DNA' in cD and 'RNA' in cD and 'NA-hybrid' in cD:
                compClass = 'DNA/RNA'
            elif 'oligosaccharide' in cD and all([cD[j] in ['oligosaccharide', 'DNA', 'RNA', 'NA-hybrid'] for j in cD]):
                compClass = 'NA/oligosaccharide'
            elif 'protein' in cD and all([cD[j] in ['protein', 'DNA', 'RNA', 'NA-hybrid'] for j in cD]):
                compClass = 'protein/NA'
            elif 'oligosaccharide' in cD and 'protein' in cD and all([cD[j] in ['protein', 'oligosaccharide', 'DNA', 'RNA', 'NA-hybrid'] for j in cD]):
                compClass = 'protein/NA/oligosaccharide'
            else:
                compClass = "other type composition"
        elif len(cD) >= 4:
            if 'oligosaccharide' in cD and all([cD[j] in ['oligosaccharide', 'DNA', 'RNA', 'NA-hybrid'] for j in cD]):
                compClass = 'NA/oligosaccharide'
            elif 'protein' in cD and all([cD[j] in ['protein', 'DNA', 'RNA', 'NA-hybrid'] for j in cD]):
                compClass = 'protein/NA'
            elif 'oligosaccharide' in cD and 'protein' in cD and all([cD[j] in ['protein', 'oligosaccharide', 'DNA', 'RNA', 'NA-hybrid'] for j in cD]):
                compClass = 'protein/NA/oligosaccharide'
            else:
                compClass = "other type composition"
        else:
            compClass = "other type composition"

        # Subset type class --
        #
        if compClass in ['homomeric protein', 'heteromeric protein']:
            ptClass = 'Protein (only)'
        elif compClass in ['DNA', 'RNA', 'NA-hybrid']:
            ptClass = 'Nucleic acid (only)'
        elif compClass in ['protein/NA']:
            ptClass = 'Protein/NA'
        else:
            ptClass = 'Other'
        #
        # NA subtype class ---
        #
        if compClass in ['DNA']:
            naClass = 'DNA (only)'
        elif compClass in ['RNA']:
            naClass = 'RNA (only)'
        elif compClass in ['NA-hybrid']:
            naClass = 'NA-hybrid (only)'
        elif compClass in ['DNA/RNA']:
            naClass = 'DNA/RNA (only)'
        else:
            naClass = 'Other'
        #
        return compClass, ptClass, naClass, cD

    def __filterExperimentalMethod(self, methodL):
        """
        'X-ray'            'X-RAY DIFFRACTION, FIBER DIFFRACTION, or POWDER DIFFRACTION'
        'NMR'              'SOLUTION NMR or SOLID-STATE NMR'
        'EM'               'ELECTRON MICROSCOPY or ELECTRON CRYSTALLOGRAPHY or ELECTRON TOMOGRAPHY'
        'Neutron'          'NEUTRON DIFFRACTION'
        'Multiple methods' 'Multiple experimental methods'
        'Other'            'SOLUTION SCATTERING, EPR, THEORETICAL MODEL, INFRARED SPECTROSCOPY or FLUORESCENCE TRANSFER'
        """
        methodCount = len(methodL)
        if methodCount > 1:
            expMethod = 'Multiple methods'
        else:
            #
            mS = methodL[0].upper()
            expMethod = 'Other'
            if mS in ['X-RAY DIFFRACTION', 'FIBER DIFFRACTION', 'POWDER DIFFRACTION']:
                expMethod = 'X-ray'
            elif mS in ['SOLUTION NMR', 'SOLID-STATE NMR']:
                expMethod = 'NMR'
            elif mS in ['ELECTRON MICROSCOPY', 'ELECTRON CRYSTALLOGRAPHY']:
                expMethod = 'EM'
            elif mS in ['NEUTRON DIFFRACTION']:
                expMethod = 'Neutron'
            elif mS in ['SOLUTION SCATTERING', 'EPR', 'THEORETICAL MODEL', 'INFRARED SPECTROSCOPY', 'FLUORESCENCE TRANSFER']:
                expMethod = 'Other'
            else:
                logger.error('Unexpected method ')

        return methodCount, expMethod

    def __hasMethodNMR(self, methodL):
        ok = False
        for method in methodL:
            if method in ['SOLUTION NMR', 'SOLID-STATE NMR']:
                return True
        return ok

    def __isFloat(self, val):
        try:
            float(val)
        except Exception:
            return False
        return True

    def __getRepresentativeModels(self, dataContainer):
        """ Return the list of representative models

            Example:
                #
                _pdbx_nmr_ensemble.entry_id                                      5TM0
                _pdbx_nmr_ensemble.conformers_calculated_total_number            15
                _pdbx_nmr_ensemble.conformers_submitted_total_number             15
                _pdbx_nmr_ensemble.conformer_selection_criteria                  'all calculated structures submitted'
                _pdbx_nmr_ensemble.representative_conformer                      ?
                _pdbx_nmr_ensemble.average_constraints_per_residue               ?
                _pdbx_nmr_ensemble.average_constraint_violations_per_residue     ?
                _pdbx_nmr_ensemble.maximum_distance_constraint_violation         ?
                _pdbx_nmr_ensemble.average_distance_constraint_violation         ?
                _pdbx_nmr_ensemble.maximum_upper_distance_constraint_violation   ?
                _pdbx_nmr_ensemble.maximum_lower_distance_constraint_violation   ?
                _pdbx_nmr_ensemble.distance_constraint_violation_method          ?
                _pdbx_nmr_ensemble.maximum_torsion_angle_constraint_violation    ?
                _pdbx_nmr_ensemble.average_torsion_angle_constraint_violation    ?
                _pdbx_nmr_ensemble.torsion_angle_constraint_violation_method     ?
                #
                _pdbx_nmr_representative.entry_id             5TM0
                _pdbx_nmr_representative.conformer_id         1
                _pdbx_nmr_representative.selection_criteria   'fewest violations'
        """
        repModelL = []
        if dataContainer.exists('pdbx_nmr_representative'):
            tObj = dataContainer.getObj('pdbx_nmr_representative')
            if tObj.hasAttribute('conformer_id'):
                for ii in range(tObj.getRowCount()):
                    nn = tObj.getValue('conformer_id', ii)
                    if nn is not None and nn.isdigit():
                        repModelL.append(nn)

        if dataContainer.exists('pdbx_nmr_ensemble'):
            tObj = dataContainer.getObj('pdbx_nmr_ensemble')
            if tObj.hasAttribute('representative_conformer'):
                nn = tObj.getValue('representative_conformer', 0)
                if nn is not None and nn.isdigit():
                    repModelL.append(nn)
        #
        repModelL = list(set(repModelL))
        if len(repModelL) < 1:
            logger.debug("Missing representative model data for %s using 1" % (dataContainer.getName()))
            repModelL = ['1']

        return repModelL

    def __filterExperimentalResolution(self, dataContainer):
        """ Collect resolution estimates from method specific sources.
        """
        rL = []
        if dataContainer.exists('refine'):
            tObj = dataContainer.getObj('refine')
            if tObj.hasAttribute('ls_d_res_high'):
                for ii in range(tObj.getRowCount()):
                    rv = tObj.getValue('ls_d_res_high', ii)
                    if self.__isFloat(rv):
                        rL.append(rv)

        if dataContainer.exists('em_3d_reconstruction'):
            tObj = dataContainer.getObj('em_3d_reconstruction')
            if tObj.hasAttribute('resolution'):
                for ii in range(tObj.getRowCount()):
                    rv = tObj.getValue('resolution', ii)
                    if self.__isFloat(rv):
                        rL.append(rv)
        return rL

    def __setEntryCache(self, entryId):
        self.__cacheEntryId = entryId

    def __testEntryCache(self, entryId):
        return self.__cacheEntryId == entryId

    def __getInstanceTypes(self, dataContainer):
        """ Return dictionary entity types, type counts and polymer type (where applicable) for
            each instance in the deposited unit.

            Returns:

              instanceTypeD[asymId] = <entity_type>
              instanceCountD[<entity_type>] = #

              For polymer instances:
              instancePolymerTypeD[asymId] = <filtered polymer type>

'             instEntityD[asymId] = entityId
              epTypeD[entityId] = <polymer type>
        """

        rD = {}
        #
        try:
            if self.__instanceD and self.__testEntryCache(dataContainer.getName()):
                return self.__instanceD
            #
            self.__instanceD = None
            #
            if not dataContainer.exists('entity') or not dataContainer.exists('struct_asym'):
                return {}

            instanceTypeD = {}
            instancePolymerTypeD = {}
            instanceTypeCountD = {}
            #
            eObj = dataContainer.getObj('entity')
            eTypeD = {}
            for ii in range(eObj.getRowCount()):
                # logger.info("Attribute %r %r" % (ii, eObj.getAttributeList()))
                entityId = eObj.getValue('id', ii)
                eType = eObj.getValue('type', ii)
                eTypeD[entityId] = eType
            #
            epTypeD = {}
            epLengthD = {}
            epTypeFilteredD = {}
            if dataContainer.exists('entity_poly'):
                epObj = dataContainer.getObj('entity_poly')
                for ii in range(epObj.getRowCount()):
                    entityId = epObj.getValue('entity_id', ii)
                    pType = epObj.getValue('type', ii)
                    epTypeFilteredD[entityId] = self.__filterEntityPolyType(pType)
                    epTypeD[entityId] = pType
                    if epObj.hasAttribute('pdbx_seq_one_letter_code_can'):
                        sampleSeq = self.__stripWhiteSpace(epObj.getValue('pdbx_seq_one_letter_code_can', ii))
                        epLengthD[entityId] = len(sampleSeq) if sampleSeq and sampleSeq not in ['?', '.'] else None

            #
            instEntityD = {}
            sObj = dataContainer.getObj('struct_asym')
            for ii in range(sObj.getRowCount()):
                entityId = sObj.getValue('entity_id', ii)
                asymId = sObj.getValue('id', ii)
                instEntityD[asymId] = entityId
                if entityId in eTypeD:
                    instanceTypeD[asymId] = eTypeD[entityId]
                else:
                    logger.warning("Missing entity id entry %r asymId %r entityId %r" % (dataContainer.getName(), entityId, asymId))
                if entityId in epTypeD:
                    instancePolymerTypeD[asymId] = epTypeFilteredD[entityId]
                #
            #
            # Count the instance by type - initialize all types
            #
            instanceTypeCountD = {k: 0 for k in ['polymer', 'non-polymer', 'branched', 'macrolide', 'water']}
            for asymId, eType in instanceTypeD.items():
                instanceTypeCountD[eType] += 1

            rD = {'instanceTypeD': instanceTypeD,
                  'instancePolymerTypeD': instancePolymerTypeD,
                  'instanceTypeCountD': instanceTypeCountD,
                  'instEntityD': instEntityD,
                  'eTypeD': eTypeD,
                  'epLengthD': epLengthD,
                  'epTypeD': epTypeD,
                  'epTypeFilteredD': epTypeFilteredD,
                  }
            self.__instanceD = rD
            #
            logger.debug("%s length struct_asym %d (%d) instanceTypeD %r" % (dataContainer.getName(), sObj.getRowCount(), len(instanceTypeD), instanceTypeD))

        #
        except Exception as e:
            logger.exception("Failing with %r with %r" % (dataContainer.getName(), str(e)))
        #
        return rD

    def __getAtomSiteInfo(self, dataContainer):
        """ Get counting information about the deposited coordinates.
        """
        numAtoms = 0
        numModels = 0
        if dataContainer.exists('atom_site'):
            tObj = dataContainer.getObj('atom_site')
            numAtoms = tObj.getRowCount()
            if tObj.hasAttribute('pdbx_PDB_model_num'):
                try:
                    numModels = int(tObj.getValue('pdbx_PDB_model_num', numAtoms - 1))
                except Exception:
                    numModels = 1
        return numAtoms, numModels

    def __getQualifiedAtomSiteInfo(self, dataContainer, instanceTypeD, modelId='1'):
        """ Get counting information for each instance in the deposited coordinates for the input model.

            instanceTypeD [asymId] = <entity type>
        """
        # Return cached dictionary
        if self.__atomSiteCountD and self.__testEntryCache(dataContainer.getName()):
            logger.debug("Using cached qualified atom_site count info for %s" % dataContainer.getName())
            return self.__atomSiteCountD
        #
        numAtomsAll = 0
        numAtomsModel = 0
        typeCountD = {}
        instanceAtomCountD = {}
        instanceModeledMonomerCountD = {}
        instanceUnmodeledMonomerCountD = {}
        modelIdL = []
        #
        try:
            if dataContainer.exists('atom_site'):
                tObj = dataContainer.getObj('atom_site')
                numAtomsAll = tObj.getRowCount()
                conditionsD = {'pdbx_PDB_model_num': modelId}
                numAtomsModel = tObj.countValuesWhereConditions(conditionsD)
                modelIdL = tObj.getAttributeUniqueValueList('pdbx_PDB_model_num')
                cD = tObj.getCombinationCounts(['label_asym_id', 'pdbx_PDB_model_num'])
                #
                for asymId, eType in instanceTypeD.items():
                    instanceAtomCountD[asymId] = cD[(asymId, modelId)] if (asymId, modelId) in cD else 0
                #
                # for eType in ['polymer', 'non-polymer', 'branched', 'macrolide', 'solvent']:
                typeCountD = {k: 0 for k in ['polymer', 'non-polymer', 'branched', 'macrolide', 'water']}
                for asymId, aCount in instanceAtomCountD.items():
                    tt = instanceTypeD[asymId]
                    typeCountD[tt] += aCount
            else:
                logger.warning("Missing atom_site category for %s" % dataContainer.getName())
            #
            numModels = len(modelIdL)
            if numModels < 1:
                logger.warning("Missing model details in atom_site category for %s" % dataContainer.getName())
            #
            self.__atomSiteCountD = {'instanceAtomCountD': instanceAtomCountD,
                                     'typeAtomCountD': typeCountD,
                                     'numAtomsAll': numAtomsAll,
                                     'numAtomsModel': numAtomsModel,
                                     'numModels': len(modelIdL),
                                     'modelId': modelId,
                                     'instanceModeledMonomerCountD': {},
                                     'instanceUnmodeledMonomerCountD': {}
                                     }
        except Exception as e:
            logger.exception("Failing with %r with %r" % (dataContainer.getName(), str(e)))

        #
        #  Get the modeled and unmodeled monomer counts by asymId
        #
        try:
            psObj = dataContainer.getObj('pdbx_poly_seq_scheme')
            if psObj is not None:
                aSeqD = {}
                for ii in range(psObj.getRowCount()):
                    asymId = psObj.getValue('asym_id', ii)
                    # entityId = psObj.getValue('entity_id', ii)
                    authSeqNum = psObj.getValue('auth_seq_num', ii)
                    # compId = psObj.getValue('auth_mon_id', ii)
                    aSeqD.setdefault(asymId, []).append(authSeqNum)
                #
                for asymId, sL in aSeqD.items():
                    instanceModeledMonomerCountD[asymId] = len([t for t in sL if t not in ['?', '.']])
                    instanceUnmodeledMonomerCountD[asymId] = len([t for t in sL if t in ['?', '.']])

            self.__atomSiteCountD['instanceModeledMonomerCountD'] = instanceModeledMonomerCountD
            self.__atomSiteCountD['instanceUnmodeledMonomerCountD'] = instanceUnmodeledMonomerCountD
            logger.debug("%s instanceModeledMonomerCountD(%d) %r" % (dataContainer.getName(), sum(self.__atomSiteCountD[
                'instanceModeledMonomerCountD'].values()), self.__atomSiteCountD['instanceModeledMonomerCountD']))
            logger.debug("%s instanceUnmodeledMonomerCountD %r" % (dataContainer.getName(), self.__atomSiteCountD['instanceUnmodeledMonomerCountD']))

        except Exception as e:
            logger.exception("Failing for %s with %s" % (dataContainer.getName(), str(e)))

        #
        return self.__atomSiteCountD

    def __getStructConnInfo(self, dataContainer):
        """ Get counting information about intermolecular linkages.
            covale  .
            disulf  .
            hydrog  .
            metalc

            loop_
            _struct_asym.id
            _struct_asym.pdbx_blank_PDB_chainid_flag
            _struct_asym.pdbx_modified
            _struct_asym.entity_id
            _struct_asym.details
            A N N 1 ?
            B N N 1 ?
            #
            _struct_biol.id   1
            #
            loop_
            _struct_conn.id
            _struct_conn.conn_type_id
            _struct_conn.pdbx_leaving_atom_flag
            _struct_conn.pdbx_PDB_id
            _struct_conn.ptnr1_label_asym_id
            _struct_conn.ptnr1_label_comp_id
            _struct_conn.ptnr1_label_seq_id
            _struct_conn.ptnr1_label_atom_id
            _struct_conn.pdbx_ptnr1_label_alt_id
            _struct_conn.pdbx_ptnr1_PDB_ins_code
            _struct_conn.pdbx_ptnr1_standard_comp_id
            _struct_conn.ptnr1_symmetry
            _struct_conn.ptnr2_label_asym_id
            _struct_conn.ptnr2_label_comp_id
            _struct_conn.ptnr2_label_seq_id
            _struct_conn.ptnr2_label_atom_id
            _struct_conn.pdbx_ptnr2_label_alt_id
            _struct_conn.pdbx_ptnr2_PDB_ins_code
            _struct_conn.ptnr1_auth_asym_id
            _struct_conn.ptnr1_auth_comp_id
            _struct_conn.ptnr1_auth_seq_id
            _struct_conn.ptnr2_auth_asym_id
            _struct_conn.ptnr2_auth_comp_id
            _struct_conn.ptnr2_auth_seq_id
            _struct_conn.ptnr2_symmetry
            _struct_conn.pdbx_ptnr3_label_atom_id
            _struct_conn.pdbx_ptnr3_label_seq_id
            _struct_conn.pdbx_ptnr3_label_comp_id
            _struct_conn.pdbx_ptnr3_label_asym_id
            _struct_conn.pdbx_ptnr3_label_alt_id
            _struct_conn.pdbx_ptnr3_PDB_ins_code
            _struct_conn.details
            _struct_conn.pdbx_dist_value
            _struct_conn.pdbx_value_order
            disulf1  disulf ? ? A CYS 31 SG ? ? ? 1_555 B CYS 31 SG ? ? A CYS 31 B CYS 31 1_555 ? ? ? ? ? ? ? 1.997 ?
            covale1  covale ? ? A VAL 8  C  ? ? ? 1_555 A DPR 9  N  ? ? A VAL 8  A DPR 9  1_555 ? ? ? ? ? ? ? 1.360 ?
            covale2  covale ? ? A DPR 9  C  ? ? ? 1_555 A GLY 10 N  ? ? A DPR 9  A GLY 10 1_555 ? ? ? ? ? ? ? 1.324 ?
            covale3  covale ? ? A THR 16 C  ? ? ? 1_555 A DPR 17 N  ? ? A THR 16 A DPR 17 1_555 ? ? ? ? ? ? ? 1.361 ?
            covale4  covale ? ? A DPR 17 C  ? ? ? 1_555 A ALA 18 N  ? ? A DPR 17 A ALA 18 1_555 ? ? ? ? ? ? ? 1.326 ?
            covale5  covale ? ? A LEU 26 C  ? ? ? 1_555 A DPR 27 N  ? ? A LEU 26 A DPR 27 1_555 ? ? ? ? ? ? ? 1.359 ?
            covale6  covale ? ? A DPR 27 C  ? ? ? 1_555 A GLY 28 N  ? ? A DPR 27 A GLY 28 1_555 ? ? ? ? ? ? ? 1.326 ?
            covale7  covale ? ? B VAL 8  C  ? ? ? 1_555 B DPR 9  N  ? ? B VAL 8  B DPR 9  1_555 ? ? ? ? ? ? ? 1.361 ?
            covale8  covale ? ? B DPR 9  C  ? ? ? 1_555 B GLY 10 N  ? ? B DPR 9  B GLY 10 1_555 ? ? ? ? ? ? ? 1.324 ?
            covale9  covale ? ? B THR 16 C  ? ? ? 1_555 B DPR 17 N  ? ? B THR 16 B DPR 17 1_555 ? ? ? ? ? ? ? 1.361 ?
            covale10 covale ? ? B DPR 17 C  ? ? ? 1_555 B ALA 18 N  ? ? B DPR 17 B ALA 18 1_555 ? ? ? ? ? ? ? 1.324 ?
            covale11 covale ? ? B LEU 26 C  ? ? ? 1_555 B DPR 27 N  ? ? B LEU 26 B DPR 27 1_555 ? ? ? ? ? ? ? 1.361 ?
            covale12 covale ? ? B DPR 27 C  ? ? ? 1_555 B GLY 28 N  ? ? B DPR 27 B GLY 28 1_555 ? ? ? ? ? ? ? 1.323 ?
            #
        """
        numDiSulf = 0
        if dataContainer.exists('struct_conn'):
            tObj = dataContainer.getObj('struct_conn')
            for ii in range(tObj.getRowCount()):
                bt = str(tObj.getValue('conn_type_id', ii)).strip().upper()
                numDiSulf = numDiSulf + 1 if bt == 'DISULF' else numDiSulf
        #
        return numDiSulf

    def __toRangeList(self, iterable):
        iterable = sorted(set(iterable))
        for key, group in itertools.groupby(enumerate(iterable), lambda t: t[1] - t[0]):
            group = list(group)
            yield group[0][1], group[-1][1]
    #

    def __getProtSecStructInfo(self, dataContainer):
        """ Get
            #
            loop_
            _struct_conf.conf_type_id
            _struct_conf.id
            _struct_conf.pdbx_PDB_helix_id
            _struct_conf.beg_label_comp_id
            _struct_conf.beg_label_asym_id
            _struct_conf.beg_label_seq_id
            _struct_conf.pdbx_beg_PDB_ins_code
            _struct_conf.end_label_comp_id
            _struct_conf.end_label_asym_id
            _struct_conf.end_label_seq_id
            _struct_conf.pdbx_end_PDB_ins_code

            _struct_conf.beg_auth_comp_id
            _struct_conf.beg_auth_asym_id
            _struct_conf.beg_auth_seq_id
            _struct_conf.end_auth_comp_id
            _struct_conf.end_auth_asym_id
            _struct_conf.end_auth_seq_id
            _struct_conf.pdbx_PDB_helix_class
            _struct_conf.details
            _struct_conf.pdbx_PDB_helix_length
            HELX_P HELX_P1 AA1 SER A 5   ? LYS A 19  ? SER A 2   LYS A 16  1 ? 15
            HELX_P HELX_P2 AA2 GLU A 26  ? LYS A 30  ? GLU A 23  LYS A 27  5 ? 5
            HELX_P HELX_P3 AA3 GLY A 47  ? LYS A 60  ? GLY A 44  LYS A 57  1 ? 14
            HELX_P HELX_P4 AA4 ASP A 111 ? LEU A 125 ? ASP A 108 LEU A 122 1 ? 15
            #
            _struct_conf_type.id          HELX_P
            _struct_conf_type.criteria    ?
            _struct_conf_type.reference   ?
            # -------------------------------------------------------------------

            loop_
            _struct_asym.id
            _struct_asym.pdbx_blank_PDB_chainid_flag
            _struct_asym.pdbx_modified
            _struct_asym.entity_id
            _struct_asym.details
            A N N 1 ?
            B N N 1 ?
            loop_
            _struct_conn_type.id
            _struct_conn_type.criteria
            _struct_conn_type.reference
            disulf ? ?
            covale ? ?
            #
            _struct_sheet.id               A
            _struct_sheet.type             ?
            _struct_sheet.number_strands   8
            _struct_sheet.details          ?
            #
            loop_
            _struct_sheet_order.sheet_id
            _struct_sheet_order.range_id_1
            _struct_sheet_order.range_id_2
            _struct_sheet_order.offset
            _struct_sheet_order.sense
            A 1 2 ? anti-parallel
            A 2 3 ? anti-parallel
            A 3 4 ? anti-parallel
            A 4 5 ? anti-parallel
            A 5 6 ? anti-parallel
            A 6 7 ? anti-parallel
            A 7 8 ? anti-parallel
            #
            loop_
            _struct_sheet_range.sheet_id
            _struct_sheet_range.id
            _struct_sheet_range.beg_label_comp_id
            _struct_sheet_range.beg_label_asym_id
            _struct_sheet_range.beg_label_seq_id
            _struct_sheet_range.pdbx_beg_PDB_ins_code
            _struct_sheet_range.end_label_comp_id
            _struct_sheet_range.end_label_asym_id
            _struct_sheet_range.end_label_seq_id
            _struct_sheet_range.pdbx_end_PDB_ins_code

            _struct_sheet_range.beg_auth_comp_id
            _struct_sheet_range.beg_auth_asym_id
            _struct_sheet_range.beg_auth_seq_id
            _struct_sheet_range.end_auth_comp_id
            _struct_sheet_range.end_auth_asym_id
            _struct_sheet_range.end_auth_seq_id
            A 1 LYS A 5  ? VAL A 8  ? LYS A 5  VAL A 8
            A 2 ARG A 11 ? THR A 16 ? ARG A 11 THR A 16
            A 3 VAL A 19 ? LEU A 26 ? VAL A 19 LEU A 26
            A 4 TYR A 29 ? ALA A 35 ? TYR A 29 ALA A 35
            A 5 TYR B 29 ? ALA B 35 ? TYR B 29 ALA B 35
            A 6 VAL B 19 ? LEU B 26 ? VAL B 19 LEU B 26
            A 7 ARG B 11 ? THR B 16 ? ARG B 11 THR B 16
            A 8 LYS B 5  ? VAL B 8  ? LYS B 5  VAL B 8
            #

        """
        #
        rD = {'helixCountD': {},
              'sheetStrandCountD': {},
              'unassignedCountD': {},

              'helixLengthD': {},
              'sheetStrandLengthD': {},
              'unassignedLengthD': {},

              'helixFracD': {},
              'sheetStrandFracD': {},
              'unassignedFracD': {},

              'sheetSenseD': {},
              'sheetFullStrandCountD': {},

              'featureMonomerSequenceD': {},
              'featureSequenceD': {},
              }
        try:
            instanceD = self.__getInstanceTypes(dataContainer)
            instancePolymerTypeD = instanceD['instancePolymerTypeD'] if 'instancePolymerTypeD' in instanceD else {}
            instEntityD = instanceD['instEntityD'] if 'instEntityD' in instanceD else {}
            epLengthD = instanceD['epLengthD'] if 'epLengthD' in instanceD else {}
            #
            helixRangeD = {}
            sheetRangeD = {}
            sheetSenseD = {}
            unassignedRangeD = {}
            #
            if dataContainer.exists('struct_conf'):
                tObj = dataContainer.getObj('struct_conf')
                helixRangeD = {}
                for ii in range(tObj.getRowCount()):
                    confType = str(tObj.getValue('conf_type_id', ii)).strip().upper()
                    if confType in ['HELX_P']:
                        hId = tObj.getValue('id', ii)
                        begAsymId = tObj.getValue('beg_label_asym_id', ii)
                        endAsymId = tObj.getValue('end_label_asym_id', ii)
                        begSeqId = int(tObj.getValue('beg_label_seq_id', ii))
                        endSeqId = int(tObj.getValue('end_label_seq_id', ii))
                        if (begAsymId == endAsymId) and (begSeqId <= endSeqId):
                            helixRangeD.setdefault(hId, []).append((begAsymId, begSeqId, endSeqId))
                        else:
                            logger.warning("%s inconsistent struct_sheet_range description id = %s" % (dataContainer.getName(), hId))

            logger.debug("%s helixRangeD %r" % (dataContainer.getName(), helixRangeD.items()))

            if dataContainer.exists('struct_sheet_range'):
                tObj = dataContainer.getObj('struct_sheet_range')
                sheetRangeD = {}
                for ii in range(tObj.getRowCount()):
                    sId = tObj.getValue('sheet_id', ii)
                    begAsymId = tObj.getValue('beg_label_asym_id', ii)
                    endAsymId = tObj.getValue('end_label_asym_id', ii)
                    begSeqId = int(tObj.getValue('beg_label_seq_id', ii))
                    endSeqId = int(tObj.getValue('end_label_seq_id', ii))
                    if (begAsymId == endAsymId) and (begSeqId <= endSeqId):
                        sheetRangeD.setdefault(sId, []).append((begAsymId, begSeqId, endSeqId))
                    else:
                        logger.warning("%s inconsistent struct_conf description id = %s" % (dataContainer.getName(), sId))

            logger.debug("%s sheetRangeD %r" % (dataContainer.getName(), sheetRangeD.items()))
            #
            if dataContainer.exists('struct_sheet_order'):
                tObj = dataContainer.getObj('struct_sheet_order')
                #
                sheetSenseD = {}
                for ii in range(tObj.getRowCount()):
                    sId = tObj.getValue('sheet_id', ii)
                    sense = str(tObj.getValue('sense', ii)).strip().lower()
                    sheetSenseD.setdefault(sId, []).append(sense)
            #
            logger.debug("%s sheetSenseD %r" % (dataContainer.getName(), sheetSenseD.items()))
            # --------

            unassignedCoverageD = {}
            unassignedCountD = {}
            unassignedLengthD = {}
            unassignedFracD = {}

            helixCoverageD = {}
            helixCountD = {}
            helixLengthD = {}
            helixFracD = {}

            sheetCoverageD = {}
            sheetStrandCountD = {}
            sheetStrandLengthD = {}
            strandsPerBetaSheetD = {}
            sheetFullStrandCountD = {}
            sheetStrandFracD = {}
            instSheetD = {}
            instSheetSenseD = {}
            #
            featureMonomerSequenceD = {}
            featureSequenceD = {}
            #
            # ------------
            # Initialize over all protein instances
            for asymId, filteredType in instancePolymerTypeD.items():
                if filteredType != 'Protein':
                    continue
                helixCoverageD[asymId] = []
                helixLengthD[asymId] = []
                helixCountD[asymId] = 0
                helixFracD[asymId] = 0.0
                #
                sheetCoverageD[asymId] = []
                sheetStrandCountD[asymId] = 0
                sheetStrandLengthD[asymId] = []
                sheetFullStrandCountD[asymId] = []
                sheetStrandFracD[asymId] = 0.0
                instSheetD[asymId] = []
                instSheetSenseD[asymId] = []
                #
                unassignedCountD[asymId] = 0
                unassignedLengthD[asymId] = []
                unassignedFracD[asymId] = 0.0
                #
                featureMonomerSequenceD[asymId] = None
                featureSequenceD[asymId] = None
            # -------------
            #
            for hId, hL in helixRangeD.items():
                for (asymId, begSeqId, endSeqId) in hL:
                    helixCoverageD.setdefault(asymId, []).extend(range(begSeqId, endSeqId + 1))
                    helixLengthD.setdefault(asymId, []).append(abs(begSeqId - endSeqId) + 1)
                    helixCountD[asymId] = helixCountD[asymId] + 1 if asymId in helixCountD else 0
            #
            # ---------
            # betaSheetCount = len(sheetRangeD)
            #
            for sId, sL in sheetRangeD.items():
                strandsPerBetaSheetD[sId] = len(sL)
                for (asymId, begSeqId, endSeqId) in sL:
                    sheetCoverageD.setdefault(asymId, []).extend(range(begSeqId, endSeqId + 1))
                    sheetStrandLengthD.setdefault(asymId, []).append(abs(begSeqId - endSeqId) + 1)
                    sheetStrandCountD[asymId] = sheetStrandCountD[asymId] + 1 if asymId in sheetStrandCountD else 0
                    instSheetD.setdefault(asymId, []).append(sId)
            #
            # ---------
            senseTypeD = {}
            for sheetId, sL in sheetSenseD.items():
                if len(sL) < 1:
                    continue
                usL = list(set(sL))
                if len(usL) == 1:
                    senseTypeD[sheetId] = usL[0]
                else:
                    senseTypeD[sheetId] = 'mixed'
            # ---------
            #
            for asymId, filteredType in instancePolymerTypeD.items():
                logger.debug("%s processing %s type %r" % (dataContainer.getName(), asymId, filteredType))
                if filteredType != 'Protein':
                    continue
                entityId = instEntityD[asymId]
                entityLen = epLengthD[entityId]
                entityS = set(range(1, entityLen + 1))
                eLen = len(entityS)
                #
                helixS = set(helixCoverageD[asymId])
                sheetS = set(sheetCoverageD[asymId])
                commonS = helixS & sheetS
                if len(commonS):
                    logger.warning("%s asymId %s overlapping secondary structure assignments for monomers %r" % (dataContainer.getName(), asymId, commonS))
                    continue

                hLen = len(helixS) if asymId in helixCoverageD else 0
                sLen = len(sheetS) if asymId in sheetCoverageD else 0
                #
                unassignedS = entityS - helixS if hLen else entityS
                unassignedS = unassignedS - sheetS if sLen else unassignedS
                tLen = len(unassignedS)
                #
                if eLen != hLen + sLen + tLen:
                    logger.warning("%s overlapping secondary structure assignments for asymId %s" % (dataContainer.getName(), asymId))
                    continue
                #
                unassignedCoverageD[asymId] = list(unassignedS)
                helixFracD[asymId] = float(hLen) / float(eLen)
                sheetStrandFracD[asymId] = float(sLen) / float(eLen)
                unassignedFracD[asymId] = float(tLen) / float(eLen)
                #
                unassignedRangeD[asymId] = list(self.__toRangeList(unassignedS))
                unassignedCountD[asymId] = len(unassignedRangeD[asymId])
                unassignedLengthD[asymId] = [abs(i - j) + 1 for (i, j) in unassignedRangeD[asymId]]
                #
                # ------
                sIdL = instSheetD[asymId]
                #
                instSheetSenseD[asymId] = [senseTypeD[sId] for sId in sIdL if sId in senseTypeD]
                sheetFullStrandCountD[asymId] = [strandsPerBetaSheetD[sId] for sId in sIdL if sId in strandsPerBetaSheetD]
                #

                # ------
                ssTypeL = ['_'] * eLen
                if hLen:
                    for idx in helixCoverageD[asymId]:
                        ssTypeL[idx - 1] = 'H'
                if sLen:
                    for idx in sheetCoverageD[asymId]:
                        ssTypeL[idx - 1] = 'S'
                if tLen:
                    for idx in unassignedCoverageD[asymId]:
                        ssTypeL[idx - 1] = '_'
                #
                featureMonomerSequenceD[asymId] = ''. join(ssTypeL)
                featureSequenceD[asymId] = ''.join([t[0] for t in itertools.groupby(ssTypeL)])
            # ---------

            rD = {'helixCountD': helixCountD,
                  'sheetStrandCountD': sheetStrandCountD,
                  'unassignedCountD': unassignedCountD,

                  'helixLengthD': helixLengthD,
                  'sheetStrandLengthD': sheetStrandLengthD,
                  'unassignedLengthD': unassignedLengthD,

                  'helixFracD': helixFracD,
                  'sheetStrandFracD': sheetStrandFracD,
                  'unassignedFracD': unassignedFracD,

                  'sheetSenseD': instSheetSenseD,
                  'sheetFullStrandCountD': sheetFullStrandCountD,

                  'featureMonomerSequenceD': featureMonomerSequenceD,
                  'featureSequenceD': featureSequenceD,
                  }
        except Exception as e:
            logger.exception("Failing for %s with %s" % (dataContainer.getName(), str(e)))
        #
        return rD

    def addProtSecStructInfo(self, dataContainer, catName, **kwargs):
        """
        Add category rcsb_prot_sec_struct_info.

        """
        try:
            logger.debug("Starting with %r %r" % (dataContainer.getName(), catName))
            # Exit if source categories are missing
            if not dataContainer.exists('entry') and not (dataContainer.exists('struct_conf') or dataContainer.exists('struct_sheet_range')):
                return False
            #
            # Create the new target category rcsb_prot_sec_struct_info
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id',
                                                                              'label_asym_id',
                                                                              'helix_count',
                                                                              'beta_strand_count',
                                                                              'unassigned_count',
                                                                              'helix_length',
                                                                              'beta_strand_length',
                                                                              'unassigned_length',
                                                                              'helix_coverage_percent',
                                                                              'beta_strand_coverage_percent',
                                                                              'unassigned_coverage_percent',
                                                                              'beta_sheet_sense',
                                                                              'beta_sheet_strand_count',
                                                                              'feature_monomer_sequence',
                                                                              'feature_sequence'
                                                                              ]))
            # --------------------------------------------------------------------------------------------------------
            sD = self.__getProtSecStructInfo(dataContainer)
            # catName = rcsb_prot_sec_struct_info
            cObj = dataContainer.getObj(catName)
            #
            xObj = dataContainer.getObj('entry')
            entryId = xObj.getValue('id', 0)
            #
            for ii, asymId in enumerate(sD['helixCountD']):
                cObj.setValue(entryId, 'entry_id', ii)
                cObj.setValue(asymId, 'label_asym_id', ii)
                #
                cObj.setValue(sD['helixCountD'][asymId], 'helix_count', ii)
                cObj.setValue(sD['sheetStrandCountD'][asymId], 'beta_strand_count', ii)
                cObj.setValue(sD['unassignedCountD'][asymId], 'unassigned_count', ii)
                #
                cObj.setValue(','.join([str(t) for t in sD['helixLengthD'][asymId]]), 'helix_length', ii)
                cObj.setValue(','.join([str(t) for t in sD['sheetStrandLengthD'][asymId]]), 'beta_strand_length', ii)
                cObj.setValue(','.join([str(t) for t in sD['unassignedLengthD'][asymId]]), 'unassigned_length', ii)

                cObj.setValue('%.2f' % (100.0 * sD['helixFracD'][asymId]), 'helix_coverage_percent', ii)
                cObj.setValue('%.2f' % (100.0 * sD['sheetStrandFracD'][asymId]), 'beta_strand_coverage_percent', ii)
                cObj.setValue('%.2f' % (100.0 * sD['unassignedFracD'][asymId]), 'unassigned_coverage_percent', ii)

                cObj.setValue(','.join(sD['sheetSenseD'][asymId]), 'beta_sheet_sense', ii)
                cObj.setValue(','.join([str(t) for t in sD['sheetFullStrandCountD'][asymId]]), 'beta_sheet_strand_count', ii)

                cObj.setValue(sD['featureMonomerSequenceD'][asymId], 'feature_monomer_sequence', ii)
                cObj.setValue(sD['featureSequenceD'][asymId], 'feature_sequence', ii)

            return True
        except Exception as e:
            logger.exception("For %s %r failing with %s" % (dataContainer.getName(), catName, str(e)))
        return False

    def __filterEntityPolyType(self, pType):
        """
        Returns mappings:
            'Protein'   'polypeptide(D) or polypeptide(L)'
            'DNA'       'polydeoxyribonucleotide'
            'RNA'       'polyribonucleotide'
            'NA-hybrid' 'polydeoxyribonucleotide/polyribonucleotide hybrid'
            'Other'      'polysaccharide(D), polysaccharide(L), cyclic-pseudo-peptide, peptide nucleic acid, or other'

        """
        polymerType = pType.lower()
        if polymerType in ['polypeptide(d)', 'polypeptide(l)']:
            rT = 'Protein'
        elif polymerType in ['polydeoxyribonucleotide']:
            rT = 'DNA'
        elif polymerType in ['polyribonucleotide']:
            rT = 'RNA'
        elif polymerType in ['polydeoxyribonucleotide/polyribonucleotide hybrid']:
            rT = 'NA-hybrid'
        else:
            rT = 'Other'
        return rT

    def __getDepositedResidueCounts(self, dataContainer):
        """ Return the number of modeled and unmodeled residues in the deposited coordinate data.

            Using data from:
                loop_
                _pdbx_poly_seq_scheme.asym_id
                _pdbx_poly_seq_scheme.entity_id
                _pdbx_poly_seq_scheme.seq_id
                _pdbx_poly_seq_scheme.mon_id
                _pdbx_poly_seq_scheme.ndb_seq_num
                _pdbx_poly_seq_scheme.pdb_seq_num
                _pdbx_poly_seq_scheme.auth_seq_num <<< ----
                _pdbx_poly_seq_scheme.pdb_mon_id
                _pdbx_poly_seq_scheme.auth_mon_id <<< ----
                _pdbx_poly_seq_scheme.pdb_strand_id
                _pdbx_poly_seq_scheme.pdb_ins_code
                _pdbx_poly_seq_scheme.hetero
                A 1 1  MET 1  1  ?  ?   ?   A . n
                A 1 2  ALA 2  2  ?  ?   ?   A . n
                A 1 3  LYS 3  3  ?  ?   ?   A . n
                A 1 4  GLY 4  4  ?  ?   ?   A . n
                A 1 5  GLN 5  5  ?  ?   ?   A . n
                A 1 6  SER 6  6  6  SER SER A . n
                A 1 7  LEU 7  7  7  LEU LEU A . n
                                ^^      ^^^

        """
        modeledCount = 0
        unModeledCount = 0
        try:
            psObj = dataContainer.getObj('pdbx_poly_seq_scheme')
            if psObj is not None:
                asnL = psObj.getAttributeValueList('auth_seq_num')
                aaidL = psObj.getAttributeValueList('pdb_strand_id')
                unModeledCount = asnL.count('?')
                tL = [(a, b) for (a, b) in zip(asnL, aaidL) if a not in ['?']]
                modeledCount = len(set(tL))
                # modeledCount = len(uL) if ('?', '?') not in uL else len(uL) - 1
                logger.debug("%s %d (%d)" % (dataContainer.getName(), modeledCount, unModeledCount))
        except Exception as e:
            logger.exception("Failing for %s with %s" % (dataContainer.getName(), str(e)))
        #
        return modeledCount, unModeledCount

    def addEntryInfo(self, dataContainer, catName, **kwargs):
        """
        Add  _rcsb_entry_info, for example:
             _rcsb_entry_info.entry_id                      1ABC
             _rcsb_entry_info.polymer_composition           'heteromeric protein'
             _rcsb_entry_info.experimental_method           'multiple methods'
             _rcsb_entry_info.experimental_method_count     2
             _rcsb_entry_info.polymer_entity_count          2
             _rcsb_entry_info.entity_count                  2
             _rcsb_entry_info.nonpolymer_entity_count       2
             _rcsb_entry_info.branched_entity_count         0
             _rcsb_entry_info.software_programs_combined    'Phenix;RefMac'
             ....

        Also add the related field:

        _entity_poly.rcsb_entity_polymer_type

            'Protein'   'polypeptide(D) or polypeptide(L)'
            'DNA'       'polydeoxyribonucleotide'
            'RNA'       'polyribonucleotide'
            'NA-hybrid' 'polydeoxyribonucleotide/polyribonucleotide hybrid'
            'Other'      'polysaccharide(D), polysaccharide(L), cyclic-pseudo-peptide, peptide nucleic acid, or other'
            #
          _rcsb_entry_info.deposited_polymer_monomer_count
          'polymer_entity_count_protein',
          'polymer_entity_count_nucleic_acid',
          'polymer_entity_count_nucleic_acid_hybrid',
          'polymer_entity_count_DNA',
          'polymer_entity_count_RNA',

        """
        try:
            logger.debug("Starting with %r %r" % (dataContainer.getName(), catName))
            # Exit if source categories are missing
            if not (dataContainer.exists('exptl') and dataContainer.exists('entity')):
                return False
            #
            # Create the new target category rcsb_entry_info
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id',
                                                                              'polymer_composition',
                                                                              'experimental_method',
                                                                              'experimental_method_count',
                                                                              'polymer_entity_count',
                                                                              'entity_count',
                                                                              'nonpolymer_entity_count',
                                                                              'branched_entity_count',
                                                                              'solvent_entity_count',
                                                                              'software_programs_combined',
                                                                              'resolution_combined',
                                                                              'deposited_atom_count',
                                                                              'deposited_model_count',
                                                                              'disulfide_bond_count',
                                                                              'deposited_polymer_monomer_count',
                                                                              'deposited_modeled_polymer_monomer_count',
                                                                              'deposited_unmodeled_polymer_monomer_count',
                                                                              'polymer_entity_count_protein',
                                                                              'polymer_entity_count_nucleic_acid',
                                                                              'polymer_entity_count_nucleic_acid_hybrid',
                                                                              'polymer_entity_count_DNA',
                                                                              'polymer_entity_count_RNA',
                                                                              'selected_polymer_entity_types',
                                                                              'na_polymer_entity_types',
                                                                              'polymer_entity_taxonomy_count',
                                                                              'assembly_count',
                                                                              'deposited_polymer_entity_instance_count',
                                                                              'deposited_nonpolymer_entity_instance_count'
                                                                              ]))
            # --------------------------------------------------------------------------------------------------------
            # catName = rcsb_entry_info
            cObj = dataContainer.getObj(catName)
            #
            # --------------------------------------------------------------------------------------------------------
            #  Filter experimental methods
            #
            xObj = dataContainer.getObj('exptl')
            entryId = xObj.getValue('entry_id', 0)
            methodL = xObj.getAttributeValueList('method')
            methodCount, expMethod = self.__filterExperimentalMethod(methodL)
            cObj.setValue(entryId, 'entry_id', 0)
            cObj.setValue(expMethod, 'experimental_method', 0)
            cObj.setValue(methodCount, 'experimental_method_count', 0)
            #
            # --------------------------------------------------------------------------------------------------------
            #  Experimental resolution -
            #
            resL = self.__filterExperimentalResolution(dataContainer)
            if resL:
                cObj.setValue(','.join(resL), 'resolution_combined', 0)
            #
            # ---------------------------------------------------------------------------------------------------------
            # Consolidate software details -
            #
            swNameL = []
            if dataContainer.exists('software'):
                swObj = dataContainer.getObj('software')
                swNameL.extend(swObj.getAttributeUniqueValueList('name'))
            if dataContainer.exists('pdbx_nmr_software'):
                swObj = dataContainer.getObj('pdbx_nmr_software')
                swNameL.extend(swObj.getAttributeUniqueValueList('name'))
            if dataContainer.exists('em_software'):
                swObj = dataContainer.getObj('em_software')
                swNameL.extend(swObj.getAttributeUniqueValueList('name'))
            if swNameL:
                cObj.setValue(';'.join(swNameL), 'software_programs_combined', 0)
            # ---------------------------------------------------------------------------------------------------------
            #  ENTITY FEATURES
            #
            #  entity and polymer entity counts -
            ##
            eObj = dataContainer.getObj('entity')
            eTypeL = eObj.getAttributeValueList('type')
            #
            numPolymers = 0
            numNonPolymers = 0
            numBranched = 0
            numSolvent = 0
            for eType in eTypeL:
                if eType == 'polymer':
                    numPolymers += 1
                elif eType == 'non-polymer':
                    numNonPolymers += 1
                elif eType == 'branched':
                    numBranched += 1
                elif eType == 'water':
                    numSolvent += 1
                else:
                    logger.error("Unexpected entity type for %s %s" % (dataContainer.getName(), eType))
            totalEntities = numPolymers + numNonPolymers + numBranched + numSolvent
            #
            # Simplified entity polymer type: 'Protein', 'DNA', 'RNA', 'NA-hybrid', or 'Other'
            pTypeL = []
            if dataContainer.exists('entity_poly'):
                epObj = dataContainer.getObj('entity_poly')
                pTypeL = epObj.getAttributeValueList('type')
                #
                atName = 'rcsb_entity_polymer_type'
                if not epObj.hasAttribute(atName):
                    epObj.appendAttribute(atName)
                for ii in range(epObj.getRowCount()):
                    epObj.setValue(self.__filterEntityPolyType(pTypeL[ii]), atName, ii)
            #
            # Add any branched entity types to the type list -
            if dataContainer.exists('entity_branch'):
                ebObj = dataContainer.getObj('entity_branch')
                pTypeL.extend(ebObj.getAttributeValueList('type'))
            #
            polymerCompClass, ptClass, naClass, eptD = self.__getPolymerComposition(pTypeL)
            #

            cObj.setValue(polymerCompClass, 'polymer_composition', 0)
            cObj.setValue(ptClass, 'selected_polymer_entity_types', 0)
            cObj.setValue(naClass, 'na_polymer_entity_types', 0)
            cObj.setValue(numPolymers, 'polymer_entity_count', 0)
            cObj.setValue(numNonPolymers, 'nonpolymer_entity_count', 0)
            cObj.setValue(numBranched, 'branched_entity_count', 0)
            cObj.setValue(numSolvent, 'solvent_entity_count', 0)
            cObj.setValue(totalEntities, 'entity_count', 0)
            #
            num = eptD['protein'] if 'protein' in eptD else 0
            cObj.setValue(num, 'polymer_entity_count_protein', 0)
            #
            num = eptD['NA-hybrid'] if 'NA-hybrid' in eptD else 0
            cObj.setValue(num, 'polymer_entity_count_nucleic_acid_hybrid', 0)
            #
            numDNA = eptD['DNA'] if 'DNA' in eptD else 0
            cObj.setValue(numDNA, 'polymer_entity_count_DNA', 0)
            #
            numRNA = eptD['RNA'] if 'RNA' in eptD else 0
            cObj.setValue(numRNA, 'polymer_entity_count_RNA', 0)
            cObj.setValue(numDNA + numRNA, 'polymer_entity_count_nucleic_acid', 0)
            #
            # ---------------------------------------------------------------------------------------------------------
            # INSTANCE FEATURES
            #
            ##
            repModelL = ['1']
            if self.__hasMethodNMR(methodL):
                repModelL = self.__getRepresentativeModels(dataContainer)
            logger.debug("Representative model list %r" % repModelL)
            #
            #  instanceTypeD[asymId] = <entity_type>
            #  instanceTypeCountD[entity_type] = #
            #
            #
            instanceD = self.__getInstanceTypes(dataContainer)
            instanceTypeD = instanceD['instanceTypeD'] if 'instanceTypeD' in instanceD else {}
            instanceTypeCountD = instanceD['instanceTypeCountD'] if 'instanceTypeCountD' in instanceD else {}

            cObj.setValue(instanceTypeCountD['polymer'], 'deposited_polymer_entity_instance_count', 0)
            cObj.setValue(instanceTypeCountD['non-polymer'], 'deposited_nonpolymer_entity_instance_count', 0)

            atomCountD = self.__getQualifiedAtomSiteInfo(dataContainer, instanceTypeD, modelId=repModelL[0])
            self.__setEntryCache(dataContainer.getName())
            #
            # Various atom counts -
            #
            logger.debug("numAtomsAll %d numAtomsModel %d numModels %d" %
                         (atomCountD['numAtomsAll'], atomCountD['numAtomsModel'], atomCountD['numModels']))
            #
            logger.debug("typeAtomCountD %r" % atomCountD['typeAtomCountD'])
            logger.debug("instanceAtomCoundD %r" % (atomCountD['instanceAtomCountD']))
            #
            if atomCountD['numAtomsModel'] > 0:
                cObj.setValue(atomCountD['numAtomsModel'], 'deposited_atom_count', 0)
                cObj.setValue(atomCountD['numModels'], 'deposited_model_count', 0)
            #

            # ---------------------------------------------------------------------------------------------------------
            #  Deposited monomer/residue instance counts
            #
            #  Get modeled and unmodeled residue counts
            #
            modeledCount, unModeledCount = self.__getDepositedResidueCounts(dataContainer)
            cObj.setValue(modeledCount, 'deposited_modeled_polymer_monomer_count', 0)
            cObj.setValue(unModeledCount, 'deposited_unmodeled_polymer_monomer_count', 0)
            cObj.setValue(modeledCount + unModeledCount, 'deposited_polymer_monomer_count', 0)
            #
            # ---------------------------------------------------------------------------------------------------------
            #  Counts of intermolecular bonds/linkages
            #
            numDiSulf = self.__getStructConnInfo(dataContainer)
            cObj.setValue(numDiSulf, 'disulfide_bond_count', 0)
            #
            # This is reset in  mehtod - filterSourceOrganismDetails()
            cObj.setValue(None, 'polymer_entity_taxonomy_count', 0)
            #
            return True
        except Exception as e:
            logger.exception("For %s %r failing with %s" % (dataContainer.getName(), catName, str(e)))
        return False

    def filterBlockByMethod(self, dataContainer, blockName, **kwargs):
        """ Filter empty placeholder data categories by experimental method.

        """
        logger.debug("Starting with %r blockName %r" % (dataContainer.getName(), blockName))
        try:
            if not dataContainer.exists('exptl'):
                return False
            #
            xObj = dataContainer.getObj('exptl')
            methodL = xObj.getAttributeValueList('method')
            objNameL = []
            # Test for a diffraction method in the case of multiple methods
            if len(methodL) > 1:
                isXtal = False
                for method in methodL:
                    if method in ['X-RAY DIFFRACTION', 'FIBER DIFFRACTION', 'POWDER DIFFRACTION', 'ELECTRON CRYSTALLOGRAPHY', 'NEUTRON DIFFRACTION']:
                        isXtal = True
                        break
                if not isXtal:
                    objNameL = ['cell', 'symmetry', 'refine', 'refine_hist', 'software', 'diffrn', 'diffrn_radiation']
            else:
                #
                mS = methodL[0].upper()
                if mS in ['X-RAY DIFFRACTION', 'FIBER DIFFRACTION', 'POWDER DIFFRACTION', 'ELECTRON CRYSTALLOGRAPHY', 'NEUTRON DIFFRACTION']:
                    objNameL = []
                elif mS in ['SOLUTION NMR', 'SOLID-STATE NMR']:
                    objNameL = ['cell', 'symmetry', 'refine', 'refine_hist', 'software', 'diffrn', 'diffrn_radiation']
                elif mS in ['ELECTRON MICROSCOPY']:
                    objNameL = ['cell', 'symmetry', 'refine', 'refine_hist', 'software', 'diffrn', 'diffrn_radiation']
                elif mS in ['SOLUTION SCATTERING', 'EPR', 'THEORETICAL MODEL', 'INFRARED SPECTROSCOPY', 'FLUORESCENCE TRANSFER']:
                    objNameL = ['cell', 'symmetry', 'refine', 'refine_hist', 'software', 'diffrn', 'diffrn_radiation']
                else:
                    logger.error('Unexpected method %r' % mS)
            #
            for objName in objNameL:
                dataContainer.remove(objName)
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (dataContainer.getName(), str(e)))
        return False

    def addBirdEntityIds(self, dataContainer, catName, atName, **kwargs):
        """ Add entity ids for BIRD molecule instances.

            loop_
            _pdbx_molecule.instance_id
            _pdbx_molecule.prd_id
            _pdbx_molecule.asym_id

            loop_
            _pdbx_entity_nonpoly.entity_id
            _pdbx_entity_nonpoly.name
            _pdbx_entity_nonpoly.comp_id


        Update/add:

        _pdbx_molecule.rcsb_entity_id
        _pdbx_molecule.rcsb_comp_id

        _pdbx_entity_nonpoly.rcsb_prd_id
        _entity_poly.rcsb_prd_id

        _rcsb_entity_containter_identifiers.prd_id

        """
        try:
            if catName != 'pdbx_molecule' and 'atName' != 'rcsb_entity_id':
                return False
            #
            if not (dataContainer.exists(catName) and dataContainer.exists('struct_asym')):
                return False
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            if not cObj.hasAttribute('rcsb_comp_id'):
                cObj.appendAttribute('rcsb_comp_id')
            #
            aD = {}
            aObj = dataContainer.getObj('struct_asym')
            for ii in range(aObj.getRowCount()):
                entityId = aObj.getValue('entity_id', ii)
                asymId = aObj.getValue('id', ii)
                aD[asymId] = entityId
            #
            eD = {}
            if dataContainer.exists('pdbx_entity_nonpoly'):
                npObj = dataContainer.getObj('pdbx_entity_nonpoly')
                for ii in range(npObj.getRowCount()):
                    entityId = npObj.getValue('entity_id', ii)
                    compId = npObj.getValue('comp_id', ii)
                    eD[entityId] = compId
            #
            #
            prdD = {}
            for ii in range(cObj.getRowCount()):
                asymId = cObj.getValue('asym_id', ii)
                prdId = cObj.getValue('prd_id', ii)
                if asymId in aD:
                    entityId = aD[asymId]
                    prdD[entityId] = prdId
                    cObj.setValue(entityId, atName, ii)
                    compId = eD[entityId] if entityId in eD else '.'
                    cObj.setValue(compId, 'rcsb_comp_id', ii)
                else:
                    logger.error("%s missing entityId for asymId %s" % (dataContainer.getName(), asymId))
            #
            if prdD and dataContainer.exists('pdbx_entity_nonpoly'):
                npObj = dataContainer.getObj('pdbx_entity_nonpoly')
                if not npObj.hasAttribute('rcsb_prd_id'):
                    npObj.appendAttribute('rcsb_prd_id')
                for ii in range(npObj.getRowCount()):
                    entityId = npObj.getValue('entity_id', ii)
                    prdId = prdD[entityId] if entityId in prdD else '.'
                    npObj.setValue(prdId, 'rcsb_prd_id', ii)
            #
            if prdD and dataContainer.exists('entity_poly'):
                pObj = dataContainer.getObj('entity_poly')
                if not pObj.hasAttribute('rcsb_prd_id'):
                    pObj.appendAttribute('rcsb_prd_id')
                for ii in range(pObj.getRowCount()):
                    entityId = pObj.getValue('entity_id', ii)
                    prdId = prdD[entityId] if entityId in prdD else '.'
                    pObj.setValue(prdId, 'rcsb_prd_id', ii)
            #
            #
            if prdD and dataContainer.exists('rcsb_entity_container_identifiers'):
                pObj = dataContainer.getObj('rcsb_entity_container_identifiers')
                if not pObj.hasAttribute('prd_id'):
                    pObj.appendAttribute('prd_id')
                for ii in range(pObj.getRowCount()):
                    entityId = pObj.getValue('entity_id', ii)
                    prdId = prdD[entityId] if entityId in prdD else '.'
                    pObj.setValue(prdId, 'prd_id', ii)
            #
            #
            return True
        except Exception as e:
            logger.exception("%s %s %s failing with %s" % (dataContainer.getName(), catName, atName, str(e)))
        return False

    def __cleanupCsv(self, tL):
        """ Ad hoc cleanup function for comma separated lists with embedded punctuation
        """
        rL = []
        try:
            key_paths = functools.cmp_to_key(cmp_elements)
            groups = [','.join(grp) for key, grp in itertools.groupby(tL, key_paths)]
            rL = list(set(groups))
        except Exception:
            pass
        return rL

    def addEntityMisc(self, dataContainer, catName, atName, **kwargs):
        """ Add miscellaneous entity attributes -

        Add:

        _entity.rcsb_macromolecular_names_combined  <<< Dictionary target

        _entity.rcsb_ec_lineage_name
        _entity.rcsb_ec_lineage_id
        _entity.rcsb_ec_lineage_depth

        """
        try:
            if not (dataContainer.exists('entry') and dataContainer.exists('entity')):
                return False
            #
            if catName == 'entity' and atName in ['rcsb_ec_lineage_name', 'rcsb_ec_lineage_id', 'rcsb_ec_lineage_depth']:
                return True
            #
            eObj = dataContainer.getObj('entity')
            if not eObj.hasAttribute('rcsb_macromolecular_names_combined_name'):
                eObj.appendAttribute('rcsb_macromolecular_names_combined_name')
            if not eObj.hasAttribute('rcsb_macromolecular_names_combined_provenance_source'):
                eObj.appendAttribute('rcsb_macromolecular_names_combined_provenance_source')
            if not eObj.hasAttribute('rcsb_macromolecular_names_combined_provenance_code'):
                eObj.appendAttribute('rcsb_macromolecular_names_combined_provenance_code')
            #
            if not eObj.hasAttribute('rcsb_ec_lineage_depth'):
                eObj.appendAttribute('rcsb_ec_lineage_depth')
            if not eObj.hasAttribute('rcsb_ec_lineage_id'):
                eObj.appendAttribute('rcsb_ec_lineage_id')
            if not eObj.hasAttribute('rcsb_ec_lineage_name'):
                eObj.appendAttribute('rcsb_ec_lineage_name')
            hasEc = eObj.hasAttribute('pdbx_ec')
            if hasEc:
                if not self.__ecU:
                    self.__ecU = EnzymeDatabaseUtils(enzymeDirPath=self.__enzymeDataPath, useCache=True, clearCache=False)
            #
            ncObj = None
            if dataContainer.exists('entity_name_com'):
                ncObj = dataContainer.getObj('entity_name_com')

            for ii in range(eObj.getRowCount()):
                entityId = eObj.getValue('id', ii)
                entityType = eObj.getValue('type', ii)
                #
                eObj.setValue('?', 'rcsb_ec_lineage_depth', ii)
                eObj.setValue('?', 'rcsb_ec_lineage_id', ii)
                eObj.setValue('?', 'rcsb_ec_lineage_name', ii)
                eObj.setValue('?', 'rcsb_macromolecular_names_combined_name', ii)
                eObj.setValue('?', 'rcsb_macromolecular_names_combined_provenance_source', ii)
                eObj.setValue('?', 'rcsb_macromolecular_names_combined_provenance_code', ii)
                #
                if entityType not in ['polymer', 'branched']:
                    continue
                #
                # --------------------------------------------------------------------------
                #  PDB assigned names
                nameL = []
                sourceL = []
                provCodeL = []
                nmL = str(eObj.getValue('pdbx_description', ii)).split(',')
                nmL = self.__cleanupCsv(nmL)
                nmL = [t.strip() for t in nmL if len(t) > 3]
                for nm in nmL:
                    nameL.append(nm)
                    sourceL.append('PDB Preferred Name')
                    provCodeL.append('ECO:0000304')
                #
                # PDB common names/synonyms
                logger.debug("%s ii %d nmL %r" % (dataContainer.getName(), ii, nmL))
                #
                if ncObj:
                    ncL = []
                    tL = ncObj.selectValuesWhere('name', entityId, 'entity_id')
                    logger.debug("%s ii %d tL %r" % (dataContainer.getName(), ii, tL))
                    for t in tL:
                        tff = t.split(',')
                        ncL.extend(tff)
                    ncL = self.__cleanupCsv(ncL)
                    ncL = [t.strip() for t in ncL if len(t) > 3]
                    for nc in ncL:
                        nameL.append(nc)
                        sourceL.append('PDB Synonym')
                        provCodeL.append('ECO:0000303')
                    logger.debug("%s ii %d ncL %r" % (dataContainer.getName(), ii, ncL))
                #
                if nameL:
                    eObj.setValue(';'.join(nameL), 'rcsb_macromolecular_names_combined_name', ii)
                    eObj.setValue(';'.join(sourceL), 'rcsb_macromolecular_names_combined_provenance_source', ii)
                    eObj.setValue(';'.join(provCodeL), 'rcsb_macromolecular_names_combined_provenance_code', ii)

                # --------------------------------------------------------------------------
                linL = []
                if hasEc:
                    ecV = eObj.getValue('pdbx_ec', ii)
                    ecIdL = ecV.split(',') if ecV else []
                    if ecIdL:
                        ecIdL = list(set(ecIdL))
                        for ecId in ecIdL:
                            tL = self.__ecU.getLineage(ecId) if ecId and len(ecId) > 7 else None
                            if tL:
                                linL.extend(tL)
                if linL:
                    eObj.setValue(';'.join([str(tup[0]) for tup in linL]), 'rcsb_ec_lineage_depth', ii)
                    eObj.setValue(';'.join([str(tup[1]) for tup in linL]), 'rcsb_ec_lineage_id', ii)
                    eObj.setValue(';'.join([tup[2] for tup in linL]), 'rcsb_ec_lineage_name', ii)

            return True
        except Exception as e:
            logger.exception("For %s %s failing with %s" % (catName, atName, str(e)))
        return False

    def addStructRefSeqEntityIds(self, dataContainer, catName, **kwargs):
        """ Add entity ids in categories struct_ref_seq and struct_ref_seq_dir instances.

        """
        try:
            logger.debug("Starting with %r %r" % (dataContainer.getName(), catName))
            if catName != 'struct_ref_seq':
                return False
            #
            if not (dataContainer.exists(catName) and dataContainer.exists('struct_ref')):
                return False
            #
            atName = 'rcsb_entity_id'
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            srObj = dataContainer.getObj('struct_ref')
            #
            srsdObj = None
            if dataContainer.exists('struct_ref_seq_dif'):
                srsdObj = dataContainer.getObj('struct_ref_seq_dif')
                if not srsdObj.hasAttribute('rcsb_entity_id'):
                    srsdObj.appendAttribute('rcsb_entity_id')

            for ii in range(srObj.getRowCount()):
                entityId = srObj.getValue('entity_id', ii)
                refId = srObj.getValue('id', ii)
                #
                # Get indices for the target refId.
                iRowL = cObj.selectIndices(refId, 'ref_id')
                for iRow in iRowL:
                    cObj.setValue(entityId, 'rcsb_entity_id', iRow)
                    alignId = cObj.getValue('align_id', iRow)
                    #
                    if srsdObj:
                        jRowL = srsdObj.selectIndices(alignId, 'align_id')
                        for jRow in jRowL:
                            srsdObj.setValue(entityId, 'rcsb_entity_id', jRow)

            return True
        except Exception as e:
            logger.exception("%s %s failing with %s" % (dataContainer.getName(), catName, str(e)))
        return False

    def buildEntityPolyInfo(self, dataContainer, catName, **kwargs):
        """ Build category rcsb_entity_poly_info

        For example:
            loop_
            _rcsb_entity_poly_info.ordinal_id
            _rcsb_entity_poly_info.entry_id
            _rcsb_entity_poly_info.entity_id
            _rcsb_entity_poly_info.comp_id
            _rcsb_entity_poly_info.is_modified
            _rcsb_entity_poly_info.is_heterogeneous
            1 1ABC 1 1 MSE Y N
            2 1ABC 1 2 TRP N N
            # ... abbreviated ...

            loop_
            _entity_poly_seq.entity_id
            _entity_poly_seq.num
            _entity_poly_seq.mon_id
            _entity_poly_seq.hetero

        """
        logger.debug("Starting with %r %r" % (dataContainer.getName(), catName))
        try:
            # Exit if source categories are missing
            if not (dataContainer.exists('entity_poly_seq') and dataContainer.exists('entity_poly') and dataContainer.exists('entry')):
                return False
            #
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['ordinal_id',
                                                                              'entry_id',
                                                                              'entity_id',
                                                                              'comp_id',
                                                                              'chem_comp_count',
                                                                              'entity_sequence_length',
                                                                              'is_modified',
                                                                              ]))
            #
            cN = 'rcsb_entity_monomer_container_identifiers'
            if not dataContainer.exists(cN):
                dataContainer.append(DataCategory(cN, attributeNameList=['ordinal_id',
                                                                         'entry_id',
                                                                         'entity_id',
                                                                         'comp_id'
                                                                         ]))
            idObj = dataContainer.getObj(cN)
            #
            eObj = dataContainer.getObj('entry')
            entryId = eObj.getValue('id', 0)
            # ------- --------- ------- --------- ------- --------- ------- --------- ------- ---------
            seqDifD = {}
            if dataContainer.exists('struct_ref_seq_dif'):
                srsdObj = dataContainer.getObj('struct_ref_seq_dif')
                for ii in range(srsdObj.getRowCount()):
                    entityId = srsdObj.getValue('rcsb_entity_id', ii)
                    if entityId not in seqDifD:
                        seqDifD[entityId] = {'mutations': 0, 'insertions': 0, 'deletions': 0, 'conflicts': 0}

                    details = srsdObj.getValue('details', ii)
                    #
                    if details in ['ACETYLATION', 'CHROMOPHORE', 'VARIANT', 'LEADER SEQUENCE',
                                   'INITIATING METHIONINE', 'LINKER', 'MODIFIED RESIDUE',
                                   'ENGINEERED', 'CLONING ARTIFACT', 'ENGINEERED MUTATION',
                                   'EXPRESSION TAG'] or ('CLONING' in details) or ('MODIFIED' in details):
                        seqDifD[entityId]['mutations'] += 1
                    #
                    if details in ['INSERTION']:
                        seqDifD[entityId]['insertions'] += 1
                    if details in ['DELETION']:
                        seqDifD[entityId]['deletions'] += 1
                    if details in ['CONFLICT']:
                        seqDifD[entityId]['conflicts'] += 1
                #
                logger.debug("seqDifD %r " % seqDifD)
            #
            epObj = dataContainer.getObj('entity_poly')
            sampleSeqLen = {}
            if epObj.hasAttribute('pdbx_seq_one_letter_code_can'):
                for ii in range(epObj.getRowCount()):
                    entityId = epObj.getValue('entity_id', ii)
                    sampleSeq = self.__stripWhiteSpace(epObj.getValue('pdbx_seq_one_letter_code_can', ii))
                    sampleSeqLen[entityId] = len(sampleSeq) if sampleSeq and sampleSeq not in ['?', '.'] else None

            #
            cObj = dataContainer.getObj(catName)
            epsObj = dataContainer.getObj('entity_poly_seq')
            eD = {}
            elD = {}
            for ii in range(epsObj.getRowCount()):
                entityId = epsObj.getValue('entity_id', ii)
                elD[entityId] = elD[entityId] + 1 if entityId in elD else 1
                if entityId not in eD:
                    eD[entityId] = {}
                compId = epsObj.getValue('mon_id', ii)
                eD[entityId][compId] = eD[entityId][compId] + 1 if compId in eD[entityId] else 1
                # seqNum = epsObj.getValue('num', ii)
                # hetFlag = epsObj.getValue('hetero', ii).upper()
            #
            #
            modMonD = {}
            ii = 0
            for entityId, cD in eD.items():
                modMonD[entityId] = []
                for compId, v in cD.items():
                    modFlag = 'N' if compId in DictMethodRunnerHelper.monDict3 else 'Y'
                    if modFlag == 'Y':
                        modMonD[entityId].append(compId)
                    cObj.setValue(ii + 1, "ordinal_id", ii)
                    cObj.setValue(entryId, "entry_id", ii)
                    cObj.setValue(entityId, "entity_id", ii)
                    cObj.setValue(compId, "comp_id", ii)
                    cObj.setValue(v, "chem_comp_count", ii)
                    cObj.setValue(elD[entityId], "entity_sequence_length", ii)
                    cObj.setValue(modFlag, "is_modified", ii)
                    #
                    idObj.setValue(ii + 1, "ordinal_id", ii)
                    idObj.setValue(entryId, "entry_id", ii)
                    idObj.setValue(entityId, "entity_id", ii)
                    idObj.setValue(compId, "comp_id", ii)
                    ii += 1
            #
            for atName in ['rcsb_mutation_count', 'rcsb_conflict_count', 'rcsb_insertion_count', 'rcsb_deletion_count',
                           'rcsb_sample_sequence_length', 'rcsb_non_std_monomer_count', 'rcsb_non_std_monomers']:
                if not epObj.hasAttribute(atName):
                    epObj.appendAttribute(atName)
            #
            for ii in range(epObj.getRowCount()):
                entityId = epObj.getValue('entity_id', ii)
                mutations = seqDifD[entityId]['mutations'] if entityId in seqDifD else 0
                conflicts = seqDifD[entityId]['conflicts'] if entityId in seqDifD else 0
                insertions = seqDifD[entityId]['insertions'] if entityId in seqDifD else 0
                deletions = seqDifD[entityId]['deletions'] if entityId in seqDifD else 0
                seqLen = sampleSeqLen[entityId] if entityId in sampleSeqLen else None
                epObj.setValue(mutations, 'rcsb_mutation_count', ii)
                epObj.setValue(conflicts, 'rcsb_conflict_count', ii)
                epObj.setValue(insertions, 'rcsb_insertion_count', ii)
                epObj.setValue(deletions, 'rcsb_deletion_count', ii)
                if seqLen is not None:
                    epObj.setValue(seqLen, 'rcsb_sample_sequence_length', ii)
                #
                numMod = len(modMonD[entityId])
                uModL = ','.join(set(modMonD[entityId])) if numMod else '?'
                epObj.setValue(numMod, 'rcsb_non_std_monomer_count', ii)
                epObj.setValue(uModL, 'rcsb_non_std_monomers', ii)

            return True
        except Exception as e:
            logger.exception("%s %s failing with %s" % (dataContainer.getName(), catName, str(e)))
        return False

    def buildEntityInstanceDomain(self, dataContainer, catName, **kwargs):
        """ Build category rcsb_entity_instance_domain ...

        Requires:
            _rcsb_entity_container_identifiers.entry_id
            _rcsb_entity_container_identifiers.entity_id
            _rcsb_entity_container_identifiers.asym_ids
            _rcsb_entity_container_identifiers.auth_asym_ids
            _rcsb_entity_container_identifiers.chem_comp_ligand,
            _rcsb_entity_container_identifiers.chem_comp_monomers
        ...

        Example:
            loop_
            _rcsb_entity_instance_domain.ordinal
            _rcsb_entity_instance_domain.domain_id
            _rcsb_entity_instance_domain.domain_name
            _rcsb_entity_instance_domain.domain_class_id
            _rcsb_entity_instance_domain.domain_class_name
            _rcsb_entity_instance_domain.domain_class_lineage_id
            _rcsb_entity_instance_domain.domain_class_lineage_name
            _rcsb_entity_instance_domain.domain_class_lineage_depth
            _rcsb_entity_instance_domain.domain_assigned_by
            _rcsb_entity_instance_domain.beg_auth_asym_id
            _rcsb_entity_instance_domain.beg_auth_seq_id
            _rcsb_entity_instance_domain.end_auth_asym_id
            _rcsb_entity_instance_domain.end_auth_seq_id
            1 4hrtA00 ? 1.10.490.10  Globins ? ? ? CATH    A 1  A 149


        And the CATH and SCOP variants for indexing -
            _rcsb_entity_instance_domain_cath.ordinal
            _rcsb_entity_instance_domain_cath.domain_id
            _rcsb_entity_instance_domain_cath.domain_name
            _rcsb_entity_instance_domain_cath.domain_class_id
            _rcsb_entity_instance_domain_cath.domain_class_name
            _rcsb_entity_instance_domain_cath.domain_class_lineage_id
            _rcsb_entity_instance_domain_cath.domain_class_lineage_name
            _rcsb_entity_instance_domain_cath.domain_class_lineage_depth
            _rcsb_entity_instance_domain_cath.domain_assigned_by
            _rcsb_entity_instance_domain_cath.domain_assigned_version
        """
        logger.debug("Starting with %r %r" % (dataContainer.getName(), catName))
        try:
            if catName != 'rcsb_entity_instance_domain':
                return False
            # Exit if source categories are missing
            if not (dataContainer.exists('rcsb_entity_container_identifiers') and dataContainer.exists('entry') and dataContainer.exists('pdbx_poly_seq_scheme')):
                return False
            #
            if not self.__scopU and self.__structDomainDataPath:
                self.__scopU = ScopClassificationUtils(scopDirPath=self.__structDomainDataPath, useCache=True)
            if not self.__cathU and self.__structDomainDataPath:
                self.__cathU = CathClassificationUtils(cathDirPath=self.__structDomainDataPath, useCache=True)
            if not self.__scopU and not self.__cathU:
                return False
            #
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['ordinal',
                                                                              'entry_id',
                                                                              'entity_id',
                                                                              'domain_id',
                                                                              'domain_name',
                                                                              'domain_class_id',
                                                                              'domain_class_name',
                                                                              'domain_class_lineage_id',
                                                                              'domain_class_lineage_name',
                                                                              'domain_class_lineage_depth',
                                                                              'domain_assigned_by',
                                                                              'domain_assigned_version',
                                                                              'beg_auth_asym_id',
                                                                              'beg_label_asym_id',
                                                                              'beg_auth_seq_id',
                                                                              'end_auth_asym_id',
                                                                              'end_label_asym_id',
                                                                              'end_auth_seq_id'
                                                                              ]))
            #
            if not dataContainer.exists('rcsb_entity_instance_domain_cath'):
                dataContainer.append(DataCategory('rcsb_entity_instance_domain_cath', attributeNameList=['ordinal',
                                                                                                         'entry_id',
                                                                                                         'entity_id',
                                                                                                         'domain_id',
                                                                                                         'domain_name',
                                                                                                         'domain_class_id',
                                                                                                         'domain_class_name',
                                                                                                         'domain_class_lineage_id',
                                                                                                         'domain_class_lineage_name',
                                                                                                         'domain_class_lineage_depth',
                                                                                                         'domain_assigned_by',
                                                                                                         'domain_assigned_version',
                                                                                                         'beg_auth_asym_id',
                                                                                                         'beg_label_asym_id',
                                                                                                         'beg_auth_seq_id',
                                                                                                         'end_auth_asym_id',
                                                                                                         'end_label_asym_id',
                                                                                                         'end_auth_seq_id'
                                                                                                         ]))
            if not dataContainer.exists('rcsb_entity_instance_domain_scop'):
                dataContainer.append(DataCategory('rcsb_entity_instance_domain_scop', attributeNameList=['ordinal',
                                                                                                         'entry_id',
                                                                                                         'entity_id',
                                                                                                         'domain_id',
                                                                                                         'domain_name',
                                                                                                         'domain_class_id',
                                                                                                         'domain_class_name',
                                                                                                         'domain_class_lineage_id',
                                                                                                         'domain_class_lineage_name',
                                                                                                         'domain_class_lineage_depth',
                                                                                                         'domain_assigned_by',
                                                                                                         'domain_assigned_version',
                                                                                                         'beg_auth_asym_id',
                                                                                                         'beg_label_asym_id',
                                                                                                         'beg_auth_seq_id',
                                                                                                         'end_auth_asym_id',
                                                                                                         'end_label_asym_id',
                                                                                                         'end_auth_seq_id'
                                                                                                         ]))

            eObj = dataContainer.getObj('entry')
            entryId = eObj.getValue('id', 0)
            #
            cObj = dataContainer.getObj(catName)
            psObj = dataContainer.getObj('pdbx_poly_seq_scheme')
            #
            asymD = {}
            authAsymD = {}
            if psObj is not None:
                for ii in range(psObj.getRowCount()):
                    asymId = psObj.getValue('asym_id', ii)
                    if asymId in asymD:
                        continue
                    entityId = psObj.getValue('entity_id', ii)
                    authAsymId = psObj.getValue('pdb_strand_id', ii)
                    asymD[asymId] = {'entry_id': entryId, 'entity_id': entityId, 'asym_id': asymId, 'auth_asym_id': authAsymId}
                    authAsymD[authAsymId] = asymId
                #
                logger.debug("authAsymD (%d) %r" % (len(authAsymD), authAsymD))
                logger.debug("asymD (%d) %r" % (len(asymD), asymD))
            #
            # Add CATH assignments
            cathObj = dataContainer.getObj('rcsb_entity_instance_domain_cath')
            scopObj = dataContainer.getObj('rcsb_entity_instance_domain_scop')
            #
            ii = cObj.getRowCount()
            kk = 0
            #
            for authAsymId in authAsymD:
                asymId = authAsymD[authAsymId]
                ad = asymD[asymId]
                entityId = ad['entity_id']
                dL = self.__cathU.getCathResidueRanges(entryId.lower(), authAsymId)
                vL = self.__cathU.getCathVersions(entryId.lower(), authAsymId)
                for (cathId, domId, tId, seqBeg, seqEnd) in dL:
                    logger.debug("entryId cathId %r domId %r asymId %r authAsymId %r seqBeg %r seqEnd %r" % (cathId, domId, authAsymId, authAsymD[authAsymId], seqBeg, seqEnd))
                    cObj.setValue(ii + 1, "ordinal", ii)
                    cObj.setValue(entryId, "entry_id", ii)
                    cObj.setValue(ad['entity_id'], "entity_id", ii)
                    #
                    cObj.setValue(str(domId), "domain_id", ii)
                    cObj.setValue(cathId, "domain_class_id", ii)
                    cObj.setValue(self.__cathU.getCathName(cathId), "domain_class_name", ii)
                    #
                    cObj.setValue(';'.join(self.__cathU.getNameLineage(cathId)), "domain_class_lineage_name", ii)
                    idLinL = self.__cathU.getIdLineage(cathId)
                    cObj.setValue(';'.join(idLinL), "domain_class_lineage_id", ii)
                    cObj.setValue(';'.join([str(jj) for jj in range(1, len(idLinL) + 1)]), "domain_class_lineage_depth", ii)
                    cObj.setValue(authAsymId, 'beg_auth_asym_id', ii)
                    cObj.setValue(asymId, 'beg_label_asym_id', ii)
                    cObj.setValue(seqBeg, 'beg_auth_seq_id', ii)
                    cObj.setValue(authAsymId, 'end_auth_asym_id', ii)
                    cObj.setValue(asymId, 'end_label_asym_id', ii)
                    cObj.setValue(seqEnd, 'end_auth_seq_id', ii)
                    cObj.setValue('CATH', 'domain_assigned_by', ii)
                    cObj.setValue(vL[0], 'domain_assigned_version', ii)
                    #
                    cathObj.setValue(kk + 1, "ordinal", kk)
                    cathObj.setValue(entryId, "entry_id", kk)
                    cathObj.setValue(ad['entity_id'], "entity_id", kk)
                    cathObj.setValue(str(domId), "domain_id", kk)
                    cathObj.setValue(cathId, "domain_class_id", kk)
                    cathObj.setValue(self.__cathU.getCathName(cathId), "domain_class_name", kk)
                    cathObj.setValue(';'.join(self.__cathU.getNameLineage(cathId)), "domain_class_lineage_name", kk)
                    cathObj.setValue(';'.join(idLinL), "domain_class_lineage_id", kk)
                    cathObj.setValue(';'.join([str(jj) for jj in range(1, len(idLinL) + 1)]), "domain_class_lineage_depth", kk)
                    cathObj.setValue(vL[0], 'domain_assigned_version', kk)
                    #
                    cathObj.setValue(authAsymId, 'beg_auth_asym_id', kk)
                    cathObj.setValue(asymId, 'beg_label_asym_id', kk)
                    cathObj.setValue(seqBeg, 'beg_auth_seq_id', kk)
                    cathObj.setValue(authAsymId, 'end_auth_asym_id', kk)
                    cathObj.setValue(asymId, 'end_label_asym_id', kk)
                    cathObj.setValue(seqEnd, 'end_auth_seq_id', kk)
                    cathObj.setValue('CATH', 'domain_assigned_by', kk)
                    cathObj.setValue(vL[0], 'domain_assigned_version', kk)
                    ii += 1
                    kk += 1

            # Add SCOP assignments
            kk = 0
            for authAsymId in authAsymD:
                asymId = authAsymD[authAsymId]
                ad = asymD[asymId]
                dL = self.__scopU.getScopResidueRanges(entryId.lower(), authAsymId)
                version = self.__scopU.getScopVersion(entryId.lower(), authAsymId)
                for (sunId, domId, sccs, tId, seqBeg, seqEnd) in dL:
                    logger.debug("sunId %r domId %r sccs %r asymId %r authAsymId %r  seqBeg %r seqEnd %r" % (sunId, domId, sccs, authAsymId, authAsymD[authAsymId], seqBeg, seqEnd))
                    cObj.setValue(ii + 1, "ordinal", ii)
                    cObj.setValue(entryId, "entry_id", ii)
                    cObj.setValue(ad['entity_id'], "entity_id", ii)
                    #
                    cObj.setValue(str(sunId), "domain_id", ii)
                    cObj.setValue(domId, "domain_class_id", ii)
                    cObj.setValue(self.__scopU.getScopName(sunId), "domain_class_name", ii)
                    #
                    tL = [t if t is not None else '' for t in self.__scopU.getNameLineage(sunId)]
                    cObj.setValue(';'.join(tL), "domain_class_lineage_name", ii)
                    idLinL = self.__scopU.getIdLineage(sunId)
                    cObj.setValue(';'.join([str(t) for t in idLinL]), "domain_class_lineage_id", ii)
                    cObj.setValue(';'.join([str(jj) for jj in range(1, len(idLinL) + 1)]), "domain_class_lineage_depth", ii)
                    #
                    cObj.setValue(authAsymId, 'beg_auth_asym_id', ii)
                    cObj.setValue(asymId, 'beg_label_asym_id', ii)
                    cObj.setValue(seqBeg, 'beg_auth_seq_id', ii)
                    cObj.setValue(authAsymId, 'end_auth_asym_id', ii)
                    cObj.setValue(asymId, 'end_label_asym_id', ii)
                    cObj.setValue(seqEnd, 'end_auth_seq_id', ii)
                    cObj.setValue('SCOPe', 'domain_assigned_by', ii)
                    cObj.setValue(version, 'domain_assigned_version', ii)
                    #
                    #
                    scopObj.setValue(kk + 1, "ordinal", kk)
                    scopObj.setValue(entryId, "entry_id", kk)
                    scopObj.setValue(ad['entity_id'], "entity_id", kk)
                    scopObj.setValue(str(sunId), "domain_id", kk)
                    scopObj.setValue(domId, "domain_class_id", kk)
                    scopObj.setValue(self.__scopU.getScopName(sunId), "domain_class_name", kk)
                    #
                    tL = [t if t is not None else '' for t in self.__scopU.getNameLineage(sunId)]
                    scopObj.setValue(';'.join(tL), "domain_class_lineage_name", kk)
                    scopObj.setValue(';'.join([str(t) for t in idLinL]), "domain_class_lineage_id", kk)
                    scopObj.setValue(';'.join([str(jj) for jj in range(1, len(idLinL) + 1)]), "domain_class_lineage_depth", kk)
                    scopObj.setValue(version, 'domain_assigned_version', kk)
                    scopObj.setValue(authAsymId, 'beg_auth_asym_id', kk)
                    scopObj.setValue(asymId, 'beg_label_asym_id', kk)
                    scopObj.setValue(seqBeg, 'beg_auth_seq_id', kk)
                    scopObj.setValue(authAsymId, 'end_auth_asym_id', kk)
                    scopObj.setValue(asymId, 'end_label_asym_id', kk)
                    scopObj.setValue(seqEnd, 'end_auth_seq_id', kk)
                    scopObj.setValue('SCOPe', 'domain_assigned_by', kk)
                    scopObj.setValue(version, 'domain_assigned_version', kk)
                    #
                    ii += 1
                    kk += 1

            return True
        except Exception as e:
            logger.exception("%s %s failing with %s" % (dataContainer.getName(), catName, str(e)))
        return False

    def filterEnumerations(self, dataContainer, catName, atName, **kwargs):
        """ Standardize the item value to conform to enumeration specifications.
        """
        subD = {('pdbx_reference_molecule', 'class'): [('Anti-tumor', 'Antitumor')]}
        try:
            if not dataContainer.exists(catName):
                return False
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                return False
            #
            subL = subD[(catName, atName)] if (catName, atName) in subD else []
            #
            for ii in range(cObj.getRowCount()):
                tV = cObj.getValue(atName, ii)
                if tV and tV not in ['.', '?']:
                    for sub in subL:
                        if sub[0] in tV:
                            tV = tV.replace(sub[0], sub[1])
                            cObj.setValue(tV, atName, ii)
            return True
        except Exception as e:
            logger.exception("%s %s %s failing with %s" % (dataContainer.getName(), catName, atName, str(e)))
        return False

    def deferredItemMethod(self, dataContainer, catName, atName, **kwargs):
        """ Placeholder method to
        """
        logger.debug("Called deferred method for %r %r %r" % (dataContainer.getName(), catName, atName))
        return True

    def __getTimeStamp(self):
        utcnow = datetime.datetime.utcnow()
        ts = utcnow.strftime("%Y-%m-%d:%H:%M:%S")
        return ts

    def __stripWhiteSpace(self, val):
        """ Remove all white space from the input value.

        """
        if val is None:
            return val
        return self.__wsPattern.sub("", val)
