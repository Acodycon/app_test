import kivy
import kivymd
import sqlalchemy
import random as rd
import math as m
import os


from kivy.config import Config
from sqlalchemy import func, Table, Column, Integer, ForeignKey, String, CHAR, Float, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_, or_
from calorie_calculator import compute_BMR, compute_TDEE
from CKC import *

from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle, SmoothLine
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.widget import MDWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.pagelayout import PageLayout
from kivymd.uix.toolbar import MDTopAppBar, MDBottomAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.list import MDList
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.list import ThreeLineIconListItem
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.list import IconRightWidget
from kivymd.uix.list import OneLineAvatarIconListItem, ThreeLineAvatarIconListItem, IRightBodyTouch
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDIconButton, MDRectangleFlatButton, MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.dialog import MDDialog
from kivymd.uix.widget import Widget
from kivymd.uix.floatlayout import MDFloatLayout

app_path = os.path.dirname(os.path.abspath(__file__))
print(app_path)
db_path = os.path.join(app_path, 'Data_Base.db')
print(db_path)

engine = create_engine('sqlite:///' + db_path, echo=False, pool_pre_ping=True) 
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Active(Base):
    __tablename__ = "active"
    id = Column(Integer,primary_key=True)
    settings_id = Column(String)
    meal_plan_id = Column(Integer)

    def __init__(self,settings_id, meal_plan_id):
        self.settings_id = settings_id # is currently the method for searching for the active settings object should be converted to use id instead !!!
        self.meal_plan_id = meal_plan_id

class Meal_Plan(Base):
    __tablename__ = "meal_plan"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    breakfast = Column(Boolean)
    breakfast_percentage = Column(Integer)
    lunch = Column(Boolean)
    lunch_percentage = Column(Integer)
    dinner = Column(Boolean)
    dinner_percentage = Column(Integer)
    snack = Column(Boolean)
    snack_percentage = Column(Integer)
    day_range = Column(Integer)
    meal_id_and_ingredient_id__unit__amount_list = Column(String)
    shopping_list = Column(String)
    adjusted = Column(Boolean)

    def init(self, name, breakfast, breakfast_percentage, lunch, lunch_percentage, dinner, dinner_percentage, snack, snack_percentage, day_range, meal_id_and_ingredient_id__unit__amount_list, shopping_list, adjusted):
        self.name = name
        self.breakfast = breakfast
        self.breakfast_percentage = breakfast_percentage
        self.lunch = lunch
        self.lunch_percentage = lunch_percentage
        self.dinner = dinner
        self.dinner_percentage = dinner_percentage
        self.snack = snack
        self.snack_percentage = snack_percentage
        self.day_range  = day_range
        self.meal_id_and_ingredient_id__unit__amount_list = meal_id_and_ingredient_id__unit__amount_list
        self.shopping_list = shopping_list
        self.adjusted = adjusted

class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    gender = Column(String)
    weight = Column(Float)
    height = Column(Float)
    age = Column(Integer)
    activity = Column(String)
    weight_gain_goal = Column(String)
    calories_per_day = Column(Float)

    def __init__(self,name,gender,weight,height,age,activity,weight_gain_goal,calories_per_day):
        self.name = name
        self.gender = gender
        self.weight = weight
        self.height = height
        self.age = age
        self.activity = activity
        self.weight_gain_goal = weight_gain_goal
        self.calories_per_day = calories_per_day

class Association(Base):
    __tablename__ = 'meal_ingredients'
    id = Column(Integer,primary_key=True)
    meal_id = Column(Integer, ForeignKey('meals.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    amount_numerator = Column(Integer)
    amount_denominator = Column(Integer)
    ingredient = relationship("Ingredient", back_populates="meals")
    meal = relationship("Meal", back_populates="ingredients")

    def __init__(self,meal,ingredient,amount_numerator,amount_denominator):
        self.meal = meal
        self.ingredient = ingredient
        self.amount_numerator = amount_numerator
        self.amount_denominator = amount_denominator

class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ingredients = relationship("Association", back_populates="meal")
    breakfast = Column(Boolean)
    lunch = Column(Boolean)
    dinner = Column(Boolean)
    snack = Column(Boolean)
    hot_cold = Column(Boolean)
    sweet_savory = Column(Boolean)

    def __init__(self, name, breakfast:bool, lunch:bool, dinner:bool, snack:bool, hot_cold:bool, sweet_savory:bool):
        self.name = name
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner
        self.snack = snack
        self.hot_cold = hot_cold
        self.sweet_savory = sweet_savory
     
    def __repr__(self):
        return self.name

    @property
    def calories(self):
        return sum([i.ingredient.calories * i.amount_numerator / i.amount_denominator  for i in self.ingredients])
    @property
    def carbohydrates(self):
        return sum([i.ingredient.carbohydrates * i.amount_numerator / i.amount_denominator for i in self.ingredients])
    @property
    def fats(self):
        return sum([i.ingredient.fats * i.amount_numerator / i.amount_denominator for i in self.ingredients])
    @property
    def proteins(self):
        return sum([i.ingredient.proteins * i.amount_numerator / i.amount_denominator for i in self.ingredients])

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit = Column(String)
    snack = Column(Boolean)
    type = Column(String)
    calories = Column(Float)
    carbohydrates = Column(Float)
    fats = Column(Float)
    proteins = Column(Float)
    divisible_by = Column(Integer)
    meals = relationship("Association", back_populates="ingredient")

    def __init__(self, name, unit, snack, type, calories, carbohydrates, fats, proteins, divisible_by):
        self.unit = unit
        self.snack = snack
        self.type = type
        self.name = name
        self.calories = calories
        self.carbohydrates = carbohydrates
        self.fats = fats
        self.proteins = proteins
        self.divisible_by = divisible_by if divisible_by else False

    def __repr__(self):
        return self.name

class Settings_Screen(MDScreen):

    def __init__(self, *args, **kwargs):
        super(Settings_Screen,self).__init__(*args, **kwargs)
        self.icon_dict = {
            "Male":"gender-male",
            "Female":"gender-female",
            "1.0":"cancel",
            "1.2":"walk",
            "1.375":"dumbbell",
            "1.725":"weight-lifter",
            "1.9":"weight",
            "-1100.0":"arrow-down-bold-circle",
            "-550.0":"arrow-down-bold-circle-outline",
            "-275.0":"arrow-down-bold-outline",
            "0.0":"checkbox-blank-circle-outline",
            "275.0":"arrow-up-bold-outline",
            "550.0":"arrow-up-bold-circle-outline",
            "1100.0":"arrow-up-bold-circle"
        }
        s = Session()
        self.active_settings_id = s.query(Active).first().settings_id
        s.close()

    def transition_to_meal_plan_screen(self):
        MDApp.get_running_app().root.ids.screen_manager.current = "Meal_Plan_Screen"
        MDApp.get_running_app().root.ids.screen_manager.transition.direction = "right"
        MDApp.get_running_app().root.load_active_profile()

    def open_gender_dropdown(self):
        self.choices_gender = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "Male",
                "icon": "gender-male",
                "height": dp(56),
                "on_release": lambda x="gender-male",y="Male": self.set_gender_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Female",
                "icon": "gender-female",
                "height": dp(56),
                "on_release": lambda x="gender-female",y="Female": self.set_gender_icon(x,y)
            }
        ]
        self.menu_list_gender = MDDropdownMenu(
            caller=self.ids.gender_input,
            items=self.choices_gender,
            position="auto",
            width_mult=4
        )
        self.menu_list_gender.open()

    def set_gender_icon(self, icon, text):
        self.ids.gender_input.text = text
        self.ids.gender_input.icon = icon
        self.menu_list_gender.dismiss()
        self.open_activity_dropdown() if not self.active_settings_id else None
        self.display_BMR()
        self.display_TDEE()
        self.display_cals_per_day()
    
    def open_activity_dropdown(self):
        self.choices_activity = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "Sedentary",
                "icon": "cancel",
                "height": dp(56),
                "on_release": lambda x="cancel",y=1: self.set_activity_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Lightly Active",
                "icon": "walk",
                "height": dp(56),
                "on_release": lambda x="walk",y=1.2: self.set_activity_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Moderately Active",
                "icon": "dumbbell",
                "height": dp(56),
                "on_release": lambda x="dumbbell",y=1.375: self.set_activity_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Very Active",
                "icon": "weight-lifter",
                "height": dp(56),
                "on_release": lambda x="weight-lifter",y=1.725: self.set_activity_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Extremely Active",
                "icon": "weight",
                "height": dp(56),
                "on_release": lambda x="weight",y=1.9: self.set_activity_icon(x,y)
            }
        ]
        self.menu_list_activity = MDDropdownMenu(
            caller=self.ids.activity_input,
            items=self.choices_activity,
            position="auto",
            width_mult=4
        )
        self.menu_list_activity.open()
    
    def set_activity_icon(self, icon, text):
        self.ids.activity_input.text = text
        self.ids.activity_input.icon = icon
        self.menu_list_activity.dismiss()
        self.open_weightgain_dropdown() if not self.active_settings_id else None
        self.display_BMR()
        self.display_TDEE()
        self.display_cals_per_day()
    
    def open_weightgain_dropdown(self):
        self.choices_weightgain = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "- 1 kg/week",
                "icon": "arrow-down-bold-circle",
                "height": dp(56),
                "on_release": lambda x="arrow-down-bold-circle",y=-1100: self.set_weightgain_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "- 1/2 kg/week",
                "icon": "arrow-down-bold-circle-outline",
                "height": dp(56),
                "on_release": lambda x="arrow-down-bold-circle-outline",y=-550: self.set_weightgain_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "- 1/4 kg/week",
                "icon": "arrow-down-bold-outline",
                "height": dp(56),
                "on_release": lambda x="arrow-down-bold-outline",y=-275: self.set_weightgain_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Maintain",
                "icon": "checkbox-blank-circle-outline",
                "height": dp(56),
                "on_release": lambda x="checkbox-blank-circle-outline",y=0: self.set_weightgain_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "+ 1/4 kg/week",
                "icon": "arrow-up-bold-outline",
                "height": dp(56),
                "on_release": lambda x="arrow-up-bold-outline",y=275: self.set_weightgain_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "+ 1/2 kg/week",
                "icon": "arrow-up-bold-circle-outline",
                "height": dp(56),
                "on_release": lambda x="arrow-up-bold-circle-outline",y=550: self.set_weightgain_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "+ 1 kg/week",
                "icon": "arrow-up-bold-circle",
                "height": dp(56),
                "on_release": lambda x="arrow-up-bold-circle",y=1100: self.set_weightgain_icon(x,y)
            }
        ]
        self.menu_list_weightgain = MDDropdownMenu(
            caller=self.ids.weight_gain_input,
            items=self.choices_weightgain,
            position="auto",
            width_mult=4
        )
        self.menu_list_weightgain.open()
    
    def set_weightgain_icon(self, icon, text):
        self.ids.weight_gain_input.text = text
        self.ids.weight_gain_input.icon = icon
        self.menu_list_weightgain.dismiss()
        self.ids.weight_input.focus = True if not self.active_settings_id else False
        self.display_cals_per_day()

    def display_BMR(self):
        gender = self.ids.gender_input.text if self.ids.gender_input.icon != "close" else False
        weight = float(self.ids.weight_input.text) if self.ids.weight_input.text else False
        height = float(self.ids.height_input.text) if self.ids.height_input.text else False
        age  = float(self.ids.age_input.text) if self.ids.age_input.text else False
        if all ([gender,weight,height,age]) and gender != "Choose":
            self.ids.bmr.text = str(round(compute_BMR(gender,weight,height,age),2))
    
    def display_TDEE(self):
        activity = float(self.ids.activity_input.text) if self.ids.activity_input.icon != "close" else False
        BMR = float(self.ids.bmr.text) if self.ids.bmr.text else False
        if all([activity,BMR]) and self.ids.activity_input.icon != "close":
            self.ids.tdee.text = str(round(compute_TDEE(BMR,activity),2))
    
    def display_cals_per_day(self):
        TDEE = float(self.ids.tdee.text) if self.ids.tdee.text else False
        WG = float(self.ids.weight_gain_input.text) if self.ids.weight_gain_input.icon != "close" else False
        if TDEE and self.ids.weight_gain_input.icon != "close":
            cpd = round(float(TDEE) + float(WG),2)
            self.ids.calories_per_day.text = str(cpd)
    ## no support for multiple settings profiles
    def save_settings(self):
        if all([self.ids.profile_name_input.text,
                self.ids.gender_input.text,
                self.ids.weight_input.text,
                self.ids.height_input.text,
                self.ids.age_input.text,
                self.ids.activity_input.text,
                self.ids.calories_per_day.text]) and self.ids.weight_gain_input.icon != "close":
            s = Session()
            settings_query = s.query(Settings).filter(Settings.name == self.ids.profile_name_input.text).first()
            if not settings_query:
                new_setting = Settings(
                    name=self.ids.profile_name_input.text,
                    gender=self.ids.gender_input.text,
                    weight=float(self.ids.weight_input.text),
                    height=float(self.ids.height_input.text),
                    age=float(self.ids.age_input.text),
                    activity=float(self.ids.activity_input.text),
                    weight_gain_goal=float(self.ids.weight_gain_input.text),
                    calories_per_day=float(self.ids.calories_per_day.text))
                s.add(new_setting)
                s.commit()
                s.query(Active).first().settings_id = new_setting.id
                self.active_settings_id = new_setting.id
                s.commit()
                s.close()
            else:
                s.close()
                c = Settings_Already_Exist_Dialog()
                self.settings_already_exist_dialog = MDDialog(
                    title="Profile already exists, would you like to overwrite?",
                    type="custom",
                    size_hint=(0.9,None),
                    content_cls=c,
                    radius=[20, 7, 20, 7]
                )
                c.settings_already_exist_dialog = self.settings_already_exist_dialog
                c.settings_screen = self
                self.settings_already_exist_dialog.open()
        else:
            pass # ("Please fill out all fields") Add Info Popup
    
    def update_settings(self): # is expected to only be called from save settings function with all fields filled
        s = Session()
        s.query(Settings).filter(Settings.id == self.active_settings_id).update({
            Settings.name: self.ids.profile_name_input.text,
            Settings.gender: self.ids.gender_input.text,
            Settings.weight: float(self.ids.weight_input.text),
            Settings.height: float(self.ids.height_input.text),
            Settings.age: float(self.ids.age_input.text),
            Settings.activity: float(self.ids.activity_input.text),
            Settings.weight_gain_goal: float(self.ids.weight_gain_input.text),
            Settings.calories_per_day: float(self.ids.calories_per_day.text)
            })
        s.commit()
        s.close()

    def load_active_settings(self):
        s = Session()
        self.active_settings_id = s.query(Active).first().settings_id
        s.close()
        if self.active_settings_id:
            s = Session()
            active_settings = s.query(Settings).get(self.active_settings_id)
            self.ids.profile_name_input.text = active_settings.name
            self.ids.gender_input.icon = self.icon_dict[active_settings.gender]
            self.ids.gender_input.text = active_settings.gender
            self.ids.weight_input.text = str(active_settings.weight)
            self.ids.height_input.text = str(active_settings.height)
            self.ids.age_input.text = str(active_settings.age)
            self.ids.activity_input.icon = self.icon_dict[active_settings.activity]
            self.ids.activity_input.text = str(active_settings.activity)
            self.ids.weight_gain_input.icon = self.icon_dict[active_settings.weight_gain_goal]
            self.ids.weight_gain_input.text = str(active_settings.weight_gain_goal)
            self.ids.calories_per_day.text = str(active_settings.calories_per_day)
            s.close()
            self.display_BMR()
            self.display_TDEE()
            self.display_cals_per_day()
        else:
            self.ids.profile_name_input.text = ""
            self.ids.gender_input.icon = "close"
            self.ids.gender_input.text = ""
            self.ids.weight_input.text = ""
            self.ids.height_input.text = ""
            self.ids.age_input.text = ""
            self.ids.activity_input.icon = "close"
            self.ids.activity_input.text = ""
            self.ids.weight_gain_input.icon = "close"
            self.ids.weight_gain_input.text = ""
            self.ids.calories_per_day.text = ""
            self.ids.bmr.text = ""
            self.ids.tdee.text = ""
            self.ids.calories_per_day.text = ""
    
    def open_settings_search(self):
        c = Settings_Dialog()
        self.popup_base = MDDialog(
            title= "Search Setting Profiles",
            type="custom",
            size_hint=(0.9,None),
            content_cls=c,
            on_open=c.display_search
        )
        c.popup_base = self.popup_base
        self.popup_base.open()

class Settings_Already_Exist_Dialog(MDBoxLayout):
    
    def overwrite(self):
        self.settings_screen.update_settings()
        self.settings_already_exist_dialog.dismiss()
    
    def cancel(self):
        self.settings_already_exist_dialog.dismiss()
        
