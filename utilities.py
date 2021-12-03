import pandas as pd
def highlight_greaterthan(s, threshold, column):
    is_max = pd.Series(data=False, index=s.index)
    is_min = pd.Series(data=False, index=s.index)
    is_max[column] = s.loc[column] >= 80
    is_min[column] = s.loc[column] < 50
    for v in is_max:
        if is_max.any():
            return ["background-color: green"]
        elif is_min.any():
            return ["background-color: red"]
        else:
            return ["background-color: orange"]
    #return ['background-color: green' if is_max.any() elif is_min.any() "background-color:red" else 'background-color:orange' for v in is_max]