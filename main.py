import threading
import PySimpleGUI as sg
from dumper import Dumper

sg.theme('DarkAmber')



def main():
    count = sg.Text()
    layout = [
        [sg.Text('CSGO Inventory History Advanced Analyzer')],
        [sg.Text('Enter your cookies: '), sg.InputText()],
        [sg.Submit('Start Dump'), sg.Cancel()],
        [sg.Text(key='count')]
    ]

    window = sg.Window('CSGOAnalyzer Dumper', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            dumper.export()
            break
        if event in 'Start Dump':
            window['Start Dump'].update(disabled=True)
            dumper = Dumper(values[0])
            threading.Thread(target=dumper.dump, daemon=True).start()

        window['count'].update(value=f"{len(dumper.dumpedItems)} items found")

    window.close()


if __name__ == '__main__':
    main()