class Settings_Dialog(MDBoxLayout):

    def __init__(self, *args, **kwargs):
        super(Settings_Dialog, self).__init__(*args, **kwargs)
        self.icon_dict = {
            "Male":"gender-male",
            "Female":"gender-female",
            "1.0":"cancel",
            "1.2":"walk",
            "1.375":"dumbbell",
            "1.725":"weight-lifter",
            "1.9":"weight",
            "-1100.0":"arrow-down-bold-circle",
            "-550.0":"arrow-down-bold-circle-outline",
            "-275.0":"arrow-down-bold-outline",
            "0.0":"checkbox-blank-circle-outline",
            "275.0":"arrow-up-bold-outline",
            "550.0":"arrow-up-bold-circle-outline",
            "1100.0":"arrow-up-bold-circle"
        }

    def display_search(self,instance):
        """
        instance is expected to be a MDTextField
        """
        search = instance.text
        s = Session()
        settings_query = s.query(Settings).filter(Settings.name.contains(search)).all()
        if search:
            if settings_query:
                self.ids.settings_search_result_list.clear_widgets()
                for i in settings_query:
                    Item = ThreeLineAvatarIconIDSListItem(
                        text=i.name,
                        settings_id=i.id,
                        secondary_text=f"{i.weight} kg",
                        tertiary_text=f"{i.height} cm",
                        on_release=self.open_profile_settings
                    )
                    Item.add_widget(IconLeftWidget(icon=self.icon_dict[str(i.weight_gain_goal)]))
                    Item.add_widget(IconRightWidget(icon=self.icon_dict[str(i.activity)]))
                    self.ids.settings_search_result_list.add_widget(Item)
            else:
                self.ids.settings_search_result_list.clear_widgets()
        else:
            self.ids.settings_search_result_list.clear_widgets()
            for i in s.query(Settings).all():
                Item = ThreeLineAvatarIconIDSListItem(
                    text=i.name,
                    settings_id=i.id,
                    secondary_text=f"{i.weight} kg",
                    tertiary_text=f"{i.height} cm",
                    on_release=self.open_profile_settings
                )
                Item.add_widget(IconLeftWidget(icon=self.icon_dict[str(i.weight_gain_goal)]))
                Item.add_widget(IconRightWidget(icon=self.icon_dict[str(i.activity)]))
                self.ids.settings_search_result_list.add_widget(Item)
        s.close()
    
    def open_profile_settings(self,instance): #instance is expected to be a ThreeLineListItem
        c = Settings_Settings_Dialog(settings_id=instance.settings_id)
        self.popup_layer2 = MDDialog(
            title=instance.text,
            type="custom",
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.popup_layer2 = self.popup_layer2
        c.popup_base = self.popup_base
        self.popup_layer2.open()

class Settings_Settings_Dialog(MDBoxLayout):
    
    def __init__(self,settings_id):
        super(Settings_Settings_Dialog,self).__init__()
        self.settings_id = settings_id
        self.settings_screen = MDApp.get_running_app().root.ids.settings_screen

    def delete(self):
        c = Delete_Settings_Dialog(settings_id=self.settings_id)
        self.popup_delete_layer3 = MDDialog(
            title="Delete profile?",
            type="custom",
            size_hint=(0.9, None),
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.popup_delete_layer3 = self.popup_delete_layer3
        c.popup_layer2 = self.popup_layer2
        c.popup_base = self.popup_base
        self.popup_delete_layer3.open()

    def use(self):
        s = Session()
        s.query(Active).update({Active.settings_id:self.settings_id})
        s.commit()
        s.close()
        self.settings_screen.active_settings_id = self.settings_id
        self.settings_screen.load_active_settings()
        self.popup_base.dismiss()
        self.popup_layer2.dismiss()

class Delete_Settings_Dialog(MDBoxLayout):
    
    def __init__(self,settings_id):
        super().__init__()
        self.settings_id = settings_id
        self.settings_screen = MDApp.get_running_app().root.ids.settings_screen

    def delete(self):
        s = Session()
        s.delete(s.query(Settings).get(self.settings_id))
        s.query(Active).update({Active.settings_id:None})
        s.commit()
        s.close()
        self.settings_screen.load_active_settings()
        self.popup_base.content_cls.display_search(self.popup_base.content_cls.ids.settings_search_input),
        self.popup_delete_layer3.dismiss()
        self.popup_layer2.dismiss()
    
    def cancel(self):
        self.popup_delete_layer3.dismiss()

class Ingredients_Screen(MDScreen):

    def __init__(self, *args,**kwargs):
        super(Ingredients_Screen,self).__init__(*args,**kwargs)
        self.ing_icon_dict = {
            "Meat":"food-steak",
            "Fish":"fish",
            "Grains / Bread":"bread-slice-outline",
            "Dairy":"cheese",
            "Vegetable":"carrot",
            "Fruit":"food-apple-outline",
            "Nuts / Seeds":"peanut",
            "Oil / Fats":"bottle-tonic",
            "Condiment":"soy-sauce",
            "Spice":"shaker-outline"
        }
        self.ing_icon_color_dict = {
            "All":(1,1,1,1),
            "Meat":(.39,.24,.04,1),
            "Fish":(1,.61,.39,1),
            "Grains / Bread":(1,.67,.35,1),
            "Dairy":(1,.78,.24,1),
            "Vegetable":(1,.55,.1,1),
            "Fruit":(.9,.16,0,1),
            "Nuts / Seeds":(.78,.53,0,1),
            "Oil / Fats":(.96,.75,0,1),
            "Condiment":(.78,.69,.24,1),
            "Spice":(.95,.95,.99,1)
        }
        self.sort_value = 4               # default value (sorts by type) others should be 2, 5, 6, 7 (cals, fats, carbs, prots)
        self.sort_order = True
        self.filter_type = "All"
        self.refresh_all_ingredients_list()

        
    def transition_to_meal_plan_screen(self):
        MDApp.get_running_app().root.ids.screen_manager.current = "Meal_Plan_Screen"
        MDApp.get_running_app().root.ids.screen_manager.transition.direction = "right"
        MDApp.get_running_app().root.load_active_profile()

    def refresh_all_ingredients_list(self): # this should only be called when an ingredient is added or deleted or edited and on start to sort the list
        s = Session()
        self.all_ingredient_id_and_stats_list = [[i.id,i.name,i.calories,i.unit,i.type,i.fats,i.carbohydrates,i.proteins] for i in s.query(Ingredient).all()]
        s.close()
        self.refresh_internal_list()

    def refresh_internal_list(self):
        if self.filter_type == "All":
            self.all_ingredient_id_and_stats_list_filtered = self.all_ingredient_id_and_stats_list
        else:
            self.all_ingredient_id_and_stats_list_filtered = list(filter(lambda x: x[4] == self.filter_type, self.all_ingredient_id_and_stats_list))
        self.display_ingredient_id_and_stats_list = sorted(self.all_ingredient_id_and_stats_list_filtered,key = lambda x: x[self.sort_value],reverse = self.sort_order)
        self.refresh_display_list() if self.ids else None

    def refresh_internal_list_old(self):
        self.ing_type = self.ids.filter.text if self.ids else "All"
        if self.ing_type == "All":
            self.display_ingredient_id_and_stats_list = self.all_ingredient_id_and_stats_list_sorted
        else:
            s = Session()
            self.display_ingredient_id_and_stats_list = list(filter(lambda x: x[4] == self.ing_type,self.all_ingredient_id_and_stats_list_sorted))
            s.close()
        self.refresh_display_list() if self.ids else None

    def refresh_display_list(self):
        self.ing_search = self.ids.ing_search.text if self.ids else ""
        self.ids.ingredients_display_list.clear_widgets()
        for i in self.display_ingredient_id_and_stats_list:
            if self.ing_search.lower() in i[1].lower():
                Item = ThreeLineAvatarIconIDSListItem(
                    ingredient_id=i[0],
                    text=i[1],
                    secondary_text=f"{i[2]} kcals" if self.sort_value == 2 or self.sort_value == 4 else f"{i[5]} grams of fat" if self.sort_value == 5 else f"{i[6]} grams of carbohydrates" if self.sort_value == 6 else f"{i[7]} grams of protein",
                    tertiary_text=f"per {'100' if i[3] =='gram' or i[3] =='ml' else ''} {i[3]}{'s' if i[3] == 'gram' or i[3] == 'ml' else ''}",
                    on_release=self.open_ingredient_options_dialog,
                )
                Icon = IconLeftWidget(
                    icon=self.ing_icon_dict[i[4]],
                    theme_text_color="Custom",
                    text_color=self.ing_icon_color_dict[i[4]],
                    )
                Item.add_widget(Icon)
                self.ids.ingredients_display_list.add_widget(Item)
        self.ids.ingredients_display_list.add_widget(Widget(size_hint_y=None,height=dp(50)))

    def open_add_ingredients_dialog(self):
        c = Add_Ingredient_Dialog()
        self.popup_base = MDDialog(
            title="Add Ingredient",
            type="custom",
            size_hint=(.9, None),
            height=MDApp.get_running_app().root.height*.8,
            pos_hint={"center_x": .5, "center_y": .5},
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.popup_base = self.popup_base
        self.popup_base.open()
    
    def open_ingredient_options_dialog(self,listitem): 
        c = Ingredient_Options_Dialog(ingredient_id=listitem.ingredient_id,
                                      ingredient_name=listitem.text)
        self.popup_base = MDDialog(
            title=f"{listitem.text} Options",
            type="custom",
            size_hint=(.9, None),
            pos_hint={"center_x": .5, "center_y": .5},
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.popup_base = self.popup_base
        self.popup_base.open()

    def open_filter_menu(self):
        c = Ingredient_List_Filter_Dialog()
        self.popup_ingredient_list_filter = MDDialog(
            title="Filter and Sort settings",
            type="custom",
            content_cls=c,
            size_hint=(.9, None),
            radius=[20, 7, 20, 7],
            pos_hint={"center_x": .5, "center_y": .5}
        )
        c.logic = self
        c.sort_value = self.sort_value # determines wether to sort by amount (3), calories (2), fats (7), carbohydrates (8) or proteins (9)
        c.sort_order = self.sort_order # bool // False = ascending, True = descending
        c.filter_type = self.filter_type # "Meat", "Fish", "Grains / Bread", "Dairy", "Vegetable", "Fruit", "Nuts / Seeds", "Oil / Fats", "Condiment", "Spice", "All"
        c.popup_ingredient_list_filter = self.popup_ingredient_list_filter
        c.set_initial_settings()
        self.popup_ingredient_list_filter.open()

class Ingredient_List_Filter_Dialog(MDBoxLayout):

    def __init__(self, *args, **kwargs):
        super(Ingredient_List_Filter_Dialog, self).__init__(*args, **kwargs)
        self.sort_value = 4 # 4 corresponds to type by default
        self.sort_order = True # corresponds to the sort reverse attribute (high to low, low to high) # what is what I havent determined yet
        self.filter_type = "All"
        self.ing_icon_dict = {
            "All":"filter-variant",
            "Meat":"food-steak",
            "Fish":"fish",
            "Grains / Bread":"bread-slice-outline",
            "Dairy":"cheese",
            "Vegetable":"carrot",
            "Fruit":"food-apple-outline",
            "Nuts / Seeds":"peanut",
            "Oil / Fats":"bottle-tonic",
            "Condiment":"soy-sauce",
            "Spice":"shaker-outline"
        }
        self.ing_icon_color_dict = {
            "All":(1,1,1,1),
            "Meat":(.39,.24,.04,1),
            "Fish":(1,.61,.39,1),
            "Grains / Bread":(1,.67,.35,1),
            "Dairy":(1,.78,.24,1),
            "Vegetable":(1,.55,.1,1),
            "Fruit":(.9,.16,0,1),
            "Nuts / Seeds":(.78,.53,0,1),
            "Oil / Fats":(.96,.75,0,1),
            "Condiment":(.78,.69,.24,1),
            "Spice":(.95,.95,.99,1)
        }
    
    def set_initial_settings(self):
        if self.sort_value == 2:
            self.ids.sort_by_calories.active = True
            self.ids.sort_by_calories_label.text_color = (1,1,1,1)
        elif self.sort_value == 5:
            self.ids.sort_by_fats.active = True
            self.ids.sort_by_fats_label.text_color = (1,1,1,1)
        elif self.sort_value == 6:
            self.ids.sort_by_carbohydrates.active = True
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,1)
        elif self.sort_value == 7:
            self.ids.sort_by_proteins.active = True
            self.ids.sort_by_proteins_label.text_color = (1,1,1,1)
        if self.sort_order:
            self.ids.sorting_direction.icon = "sort-descending"
            self.ids.sort_order_label.text = "High to Low"
        else:
            self.ids.sorting_direction.icon = "sort-ascending"
            self.ids.sort_order_label.text = "Low to High"
        self.ids.ingredient_type_filter.icon = self.ing_icon_dict[self.filter_type]
        self.ids.ingredient_type_filter.text_color = self.ing_icon_color_dict[self.filter_type]

    def cancel(self):
        self.popup_ingredient_list_filter.dismiss()

    def check_calories(self,instance,value):
        if value:
            self.ids.sort_by_fats.active = False
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates.active = False
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins.active = False
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)
            self.ids.sort_by_calories_label.text_color = (1,1,1,1)
            self.sort_value = 2
        else:
            self.sort_value = 4
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)

    def check_fats(self,instance,value):
        if value:
            self.ids.sort_by_calories.active = False
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates.active = False
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins.active = False
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)
            self.ids.sort_by_fats_label.text_color = (1,1,1,1)
            self.sort_value = 5
        else:
            self.sort_value = 4
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
    
    def check_carbohydrates(self,instance,value):
        if value:
            self.ids.sort_by_calories.active = False
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)
            self.ids.sort_by_fats.active = False
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins.active = False
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,1)
            self.sort_value = 6
        else:
            self.sort_value = 4
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)

    def check_proteins(self,instance,value):
        if value:
            self.ids.sort_by_calories.active = False
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)
            self.ids.sort_by_fats.active = False
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates.active = False
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins_label.text_color = (1,1,1,1)
            self.sort_value = 7
        else:
            self.sort_value = 4
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)

    def set_sort_order(self):
        self.ids.sorting_direction.icon = "sort-ascending" if self.ids.sorting_direction.icon == "sort-descending" else "sort-descending"
        self.sort_order = False if self.ids.sorting_direction.icon == "sort-ascending" else True
        self.ids.sort_order_label.text = "High to Low" if self.sort_order else "Low to High"

    def open_filter_dropdown(self):
        self.choices_filter = [
            {
                "viewclass": "OneLineAvatarIconListItem",
                "text": "All",
                "icon":"filter-variant",
                "height": dp(56),
                "on_release": lambda x="filter-variant",y="All": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineAvatarIconListItem",
                "text": "Meat",
                "icon": "food-steak",
                "height": dp(56),
                "on_release": lambda x="food-steak",y="Meat": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fish",
                "icon": "fish",
                "height": dp(56),
                "on_release": lambda x="fish",y="Fish": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Grains / Bread",
                "icon": "bread-slice-outline",
                "height": dp(56),
                "on_release": lambda x="bread-slice-outline",y="Grains / Bread": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Dairy",
                "icon": "cheese",
                "height": dp(56),
                "on_release": lambda x="cheese",y="Dairy": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Vegetable",
                "icon": "carrot",
                "height": dp(56),
                "on_release": lambda x="carrot",y="Vegetable": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fruit",
                "icon": "food-apple-outline",
                "height": dp(56),
                "on_release": lambda x="food-apple-outline",y="Fruit": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Nuts / Seeds",
                "icon": "peanut",
                "height": dp(56),
                "on_release": lambda x="peanut",y="Nuts / Seeds": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Oil / Fats",
                "icon": "bottle-tonic",
                "height": dp(56),
                "on_release": lambda x="bottle-tonic",y="Oil / Fats": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Condiment",
                "icon": "soy-sauce",
                "height": dp(56),
                "on_release": lambda x="soy-sauce",y="Condiment": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Spice",
                "icon": "shaker-outline",
                "height": dp(56),
                "on_release": lambda x="shaker-outline",y="Spice": self.set_filter_icon(x,y)
            },
        ]
        self.menu_list_type = MDDropdownMenu(
            caller=self.ids.ingredient_type_filter,
            items=self.choices_filter,
            position="auto",
            width_mult=4
        )
        self.menu_list_type.open()

    def set_filter_icon(self, icon, ing_type):
        self.ids.ingredient_type_filter.icon = icon
        self.ids.ingredient_type_filter.text_color = self.ing_icon_color_dict[ing_type]
        self.filter_type = ing_type
        self.menu_list_type.dismiss()

    def apply_filter(self):
        self.logic.sort_value = self.sort_value
        self.logic.sort_order = self.sort_order
        self.logic.filter_type = self.filter_type
        self.logic.refresh_internal_list()
        self.popup_ingredient_list_filter.dismiss()

class Add_Ingredient_Dialog(MDBoxLayout):
    
    def __init__(self, *args, **kwargs):
        super(Add_Ingredient_Dialog, self).__init__(*args, **kwargs)
        self.ing_icon_dict = {
            "Meat":"food-steak",
            "Fish":"fish",
            "Grains / Bread":"bread-slice-outline",
            "Dairy":"cheese",
            "Vegetable":"carrot",
            "Fruit":"food-apple-outline",
            "Nuts / Seeds":"peanut",
            "Oil / Fats":"bottle-tonic",
            "Condiment":"soy-sauce",
            "Spice":"shaker-outline",
            "1":"cancel",
            "2":"numeric-2",
            "3":"numeric-3",
            "4":"numeric-4",
            "5":"numeric-5",
            "6":"numeric-6",
            "7":"numeric-7",
            "8":"numeric-8",
            "9":"numeric-9",
            "10":"numeric-10",
            "False":"all-inclusive",
            "gram":"weight-gram",
            "ml":"cup",
            "piece":"puzzle-outline"
        }
        self.ing_screen = MDApp.get_running_app().root.ids.ingredients_screen
    
    def open_divisibility_dropdown(self):
        self.choices_divisibility = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "Indivisible",
                "icon": "cancel",
                "height": dp(56),
                "on_release": lambda x="cancel",y=1: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "2",
                "icon": "numeric-2",
                "height": dp(56),
                "on_release": lambda x="numeric-2",y=2: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "3",
                "icon": "numeric-3",
                "height": dp(56),
                "on_release": lambda x="numeric-3",y=3: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "4",
                "icon": "numeric-4",
                "height": dp(56),
                "on_release": lambda x="numeric-4",y=4: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "5",
                "icon": "numeric-5",
                "height": dp(56),
                "on_release": lambda x="numeric-5",y=5: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "6",
                "icon": "numeric-6",
                "height": dp(56),
                "on_release": lambda x="numeric-6",y=6: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "7",
                "icon": "numeric-7",
                "height": dp(56),
                "on_release": lambda x="numeric-7",y=7: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "8",
                "icon": "numeric-8",
                "height": dp(56),
                "on_release": lambda x="numeric-8",y=8: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "9",
                "icon": "numeric-9",
                "height": dp(56),
                "on_release": lambda x="numeric-9",y=9: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "10",
                "icon": "numeric-10",
                "height": dp(56),
                "on_release": lambda x="numeric-10",y=10: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "By any amount",
                "icon": "all-inclusive",
                "height": dp(56),
                "on_release": lambda x="all-inclusive",y=False: self.set_divisibility_icon(x,y),
            }
        ]
        self.menu_list_divisibility = MDDropdownMenu(
            caller=self.ids.add_ing_divisibility,
            items=self.choices_divisibility,
            position="auto",
            width_mult=4
        )
        self.menu_list_divisibility.open()
    
    def set_divisibility_icon(self, icon, value):
        self.ids.add_ing_divisibility.icon = icon
        self.ids.add_ing_divisibility.value = value
        self.menu_list_divisibility.dismiss()
        self.add_button_check_validity()
    
    def open_type_dropdown(self):
        self.choices_type = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "Meat",
                "icon": "food-steak",
                "height": dp(56),
                "on_release": lambda x="food-steak",y="Meat": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fish",
                "icon": "fish",
                "height": dp(56),
                "on_release": lambda x="fish",y="Fish": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Grains / Bread",
                "icon": "bread-slice-outline",
                "height": dp(56),
                "on_release": lambda x="bread-slice-outline",y="Grains / Bread": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Dairy",
                "icon": "cheese",
                "height": dp(56),
                "on_release": lambda x="cheese",y="Dairy": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Vegetable",
                "icon": "carrot",
                "height": dp(56),
                "on_release": lambda x="carrot",y="Vegetable": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fruit",
                "icon": "food-apple-outline",
                "height": dp(56),
                "on_release": lambda x="food-apple-outline",y="Fruit": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Nuts / Seeds",
                "icon": "peanut",
                "height": dp(56),
                "on_release": lambda x="peanut",y="Nuts / Seeds": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Oil / Fats",
                "icon": "bottle-tonic",
                "height": dp(56),
                "on_release": lambda x="bottle-tonic",y="Oil / Fats": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Condiment",
                "icon": "soy-sauce",
                "height": dp(56),
                "on_release": lambda x="soy-sauce",y="Condiment": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Spice",
                "icon": "shaker-outline",
                "height": dp(56),
                "on_release": lambda x="shaker-outline",y="Spice": self.set_type_icon(x,y)
            },
        ]
        self.menu_list_type = MDDropdownMenu(
            caller=self.ids.add_ing_type,
            items=self.choices_type,
            position="auto",
            width_mult=4
        )
        self.menu_list_type.open()
    
    def set_type_icon(self, icon, text):
        self.ids.add_ing_type.icon = icon
        self.ids.add_ing_type.text = text
        self.menu_list_type.dismiss()
        self.ids.add_ing_calories.focus = True
        self.add_button_check_validity()
    
    def open_unit_dropdown(self):
        self.choices_unit = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "grams",
                "icon": "weight-gram",
                "height": dp(56),
                "on_release": lambda x="weight-gram",y="gram": self.set_unit_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "milliliters",
                "icon": "cup",
                "height": dp(56),
                "on_release": lambda x="cup",y="ml": self.set_unit_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "pieces",
                "icon": "puzzle-outline",
                "height": dp(56),
                "on_release": lambda x="puzzle-outline",y="piece": self.set_unit_icon(x,y)
            }
        ]
        self.menu_list_unit = MDDropdownMenu(
            caller=self.ids.add_ing_unit,
            items=self.choices_unit,
            position="auto",
            width_mult=4
        )
        self.menu_list_unit.open()
    
    def set_unit_icon(self, icon, text):
        self.ids.add_ing_unit.icon = icon
        self.ids.add_ing_unit.text = text
        self.menu_list_unit.dismiss()
        self.open_type_dropdown()
        self.add_ing_divisibility_check_validity()
        self.add_button_check_validity()
    
    def add_ing_divisibility_check_validity(self):
        if self.ids.add_ing_unit.text == "gram" or self.ids.add_ing_unit.text == "ml":
            self.ids.add_ing_divisibility.disabled = True
            self.ids.divisibility_label.color = (1,1,1,.5)
            self.ids.add_ing_divisibility.value = False
            self.ids.add_ing_divisibility.icon = "all-inclusive"
        else:
            self.ids.add_ing_divisibility.disabled = False
            self.ids.divisibility_label.color = (1,1,1,1)
    
    def cancel(self):
        self.popup_base.dismiss()
    
    def add_button_check_validity(self):
        if all(
            [
                self.ids.add_ing_name.text,
                self.ids.add_ing_calories.text,
                self.ids.add_ing_fats.text,
                self.ids.add_ing_carbohydrates.text,
                self.ids.add_ing_proteins.text
            ]
        ) and self.ids.add_ing_unit.icon != "close" and self.ids.add_ing_type.icon != "close" and self.ids.add_ing_divisibility.icon != "close":
            self.ids.add_ing_button.disabled = False
        else:
            self.ids.add_ing_button.disabled = True
    
    def add_ingredient(self):
        s = Session()
        ing_query = s.query(Ingredient).filter(Ingredient.name == self.ids.add_ing_name.text).first()
        if not ing_query:
            new_ingredient = Ingredient(
                name = self.ids.add_ing_name.text,
                type = self.ids.add_ing_type.text,
                unit = self.ids.add_ing_unit.text,
                divisible_by = self.ids.add_ing_divisibility.value,
                calories = self.ids.add_ing_calories.text,
                fats = self.ids.add_ing_fats.text,
                carbohydrates = self.ids.add_ing_carbohydrates.text,
                proteins = self.ids.add_ing_proteins.text,
                snack=False
            )
            s.add(new_ingredient)
            s.commit()
            s.close()
            self.ing_screen.refresh_all_ingredients_list()
            self.popup_base.dismiss()
        else:
            s.close()
            c = Ingredient_Already_Exists_Dialog(ingredient_id=ing_query.id)
            self.ingredient_already_exists_dialog = MDDialog(
                title=f"{self.ids.add_ing_name.text} Already Exists, would you like to update it?",
                type="custom",
                content_cls=c,
                size_hint_x=.9,
                radius=[20, 7, 20, 7]
            )
            c.logic = self
            c.popup_base = self.popup_base
            c.ingredient_already_exists_dialog = self.ingredient_already_exists_dialog
            self.ingredient_already_exists_dialog.open()

