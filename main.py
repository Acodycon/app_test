<Main_Logic>:
    name: "Main_Logic"
    screen_manager: screen_manager
    meal_plan_screen: meal_plan_screen
    settings_screen: settings_screen
    ingredients_screen: ingredients_screen
    meals_screen: meals_screen
    shopping_list_screen: shopping_list_screen
    nav_drawer: nav_drawer
    MDNavigationLayout:
        size_hint_y:1
        MDScreenManager:
            id: screen_manager
            Meal_Plan_Screen:
                id: meal_plan_screen
            Settings_Screen:
                id: settings_screen
            Ingredients_Screen:
                id: ingredients_screen
            Meals_Screen:
                id: meals_screen
            Shopping_List_Screen:
                id: shopping_list_screen
        Nav_Drawer:
            id: nav_drawer

<Nav_Drawer@MDNavigationDrawer>:
    swipe_distance: 0
    swipe_edge_width: 0
    name: "nav_drawer"
    padding: dp(5)
    profile_gender_icon: profile_gender_icon
    profile_name: profile_name
    profile_weight: profile_weight
    navigation_list: navigation_list
    MDBoxLayout:
        padding: dp(5)
        spacing: dp(10)
        orientation: "vertical"
        MDBoxLayout:
            size_hint_y: None
            height: profile_name.height
            MDIconButton:
                id: profile_gender_icon
                pos_hint: {"center_y":.5,"left":0}
                icon: ""
            MDLabel:
                id: profile_name
                text: "Current Settings"
                font_style: "H6"
                size_hint_y: None
                height: self.texture_size[1]
        MDLabel:
            id: profile_weight
            text: "Setting 2"
            font_style: "Subtitle1"
            size_hint_y: None
            height: self.texture_size[1]
        MDLabel:
            id: profile_calories_per_day
            text: "Setting 3"
            font_style: "Subtitle1"
            size_hint_y: None
            height: self.texture_size[1]
        MDScrollView:
            MDList:
                id: navigation_list
                OneLineIconListItem:
                    text: "Settings"
                    on_release:
                        app.root.ids.screen_manager.current = "Settings_Screen"
                        root.set_state("close")
                    IconLeftWidget:
                        icon: "cogs"
                OneLineIconListItem:
                    text: "Ingredients"
                    on_release:
                        app.root.ids.screen_manager.current = "Ingredients_Screen"
                        root.set_state("close")
                    IconLeftWidget:
                        icon: "food-drumstick-outline"
                OneLineIconListItem:
                    text: "Meals"
                    on_release:
                        app.root.ids.screen_manager.current = "Meals_Screen"
                        root.set_state("close")
                    IconLeftWidget:
                        icon: "food"
                OneLineIconListItem:
                    text: "Shopping list"
                    on_release:
                        app.root.ids.screen_manager.current = "Shopping_List_Screen"
                        root.set_state("close")
                    IconLeftWidget:
                        icon: "shopping-outline"
<Meal_Plan_Screen>:
    name: "Meal_Plan_Screen"
    meal_plan_title: meal_plan_title
    increment_page_button: increment_page_button
    current_meal_plan_display_name: current_meal_plan_display_name
    decrement_page_button: decrement_page_button
    meal_plan: meal_plan
    bottom_app_bar: bottom_app_bar
    erase_meal_plan_button: erase_meal_plan_button
    save_meal_plan_button: save_meal_plan_button
    display_saved_meal_plans_button: display_saved_meal_plans_button
    adjust_calories_button: adjust_calories_button
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Navigator"
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("toggle")]]
        Widget:
            size_hint_y:None
            height: dp(2)
        MDTopAppBar:
            id: meal_plan_title
            MDBoxLayout:
                ActionTopAppBarButton:
                    id: decrement_page_button
                    icon: "chevron-left"
                    theme_text_color: "Custom"
                    text_color: (0,0,0,1)
                    pos_hint: {"center_y":1}
                    on_release:
                        root.decrement_page()
                MDLabel:
                    id: current_meal_plan_display_name
                    text: "No current meal plan!"
                    theme_text_color: "Custom"
                    text_color: 0,0,0,1
                    pos_hint: {"center_y":1}
                    halign: "center"
                    font_style: "H6"
                ActionTopAppBarButton:
                    id: increment_page_button
                    icon: "chevron-right"
                    theme_text_color: "Custom"
                    text_color: (0,0,0,1)
                    pos_hint: {"center_y":1}
                    on_release:
                        root.increment_page()
            # right_action_items: [["chevron-right", lambda x: root.increment_page()]]
            # left_action_items: [["chevron-left", lambda x: root.decrement_page()]]
        Widget:
            size_hint_y:None
            height: dp(2)
        PageLayout:
            id: meal_plan
            on_page:
                root.display_page_title()
    MDBottomAppBar:
        MDTopAppBar:
            id: bottom_app_bar
            icon: "restart"
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            on_action_button: root.generate_meal_plan()
            type: "bottom"
            mode: "end"
            MDBoxLayout:
                ActionTopAppBarButton:
                    icon: "dots-vertical"
                    theme_text_color: "Custom"
                    text_color: (0,0,0,1)
                    pos_hint: {"center_y":1}
                    on_release:
                        root.open_meal_plan_settings()
                ActionTopAppBarButton:
                    id: erase_meal_plan_button
                    icon: "eraser"
                    theme_text_color: "Custom"
                    text_color: (0,0,0,1)
                    pos_hint: {"center_y":1}
                    on_touch_down:
                        root.test_touch_down(*args)
                    on_touch_up:
                        root.test_touch_up(*args)
                    on_release:
                        root.erase_meal_plan()
                ActionTopAppBarButton:
                    id: save_meal_plan_button
                    icon: "content-save-outline"
                    theme_text_color: "Custom"
                    text_color: (0,0,0,1)
                    pos_hint: {"center_y":1}
                    on_touch_down:
                        root.test_touch_down(*args)
                    on_touch_up:
                        root.test_touch_up(*args)
                    on_release:
                        root.open_save_meal_plan_options()
                ActionTopAppBarButton:
                    id: display_saved_meal_plans_button
                    icon: "folder-open-outline"
                    theme_text_color: "Custom"
                    text_color: (0,0,0,1)
                    pos_hint: {"center_y":1}
                    on_touch_down:
                        root.test_touch_down(*args)
                    on_touch_up:
                        root.test_touch_up(*args)
                    on_release:
                        root.open_load_meal_plan_dialog()
                ActionTopAppBarButton:
                    id: adjust_calories_button
                    icon: "adjust"
                    theme_text_color: "Custom"
                    text_color: (0,0,0,1)
                    pos_hint: {"center_y":1}
                    on_touch_down:
                        root.test_touch_down(*args)
                    on_touch_up:
                        root.test_touch_up(*args)
                    on_release:
                        root.adjust_calories()
