import random
import igraph as ig
import smtplib

#Les personnes qui s'offrent des cadeaux et leur adresse email
personnes = {
    'personne1':{''},
    'personne2':{''}
}

#Ne pas offrir de cadeaux entre ces liens
liens_a_eviter = {
    'personne1': [],
    'personne2' : []
}

#Themes des cadeau à renseigner par personne
types  = [('taille1','theme1'),('taille2','theme2')]

#Configuration pour l'envoi des mails.
serveur_smtp=''      #'smtp.gmail.com'
identifiant_smtp=''  #'nom@gmail.com'
mot_de_passe_smtp='' #'motdepass'e


#########################################################################################################################
############################ Definition des fonctions utiles au tirage au sort  #########################################
#########################################################################################################################
    
def build_graph(peoples, types, rm_links):
    g = ig.Graph(directed=True)
    g.add_vertices(list(peoples.keys()))
                   
    for src in g.vs:
        targets = [ tgt for tgt in g.vs if tgt!=src and tgt['name'] not in rm_links[src['name']] ]
        for dst in targets:
            for t in types:
                g.add_edge(src, dst, type=t)        
    return g

def plot(g):
    ig.plot(g, vertex_label = g.vs['name'], edge_label=[ e['type'][0] for e in g.es ])

def remove_path(g, path):
    #plot(g)
    for e0 in path.es:
        source   = path.vs[e0.source]['name']
        target   = path.vs[e0.target]['name']
        type     = e0['type']
        rm_edges = []
        for e in g.es:            
            src = g.vs[e.source]['name']
            tgt = g.vs[e.target]['name']
            tp  = e['type']

            if ((src == source and tgt == target)  or
                (src == source and type == tp)  or
                (tgt == target and type == tp)):
                rm_edges.append(e)
        g.delete_edges(rm_edges)
        #plot(g)
    return g
    
            
def random_circuit(g):
    """ Circuit aleatoire dans un graph """

    def outdegree(g, v):
        return len([ e for e in g.es if e.source == v])
    
    def next_edge(g, v=None):
        """ 
        A partir d'un sommet retourne  le sommet suivant du chemin aleatoire. 
        Supprime les liens vers le sommet suivant excepté celui depuis le sommet source.
        Supprime les liens depuis le sommet source excepté celui vers le sommet suivant.
        Si aucun sommet n'est donné, effectue un départ aléatoire en supprimant les arrêtes entrante au départ.
        Si aucun voisin n'existe, retourne None
        """
        if v is None or v<0:
            #Départ
            edge = g.es[random.randint(0, len(g.es)-1)]
            source= edge.source
            target = edge.target
            init_edges = [ (e.source, e.target, e['type'], g.vs[e.source]['name'], g.vs[e.target]['name']) for e in g.es if e.target == source ]
            g.delete_edges([ e for e in g.es if e.index != edge.index and (e.target == source or e.target == target or e.source == source) ])
            return target, source, init_edges
        
        elif g.vs[v].outdegree() == 0:
            #Arrivée
            return None

        else:
            #Autre que départ ou arrivée.
            out_edges = [ e for e in g.es if e.source == v ]
            edge = out_edges[random.randint(0, len(out_edges)-1)]
            target = edge.target
            g.delete_edges([ e for e in g.es if e.index != edge.index and (e.source == edge.source or e.target == edge.target)])
            return target

    tmp = g.copy()
    nxt, first, init_edges = next_edge(g=tmp)
    while nxt is not None:
        current = nxt
        nxt     = next_edge(tmp,current)

    init_edges = [ e for e in init_edges if e[0] == current and e[1] == first ]
    #Mauvais tirage, les sommets de départ et d'arrivé n'avaient pas de lien... On recommence
    if len(init_edges) == 0 or len(tmp.es) < len(tmp.vs)-1:
        return None
    init_edge = init_edges[random.randint(0, len(init_edges)-1)]
    tmp.add_edge(init_edge[3], init_edge[4], type=init_edge[2])
    #plot(tmp)
    return tmp