class Ingredient_Already_Exists_Dialog(MDBoxLayout):
    
    def __init__(self, ingredient_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ingredient_id = ingredient_id
        self.ing_screen = MDApp.get_running_app().root.ids.ingredients_screen

    def cancel(self):
        self.ingredient_already_exists_dialog.dismiss()
        self.popup_base.dismiss()
    
    def update(self): # updates the ingredient in the database
        s = Session()
        self.ing = s.query(Ingredient).get(self.ingredient_id)
        self.ing.name = self.logic.add_ing_name.text
        self.ing.unit = self.logic.add_ing_unit.text
        self.ing.type = self.logic.add_ing_type.text
        self.ing.calories = self.logic.add_ing_calories.text
        self.ing.fats = self.logic.add_ing_fats.text
        self.ing.carbohydrates = self.logic.add_ing_carbohydrates.text
        self.ing.proteins = self.logic.add_ing_proteins.text
        self.ing.divisible_by = self.logic.add_ing_divisibility.value
        s.commit()
        s.close()
        self.ing_screen.refresh_all_ingredients_list()
        self.ingredient_already_exists_dialog.dismiss()
        self.popup_base.dismiss()

class Ingredient_Options_Dialog(MDBoxLayout):
    
    def __init__(self, ingredient_id, ingredient_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ingredient_id = ingredient_id
        self.ingredient_name = ingredient_name
        self.ing_icon_dict = {
            "Meat":"food-steak",
            "Fish":"fish",
            "Grains / Bread":"bread-slice-outline",
            "Dairy":"cheese",
            "Vegetable":"carrot",
            "Fruit":"food-apple-outline",
            "Nuts / Seeds":"peanut",
            "Oil / Fats":"bottle-tonic",
            "Condiment":"soy-sauce",
            "Spice":"shaker-outline",
            "1":"cancel",
            "2":"numeric-2",
            "3":"numeric-3",
            "4":"numeric-4",
            "5":"numeric-5",
            "6":"numeric-6",
            "7":"numeric-7",
            "8":"numeric-8",
            "9":"numeric-9",
            "10":"numeric-10",
            "False":"all-inclusive",
            "0":"all-inclusive",
            "gram":"weight-gram",
            "ml":"cup",
            "piece":"puzzle-outline"
        }
    
    def edit(self):
        s = Session()
        self.ing = s.query(Ingredient).get(self.ingredient_id)
        c = Edit_Ingredient_Dialog(ingredient_id=self.ing.id,
                                   ingredient_name=self.ing.name)
        self.popup_layer2_edit = MDDialog(
            title=f"Edit {self.ing.name}?",
            type="custom",
            size_hint=(.9, None),
            pos_hint={"center_x": .5, "center_y": .5},
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.popup_layer2_edit = self.popup_layer2_edit
        c.popup_base = self.popup_base
        c.ids.update_ing_name.text = self.ing.name
        c.ids.update_ing_calories.text = str(self.ing.calories)
        c.ids.update_ing_fats.text = str(self.ing.fats)
        c.ids.update_ing_carbohydrates.text = str(self.ing.carbohydrates)
        c.ids.update_ing_proteins.text = str(self.ing.proteins)
        c.ids.update_ing_unit.text = str(self.ing.unit)
        c.ids.update_ing_unit.icon = self.ing_icon_dict[str(self.ing.unit)]
        c.ids.update_ing_type.text = str(self.ing.type)
        c.ids.update_ing_type.icon = self.ing_icon_dict[str(self.ing.type)]
        c.ids.update_ing_divisibility.value = str(self.ing.divisible_by)
        c.ids.update_ing_divisibility.icon = self.ing_icon_dict[str(self.ing.divisible_by)]
        c.update_ing_divisibility_check_validity()
        s.close()
        self.popup_layer2_edit.open()
   
    def open_delete_ingredient_dialog(self):
        c = Delete_Ingredient_Dialog(ingredient_id=self.ingredient_id)
        self.popup_layer2_delete = MDDialog(
            title=f"Delete {self.ingredient_name} ?",
            type="custom",
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.popup_layer2_delete = self.popup_layer2_delete
        c.popup_base = self.popup_base
        self.popup_layer2_delete.open()

class Delete_Ingredient_Dialog(MDBoxLayout):
    
    def __init__(self, ingredient_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ingredient_id = ingredient_id
        self.ing_screen = MDApp.get_running_app().root.ids.ingredients_screen
    
    def cancel(self):
        self.popup_layer2_delete.dismiss()
    
    def delete(self):
        s = Session()
        self.ing = s.query(Ingredient).get(self.ingredient_id)
        self.asc_objs = s.query(Association).filter(Association.ingredient_id == self.ing.id).all()
        for i in self.asc_objs: # makes sure that the associations are also deleted
            s.delete(i)
        s.delete(self.ing)
        s.commit()
        s.close()
        self.ing_screen.refresh_all_ingredients_list()
        self.popup_layer2_delete.dismiss()
        self.popup_base.dismiss()

class Edit_Ingredient_Dialog(MDBoxLayout):
    
    def __init__(self, ingredient_id, ingredient_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ingredient_id = ingredient_id
        self.ingredient_name = ingredient_name
        self.ing_screen = MDApp.get_running_app().root.ids.ingredients_screen
        s = Session()
        self.ingredient_name_list = [i.name if i.name != self.ingredient_name else None for i in s.query(Ingredient).all()]
        s.close()

    def open_divisibility_dropdown(self):
        self.choices_divisibility = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "Indivisible",
                "icon": "cancel",
                "height": dp(56),
                "on_release": lambda x="cancel",y=1: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "2",
                "icon": "numeric-2",
                "height": dp(56),
                "on_release": lambda x="numeric-2",y=2: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "3",
                "icon": "numeric-3",
                "height": dp(56),
                "on_release": lambda x="numeric-3",y=3: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "4",
                "icon": "numeric-4",
                "height": dp(56),
                "on_release": lambda x="numeric-4",y=4: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "5",
                "icon": "numeric-5",
                "height": dp(56),
                "on_release": lambda x="numeric-5",y=5: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "6",
                "icon": "numeric-6",
                "height": dp(56),
                "on_release": lambda x="numeric-6",y=6: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "7",
                "icon": "numeric-7",
                "height": dp(56),
                "on_release": lambda x="numeric-7",y=7: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "8",
                "icon": "numeric-8",
                "height": dp(56),
                "on_release": lambda x="numeric-8",y=8: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "9",
                "icon": "numeric-9",
                "height": dp(56),
                "on_release": lambda x="numeric-9",y=9: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "10",
                "icon": "numeric-10",
                "height": dp(56),
                "on_release": lambda x="numeric-10",y=10: self.set_divisibility_icon(x,y),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "By any amount",
                "icon": "all-inclusive",
                "height": dp(56),
                "on_release": lambda x="all-inclusive",y=False: self.set_divisibility_icon(x,y),
            }
        ]
        self.menu_list_divisibility = MDDropdownMenu(
            caller=self.ids.update_ing_divisibility,
            items=self.choices_divisibility,
            position="auto",
            width_mult=4
        )
        self.menu_list_divisibility.open()
    
    def set_divisibility_icon(self, icon, value):
        self.ids.update_ing_divisibility.icon = icon
        self.ids.update_ing_divisibility.value = value
        self.menu_list_divisibility.dismiss()
        self.update_button_check_validity()
    
    def open_type_dropdown(self):
        self.choices_type = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "Meat",
                "icon": "food-steak",
                "height": dp(56),
                "on_release": lambda x="food-steak",y="Meat": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fish",
                "icon": "fish",
                "height": dp(56),
                "on_release": lambda x="fish",y="Fish": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Grains / Bread",
                "icon": "bread-slice-outline",
                "height": dp(56),
                "on_release": lambda x="bread-slice-outline",y="Grains / Bread": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Dairy",
                "icon": "cheese",
                "height": dp(56),
                "on_release": lambda x="cheese",y="Dairy": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Vegetable",
                "icon": "carrot",
                "height": dp(56),
                "on_release": lambda x="carrot",y="Vegetable": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fruit",
                "icon": "food-apple-outline",
                "height": dp(56),
                "on_release": lambda x="food-apple-outline",y="Fruit": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Nuts / Seeds",
                "icon": "peanut",
                "height": dp(56),
                "on_release": lambda x="peanut",y="Nuts / Seeds": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Oil / Fats",
                "icon": "bottle-tonic",
                "height": dp(56),
                "on_release": lambda x="bottle-tonic",y="Oil / Fats": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Condiment",
                "icon": "soy-sauce",
                "height": dp(56),
                "on_release": lambda x="soy-sauce",y="Condiment": self.set_type_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Spice",
                "icon": "shaker-outline",
                "height": dp(56),
                "on_release": lambda x="shaker-outline",y="Spice": self.set_type_icon(x,y)
            },
        ]
        self.menu_list_type = MDDropdownMenu(
            caller=self.ids.update_ing_type,
            items=self.choices_type,
            position="auto",
            width_mult=4
        )
        self.menu_list_type.open()
    
    def set_type_icon(self, icon, text):
        self.ids.update_ing_type.icon = icon
        self.ids.update_ing_type.text = text
        self.menu_list_type.dismiss()
        self.update_button_check_validity()
    
    def open_unit_dropdown(self):
        self.choices_unit = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "grams",
                "icon": "weight-gram",
                "height": dp(56),
                "on_release": lambda x="weight-gram",y="gram": self.set_unit_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "milliliters",
                "icon": "cup",
                "height": dp(56),
                "on_release": lambda x="cup",y="ml": self.set_unit_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "pieces",
                "icon": "puzzle-outline",
                "height": dp(56),
                "on_release": lambda x="puzzle-outline",y="piece": self.set_unit_icon(x,y)
            }
        ]
        self.menu_list_unit = MDDropdownMenu(
            caller=self.ids.update_ing_unit,
            items=self.choices_unit,
            position="auto",
            width_mult=4
        )
        self.menu_list_unit.open()
    
    def set_unit_icon(self, icon, text):
        self.ids.update_ing_unit.icon = icon
        self.ids.update_ing_unit.text = text
        self.menu_list_unit.dismiss()
        self.update_button_check_validity()
        self.update_ing_divisibility_check_validity()

    def update_ing_divisibility_check_validity(self):
        if self.ids.update_ing_unit.text == "gram" or self.ids.update_ing_unit.text == "ml":
            self.ids.update_ing_divisibility.disabled = True
            self.ids.divisibility_label.color = (1,1,1,.5)
            self.ids.update_ing_divisibility.value = False
            self.ids.update_ing_divisibility.icon = "all-inclusive"
        else:
            self.ids.update_ing_divisibility.disabled = False
            self.ids.divisibility_label.color = (1,1,1,1)

    def ing_name_check_validity(self):
        if self.ids.update_ing_name.text in self.ingredient_name_list:
            self.ids.update_ing_name.hint_text = "Already exists!"
            self.ids.update_ing_name.text_color_normal = (1,0,0,1)
            return False
        else:
            self.ids.update_ing_name.hint_text = ""
            self.ids.update_ing_name.text_color_normal = (1,1,1,.25) # MDApp.get_running_app().theme_cls.primary_color
            return True

    def stats_check_validity(self):
        if all(
            [
                self.ids.update_ing_name.text,
                self.ids.update_ing_calories.text,
                self.ids.update_ing_fats.text,
                self.ids.update_ing_carbohydrates.text,
                self.ids.update_ing_proteins.text
            ]
        ) and self.ids.update_ing_unit.icon != "close" and self.ids.update_ing_type.icon != "close" and self.ids.update_ing_divisibility.icon != "close":
            return True
        else:
            return False

    def update_button_check_validity(self):
        if self.ing_name_check_validity() and self.stats_check_validity():
            self.ids.update_ing_button.disabled = False
        else:
            self.ids.update_ing_button.disabled = True
    
    def cancel(self):
        self.popup_layer2_edit.dismiss()
    
    def update_ingredient(self):
        s = Session()
        self.ing = s.query(Ingredient).get(self.ingredient_id)
        self.ing.name = self.ids.update_ing_name.text
        self.ing.calories = self.ids.update_ing_calories.text
        self.ing.fats = self.ids.update_ing_fats.text
        self.ing.carbohydrates = self.ids.update_ing_carbohydrates.text
        self.ing.proteins = self.ids.update_ing_proteins.text
        self.ing.unit = self.ids.update_ing_unit.text
        self.ing.type = self.ids.update_ing_type.text
        self.ing.divisible_by = self.ids.update_ing_divisibility.value
        s.commit()
        s.close()
        self.ing_screen.refresh_all_ingredients_list()
        self.popup_layer2_edit.dismiss()
        self.popup_base.dismiss()

