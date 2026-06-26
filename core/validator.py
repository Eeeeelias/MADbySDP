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

COL_MAP_XCT1 = {'tb.1/n.sd': 'tTb.1/N.SD1',
                'tb.sp': 'tTb.Sp1',
                'tb.th': 'tTb.Th1',
                'tb.n': 'tTb.N1',
                'tb.ar': 'TrabArea1',
                'ct.ar': 'CortArea1',
                'bv/tv': 'tBV/TV1',
                'ct.pm': 'Ct.Pm1',
                'ct.th': 'Ct.Th1',
                'tt.bmd': 'D100-1',
                'tt.ar': 'Tt.Ar1',
                'tb.bmd': 'Dtrab1',
                'ct.bmd': 'Dcomp1',
}

COL_MAP_XCT2 = {'tb.1/n.sd': 'Tb.1/N.SD1',
                'tb.sp': 'Tb.Sp1',
                'tb.th': 'Tb.Th1',
                'tb.n': 'Tb.N1',
                'tb.ar': 'Tb.Ar1',
                'bv/tv': 'Tb.BV/TV1',
                'ct.pm': 'Ct.Pm1',
                'ct.th': 'Ct.Th1',
                'ct.ar': 'Ct.Ar1',
                'tt.bmd': 'Tot.vBMD1',
                'tb.bmd': 'Tb.vBMD1',
                'ct.bmd': 'Ct.vBMD1',
                'ct.po': 'Ct.Po1',
                'ct.po.dm': 'Ct.Po.Dm1',
                'tt.ar': 'Tt.Ar1',
}

def validate_dataframe(df, xct_gen):
    missing = []

    if xct_gen == 0:
        return ['XCT generation']

    lower_cols = df.columns.str.lower()

    for col in REQUIRED_COLUMNS:
        if col.lower() not in lower_cols and  \
            COL_MAP_XCT1.get(col.lower(), "").lower() not in lower_cols and \
            COL_MAP_XCT2.get(col.lower(), "").lower() not in lower_cols:
            if xct_gen == 1 and (col == 'Ct.Po' or col == 'Ct.Po.Dm'):
                continue
            missing.append(col)
    return missing
