class DebtRecord:
    __slots__ = ("__DebtID","__Debt")
    def __init__(self,debtID,debt):
        self.__DebtID = debtID
        self.__Debt = debt
    @property
    def debt(self):
        return self.__Debt
    @property
    def debtID(self):
        return self.__DebtID
    def setDebt(self,debt):
        try:
            debt = int(debt)
            if debt < 0:
                return False
            self.__Debt = debt
            return True
        except ValueError:
            return False
    
        