class Meals_Screen(MDScreen):
        # migrate the inglist to this instance to midigate more frequent loading and queries
    def __init__(self, *args, **kwargs):
        super(Meals_Screen, self).__init__(*args, **kwargs)
        self.meal_icon_dict = {
            "hot":"thermometer",
            "cold":"snowflake",
            "sweet":"candy-outline",
            "savory":"french-fries",
            "breakfast_hot":"egg-fried",
            "breakfast_cold":"bowl-mix-outline",
            "dinner_lunch_hot":"pot-steam-outline",
            "dinner_lunch_cold":"fridge-outline",
            "snack_sweet":"cookie-outline",
            "snack_savory":"sausage",
        }
        self.meal_icon_color_dict = {
            "thermometer":(1,0,0,1),
            "snowflake":(0,.7,1,1),
            "candy-outline":(1,.4,.8,1),
            "french-fries":(1,.8,0,1),
            "egg-fried":(1,.5,0,1),
            "bowl-mix-outline":(1,.9,0,1),
            "pot-steam-outline":(.7,0,0.1),
            "fridge-outline":(0.4,.2,1),
            "cookie-outline":(.7,0,.15,1),
            "sausage":(.7,.2,.04,1)
        }
        self.show_all_meals = True
        self.ignore_sweet_savory = True
        self.ignore_hot_cold = True
        self.breakfast = False
        self.lunch = False
        self.dinner = False
        self.snack = False
        self.hot_cold = False
        self.sweet_savory = False
    
    def transition_to_meal_plan_screen(self):
        MDApp.get_running_app().root.ids.screen_manager.current = "Meal_Plan_Screen"
        MDApp.get_running_app().root.ids.screen_manager.transition.direction = "right"
        MDApp.get_running_app().root.load_active_profile()

    def open_filter_dialog(self):
        c = Filter_Dialog()
        self.popup_base = MDDialog(
            title="Search filter",
            type="custom",
            size_hint=(.9, None),
            height=MDApp.get_running_app().root.height*.8,
            pos_hint={"center_x": .5, "center_y": .5},
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.popup_base = self.popup_base
        c.ids.breakfast.active = self.breakfast
        c.ids.lunch.active = self.lunch
        c.ids.dinner.active = self.dinner
        c.ids.snack.active = self.snack
        c.ids.hot_cold.active = self.hot_cold
        c.ids.sweet_savory.active = self.sweet_savory
        c.ids.ignore_hot_cold.active = not(self.ignore_hot_cold)
        c.ids.ignore_sweet_savory.active = not(self.ignore_sweet_savory)
        self.popup_base.open()

    def refresh_internal_list(self):
        s = Session()
        if self.show_all_meals:
            self.meal_list = s.query(Meal).all()
        else:
            filter_conditions = [
                Meal.breakfast == True,
                Meal.lunch == True,
                Meal.dinner == True,
                Meal.snack == True
            ]
            filter_condition_inputs = [self.breakfast,self.lunch,self.dinner,self.snack]
            for index, i in enumerate(filter_conditions.copy()):
                if not filter_condition_inputs[index]:
                    filter_conditions.remove(i)
            if self.ignore_hot_cold and self.ignore_sweet_savory:
                self.meal_list = s.query(Meal).filter(
                    or_(
                        *filter_conditions
                    )
                ).all()
            elif self.ignore_hot_cold:
                self.meal_list = s.query(Meal).filter(
                    and_(
                        or_(
                            *filter_conditions
                        ),
                        Meal.sweet_savory == self.sweet_savory
                    )
                ).all()
            elif self.ignore_sweet_savory:
                self.meal_list = s.query(Meal).filter(
                    and_(
                        or_(
                            *filter_conditions
                        ),
                        Meal.hot_cold == self.hot_cold
                    )
                ).all()
            else:
                self.meal_list = s.query(Meal).filter(
                    and_(
                        or_(
                            *filter_conditions
                        ),
                        Meal.hot_cold == self.hot_cold,
                        Meal.sweet_savory == self.sweet_savory
                    )
                ).all()
        s.close()
    
    def refresh_display_list(self):
        search = self.ids.meal_search.text
        self.ids.meals_display_list.clear_widgets()
        if self.meal_list:
            self.meal_list_for_search = list(filter(lambda x: True if search.lower() in x.name.lower() else False, self.meal_list))
            s = Session()
            for index, i in enumerate(self.meal_list_for_search):
                s.add(i)
                icon_hot_cold = self.meal_icon_dict["cold" if i.hot_cold else "hot"]
                icon_hot_cold_color = self.meal_icon_color_dict[icon_hot_cold]
                icon_sweet_savory = self.meal_icon_dict["savory" if i.sweet_savory else "sweet"]
                icon_sweet_savor_color = self.meal_icon_color_dict[icon_sweet_savory]
                icon_type = self.meal_icon_dict["breakfast_hot" if i.breakfast and not i.hot_cold else "breakfast_cold" if i.breakfast and i.hot_cold else "dinner_lunch_hot" if i.dinner and not i.hot_cold or i.lunch and not i.hot_cold else "dinner_lunch_cold" if i.dinner and i.hot_cold or i.lunch and i.hot_cold else "snack_sweet" if i.snack and not i.sweet_savory else "snack_savory"]
                icon_type_color = self.meal_icon_color_dict[icon_type]
                Item = ThreeLineAvatarIconIDSListItem(
                    meal_id=i.id,
                    text=i.name,
                    secondary_text=f"{round(i.calories,2)} kcals",
                    tertiary_text=f"{round(i.proteins,2)}g protein, {round(i.carbohydrates,2)}g carbs, {round(i.fats,2)}g fat",
                    on_release=self.open_meal_options_dialog
                    )
                
                Item.add_widget(
                    IconLeftWidget(
                        icon=icon_type,
                        theme_text_color="Custom",
                        text_color=icon_type_color
                    )
                )
                Item.add_widget(
                    MDBoxLayout(
                        Widget(size_hint_x=15),
                        MDIconButton(
                            size_hint_x=2,
                            pos_hint={"center_y":.6},
                            icon=icon_sweet_savory,
                            theme_text_color="Custom",
                            text_color=icon_sweet_savor_color
                        ),
                        MDIconButton(
                            size_hint_x=2,
                            pos_hint={"center_y":.6},
                            icon=icon_hot_cold,
                            theme_text_color="Custom",
                            text_color=icon_hot_cold_color
                        ),
                        orientation='horizontal',
                        size_hint_x=None,
                        width=MDApp.get_running_app().root.width*.95,
                        pos_hint={"center_y": .5}
                    )
                )
                self.ids.meals_display_list.add_widget(Item)
            s.close()
        self.ids.meals_display_list.add_widget(Widget(size_hint_y=None,height=dp(50)))

    def open_add_meal_dialog(self):
        c = Add_Meal_Dialog()
        self.popup_base = MDDialog(
            title="Add Meal",
            type="custom",
            size_hint=(.9, None),
            height=MDApp.get_running_app().root.height*.8,
            pos_hint={"center_x": .5, "center_y": .5},
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.popup_base = self.popup_base
        self.popup_base.open()
    
    def open_meal_options_dialog(self,listitem):
        c = Meal_Options_Dialog(meal_id=listitem.meal_id,
                                meal_name=listitem.text)
        self.popup_base = MDDialog(
            title="Meal Options",
            type="custom",
            size_hint=(.9, None),
            pos_hint={"center_x": .5, "center_y": .5},
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.popup_base = self.popup_base
        self.popup_base.open()

class Filter_Dialog(MDBoxLayout):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meals_screen = MDApp.get_running_app().root.ids.meals_screen
    
    def cancel(self):
        self.popup_base.dismiss()
    
    def apply_filter(self):
        self.meals_screen.breakfast = self.ids.breakfast.active
        self.meals_screen.lunch = self.ids.lunch.active
        self.meals_screen.dinner = self.ids.dinner.active
        self.meals_screen.snack = self.ids.snack.active
        self.meals_screen.hot_cold = self.ids.hot_cold.active
        self.meals_screen.sweet_savory = self.ids.sweet_savory.active
        self.meals_screen.show_all_meals = False
        self.meals_screen.refresh_internal_list()
        self.meals_screen.refresh_display_list()
        self.popup_base.dismiss()

    def activate_deactivate_sweet_savory_filter(self,state):
        if state == "down":
            self.ids.sweet_savory.disabled = False
            self.ids.label_sweet.text_color = 1,1,1,1
            self.ids.label_savory.text_color = 1,1,1,1
            self.meals_screen.ignore_sweet_savory = False
        else:
            self.ids.sweet_savory.disabled = True
            self.ids.label_sweet.text_color = 1,1,1,.25
            self.ids.label_savory.text_color = 1,1,1,.25
            self.meals_screen.ignore_sweet_savory = True
    
    def activate_deactivate_hot_cold_filter(self,state):
        if state == "down":
            self.ids.hot_cold.disabled = False
            self.ids.label_hot.text_color = 1,1,1,1
            self.ids.label_cold.text_color = 1,1,1,1
            self.meals_screen.ignore_hot_cold = False
        else:
            self.ids.hot_cold.disabled = True
            self.ids.label_hot.text_color = 1,1,1,.25
            self.ids.label_cold.text_color = 1,1,1,.25
            self.meals_screen.ignore_hot_cold = True

    def reset_filter(self):
        self.meals_screen.show_all_meals = True
        self.meals_screen.ignore_sweet_savory = True
        self.meals_screen.ignore_hot_cold = True
        self.meals_screen.breakfast = False
        self.meals_screen.lunch = False
        self.meals_screen.dinner = False
        self.meals_screen.snack = False
        self.meals_screen.hot_cold = False
        self.meals_screen.sweet_savory = False
        self.meals_screen.refresh_internal_list()
        self.meals_screen.refresh_display_list()
        self.popup_base.dismiss()
    
    def check_apply_filter_button_validity(self):
        if self.ids.breakfast.active or self.ids.lunch.active or self.ids.dinner.active or self.ids.snack.active:
            self.ids.apply_filter_button.disabled = False
        else:
            self.ids.apply_filter_button.disabled = True

class Add_Meal_Dialog(MDBoxLayout):
    
    def __init__(self, *args, **kwargs):
        super(Add_Meal_Dialog, self).__init__(*args, **kwargs)
        self.meal_screen = MDApp.get_running_app().root.ids.meals_screen
    
    def cancel(self):
        self.popup_base.dismiss()

    def check_add_meal_button_validity(self):
        if any([self.ids.breakfast.active,self.ids.lunch.active,self.ids.dinner.active,self.ids.snack.active]) and self.ids.meal_name.text != "":
            self.ids.add_meal_button.disabled = False
        else:
            self.ids.add_meal_button.disabled = True

    def add_meal(self):
        s = Session()
        meal_query = s.query(Meal).filter(Meal.name == self.ids.meal_name.text).first()
        if meal_query:
            s.close()
            self.open_meal_already_exists_dialog(meal_query)
        else:
            new_meal = Meal(
                name = self.ids.meal_name.text,
                breakfast = self.ids.breakfast.active,
                lunch = self.ids.lunch.active,
                dinner = self.ids.dinner.active,
                snack = self.ids.snack.active,
                hot_cold = self.ids.hot_cold.active,
                sweet_savory = self.ids.sweet_savory.active
            )
            s.add(new_meal)
            s.commit()
            s.close()
            self.meal_screen.refresh_internal_list()
            self.meal_screen.refresh_display_list()
            self.popup_base.dismiss()

    def open_meal_already_exists_dialog(self,meal):
        c = Meal_Already_Exists_Dialog(meal)
        self.popup_layer2 = MDDialog(
            title=f"{meal.name} Already Exists, would you like to update it?",
            type="custom",
            content_cls=c,
            size_hint_x=.9,
            radius=[20, 7, 20, 7]
        )
        c.popup_base = self.popup_base
        c.popup_layer2 = self.popup_layer2
        self.popup_layer2.open()

class Meal_Already_Exists_Dialog(MDBoxLayout):

    def __init__(self, meal, *args, **kwargs):
        super(Meal_Already_Exists_Dialog, self).__init__(*args, **kwargs)
        self.meal = meal
    
    def cancel(self):
        self.popup_layer2.dismiss()
    
    def update(self):
        pass # should open the display meal screen that is yet to be added

class Meal_Options_Dialog(MDBoxLayout):

    def __init__(self, meal_id, meal_name, *args, **kwargs):
        super(Meal_Options_Dialog, self).__init__(*args, **kwargs)
        self.meal_id = meal_id
        self.meal_name = meal_name
        self.screen_manager = MDApp.get_running_app().root.ids.screen_manager

    def open_delete_meal_dialog(self):
        c = Delete_Meal_Dialog(meal_id=self.meal_id)
        self.popup_layer2 = MDDialog(
            title=f"Delete {self.meal_name} ?",
            type="custom",
            content_cls=c,
            size_hint=(.9, None),
            height=dp(75),
            radius=[20, 7, 20, 7]
        )
        c.popup_base = self.popup_base
        c.popup_layer2 = self.popup_layer2
        self.popup_layer2.open()
    
    def edit(self):
        self.screen_manager.add_widget(
            Display_Meal_Screen(meal_id=self.meal_id)
        )
        self.screen_manager.get_screen("Display_Meal_Screen").ids.top_app_bar.title = self.meal_name
        self.screen_manager.get_screen("Display_Meal_Screen").refresh_internal_ingredient_list()
        self.screen_manager.get_screen("Display_Meal_Screen").refresh_display_ingredient_list()
        self.screen_manager.current = "Display_Meal_Screen"
        self.screen_manager.transition.direction = "left"
        self.popup_base.dismiss()

class Delete_Meal_Dialog(MDBoxLayout):

    def __init__(self, meal_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meal_id = meal_id
        self.meal_screen = MDApp.get_running_app().root.ids.meals_screen
    def cancel(self):
        self.popup_layer2.dismiss()
    
    def delete(self):
        s = Session()
        s.delete(s.query(Meal).get(self.meal_id))
        s.commit()
        s.close()
        self.meal_screen.refresh_internal_list()
        self.meal_screen.refresh_display_list()
        self.popup_layer2.dismiss()
        self.popup_base.dismiss()

class Display_Meal_Screen(MDScreen):

    def __init__(self, meal_id, *args, **kwargs):
        super(Display_Meal_Screen, self).__init__(*args, **kwargs)
        s = Session()
        self.ing_icon_dict = {
            "Meat":"food-steak",
            "Fish":"fish",
            "Grains / Bread":"bread-slice-outline",
            "Dairy":"cheese",
            "Vegetable":"carrot",
            "Fruit":"food-apple-outline",
            "Nuts / Seeds":"peanut",
            "Oil / Fats":"bottle-tonic",
            "Condiment":"soy-sauce",
            "Spice":"shaker-outline"
        }
        self.ing_icon_color_dict = {
            "All":(1,1,1,1),
            "Meat":(.39,.24,.04,1),
            "Fish":(1,.61,.39,1),
            "Grains / Bread":(1,.67,.35,1),
            "Dairy":(1,.78,.24,1),
            "Vegetable":(1,.55,.1,1),
            "Fruit":(.9,.16,0,1),
            "Nuts / Seeds":(.78,.53,0,1),
            "Oil / Fats":(.96,.75,0,1),
            "Condiment":(.78,.69,.24,1),
            "Spice":(.95,.95,.99,1)
        }
        self.screen_manager = MDApp.get_running_app().root.ids.screen_manager
        self.meal_id = meal_id
        self.asc_obj_id_list = [i.id for i in s.query(Association).filter(Association.meal_id == self.meal_id).all()]
        self.all_ingredient_id_list = [i.id for i in s.query(Ingredient).all()]
        s.close()

    def transition_to_meal_plan_screen(self):
        MDApp.get_running_app().root.ids.meals_screen.refresh_internal_list()
        MDApp.get_running_app().root.ids.meals_screen.refresh_display_list()
        MDApp.get_running_app().root.ids.screen_manager.current = "Meals_Screen"
        MDApp.get_running_app().root.ids.screen_manager.transition.direction = "right"

    def remove_display_screen(self):
        self.screen_manager.remove_widget(self.screen_manager.current_screen)

    def refresh_internal_ingredient_list(self):
        s = Session()
        self.asc_obj_id_list = [i.id for i in s.query(Association).filter(Association.meal_id == self.meal_id).all()]
        self.meal_ingredient_id_list = [i.ingredient_id for i in s.query(Association).filter(Association.meal_id == self.meal_id).all()]
        s.close()

    def refresh_display_ingredient_list(self):
        self.ids.meal_ingredient_list.clear_widgets()
        s = Session()
        for i in s.query(Association).filter(Association.meal_id == self.meal_id).all():
            s.add(i)
            Item = ThreeLineAvatarIconIDSListItem(
                    asc_obj_id=i.id,
                    meal_id=i.meal_id,
                    ingredient_id=i.ingredient_id,
                    text=i.ingredient.name,
                    secondary_text=f"{i.ingredient.calories * i.amount_numerator / 100 if i.ingredient.unit == 'gram' or i.ingredient.unit == 'ml' else round(i.ingredient.calories * i.amount_numerator / i.amount_denominator,2)} kcals",
                    tertiary_text=f"{i.amount_numerator} {i.ingredient.unit}{'s' if i.amount_numerator != 1 else ''}" if i.ingredient.unit != "piece" else f"{str(int(i.amount_numerator/i.amount_denominator))} " + f"{str(i.amount_numerator%i.amount_denominator) + '/' + str(i.amount_denominator) if i.amount_numerator%i.amount_denominator != 0 else ''} {i.ingredient.unit}{'s' if i.amount_numerator != i.amount_denominator else ''}",
                    on_release=self.open_meal_ingredient_options_dialog,
                )
            Icon = IconLeftWidget(
                icon=self.ing_icon_dict[i.ingredient.type],
                theme_text_color="Custom",
                text_color=self.ing_icon_color_dict[i.ingredient.type]
                )
            Item.add_widget(Icon)
            self.ids.meal_ingredient_list.add_widget(Item)
        Add_Item = OneLineIconListItem(
            text="Add Ingredient",
            on_release=self.open_add_meal_ingredient_dialog
        )
        Add_Item.add_widget(
            IconLeftWidget(
                icon="plus"
            )
        )
        self.ids.meal_ingredient_list.add_widget(Add_Item)
        s.close()

    def open_meal_ingredient_options_dialog(self, listitem):
        c = Meal_Ingredient_Options_Dialog(asc_obj_id=listitem.asc_obj_id,ing_name=listitem.text)
        self.popup_base_ing_opt = MDDialog(
            title=f"{listitem.text} Options",
            type="custom",
            size_hint=(.9, None),
            pos_hint={"center_x": .5, "center_y": .5},
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.display_meal_screen = self
        c.popup_base_ing_opt = self.popup_base_ing_opt
        self.popup_base_ing_opt.open()

    def open_add_meal_ingredient_dialog(self,junk):
        c = Add_Meal_Ingredient_Dialog(meal_id=self.meal_id,all_ingredient_id_list=self.all_ingredient_id_list)
        self.popup_base_add_ing = MDDialog(
            title="Add Ingredient",
            type="custom",
            size_hint=(.9, None),
            height=MDApp.get_running_app().root.height*.8,
            pos_hint={"center_x": .5, "center_y": .5},
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.refresh_all_ingredients_list()
        c.display_meal_screen = self
        c.popup_base_add_ing = self.popup_base_add_ing
        self.popup_base_add_ing.open()

class Add_Meal_Ingredient_Dialog(MDBoxLayout):

    def __init__(self, meal_id, all_ingredient_id_list, *args, **kwargs):
        super(Add_Meal_Ingredient_Dialog, self).__init__(*args, **kwargs)
        self.all_ingredient_id_list = all_ingredient_id_list # should never change
        self.display_ingredient_id_list = all_ingredient_id_list        # is supposed to be modified based on the filter settings
        self.meal_id = meal_id                               # should never change
        s = Session()
        self.meal_name = s.query(Meal).filter(Meal.id == self.meal_id).first().name
        s.close()
        self.ing_icon_dict = {
            "All":"filter-variant",
            "Meat":"food-steak",
            "Fish":"fish",
            "Grains / Bread":"bread-slice-outline",
            "Dairy":"cheese",
            "Vegetable":"carrot",
            "Fruit":"food-apple-outline",
            "Nuts / Seeds":"peanut",
            "Oil / Fats":"bottle-tonic",
            "Condiment":"soy-sauce",
            "Spice":"shaker-outline"
        }
        self.ing_icon_color_dict = {
            "All":(1,1,1,1),
            "Meat":(.39,.24,.04,1),
            "Fish":(1,.61,.39,1),
            "Grains / Bread":(1,.67,.35,1),
            "Dairy":(1,.78,.24,1),
            "Vegetable":(1,.55,.1,1),
            "Fruit":(.9,.16,0,1),
            "Nuts / Seeds":(.78,.53,0,1),
            "Oil / Fats":(.96,.75,0,1),
            "Condiment":(.78,.69,.24,1),
            "Spice":(.95,.95,.99,1)
        }
        self.sort_value = 5             # default value (sorts by type) others should be 2, 5, 6, 7 (cals, fats, carbs, prots)
        self.sort_order = True
        self.filter_type = "All"

    def cancel(self):
        self.popup_base_add_ing.dismiss()

    def open_filter_dropdown(self):
        self.choices_filter = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "All",
                "icon":"filter-variant",
                "height": dp(56),
                "on_release": lambda x="filter-variant",y="All": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Meat",
                "icon": "food-steak",
                "height": dp(56),
                "on_release": lambda x="food-steak",y="Meat": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fish",
                "icon": "fish",
                "height": dp(56),
                "on_release": lambda x="fish",y="Fish": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Grains / Bread",
                "icon": "bread-slice-outline",
                "height": dp(56),
                "on_release": lambda x="bread-slice-outline",y="Grains / Bread": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Dairy",
                "icon": "cheese",
                "height": dp(56),
                "on_release": lambda x="cheese",y="Dairy": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Vegetable",
                "icon": "carrot",
                "height": dp(56),
                "on_release": lambda x="carrot",y="Vegetable": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fruit",
                "icon": "food-apple-outline",
                "height": dp(56),
                "on_release": lambda x="food-apple-outline",y="Fruit": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Nuts / Seeds",
                "icon": "peanut",
                "height": dp(56),
                "on_release": lambda x="peanut",y="Nuts / Seeds": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Oil / Fats",
                "icon": "bottle-tonic",
                "height": dp(56),
                "on_release": lambda x="bottle-tonic",y="Oil / Fats": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Condiment",
                "icon": "soy-sauce",
                "height": dp(56),
                "on_release": lambda x="soy-sauce",y="Condiment": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Spice",
                "icon": "shaker-outline",
                "height": dp(56),
                "on_release": lambda x="shaker-outline",y="Spice": self.set_filter_icon(x,y)
            },
        ]
        self.menu_list_type = MDDropdownMenu(
            caller=self.ids.filter,
            items=self.choices_filter,
            position="auto",
            width_mult=4
        )
        self.menu_list_type.open()

    def set_filter_icon(self, icon, text):
        self.ids.filter.icon = icon
        self.ids.filter.text_color = self.ing_icon_color_dict[text]
        self.ids.filter.text = text
        self.refresh_internal_list()
        self.menu_list_type.dismiss()

    def open_filter_menu(self):
        c = Ingredient_List_Filter_For_Add_Ing_To_Meal_Dialog()
        self.popup_ingredient_list_filter_for_add_ing_to_meal = MDDialog(
            title="Filter and Sort settings",
            type="custom",
            content_cls=c,
            size_hint=(.9, None),
            radius=[20, 7, 20, 7],
            pos_hint={"center_x": .5, "center_y": .5}
        )
        c.logic = self
        c.sort_value = self.sort_value
        c.sort_order = self.sort_order # bool // False = ascending, True = descending
        c.filter_type = self.filter_type # "Meat", "Fish", "Grains / Bread", "Dairy", "Vegetable", "Fruit", "Nuts / Seeds", "Oil / Fats", "Condiment", "Spice", "All"
        c.popup_ingredient_list_filter_for_add_ing_to_meal = self.popup_ingredient_list_filter_for_add_ing_to_meal
        c.set_initial_settings()
        self.popup_ingredient_list_filter_for_add_ing_to_meal.open()
    def refresh_all_ingredients_list(self): # this should only be called when an ingredient is added or deleted or edited and on start to sort the list
        s = Session()
        self.all_ingredient_id_and_stats_list = [[i.id,i.name,i.unit,i.divisible_by,i.calories,i.type,i.fats,i.carbohydrates,i.proteins] for i in s.query(Ingredient).all()]
        s.close()
        self.refresh_internal_list()

    def refresh_internal_list(self):
        if self.filter_type == "All":
            self.all_ingredient_id_and_stats_list_filtered = self.all_ingredient_id_and_stats_list
        else:
            self.all_ingredient_id_and_stats_list_filtered = list(filter(lambda x: x[5] == self.filter_type, self.all_ingredient_id_and_stats_list))
        self.display_ingredient_id_and_stats_list = sorted(self.all_ingredient_id_and_stats_list_filtered,key = lambda x: x[self.sort_value],reverse = self.sort_order)
        self.refresh_display_list() if self.ids else None

    def refresh_display_list(self):
        self.ing_search = self.ids.ing_search.text
        self.ids.ingredients_display_list.clear_widgets()
        for i in self.display_ingredient_id_and_stats_list:
            if self.ing_search.lower() in i[1].lower():
                Item = ThreeLineAvatarIconIDSListItem(
                    ingredient_id=i[0],
                    meal_id=self.meal_id,
                    text=i[1],
                    ing_unit=i[2],
                    divisible_by=i[3],
                    secondary_text=f"{i[2]} kcals" if self.sort_value == 4 or self.sort_value == 5 else f"{i[6]} grams of fat" if self.sort_value == 6 else f"{i[7]} grams of carbohydrates" if self.sort_value == 7 else f"{i[8]} grams of protein",
                    tertiary_text=f"per {'100' if i[2] =='gram' or i[2] =='ml' else ''} {i[2]}{'s' if i[2] == 'gram' or i[2] == 'ml' else ''}",
                    on_release=self.open_ingredient_amount_input_dialog,
                )
                Icon = IconLeftWidget(
                    icon=self.ing_icon_dict[i[5]],
                    theme_text_color="Custom",
                    text_color=self.ing_icon_color_dict[i[5]],
                    )
                Item.add_widget(Icon)
                self.ids.ingredients_display_list.add_widget(Item)
    
    def open_ingredient_amount_input_dialog(self,listitem):
        s = Session()
        asc_obj = s.query(Association).filter(Association.ingredient_id==listitem.ingredient_id,Association.meal_id==listitem.meal_id).first()
        if asc_obj:
            asc_obj_id = asc_obj.id
            s.close()
            c = Ingredient_Is_Already_In_Meal_Dialog(listitem=listitem,
                                                     asc_obj_id=asc_obj_id)
            self.popup_ingredient_is_already_in_meal = MDDialog(
                title=f"{listitem.text} is already in {self.meal_name}, would you like to change the amount?",
                type="custom",
                size_hint=(.9, None),
                height=MDApp.get_running_app().root.height*.8,
                pos_hint={"center_x": .5, "center_y": .5},
                content_cls=c,
                radius=[20, 7, 20, 7]
            )
            c.display_meal_screen = self.display_meal_screen
            c.popup_ingredient_is_already_in_meal = self.popup_ingredient_is_already_in_meal
            self.popup_ingredient_is_already_in_meal.open()
        else:
            s.close()
            if listitem.ing_unit == "gram" or listitem.ing_unit == "ml":
                c = Add_Ing_To_Meal_Unit_Gram_Ml_Dialog(caller_already_exists=False,
                                                        caller_change=False,
                                                        asc_obj_id=None,
                                                        ingredient_id=listitem.ingredient_id,
                                                        meal_id=listitem.meal_id)
                self.popup_add_ing_gram_ml = MDDialog(
                    title=f"Add {listitem.text}",
                    type="custom",
                    size_hint=(.9, None),
                    height=MDApp.get_running_app().root.height*.8,
                    pos_hint={"center_x": .5, "center_y": .5},
                    content_cls=c,
                    radius=[20, 7, 20, 7]
                )
                c.display_meal_screen = self.display_meal_screen
                c.popup_add_ing_gram_ml = self.popup_add_ing_gram_ml
                c.ids.unit_label.text = listitem.ing_unit
                c.ids.ing_stats_label.text = listitem.text
                c.ids.meal_stats_label.text = self.meal_name
                c.decrement_amount_button_check_validity()
                c.refresh_stats()
                c.confirm_button_check_validity()
                self.popup_add_ing_gram_ml.open()
            else:
                if listitem.divisible_by > 1:
                    c = Add_Ing_To_Meal_Unit_Piece_Divisible_Dialog(caller_already_exists=False,
                                                                    caller_change=False,
                                                                    asc_obj_id=None,
                                                                    ingredient_id=listitem.ingredient_id,
                                                                    meal_id=listitem.meal_id)
                    self.popup_add_ing_piece_divisible = MDDialog(
                        title=f"Add {listitem.text}",
                        type="custom",
                        size_hint=(.9, None),
                        height=MDApp.get_running_app().root.height*.8,
                        pos_hint={"center_x": .5, "center_y": .5},
                        content_cls=c,
                        radius=[20, 7, 20, 7]
                    )
                    c.display_meal_screen = self.display_meal_screen
                    c.popup_add_ing_piece_divisible = self.popup_add_ing_piece_divisible
                    c.ids.pieces_amount_label.text = "0"
                    c.ids.pieces_amount_label.number = 0
                    c.ids.slices_amount_label.numerator = 0
                    c.ids.slices_amount_label.denominator = listitem.divisible_by
                    c.ids.ing_stats_label.text = listitem.text
                    c.ids.meal_stats_label.text = self.meal_name
                    c.refresh_stats()
                    c.confirm_button_check_validity()
                    self.popup_add_ing_piece_divisible.open()
                else:
                    c = Add_Ing_To_Meal_Unit_Piece_Indivisible_Dialog(caller_already_exists=False,
                                                                      caller_change=False,
                                                                      asc_obj_id=None,
                                                                      ingredient_id=listitem.ingredient_id,
                                                                      meal_id=listitem.meal_id)
                    self.popup_add_ing_piece_indivisible = MDDialog(
                        title=f"Add {listitem.text}",
                        type="custom",
                        size_hint=(.9, None),
                        height=MDApp.get_running_app().root.height*.8,
                        pos_hint={"center_x": .5, "center_y": .5},
                        content_cls=c,
                        radius=[20, 7, 20, 7]
                    )
                    c.display_meal_screen = self.display_meal_screen
                    c.popup_add_ing_piece_indivisible = self.popup_add_ing_piece_indivisible
                    c.ids.pieces_amount_label.text = "0"
                    c.ids.pieces_amount_label.number = 0
                    c.ids.ing_stats_label.text = listitem.text
                    c.ids.meal_stats_label.text = self.meal_name
                    c.refresh_stats()
                    c.confirm_button_check_validity()
                    self.popup_add_ing_piece_indivisible.open()

class Ingredient_List_Filter_For_Add_Ing_To_Meal_Dialog(MDBoxLayout):

    def __init__(self, *args, **kwargs):
        super(Ingredient_List_Filter_For_Add_Ing_To_Meal_Dialog, self).__init__(*args, **kwargs)
        self.ing_icon_dict = {
            "All":"filter-variant",
            "Meat":"food-steak",
            "Fish":"fish",
            "Grains / Bread":"bread-slice-outline",
            "Dairy":"cheese",
            "Vegetable":"carrot",
            "Fruit":"food-apple-outline",
            "Nuts / Seeds":"peanut",
            "Oil / Fats":"bottle-tonic",
            "Condiment":"soy-sauce",
            "Spice":"shaker-outline"
        }
        self.ing_icon_color_dict = {
            "All":(1,1,1,1),
            "Meat":(.39,.24,.04,1),
            "Fish":(1,.61,.39,1),
            "Grains / Bread":(1,.67,.35,1),
            "Dairy":(1,.78,.24,1),
            "Vegetable":(1,.55,.1,1),
            "Fruit":(.9,.16,0,1),
            "Nuts / Seeds":(.78,.53,0,1),
            "Oil / Fats":(.96,.75,0,1),
            "Condiment":(.78,.69,.24,1),
            "Spice":(.95,.95,.99,1)
        }
    
    def set_initial_settings(self):
        if self.sort_value == 4:
            self.ids.sort_by_calories.active = True
            self.ids.sort_by_calories_label.text_color = (1,1,1,1)
        elif self.sort_value == 6:
            self.ids.sort_by_fats.active = True
            self.ids.sort_by_fats_label.text_color = (1,1,1,1)
        elif self.sort_value == 7:
            self.ids.sort_by_carbohydrates.active = True
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,1)
        elif self.sort_value == 8:
            self.ids.sort_by_proteins.active = True
            self.ids.sort_by_proteins_label.text_color = (1,1,1,1)
        if self.sort_order:
            self.ids.sorting_direction.icon = "sort-descending"
            self.ids.sort_order_label.text = "High to Low"
        else:
            self.ids.sorting_direction.icon = "sort-ascending"
            self.ids.sort_order_label.text = "Low to High"
        self.ids.ingredient_type_filter.icon = self.ing_icon_dict[self.filter_type]
        self.ids.ingredient_type_filter.text_color = self.ing_icon_color_dict[self.filter_type]

    def cancel(self):
        self.popup_ingredient_list_filter_for_add_ing_to_meal.dismiss()

    def check_calories(self,instance,value):
        if value:
            self.ids.sort_by_fats.active = False
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates.active = False
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins.active = False
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)
            self.ids.sort_by_calories_label.text_color = (1,1,1,1)
            self.sort_value = 4
        else:
            self.sort_value = 5
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)

    def check_fats(self,instance,value):
        if value:
            self.ids.sort_by_calories.active = False
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates.active = False
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins.active = False
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)
            self.ids.sort_by_fats_label.text_color = (1,1,1,1)
            self.sort_value = 6
        else:
            self.sort_value = 5
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
    
    def check_carbohydrates(self,instance,value):
        if value:
            self.ids.sort_by_calories.active = False
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)
            self.ids.sort_by_fats.active = False
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins.active = False
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,1)
            self.sort_value = 7
        else:
            self.sort_value = 5
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)

    def check_proteins(self,instance,value):
        if value:
            self.ids.sort_by_calories.active = False
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)
            self.ids.sort_by_fats.active = False
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates.active = False
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins_label.text_color = (1,1,1,1)
            self.sort_value = 8
        else:
            self.sort_value = 5
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)

    def set_sort_order(self):
        self.ids.sorting_direction.icon = "sort-ascending" if self.ids.sorting_direction.icon == "sort-descending" else "sort-descending"
        self.sort_order = False if self.ids.sorting_direction.icon == "sort-ascending" else True
        self.ids.sort_order_label.text = "High to Low" if self.sort_order else "Low to High"

    def open_filter_dropdown(self):
        self.choices_filter = [
            {
                "viewclass": "OneLineAvatarIconListItem",
                "text": "All",
                "icon":"filter-variant",
                "height": dp(56),
                "on_release": lambda x="filter-variant",y="All": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineAvatarIconListItem",
                "text": "Meat",
                "icon": "food-steak",
                "height": dp(56),
                "on_release": lambda x="food-steak",y="Meat": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fish",
                "icon": "fish",
                "height": dp(56),
                "on_release": lambda x="fish",y="Fish": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Grains / Bread",
                "icon": "bread-slice-outline",
                "height": dp(56),
                "on_release": lambda x="bread-slice-outline",y="Grains / Bread": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Dairy",
                "icon": "cheese",
                "height": dp(56),
                "on_release": lambda x="cheese",y="Dairy": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Vegetable",
                "icon": "carrot",
                "height": dp(56),
                "on_release": lambda x="carrot",y="Vegetable": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fruit",
                "icon": "food-apple-outline",
                "height": dp(56),
                "on_release": lambda x="food-apple-outline",y="Fruit": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Nuts / Seeds",
                "icon": "peanut",
                "height": dp(56),
                "on_release": lambda x="peanut",y="Nuts / Seeds": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Oil / Fats",
                "icon": "bottle-tonic",
                "height": dp(56),
                "on_release": lambda x="bottle-tonic",y="Oil / Fats": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Condiment",
                "icon": "soy-sauce",
                "height": dp(56),
                "on_release": lambda x="soy-sauce",y="Condiment": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Spice",
                "icon": "shaker-outline",
                "height": dp(56),
                "on_release": lambda x="shaker-outline",y="Spice": self.set_filter_icon(x,y)
            },
        ]
        self.menu_list_type = MDDropdownMenu(
            caller=self.ids.ingredient_type_filter,
            items=self.choices_filter,
            position="auto",
            width_mult=4
        )
        self.menu_list_type.open()

    def set_filter_icon(self, icon, ing_type):
        self.ids.ingredient_type_filter.icon = icon
        self.ids.ingredient_type_filter.text_color = self.ing_icon_color_dict[ing_type]
        self.filter_type = ing_type
        self.menu_list_type.dismiss()

    def apply_filter(self):
        self.logic.sort_value = self.sort_value
        self.logic.sort_order = self.sort_order
        self.logic.filter_type = self.filter_type
        self.logic.refresh_internal_list()
        self.popup_ingredient_list_filter_for_add_ing_to_meal.dismiss()

class Ingredient_Is_Already_In_Meal_Dialog(MDBoxLayout):

    def __init__(self, listitem, asc_obj_id, *args, **kwargs):
        super(Ingredient_Is_Already_In_Meal_Dialog, self).__init__(*args, **kwargs)
        self.listitem = listitem
        self.asc_obj_id = asc_obj_id
        s = Session()
        asc_obj = s.query(Association).get(self.asc_obj_id)
        self.meal_name = asc_obj.meal.name
        self.amount_numerator = asc_obj.amount_numerator
        self.amount_denominator = asc_obj.amount_denominator
        s.close()

    def cancel(self):
        self.popup_ingredient_is_already_in_meal.dismiss()
    
    def change_amount(self):
        if self.listitem.ing_unit == "gram" or self.listitem.ing_unit == "ml":
            c = Add_Ing_To_Meal_Unit_Gram_Ml_Dialog(caller_already_exists=True,
                                                    caller_change=False,
                                                    asc_obj_id=self.asc_obj_id,
                                                    ingredient_id=self.listitem.ingredient_id,
                                                    meal_id=self.listitem.meal_id)
            self.popup_add_ing_gram_ml = MDDialog(
                title=f"Change amount of {self.listitem.text}",
                type="custom",
                size_hint=(.9, None),
                height=MDApp.get_running_app().root.height*.8,
                pos_hint={"center_x": .5, "center_y": .5},
                content_cls=c,
                radius=[20, 7, 20, 7]
            )
            c.popup_ingredient_is_already_in_meal = self.popup_ingredient_is_already_in_meal
            c.display_meal_screen = self.display_meal_screen
            c.popup_add_ing_gram_ml = self.popup_add_ing_gram_ml
            c.ids.amount_input.text = str(self.amount_numerator)
            c.decrement_amount_button_check_validity()
            c.ids.unit_label.text = self.listitem.ing_unit
            c.ids.ing_stats_label.text = self.listitem.text
            c.ids.meal_stats_label.text = self.meal_name
            c.refresh_stats()
            c.confirm_button_check_validity()
            self.popup_add_ing_gram_ml.open()
        else:
            if self.listitem.divisible_by > 1:
                c = Add_Ing_To_Meal_Unit_Piece_Divisible_Dialog(caller_already_exists=True,
                                                                caller_change=False,
                                                                asc_obj_id=self.asc_obj_id,
                                                                ingredient_id=self.listitem.ingredient_id,
                                                                meal_id=self.listitem.meal_id)
                self.popup_add_ing_piece_divisible = MDDialog(
                    title=f"Change amount of {self.listitem.text}",
                    type="custom",
                    size_hint=(.9, None),
                    height=MDApp.get_running_app().root.height*.8,
                    pos_hint={"center_x": .5, "center_y": .5},
                    content_cls=c,
                    radius=[20, 7, 20, 7]
                )
                c.popup_ingredient_is_already_in_meal = self.popup_ingredient_is_already_in_meal
                c.display_meal_screen = self.display_meal_screen
                c.popup_add_ing_piece_divisible = self.popup_add_ing_piece_divisible
                c.ids.pieces_amount_label.text = str(int(self.amount_numerator / self.listitem.divisible_by))
                c.ids.pieces_amount_label.number = int(self.amount_numerator / self.listitem.divisible_by)
                c.ids.slices_amount_label.numerator = int(self.amount_numerator % self.listitem.divisible_by)
                c.ids.slices_amount_label.denominator = self.listitem.divisible_by
                c.ids.ing_stats_label.text = self.listitem.text
                c.ids.meal_stats_label.text = self.meal_name
                c.refresh_stats()
                c.confirm_button_check_validity()
                self.popup_add_ing_piece_divisible.open()
            else:
                c = Add_Ing_To_Meal_Unit_Piece_Indivisible_Dialog(caller_already_exists=True,
                                                                  caller_change=False,
                                                                  asc_obj_id=self.asc_obj_id,
                                                                  ingredient_id=self.listitem.ingredient_id,
                                                                  meal_id=self.listitem.meal_id)
                self.popup_add_ing_piece_indivisible = MDDialog(
                    title=f"Change amount of {self.listitem.text}",
                    type="custom",
                    size_hint=(.9, None),
                    height=MDApp.get_running_app().root.height*.8,
                    pos_hint={"center_x": .5, "center_y": .5},
                    content_cls=c,
                    radius=[20, 7, 20, 7]
                )
                c.popup_ingredient_is_already_in_meal = self.popup_ingredient_is_already_in_meal
                c.display_meal_screen = self.display_meal_screen
                c.popup_add_ing_piece_indivisible = self.popup_add_ing_piece_indivisible
                c.ids.pieces_amount_label.text = str(self.amount_numerator)
                c.ids.pieces_amount_label.number = self.amount_numerator
                c.ids.ing_stats_label.text = self.listitem.text
                c.ids.meal_stats_label.text = self.meal_name
                c.refresh_stats()
                c.confirm_button_check_validity()
                self.popup_add_ing_piece_indivisible.open()

