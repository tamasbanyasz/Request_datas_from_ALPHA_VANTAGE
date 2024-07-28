import requests
import orjson
import jmespath
from datetime import datetime
from nicegui import ui
from pandas import DataFrame

"""
It's just a practicing and learnig how to request datas effeciantly from Alpha Vantage with some interesting library.
And how can we query datas from the gathered datas and display those datas in NiceGUI...

I
"""

class RequestFromAlphaVantage:
    def __init__(self):
        self.url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=AIHU0QXP4BWWFEAE"

    def get_datas(self):
        datas = requests.get(self.url)
        return datas.json()
        
    def overwrite_json_file(self, data):
        with open('NiceGUI_practice_1_0v/file.json', 'wb') as f:
            f.write(orjson.dumps(data))
    
    def read_from_json(self):
        with open('NiceGUI_practice_1_0v/file.json', 'rb') as f:
            data = orjson.loads(f.read())
            return data

class GuiOfAlphaVantage:
    def __init__(self) -> None:                
        self.request_class = RequestFromAlphaVantage()

        datas = self.request_class.read_from_json()
        print(datas)

        def show_time(self) -> None:
            ui.notify(f'Current time is {datetime.now()}')

        def close_table(card) -> None:
            if card.visible:
                card.classes('invisible')
            
        def load_special_datas_from_json(self) -> None:
            
            symbol = jmespath.search('"Meta Data"."2. Symbol"', datas)
            print(symbol)
            
            queried_dates = jmespath.search('keys("Time Series (Daily)")', datas)
            print(queried_dates)
            
            with ui.card().style('display: flex; position: absolute; right: 180%; top: 1%; height: 240px; width: 300px; background-color: #ba543b;').classes('visible') as card:
                df = DataFrame(data={symbol: queried_dates})
                ui.table.from_pandas(df).classes('max-h-40')
                with ui.row().style('padding-left: 110px;'):
                    ui.button('Exit', on_click=lambda: close_table(card))
                
        with ui.row().style('display: flex; position: absolute; right: 4%; top: 1%;'):
            with ui.card().style('display: flex; height: 200px; width: 300px; background-color: #ba543b;'):
                with ui.row().style('margin-left: 100px'):
                    ui.chat_message('Welcome Stranger!',
                        name='Robot',
                        stamp='Click to ...',
                        avatar='https://robohash.org/ui')
                
                with ui.row().style('padding-left: 10px;'):
                    ui.button('Time', on_click=show_time)
                    ui.button('Alpha Vantage', on_click=load_special_datas_from_json)

        ui.run()
        
GuiOfAlphaVantage()
