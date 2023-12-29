import kivy
import kivymd
from kivy.app import App
from kivy.uix.pagelayout import PageLayout
from kivy.properties import NumericProperty
from kivymd.uix.button import MDRoundFlatButton, MDRaisedButton
from sqlalchemy import func, Table, Column, Integer, ForeignKey, String, CHAR, Float, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_, or_
import random as rd
import math as m

engine = create_engine("sqlite:///My_new_Data.db", echo=False) 
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Test(Base):
    __tablename__ = "Test"
    id = Column(Integer, primary_key=True)
    b1 = Column(Float)
    b2 = Column(String)
    b3 = Column(Integer)
    b4 = Column(Integer)
    b5 = Column(Integer)
    b6 = Column(Integer)
    b7 = Column(Integer)
    b8 = Column(Integer)
    b9 = Column(Integer)

    def __init__(self, b1, b2, b3, b4, b5, b6, b7, b8, b9):
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.b4 = b4
        self.b5 = b5
        self.b6 = b6
        self.b7 = b7
        self.b8 = b8
        self.b9 = b9

class CustomButton(MDRoundFlatButton):

    btn_id = NumericProperty(0)

    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
    

class main_logic(PageLayout):

    def __init__(self, **kwargs):
        super(main_logic, self).__init__(**kwargs)
    
    def increment_counter(self,btn):
        btn.text = str(int(btn.text[0]) + 1)
    
    def increment_counter_test_random(self):
        self.ids.b1.text = str(rd.randint(0,100))

    def increment_counter_test_math(self):
        self.ids.b1.text = str(m.sqrt(int(self.ids.b1.text)))

    def increment_counter_test_sympy(self):
        self.ids.b2.text = f"{int(self.ids.b2.text)}/{int(self.ids.b3.text)}"

    def safe(self):
        s = Session()
        s.query(Test).update(
            {"b1":float(self.ids.b1.text),
             "b2":str(self.ids.b2.text),
             "b3":int(self.ids.b3.text),
             "b4":int(self.ids.b4.text),
             "b5":int(self.ids.b5.text),
             "b6":int(self.ids.b6.text),
             "b7":int(self.ids.b7.text),
             "b8":int(self.ids.b8.text),
             "b9":int(self.ids.b9.text)})
        s.commit()
        s.close()


    def load_data_from_database(self):
        session = Session()
        d = session.query(Test).first()
        session.close()
        if d:
            self.ids.b1.text = str(d.b1)
            self.ids.b2.text = str(d.b2)
            self.ids.b3.text = str(d.b3)
            self.ids.b4.text = str(d.b4)
            self.ids.b5.text = str(d.b5)
            self.ids.b6.text = str(d.b6)
            self.ids.b7.text = str(d.b7)
            self.ids.b8.text = str(d.b8)
            self.ids.b9.text = str(d.b9)
        else:
            d = Test(1,1,1,1,1,1,1,1,1)
            session.add(d)
            session.commit()
            session.close()

class mainapp(App):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return main_logic()
    
    def on_start(self):
        Base.metadata.create_all(engine)
        self.root.load_data_from_database()
if __name__ == "__main__":
    mainapp().run()