<Meal_Plan_Item>:
    size_hint_x: None
    width: app.root.width*.8
    size_hint_y: None
    height: box_name_and_icons.height + box_stats.height
    orientation: "vertical"
    box_name_and_icons: box_name_and_icons
    box_stats: box_stats
    meal_name: meal_name
    icon_meal_type: icon_meal_type
    icon_meal_sweet_savory: icon_meal_sweet_savory
    icon_meal_hot_cold: icon_meal_hot_cold
    meal_calories: meal_calories
    meal_fats: meal_fats
    meal_carbohydrates: meal_carbohydrates
    meal_proteins: meal_proteins
    canvas:
        Color:
            rgba: self.color
        RoundedRectangle:
            pos: self.pos
            size: self.width,self.height
            radius: [20,20,20,20]
        Color:
            rgba: .9,.9,.9,1
        Line:
            width:1.5
            rounded_rectangle:self.x,self.y,self.width,self.height,20,20,20,20
    MDBoxLayout:
        name: "Box_Name_And_Icons"
        id: box_name_and_icons
        orientation: "vertical"
        size_hint_y: None
        height: meal_name.height + icon_meal_type.height*1.5
        MDBoxLayout:
            MDIconButton:
                id: icon_meal_type
                icon_size: dp(25)
                pos_hint: {"center_y":.5,"left":1}
                theme_text_color: "Custom"
                on_release:
                    root.show_type()
            Widget:
            MDIconButton:
                id: icon_meal_sweet_savory
                icon_size: dp(25)
                pos_hint: {"center_y":.5,"right":.8}
                theme_text_color: "Custom"
                on_release:
                    root.show_sweet_savory()
            MDIconButton:
                id: icon_meal_hot_cold
                icon_size: dp(25)
                pos_hint: {"center_y":.5,"right":.9}
                theme_text_color: "Custom"
                on_release:
                    root.show_hot_cold()
            MDIconButton:
                icon: "swap-horizontal"
                icon_size: dp(25)
                pos_hint: {"center_y":.5,"right":1}
                on_release:
                    root.open_swap_options_dialog()
        MDBoxLayout:
            size_hint_y: None
            height: meal_name.height
            Widget:
                size_hint_x:1
            MDLabel:
                id: meal_name
                text: "meal title"
                theme_text_color: "Custom"
                text_color: 1,1,1,1
                font_style: "H5"
                size_hint_x:8
                size_hint_y: None
                height: self.texture_size[1]
            Widget:
                size_hint_x:1
    MDBoxLayout:
        name: "Box_Stats"
        id: box_stats
        orientation: "vertical"
        size_hint_y: None
        height: meal_calories.height + meal_fats.height * 7
        canvas:
            Color:
                rgba: 0,0,0,.5
            RoundedRectangle:
                pos: self.x + self.width*.05,self.y + self.height*.05
                size: self.width*.9,self.height*.9
                radius: [20,20,20,20]
            Color:
                rgba: 0,0,0,1
            Line:
                width:1
                rounded_rectangle:self.x + self.width*.05,self.y + self.height*.05,self.width*.9,self.height*.9,20,20,20,20
        Widget:
            size_hint_y: None
            height: meal_fats.height
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: meal_calories
                text: "Calories"
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: .85,.85,.85,1
                size_hint_x:9
                size_hint_y: None
                height: self.texture_size[1]
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: meal_fats
                text: "Stats"
                font_style: "Subtitle2"
                theme_text_color: "Custom"
                text_color: .6,.6,.6,1
                size_hint_x:9
                size_hint_y: None
                height: self.texture_size[1]
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: meal_carbohydrates
                text: "Stats"
                font_style: "Subtitle2"
                theme_text_color: "Custom"
                text_color: .6,.6,.6,1
                size_hint_x:9
                size_hint_y: None
                height: self.texture_size[1]
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: meal_proteins
                text: "Stats"
                font_style: "Subtitle2"
                theme_text_color: "Custom"
                text_color: .6,.6,.6,1
                size_hint_x:9
                size_hint_y: None
                height: self.texture_size[1]
        Widget:
            size_hint_y: None
            height: meal_fats.height
<Swap_Options_Dialog>:
    size_hint_y:None
    height: app.root.height *.1
    MDBoxLayout:
        orientation: "vertical"
        size_hint_x:1
        MDFlatButton:
            text: "Cancel"
            size_hint_y:1
            pos_hint: {"center_y":.5,"center_x":.5}
            on_release:
                root.cancel()
    MDBoxLayout:
        orientation: "vertical"
        size_hint_x:1
        MDLabel:
            text: "Random"
            halign: "center"
        MDIconButton:
            icon: "dice-5-outline"
            pos_hint: {"center_x":.5,"center_y":.5}
            on_release:
                root.select_new_meal_random()
    MDBoxLayout:
        orientation: "vertical"
        size_hint_x:1
        MDLabel:
            text: "Manuel"
            halign: "center"
        MDIconButton:
            icon: "card-multiple-outline"
            pos_hint: {"center_x":.5}
            on_release:
                root.select_new_meal_manuel()
<Save_Meal_Plan_Dialog>:
    size_hint_y:None
    height: app.root.height *.1
    orientation: "vertical"
    meal_plan_name: meal_plan_name
    safe_button: safe_button
    MDTextField:
        size_hint_y: 1
        id: meal_plan_name
        on_text:
            root.check_save_button_validity()
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x:.5
        MDFlatButton:
            text: "Cancel"
            size_hint_x:1
            on_release:
                root.cancel()
        Widget:
            size_hint_x:1
        MDRaisedButton:
            id: safe_button
            text: "Save"
            size_hint_x:1
            disabled: True
            on_release:
                root.save_meal_plan()
        Widget:
            size_hint_x:.5
<Save_Meal_Plan_Changes_Dialog>:
    size_hint_y:None
    height: app.root.height *.1
    Widget:
        size_hint_x:1
    MDFlatButton:
        text: "Cancel"
        size_hint:2,.5
        on_release:
            root.cancel()
    Widget:
        size_hint_x:2
    MDRaisedButton:
        text: "Save"
        size_hint:2,.5
        on_release:
            root.save_changes()
    Widget:
        size_hint_x:1

<Meal_Plan_Already_Exists_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint: 6,None
    MDFlatButton:
        text: "Cancel"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.cancel()
    Widget:
        size_hint: 1,None
    MDRaisedButton:
        text: "Overwrite"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.overwrite_meal_plan()
    Widget:
        size_hint: 1,None

<Load_Meal_Plan_Dialog>:
    size_hint_y: None
    height: app.root.height*.8
    search: search
    meal_plan_list: meal_plan_list
    MDBoxLayout:
        orientation: "vertical"
        MDTextField:
            id: search
            size_hint_y:1
            hint_text: "Search"
            pos_hint: {"top":1}
            on_text:
                root.refresh_display_list()
        MDScrollView:
            size_hint_y:8
            MDList:
                id: meal_plan_list
        MDBoxLayout:
            size_hint_y:1
            Widget:
                size_hint_x: 1
            MDFlatButton:
                text: "Cancel"
                size_hint:1,.5
                on_release:
                    root.cancel()
            Widget:
                size_hint_x: 1

<Select_Meal_Plan_Options_Dialog>:
    size_hint_y:None
    height: app.root.height *.1
    Widget:
        size_hint_x:1
    MDRaisedButton:
        text: "Delete"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.delete()
    Widget:
        size_hint_x:1
    MDRaisedButton:
        text: "Load plan"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.load_meal_plan()
    Widget:
        size_hint_x:1

<Delete_Meal_Plan_Dialog>
    size_hint_y:None
    height: app.root.height *.1
    Widget:
        size_hint: 6,None
    MDFlatButton:
        text: "Cancel"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.cancel()
    Widget:
        size_hint: 1,None
    MDRaisedButton:
        text: "Delete"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.delete()
    Widget:
        size_hint: 1,None