def print_tirage(tirage):
    """ Affiche un tirage """
    print("Resultat du tirage:")
    for e in tirage.es:
        donneur = tirage.vs[e.source]['name']
        receveur= tirage.vs[e.target]['name']
        taille  = e['type'][0]
        theme= e['type'][1]
        print( "\t%10s offre un %10s cadeau à %10s sur le thème %10s" % (donneur, taille, receveur, theme) )

def envoyer_email(tirage,
                  host=serveur_smtp,
                  user=identifiant_smtp,
                  password=mot_de_passe_smtp):
    """ 
    Envoi par email aux participants le résultat du tirage pour chacun d'entre eux.
    :param tirage: le résultat d'un tirage comme graph
    :param host: Le nom du serveur mail smtp.
    :param user: L'identifiant de l'utilisateur sur le serveur.
    :param password: Le mot de passe du serveur mail.
    """
    server = smtplib.SMTP_SSL(host)
    server.login(user, password)

    for e in tirage.es:
        donneur = tirage.vs[e.source]['name']
        receveur= tirage.vs[e.target]['name']
        taille  = e['type'][0]
        theme= e['type'][1]
        toaddr   = personnes[donneur]['email']
        fromaddr = 'pere@noel.fr'
        msg = ("From: %s\r\nTo: %s\r\n\r\n"
               % (fromaddr, toaddr))
        msg += "Bonjour %s,\nTu dois offrir un %s cadeau a %s\n" % (donneur, taille, receveur)
        msg += "Ce cadeau doit respecter le theme: %s\n" % theme
        msg += "\nJoyeux Noel !\n--Pere Noel"
        server.sendmail(fromaddr, toaddr, msg)
        
    server.quit()

#########################################################################################################################
########################################### TIRAGE AU SORT ! ############################################################
#########################################################################################################################

def faire_les_tirages():
    tirages = []
    g = build_graph(personnes, types, liens_a_eviter)

    for i in range(len(types)):
        #plot(g)
        t = random_circuit(g)
        if t is None: return faire_les_tirages()
        remove_path(g,t)        
        tirages.append(t)
        
    return tirages

def has_duplicate(array):
    dup = [ a for n, a in enumerate(array) if a in array[:n] ]
    return len(dup)>0

def verifier_tirages(tirages):        
    """ 
    Pour chaque personnes on vérifie qu'elle n'offre pas ou ne recoit pas deux fois le même cadeau ou deux fois le même thème.
    """
    ret = False
    participants = personnes.copy()
    for p in participants.keys():
        participants[p] = {}
        participants[p]['type_to']   = []
        participants[p]['type_from'] = []
        participants[p]['receveur']  = []
        
    for tirage in tirages:
        if len(tirage.es) < len(participants.keys()):
            print("Tirage trop petit")
            #plot(tirage)
            return True
        
        for e in tirage.es:
            donneur = tirage.vs[e.source]['name']
            receveur= tirage.vs[e.target]['name']
            type  = e['type']
            participants[donneur]['type_to'].append(type)
            participants[donneur]['receveur'].append(receveur)
            participants[receveur]['type_from'].append(type)
    
    for p in participants.keys():
        for r in participants[p]['receveur']:
            if r in liens_a_eviter[p]:
                print('%s ne doit pas offrir à %s.' % (p,r))
                return True

        for k in participants[p].keys():
            if has_duplicate(participants[p][k]):
                print("Duplicate in %s %s %s" % (p, k, str(participants[p][k])))
                return True
    return False


tirages = faire_les_tirages()
while verifier_tirages(tirages):
     tirages = faire_les_tirages()

for tirage in tirages or []:    
    if len(serveur_smtp) == 0 or len(identifiant_smtp) == 0 or len(mot_de_passe_smtp) == 0:
        print_tirage(tirage)
    else:
        envoyer_email(tirage)

