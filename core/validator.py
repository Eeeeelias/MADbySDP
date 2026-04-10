REQUIRED_COLUMNS = [
    'Site',
    'Tt.BMD',
    'Tt.Ar',
    'Tb.BMD',
    'BV/TV',
    'Tb.N',
    'Tb.Th',
    'Tb.Sp',
    'Tb.1/N.SD',
    'Tb.Ar',
    'Ct.BMD',
    'Ct.Th',
    'Ct.Po',
    'Ct.Po.Dm',
    'Ct.Pm',
    'Ct.Ar'
]

COL_MAP_XCT1 = {'tTb.1/N.SD1': 'Tb.1/N.SD',
                'tTb.Sp1': 'Tb.Sp',
                'tTb.Th1': 'Tb.Th',
                'tTb.N1': 'Tb.N',
                'TrabArea1': 'Tb.Ar',
                'CortArea1': 'Ct.Ar',
                'tBV/TV1': 'BV/TV',
                'Ct.Pm1': 'Ct.Pm',
                'Ct.Th1': 'Ct.Th',
                'D100-1': 'Tt.BMD',
                'Tt.Ar1': 'Tt.Ar',
                'Dtrab1': 'Tb.BMD',
                'Dcomp1': 'Ct.BMD',
                }

COL_MAP_XCT2 = {'Tb.1/N.SD1': 'Tb.1/N.SD',
           'Tb.Sp1': 'Tb.Sp',
           'Tb.Th1': 'Tb.Th',
           'Tb.N1': 'Tb.N',
           'Tb.Ar1': 'Tb.Ar',
           'Tb.BV/TV1': 'BV/TV',
           'Ct.Pm1': 'Ct.Pm',
           'Ct.Th1': 'Ct.Th',
           'Ct.Ar1': 'Ct.Ar',
           'Tot.vBMD1': 'Tt.BMD',
           'Tb.vBMD1': 'Tb.BMD',
           'Ct.vBMD1': 'Ct.BMD',
           'Ct.Po1': 'Ct.Po',
           'Ct.Po.Dm1': 'Ct.Po.Dm',
           'Tt.Ar1': 'Tt.Ar',
           }


def validate_dataframe(df, xct_gen):
    missing = []

    if xct_gen == 0:
        return ['XCT generation']

    for col in REQUIRED_COLUMNS:
        if col not in df.columns and COL_MAP_XCT1.get(col) not in df.columns:
            if xct_gen == 1 and (col == 'Ct.Po' or col == 'Ct.Po.Dm'):
                continue
            missing.append(col)
    return missing