class Add_Ing_To_Meal_Unit_Piece_Divisible_Dialog(MDBoxLayout):

    def __init__(self, asc_obj_id, ingredient_id, meal_id, caller_already_exists:bool, caller_change:bool, *args, **kwargs):
        super(Add_Ing_To_Meal_Unit_Piece_Divisible_Dialog, self).__init__(*args, **kwargs)
        self.asc_obj_id = asc_obj_id
        self.caller_already_exists = caller_already_exists
        self.caller_change = caller_change
        self.ingredient_id = ingredient_id
        self.meal_id = meal_id
        s = Session()
        self.amount_numerator = s.query(Association).get(self.asc_obj_id).amount_numerator if self.caller_already_exists or self.caller_change else None
        self.amount_denominator = s.query(Association).get(self.asc_obj_id).amount_denominator if self.caller_already_exists or self.caller_change else None

    def cancel(self):
        if self.caller_already_exists:
            self.popup_add_ing_piece_divisible.dismiss()
            self.popup_ingredient_is_already_in_meal.dismiss()
        elif self.caller_change:
            self.popup_add_ing_piece_divisible.dismiss()
            self.popup_base_ing_opt.dismiss()
        else:
            self.popup_add_ing_piece_divisible.dismiss()

    def confirm_button_check_validity(self):
        if self.ids.pieces_amount_label.number == 0 and self.ids.slices_amount_label.numerator == 0:
            self.ids.confirm_button.disabled = True
        else:
            self.ids.confirm_button.disabled = False

    def increment_pieces(self):
        self.ids.pieces_amount_label.number += 1
        self.confirm_button_check_validity()

    def decrement_pieces(self):
        if self.ids.pieces_amount_label.number > 0:
            self.ids.pieces_amount_label.number -= 1
        self.confirm_button_check_validity()

    def increment_slices(self):
        if self.ids.slices_amount_label.numerator < self.ingredient.divisible_by - 1:
            self.ids.slices_amount_label.numerator += 1
            self.confirm_button_check_validity()
        else:
            self.ids.slices_amount_label.numerator = 0
            self.increment_pieces()

    def decrement_slices(self):
        if self.ids.slices_amount_label.numerator > 0:
            self.ids.slices_amount_label.numerator -= 1
            self.confirm_button_check_validity()
        elif self.ids.slices_amount_label.numerator == 0 and self.ids.pieces_amount_label.number != 0:
            self.ids.slices_amount_label.numerator = self.ingredient.divisible_by - 1
            self.decrement_pieces()

    def refresh_stats(self):
        s = Session()
        self.ingredient = s.query(Ingredient).get(self.ingredient_id)
        self.meal = s.query(Meal).get(self.meal_id)
        self.ids.ing_calories.text = str(round(self.ingredient.calories * self.ids.pieces_amount_label.number + self.ingredient.calories * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))
        self.ids.ing_fats.text = f"{str(round(self.ingredient.fats * self.ids.pieces_amount_label.number + self.ingredient.fats * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))} g"
        self.ids.ing_carbohydrates.text = f"{str(round(self.ingredient.carbohydrates * self.ids.pieces_amount_label.number + self.ingredient.carbohydrates * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))} g"
        self.ids.ing_proteins.text = f"{str(round(self.ingredient.proteins * self.ids.pieces_amount_label.number + self.ingredient.proteins * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))} g"
        if self.caller_already_exists or self.caller_change:
            self.ids.meal_calories.text = str(round((self.meal.calories - self.ingredient.calories * self.amount_numerator / self.amount_denominator) + self.ingredient.calories * self.ids.pieces_amount_label.number + self.ingredient.calories * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))
            self.ids.meal_fats.text = f"{str(round((self.meal.fats - self.ingredient.fats * self.amount_numerator / self.amount_denominator) + self.ingredient.fats * self.ids.pieces_amount_label.number + self.ingredient.fats * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))} g"
            self.ids.meal_carbohydrates.text = f"{str(round((self.meal.carbohydrates - self.ingredient.carbohydrates * self.amount_numerator / self.amount_denominator) + self.ingredient.carbohydrates * self.ids.pieces_amount_label.number + self.ingredient.carbohydrates * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))} g"
            self.ids.meal_proteins.text = f"{str(round((self.meal.proteins - self.ingredient.proteins * self.amount_numerator / self.amount_denominator) + self.ingredient.proteins * self.ids.pieces_amount_label.number + self.ingredient.proteins * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))} g"
        else:
            self.ids.meal_calories.text = str(round(self.meal.calories + self.ingredient.calories * self.ids.pieces_amount_label.number + self.ingredient.calories * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))
            self.ids.meal_fats.text = f"{str(round(self.meal.fats + self.ingredient.fats * self.ids.pieces_amount_label.number + self.ingredient.fats * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))} g"
            self.ids.meal_carbohydrates.text = f"{str(round(self.meal.carbohydrates + self.ingredient.carbohydrates * self.ids.pieces_amount_label.number + self.ingredient.carbohydrates * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))} g"
            self.ids.meal_proteins.text = f"{str(round(self.meal.proteins + self.ingredient.proteins * self.ids.pieces_amount_label.number + self.ingredient.proteins * self.ids.slices_amount_label.numerator / self.ingredient.divisible_by,2))} g"
        s.close()
    
    def add_to_meal(self):
        s = Session()
        if self.caller_already_exists or self.caller_change:
            asc_obj = s.query(Association).get(self.asc_obj_id)
            asc_obj.amount_numerator = self.ids.pieces_amount_label.number * self.ingredient.divisible_by + self.ids.slices_amount_label.numerator
            asc_obj.amount_denominator = self.ingredient.divisible_by
        else:
            s.add(Association(
                meal = s.query(Meal).get(self.meal_id),
                ingredient = s.query(Ingredient).get(self.ingredient_id),
                amount_numerator = self.ids.pieces_amount_label.number * self.ingredient.divisible_by + self.ids.slices_amount_label.numerator,
                amount_denominator = self.ingredient.divisible_by
                )
            )
        s.commit()
        s.close()
        self.display_meal_screen.refresh_internal_ingredient_list()
        self.display_meal_screen.refresh_display_ingredient_list()
        self.cancel()

class Add_Ing_To_Meal_Unit_Piece_Indivisible_Dialog(MDBoxLayout):

    def __init__(self, asc_obj_id, ingredient_id, meal_id, caller_already_exists:bool, caller_change:bool, *args, **kwargs):
        super(Add_Ing_To_Meal_Unit_Piece_Indivisible_Dialog, self).__init__(*args, **kwargs)
        self.asc_obj_id = asc_obj_id
        self.caller_already_exists = caller_already_exists
        self.caller_change = caller_change
        self.ingredient_id = ingredient_id
        self.meal_id = meal_id
        s = Session()
        self.amount = s.query(Association).get(self.asc_obj_id).amount_numerator if self.caller_already_exists or self.caller_change else None
        s.close()

    def cancel(self):
        if self.caller_already_exists:
            self.popup_add_ing_piece_indivisible.dismiss()
            self.popup_ingredient_is_already_in_meal.dismiss()
        elif self.caller_change:
            self.popup_add_ing_piece_indivisible.dismiss()
            self.popup_base_ing_opt.dismiss()
        else:
            self.popup_add_ing_piece_indivisible.dismiss()

    def confirm_button_check_validity(self):
        if self.ids.pieces_amount_label.number > 0:
            self.ids.confirm_button.disabled = False
        else:
            self.ids.confirm_button.disabled = True

    def increment_pieces(self):
        self.ids.pieces_amount_label.number += 1
        self.confirm_button_check_validity()

    def decrement_pieces(self):
        if self.ids.pieces_amount_label.number > 0:
            self.ids.pieces_amount_label.number -= 1
            self.confirm_button_check_validity()

    def refresh_stats(self):
        s = Session()
        self.ingredient = s.query(Ingredient).get(self.ingredient_id)
        self.meal = s.query(Meal).get(self.meal_id)
        self.ids.ing_calories.text = str(round(self.ingredient.calories * self.ids.pieces_amount_label.number,2))
        self.ids.ing_fats.text = f"{str(round(self.ingredient.fats * self.ids.pieces_amount_label.number,2))} g"
        self.ids.ing_carbohydrates.text = f"{str(round(self.ingredient.carbohydrates * self.ids.pieces_amount_label.number,2))} g"
        self.ids.ing_proteins.text = f"{str(round(self.ingredient.proteins * self.ids.pieces_amount_label.number,2))} g"
        if self.caller_already_exists or self.caller_change:
            self.ids.meal_calories.text = str(round((self.meal.calories - self.ingredient.calories * self.amount) + self.ingredient.calories * self.ids.pieces_amount_label.number,2))
            self.ids.meal_fats.text = f"{str(round((self.meal.fats - self.ingredient.fats * self.amount) + self.ingredient.fats * self.ids.pieces_amount_label.number,2))} g"
            self.ids.meal_carbohydrates.text = f"{str(round((self.meal.carbohydrates - self.ingredient.carbohydrates * self.amount) + self.ingredient.carbohydrates * self.ids.pieces_amount_label.number,2))} g"
            self.ids.meal_proteins.text = f"{str(round((self.meal.proteins - self.ingredient.proteins * self.amount) + self.ingredient.proteins * self.ids.pieces_amount_label.number,2))} g"
        else:
            self.ids.meal_calories.text = str(round(self.meal.calories + self.ingredient.calories * self.ids.pieces_amount_label.number,2))
            self.ids.meal_fats.text = f"{str(round(self.meal.fats + self.ingredient.fats * self.ids.pieces_amount_label.number,2))} g"
            self.ids.meal_carbohydrates.text = f"{str(round(self.meal.carbohydrates + self.ingredient.carbohydrates * self.ids.pieces_amount_label.number,2))} g"
            self.ids.meal_proteins.text = f"{str(round(self.meal.proteins + self.ingredient.proteins * self.ids.pieces_amount_label.number,2))} g"
        s.close()
    
    def add_to_meal(self):
        s = Session()
        if self.caller_already_exists or self.caller_change: # could integrate check if amount has changed or not if no change is made just dismiss
            s.query(Association).get(self.asc_obj_id).amount_numerator = self.ids.pieces_amount_label.number
        else:
            s.add(Association(
                meal = s.query(Meal).get(self.meal_id),
                ingredient = s.query(Ingredient).get(self.ingredient_id),
                amount_numerator = self.ids.pieces_amount_label.number,
                amount_denominator = 1   
                )
            )
        s.commit()
        s.close()
        self.display_meal_screen.refresh_internal_ingredient_list()
        self.display_meal_screen.refresh_display_ingredient_list()
        self.cancel()

class Add_Ing_To_Meal_Unit_Gram_Ml_Dialog(MDBoxLayout):
    
    def __init__(self, asc_obj_id:int, ingredient_id:int, meal_id:int, caller_already_exists:bool, caller_change:bool, *args, **kwargs):
        super(Add_Ing_To_Meal_Unit_Gram_Ml_Dialog, self).__init__(*args, **kwargs)
        self.asc_obj_id = asc_obj_id
        self.caller_already_exists = caller_already_exists
        self.caller_change = caller_change
        self.ingredient_id = ingredient_id
        self.meal_id = meal_id
        s = Session()
        self.amount = s.query(Association).get(self.asc_obj_id).amount_numerator if self.caller_already_exists or self.caller_change else None
        s.close()
    
    def increment_amount(self):
        self.ids.amount_input.text = str(int(self.ids.amount_input.text) + 1)

    def decrement_amount_button_check_validity(self):
        if self.ids.amount_input.text != "":
            if int(self.ids.amount_input.text) > 1:
                self.ids.decrement_amount_button.disabled = False
                return True
            else:
                return False
        else:
            self.ids.decrement_amount_button.disabled = True
            return False

    def decrement_amount(self):
        if self.decrement_amount_button_check_validity():
            self.ids.amount_input.text = str(int(self.ids.amount_input.text) - 1)

    def cancel(self):
        if self.caller_already_exists:
            self.popup_add_ing_gram_ml.dismiss()
            self.popup_ingredient_is_already_in_meal.dismiss()
        elif self.caller_change:
            self.popup_add_ing_gram_ml.dismiss()
            self.popup_base_ing_opt.dismiss()
        else:
            self.popup_add_ing_gram_ml.dismiss()

    def confirm_button_check_validity(self):
        if self.ids.amount_input.text == "" or self.ids.amount_input.text == "0":
            self.ids.confirm_button.disabled = True
        else:
            self.ids.confirm_button.disabled = False

    def refresh_stats(self):
        s = Session()
        self.ingredient = s.query(Ingredient).get(self.ingredient_id) # another exception where I use the ingredient object itself # Optimization == get all the necessary stats on initialization
        self.meal = s.query(Meal).get(self.meal_id)
        self.ids.ing_calories.text = str(round(self.ingredient.calories * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))
        self.ids.ing_fats.text = f"{str(round(self.ingredient.fats * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))} g"
        self.ids.ing_carbohydrates.text = f"{str(round(self.ingredient.carbohydrates * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))} g"
        self.ids.ing_proteins.text = f"{str(round(self.ingredient.proteins * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))} g"
        if self.caller_already_exists or self.caller_change:
            self.ids.meal_calories.text = str(round((self.meal.calories - self.ingredient.calories * self.amount / 100) + self.ingredient.calories * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))
            self.ids.meal_fats.text = f"{str(round((self.meal.fats - self.ingredient.fats * self.amount / 100) + self.ingredient.fats * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))} g"
            self.ids.meal_carbohydrates.text = f"{str(round((self.meal.carbohydrates - self.ingredient.carbohydrates * self.amount / 100) + self.ingredient.carbohydrates * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))} g"
            self.ids.meal_proteins.text = f"{str(round((self.meal.proteins - self.ingredient.proteins * self.amount / 100) + self.ingredient.proteins * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))} g"
        else:
            self.ids.meal_calories.text = str(round(self.meal.calories + self.ingredient.calories * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))
            self.ids.meal_fats.text = f"{str(round(self.meal.fats + self.ingredient.fats * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))} g"
            self.ids.meal_carbohydrates.text = f"{str(round(self.meal.carbohydrates + self.ingredient.carbohydrates * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))} g"
            self.ids.meal_proteins.text = f"{str(round(self.meal.proteins + self.ingredient.proteins * int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) / 100,2))} g"
        s.close()

    def add_to_meal_button_check_validity(self):
        if int(self.ids.amount_input.text if self.ids.amount_input.text.isdigit() else 0) > 0:
            self.ids.add_to_meal_button.disabled = False
        else:
            self.ids.add_to_meal_button.disabled = True

    def add_to_meal(self):
        s = Session()
        if self.caller_already_exists or self.caller_change:
            s.query(Association).get(self.asc_obj_id).amount_numerator = int(self.ids.amount_input.text)
        else:
            s.add(
                Association(
                    meal=s.query(Meal).get(self.meal_id),
                    ingredient=s.query(Ingredient).get(self.ingredient_id),
                    amount_numerator=int(self.ids.amount_input.text),
                    amount_denominator=100
                )
            )
        s.commit()
        s.close()
        self.display_meal_screen.refresh_internal_ingredient_list()
        self.display_meal_screen.refresh_display_ingredient_list()
        self.cancel()