<Meal_Plan_Settings_Dialog>:
    size_hint_y: None
    height: app.root.height*.8
    orientation: "vertical"
    day_range_decrement_button: day_range_decrement_button
    day_range: day_range
    breakfast: breakfast
    set_min_breakfast_button: set_min_breakfast_button
    breakfast_percent_decrement_button: breakfast_percent_decrement_button
    breakfast_percent_label: breakfast_percent_label
    breakfast_percent_increment_button: breakfast_percent_increment_button
    set_max_breakfast_button: set_max_breakfast_button
    lunch: lunch
    set_min_lunch_button: set_min_lunch_button
    lunch_percent_decrement_button: lunch_percent_decrement_button
    lunch_percent_label: lunch_percent_label
    lunch_percent_increment_button: lunch_percent_increment_button
    set_max_lunch_button: set_max_lunch_button
    snack: snack
    set_min_snack_button: set_min_snack_button
    snack_percent_decrement_button: snack_percent_decrement_button
    snack_percent_label: snack_percent_label
    snack_percent_increment_button: snack_percent_increment_button
    set_max_snack_button: set_max_snack_button
    dinner: dinner
    dinner_percent_label: dinner_percent_label
    apply_settings_button: apply_settings_button
    MDLabel:
        size_hint_y:1
        text: "Length in days"
        halign: "center"
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:.5
        MDIconButton:
            id: day_range_decrement_button
            icon: "minus"
            icon_size: dp(25)
            pos_hint: {"center_y":.5}
            size_hint_x:1
            on_release:
                root.decrement_day_range()
        MDLabelNumber:
            id: day_range
            number: 0
            halign: "center"
            size_hint_x:1
        MDIconButton:
            icon: "plus"
            icon_size: dp(25)
            pos_hint: {"center_y":.5}
            size_hint_x:1
            on_release:
                root.increment_day_range()
        Widget:
            size_hint_x:.5
    MDLabel:
        size_hint_y:1
        text: "Meals included and percentage"
        halign: "center"
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "breakfast"
            size_hint_x:2
        MDCheckbox:
            id: breakfast
            size_hint_x:.8
            on_active:
                root.check_apply_settings_button_validity()
                root.set_percentage_availability_breakfast()
        MDIconButton:
            id: breakfast_percent_decrement_button
            icon: "minus"
            pos_hint: {"center_y":.5}
            on_release:
                root.decrement_breakfast_percentage()
        MDLabelPercentage:
            id: breakfast_percent_label
            theme_text_color: "Custom"
            percentage: 25
            halign: "center"
        MDIconButton:
            id: breakfast_percent_increment_button
            icon: "plus"
            pos_hint: {"center_y":.5}
            on_release:
                root.increment_breakfast_percentage()
        MDBoxLayout:
            orientation: "vertical"
            MDIconButton:
                id: set_max_breakfast_button
                icon: "chevron-double-up"
                pos_hint: {"center_y":.5}
                on_release:
                    root.set_max_breakfast()
            MDIconButton:
                id: set_min_breakfast_button
                icon: "chevron-double-down"
                pos_hint: {"center_y":.5}
                on_release:
                    root.set_min_breakfast()
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "lunch"
            size_hint_x:2
        MDCheckbox:
            id: lunch
            size_hint_x:.8
            on_active:
                root.check_apply_settings_button_validity()
                root.set_percentage_availability_lunch()
        MDIconButton:
            id: lunch_percent_decrement_button
            icon: "minus"
            pos_hint: {"center_y":.5}
            on_release:
                root.decrement_lunch_percentage()
        MDLabelPercentage:
            id: lunch_percent_label
            theme_text_color: "Custom"
            percentage: 25
            halign: "center"
        MDIconButton:
            id: lunch_percent_increment_button
            icon: "plus"
            pos_hint: {"center_y":.5}
            on_release:
                root.increment_lunch_percentage()
        MDBoxLayout:
            orientation: "vertical"
            MDIconButton:
                id: set_max_lunch_button
                icon: "chevron-double-up"
                pos_hint: {"center_y":.5}
                on_release:
                    root.set_max_lunch()
            MDIconButton:
                id: set_min_lunch_button
                icon: "chevron-double-down"
                pos_hint: {"center_y":.5}
                on_release:
                    root.set_min_lunch()
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "snack"
            size_hint_x:2
        MDCheckbox:
            id: snack
            size_hint_x:.8
            on_active:
                root.check_apply_settings_button_validity()
                root.set_percentage_availability_snack()
        MDIconButton:
            id: snack_percent_decrement_button
            icon: "minus"
            pos_hint: {"center_y":.5}
            on_release:
                root.decrement_snack_percentage()
        MDLabelPercentage:
            id: snack_percent_label
            theme_text_color: "Custom"
            percentage: 25
            halign: "center"
        MDIconButton:
            id: snack_percent_increment_button
            icon: "plus"
            pos_hint: {"center_y":.5}
            on_release:
                root.increment_snack_percentage()
        MDBoxLayout:
            orientation: "vertical"
            MDIconButton:
                id: set_max_snack_button
                icon: "chevron-double-up"
                pos_hint: {"center_y":.5}
                on_release:
                    root.set_max_snack()
            MDIconButton:
                id: set_min_snack_button
                icon: "chevron-double-down"
                pos_hint: {"center_y":.5}
                on_release:
                    root.set_min_snack()
    MDBoxLayout:
        size_hint_y:1
        MDLabel:
            text: "dinner"
            halign: "center"
        MDCheckbox:
            id: dinner
            on_active:
                root.check_apply_settings_button_validity()
                root.set_percentage_availability_dinner()
        MDLabelPercentage:
            id: dinner_percent_label
            theme_text_color: "Custom"
            percentage: 25
            halign: "center"
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDFlatButton:
            text: "Cancel"
            size_hint_y:.5
            size_hint_x:2
            pos_hint: {"center_y":.5}
            on_release:
                root.cancel()
        Widget:
            size_hint_x:1
        MDRaisedButton:
            id: apply_settings_button
            disabled: True
            size_hint_y:.5
            size_hint_x:2
            pos_hint: {"center_y":.5}
            text: "Save settings"
            on_release:
                root.save_settings()
        Widget:
            size_hint_x:1

<Settings_Screen>:
    name: "Settings_Screen"
    profile_name_input: profile_name_input
    gender_input: gender_input
    activity_input: activity_input
    weight_gain_input: weight_gain_input
    weight_input: weight_input
    height_input: height_input
    age_input: age_input
    calories_per_day: calories_per_day
    bmr: bmr
    tdee: tdee
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            pos_hint: {"top":1}
            title: "Settings"
            font_style: "H1"
            left_action_items: [["chevron-left", lambda x: root.transition_to_meal_plan_screen()],["swap-horizontal", lambda x: root.open_settings_search()]]
        MDScrollView:
            size_hint: .9,7.5
            MDGridLayout:
                cols:1
                size_hint_y: None
                pos_hint_x: "center"
                spacing: dp(10)
                padding: dp(10)
                row_default_height: dp(50)
                height: self.minimum_height
                MDBoxLayout:
                    Widget:
                        size_hint_x: 1
                    MDLabel:
                        text: "Name"
                        size_hint_x: 8
                    MDTextField:
                        id: profile_name_input
                        size_hint_x: 4
                        on_text:
                            root.open_gender_dropdown() if not root.active_settings_id else None
                        on_focus:
                            app.root.open_text_input_dialog(self,"Name")
                    Widget:
                        size_hint_x: 1
                MDBoxLayout:
                    Widget:
                        size_hint_x: 1
                    MDLabel:
                        text: "Gender"
                        size_hint_x: 9
                    MDIconButtonSpinner:
                        id: gender_input
                        size_hint_x: 2
                        icon: "close"
                        on_release:
                            root.open_gender_dropdown()
                    Widget:
                        size_hint_x: 2
                MDBoxLayout:
                    Widget:
                        size_hint_x: 1
                    MDLabel:
                        text: "Activity"
                        size_hint_x: 9
                    MDIconButtonSpinner:
                        id: activity_input
                        size_hint_x: 2
                        icon: "close"
                        on_release:
                            root.open_activity_dropdown()
                    Widget:
                        size_hint_x: 2
                MDBoxLayout:
                    Widget:
                        size_hint_x: 1
                    MDLabel:
                        text: "weight loss goal"
                        size_hint_x: 9
                    MDIconButtonSpinner:
                        id: weight_gain_input
                        size_hint_x: 2
                        icon: "close"
                        on_release:
                            root.open_weightgain_dropdown()
                    Widget:
                        size_hint_x: 2
                MDBoxLayout:
                    Widget:
                        size_hint_x: 1
                    MDLabel:
                        text: "Weight"
                        size_hint_x: 8
                    MDTextField:
                        id: weight_input
                        size_hint_x: 4
                        hint_text: "in kg"
                        input_filter: "float"
                        multiline: False
                        on_focus:
                            app.root.open_number_input_dialog(self,"Weight")
                        on_text:
                            root.display_BMR()
                            root.display_TDEE()
                            root.display_cals_per_day()
                            height_input.focus = True if not root.active_settings_id else False
                    Widget:
                        size_hint_x: 1
                MDBoxLayout:
                    Widget:
                        size_hint_x: 1
                    MDLabel:
                        text: "Height"
                        size_hint_x: 8
                    MDTextField:
                        id: height_input
                        size_hint_x: 4
                        hint_text: "in cm"
                        input_filter: "float"
                        multiline: False
                        on_focus:
                            app.root.open_number_input_dialog(self,"Height")
                        on_text:
                            root.display_BMR()
                            root.display_TDEE()
                            root.display_cals_per_day()
                            age_input.focus = True if not root.active_settings_id else False
                    Widget:
                        size_hint_x: 1
                MDBoxLayout:
                    Widget:
                        size_hint_x: 1
                    MDLabel:
                        text: "Age"
                        size_hint_x: 8
                    MDTextField:
                        id: age_input
                        size_hint_x: 4
                        input_filter: "float"
                        multiline: False
                        on_focus:
                            app.root.open_number_input_dialog(self,"Age")
                        on_text:
                            root.display_BMR()
                            root.display_TDEE()
                            root.display_cals_per_day()
                    Widget:
                        size_hint_x: 1
                MDBoxLayout:
                    Widget:
                        size_hint_x: 1
                    MDLabel:
                        text: "BMR"
                        size_hint_x: 9
                    MDLabel:
                        id: bmr
                        size_hint_x: 2
                    Widget:
                        size_hint_x: 2
                MDBoxLayout:
                    Widget:
                        size_hint_x: 1
                    MDLabel:
                        text: "TDEE"
                        size_hint_x: 9
                    MDLabel:
                        id: tdee
                        size_hint_x: 2
                    Widget:
                        size_hint_x: 2
                MDBoxLayout:
                    Widget:
                        size_hint_x: 1
                    MDLabel:
                        text: "Calorie Goal Per Day"
                        size_hint_x: 9
                    MDLabel:
                        id: calories_per_day
                        size_hint_x: 2
                    Widget:
                        size_hint_x: 2
        MDBoxLayout:
            pos_hint: {"center_x":.5}
            orientation: "vertical"
            size_hint: .5,1.5
            padding: dp(25)
            MDRaisedButton:
                pos_hint: {"center_x":.5}
                text: "Save Settings"
                on_release:
                    root.save_settings()
<Settings_Dialog>:
    settings_search_input: settings_search_input
    settings_search_result_list: settings_search_result_list
    orientation: "vertical"
    size_hint_y: None
    height: app.root.height *.6
    MDTextField:
        id: settings_search_input
        pos_hint: {"top":1}
        hint_text: "Name"
        on_text:
            root.display_search(self)
    ScrollView:
        MDList:
            id: settings_search_result_list

