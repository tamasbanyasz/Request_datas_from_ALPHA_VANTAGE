import requests
import orjson
import jmespath
from datetime import datetime
from nicegui import ui
from pandas import DataFrame, json_normalize

"""
It's just a practicing and learnig how to request datas effeciantly from Alpha Vantage with some interesting library.
And how can we query datas from the gathered datas and display those datas in NiceGUI...

"""

class RequestFromAlphaVantage:
    def __init__(self):
        self.url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=AIHU0QXP4BWWFEAE"
        self.clumns = {
                "Symbol": '"Meta Data"."2. Symbol"',
                "Last refresh": '"Meta Data"."3. Last Refreshed"',
                "Time Zone": '"Meta Data"."5. Time Zone"'
        }
        self.json_path = 'NiceGUI_practice_1_1v/file.json'

    def get_datas(self):
        datas = requests.get(self.url)
        return datas.json()
        
    def overwrite_json_file(self, data):
        with open(self.json_path, 'wb') as f:
            f.write(orjson.dumps(data))
    
    def read_from_json(self):
        with open(self.json_path, 'rb') as f:
            data = orjson.loads(f.read())
            return data

class GuiOfAlphaVantage:
    def __init__(self) -> None:                
        self.request_class = RequestFromAlphaVantage()
        self.card_opened = False
        
        datas = self.request_class.read_from_json()
        print(datas)

        def show_time(self) -> None:
            ui.notify(f'Current time is {datetime.now()}')

        def close_table(card, top_card) -> None:
            
            if card.visible and top_card:
                card.classes('invisible')
                top_card.classes('invisible')
            self.card_opened = False
            
            
        def load_special_datas_from_json() -> None:
            if not self.card_opened:
                
                symbol = [{key: jmespath.search(query, datas) for key, query in self.request_class.clumns.items()}]
                print(symbol)
            
                queried_dates = jmespath.search('"Time Series (Daily)"', datas)
                print(queried_dates)
                
                with ui.card().style('display: flex; position: absolute; right: 237%; top: 1%; height: 55px; width: 438px; background-color: #f3ad05;').classes('visible') as top_card:
                    with ui.element('div').classes('p-2 bg-blue-100'):
                        ui.label(', '.join(f"{key}: {value}" for key, value in symbol[0].items()))
                
                with ui.card().style('display: flex; position: absolute; right: 180%; top: 23%; height: 240px; width: 590px; background-color: #ba543b;').classes('visible') as card:
                    self.card_opened = True
                    df = DataFrame(queried_dates).T
                    df.index.name = 'Date'
                    df.reset_index(inplace=True)
                    table = ui.table.from_pandas(df).classes('max-h-40')
                    table.add_slot('body-cell-1. open', '''
                        <q-td key="open" :props="props">
                            <q-badge :color="props.value < 170 ? 'red' : 'green'">
                                {{ props.value }}
                            </q-badge>
                        </q-td>
                    ''')
                    table.add_slot('body-cell-Date', '''
                        <q-td :props="props" :class="props.row['1. open'] < 170 ? 'text-red' : 'text-green'">
                                {{ props.value }}
                        </q-td>
                    ''')
                    with ui.row().style('padding-left: 240px;'):
                        ui.button('Exit', on_click=lambda: close_table(card, top_card))
                    
                
        with ui.row().style('display: flex; position: absolute; right: 4%; top: 1%;'):
            with ui.card().style('display: flex; height: 200px; width: 300px; background-color: #ba543b;'):
                with ui.row().style('margin-left: 100px'):
                    ui.chat_message('Welcome Stranger!',
                        name='Robot',
                        stamp= "Click to..",
                        avatar='https://robohash.org/ui')
                
                with ui.row().style('padding-left: 10px;'):
                    ui.button('Time', on_click=show_time)
                    ui.button('Alpha Vantage', on_click=load_special_datas_from_json)

        ui.run()
        
GuiOfAlphaVantage()
