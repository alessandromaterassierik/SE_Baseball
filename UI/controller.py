import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        y_input = self._view.dd_anno.value
        self._model.build_graph(y_input)

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        self._view.txt_risultato.controls.clear()
        text_input= self._view.dd_squadra.value
        node_input = text_input[0:3]
        list_nodes=[]

        for i in list(self._model.G.neighbors(node_input)):
            list_nodes.append((i ,{self._model.G[node_input][i]['weight']}))

        list_nodes.sort(key=lambda x: x[1], reverse=True)

        for j in list_nodes:
            n = self._model.teams_dict[j[0]]
            self._view.txt_risultato.controls.append(ft.Text(f'{j[0]} ({n}) peso {j[1]}'))
        self._view.update()

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        text_input = self._view.dd_squadra.value
        n_input = text_input[0:3]
        sol_ott, w_ott = self._model.ricerca_cammino(n_input)

        self._view.txt_risultato.controls.clear()
        c=-1
        for i in sol_ott:
            c+=1
            if c == len(sol_ott)-1:break
            else:
                self._view.txt_risultato.controls.append(ft.Text(f'{i} --> {sol_ott[c+1]} peso {self._model.G[i][sol_ott[c+1]]['weight']}'))
                self._view.update()

        self._view.txt_risultato.controls.append(ft.Text(f'Peso totale: {w_ott}'))

        self._view.update()

    def populate_dd_anno(self):
        """ Metodo per popolare i dropdown """
        self._view.dd_anno.options.clear()
        self._model.get_years()
        for y in self._model.years:
            self._view.dd_anno.options.append(ft.dropdown.Option(key=y, text=y))
        self._view.update()

    def populate_dd_squadra(self, e):
        y_input = self._view.dd_anno.value
        self._model.get_teams(y_input)

        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f'Numero squadre: {len(self._model.teams)}'))
        for i in range(len(self._model.teams)):
            self._view.txt_out_squadre.controls.append(ft.Text(f'{self._model.teams[i][0]} ({self._model.teams[i][1]})'))

        for t in range(len(self._model.teams)):
            team = f'{self._model.teams[t][0]} ({self._model.teams[t][1]})'
            self._view.dd_squadra.options.append(ft.dropdown.Option(key=self._model.teams[t][0], text=team))
        self._view.update()