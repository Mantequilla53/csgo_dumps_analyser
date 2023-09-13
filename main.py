import threading
import PySimpleGUI as sg
from pypresence import Presence
from dumper import Dumper

sg.theme('DarkAmber')
clientId = '1108239399726108702'

def main():
    RPC = Presence(clientId)
    RPC.connect()
    layout = [
        [sg.Text('CSGO Inventory History Advanced Analyzer')],
        [sg.Text('Enter your cookies: '), sg.InputText()],
        [sg.Submit('Start Dump'), sg.Cancel()],
        [sg.Text(f"0 items found - you need to start the dump.", key='status')]
    ]

    window = sg.Window('CSGOAnalyzer Dumper', layout)
    RPC.update(
        details="Searching for Steam Cookie to begin..",
        buttons=[{"label": "CSGOAnalyzer", "url": "https://csgoanalyzer.com"}]
    )
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            dumper.export()
            break
        if event in 'Start Dump':
            window['Start Dump'].update(disabled=True)
            try:
                dumper = Dumper(values[0])
            except ValueError as e:
                sg.popup_error(e)
                window['Start Dump'].update(disabled=False)
            threading.Thread(target=dumper.dump, args=(window,RPC,), daemon=True).start()
        window['status'].update(f"{len(dumper.dumpedItems)} items found")
        print(len(dumper.dumpedItems))
        window.refresh()

    window.close()


if __name__ == '__main__':
    main()