<Settings_Settings_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint: .5,None
    MDRaisedButton:
        text: "Delete Profile"
        size_hint: 1,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.delete()
    Widget:
        size_hint: 1,None
    MDRaisedButton:
        text: "Use Profile"
        size_hint: 1,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.use()
    Widget:
        size_hint: .5,None

<Delete_Settings_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint: 6,None
    MDFlatButton:
        text: "Cancel"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.cancel()
    Widget:
        size_hint: 1,None
    MDRaisedButton:
        text: "Delete"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.delete()
    Widget:
        size_hint: 1,None

<Settings_Already_Exist_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint: 6,None
    MDFlatButton:
        text: "Cancel"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.cancel()
    Widget:
        size_hint: 1,None
    MDRaisedButton:
        text: "Overwrite"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.overwrite()
    Widget:
        size_hint: 1,None

<Ingredients_Screen>:
    name: "Ingredients_Screen"
    search_icon: search_icon
    ing_search: ing_search
    filter: filter
    layout: layout
    ingredients_display_list: ingredients_display_list
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            pos_hint: {"top":1}
            title: "Ingredients"
            font_style: "H3"
            left_action_items: [["chevron-left", lambda x: root.transition_to_meal_plan_screen()]]
        MDBoxLayout:
            size_hint_y: None
            height: search_icon.height
            pos_hint: {"top":.9}
            MDIconButton:
                id: search_icon
                icon: "magnify"
                icon_size: dp(50)
            MDTextField:
                id: ing_search
                hint_text: "Name of Ingredient"
                on_text:
                    root.refresh_display_list()
            MDIconButtonSpinner:
                id: filter
                text: "All"
                icon: "filter-variant"
                theme_text_color: "Custom"
                text_color: (1,1,1,1)
                icon_size: dp(50)
                on_release:
                    root.open_filter_menu()
        MDBoxLayout:
            id: layout
            orientation: "vertical"
            size_hint_y: 1
            pos_hint: {"top":.95}
            MDBoxLayout:
                orientation: "vertical"
                ScrollView:
                    MDList:
                        id: ingredients_display_list
    MDBottomAppBar:
        MDTopAppBar:
            icon: "plus"
            type: "bottom"
            mode: "center"
            on_action_button: root.open_add_ingredients_dialog()
<Ingredient_List_Filter_Dialog>:
    size_hint_y: None
    height: app.root.height *.8
    sort_order_label: sort_order_label
    sorting_direction: sorting_direction
    sort_by_calories_label: sort_by_calories_label
    sort_by_fats_label: sort_by_fats_label
    sort_by_carbohydrates_label: sort_by_carbohydrates_label
    sort_by_proteins_label: sort_by_proteins_label
    ingredient_type_filter: ingredient_type_filter
    MDBoxLayout:
        orientation: "vertical"
        MDLabel:
            text: "Sort order"
            halign: "center"
            font_style: "H5"
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_order_label
                text: "High to Low"
                size_hint_x:4
            MDIconButton:
                id: sorting_direction
                icon: "sort-descending"
                size_hint_x:1
                pos_hint: {"center_y":.5}
                on_release:
                    root.set_sort_order()
            Widget:
                size_hint_x:1
        MDLabel:
            text: "Sort by"
            halign: "center"
            font_style: "H5"
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_calories_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Calories"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_calories
                size_hint_x:1
                on_active:
                    root.check_calories(*args)
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_fats_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Fats"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_fats
                size_hint_x:1
                on_active:
                    root.check_fats(*args)
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_carbohydrates_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Carbohydrates"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_carbohydrates
                size_hint_x:1
                on_active:
                    root.check_carbohydrates(*args)
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_proteins_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Proteins"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_proteins
                size_hint_x:1
                on_active:
                    root.check_proteins(*args)
            Widget:
                size_hint_x:1
        MDLabel:
            text: "Filter by"
            halign: "center"
            font_style: "H5"
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                text: "Type"
                size_hint_x:4
            MDIconButton:
                id: ingredient_type_filter
                icon: "filter-variant"
                theme_text_color: "Custom"
                size_hint_x:1
                on_release:
                    root.open_filter_dropdown()
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x: 1
            MDFlatButton:
                text: "Cancel"
                size_hint: 2,.5
                on_release:
                    root.cancel()
            Widget:
                size_hint_x: 2
            MDRaisedButton:
                text: "Apply"
                size_hint: 2,.5
                on_release:
                    root.apply_filter()
            Widget:
                size_hint_x: 1
<Add_Ingredient_Dialog>:
    size_hint_y: None
    height: app.root.height *.8
    orientation: "vertical"
    add_ing_button: add_ing_button
    add_ing_name: add_ing_name
    add_ing_unit: add_ing_unit
    add_ing_type: add_ing_type
    add_ing_calories: add_ing_calories
    add_ing_fats: add_ing_fats
    add_ing_carbohydrates: add_ing_carbohydrates
    add_ing_proteins: add_ing_proteins
    add_ing_divisibility: add_ing_divisibility
    divisibility_label: divisibility_label
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Name"
            size_hint_x: 4
        MDTextField:
            id: add_ing_name
            size_hint_x: 2
            on_focus:
                app.root.open_text_input_dialog(self,"Name")
            on_text:
                root.open_unit_dropdown() if not self.focus else None
                root.add_button_check_validity()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Unit"
            size_hint_x:5
        MDIconButtonSpinner:
            id: add_ing_unit
            icon: "close"
            icon_size: dp(50)
            pos_hint: {"center_y":.5}
            on_release:
                root.open_unit_dropdown()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Type"
            size_hint_x:5
        MDIconButtonSpinner:
            id: add_ing_type
            icon: "close"
            icon_size: dp(50)
            pos_hint: {"center_y":.5}
            on_release:
                root.open_type_dropdown()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Calories"
            size_hint_x:4
        MDTextField:
            id: add_ing_calories
            size_hint_x:2
            hint_text: "per 100 grams" if add_ing_unit.icon == "weight-gram" else "per 100 mls" if add_ing_unit.icon == "cup" else "per piece" if add_ing_unit.icon == "puzzle-outline" else ""
            input_filter: "float"
            on_focus:
                app.root.open_number_input_dialog(self,"Calories")
            on_text:
                add_ing_fats.focus = True if not self.focus else False
                root.add_button_check_validity()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Fats"
            size_hint_x:4
        MDTextField:
            id: add_ing_fats
            size_hint_x:2
            hint_text: "per 100 grams" if add_ing_unit.icon == "weight-gram" else "per 100 mls" if add_ing_unit.icon == "cup" else "per piece" if add_ing_unit.icon == "puzzle-outline" else ""
            input_filter: "float"
            on_focus:
                app.root.open_number_input_dialog(self,"Fats")
            on_text:
                add_ing_carbohydrates.focus = True if not self.focus else False
                root.add_button_check_validity()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Carbohydrates"
            size_hint_x:4
        MDTextField:
            id: add_ing_carbohydrates
            size_hint_x:2
            hint_text: "per 100 grams" if add_ing_unit.icon == "weight-gram" else "per 100 mls" if add_ing_unit.icon == "cup" else "per piece" if add_ing_unit.icon == "puzzle-outline" else ""
            input_filter: "float"
            on_focus:
                app.root.open_number_input_dialog(self,"Carbohydrates")
            on_text:
                add_ing_proteins.focus = True if not self.focus else False
                root.add_button_check_validity()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Proteins"
            size_hint_x:4
        MDTextField:
            id: add_ing_proteins
            size_hint_x:2
            hint_text: "per 100 grams" if add_ing_unit.icon == "weight-gram" else "per 100 mls" if add_ing_unit.icon == "cup" else "per piece" if add_ing_unit.icon == "puzzle-outline" else ""
            input_filter: "float"
            on_focus:
                app.root.open_number_input_dialog(self,"Proteins")
            on_text:
                root.open_divisibility_dropdown() if not self.focus and add_ing_unit.icon == "puzzle-outline" else None
                root.add_button_check_validity()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            id: divisibility_label
            text: "Divisibility"
            color: 1,1,1,.5
            size_hint_x:5
        MDIconButtonSpinner:
            id: add_ing_divisibility
            icon: "close"
            icon_size: dp(50)
            pos_hint: {"center_y":.5}
            disabled: True
            on_release:
                root.open_divisibility_dropdown()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDFlatButton:
            text: "Cancel"
            size_hint_y: .5
            size_hint_x: 2
            pos_hint: {"center_y":.5}
            on_release:
                root.cancel()
        Widget:
            size_hint_x: 2
        MDRaisedButton:
            id: add_ing_button
            disabled: True
            size_hint_y: .5
            size_hint_x: 2
            pos_hint: {"center_y":.5}
            text: "Add Ingredient"
            on_release:
                root.add_ingredient()
        Widget:
            size_hint_x: 1

