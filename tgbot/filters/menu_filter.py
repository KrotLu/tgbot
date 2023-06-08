from aiogram.dispatcher.filters.state import State, StatesGroup

class Menu_states(StatesGroup):
    Q1_Temp=State()
    Q2_Vol=State()
    Q3_Grade=State()
    Q4_Taste=State()
    Q5_Aroma1=State()
    Q6_Aroma2=State()
    Q7_Fin=State()