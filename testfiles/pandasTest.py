import pandas

data = pandas.read_csv('exampleData.csv',names=['Title', 'Value'], index_col=0)
# print(data)
# print(data.loc['First', 'Value'])

dataDict = data.to_dict('index')
print(dataDict)