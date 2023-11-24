from bs4 import BeautifulSoup
import urllib.request as rq



def screenshot(l_id_restaurant):
    # VAR
    les_restaurants = {"le-lac": "Le Lac", "le-forum": "Le Forum", "lanatide": "L'Anatidé", "pizzeria-le-borsalino": "Le Borsalino", "le-bistrot": "Le Bistrot", "cafebulle": "Café'bulle"}
    message = ""
    les_entrees = ""
    les_plats_du_jour = ""
    les_desserts = ""
    le_restaurant_titre = les_restaurants[l_id_restaurant]

    # BEGIN
    try :
        site = rq.urlopen("http://ru.florian.vanbraekel.fr/menu.html")
        html = site.read()
        soup = BeautifulSoup(html, 'html.parser')
        son_div = soup.find("div", {"id" : l_id_restaurant[:-2]})
        repas = son_div.find("ul", {"class" : "meal_foodies"})
        n=0
        for les_parties in repas:
            n+=1
            for la_partie in les_parties:
                if type(la_partie) == type(les_parties):
                    for plat in la_partie:
                        match n:
                            case 2:
                                les_entrees += "\t\t " + plat.string + "\n"
                            case 3:
                                les_plats_du_jour += "\t\t " + plat.string + "\n"
                            case 4:
                                les_desserts += "\t\t " + plat.string + "\n"
        
        # print(les_entrees)
        # print(les_plats_du_jour)
        # print(les_desserts)
        message += "**"+le_restaurant_titre+":**\n"


        if "Structure fermée" in les_entrees:
            message += les_entrees
        else:        
            message += "\tEntrée\n"
            message += les_entrees
            message += "\n\tPlat principal\n"
            message += les_plats_du_jour
            message += "\n\tDesserts\n"
            message += les_desserts

        message = "```" + message + "```"

        # print(message)

        return message
    
    except:
        return "***"+le_restaurant_titre+" : Le menu n'a pas pu être récupéré.***"


# screenshot("le forum")