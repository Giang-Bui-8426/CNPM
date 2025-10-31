class DebtRecord:
    __slots__ = ("__DebtID","__Debt")
    def __init__(self,DebtID,Debt):
        self.__DebtID = DebtID
        self.__Debt = Debt
    @property
    def getDebt(self):
        return self.__Debt
    @property
    def getDebtID(self):
        return self.__DebtID
    def setDebt(self,debt):
        if debt < 0:
            return False
        self.__Debt = debt
        return True
    
        