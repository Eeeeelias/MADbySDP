import pickle

from openpyxl.formatting.rule import CellIsRule
from openpyxl.reader.excel import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

from core.resources import resource_path

PRED_COLS = ['Tt.BMD', 'Tt.Ar', 'Tb.BMD', 'BV/TV', 'Tb.N', 'Tb.Th', 'Tb.Sp', 'Tb.1/N.SD',
             'Tb.Ar', 'Ct.BMD', 'Ct.Th', 'Ct.Po', 'Ct.Po.Dm', 'Ct.Pm', 'Ct.Ar']

def load_scaler(xct_gen):
    scalers = {}
    radius_path = resource_path(f"models/radius_XCT{xct_gen}_scaler.pkl")
    with open(radius_path, 'rb') as f:
        scalers['radius'] = pickle.load(f)

    tibia_path = resource_path(f"models/tibia_XCT{xct_gen}_scaler.pkl")
    with open(tibia_path, 'rb') as f:
        scalers['tibia'] = pickle.load(f)
    return scalers

def load_model(xct_gen, model_type):
    machine = "old" if xct_gen == 1 else "new"
    weighted = "_balanced" if model_type == "balanced" else ""

    models = {}

    radius_path = resource_path(f"models/radius_{machine}{weighted}_model.pkl")
    with open(radius_path, 'rb') as f:
        models['radius'] = pickle.load(f)

    tibia_path = resource_path(f"models/tibia_{machine}{weighted}_model.pkl")
    with open(tibia_path, 'rb') as f:
        models['tibia'] = pickle.load(f)

    return models

def conformal_marking(output_path, dataframe, highlight):

    # get the cell range
    confidence_col_index = dataframe.columns.get_loc("Confidence") + 1
    confidence_col_letter = get_column_letter(confidence_col_index)
    max_row = len(dataframe)+1
    cell_range = f"{confidence_col_letter}2:{confidence_col_letter}{max_row}"

    # process the workbook
    wb = load_workbook(output_path)
    ws = wb.active

    red_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
    yellow_fill = PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')

    if "85th" in highlight:
        ws.conditional_formatting.add(cell_range,
                                      CellIsRule(operator="lessThan", formula=["0.61"], fill=red_fill))
    if "95th" in highlight:
        ws.conditional_formatting.add(cell_range,
                                      CellIsRule(operator="between", formula=["0.61", "0.8"], fill=yellow_fill))

    wb.save(output_path)

def run_processing(dataframe, model_type, xct_gen, conformal, output_path):

    # remove XCT2 specific columns from pred_cols if not needed
    selected_cols = PRED_COLS.copy()
    if xct_gen == 1:
        selected_cols.remove('Ct.Po')
        selected_cols.remove('Ct.Po.Dm')

    # load needed models
    scalers = load_scaler(xct_gen)
    models = load_model(xct_gen, model_type)

    output_preds = []
    output_probs = []

    for _, row in dataframe.iterrows():
        if row['Site'].startswith('R'):
            site = 'radius'
        elif row['Site'].startswith('T'):
            site = 'tibia'
        else:
            raise Exception(f"Unknown site {row['Site']}: Make sure Site column indicates Radius (R) or Tibia (T).")

        values = [row[selected_cols].tolist()]
        values_transformed = scalers[site].transform(values)
        prediction = models[site].predict(values_transformed)
        prediction_prob = models[site].predict_proba(values_transformed)

        output_preds.append("pass" if prediction[0] == 0 else "fail")
        output_probs.append(round(max(prediction_prob[0]), 3))

    dataframe['Grading'] = output_preds
    dataframe['Confidence'] = output_probs

    dataframe.to_excel(output_path, index=False)

    if len(conformal) > 0:
        conformal_marking(output_path, dataframe, conformal)

    return
