class Graphe:
    def __init__(self,nbs):
        self.nbs = nbs
        self.LgrapheAdj = [[0 for i in range(self.nbs)]for j in range(self.nbs)]
        self.LgrapheI = [[]for j in range(self.nbs)]
    
    #yan + zizi = coeur
    def sommet(self):
        return [i for i in range(self.nbs)]
    
    def arcs(self):
        lArc = []
        for i in range(len(self.LgrapheAdj)):
            for j in range(len(self.LgrapheAdj[0])):
                if self.LgrapheAdj[i][j] != 0:
                    lArc.append((i,j,self.LgrapheAdj[i][j]))
        return lArc
    
    def arcSommet(self,sommet):
        
        if sommet in self.sommet():            
                
            lArc = []
            for i in range(len(self.LgrapheAdj)):
                if self.LgrapheAdj[i][sommet] != 0:
                    lArc.append((i,sommet,self.LgrapheAdj[i][sommet]))
            for i in range(len(self.LgrapheAdj[sommet])):
                if self.LgrapheAdj[sommet][i] != 0:
                    lArc.append((sommet,i,self.LgrapheAdj[sommet][i]))
            return lArc
        else : print("ce sommet n'existe pas")
        
    def arcsEntrant(self,sommet):
        
        if sommet in self.sommet():            
                
            lArc = []
            for i in range(len(self.LgrapheAdj)):
                if self.LgrapheAdj[i][sommet] != 0:
                    lArc.append((i,sommet,self.LgrapheAdj[i][sommet]))

            return lArc
        else : print("ce sommet n'existe pas")
        
    def arcsSortant(self,sommet):
        
        if sommet in self.sommet():            
                
            lArc = []
            for i in range(len(self.LgrapheAdj[sommet])):
                if self.LgrapheAdj[sommet][i] != 0:
                    lArc.append((sommet,i,self.LgrapheAdj[sommet][i]))
                    
            return lArc
        else : print("ce sommet n'existe pas")
                            
    def afficherListe(self,type="both"):
        if type != "Incidence" :
            
            for i in self.LgrapheAdj:
                ligne = "| "
                for j in i:
                    if 0 <=j < 10:
                        j = " " + str(j)
                    ligne+=str(j)+" "
                print(ligne+"|")
                
            print("")
        if type != "Adjacence" :

            for i in self.LgrapheI:
                ligne = "| "
                for j in i:
                    if 0 <=j < 10:
                        j = " " + str(j)
                    ligne+=str(j)+" "
                print(ligne+"|")
            print(" ")
            
    def voisin(self,sommet):
        if sommet in self.sommet():
            voisin = []
            for i in self.arcsEntrant(sommet):
                voisin.append(i[0])
            for i in self.arcsSortant(sommet):
                voisin.append(i[1])
            return voisin
        else:
            print("ce sommet n'existe pas")
                
    def ajouterSommets(self,nbSommet):
        self.nbs += nbSommet
        
        if self.nbs == 1:
            self.LgrapheI = [[0]]
            self.LgrapheAdj = [[0]]
            
        else:
            for i in range(nbSommet):
                self.LgrapheI += [[0 for t in range(len(self.LgrapheI[0]))]]
                for j in range(len(self.LgrapheAdj)):
                    self.LgrapheAdj[j].append(0)
                
            for i in range(nbSommet):
                self.LgrapheAdj.append([0 for n in range(self.nbs)])    
                
                
    def ajouterLien(self,s1,s2,poids = 1,orientation=1):
        
        if orientation >= 0:
            self.LgrapheAdj[s1][s2] = poids
            
            for i in range(len(self.LgrapheI)):
                if i == s1:
                    self.LgrapheI[i].append(-1)
                elif i == s2:
                    self.LgrapheI[i].append(1)                
                else:
                    self.LgrapheI[i].append(0)
 
                
        if orientation <= 0:
            self.LgrapheAdj[s2][s1] = poids
            for i in range(len(self.LgrapheI)):
                if i == s1:
                    self.LgrapheI[i].append(1)
                elif i == s2:
                    self.LgrapheI[i].append(-1)                
                else:
                    self.LgrapheI[i].append(0)
    
    def isOriente(self):
        for i in range(self.nbs):
            for j in range(self.nbs):
                if self.LgrapheAdj[i][j] != self.LgrapheAdj[j][i]:
                    return True
        return False
    
    def isOrienteInc(self):
        for i in self.LgrapheI:
            sum = 0
            for j in i:
                sum+=j
            if sum !=0:
                return True
        return False   
    
    def cree_GrapheAdjDico(self):
        self.grapheAdjDico = {i:{} for i in range(len(self.LgrapheAdj))}
        for i in range(len(self.LgrapheAdj)):
            for j in range(len(self.LgrapheAdj[i])):
                if self.LgrapheAdj[i][j] != 0:
                    self.grapheAdjDico[i][j] = self.LgrapheAdj[i][j]                                