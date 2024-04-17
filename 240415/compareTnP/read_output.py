import pandas as pd

path = '/u/user/sjws5411/Workspace/Efficiency/CMSSW_14_1_0_pre2/src/Workspace-RPC/240415/compareTnP/data/count/run-316187.csv'
data = pd.read_csv(path, index_col=False)
print(data)

print(data.denominator.sum())
print(data.numerator.sum())

