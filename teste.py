import PySimpleGUI as sg

hl=['a', 'b', 'c', 'd']
empty_table=[['' for _ in range(len(hl))]]
window = sg.Window("title", layout=[[sg.Table(empty_table, headings=hl, key='table', max_col_width=20), sg.Ok()]])
window.Read()
window.Element('table').Update(values=[[1,2,3,4],[5,6,7,8],[9,10,11,12]])
window.Read()
window.Close