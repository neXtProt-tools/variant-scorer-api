WEIGHTS = {
    'NX_P00533': {
        'features': {
            'interaction-mapping': 1,
            'topological-domain': 0,
            'miscellaneous-region': 1,
            'variant': 0,
            'domain': 1,
            'binding-site': 2,
            'modified-residue': 2,
            'repeat': 0,
            'disulfide-bond': 2,
            'cross-link': 2,
            'transmembrane-region': 0,
            'active-site': 2,
            'signal-peptide': 1,
            'glycosylation-site': 1,
            'sequence-conflict': 0,
            'lipidation-site': 2,
            'site': 2
        },
        'mutagenesis': {
            'Mutagenesis -- Strongly reduced autophosphorylation and activation of downstream kinases': 1,
            'Mutagenesis -- Abolishes autophosphorylation and activation of downstream kinases': 1,
            'Mutagenesis -- Decreases intramolecular interactions and facilitates EGF binding': 1,
            'Mutagenesis -- Strongly reduced phosphorylation': 1,
            'Mutagenesis -- Reduced autophosphorylation': 1,
            'Mutagenesis -- Constitutively activated kinase': 1,
            'Mutagenesis -- Reduced phosphorylation': 1,
            'Mutagenesis -- Increased phosphorylation': 1,
            'Mutagenesis -- Abolishes phosphorylation': 1,
            'Mutagenesis -- Abolishes kinase activity': 1,
            'Mutagenesis -- Abolishes palmitoylation': 1,
            'Mutagenesis -- Decreased palmitoylation': 1,
            'Mutagenesis -- Strongly decreases interaction with CBLC': 1,
            'Mutagenesis -- Abolishes interaction with CBLC': 1,
            'Mutagenesis -- No effect on interaction with CBLC': -1,
            'Mutagenesis -- No change in interaction with PIK3C2B, 65% decrease in interaction with PIK3C2B; when associated with F-1016, Abolishes interaction with PIK3C2B; when associated with F-1092 and F-1016': -1,
            'Mutagenesis -- Increased EGF binding': 0
        },
        'vep': {
            'Deleterious and probably damaging': 1,
            'Deleterious and possibly damaging': 0.5,
            'Deleterious_low_confidence and probably damaging': 0.5,
            'Tolerated_low_confidence and probably damaging': 0.5,
            'Deleterious_low_confidence and possibly damaging': 0,
            'Tolerated_low_confidence and possibly damaging': 0,
            'Tolerated and probably damaging': 0,
            'Deleterious and bening': 0,
            'Deleterious_low_confidence and bening': -0.5,
            'Tolerated_low_confidence and bening': -0.5,
            'Tolerated and possibly damaging': -0.5,
            'Tolerated and bening': -1
        }
    },
    'NX_Q92560': {
        'features': {
            'interaction-mapping': 1,
            'modified-residue': 1,
            'glycosylation-site': 2,
            'lipidation-site': 2,
            'binding-site': 2,
            'site': 2,
            'active-site': 2
        },
        'mutagenesis': {

        }
    },
    'NX_P35240': {
        'features': {
            'domain': 1,
            'modified-residue': 1,
        },
        'mutagenesis': {

        },
    }
}


def get_weights_by_entry(entry):
    if entry in WEIGHTS:
        return WEIGHTS[entry]
    return None