import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.years = ''
        self.teams = ''
        self.teams_salary = ''
        self.st_dist =''
        self.G = nx.DiGraph()

    def get_years(self):    #[1980, 1981, 1982, 1983, 1984
        years = DAO.load_years()
        self.years = [y['year'] for y in years]

    def get_teams(self, year):#[('ATL', 'Atlanta Braves'), ('BAL', 'Baltimore Orioles'),
        teams = DAO.load_teams(year)
        self.teams = [(t['team_code'], t['name']) for t in teams]
        self.teams_dict = {t['team_code'] : t['name'] for t in teams}

    def get_teams_salary(self, year):       #[{'team_code': 'BAL', 'tuple_teams': 'ATL', 'total_salary': 3930334652.0},
        tot_salary = DAO.load_teams_salary(year)
        self.teams_salary = [(t['team1'], t['team2'], t['total_salary']) for t in tot_salary]

    def build_graph(self, year):
        self.get_teams_salary(year)
        for i in self.teams_salary:
            self.G.add_edge(i[0], i[1], weight=i[2])

            '''path di peso max:
            Il punto di partenza  vertice selezionato
            Il peso degli archi decrescente.
            solo primi K archi adiacenti ordinati peso decrescente (ad esempio K=3),  ogni vertice esplora al massimo i K vicini più pesanti che rispettano il vincolo decrescente.
            '''

    def ricerca_cammino(self, n_input):
        self.sol_ott = []
        self.w_ott = 0
        self.ricorsione(n_input, sol_part=[n_input], w_cur=0)
        return self.sol_ott, self.w_ott

    def ricorsione(self, n, sol_part, w_cur, k=3):
        # update
        if w_cur > self.w_ott:
            self.sol_ott = sol_part.copy()
            self.w_ott = w_cur

        # end
        if len(self.sol_ott) == len(self.G.nodes):
            return

        # ciclo
        #('CA', 'AZ', {'weight': 43}) -> post self.G.edges(n, data=True)
        neigh = sorted(self.G.edges(n, data=True) , key=lambda x: x[2]['weight'])
        # neigh with weight  -> ordino in senso decrescente in funzione del peso
        #neigh.sort(key=lambda x: x[2]['weight'], reverse=False)

        for n_i in neigh[0:k]:
            n_i = n_i[1]
            if n_i not in sol_part and self.vincoli(n, n_i, sol_part):
                w = self.G[sol_part[-1]][n_i]['weight']
                sol_part.append(n_i)
                self.ricorsione(n_i, sol_part, w_cur + w, k=3)
                sol_part.pop()

    def vincoli(self, n, n_i, sol_part):
        if len(sol_part) == 1:
            print('primo giro')
            return True
        else:
            if int(self.G[sol_part[-2]][sol_part[-1]]['weight']) > int(self.G[sol_part[-1]][n_i]['weight']):
            # peso dell ultimo arco in sol parziale maggiore rispetto all arco che andrei a creare
                return True
            else:
                return False