<Ingredient_Already_Exists_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint: 6,None
    MDFlatButton:
        text: "Cancel"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.cancel()
    Widget:
        size_hint: 1,None
    MDRaisedButton:
        text: "Update"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.update()
    Widget:
        size_hint: 1,None

<Ingredient_Options_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint_x: 1
    MDRaisedButton:
        text: "Edit"
        size_hint_x: 2
        pos_hint: {"center_y":.5}
        on_release:
            root.edit()
    Widget:
        size_hint_x: 2
    MDRaisedButton:
        text: "Delete"
        size_hint_x: 2
        pos_hint: {"center_y":.5}
        on_release:
            root.open_delete_ingredient_dialog()
    Widget:
        size_hint_x: 1

<Delete_Ingredient_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint: 6,None
    MDFlatButton:
        text: "Cancel"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.cancel()
    Widget:
        size_hint: 1,None
    MDRaisedButton:
        text: "Delete"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.delete()
    Widget:
        size_hint: 1,None

<Edit_Ingredient_Dialog>:
    size_hint_y: None
    height: app.root.height *.8
    orientation: "vertical"
    update_ing_button: update_ing_button
    update_ing_name: update_ing_name
    update_ing_unit: update_ing_unit
    update_ing_type: update_ing_type
    update_ing_calories: update_ing_calories
    update_ing_fats: update_ing_fats
    update_ing_carbohydrates: update_ing_carbohydrates
    update_ing_proteins: update_ing_proteins
    divisibility_label: divisibility_label
    update_ing_divisibility: update_ing_divisibility
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Name"
            size_hint_x: 4
        MDTextField:
            id: update_ing_name
            size_hint_x: 2
            on_text:
                root.ing_name_check_validity()
                root.update_button_check_validity()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Unit"
            size_hint_x:5
        MDIconButtonSpinner:
            id: update_ing_unit
            icon: "close"
            icon_size: dp(50)
            on_release:
                root.open_unit_dropdown()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Type"
            size_hint_x:5
        MDIconButtonSpinner:
            id: update_ing_type
            icon: "close"
            icon_size: dp(50)
            on_release:
                root.open_type_dropdown()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Calories"
            size_hint_x:4
        MDTextField:
            id: update_ing_calories
            size_hint_x:2
            hint_text: "per 100 grams" if update_ing_unit.icon == "weight-gram" else "per 100 mls" if update_ing_unit.icon == "cup" else "per piece" if update_ing_unit.icon == "puzzle-outline" else ""
            input_filter: "float"
            on_focus:
                app.root.open_number_input_dialog(self,"Calories")
            on_text:
                root.update_button_check_validity()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Fats"
            size_hint_x:4
        MDTextField:
            id: update_ing_fats
            size_hint_x:2
            hint_text: "per 100 grams" if update_ing_unit.icon == "weight-gram" else "per 100 mls" if update_ing_unit.icon == "cup" else "per piece" if update_ing_unit.icon == "puzzle-outline" else ""
            input_filter: "float"
            on_focus:
                app.root.open_number_input_dialog(self,"Fats")
            on_text:
                root.update_button_check_validity()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Carbohydrates"
            size_hint_x:4
        MDTextField:
            id: update_ing_carbohydrates
            size_hint_x:2
            hint_text: "per 100 grams" if update_ing_unit.icon == "weight-gram" else "per 100 mls" if update_ing_unit.icon == "cup" else "per piece" if update_ing_unit.icon == "puzzle-outline" else ""
            input_filter: "float"
            on_focus:
                app.root.open_number_input_dialog(self,"Carbohydrates")
            on_text:
                root.update_button_check_validity()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            text: "Proteins"
            size_hint_x:4
        MDTextField:
            id: update_ing_proteins
            size_hint_x:2
            hint_text: "per 100 grams" if update_ing_unit.icon == "weight-gram" else "per 100 mls" if update_ing_unit.icon == "cup" else "per piece" if update_ing_unit.icon == "puzzle-outline" else ""
            input_filter: "float"
            on_focus:
                app.root.open_number_input_dialog(self,"Proteins")
            on_text:
                root.update_button_check_validity()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDLabel:
            id: divisibility_label
            text: "Divisibility"
            size_hint_x:5
        MDIconButtonSpinner:
            id: update_ing_divisibility
            icon: "close"
            icon_size: dp(50)
            on_release:
                root.open_divisibility_dropdown()
        Widget:
            size_hint_x: 1
    MDBoxLayout:
        size_hint_y: 1
        Widget:
            size_hint_x: 1
        MDFlatButton:
            text: "Cancel"
            size_hint_y: .5
            size_hint_x: 2
            pos_hint: {"center_y":.5}
            on_release:
                root.cancel()
        Widget:
            size_hint_x: 2
        MDRaisedButton:
            id: update_ing_button
            disabled: False
            size_hint_y: .5
            size_hint_x: 2
            pos_hint: {"center_y":.5}
            text: "Update"
            on_release:
                root.update_ingredient()
        Widget:
            size_hint_x: 1

<Meals_Screen>:
    name: "Meals_Screen"
    search_icon: search_icon
    meal_search: meal_search
    filter: filter
    layout: layout
    meals_display_list: meals_display_list
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            pos_hint: {"top":1}
            title: "Meals"
            font_style: "H3"
            left_action_items: [["chevron-left", lambda x: root.transition_to_meal_plan_screen()]]
        MDBoxLayout:
            size_hint_y: None
            height: search_icon.height
            pos_hint: {"top":.9}
            MDIconButton:
                id: search_icon
                icon: "magnify"
                icon_size: dp(50)
            MDTextField:
                id: meal_search
                hint_text: "Name of Meals"
                on_text:
                    root.refresh_display_list()
            MDIconButtonSpinner:
                id: filter
                text: "All"
                icon: "filter-variant"
                icon_size: dp(50)
                on_release:
                    root.open_filter_dialog()
        MDBoxLayout:
            id: layout
            orientation: "vertical"
            size_hint_y:1
            pos_hint: {"top":.95}
            MDBoxLayout:
                orientation: "vertical"
                ScrollView:
                    MDList:
                        id: meals_display_list
    MDBottomAppBar:
        MDTopAppBar:
            icon: "plus"
            type: "bottom"
            mode: "center"
            on_action_button: root.open_add_meal_dialog()


<Filter_Dialog>:
    size_hint_y: None
    height: app.root.height *.8
    orientation: "vertical"
    breakfast: breakfast
    lunch: lunch
    dinner: dinner
    snack: snack
    ignore_hot_cold:ignore_hot_cold
    label_hot: label_hot
    hot_cold: hot_cold
    label_cold: label_cold
    ignore_sweet_savory: ignore_sweet_savory
    label_sweet: label_sweet
    sweet_savory: sweet_savory
    label_savory: label_savory
    apply_filter_button: apply_filter_button
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "breakfast"
            size_hint_x:2
        Widget:
            size_hint_x:1.2
        MDCheckbox:
            id: breakfast
            size_hint_x:.8
            on_active:
                root.check_apply_filter_button_validity()
        Widget:
            size_hint_x:1
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "lunch"
            size_hint_x:2
        Widget:
            size_hint_x:1.2
        MDCheckbox:
            id: lunch
            size_hint_x:.8
            on_active:
                root.check_apply_filter_button_validity()
        Widget:
            size_hint_x:1
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "dinner"
            size_hint_x:2
        Widget:
            size_hint_x:1.2
        MDCheckbox:
            id: dinner
            size_hint_x:.8
            on_active:
                root.check_apply_filter_button_validity()
        Widget:
            size_hint_x:1
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "snack"
            size_hint_x:2
        Widget:
            size_hint_x:1.2
        MDCheckbox:
            id: snack
            size_hint_x:.8
            on_active:
                root.check_apply_filter_button_validity()
        Widget:
            size_hint_x:1
    MDCheckbox:
        id: ignore_hot_cold
        size_hint_x:1
        on_active:
            root.activate_deactivate_hot_cold_filter(self.state)
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_y:1
        MDLabel:
            id: label_hot
            text: "hot"
            theme_text_color: "Custom"
            text_color: 1,1,1,.25
            size_hint_x:1.75
        MDSwitch:
            id: hot_cold
            size_hint_x:.75
            pos_hint: {"center_y":.5}
            disabled: True
        MDLabel:
            id: label_cold
            text: "cold"
            theme_text_color: "Custom"
            text_color: 1,1,1,.25
            halign: "right"
            size_hint_x:1.75
        Widget:
            size_hint_x:1
    MDCheckbox:
        id: ignore_sweet_savory
        size_hint_x:1
        on_active:
            root.activate_deactivate_sweet_savory_filter(self.state)
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_y:.5
        MDLabel:
            id: label_sweet
            text: "sweet"
            theme_text_color: "Custom"
            text_color: 1,1,1,.25
            size_hint_x:1.75
        MDSwitch:
            id: sweet_savory
            size_hint_x:.75
            pos_hint: {"center_y":.5}
            disabled: True
        MDLabel:
            id: label_savory
            text: "savory"
            theme_text_color: "Custom"
            text_color: 1,1,1,.25
            halign: "right"
            size_hint_x:1.75
        Widget:
            size_hint_x:1
    Widget:
        size_hint_y:1
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDFlatButton:
            text: "Cancel"
            size_hint_y:.5
            size_hint_x:2
            pos_hint: {"center_y":.5}
            on_release:
                root.cancel()
        Widget:
            size_hint_x:1
        MDRectangleFlatButton:
            text: "show all"
            size_hint_x:2
            size_hint_y:.5
            pos_hint: {"center_y":.5}
            on_release:
                root.reset_filter()
        Widget:
            size_hint_x:1
        MDRaisedButton:
            id: apply_filter_button
            disabled: True
            size_hint_y:.5
            size_hint_x:2
            pos_hint: {"center_y":.5}
            text: "Apply filter"
            on_release:
                root.apply_filter()
        Widget:
            size_hint_x:1

