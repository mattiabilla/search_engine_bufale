"""
Script che contiene tutta la parte di ricerca sull'indice e utilizza flask per restituire i risultati in una pagina web.
"""
from whoosh import qparser
from whoosh.analysis import LanguageAnalyzer
from whoosh.qparser import MultifieldParser, OrGroup

from whoosh.index import open_dir

import re
from flask import Flask, request, render_template

from whoosh.highlight import SentenceFragmenter

from nltk.corpus import wordnet as wn

from whoosh.query import Term, Or, And, DateRange

from datetime import date, time, datetime

from whoosh.scoring import TF_IDF

app = Flask(__name__)


def parseconc(par):
    """
    Funzione che, per ogni parola specificata come concept, costruisce una lista di tutte le parole.
    selezionate per l'espansione.
    :param par: Lista stringhe, formate da parola_da_espandere:espansione nell'URL.
    :return: Dizionario composto da, come chiave la parola che va espansa e come valore una lista composta dalle parole
    selezionate.
    """
    ret = dict()
    for i in par:
        conc = i[:i.find(':')]
        try:
            ret[conc]
        except KeyError:
            ret[conc] = list()
        val = i[i.find(':') + 1:]
        ret[conc].append(val.replace('_', ' '))

    return ret


# restituisce una lista che serve per costruire il filtro con l'oggetto Or
# quando andiamo ad effettuare una richiesta
def filter_site(site_pref):
    """
    Funzione utilizzata per ottenere una lista di Term, da mettere poi in un Or per poter utilizzare il filtro sulla
    fonte desiderata.
    :param site_pref: Lista di siti da cui vogliamo ottenere le informazioni.
    :return: Lista di Term con le preferenze indicate.
    """
    ret_list = list()
    for i in site_pref:
        ret_list.append(Term('site', i))

    return ret_list


@app.route('/', methods=['GET'])
def home_results():
    """
    Funzione principale, dove si ottengono i parametri di ricerca, la si effettua e si possono applicare filtri.
    :return: Oggetto per creare la struttura della pagina tramite il template indicato.
    """
    log = open('trace8_.txt', 'w', encoding='utf-8')
    data = ""
    par_conc = dict()  # struttura dati per rappresentare i concetti che vogliamo cercare
    site_pref = list()  # filtro per la lista dei siti che vogliamo cercare
    startdate = datetime.min  # le date da usare come filtro
    enddate = datetime.today()

    boost_title = 2.0           # parametri di tuning per la ricerca tramite concetti o "normale"
    boost_categories = 1.0
    boost_content = 1.0

    # prendo tutti i parametri che mi servono dalla query GET
    if request.method == 'GET' and 'query' in request.args:
        data = request.args.get('query')

        if 'concept' in request.args:
            par_conc = parseconc(request.args.getlist('concept'))

        if 'site' in request.args:
            site_pref = request.args.getlist('site')

        if 'start-date' in request.args and not request.args.get('start-date') == '':
            startdate = datetime.strptime(request.args.get('start-date'), '%Y-%m-%d')

        if 'end-date' in request.args and not request.args.get('end-date') == '':
            enddate = datetime.strptime(request.args.get('end-date'), '%Y-%m-%d')

        # controllo coerenza temporale sulle date
        if startdate > enddate:
            startdate, enddate = enddate, startdate

    retrieved = []
    did_you_mean = None
    ix = open_dir("../indexdir")
    with ix.searcher() as searcher:
        qp = None
        thterm = ""
        concepts = dict()

        # ricerca con thesaurus con []
        p = re.compile(r'\[\w*\]')
        for i in p.findall(data):
            boost_categories = 2.0                      # se sono per concetti allora effettuo il boost
            thterm = i[1:len(i) - 1]                    # prendo il termine escludendo le parentesi quadre
            synlist = wn.synsets(thterm, lang="ita")

            # struttura dati da passare alla pagina HTML
            concepts[thterm] = {"Iperonimo": [], "Iponimo": [], "Correlato": []}

            # ottengo tutte le possibili espansioni di una parola indicata tra parentesi quadre
            for syn in synlist:
                for i in syn.hyponyms():
                    if len(i.lemmas(lang="ita")):
                        concepts[thterm]["Iponimo"].append(i.lemmas(lang="ita")[0].name())
                for i in syn.hypernyms():
                    if len(i.lemmas(lang="ita")):
                        concepts[thterm]["Iperonimo"].append(i.lemmas(lang="ita")[0].name())

                concepts[thterm]["Correlato"].extend(syn.lemma_names(lang="ita"))

            concepts[thterm]["Correlato"] = list(set(concepts[thterm]["Correlato"]).difference(set([thterm])))

            # limitiamo la lunghezza delle liste a 5 risultati
            try:
                concepts[thterm]['Iperonimo'] = concepts[thterm]['Iperonimo'][0:5]
                concepts[thterm]['Iponimo'] = concepts[thterm]['Iponimo'][0:5]
                concepts[thterm]['Correlato'] = concepts[thterm]['Correlato'][0:5]
            except IndexError:
                pass

        # si salva la query per scriverla nella barra di ricerca del template, prima di espanderla
        olddata = data

        # espansione della query con i concetti dati dall'utente per ogni parola considerata
        # con struttura del tipo "(parola OR parola OR parola)"
        for i in p.findall(data):
            thterm = i[1:len(i) - 1]
            replstr = f"({thterm}"
            try:
                for c in par_conc[thterm]:
                    replstr += f" OR {c}"
            except KeyError:
                pass
            finally:
                replstr += ")"

            data = data.replace(i, replstr)

        # costruzione del parser su diversi campi con i relativi boost
        qp = MultifieldParser(["categories", "title", "content"], ix.schema, group=OrGroup,
                              fieldboosts={'categories': boost_categories, 'title': boost_title,
                                           'content': boost_content})
        qp.remove_plugin_class(qparser.WildcardPlugin)
        query = qp.parse(data)

        # correzione degli errori nella query
        corrected = searcher.correct_query(query, data)
        if corrected.query != query:
            did_you_mean = corrected.string

        # effettuo la ricerca applicando i filtri
        results = searcher.search(query,
                                  filter=And([Or(filter_site(site_pref)), DateRange('date', startdate, enddate)]))
        results.fragmenter = SentenceFragmenter()

        # per ogni risultato, ottengo i dati e li metto in una lista e poi li passo alla pagina html
        for i in results:
            link = i["url"]
            log.write(link + '\n')
            title = i["title"]
            linkimage = i["urlimage"]
            resultdate = i["date"]
            resultdate = resultdate.strftime("%d/%m/%Y")
            snippet = i.highlights("content", top=1)
            print(snippet)

            p = re.compile(r"www\.[^\/]+")
            match = p.search(link)
            site = match.group(0)
            print(site)

            retrieved.append(
                {"link": link, "title": title, "site": site, "urlimage": linkimage, "date": resultdate,
                 "snippet": snippet})

        log.close()

    # si mandano al template tutti i dati che servono per restituire i risultati
    return render_template("index.html", results=retrieved, correction=did_you_mean, concepts=concepts, query=olddata)
