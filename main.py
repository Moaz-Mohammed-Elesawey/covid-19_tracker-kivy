from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior


from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem

from kivy_garden.mapview import MapView
from kivy_garden.graph import LinePlot

from api import get_countries_data, get_cases_data

import utils

# Window.size = 360, 640


class TableScreen(Screen, BoxLayout):
    pass


class MapScreen(Screen, BoxLayout):
    pass


class GraphScreen(Screen, BoxLayout):
    pass


class HomeScreen(Screen, BoxLayout):
    pass


class Map(MapView):
    pass


class MyListItem(OneLineListItem, ButtonBehavior):
    id = NumericProperty()


class MyList(ScrollView):
    items = ListProperty()
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.size = (1, dp(400))

        self.list = MDList()

        for i in self.items:
            self.list.add_widget(i)

        self.add_widget(self.list)


class MainApp(MDApp):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.primary_hue = '700'
        # self.theme_cls.theme_style = 'Dark'

        self._countries_data = get_countries_data()

        self._cases_plot = LinePlot(color=(1,0,0,1), line_width=(1.3))

        self.data_tables = MDDataTable(
            size_hint=(1, 1),
            rows_num=222,
            column_data=[
                ("No", dp(10)),
                ("Country", dp(40)),
                ("Total Cases", dp(30)),
            ],
            row_data=self.set_row_data()[0],
            sort=True,
            on_row_press=self.on_row_pressed_,
        )
        self.country_dialog = MDDialog(
                    title='Select A Country',
                    type='custom',
                    size_hint=(.8, .9),
                    content_cls=MyList(items=[MyListItem(id=idx, text=val, on_press=lambda e: self.on_select_country(e.id)) \
                            for idx, val in enumerate(self.set_row_data()[1])])
            )


    def build(self):
        pass
        self.root.ids['table_screen'].add_widget(self.data_tables)

    def change_screen(self, screen_name, direction='left'):
        self.root.ids['screen_manager'].current = screen_name
        self.root.ids['screen_manager'].transition.direction = direction

    def callback(self, ins):
        if ins.icon == 'home':
            self.change_screen('home_screen')
        elif ins.icon == 'map':
            self.change_screen('map_screen')
        elif ins.icon == 'table':
            self.change_screen('table_screen')
        elif ins.icon == 'graph':
            self.change_screen('graph_screen')
        else:
            pass

        self.root.ids['dial_btn'].close_stack()

    def on_start(self):

        self.root.ids['home_screen'].ids['cases_tot'].text = "+"+utils.format_number(self._countries_data[0]['cases'])+' Total'
        self.root.ids['home_screen'].ids['cases_inc'].text = "+"+utils.format_number(self._countries_data[0]['today_cases'])
        self.root.ids['home_screen'].ids['recovered_tot'].text = "+"+utils.format_number(self._countries_data[0]['recovered'])+' Total'
        self.root.ids['home_screen'].ids['recovered_inc'].text = "+"+utils.format_number(self._countries_data[0]['today_recovered'])
        self.root.ids['home_screen'].ids['deaths_tot'].text = '+'+utils.format_number(self._countries_data[0]['deaths'])+' Total'
        self.root.ids['home_screen'].ids['deaths_inc'].text = '+'+utils.format_number(self._countries_data[0]['today_deaths'])

        self.create_graph()

    def open_modal(self):
        self.country_dialog.open()

    def set_row_data(self):
        _row_data = []
        _list_items = []

        for idx, country in enumerate(self._countries_data):
            _row_data.append((idx+1, country['country_name'], utils.format_number(country['cases'])))
            _list_items.append(country['country_name'])

        return _row_data[::-1], _list_items

    def on_row_pressed_(self, *args):
        print(args)

    def on_select_country(self, id):

        _select_button = self.root.ids['home_screen'].ids['select_btn']

        _cases_inc = self.root.ids['home_screen'].ids['cases_inc']
        _cases_tot =  self.root.ids['home_screen'].ids['cases_tot']
        _recovered_inc = self.root.ids['home_screen'].ids['recovered_inc']
        _recovered_tot = self.root.ids['home_screen'].ids['recovered_tot']
        _deaths_inc = self.root.ids['home_screen'].ids['deaths_inc']
        _deaths_tot = self.root.ids['home_screen'].ids['deaths_tot']

        _cases_tot.text = "+"+utils.format_number(self._countries_data[id]['cases'])+' Total'
        _cases_inc.text = "+"+utils.format_number(self._countries_data[id]['today_cases'])
        _recovered_tot.text = "+"+utils.format_number(self._countries_data[id]['recovered'])+' Total'
        _recovered_inc.text = "+"+utils.format_number(self._countries_data[id]['today_recovered'])
        _deaths_tot.text = '+'+utils.format_number(self._countries_data[id]['deaths'])+' Total'
        _deaths_inc.text = '+'+utils.format_number(self._countries_data[id]['today_deaths'])

        _select_button.text = self._countries_data[id]['country_name']

        self.country_dialog.dismiss()

    def create_graph(self):
        self._cases_graph = self.root.ids['graph_screen'].ids['cases_graph']

        _cases = get_cases_data()
        self._cases_graph.ymax = max(_cases.values()) + 2000000
        self._cases_graph.ymin = min(_cases.values()) - 2000000

        self._cases_graph.xmin = -5
        self._cases_graph.xmax = 125

        _data_points = [(i, val) for i, val in enumerate(_cases.values() )]
        self._cases_plot.points = _data_points

        self._cases_graph.add_plot(self._cases_plot)

if __name__ == '__main__':
    MainApp().run()