<Add_Meal_Dialog>:
    size_hint_y: None
    height: app.root.height *.8
    orientation: "vertical"
    meal_name: meal_name
    breakfast: breakfast
    lunch: lunch
    dinner: dinner
    snack: snack
    label_hot: label_hot
    hot_cold: hot_cold
    label_cold: label_cold
    label_sweet: label_sweet
    sweet_savory: sweet_savory
    label_savory: label_savory
    add_meal_button: add_meal_button
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "Name"
            size_hint_x:2
        MDTextField:
            id: meal_name
            hint_text: "Name"
            size_hint_x:2
        Widget:
            size_hint_x:1
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "breakfast"
            size_hint_x:2
        Widget:
            size_hint_x:1.2
        MDCheckbox:
            id: breakfast
            size_hint_x:.8
            on_active:
                root.check_add_meal_button_validity()
        Widget:
            size_hint_x:1
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "lunch"
            size_hint_x:2
        Widget:
            size_hint_x:1.2
        MDCheckbox:
            id: lunch
            size_hint_x:.8
            on_active:
                root.check_add_meal_button_validity()
        Widget:
            size_hint_x:1
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "dinner"
            size_hint_x:2
        Widget:
            size_hint_x:1.2
        MDCheckbox:
            id: dinner
            size_hint_x:.8
            on_active:
                root.check_add_meal_button_validity()
        Widget:
            size_hint_x:1
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:1
        MDLabel:
            text: "snack"
            size_hint_x:2
        Widget:
            size_hint_x:1.2
        MDCheckbox:
            id: snack
            size_hint_x:.8
            on_active:
                root.check_add_meal_button_validity()
        Widget:
            size_hint_x:1
    Widget:
        size_hint_x:1
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_y:1
        MDLabel:
            id: label_hot
            text: "hot"
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            size_hint_x:1.75
        MDSwitch:
            id: hot_cold
            size_hint_x:.75
            pos_hint: {"center_y":.5}
        MDLabel:
            id: label_cold
            text: "cold"
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            halign: "right"
            size_hint_x:1.75
        Widget:
            size_hint_x:1
    Widget:
        size_hint_x:1
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_y:.5
        MDLabel:
            id: label_sweet
            text: "sweet"
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            size_hint_x:1.75
        MDSwitch:
            id: sweet_savory
            size_hint_x:.75
            pos_hint: {"center_y":.5}
        MDLabel:
            id: label_savory
            text: "savory"
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            halign: "right"
            size_hint_x:1.75
        Widget:
            size_hint_x:1
    Widget:
        size_hint_y:1
    MDBoxLayout:
        size_hint_y:1
        Widget:
            size_hint_x:.5
        MDFlatButton:
            text: "Cancel"
            size_hint_y:.5
            size_hint_x:2
            pos_hint: {"center_y":.5}
            on_release:
                root.cancel()
        Widget:
            size_hint_x:1
        MDRaisedButton:
            id: add_meal_button
            disabled: True
            size_hint_y:.5
            size_hint_x:2
            pos_hint: {"center_y":.5}
            text: "Add meal"
            on_release:
                root.add_meal()
        Widget:
            size_hint_x:.5

<Meal_Already_Exists_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint: 6,None
    MDFlatButton:
        text: "Cancel"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.cancel()
    Widget:
        size_hint: 1,None
    MDRaisedButton:
        text: "Update"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.update()
    Widget:
        size_hint: 1,None

<Meal_Options_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint_x: 1
    MDRaisedButton:
        text: "Edit"
        size_hint_x: 2
        pos_hint: {"center_y":.5}
        on_release:
            root.edit()
    Widget:
        size_hint_x: 2
    MDRaisedButton:
        text: "Delete"
        size_hint_x: 2
        pos_hint: {"center_y":.5}
        on_release:
            root.open_delete_meal_dialog()
    Widget:
        size_hint_x: 1

<Delete_Meal_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint: 6,None
    MDFlatButton:
        text: "Cancel"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.cancel()
    Widget:
        size_hint: 1,None
    MDRaisedButton:
        text: "Delete"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.delete()
    Widget:
        size_hint: 1,None

<Display_Meal_Screen>:
    name: "Display_Meal_Screen"
    top_app_bar: top_app_bar
    meal_ingredient_list: meal_ingredient_list
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            id: top_app_bar
            pos_hint: {"top":1}
            title: "Meals"
            font_style: "H3"
            left_action_items: [["chevron-left", lambda x: root.transition_to_meal_plan_screen()]]
        # MDBoxLayout:
            # size_hint_y:None
            # height: meal_name.height
            # pos_hint: {"top":1}
            # MDIconButton:
            #     id: back_button
            #     icon: "chevron-left"
            #     pos_hint: {"center_y":.5}
            #     icon_size: dp(50)
            #     on_release:
            #         root.remove_display_screen()
            #         app.root.ids.meals_screen.refresh_internal_list()
            #         app.root.ids.meals_screen.refresh_display_list()
            #         app.root.ids.screen_manager.current = "Meals_Screen"
            #         app.root.ids.screen_manager.transition.direction = "right"
            # Widget:
            #     size_hint_x:.1
            # MDLabel:
            #     id: meal_name
            #     size_hint_x: 1
            #     text: "Place_holder"
            #     font_style: "H4"
            # Widget:
            #     size_hint_x:.1
        ScrollView:
            MDList:
                id: meal_ingredient_list

<Meal_Ingredient_Options_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint_x: 1
    MDRaisedButton:
        text: "Change amount"
        size_hint_x: 2
        pos_hint: {"center_y":.5}
        on_release:
            root.open_change_amount_dialog()
    Widget:
        size_hint_x: 2
    MDRaisedButton:
        text: "Delete"
        size_hint_x: 2
        pos_hint: {"center_y":.5}
        on_release:
            root.open_delete_ingredient_dialog()
    Widget:
        size_hint_x: 1
<Ingredient_Is_Already_In_Meal_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint: 4,None
    MDFlatButton:
        text: "Cancel"
        size_hint: 2,.5
        pos_hint: {"center_y":.5}
        on_release:
            root.cancel()
    Widget:
        size_hint: 1,None
    MDRaisedButton:
        text: "Change amount"
        size_hint: 2,.5
        pos_hint: {"center_y":.5}
        on_release:
            root.change_amount()
    Widget:
        size_hint: 1,None

<Delete_Meal_Ingredient_Dialog>:
    size_hint_y: None
    height: app.root.height *.1
    Widget:
        size_hint: 6,None
    MDFlatButton:
        text: "Cancel"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.cancel()
    Widget:
        size_hint: 1,None
    MDRaisedButton:
        text: "Delete"
        size_hint: 2,.5
        pos_hint: {"center_y":.4}
        on_release:
            root.delete()
    Widget:
        size_hint: 1,None

<Add_Meal_Ingredient_Dialog>:
    size_hint_y: None
    height: app.root.height *.8
    search_icon: search_icon
    ing_search: ing_search
    filter: filter
    layout: layout
    ingredients_display_list: ingredients_display_list
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            size_hint_y: None
            height: search_icon.height
            MDIconButton:
                id: search_icon
                icon: "magnify"
                icon_size: dp(50)
            MDTextField:
                id: ing_search
                hint_text: "Name of Ingredient"
                on_text:
                    root.refresh_display_list()
            MDIconButtonSpinner:
                id: filter
                text: "All"
                icon: "filter-variant"
                theme_text_color: "Custom"
                text_color: (1,1,1,1)
                icon_size: dp(50)
                on_release:
                    root.open_filter_menu()
        MDBoxLayout:
            id: layout
            orientation: "vertical"
            size_hint_y: 6.5
            ScrollView:
                MDList:
                    id: ingredients_display_list
        MDBoxLayout:
            size_hint_y: 1
            Widget:
                size_hint_x:1
            MDFlatButton:
                text: "Cancel"
                size_hint_x:1
                pos_hint: {"center_x":.5}
                on_release:
                    root.cancel()
            Widget:
                size_hint_x:1