class Meal_Ingredient_Options_Dialog(MDBoxLayout):

    def __init__(self, asc_obj_id, ing_name, *args, **kwargs):
        super(Meal_Ingredient_Options_Dialog, self).__init__(*args, **kwargs)
        self.asc_obj_id = asc_obj_id
        s = Session()
        asc_obj = s.query(Association).get(self.asc_obj_id)
        self.meal_name = asc_obj.meal.name
        self.meal_id = asc_obj.meal.id
        self.ingredient_name = asc_obj.ingredient.name
        self.ingredient_unit = asc_obj.ingredient.unit
        self.ingredient_id = asc_obj.ingredient.id
        self.ingredient_divisible_by = asc_obj.ingredient.divisible_by
        self.amount_numerator = asc_obj.amount_numerator
        self.amount_denominator = asc_obj.amount_denominator
        s.close()

    def cancel(self):
        self.popup_base_ing_opt.dismiss()

    def open_change_amount_dialog(self):
        if self.ingredient_unit == "gram" or self.ingredient_unit == "ml":
            c = Add_Ing_To_Meal_Unit_Gram_Ml_Dialog(caller_change=True,
                                                    caller_already_exists=False,
                                                    asc_obj_id=self.asc_obj_id,
                                                    ingredient_id=self.ingredient_id,
                                                    meal_id=self.meal_id)
            self.popup_add_ing_gram_ml = MDDialog(
                title=f"Change amount of {self.ingredient_name}",
                type="custom",
                size_hint=(.9, None),
                height=MDApp.get_running_app().root.height*.8,
                pos_hint={"center_x": .5, "center_y": .5},
                content_cls=c,
                radius=[20, 7, 20, 7]
            )
            c.popup_base_ing_opt = self.popup_base_ing_opt
            c.display_meal_screen = self.display_meal_screen
            c.popup_add_ing_gram_ml = self.popup_add_ing_gram_ml
            c.ids.amount_input.text = str(self.amount_numerator)
            c.decrement_amount_button_check_validity()
            c.ids.unit_label.text = self.ingredient_unit
            c.ids.ing_stats_label.text = self.ingredient_name
            c.ids.meal_stats_label.text = self.meal_name
            c.refresh_stats()
            c.confirm_button_check_validity()
            self.popup_add_ing_gram_ml.open()
        else:
            if self.ingredient_divisible_by > 1:
                c = Add_Ing_To_Meal_Unit_Piece_Divisible_Dialog(caller_change=True,
                                                                caller_already_exists=False,
                                                                asc_obj_id=self.asc_obj_id,
                                                                ingredient_id=self.ingredient_id,
                                                                meal_id=self.meal_id)
                self.popup_add_ing_piece_divisible = MDDialog(
                    title=f"Change amount of {self.ingredient_name}",
                    type="custom",
                    size_hint=(.9, None),
                    height=MDApp.get_running_app().root.height*.8,
                    pos_hint={"center_x": .5, "center_y": .5},
                    content_cls=c,
                    radius=[20, 7, 20, 7]
                )
                c.popup_base_ing_opt = self.popup_base_ing_opt
                c.display_meal_screen = self.display_meal_screen
                c.popup_add_ing_piece_divisible = self.popup_add_ing_piece_divisible
                c.ids.pieces_amount_label.text = str(int(self.amount_numerator / self.ingredient_divisible_by))
                c.ids.pieces_amount_label.number = int(self.amount_numerator / self.ingredient_divisible_by)
                c.ids.slices_amount_label.numerator = int(self.amount_numerator % self.ingredient_divisible_by)
                c.ids.slices_amount_label.denominator = self.ingredient_divisible_by
                c.ids.ing_stats_label.text = self.ingredient_name
                c.ids.meal_stats_label.text = self.meal_name
                c.refresh_stats()
                c.confirm_button_check_validity()
                self.popup_add_ing_piece_divisible.open()
            else:
                c = Add_Ing_To_Meal_Unit_Piece_Indivisible_Dialog(caller_change=True,
                                                                  caller_already_exists=False,
                                                                  asc_obj_id=self.asc_obj_id,
                                                                  ingredient_id=self.ingredient_id,
                                                                  meal_id=self.meal_id)
                self.popup_add_ing_piece_indivisible = MDDialog(
                    title=f"Change amount of {self.ingredient_name}",
                    type="custom",
                    size_hint=(.9, None),
                    height=MDApp.get_running_app().root.height*.8,
                    pos_hint={"center_x": .5, "center_y": .5},
                    content_cls=c,
                    radius=[20, 7, 20, 7]
                )
                c.popup_base_ing_opt = self.popup_base_ing_opt
                c.display_meal_screen = self.display_meal_screen
                c.popup_add_ing_piece_indivisible = self.popup_add_ing_piece_indivisible
                c.ids.pieces_amount_label.text = str(self.amount_numerator)
                c.ids.pieces_amount_label.number = self.amount_numerator
                c.ids.ing_stats_label.text = self.ingredient_name
                c.ids.meal_stats_label.text = self.meal_name
                c.refresh_stats()
                c.confirm_button_check_validity()
                self.popup_add_ing_piece_indivisible.open()

    def open_delete_ingredient_dialog(self):
        c = Delete_Meal_Ingredient_Dialog(asc_obj_id=self.asc_obj_id)
        self.popup_delete_layer2 = MDDialog(
            title=f"Delete {self.ingredient_name} ?",
            type="custom",
            size_hint=(.9, None),
            pos_hint={"center_x": .5, "center_y": .5},
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.display_meal_screen = self.display_meal_screen
        c.popup_base_ing_opt = self.popup_base_ing_opt
        c.popup_delete_layer2 = self.popup_delete_layer2
        self.popup_delete_layer2.open()

class Delete_Meal_Ingredient_Dialog(MDBoxLayout):

    def __init__(self, asc_obj_id, *args, **kwargs):
        super(Delete_Meal_Ingredient_Dialog, self).__init__(*args, **kwargs)
        self.asc_obj_id = asc_obj_id
        self.screen_manager = MDApp.get_running_app().root.ids.screen_manager

    def cancel(self):
        self.popup_delete_layer2.dismiss()
    
    def delete(self):
        s = Session()
        s.delete(s.query(Association).get(self.asc_obj_id))
        s.commit()
        s.close()
        self.popup_base_ing_opt.dismiss()
        self.popup_delete_layer2.dismiss()
        self.display_meal_screen.refresh_internal_ingredient_list()
        self.display_meal_screen.refresh_display_ingredient_list()

class Meal_Plan_Item(MDBoxLayout):
    color = ListProperty([0,0,0,1])

    def __init__(self, meal_id, meal_type, pos_in_list, ingredient_id__unit__amount_list, *args, **kwargs):
        super(Meal_Plan_Item, self).__init__(*args, **kwargs)
        self.meal_id = meal_id
        self.meal_type = meal_type
        self.pos_in_list = pos_in_list
        self.meal_plan_screen = MDApp.get_running_app().root.ids.meal_plan_screen
        self.meal_icon_color_dict = {
            "thermometer":(1,0,0,1),
            "snowflake":(0,.7,1,1),
            "candy-outline":(1,.4,.8,1),
            "french-fries":(1,.8,0,1),
            "egg-fried":(1,.5,0,1),
            "bowl-mix-outline":(1,.9,0,1),
            "pot-steam-outline":(.7,0,0.1),
            "fridge-outline":(0.4,.2,1),
            "cookie-outline":(.7,0,.15,1),
            "sausage":(.7,.2,.04,1)
        }
        self.color = [.5,.5,.5,1] if self.meal_type == "Breakfast" else [.2,.2,.2,1] if self.meal_type == "Lunch" else [.1,.1,.1,1] if self.meal_type == "Dinner" else [.05,.05,.05,1]
        self.ingredient_id__unit__amount_list = ingredient_id__unit__amount_list
        self.get_stats()
        self.set_stats()
    
    def get_stats(self):
        s = Session()
        self.meal = s.query(Meal).get(self.meal_id)
        self.meal_name = self.meal.name
        self.sweet_savory = self.meal.sweet_savory
        self.hot_cold = self.meal.hot_cold
        s.close()
    
    def set_stats(self):
        self.meal_calories = sum([i[2] * i[6] / i[7] for i in self.ingredient_id__unit__amount_list])
        self.meal_fats = sum([i[3] * i[6] / i[7] for i in self.ingredient_id__unit__amount_list])
        self.meal_carbohydrates = sum([i[4] * i[6] / i[7] for i in self.ingredient_id__unit__amount_list])
        self.meal_proteins = sum([i[5] * i[6] / i[7] for i in self.ingredient_id__unit__amount_list])  
        self.ids.meal_name.text = self.meal_name
        self.ids.meal_calories.text = f"Calories:{'  '}{round(self.meal_calories,2)} kcals"
        self.ids.meal_fats.text = f"Fats:{'          '}{round(self.meal_fats,2)} g"
        self.ids.meal_carbohydrates.text = f"Carbs:{'       '}{round(self.meal_carbohydrates,2)} g"
        self.ids.meal_proteins.text = f"Proteins:{'  '}{round(self.meal_proteins,2)} g"
        self.ids.icon_meal_type.icon = ("egg-fried" if not self.hot_cold else "bowl-mix-outline") if self.meal_type == "Breakfast" else ("pot-steam-outline" if not self.hot_cold else "fridge-outline") if self.meal_type == "Lunch" or self.meal_type == "Dinner" else ("cookie-outline" if not self.sweet_savory else "sausage")
        self.ids.icon_meal_type.text_color = (self.meal_icon_color_dict["egg-fried"] if not self.hot_cold else self.meal_icon_color_dict["bowl-mix-outline"]) if self.meal_type == "Breakfast" else (self.meal_icon_color_dict["pot-steam-outline"] if not self.hot_cold else self.meal_icon_color_dict["fridge-outline"]) if self.meal_type == "Lunch" or self.meal_type == "Dinner" else (self.meal_icon_color_dict["cookie-outline"] if not self.sweet_savory else self.meal_icon_color_dict["sausage"])
        self.ids.icon_meal_sweet_savory.icon = ("candy-outline" if not self.sweet_savory else "french-fries") if self.meal_type == "Breakfast" else "candy-outline" if not self.sweet_savory else "french-fries" if self.meal_type == "Lunch" or self.meal_type == "Dinner" else "candy-outline" if not self.sweet_savory else "french-fries"
        self.ids.icon_meal_sweet_savory.text_color = (self.meal_icon_color_dict["candy-outline"] if not self.sweet_savory else self.meal_icon_color_dict["french-fries"]) if self.meal_type == "Breakfast" else (self.meal_icon_color_dict["candy-outline"] if not self.sweet_savory else self.meal_icon_color_dict["french-fries"]) if self.meal_type == "Lunch" or self.meal_type == "Dinner" else (self.meal_icon_color_dict["candy-outline"] if not self.sweet_savory else self.meal_icon_color_dict["french-fries"])
        self.ids.icon_meal_hot_cold.icon = ("thermometer" if not self.hot_cold else "snowflake") if self.meal_type == "Breakfast" else ("thermometer" if not self.hot_cold else "snowflake") if self.meal_type == "Lunch" or self.meal_type == "Dinner" else ("thermometer" if not self.hot_cold else "snowflake")
        self.ids.icon_meal_hot_cold.text_color =( self.meal_icon_color_dict["thermometer"] if not self.hot_cold else self.meal_icon_color_dict["snowflake"]) if self.meal_type == "Breakfast" else (self.meal_icon_color_dict["thermometer"] if not self.hot_cold else self.meal_icon_color_dict["snowflake"]) if self.meal_type == "Lunch" or self.meal_type == "Dinner" else (self.meal_icon_color_dict["thermometer"] if not self.hot_cold else self.meal_icon_color_dict["snowflake"])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            for child in self.children:
                if child.collide_point(*touch.pos):
                    if child.name == "Box_Stats":
                        self.display_meal()
        return super().on_touch_down(touch)

    def display_meal(self):
        pass # should display the display meal screen

    def show_type(self):
        pass # should show Info Popup
    
    def show_sweet_savory(self):
        pass # should show Info Popup
    
    def show_hot_cold(self):
        pass # should show Info Popup

    def open_swap_options_dialog(self):
        c = Swap_Options_Dialog(meal_id=self.meal_id,
                                meal_type=self.meal_type)
        self.popup_base = MDDialog(
            title=f"Swap {self.meal_name}",
            type="custom",
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.logic = self
        c.popup_base = self.popup_base
        self.popup_base.open()

class Swap_Options_Dialog(MDBoxLayout):

    def __init__(self, meal_id, meal_type, *args, **kwargs):
        super(Swap_Options_Dialog, self).__init__(*args, **kwargs)
        self.current_meal_id = meal_id
        self.filter_conditions_input = [
            True if meal_type == "Breakfast" else False,
            True if meal_type == "Lunch" else False,
            True if meal_type == "Snack" else False,
            True if meal_type == "Dinner" else False
        ]
        self.filter_conditions = [
            Meal.breakfast == True,
            Meal.lunch == True,
            Meal.snack == True,
            Meal.dinner == True
        ]

    def cancel(self):
        self.popup_base.dismiss()

    def select_new_meal_random(self):
        s = Session()
        new_meal_id_list = [i.id for i in s.query(Meal).filter(Meal.id != self.current_meal_id,*[self.filter_conditions[index] for index, i in enumerate(self.filter_conditions_input) if i]).all()]
        if new_meal_id_list:
            new_random_meal_id = rd.choice(new_meal_id_list)
            self.logic.meal_id = new_random_meal_id
            self.logic.meal_plan_screen.meal_id_and_ingredient_id__unit__amount_list[self.logic.pos_in_list[0]][self.logic.pos_in_list[1]][0] = new_random_meal_id
            self.logic.meal_plan_screen.meal_id_and_ingredient_id__unit__amount_list[self.logic.pos_in_list[0]][self.logic.pos_in_list[1]][1] = [[i.ingredient_id,i.ingredient.unit,i.ingredient.calories,i.ingredient.fats,i.ingredient.carbohydrates,i.ingredient.proteins,i.amount_numerator,i.amount_denominator,i.ingredient.name,i.ingredient.type] for i in s.query(Association).filter(Association.meal_id == new_random_meal_id).all()]
            self.logic.meal_plan_screen.adjusted = False
            self.logic.meal_plan_screen.adjust_calories_button_check_validity()
            self.logic.get_stats()
            self.logic.set_stats()
            self.popup_base.dismiss()
        else:
            pass # ("no more meals are saved")
    def select_new_meal_manuel(self):
        pass  # misses the manual swap option

class Meal_Plan_Screen(MDScreen):

    def __init__(self, *args, **kwargs):
        super(Meal_Plan_Screen,self).__init__(*args, **kwargs)
        s = Session()
        print(kivy.__version__)
        print(kivymd.__version__)
        active = s.query(Active).first()
        if active:
            if active.meal_plan_id:
                active_meal_plan = s.query(Meal_Plan).get(active.meal_plan_id)
                self.breakfast = active_meal_plan.breakfast
                self.breakfast_percentage = active_meal_plan.breakfast_percentage
                self.lunch = active_meal_plan.lunch
                self.lunch_percentage = active_meal_plan.lunch_percentage
                self.snack = active_meal_plan.snack
                self.snack_percentage = active_meal_plan.snack_percentage
                self.dinner = active_meal_plan.dinner
                self.dinner_percentage = active_meal_plan.dinner_percentage
                self.day_range = active_meal_plan.day_range
                self.meal_id_and_ingredient_id__unit__amount_list = eval(active_meal_plan.meal_id_and_ingredient_id__unit__amount_list)
                self.adjusted = active_meal_plan.adjusted
                self.shopping_list = eval(active_meal_plan.shopping_list)
                self.active_meal_plan_id = active_meal_plan.id
                self.active_meal_plan_name = active_meal_plan.name
            else:
                self.breakfast = False
                self.breakfast_percentage = 0
                self.lunch = False
                self.lunch_percentage = 0
                self.snack = False
                self.snack_percentage = 0
                self.dinner = False
                self.dinner_percentage = 0
                self.day_range = 1
                self.meal_id_and_ingredient_id__unit__amount_list = None
                self.shopping_list = []
                self.adjusted = False
                self.active_meal_plan_id = None
        else:
            self.breakfast = False
            self.breakfast_percentage = 0
            self.lunch = False
            self.lunch_percentage = 0
            self.snack = False
            self.snack_percentage = 0
            self.dinner = False
            self.dinner_percentage = 0
            self.day_range = 1
            self.meal_id_and_ingredient_id__unit__amount_list = None
            self.shopping_list = []
            self.adjusted = False
            self.active_meal_plan_id = None
        s.close()
        self.erase_meal_plan_button_info_opened = False
        self.save_meal_plan_button_info_opened = False
        self.display_saved_meal_plans_button_info_opened = False
        self.adjust_calories_button_info_opened = False        
        self.event = False

    def open_meal_plan_settings(self):
        c = Meal_Plan_Settings_Dialog()
        self.popup_meal_plan_settings = MDDialog(
            title="Meal Plan Settings",
            type="custom",
            size_hint=(.9, None),
            pos_hint={"center_x": .5, "center_y": .5},
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.popup_meal_plan_settings = self.popup_meal_plan_settings
        if self.active_meal_plan_id:
            s = Session()
            active_meal_plan_settings = s.query(Meal_Plan).get(s.query(Active).first().meal_plan_id)
            c.ids.breakfast.active = active_meal_plan_settings.breakfast
            c.ids.lunch.active = active_meal_plan_settings.lunch
            c.ids.dinner.active = active_meal_plan_settings.dinner
            c.ids.snack.active = active_meal_plan_settings.snack
            c.set_percentage_availability_all()
            c.ids.breakfast_percent_label.percentage = active_meal_plan_settings.breakfast_percentage
            c.ids.lunch_percent_label.percentage = active_meal_plan_settings.lunch_percentage
            c.ids.dinner_percent_label.percentage = active_meal_plan_settings.dinner_percentage
            c.ids.snack_percent_label.percentage = active_meal_plan_settings.snack_percentage
            c.ids.day_range.number = active_meal_plan_settings.day_range
            c.ids.day_range_decrement_button.disabled = True if active_meal_plan_settings.day_range <= 1 else False
            s.close()   
        else:
            c.ids.breakfast.active = self.breakfast
            c.ids.lunch.active = self.lunch
            c.ids.dinner.active = self.dinner
            c.ids.snack.active = self.snack
            c.set_percentage_availability_all()
            c.ids.breakfast_percent_label.percentage = self.breakfast_percentage
            c.ids.lunch_percent_label.percentage = self.lunch_percentage
            c.ids.dinner_percent_label.percentage = self.dinner_percentage
            c.ids.snack_percent_label.percentage = self.snack_percentage
            c.ids.day_range.number = self.day_range
            c.ids.day_range_decrement_button.disabled = True if self.day_range <= 1 else False
        c.Meal_Plan_Screen = self
        self.popup_meal_plan_settings.open()

    def set_page_icon_validity_status(self):
        if self.day_range - 1 == self.ids.meal_plan.page:
            self.ids.increment_page_button.text_color = (0,0,0,.25)
        else:
            self.ids.increment_page_button.text_color = (0,0,0,1)
        if self.ids.meal_plan.page == 0:
            self.ids.decrement_page_button.text_color = (0,0,0,.25)
        else:
            self.ids.decrement_page_button.text_color = (0,0,0,1)

    def increment_page(self):
        if self.day_range - 1 > self.ids.meal_plan.page:
            self.ids.meal_plan.page += 1
        self.set_page_icon_validity_status()

    def decrement_page(self):
        if self.meal_plan.page > 0:
            self.ids.meal_plan.page -= 1
        self.set_page_icon_validity_status()

    def generate_button_check_validity(self):
        if any ([self.breakfast,self.lunch,self.snack,self.dinner]) and self.day_range > 0 and not self.ids.meal_plan.children:
            return True
        else:
            return False

    def test_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            instance.event = Clock.schedule_once(lambda dt: self.test_show_eraser_button(instance), 1)

    def set_opened_infos_to_false(self,identifier):
        if identifier == "eraser":
            self.erase_meal_plan_button_info_opened = False
        elif identifier == "content-save-outline":
            self.save_meal_plan_button_info_opened = False
        elif identifier == "folder-open-outline":
            self.display_saved_meal_plans_button_info_opened = False
        elif identifier == "adjust":
            self.adjust_calories_button_info_opened = False

    def test_touch_up(self, instance, touch):
        try:
            if instance.collide_point(*touch.pos):
                instance.event.cancel()
                if instance.icon == "eraser":
                    if self.erase_meal_plan_button_info_opened:
                        Clock.schedule_once(lambda dt: self.set_opened_infos_to_false("eraser"), 0)
                        self.erase_meal_plan_button_info.dismiss()
                elif instance.icon == "content-save-outline":
                    if self.save_meal_plan_button_info_opened:
                        Clock.schedule_once(lambda dt: self.set_opened_infos_to_false("content-save-outline"), 0)
                        self.save_meal_plan_button_info.dismiss()
                elif instance.icon == "folder-open-outline":
                    if self.display_saved_meal_plans_button_info_opened:
                        Clock.schedule_once(lambda dt: self.set_opened_infos_to_false("folder-open-outline"), 0)
                        self.display_saved_meal_plans_button_info.dismiss()
                elif instance.icon == "adjust":
                    if self.adjust_calories_button_info_opened:
                        Clock.schedule_once(lambda dt: self.set_opened_infos_to_false("adjust"), 0)
                        self.adjust_calories_button_info.dismiss()
        except AttributeError:
            pass

    def test_show_eraser_button(self, instance):
        icon = instance.icon
        instance.event.cancel()
        self.erase_meal_plan_button_info = MDDropdownMenu(
            caller=self.ids.erase_meal_plan_button,
            items=[
                {
                    "viewclass": "MDLabel",
                    "text": "Erases the current meal plan"
                }
            ],
            width_mult=4,
            position="auto"
        )
        self.save_meal_plan_button_info = MDDropdownMenu(
            caller=self.ids.save_meal_plan_button,
            items=[
                {
                    "viewclass": "MDLabel",
                    "text": "Saves the current meal plan or saves the changes"
                }
            ],
            width_mult=4,
            position="auto"
        )
        self.display_saved_meal_plans_button_info = MDDropdownMenu(
            caller=self.ids.display_saved_meal_plans_button,
            items=[
                {
                    "viewclass": "MDLabel",
                    "text": "Displays saved meal plans to load or delete them"
                }
            ],
            width_mult=4,
            position="auto"

        )
        self.adjust_calories_button_info = MDDropdownMenu(
            caller=self.ids.adjust_calories_button,
            items=[
                {
                    "viewclass": "MDLabel",
                    "text": "Adjusts the amount of calories in the meal plan according to your daily calorie goal"
                }
            ],
            width_mult=4,
            position="auto"
        )
        if icon == "eraser":
            self.erase_meal_plan_button_info.open()
            self.erase_meal_plan_button_info_opened = True
        elif icon == "content-save-outline":
            self.save_meal_plan_button_info.open()
            self.save_meal_plan_button_info_opened = True
        elif icon == "folder-open-outline":
            self.display_saved_meal_plans_button_info.open()
            self.display_saved_meal_plans_button_info_opened = True
        elif icon == "adjust":
            self.adjust_calories_button_info.open()
            self.adjust_calories_button_info_opened = True

    def erase_meal_plan_and_save_meal_plan_button_check_validity(self):
        if self.ids.meal_plan.children:
            self.ids.erase_meal_plan_button.text_color = (0,0,0,1)
            self.ids.save_meal_plan_button.text_color = (0,0,0,1)
            return True
        else:
            self.ids.erase_meal_plan_button.text_color = (0,0,0,.25)
            self.ids.save_meal_plan_button.text_color = (0,0,0,.25)
            return False
    
    def erase_meal_plan(self): # clears the current meal plan list and settings, doesnt delete it if it is already saved
        if self.erase_meal_plan_and_save_meal_plan_button_check_validity():
            if not self.erase_meal_plan_button_info_opened:
                self.ids.meal_plan.clear_widgets()
                self.meal_id_and_ingredient_id__unit__amount_list = None
                self.shopping_list = []
                MDApp.get_running_app().root.ids.shopping_list_screen.shopping_list = []
                MDApp.get_running_app().root.ids.shopping_list_screen.clear_shopping_list_list()
                self.adjusted = False
                self.active_meal_plan_id = None
                self.ids.current_meal_plan_display_name.text = "No current meal plan!"
                s = Session()
                s.query(Active).update({Active.meal_plan_id: None})
                s.commit()
                s.close()
                self.adjust_calories_button_check_validity()
                MDApp.get_running_app().root.ids.shopping_list_screen.clear_shopping_list_list()
                self.erase_meal_plan_and_save_meal_plan_button_check_validity()
                self.set_page_icon_validity_status()

    def open_save_meal_plan_options(self):
        if self.erase_meal_plan_and_save_meal_plan_button_check_validity():
            if not self.save_meal_plan_button_info_opened:
                if not self.active_meal_plan_id:
                    c = Save_Meal_Plan_Dialog() # gives option to save meal plan when no active meal plan
                    self.popup_base = MDDialog(
                        title="Save Meal Plan",
                        type="custom",
                        size_hint=(.9, None),
                        height=MDApp.get_running_app().root.height*.8,
                        pos_hint={"center_x": .5, "center_y": .65},
                        content_cls=c,
                        radius=[20, 7, 20, 7]
                    )
                    c.logic = self
                    c.popup_base = self.popup_base
                    self.popup_base.open()
                else:
                    c = Save_Meal_Plan_Changes_Dialog() # gives option to save changes
                    self.popup_base = MDDialog(
                        title="Save Changes?",
                        type="custom",
                        size_hint=(.9, None),
                        pos_hint={"center_x": .5, "center_y": .5},
                        content_cls=c,
                        radius=[20, 7, 20, 7]
                    )
                    c.logic = self
                    c.popup_base = self.popup_base
                    self.popup_base.open()
    
    def load_meal_plan_settings(self,meal_plan_id):
        s = Session()
        meal_plan = s.query(Meal_Plan).get(meal_plan_id)
        self.breakfast = meal_plan.breakfast
        self.lunch = meal_plan.lunch
        self.snack = meal_plan.snack
        self.dinner = meal_plan.dinner
        self.day_range = meal_plan.day_range
        self.meal_id_and_ingredient_id__unit__amount_list = eval(meal_plan.meal_id_and_ingredient_id__unit__amount_list)
        self.shopping_list = eval(meal_plan.shopping_list)
        self.adjusted = meal_plan.adjusted
        self.active_meal_plan_name = meal_plan.name
        self.active_meal_plan_id = meal_plan.id
        MDApp.get_running_app().root.ids.shopping_list_screen.shopping_list = self.shopping_list
        self.display_meal_plan()
        self.adjust_calories_button_check_validity()
    
    def display_meal_plan(self): # displays the current meal plan when one is active
        if self.active_meal_plan_id:
            self.ids.meal_plan.clear_widgets()
            self.ids.current_meal_plan_display_name.text = f"{self.active_meal_plan_name} : Day {self.ids.meal_plan.page + 1}"
            self.meal_type_list = [i for i in ["Breakfast" if self.breakfast else None, "Lunch" if self.lunch else None, "Snack" if self.snack else None, "Dinner" if self.dinner else None] if i]
            for index, i in enumerate(self.meal_id_and_ingredient_id__unit__amount_list):
                self.ids.meal_plan.add_widget(MDScrollView(pos_hint={"center_x":.5}))
                self.ids.meal_plan.children[0].add_widget(Custom_MDGridLayout())
                self.ids.meal_plan.children[0].children[0].add_widget(Widget(size_hint_y=None,height=dp(25)))
                for index2,j in enumerate(i):
                    self.ids.meal_plan.children[0].children[0].add_widget(Meal_Plan_Item(meal_id=j[0],
                                                                                         meal_type=self.meal_type_list[index2],
                                                                                         pos_in_list=(index,index2),
                                                                                         ingredient_id__unit__amount_list=j[1]))
                    self.ids.meal_plan.children[0].children[0].add_widget(Widget(size_hint_y=None,height=dp(25)))
                self.ids.meal_plan.children[0].children[0].add_widget(Widget(size_hint_y=None,height=dp(100)))
            self.display_page_title()
            MDApp.get_running_app().root.ids.shopping_list_screen.refresh_internal_list()

    def open_load_meal_plan_dialog(self):
        if not self.display_saved_meal_plans_button_info_opened:
            c = Load_Meal_Plan_Dialog()
            self.popup_base = MDDialog(
                title="Load Meal Plan",
                type="custom",
                size_hint=(.9, None),
                height=MDApp.get_running_app().root.height*.8,
                pos_hint={"center_x": .5, "center_y": .5},
                content_cls=c,
                radius=[20, 7, 20, 7]
            )
            c.popup_base = self.popup_base
            c.poup_base_logic = self
            c.refresh_display_list()
            self.popup_base.open()

    def generate_meal_plan(self):
        if self.generate_button_check_validity():
            s = Session() # I get the id lists in the function as to not miss when a meal is added or deleted
            self.breakfast_id_list = [i.id for i in s.query(Meal).filter(Meal.breakfast == True).all()]
            self.lunch_id_list = [i.id for i in s.query(Meal).filter(Meal.lunch == True).all()]
            self.snack_id_list = [i.id for i in s.query(Meal).filter(Meal.snack == True).all()]
            self.dinner_id_list = [i.id for i in s.query(Meal).filter(Meal.dinner == True).all()]
            s.close()
            self.meal_id_and_ingredient_id__unit__amount_list = [[] for i in range(self.day_range)]
            for index, i in enumerate(range(self.day_range)):
                self.ids.meal_plan.add_widget(MDScrollView(pos_hint={"center_x":.5}))
                self.ids.meal_plan.children[0].add_widget(Custom_MDGridLayout())
                self.ids.meal_plan.children[0].children[0].add_widget(Widget(size_hint_y=None,height=dp(25)))
                if self.breakfast:
                    if self.breakfast_id_list:
                        breakfast_choice = rd.choice(self.breakfast_id_list)
                        ingredient_id__unit__amount_list = [[j.ingredient_id,j.ingredient.unit,j.ingredient.calories,j.ingredient.fats,j.ingredient.carbohydrates,j.ingredient.proteins,j.amount_numerator,j.amount_denominator,j.ingredient.name,j.ingredient.type] for j in s.query(Association).filter(Association.meal_id == breakfast_choice).all()]
                        self.ids.meal_plan.children[0].children[0].add_widget(Meal_Plan_Item(meal_id=breakfast_choice,
                                                                                             meal_type="Breakfast",
                                                                                             pos_in_list=(index,0),
                                                                                             ingredient_id__unit__amount_list=ingredient_id__unit__amount_list))
                        self.meal_id_and_ingredient_id__unit__amount_list[index].append([breakfast_choice,ingredient_id__unit__amount_list])
                        self.ids.meal_plan.children[0].children[0].add_widget(Widget(size_hint_y=None,height=dp(25)))
                    else:
                        pass # show info Popup ("no breakfasts saved")
                if self.lunch:
                    if self.lunch_id_list:
                        lunch_choice = rd.choice(self.lunch_id_list)
                        ingredient_id__unit__amount_list = [[j.ingredient_id,j.ingredient.unit,j.ingredient.calories,j.ingredient.fats,j.ingredient.carbohydrates,j.ingredient.proteins,j.amount_numerator,j.amount_denominator,j.ingredient.name,j.ingredient.type] for j in s.query(Association).filter(Association.meal_id == lunch_choice).all()]
                        self.ids.meal_plan.children[0].children[0].add_widget(Meal_Plan_Item(meal_id=lunch_choice,
                                                                                             meal_type="Lunch",
                                                                                             pos_in_list=(index,1 if self.breakfast else 0),
                                                                                             ingredient_id__unit__amount_list=ingredient_id__unit__amount_list))
                        self.meal_id_and_ingredient_id__unit__amount_list[index].append([lunch_choice,ingredient_id__unit__amount_list])
                        self.ids.meal_plan.children[0].children[0].add_widget(Widget(size_hint_y=None,height=dp(25)))
                    else:
                        pass # show info Popup ("no lunchs saved")
                if self.snack:
                    if self.snack_id_list:
                        snack_choice = rd.choice(self.snack_id_list)
                        ingredient_id__unit__amount_list = [[j.ingredient_id,j.ingredient.unit,j.ingredient.calories,j.ingredient.fats,j.ingredient.carbohydrates,j.ingredient.proteins,j.amount_numerator,j.amount_denominator,j.ingredient.name,j.ingredient.type] for j in s.query(Association).filter(Association.meal_id == snack_choice).all()]
                        self.ids.meal_plan.children[0].children[0].add_widget(Meal_Plan_Item(meal_id=snack_choice,
                                                                                             meal_type="Snack",
                                                                                             pos_in_list=(index,sum([1 for i in (self.breakfast,self.lunch) if i])),
                                                                                             ingredient_id__unit__amount_list=ingredient_id__unit__amount_list))
                        self.meal_id_and_ingredient_id__unit__amount_list[index].append([snack_choice,ingredient_id__unit__amount_list])
                        self.ids.meal_plan.children[0].children[0].add_widget(Widget(size_hint_y=None,height=dp(25)))
                    else:
                        pass # show info Popup ("no snacks saved")
                if self.dinner:
                    if self.dinner_id_list:
                        dinner_choice = rd.choice(self.dinner_id_list)
                        ingredient_id__unit__amount_list = [[j.ingredient_id,j.ingredient.unit,j.ingredient.calories,j.ingredient.fats,j.ingredient.carbohydrates,j.ingredient.proteins,j.amount_numerator,j.amount_denominator,j.ingredient.name,j.ingredient.type] for j in s.query(Association).filter(Association.meal_id == dinner_choice).all()]
                        self.ids.meal_plan.children[0].children[0].add_widget(Meal_Plan_Item(meal_id=dinner_choice,
                                                                                             meal_type="Dinner",
                                                                                             pos_in_list=(index,sum([1 for i in (self.breakfast,self.lunch,self.snack) if i])),
                                                                                             ingredient_id__unit__amount_list=ingredient_id__unit__amount_list))
                        self.meal_id_and_ingredient_id__unit__amount_list[index].append([dinner_choice,ingredient_id__unit__amount_list])
                    else:
                        pass # show info Popup ("no dinners saved")
                    self.ids.meal_plan.children[0].children[0].add_widget(Widget(size_hint_y=None,height=dp(100)))
            self.adjusted = False
            self.adjust_calories_button_check_validity()
            self.erase_meal_plan_and_save_meal_plan_button_check_validity()
            self.set_page_icon_validity_status()
            self.display_page_title()
            self.generate_shopping_list()
            MDApp.get_running_app().root.ids.shopping_list_screen.refresh_internal_list()

    def adjust_calories_button_check_validity(self):
        if not self.adjusted and self.ids.meal_plan.children:
            self.ids.adjust_calories_button.text_color = (0,0,0,1)
            return True
        else:
            self.ids.adjust_calories_button.text_color = (0,0,0,.25)
            return False

    def adjust_calories(self):
        if self.adjust_calories_button_check_validity() and not self.adjust_calories_button_info_opened:
            if MDApp.get_running_app().root.ids.settings_screen.ids.calories_per_day.text != "":
                calorie_goal = float(MDApp.get_running_app().root.ids.settings_screen.ids.calories_per_day.text)
                below = False
                for i in range(self.day_range)[::-1]: # one loop = one day # Backwards to keep the order correct cause kivy iterates backwards over the children by default
                    meal_plan_item_list = [j for j in self.meal_plan.children[i].children[0].children[::-1] if isinstance(j, Meal_Plan_Item)] # j are the boxlayouts that hold the meal data # helper variable for later !
                    calories_per_meal = [j.meal_calories for j in meal_plan_item_list] 
                    current_calories_per_day = sum(calories_per_meal)
                    calorie_factor_per_meal_per_day = [j/current_calories_per_day for j in calories_per_meal] # how much each meal contributes to the total
                    calorie_factor_goal_per_meal = [i for i in [
                        self.breakfast_percentage/100,
                        self.lunch_percentage/100,
                        self.snack_percentage/100,
                        self.dinner_percentage/100] if i != 0] # how each meal should make up for in calories, supposed to be adjustable in the settings ######## NEEDS TO BE ADDED TO THE SETTINGS
                    calorie_goal_per_meal = [j*calorie_goal for j in calorie_factor_goal_per_meal]
                    ΔCals_for_current_meal = [j-calories_per_meal[index] for index, j in enumerate(calorie_goal_per_meal)]
                    ΔCals = calorie_goal - current_calories_per_day # number of calories that needs to be adjusted for
                    # ΔCals_for_current_meal2 = [ΔCals * j for j in calorie_factor_per_meal_per_day] # how many calories to add to each meal
                    for index, j in enumerate(ΔCals_for_current_meal): # loop responsible for adjusting each meal individually this loop handles the divisible_by and indivisible ones in the first half and the others further down
                        calories_per_ingredient = [k[2]*k[6]/k[7] for k in meal_plan_item_list[index].ingredient_id__unit__amount_list]
                        calorie_factor_per_ingredient = [k[2]*k[6]/k[7]/sum(calories_per_ingredient) for k in (meal_plan_item_list[index].ingredient_id__unit__amount_list)] # the unit might not be neccessary, the same condition can be checked with the denominator value !!!
                        numerator_amount_to_add_per_ingredient = [(m.floor(j*calorie_factor_per_ingredient[index2]/(k[2]/k[7])) if below else m.ceil(j*calorie_factor_per_ingredient[index2]/(k[2]/k[7]))) if abs(j*calorie_factor_per_ingredient[index2]) > (k[2]/k[7]) else 0 for index2,k in enumerate(meal_plan_item_list[index].ingredient_id__unit__amount_list)]
                        for index2,k in enumerate(numerator_amount_to_add_per_ingredient):
                            new_numerator_amount = meal_plan_item_list[index].ingredient_id__unit__amount_list[index2][6] + numerator_amount_to_add_per_ingredient[index2] if meal_plan_item_list[index].ingredient_id__unit__amount_list[index2][6] + numerator_amount_to_add_per_ingredient[index2] >= 1 else 1
                            j -= meal_plan_item_list[index].ingredient_id__unit__amount_list[index2][2] * (new_numerator_amount - meal_plan_item_list[index].ingredient_id__unit__amount_list[index2][6]) / meal_plan_item_list[index].ingredient_id__unit__amount_list[index2][7]
                            meal_plan_item_list[index].ingredient_id__unit__amount_list[index2][6] = new_numerator_amount
                        previousj = j-1
                        while previousj != j:
                            previousj = j
                            for index2,k in enumerate(meal_plan_item_list[index].ingredient_id__unit__amount_list):
                                minimum_calorie_amount_for_current_ingredient = k[2]/k[7]
                                if j > 0:
                                    if j >= minimum_calorie_amount_for_current_ingredient:
                                        j -= minimum_calorie_amount_for_current_ingredient
                                        meal_plan_item_list[index].ingredient_id__unit__amount_list[index2][6] += 1
                                elif j < 0:
                                    if abs(j) >= minimum_calorie_amount_for_current_ingredient and meal_plan_item_list[index].ingredient_id__unit__amount_list[index2][6] > 1:
                                        meal_plan_item_list[index].ingredient_id__unit__amount_list[index2][6] -= 1
                                        j += minimum_calorie_amount_for_current_ingredient
                        meal_plan_item_list[index].set_stats()
                self.adjusted = True
                self.adjust_calories_button_check_validity()
                self.display_page_title()
                self.generate_shopping_list()
                MDApp.get_running_app().root.ids.shopping_list_screen.refresh_internal_list()
            else:
                pass # show info Popup ("you need to set your settings first")
        else:
            pass # show info Popup ("plan has already been adjusted!")

    def display_page_title(self):
        if not self.active_meal_plan_id:
            if self.ids.meal_plan.children:
                self.ids.current_meal_plan_display_name.text = f"Day: {self.ids.meal_plan.page + 1} // Calories: {round(sum(i.meal_calories for i in self.meal_plan.children[self.day_range-self.ids.meal_plan.page - 1].children[0].children[::-1] if isinstance(i, Meal_Plan_Item)),2)}"
        else:
            s = Session()
            self.ids.current_meal_plan_display_name.text = f"{s.query(Meal_Plan).get(self.active_meal_plan_id).name}: // Day: {self.ids.meal_plan.page + 1} // Calories: {round(sum(i.meal_calories for i in self.meal_plan.children[self.day_range-self.ids.meal_plan.page - 1].children[0].children[::-1] if isinstance(i, Meal_Plan_Item)),2)}"
            s.close()

    def generate_shopping_list(self):
        self.shopping_list = []
        self.meal_id_and_ingredient_id__unit__amount_list = MDApp.get_running_app().root.ids.meal_plan_screen.meal_id_and_ingredient_id__unit__amount_list
        for i in self.meal_id_and_ingredient_id__unit__amount_list:
            for j in i:
                for k in j[1]:
                    if not [True for l in self.shopping_list if l[0] == k[8]]:
                        self.shopping_list.append([k[8],k[1],k[2],k[6],k[7],k[9],False,k[3],k[4],k[5]])
                    else:
                        self.shopping_list[next(index for index, l in enumerate(self.shopping_list) if l[0] == k[8])][3] += k[6]
        MDApp.get_running_app().root.ids.shopping_list_screen.shopping_list = self.shopping_list

class Save_Meal_Plan_Changes_Dialog(MDBoxLayout):

    def __init__(self, *args, **kwargs):
        super(Save_Meal_Plan_Changes_Dialog,self).__init__(*args, **kwargs)
    
    def cancel(self):
        self.popup_base.dismiss()
    
    def save_changes(self):
        s = Session()
        s.query(Meal_Plan).filter(Meal_Plan.id == self.logic.active_meal_plan_id).update({
            Meal_Plan.breakfast : self.logic.breakfast,
            Meal_Plan.breakfast_percentage : self.logic.breakfast_percentage,
            Meal_Plan.lunch : self.logic.lunch,
            Meal_Plan.lunch_percentage : self.logic.lunch_percentage,
            Meal_Plan.snack : self.logic.snack,
            Meal_Plan.snack_percentage : self.logic.snack_percentage,
            Meal_Plan.dinner : self.logic.dinner,
            Meal_Plan.dinner_percentage : self.logic.dinner_percentage,
            Meal_Plan.day_range : self.logic.day_range,
            Meal_Plan.meal_id_and_ingredient_id__unit__amount_list : str(self.logic.meal_id_and_ingredient_id__unit__amount_list),
            Meal_Plan.shopping_list : str(self.logic.shopping_list),
            Meal_Plan.adjusted : self.logic.adjusted
            }
        )
        s.commit()
        s.close()
        self.popup_base.dismiss()

class Load_Meal_Plan_Dialog(MDBoxLayout):

    def __init__(self, *args, **kwargs):
        super(Load_Meal_Plan_Dialog,self).__init__(*args, **kwargs)
    
    def cancel(self):
        self.popup_base.dismiss()
    
    def refresh_display_list(self):
        self.search = self.ids.search.text
        self.ids.meal_plan_list.clear_widgets()
        s = Session()
        meal_plan_query = s.query(Meal_Plan).filter(Meal_Plan.name.like(f"%{self.search}%")).all()
        for i in meal_plan_query:
            self.ids.meal_plan_list.add_widget(ThreeLineValueListItem(
                text=i.name,
                meal_plan_id=i.id,
                secondary_text=f"{'Breakfast, ' if i.breakfast and any([i.lunch, i.snack, i.dinner]) else 'Breakfast' if i.breakfast else ''}{'Lunch, ' if i.lunch and any([i.snack, i.dinner]) else 'Lunch' if i.lunch else ''}{'Snack, ' if i.snack and i.dinner else 'Snack' if i.snack else ''}{'Dinner' if i.dinner else ''}",
                tertiary_text=f"placeholder, should display the calories per day",
                on_release=self.open_select_meal_plan_options_dialog
                )
            )
        s.close()

    def open_select_meal_plan_options_dialog(self,listitem):
        c = Select_Meal_Plan_Options_Dialog(meal_plan_id=listitem.meal_plan_id)
        self.popup_select_meal_plan_options_dialog = MDDialog(
            title=f"{listitem.text} options",
            type="custom",
            size_hint=(.9, None),
            pos_hint={"center_x": .5, "center_y": .5},
            content_cls=c,
            radius=[20, 7, 20, 7]
        )
        c.popup_select_meal_plan_options_dialog = self.popup_select_meal_plan_options_dialog
        c.popup_base = self.popup_base
        c.load_meal_plan_dialog = self
        self.popup_select_meal_plan_options_dialog.open()

class Select_Meal_Plan_Options_Dialog(MDBoxLayout):

    def __init__(self, meal_plan_id, *args, **kwargs):
        super(Select_Meal_Plan_Options_Dialog,self).__init__(*args, **kwargs)
        self.meal_plan_id = meal_plan_id
        self.meal_plan_screen = MDApp.get_running_app().root.ids.meal_plan_screen

    def delete(self):
        c = Delete_Meal_Plan_Dialog(meal_plan_id=self.meal_plan_id)
        self.popup_delete_layer3 = MDDialog(
            title="Delete meal plan?",
            type="custom",
            content_cls=c,
            pos_hint={"center_x": .5, "center_y": .5},
            radius=[20, 7, 20, 7]
        )
        c.popup_base = self.popup_base
        c.popup_delete_layer3 = self.popup_delete_layer3
        c.popup_select_meal_plan_options_dialog = self.popup_select_meal_plan_options_dialog
        c.load_meal_plan_dialog = self.load_meal_plan_dialog
        self.popup_delete_layer3.open()

    def load_meal_plan(self):
        self.meal_plan_screen.load_meal_plan_settings(self.meal_plan_id)
        self.meal_plan_screen.set_page_icon_validity_status()
        self.meal_plan_screen.display_page_title()
        self.meal_plan_screen.erase_meal_plan_and_save_meal_plan_button_check_validity()
        s = Session()
        s.query(Active).update({Active.meal_plan_id:self.meal_plan_id})
        s.commit()
        s.close()
        self.popup_select_meal_plan_options_dialog.dismiss()
        self.popup_base.dismiss()

class Delete_Meal_Plan_Dialog(MDBoxLayout):

    def __init__(self, meal_plan_id, *args, **kwargs):
        super(Delete_Meal_Plan_Dialog,self).__init__(*args, **kwargs)
        self.meal_plan_id = meal_plan_id
        self.meal_plan_screen = MDApp.get_running_app().root.ids.meal_plan_screen

    def cancel(self):
        self.popup_delete_layer3.dismiss()

    def delete(self):
        s = Session()
        meal_plan_to_delete = s.query(Meal_Plan).get(self.meal_plan_id)
        s.delete(meal_plan_to_delete)
        s.commit()
        s.close()
        self.load_meal_plan_dialog.refresh_display_list()
        if self.meal_plan_id == s.query(Active).first().meal_plan_id:
            self.meal_plan_screen.erase_meal_plan()
            s.commit()
            s.close()
        self.popup_delete_layer3.dismiss()
        self.popup_select_meal_plan_options_dialog.dismiss()

class Save_Meal_Plan_Dialog(MDBoxLayout):

    def __init__(self, *args, **kwargs):
        super(Save_Meal_Plan_Dialog,self).__init__(*args, **kwargs)
        self.meal_plan_screen = MDApp.get_running_app().root.ids.meal_plan_screen
    def cancel(self):
        self.popup_base.dismiss()

    def check_save_button_validity(self):
        if self.ids.meal_plan_name.text == "":
            self.ids.safe_button.disabled = True
        else:
            self.ids.safe_button.disabled = False

    def save_meal_plan(self):
        s = Session()
        meal_plan_query = s.query(Meal_Plan).filter(Meal_Plan.name == self.ids.meal_plan_name.text).first()
        if meal_plan_query:
            if not meal_plan_query.id == s.query(Active).first().meal_plan_id:
                c = Meal_Plan_Already_Exists_Dialog(meal_plan_id=meal_plan_query.id)
                self.popup_meal_plan_already_exists_layer2 = MDDialog(
                    title=f"{meal_plan_query.name} already exists, would you like to overwrite?",
                    type="custom",
                    size_hint=(.9, None),
                    pos_hint={"center_x": .5, "center_y": .5},
                    content_cls=c,
                    radius=[20, 7, 20, 7]
                )
                c.meal_plan_name = meal_plan_query.name
                s.close()
                c.logic = self.logic
                c.popup_base = self.popup_base
                c.breakfast = self.breakfast
                c.lunch = self.lunch
                c.snack = self.snack
                c.dinner = self.dinner
                c.day_range = self.day_range
                c.meal_id_and_ingredient_id__unit__amount_list = self.meal_id_and_ingredient_id__unit__amount_list
                c.shopping_list = self.shopping_list
                c.adjusted = self.adjusted
                c.popup_meal_plan_already_exists_layer2 = self.popup_meal_plan_already_exists_layer2
                self.popup_meal_plan_already_exists_layer2.open()
            else:
                meal_plan_query.name = self.ids.meal_plan_name.text
                meal_plan_query.breakfast = self.logic.breakfast
                meal_plan_query.breakfast_percentage = self.logic.breakfast_percentage
                meal_plan_query.lunch = self.logic.lunch
                meal_plan_query.lunch_percentage = self.logic.lunch_percentage
                meal_plan_query.snack = self.logic.snack
                meal_plan_query.dinner_percentage = self.logic.dinner_percentage
                meal_plan_query.dinner = self.logic.dinner
                meal_plan_query.snack_percentage = self.logic.snack_percentage
                meal_plan_query.day_range = self.logic.day_range
                meal_plan_query.meal_id_and_ingredient_id__unit__amount_list = str(self.logic.meal_id_and_ingredient_id__unit__amount_list)
                meal_plan_query.shopping_list = str(self.logic.shopping_list)
                meal_plan_query.adjusted = self.logic.adjusted
                s.commit()
                s.close()
        else:
            new_meal_plan = Meal_Plan(
                name=self.ids.meal_plan_name.text,
                breakfast=self.logic.breakfast,
                breakfast_percentage=self.logic.breakfast_percentage,
                lunch=self.logic.lunch,
                lunch_percentage=self.logic.lunch_percentage,
                snack=self.logic.snack,
                dinner_percentage=self.logic.dinner_percentage,
                dinner=self.logic.dinner,
                snack_percentage=self.logic.snack_percentage,
                day_range=self.logic.day_range,
                meal_id_and_ingredient_id__unit__amount_list=str(self.logic.meal_id_and_ingredient_id__unit__amount_list),
                shopping_list=str(self.logic.shopping_list),
                adjusted=self.logic.adjusted
            )
            s.add(new_meal_plan)            
            s.commit()
            meal_plan_id = new_meal_plan.id
            self.meal_plan_screen.active_meal_plan_id = meal_plan_id
            self.meal_plan_screen.display_page_title()
            s.query(Active).update({Active.meal_plan_id: meal_plan_id})
            s.commit()
            s.close()
            self.popup_base.dismiss()

class Meal_Plan_Already_Exists_Dialog(MDBoxLayout):

    def __init__(self, meal_plan_id, *args, **kwargs):
        super(Meal_Plan_Already_Exists_Dialog,self).__init__(*args, **kwargs)
        self.meal_plan_id = meal_plan_id

    def cancel(self):
        self.popup_meal_plan_already_exists_layer2.dismiss()
    
    def overwrite_meal_plan(self):
        s = Session()
        meal_plan_query = s.query(Meal_Plan).get(self.meal_plan_id)
        meal_plan_query.name = self.meal_plan_name
        meal_plan_query.breakfast = self.logic.breakfast
        meal_plan_query.breakfast_percentage = self.logic.breakfast_percentage
        meal_plan_query.lunch = self.logic.lunch
        meal_plan_query.lunch_percentage = self.logic.lunch_percentage
        meal_plan_query.snack = self.logic.snack
        meal_plan_query.dinner_percentage = self.logic.dinner_percentage
        meal_plan_query.dinner = self.logic.dinner
        meal_plan_query.snack_percentage = self.logic.snack_percentage
        meal_plan_query.day_range = self.logic.day_range
        meal_plan_query.meal_id_and_ingredient_id__unit__amount_list = str(self.logic.meal_id_and_ingredient_id__unit__amount_list)
        meal_plan_query.shopping_list = str(self.logic.shopping_list)
        meal_plan_query.adjusted = self.logic.adjusted
        s.query(Active).update({Active.meal_plan_id: self.meal_plan_id})
        s.commit()
        s.close()
        self.popup_meal_plan_already_exists_layer2.dismiss()
        self.popup_base.dismiss()

class Meal_Plan_Settings_Dialog(MDBoxLayout):

    def __init__(self, *args, **kwargs):
        super(Meal_Plan_Settings_Dialog,self).__init__(*args, **kwargs)
    
    def cancel(self):
        self.popup_meal_plan_settings.dismiss()
    
    def set_percentage_availability_all(self):
        self.set_percentage_availability_breakfast()
        self.set_percentage_availability_lunch()
        self.set_percentage_availability_snack()
        self.set_percentage_availability_dinner()

    def set_initial_percentages(self):
        active_number= sum([
            1 for i in (
                self.ids.breakfast.active,
                self.ids.lunch.active,
                self.ids.snack.active,
                self.ids.dinner.active) if i])
        self.ids.breakfast_percent_label.percentage = int(100 / active_number if active_number > 0 else 1) if self.ids.breakfast.active else 0
        self.ids.lunch_percent_label.percentage = int(100 / active_number if active_number > 0 else 1) if self.ids.lunch.active else 0
        self.ids.snack_percent_label.percentage = int(100 / active_number if active_number > 0 else 1) if self.ids.snack.active else 0
        self.ids.dinner_percent_label.percentage = int(100 / active_number if active_number > 0 else 1) if self.ids.dinner.active else 0

    def decrement_breakfast_percentage(self):
        if self.ids.breakfast_percent_label.percentage > 10:
            if self.ids.lunch.active:
                self.ids.breakfast_percent_label.percentage -= 1
                self.ids.lunch_percent_label.percentage += 1
            elif self.ids.snack.active:
                self.ids.breakfast_percent_label.percentage -= 1
                self.ids.snack_percent_label.percentage += 1
            elif self.ids.dinner.active:
                self.ids.breakfast_percent_label.percentage -= 1
                self.ids.dinner_percent_label.percentage += 1

    def set_min_breakfast(self):
        while True:
            old_percentage = self.ids.breakfast_percent_label.percentage
            self.decrement_breakfast_percentage()
            if old_percentage == self.ids.breakfast_percent_label.percentage:
                break
            old_percentage = self.ids.breakfast_percent_label.percentage

    def increment_breakfast_percentage(self):
        if self.ids.breakfast_percent_label.percentage < 100:
            if self.ids.lunch.active and self.ids.lunch_percent_label.percentage > 10:
                self.ids.breakfast_percent_label.percentage += 1
                self.ids.lunch_percent_label.percentage -= 1
            elif self.ids.snack.active and self.ids.snack_percent_label.percentage > 10:
                self.ids.breakfast_percent_label.percentage += 1
                self.ids.snack_percent_label.percentage -= 1
            elif self.ids.dinner.active and self.ids.dinner_percent_label.percentage > 10:
                self.ids.breakfast_percent_label.percentage += 1
                self.ids.dinner_percent_label.percentage -= 1
    
    def set_max_breakfast(self):
        while True:
            old_percentage = self.ids.breakfast_percent_label.percentage
            self.increment_breakfast_percentage()
            if old_percentage == self.ids.breakfast_percent_label.percentage:
                break
            old_percentage = self.ids.breakfast_percent_label.percentage

    def set_percentage_availability_breakfast(self):
        if self.ids.breakfast.active:
            self.ids.set_min_breakfast_button.disabled = False
            self.ids.breakfast_percent_decrement_button.disabled = False
            self.ids.breakfast_percent_label.text_color = (1,1,1,1)
            self.ids.breakfast_percent_increment_button.disabled = False
            self.ids.set_max_breakfast_button.disabled = False
        else:
            self.ids.set_min_breakfast_button.disabled = True
            self.ids.breakfast_percent_decrement_button.disabled = True
            self.ids.breakfast_percent_label.text_color = (1,1,1,.25)
            self.ids.breakfast_percent_increment_button.disabled = True
            self.ids.set_max_breakfast_button.disabled = True
            self.ids.breakfast_percent_label.percentage = 0
        self.set_initial_percentages()

    def decrement_lunch_percentage(self):
        if self.ids.lunch.active:
            if self.ids.lunch_percent_label.percentage > 10:
                if self.ids.snack.active:
                    self.ids.snack_percent_label.percentage += 1
                    self.ids.lunch_percent_label.percentage -= 1
                elif self.ids.dinner.active:
                    self.ids.dinner_percent_label.percentage += 1
                    self.ids.lunch_percent_label.percentage -= 1
    
    def set_min_lunch(self):
        while True:
            old_percentage = self.ids.lunch_percent_label.percentage
            self.decrement_lunch_percentage()
            if old_percentage == self.ids.lunch_percent_label.percentage:
                break
            old_percentage = self.ids.lunch_percent_label.percentage

    def increment_lunch_percentage(self):
        if self.ids.lunch.active:
            if self.ids.lunch_percent_label.percentage + self.ids.breakfast_percent_label.percentage < 100:
                if self.ids.snack.active and self.ids.snack_percent_label.percentage > 10:
                    self.ids.snack_percent_label.percentage -= 1
                    self.ids.lunch_percent_label.percentage += 1
                elif self.ids.dinner.active and self.ids.dinner_percent_label.percentage > 10:
                    self.ids.dinner_percent_label.percentage -= 1
                    self.ids.lunch_percent_label.percentage += 1

    def set_max_lunch(self):
        while True:
            old_percentage = self.ids.lunch_percent_label.percentage
            self.increment_lunch_percentage()
            if old_percentage == self.ids.lunch_percent_label.percentage:
                break
            old_percentage = self.ids.lunch_percent_label.percentage

    def set_percentage_availability_lunch(self):
        if self.ids.lunch.active:
            self.ids.set_min_lunch_button.disabled = False
            self.ids.lunch_percent_decrement_button.disabled = False
            self.ids.lunch_percent_label.text_color = (1,1,1,1)
            self.ids.lunch_percent_increment_button.disabled = False
            self.ids.set_max_lunch_button.disabled = False
        else:
            self.ids.set_min_lunch_button.disabled = True
            self.ids.lunch_percent_decrement_button.disabled = True
            self.ids.lunch_percent_label.text_color = (1,1,1,.25)
            self.ids.lunch_percent_increment_button.disabled = True
            self.ids.set_max_lunch_button.disabled = True
            self.ids.lunch_percent_label.percentage = 0
        self.set_initial_percentages()

    def decrement_snack_percentage(self):
        if self.ids.snack.active:
            if self.ids.snack_percent_label.percentage > 10:
                if self.ids.dinner.active:
                    self.ids.dinner_percent_label.percentage += 1
                    self.ids.snack_percent_label.percentage -= 1
    
    def set_min_snack(self):
        while True:
            old_percentage = self.ids.snack_percent_label.percentage
            self.decrement_snack_percentage()
            if old_percentage == self.ids.snack_percent_label.percentage:
                break
            old_percentage = self.ids.snack_percent_label.percentage

    def increment_snack_percentage(self):
        if self.ids.lunch_percent_label.percentage + self.ids.breakfast_percent_label.percentage + self.ids.snack_percent_label.percentage < 100:
            if self.ids.dinner.active and self.ids.dinner_percent_label.percentage > 10:
                self.ids.dinner_percent_label.percentage -= 1
                self.ids.snack_percent_label.percentage += 1

    def set_max_snack(self):
        while True:
            old_percentage = self.ids.snack_percent_label.percentage
            self.increment_snack_percentage()
            if old_percentage == self.ids.snack_percent_label.percentage:
                break
            old_percentage = self.ids.snack_percent_label.percentage

    def set_percentage_availability_snack(self):
        if self.ids.snack.active:
            self.ids.set_min_snack_button.disabled = False
            self.ids.snack_percent_decrement_button.disabled = False
            self.ids.snack_percent_label.text_color = (1,1,1,1)
            self.ids.snack_percent_increment_button.disabled = False
            self.ids.set_max_snack_button.disabled = False
        else:
            self.ids.set_min_snack_button.disabled = True
            self.ids.snack_percent_decrement_button.disabled = True
            self.ids.snack_percent_label.text_color = (1,1,1,.25)
            self.ids.snack_percent_increment_button.disabled = True
            self.ids.set_max_snack_button.disabled = True
            self.ids.snack_percent_label.percentage = 0
        self.set_initial_percentages()

    def set_percentage_availability_dinner(self):
        if self.ids.dinner.active:
            self.ids.dinner_percent_label.text_color = (1,1,1,1)
        else:
            self.ids.dinner_percent_label.text_color = (1,1,1,.25)
            self.ids.dinner_percent_label.percentage = 0
        self.set_initial_percentages()

    def check_apply_settings_button_validity(self):
        if any([self.ids.breakfast.active,self.ids.lunch.active,self.ids.dinner.active,self.ids.snack.active]):
            self.ids.apply_settings_button.disabled = False
        else:
            self.ids.apply_settings_button.disabled = True

    def decrement_day_range(self):
        if self.ids.day_range.number > 1:
            self.ids.day_range.number -= 1
            if self.ids.day_range.number == 1:
                self.ids.day_range_decrement_button.disabled = True
    
    def increment_day_range(self):
        self.ids.day_range.number += 1
        self.ids.day_range_decrement_button.disabled = False

    def save_settings(self):
        self.Meal_Plan_Screen.breakfast = self.ids.breakfast.active
        self.Meal_Plan_Screen.breakfast_percentage = self.ids.breakfast_percent_label.percentage
        self.Meal_Plan_Screen.lunch = self.ids.lunch.active
        self.Meal_Plan_Screen.lunch_percentage = self.ids.lunch_percent_label.percentage
        self.Meal_Plan_Screen.dinner = self.ids.dinner.active
        self.Meal_Plan_Screen.dinner_percentage = self.ids.dinner_percent_label.percentage
        self.Meal_Plan_Screen.snack = self.ids.snack.active
        self.Meal_Plan_Screen.snack_percentage = self.ids.snack_percent_label.percentage
        self.Meal_Plan_Screen.day_range = self.ids.day_range.number
        self.popup_meal_plan_settings.dismiss()

class Shopping_List_Screen(MDScreen):

    def __init__(self, *args, **kwargs):
        super(Shopping_List_Screen, self).__init__(*args, **kwargs)
        self.ing_icon_dict = {
            "Meat":"food-steak",
            "Fish":"fish",
            "Grains / Bread":"bread-slice-outline",
            "Dairy":"cheese",
            "Vegetable":"carrot",
            "Fruit":"food-apple-outline",
            "Nuts / Seeds":"peanut",
            "Oil / Fats":"bottle-tonic",
            "Condiment":"soy-sauce",
            "Spice":"shaker-outline"
        }
        self.ing_icon_color_dict = {
            "All":(1,1,1,1),
            "Meat":(.39,.24,.04,1),
            "Fish":(1,.61,.39,1),
            "Grains / Bread":(1,.67,.35,1),
            "Dairy":(1,.78,.24,1),
            "Vegetable":(1,.55,.1,1),
            "Fruit":(.9,.16,0,1),
            "Nuts / Seeds":(.78,.53,0,1),
            "Oil / Fats":(.96,.75,0,1),
            "Condiment":(.78,.69,.24,1),
            "Spice":(.95,.95,.99,1)
        }
        s = Session()
        self.shopping_list = eval(s.query(Meal_Plan).get(s.query(Active).first().meal_plan_id).shopping_list) if s.query(Active).first().meal_plan_id else []
        s.close()
        self.sort_value = 5
        self.sort_order = True
        self.filter_type = "All"
        self.exclude_checked_items = False
    
    def transition_to_meal_plan_screen(self):
        self.save_changes()
        MDApp.get_running_app().root.ids.screen_manager.current = "Meal_Plan_Screen"
        MDApp.get_running_app().root.ids.screen_manager.transition.direction = "right"
        MDApp.get_running_app().root.load_active_profile()

    def clear_shopping_list_list(self):
        self.ids.shopping_list_list.clear_widgets()

    def open_filter_menu(self):
        c = Shopping_List_Filter_Dialog()
        self.popup_shopping_list_filter = MDDialog(
            title="Filter and Sort settings",
            type="custom",
            content_cls=c,
            size_hint=(.9, None),
            radius=[20, 7, 20, 7],
            pos_hint={"center_x": .5, "center_y": .5}
        )
        c.logic = self
        c.sort_value = self.sort_value # determines wether to sort by amount (3), calories (2), fats (7), carbohydrates (8) or proteins (9)
        c.sort_order = self.sort_order # bool // False = ascending, True = descending
        c.filter_type = self.filter_type # "Meat", "Fish", "Grains / Bread", "Dairy", "Vegetable", "Fruit", "Nuts / Seeds", "Oil / Fats", "Condiment", "Spice", "All"
        c.exclude_checked_items = self.exclude_checked_items # bool // False = include checked items, True = exclude checked items
        c.popup_shopping_list_filter = self.popup_shopping_list_filter
        c.set_initial_settings()
        self.popup_shopping_list_filter.open()
    
    def refresh_internal_list(self):
        if self.filter_type == "All":
            self.internal_list = list(filter(lambda x: x[6] == False or (x[6] == True and not self.exclude_checked_items), self.shopping_list))
        else:
            self.internal_list = list(filter(lambda x: (x[6] == False and x[5] == self.filter_type) or (x[6] == True and not self.exclude_checked_items and x[5] == self.filter_type), self.shopping_list))
        self.internal_list = sorted(self.internal_list,key = lambda x: x[self.sort_value],reverse = self.sort_order)
        self.display_shopping_list()

    def display_shopping_list(self):
        search = self.ids.ing_search.text
        self.clear_shopping_list_list()
        for i in [i for i in self.internal_list if search.lower() in i[0].lower()]:
            Item = ThreeLineAvatarIconListItem(
                text=i[0],
                secondary_text=(f"{i[2]} kcals " if self.sort_value in [2,3,5] else f"{i[7]} grams of fat " if self.sort_value == 7 else f"{i[8]} grams of carbohydrates " if self.sort_value == 8 else f"{i[9]} grams of protein ") + f"per {'100' if i[1] =='gram' or i[1] =='ml' else ''} {i[1]}{'s' if i[1] == 'gram' or i[1] == 'ml' else ''}",
                tertiary_text=f"{i[3]} {i[1]}{'s' if i[3] != 1 else ''}" if i[1] != "piece" else f"{str(int(i[3]/i[4]))} " + f"{str(i[3]%i[4]) + '/' + str(i[4]) if i[3]%i[4] != 0 else ''} {i[1]}{'s' if i[3] != i[4] else ''}",
                on_release=self.check_list_item
            )
            Item.add_widget(
                MDBoxLayout(
                    Widget(size_hint_x=15),
                    IconRightWidget(
                        icon="check" if i[6] else "close",
                        theme_text_color="Custom",
                        text_color=(0,1,0,1) if i[6] else (1,0,0,1),
                        size_hint_x=2,
                        pos_hint={"center_y":.5}
                    ),
                    orientation='horizontal',
                    size_hint_x=None,
                    width=MDApp.get_running_app().root.width*.95,
                    pos_hint={"center_y": .5}
                )
            )
            Item.add_widget(IconLeftWidget(
                    icon=self.ing_icon_dict[i[5]],
                    theme_text_color="Custom",
                    text_color=self.ing_icon_color_dict[i[5]]
                )
            )
            MDApp.get_running_app().root.ids.shopping_list_screen.ids.shopping_list_list.add_widget(Item)

    def check_list_item(self, instance):
        instance.children[0].children[0].icon = "check" if instance.children[0].children[0].icon == "close" else "close"
        instance.children[0].children[0].text_color = (0,1,0,1) if instance.children[0].children[0].icon == "check" else (1,0,0,1)
        self.shopping_list[next(index for index, i in enumerate(self.shopping_list) if i[0] == instance.text)][6] = True if instance.children[0].children[0].icon == "check" else False
        if self.exclude_checked_items:
            self.ids.shopping_list_list.remove_widget(instance)
    def save_changes(self): # function currently gets executed only when switching back to the meal plan screen
        if MDApp.get_running_app().root.ids.meal_plan_screen.active_meal_plan_id: # ensures that there is a database entry for the mealplan the shoppinglist is associated with!
            s = Session()
            s.query(Meal_Plan).filter(Meal_Plan.id == MDApp.get_running_app().root.ids.meal_plan_screen.active_meal_plan_id).update({"shopping_list":str(self.shopping_list)})
            s.commit()
            s.close()

class Shopping_List_Filter_Dialog(MDBoxLayout):

    def __init__(self, *args, **kwargs):
        super(Shopping_List_Filter_Dialog, self).__init__(*args, **kwargs)
        self.sort_value = 5 # 5 corresponds to type by default
        self.sort_order = True # corresponds to the sort reverse attribute (high to low, low to high) # what is what I havent determined yet
        self.filter_type = "All"
        self.exclude_checked_items = False # corresponds to wether or not checked items should be shown
        self.ing_icon_dict = {
            "All":"filter-variant",
            "Meat":"food-steak",
            "Fish":"fish",
            "Grains / Bread":"bread-slice-outline",
            "Dairy":"cheese",
            "Vegetable":"carrot",
            "Fruit":"food-apple-outline",
            "Nuts / Seeds":"peanut",
            "Oil / Fats":"bottle-tonic",
            "Condiment":"soy-sauce",
            "Spice":"shaker-outline"
        }
        self.ing_icon_color_dict = {
            "All":(1,1,1,1),
            "Meat":(.39,.24,.04,1),
            "Fish":(1,.61,.39,1),
            "Grains / Bread":(1,.67,.35,1),
            "Dairy":(1,.78,.24,1),
            "Vegetable":(1,.55,.1,1),
            "Fruit":(.9,.16,0,1),
            "Nuts / Seeds":(.78,.53,0,1),
            "Oil / Fats":(.96,.75,0,1),
            "Condiment":(.78,.69,.24,1),
            "Spice":(.95,.95,.99,1)
        }
    
    def set_initial_settings(self):
        if self.sort_value == 3:
            self.ids.sort_by_amount.active = True
            self.ids.sort_by_amount_label.text_color = (1,1,1,1)
        elif self.sort_value == 2:
            self.ids.sort_by_calories.active = True
            self.ids.sort_by_calories_label.text_color = (1,1,1,1)
        elif self.sort_value == 7:
            self.ids.sort_by_fats.active = True
            self.ids.sort_by_fats_label.text_color = (1,1,1,1)
        elif self.sort_value == 8:
            self.ids.sort_by_carbohydrates.active = True
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,1)
        elif self.sort_value == 9:
            self.ids.sort_by_proteins.active = True
            self.ids.sort_by_proteins_label.text_color = (1,1,1,1)
        if self.sort_order:
            self.ids.sorting_direction.icon = "sort-descending"
            self.ids.sort_order_label.text = "High to Low"
        else:
            self.ids.sorting_direction.icon = "sort-ascending"
            self.ids.sort_order_label.text = "Low to High"
        self.ids.ingredient_type_filter.icon = self.ing_icon_dict[self.filter_type]
        self.ids.ingredient_type_filter.text_color = self.ing_icon_color_dict[self.filter_type]
        self.ids.exclude_checked_items.active = self.exclude_checked_items

    def cancel(self):
        self.popup_shopping_list_filter.dismiss()

    def check_amount(self,instance,value):
        if value:
            self.ids.sort_by_calories.active = False
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)
            self.ids.sort_by_fats.active = False
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates.active = False
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins.active = False
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)
            self.ids.sort_by_amount_label.text_color = (1,1,1,1)
            self.sort_value = 3
        else:
            self.sort_value = 5
            self.ids.sort_by_amount_label.text_color = (1,1,1,.25)

    def check_calories(self,instance,value):
        if value:
            self.ids.sort_by_amount.active = False
            self.ids.sort_by_amount_label.text_color = (1,1,1,.25)
            self.ids.sort_by_fats.active = False
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates.active = False
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins.active = False
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)
            self.ids.sort_by_calories_label.text_color = (1,1,1,1)
            self.sort_value = 2
        else:
            self.sort_value = 5
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)

    def check_fats(self,instance,value):
        if value:
            self.ids.sort_by_amount.active = False
            self.ids.sort_by_amount_label.text_color = (1,1,1,.25)
            self.ids.sort_by_calories.active = False
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates.active = False
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins.active = False
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)
            self.ids.sort_by_fats_label.text_color = (1,1,1,1)
            self.sort_value = 7
        else:
            self.sort_value = 5
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
    
    def check_carbohydrates(self,instance,value):
        if value:
            self.ids.sort_by_amount.active = False
            self.ids.sort_by_amount_label.text_color = (1,1,1,.25)
            self.ids.sort_by_calories.active = False
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)
            self.ids.sort_by_fats.active = False
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins.active = False
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,1)
            self.sort_value = 8
        else:
            self.sort_value = 5
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)

    def check_proteins(self,instance,value):
        if value:
            self.ids.sort_by_amount.active = False
            self.ids.sort_by_amount_label.text_color = (1,1,1,.25)
            self.ids.sort_by_calories.active = False
            self.ids.sort_by_calories_label.text_color = (1,1,1,.25)
            self.ids.sort_by_fats.active = False
            self.ids.sort_by_fats_label.text_color = (1,1,1,.25)
            self.ids.sort_by_carbohydrates.active = False
            self.ids.sort_by_carbohydrates_label.text_color = (1,1,1,.25)
            self.ids.sort_by_proteins_label.text_color = (1,1,1,1)
            self.sort_value = 9
        else:
            self.sort_value = 5
            self.ids.sort_by_proteins_label.text_color = (1,1,1,.25)

    def set_sort_order(self):
        self.ids.sorting_direction.icon = "sort-ascending" if self.ids.sorting_direction.icon == "sort-descending" else "sort-descending"
        self.sort_order = False if self.ids.sorting_direction.icon == "sort-ascending" else True
        self.ids.sort_order_label.text = "High to Low" if self.sort_order else "Low to High"

    def open_filter_dropdown(self):
        self.choices_filter = [
            {
                "viewclass": "OneLineAvatarIconListItem",
                "text": "All",
                "icon":"filter-variant",
                "height": dp(56),
                "on_release": lambda x="filter-variant",y="All": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineAvatarIconListItem",
                "text": "Meat",
                "icon": "food-steak",
                "height": dp(56),
                "on_release": lambda x="food-steak",y="Meat": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fish",
                "icon": "fish",
                "height": dp(56),
                "on_release": lambda x="fish",y="Fish": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Grains / Bread",
                "icon": "bread-slice-outline",
                "height": dp(56),
                "on_release": lambda x="bread-slice-outline",y="Grains / Bread": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Dairy",
                "icon": "cheese",
                "height": dp(56),
                "on_release": lambda x="cheese",y="Dairy": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Vegetable",
                "icon": "carrot",
                "height": dp(56),
                "on_release": lambda x="carrot",y="Vegetable": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Fruit",
                "icon": "food-apple-outline",
                "height": dp(56),
                "on_release": lambda x="food-apple-outline",y="Fruit": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Nuts / Seeds",
                "icon": "peanut",
                "height": dp(56),
                "on_release": lambda x="peanut",y="Nuts / Seeds": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Oil / Fats",
                "icon": "bottle-tonic",
                "height": dp(56),
                "on_release": lambda x="bottle-tonic",y="Oil / Fats": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Condiment",
                "icon": "soy-sauce",
                "height": dp(56),
                "on_release": lambda x="soy-sauce",y="Condiment": self.set_filter_icon(x,y)
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Spice",
                "icon": "shaker-outline",
                "height": dp(56),
                "on_release": lambda x="shaker-outline",y="Spice": self.set_filter_icon(x,y)
            },
        ]
        self.menu_list_type = MDDropdownMenu(
            caller=self.ids.ingredient_type_filter,
            items=self.choices_filter,
            position="auto",
            width_mult=4
        )
        self.menu_list_type.open()

    def set_filter_icon(self, icon, ing_type):
        self.ids.ingredient_type_filter.icon = icon
        self.ids.ingredient_type_filter.text_color = self.ing_icon_color_dict[ing_type]
        self.filter_type = ing_type
        self.menu_list_type.dismiss()

    def check_checked_items(self, instance, value):
        self.exclude_checked_items = value

    def apply_filter(self):
        self.logic.sort_value = self.sort_value
        self.logic.sort_order = self.sort_order
        self.logic.filter_type = self.filter_type
        self.logic.exclude_checked_items = self.exclude_checked_items
        self.logic.refresh_internal_list()
        self.popup_shopping_list_filter.dismiss()

