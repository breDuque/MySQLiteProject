class Banco:
    def __init__(self):
        import sqlite3
        self.banco = sqlite3.connect('discografia.db', isolation_level=None)
        self.banco.row_factory = sqlite3.Row
        self.cursor = self.banco.cursor()


    def CreateTable(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS album ( 
                nome_album TEXT, 
                nome_banda TEXT, 
                data_album TEXT)
            """)
        
        self.Commit() 

    def InsetTable(self,nome_album,nome_banda,data_album):
        self.cursor.execute(f"INSERT INTO album (nome_album, nome_banda, data_album) VALUES (?, ?, ?)", (nome_album, nome_banda, data_album))
        self.Commit()

    def DeleteTable(self,x):
        self.cursor.execute("DELETE FROM album WHERE rowid = ?",(x+1,))
        self.cursor.execute('VACUUM')
        self.Commit()

    def UpdateTable(self,updateTuple,x):
        self.cursor.execute("""
            UPDATE album 
            SET nome_album = ? 
            WHERE rowid = ?
        """, (updateTuple[0], x+1))

        self.cursor.execute("""
            UPDATE album 
            SET nome_banda = ? 
            WHERE rowid = ?
        """, (updateTuple[1], x+1))        

        self.cursor.execute("""
            UPDATE album 
            SET data_album = ? 
            WHERE rowid = ?
        """, (updateTuple[2], x+1))

    def SelectTable(self):
        self.cursor.execute("SELECT rowid, * FROM album")
        return [list(row) for row in self.cursor.fetchall()]

    def SelectRow(self,x):
        self.cursor.execute("SELECT * FROM album WHERE rowid = ?",(x+1,))
        return [list(row) for row in self.cursor.fetchall()]

    def Commit(self):
        self.banco.commit()

class Telas:
    import PySimpleGUI as sg
    import pandas as pd
    def __init__(self):
        self.sg.theme('Reddit')
        self.banco = Banco()
        self.banco.CreateTable()
        
    def UpdateData(self):
        return self.banco.SelectTable()

    def TelaInicio(self):
        headerList = ['ID','Album Name', 'Band Name', 'Album Date']
        empty_data=[['' for _ in range(len(headerList))]]
        data = self.UpdateData()

        layoutWithoutData = [
            [self.sg.Text('Please, select one option.')],
            [self.sg.Table(values=empty_data,
            headings=headerList,
            max_col_width=25,
            key='-TABLE-',
            auto_size_columns=True,
            justification='left',
            num_rows=10)],
            [self.sg.Button('INSERT'),self.sg.Button('DELETE'),self.sg.Button('UPDATE'),self.sg.Button('EXIT')]
        ]
        layoutWithData = [
            [self.sg.Text('Please, select one option.')],
            [self.sg.Table(values=data,
            headings=headerList,
            max_col_width=25,
            key='-TABLE-',
            auto_size_columns=True,
            justification='left',
            num_rows=10)],
            [self.sg.Button('INSERT'),self.sg.Button('DELETE'),self.sg.Button('UPDATE'),self.sg.Button('EXIT')]
        ]
        
        if data:
            window = self.sg.Window('Start',element_justification='c').layout(layoutWithData)
        else:
            window = self.sg.Window('Start',element_justification='c').layout(layoutWithoutData)

        while True:
            event, values = window.Read()

            if event == self.sg.WIN_CLOSED or event == 'EXIT':
                window.close()
                break

            if event == 'INSERT':
                self.TelaInsert()

            if event == 'DELETE':
                x = values['-TABLE-'][0]
                self.banco.DeleteTable(x)

            if event == 'UPDATE':
                x = values['-TABLE-'][0]
                self.defaultValues = self.banco.SelectRow(x)
                print(self.defaultValues)
                self.TelaUpdate(x)  

            window['-TABLE-'].update(values=self.UpdateData())
            window.Refresh()

        
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

    def TelaUpdate(self,x):
        layout = [
            [self.sg.Text('Album Name:'),self.sg.Input(default_text=self.defaultValues[0][0],k='-AlbumName-',size=(25,0))],
            [self.sg.Text('Band Name:  '),self.sg.Input(default_text=self.defaultValues[0][1],k='-BandName-',size=(25,0))],
            [self.sg.Text('Album Date:  '),self.sg.Input(default_text=self.defaultValues[0][2],k='-AlbumDate-',size=(25,0))],
            [self.sg.Button('UPDATE')]
            ]

        window = self.sg.Window('Update Album').layout(layout)
        
        while True:
            event, values = window.Read()
            albumName = values['-AlbumName-']
            bandName = values['-BandName-']
            albumDate = values['-AlbumDate-']

            updateTuple = (albumName,bandName,albumDate)

            if event == self.sg.WIN_CLOSED:
                break

            if event == 'UPDATE':
                self.banco.UpdateTable(updateTuple,x)
                window.close()
                break

tela = Telas()
tela.TelaInicio()