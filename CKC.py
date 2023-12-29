#Custom Kivy Classes

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import ThreeLineAvatarIconListItem, ThreeLineListItem
from kivy.properties import NumericProperty, StringProperty, ObjectProperty

class Custom_MDGridLayout(MDGridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

class MDLabelPercentage(MDLabel):
    percentage = NumericProperty(0)

    def on_percentage(self, instance, value):
        self.text = f"{value} %"

class MDLabelNumber(MDLabel):
    number = NumericProperty(0)

    def on_number(self, instance, value):
        self.text = str(value)

class MDLabelFraction(MDLabel):
    numerator = NumericProperty(0)
    denominator = NumericProperty(0)

    def on_numerator(self, instance, value):
        self.text = f"{self.numerator}/{self.denominator}"

    def on_denominator(self, instance, value):
        self.text = f"{self.numerator}/{self.denominator}"

class MDIconButtonSpinner(MDIconButton):
    text = ObjectProperty(None)
    value = ObjectProperty(None)

class ThreeLineAvatarIconObjectListItem(ThreeLineAvatarIconListItem):
    obj = ObjectProperty(None)
    asc_obj_id = NumericProperty(None)
    meal_id = NumericProperty(None)
    ingredient_id = NumericProperty(None)
    ing_unit = StringProperty(None)
    divisible_by = NumericProperty(None)

class ThreeLineValueListItem(ThreeLineListItem):
    meal_plan_id = NumericProperty(None)
