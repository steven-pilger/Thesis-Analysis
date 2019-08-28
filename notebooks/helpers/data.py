def get_interactions(interactions):
    d = []
    last_int_id = None
    append = d.append
    for i in interactions:
        int_id = i.interacting_pair

        if last_int_id is None:        
            r = {}
            r['int_ty'] = set()
            last_int_id = int_id

        r['int_ty'].update([i.interaction_type])
        r['pdb_id'] = i.interacting_pair.referenced_structure.pdb_code.index
        r['gprot'] = i.interacting_pair.referenced_structure.signprot_complex.protein.entry_name
        r['entry_name'] = i.interacting_pair.referenced_structure.protein_conformation.protein.entry_name

        r['rec_aa'] = i.interacting_pair.res1.amino_acid
        r['rec_pos'] = i.interacting_pair.res1.sequence_number
        r['rec_gn'] = i.interacting_pair.res1.display_generic_number.label

        r['sig_aa'] = i.interacting_pair.res2.amino_acid
        r['sig_pos'] = i.interacting_pair.res2.sequence_number
        r['sig_gn'] = i.interacting_pair.res2.display_generic_number.label

        if last_int_id != int_id:
            append(r)
            last_int_id = None
            
    return d