from pandas import read_excel, DataFrame


class Task_Menu:
    def __init__(self) -> None:
    
        excel_data = read_excel('tgbot\data_base\\Bd.xlsx', index_col=0, header=1)
        self.data = DataFrame(excel_data)
        self.data= self.data.astype(str)
        
        self.temp = self.data.iloc[0:,0:2]
        self.vol = self.data.iloc[0:,2:4]
        self.grade = self.data.iloc[0:,4:7]
        self.taste = self.data.iloc[0:,7:15]
        self.aroma1 = self.data.iloc[0:,15:23]
        self.aroma2 = self.data.iloc[0:,23:31]
        self.glass = self.data.iloc[0:,32:38]
        self.price = self.data.iloc[0:,31]
        self.comp = self.data.iloc[0:,38]
        self.descr = self.data.iloc[0:,39]
        self.photo = self.data.iloc[0:,40]
        
    def put_columns(self,data:DataFrame):
        return data.columns

ee = Task_Menu()
