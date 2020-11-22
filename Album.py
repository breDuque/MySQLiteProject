class Banco:
    def __init__(self):
        import sqlite3
        self.banco = sqlite3.connect('discografia.db')
        self.banco.row_factory = sqlite3.Row
        self.cursor = self.banco.cursor()

    def CreateTable(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS album (
                id INTEGER PRIMARY KEY, 
                nome_album TEXT, 
                nome_banda TEXT, 
                data_album TEXT)
            """)
        self.Commit() 

    def InsetTable(self,nome_album,nome_banda,data_album):
        self.cursor.execute(f"INSERT INTO album (nome_album, nome_banda, data_album) VALUES (?, ?, ?)", (nome_album, nome_banda, data_album))
        self.Commit()

    def DeleteTable(self,x):
        self.cursor.execute("DELETE FROM album WHERE id=?",(x+1,))
        self.Commit()

    def SelectTable(self):
        self.cursor.execute("SELECT * FROM album")
        return [list(row) for row in self.cursor.fetchall()]

    def Commit(self):
        self.banco.commit()

class Telas:
    import PySimpleGUI as sg
    import pandas as pd
    def __init__(self):
        self.sg.theme('DarkAmber')
        self.banco = Banco()
        self.banco.CreateTable()
        
    def TelaInicio(self):
        headerList = ['ID','Album Name', 'Band Name', 'Album Date']
        empty_data=[['' for _ in range(len(headerList))]]
        data = self.banco.SelectTable()
        layout = [
            [self.sg.Text('Please, select one option.')],
            [self.sg.Table(values=data,
            headings=headerList,
            max_col_width=25,
            key='-TABLE-',
            auto_size_columns=True,
            justification='left',
            num_rows=min(len(data), 10))],
            [self.sg.Button('INSERT'),self.sg.Button('DELETE')],
            [self.sg.Button('REFRESH')]
        ]

        window = self.sg.Window('Start',element_justification='c').layout(layout)

        while True:
            event, values = window.Read(timeout=1)
            
            # window.find_element('-TABLE').Update(values=data)

            if event == self.sg.WIN_CLOSED:
                window.close()
                break

            if event == 'INSERT':
                self.TelaInsert()


            if event == 'DELETE':
                x = values['-TABLE-'][0]
                self.banco.DeleteTable(x)

        
    def TelaInsert(self):
        layout = [
            [self.sg.Text('Album Name:'),self.sg.Input(k='-AlbumName-',size=(25,0))],
            [self.sg.Text('Band Name:  '),self.sg.Input(k='-BandName-',size=(25,0))],
            [self.sg.Text('Album Date:  '),self.sg.Input(k='-AlbumDate-',size=(25,0))],
            [self.sg.Button('INSERT')]
            ]

        window = self.sg.Window('Insert Album').layout(layout)
        
        while True:
            event, values = window.Read()
            albumName = values['-AlbumName-']
            bandName = values['-BandName-']
            albumDate = values['-AlbumDate-']

            if event == self.sg.WIN_CLOSED:
                break

            if event == 'INSERT':
                self.banco.InsetTable(albumName,bandName,albumDate)
                window.close()
                break


tela = Telas()
tela.TelaInicio()