<Ingredient_List_Filter_For_Add_Ing_To_Meal_Dialog>:
    size_hint_y: None
    height: app.root.height *.8
    sort_order_label: sort_order_label
    sorting_direction: sorting_direction
    sort_by_calories_label: sort_by_calories_label
    sort_by_fats_label: sort_by_fats_label
    sort_by_carbohydrates_label: sort_by_carbohydrates_label
    sort_by_proteins_label: sort_by_proteins_label
    ingredient_type_filter: ingredient_type_filter
    MDBoxLayout:
        orientation: "vertical"
        MDLabel:
            text: "Sort order"
            halign: "center"
            font_style: "H5"
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_order_label
                text: "High to Low"
                size_hint_x:4
            MDIconButton:
                id: sorting_direction
                icon: "sort-descending"
                size_hint_x:1
                pos_hint: {"center_y":.5}
                on_release:
                    root.set_sort_order()
            Widget:
                size_hint_x:1
        MDLabel:
            text: "Sort by"
            halign: "center"
            font_style: "H5"
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_calories_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Calories"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_calories
                size_hint_x:1
                on_active:
                    root.check_calories(*args)
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_fats_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Fats"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_fats
                size_hint_x:1
                on_active:
                    root.check_fats(*args)
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_carbohydrates_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Carbohydrates"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_carbohydrates
                size_hint_x:1
                on_active:
                    root.check_carbohydrates(*args)
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_proteins_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Proteins"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_proteins
                size_hint_x:1
                on_active:
                    root.check_proteins(*args)
            Widget:
                size_hint_x:1
        MDLabel:
            text: "Filter by"
            halign: "center"
            font_style: "H5"
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                text: "Type"
                size_hint_x:4
            MDIconButton:
                id: ingredient_type_filter
                icon: "filter-variant"
                theme_text_color: "Custom"
                size_hint_x:1
                on_release:
                    root.open_filter_dropdown()
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x: 1
            MDFlatButton:
                text: "Cancel"
                size_hint: 2,.5
                on_release:
                    root.cancel()
            Widget:
                size_hint_x: 2
            MDRaisedButton:
                text: "Apply"
                size_hint: 2,.5
                on_release:
                    root.apply_filter()
            Widget:
                size_hint_x: 1
<Add_Ing_To_Meal_Unit_Piece_Divisible_Dialog>:
    size_hint_y: None
    height: app.root.height *.8
    pieces_label: pieces_label
    pieces_amount_label: pieces_amount_label
    slices_label: slices_label
    slices_amount_label: slices_amount_label
    ing_stats_label: ing_stats_label
    meal_stats_label: meal_stats_label
    ing_calories: ing_calories
    ing_fats: ing_fats
    ing_carbohydrates: ing_carbohydrates
    ing_proteins: ing_proteins
    meal_calories: meal_calories
    meal_fats: meal_fats
    meal_carbohydrates: meal_carbohydrates
    meal_proteins: meal_proteins
    confirm_button: confirm_button
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            size_hint_y:1
            MDLabel:
                id: pieces_label
                text: "Pieces"
                halign: "center"
            MDIconButton:
                icon: "minus"
                icon_size: dp(50)
                pos_hint: {"center_y":.5}
                on_release:
                    root.decrement_pieces()
                    root.refresh_stats()
            MDLabelNumber:
                id: pieces_amount_label
                halign: "center"
            MDIconButton:
                icon: "plus"
                icon_size: dp(50)
                pos_hint: {"center_y":.5}
                on_release:
                    root.increment_pieces()
                    root.refresh_stats()
        MDBoxLayout:
            size_hint_y:1
            MDLabel:
                id: slices_label
                text: "Slices"
                halign: "center"
            MDIconButton:
                icon: "minus"
                icon_size: dp(50)
                pos_hint: {"center_y":.5}
                on_release:
                    root.decrement_slices()
                    root.refresh_stats()
            MDLabelFraction:
                id: slices_amount_label
                halign: "center"
            MDIconButton:
                icon: "plus"
                icon_size: dp(50)
                pos_hint: {"center_y":.5}
                on_release:
                    root.increment_slices()
                    root.refresh_stats()
        MDBoxLayout:
            size_hint_y:.5
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Stats for"
                    font_style: "H6"
                    halign: "center"
                MDLabel:
                    id: ing_stats_label
                    text: ""
                    font_style: "Subtitle2"
                    halign: "center"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Stats for"
                    font_style: "H6"
                    halign: "center"
                MDLabel:
                    id: meal_stats_label
                    text: ""
                    font_style: "Subtitle2"
                    halign: "center"
        MDBoxLayout:
            size_hint_y:3
            MDBoxLayout:
                orientation: "vertical"
                MDLabelNumber:
                    id: ing_calories
                    halign: "center"
                MDLabelNumber:
                    id: ing_fats
                    halign: "center"
                MDLabelNumber:
                    id: ing_carbohydrates
                    halign: "center"
                MDLabelNumber:
                    id: ing_proteins
                    halign: "center"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "kcals"
                    halign: "center"
                MDLabel:
                    text: "fats"
                    halign: "center"
                MDLabel:
                    text: "carbohydrates"
                    halign: "center"
                MDLabel:
                    text: "proteins"
                    halign: "center"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    id: meal_calories
                    halign: "center"
                MDLabel:
                    id: meal_fats
                    halign: "center"
                MDLabel:
                    id: meal_carbohydrates
                    halign: "center"
                MDLabel:
                    id: meal_proteins
                    halign: "center"
        MDBoxLayout:
            size_hint_y:1
            Widget:
                size_hint: 1,None
            MDFlatButton:
                text: "Cancel"
                size_hint: 2,.25
                pos_hint: {"center_y":.5}
                on_release:
                    root.cancel()
            Widget:
                size_hint: 1,None
            MDRaisedButton:
                id: confirm_button
                text: "Confirm"
                size_hint: 2,.25
                pos_hint: {"center_y":.5}
                on_release:
                    root.add_to_meal()
            Widget:
                size_hint: 1,None

<Add_Ing_To_Meal_Unit_Piece_Indivisible_Dialog>:
    size_hint_y: None
    height: app.root.height *.8
    pieces_label: pieces_label
    pieces_amount_label: pieces_amount_label
    ing_stats_label: ing_stats_label
    meal_stats_label: meal_stats_label
    ing_calories: ing_calories
    ing_fats: ing_fats
    ing_carbohydrates: ing_carbohydrates
    ing_proteins: ing_proteins
    meal_calories: meal_calories
    meal_fats: meal_fats
    meal_carbohydrates: meal_carbohydrates
    meal_proteins: meal_proteins
    confirm_button: confirm_button
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            size_hint_y:1
            MDLabel:
                id: pieces_label
                text: "Pieces"
                halign: "center"
            MDIconButton:
                icon: "minus"
                icon_size: dp(50)
                pos_hint: {"center_y":.5}
                on_release:
                    root.decrement_pieces()
                    root.refresh_stats()
            MDLabelNumber:
                id: pieces_amount_label
                halign: "center"
            MDIconButton:
                icon: "plus"
                icon_size: dp(50)
                pos_hint: {"center_y":.5}
                on_release:
                    root.increment_pieces()
                    root.refresh_stats()
        MDBoxLayout:
            size_hint_y:.5
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Stats for"
                    font_style: "H6"
                    halign: "center"
                MDLabel:
                    id: ing_stats_label
                    text: ""
                    font_style: "Subtitle2"
                    halign: "center"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Stats for"
                    font_style: "H6"
                    halign: "center"
                MDLabel:
                    id: meal_stats_label
                    text: ""
                    font_style: "Subtitle2"
                    halign: "center"
        MDBoxLayout:
            size_hint_y:3
            MDBoxLayout:
                orientation: "vertical"
                MDLabelNumber:
                    id: ing_calories
                    halign: "center"
                MDLabelNumber:
                    id: ing_fats
                    halign: "center"
                MDLabelNumber:
                    id: ing_carbohydrates
                    halign: "center"
                MDLabelNumber:
                    id: ing_proteins
                    halign: "center"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "kcals"
                    halign: "center"
                MDLabel:
                    text: "fats"
                    halign: "center"
                MDLabel:
                    text: "carbohydrates"
                    halign: "center"
                MDLabel:
                    text: "proteins"
                    halign: "center"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    id: meal_calories
                    halign: "center"
                MDLabel:
                    id: meal_fats
                    halign: "center"
                MDLabel:
                    id: meal_carbohydrates
                    halign: "center"
                MDLabel:
                    id: meal_proteins
                    halign: "center"
        MDBoxLayout:
            size_hint_y:1
            Widget:
                size_hint: 1,None
            MDFlatButton:
                text: "Cancel"
                size_hint: 2,.25
                pos_hint: {"center_y":.5}
                on_release:
                    root.cancel()
            Widget:
                size_hint: 1,None
            MDRaisedButton:
                id: confirm_button
                text: "Confirm"
                size_hint: 2,.25
                pos_hint: {"center_y":.5}
                disabled: True
                on_release:
                    root.add_to_meal()
            Widget:
                size_hint: 1,None

