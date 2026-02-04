import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        value = self._view.dd_ruolo.value
        self._model.build_graph(value)
        self._view.btn_classifica.disabled = False
        self._view.btn_cerca_percorso.disabled = False
        self._view.dd_iniziale.disabled = False
        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(ft.Text(f"Nodi: {self._model.G.number_of_nodes()} | Archi: {self._model.G.number_of_edges()}"))
        self._view.update()

    def handle_classifica(self, e):
        list = self._model.classifica()
        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(ft.Text(f"Artisti in ordine decrescente di influenza"))
        for l in list:
            self._view.list_risultato.controls.append(ft.Text(f"{l[0]} --> Delta: {l[1]}"))
        self._view.update()


    def popola_dropdown_ruolo(self):
        ruoli = self._model.get_role()
        self._view.dd_ruolo.options = [ft.dropdown.Option(text=r) for r in ruoli]
        self._view.update()

    def popola_dropdown_iniziale(self):
        artisti = self._model.G.nodes()
        self._view.dd_ruolo.options = [ft.dropdown.Option(key= r.artist_id, text=r.name) for r in artisti]
        self._view.update()


    def handle_percorso(self,e):
        try:
            value = int(self._view._input_L.value)
            artista = self._view.dd_iniziale.value
            if value >= 3 and value <= len(self._model.G.nodes()):
                self._model.compute_path(value, artista)
                for e in len(self._model.path) - 1:
                    self._view.list_risultato.controls.clear()
                    self._view.list_risultato.controls.append(f"{self._model.path[e]} --> {self._model.path[e+1]}", end=" ")
                self._view.list_risultato.controls.append(f"peso massimo: {self._model.sol_best}")
                self._view.update()
            else:
                self._view.show_alert(f"valore non rientrante nell'intervallo [3,{len(self._model.G.nodes())}]")
        except ValueError:
            self._view.show_alert("Input non accettato")