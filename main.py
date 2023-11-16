import requests
import wikipediaapi
import traceback


def print_categorymembers(categorymembers, file, error, level, max_level):
    for c in categorymembers.values():
        try:
            if (c.ns == wikipediaapi.Namespace.MAIN):
                lastindex = c.fullurl.rindex("/") + 1
                pageName = c.fullurl[lastindex:]
                resp = requests.get(urlApi+pageName+'/daily/'+start+'/'+end, headers=header)
                data = resp.json()
                if 'items' in data:
                    for p in data['items']:
                        file.write(p['article']+";"+p['timestamp']+";"+str(p['views'])+"\n")
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                print_categorymembers(c.categorymembers, file, error, level=level + 1, max_level=max_level)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            error.write(c.fullurl + '\n')
            pass

try:
    start='20160101'
    end='20230101'
    urlApi = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/'
    header={'User-Agent':'dboberic@uns.ac.rs','Api-User-Agent':'dboberic@uns.ac.rs'}
    wiki_wiki = wikipediaapi.Wikipedia('FeminismProject (dboberic@uns.ac.rs)', 'en')
    cat = wiki_wiki.page("Category:Feminism")
    f = open("categoryFeminism-level1.txt", "a")
    fe = open("error-level1.txt", "a")
    print_categorymembers(cat.categorymembers, f, fe,level=0,max_level=1)
except:
    traceback.print_exc(file=fe)
    pass
f.close()
fe.close()