<Add_Ing_To_Meal_Unit_Gram_Ml_Dialog>:
    size_hint_y: None
    height: app.root.height *.8
    decrement_amount_button: decrement_amount_button
    unit_label: unit_label
    amount_input: amount_input
    ing_stats_label: ing_stats_label
    meal_stats_label: meal_stats_label
    ing_calories: ing_calories
    ing_fats: ing_fats
    ing_carbohydrates: ing_carbohydrates
    ing_proteins: ing_proteins
    meal_calories: meal_calories
    meal_fats: meal_fats
    meal_carbohydrates: meal_carbohydrates
    meal_proteins: meal_proteins
    confirm_button: confirm_button
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            size_hint_y:1
            Widget:
                size_hint_x:1
            MDIconButton:
                id: decrement_amount_button
                icon: "minus"
                pos_hint: {"center_y":.5}
                on_release:
                    root.decrement_amount()
            MDTextField:
                id: amount_input
                hint_text: "enter amount"
                input_filter: "int"
                pos_hint: {"center_y":.5}
                size_hint_x:4
                on_text:
                    root.refresh_stats()
                    root.confirm_button_check_validity()
                    root.decrement_amount_button_check_validity()
            MDIconButton:
                icon: "plus"
                pos_hint: {"center_y":.5}
                on_release:
                    root.increment_amount()
            Widget:
                size_hint_x:1
            MDLabel:
                id: unit_label
                text: "unit"
                size_hint_x:3
        MDBoxLayout:
            size_hint_y:.5
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Stats for"
                    font_style: "H6"
                    halign: "center"
                MDLabel:
                    id: ing_stats_label
                    text: ""
                    font_style: "Subtitle2"
                    halign: "center"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Stats for"
                    font_style: "H6"
                    halign: "center"
                MDLabel:
                    id: meal_stats_label
                    text: ""
                    font_style: "Subtitle2"
                    halign: "center"
        MDBoxLayout:
            size_hint_y:3
            MDBoxLayout:
                orientation: "vertical"
                MDLabelNumber:
                    id: ing_calories
                    halign: "center"
                MDLabelNumber:
                    id: ing_fats
                    halign: "center"
                MDLabelNumber:
                    id: ing_carbohydrates
                    halign: "center"
                MDLabelNumber:
                    id: ing_proteins
                    halign: "center"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Calories"
                    halign: "center"
                MDLabel:
                    text: "Fats"
                    halign: "center"
                MDLabel:
                    text: "Carbohydrates"
                    halign: "center"
                MDLabel:
                    text: "Proteins"
                    halign: "center"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    id: meal_calories
                    halign: "center"
                MDLabel:
                    id: meal_fats
                    halign: "center"
                MDLabel:
                    id: meal_carbohydrates
                    halign: "center"
                MDLabel:
                    id: meal_proteins
                    halign: "center"
        MDBoxLayout:
            size_hint_y:1
            Widget:
                size_hint: 1,None
            MDFlatButton:
                text: "Cancel"
                size_hint: 2,.25
                pos_hint: {"center_y":.5}
                on_release:
                    root.cancel()
            Widget:
                size_hint: 1,None
            MDRaisedButton:
                id: confirm_button
                text: "Confirm"
                size_hint: 2,.25
                pos_hint: {"center_y":.5}
                disabled: True
                on_release:
                    root.add_to_meal()
            Widget:
                size_hint: 1,None

<Shopping_List_Screen>:
    name: "Shopping_List_Screen"
    search_icon: search_icon
    ing_search: ing_search
    filter: filter
    shopping_list_list: shopping_list_list
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            pos_hint: {"top":1}
            title: "Shopping list"
            font_style: "H3"
            left_action_items: [["chevron-left",lambda x: root.transition_to_meal_plan_screen()]]
        MDBoxLayout:
            size_hint_y: None
            height: search_icon.height
            pos_hint: {"top":.9}
            MDIconButton:
                id: search_icon
                icon: "magnify"
                icon_size: dp(50)
            MDTextField:
                id: ing_search
                hint_text: "Name of Ingredient"
                on_text:
                    root.display_shopping_list()
            MDIconButtonSpinner:
                id: filter
                text: "All"
                icon: "filter-variant"
                theme_text_color: "Custom"
                text_color: (1,1,1,1)
                icon_size: dp(50)
                on_release:
                    root.open_filter_menu()
        ScrollView:
            MDList:
                id: shopping_list_list

<Shopping_List_Filter_Dialog>:
    size_hint_y: None
    height: app.root.height *.8
    sort_order_label: sort_order_label
    sorting_direction: sorting_direction
    sort_by_amount_label: sort_by_amount_label
    sort_by_calories_label: sort_by_calories_label
    sort_by_fats_label: sort_by_fats_label
    sort_by_carbohydrates_label: sort_by_carbohydrates_label
    sort_by_proteins_label: sort_by_proteins_label
    ingredient_type_filter: ingredient_type_filter
    exclude_checked_items: exclude_checked_items
    MDBoxLayout:
        orientation: "vertical"
        MDLabel:
            text: "Sort order"
            halign: "center"
            font_style: "H5"
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_order_label
                text: "High to Low"
                size_hint_x:4
            MDIconButton:
                id: sorting_direction
                icon: "sort-descending"
                size_hint_x:1
                pos_hint: {"center_y":.5}
                on_release:
                    root.set_sort_order()
            Widget:
                size_hint_x:1
        MDLabel:
            text: "Sort by"
            halign: "center"
            font_style: "H5"
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_amount_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Amount"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_amount
                size_hint_x:1
                on_active:
                    root.check_amount(*args)
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_calories_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Calories"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_calories
                size_hint_x:1
                on_active:
                    root.check_calories(*args)
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_fats_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Fats"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_fats
                size_hint_x:1
                on_active:
                    root.check_fats(*args)
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_carbohydrates_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Carbohydrates"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_carbohydrates
                size_hint_x:1
                on_active:
                    root.check_carbohydrates(*args)
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                id: sort_by_proteins_label
                theme_text_color: "Custom"
                text_color: 1,1,1,.25
                text: "Proteins"
                size_hint_x:4
            MDCheckbox:
                id: sort_by_proteins
                size_hint_x:1
                on_active:
                    root.check_proteins(*args)
            Widget:
                size_hint_x:1
        MDLabel:
            text: "Filter by"
            halign: "center"
            font_style: "H5"
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                text: "Type"
                size_hint_x:4
            MDIconButton:
                id: ingredient_type_filter
                icon: "filter-variant"
                theme_text_color: "Custom"
                size_hint_x:1
                on_release:
                    root.open_filter_dropdown()
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x:1
            MDLabel:
                text: "Exclude checked Items"
                size_hint_x:4
            MDCheckbox:
                id: exclude_checked_items
                size_hint_x:1
                on_active:
                    root.check_checked_items(*args)
            Widget:
                size_hint_x:1
        MDBoxLayout:
            Widget:
                size_hint_x: 1
            MDFlatButton:
                text: "Cancel"
                size_hint: 2,.5
                on_release:
                    root.cancel()
            Widget:
                size_hint_x: 2
            MDRaisedButton:
                text: "Apply"
                size_hint: 2,.5
                on_release:
                    root.apply_filter()
            Widget:
                size_hint_x: 1
<Text_Input_Dialog>:
    size_hint_y: None
    height: text_input.height
    text_input: text_input
    MDTextField:
        size_hint_x:9
        id: text_input
        on_text_validate:
            root.apply(self)
    MDIconButton:
        icon: "close"
        pos_hint: {"center_y":.5}
        size_hint_x:1
        on_release:
            text_input.text = ""
            text_input.focus = True
<Number_Input_Dialog>:
    size_hint_y: None
    height: number_input.height
    number_input: number_input
    MDTextField:
        size_hint_x:9
        id: number_input
        input_type: "number"
        on_text_validate:
            root.apply(self)
    MDIconButton:
        icon: "close"
        pos_hint: {"center_y":.5}
        size_hint_x:1
        on_release:
            number_input.text = ""
            number_input.focus = True