class Text_Input_Dialog(MDBoxLayout):

    def __init__(self, instance, *args, **kwargs):
        super(Text_Input_Dialog, self).__init__(*args, **kwargs)
        self.instance = instance
        self.ids.text_input.hint_text = instance.hint_text
        self.ids.text_input.text = instance.text
        self.ids.text_input.focus = True

    def apply(self,instance):
        self.instance.text = instance.text
        self.popup_base.dismiss()

class Number_Input_Dialog(MDBoxLayout):

    def __init__(self, instance, *args, **kwargs):
        super(Number_Input_Dialog, self).__init__(*args, **kwargs)
        self.instance = instance
        self.ids.number_input.hint_text = instance.hint_text
        self.ids.number_input.text = instance.text
        self.ids.number_input.focus = True
    
    def apply(self,instance):
        self.instance.text = instance.text
        self.popup_base.dismiss()

class Main_Logic(MDScreen):

    def __init__(self, *args, **kwargs):
        super(Main_Logic, self).__init__(*args, **kwargs)
        s = Session()
        if not s.query(Active).first():
            s.add(Active(settings_id=None,
                         meal_plan_id=None))
        s.commit()
        s.close()

    def open_number_input_dialog(self,instance,title):
        if instance.focus:
            instance.focus = False
            c = Number_Input_Dialog(instance=instance)
            self.popup_base = MDDialog(
                title=title,
                type="custom",
                content_cls=c,
                size_hint=(.9,None),
                pos_hint={"center_y":.65,"center_x":.5},
                radius=[20, 7, 20, 7]
            )
            c.popup_base = self.popup_base
            self.popup_base.open()

    def open_text_input_dialog(self,instance,title):
        if instance.focus:
            instance.focus = False
            c = Text_Input_Dialog(instance=instance)
            self.popup_base = MDDialog(
                title=title,
                type="custom",
                content_cls=c,
                size_hint=(.9,None),
                pos_hint={"center_y":.65,"center_x":.5},
                radius=[20, 7, 20, 7]
            )
            c.popup_base = self.popup_base
            self.popup_base.open()

    def load_active_profile(self):
        s = Session()
        active = s.query(Active).first()
        if active:
            settings = s.query(Settings).filter(Settings.id == active.settings_id).first()
            if settings:
                MDApp.get_running_app().root.ids.settings_screen.load_active_settings()
                icon_dict = {
                    "Male":"gender-male",
                    "Female":"gender-female"
                }
                self.ids.nav_drawer.ids.profile_gender_icon.icon = icon_dict[str(settings.gender)]
                self.ids.nav_drawer.ids.profile_name.text = settings.name
                self.ids.nav_drawer.ids.profile_weight.text = f"{settings.weight} kg"
                self.ids.nav_drawer.ids.profile_calories_per_day.text = f"{settings.calories_per_day} kcals/day"
        s.close()

    def get_ingredients(self):
        # Populates the ingredient list with all ingredients in the database
        MDApp.get_running_app().root.ids.ingredients_screen.refresh_all_ingredients_list()
    def get_meals(self):
        # Populates the meal list with all meals in the database
        MDApp.get_running_app().root.ids.meals_screen.refresh_internal_list()
        MDApp.get_running_app().root.ids.meals_screen.refresh_display_list()
    
    def get_meal_plan(self):
        MDApp.get_running_app().root.ids.meal_plan_screen.display_meal_plan()
        MDApp.get_running_app().root.ids.meal_plan_screen.erase_meal_plan_and_save_meal_plan_button_check_validity()
        MDApp.get_running_app().root.ids.meal_plan_screen.adjust_calories_button_check_validity()
        MDApp.get_running_app().root.ids.meal_plan_screen.set_page_icon_validity_status()

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return Main_Logic()
    
    def on_start(self):
        Base.metadata.create_all(bind=engine)
        self.root.load_active_profile()
        self.root.get_ingredients()
        self.root.get_meals()
        self.root.get_meal_plan()

if __name__ == "__main__":
    MainApp().run()
