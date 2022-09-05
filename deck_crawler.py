import sys 
import requests_html
import re

def main():
    session = requests_html.HTMLSession()
    mtgsite = session.get('https://www.mtgstocks.com/formats/3') #, context=ssl.create_default_context(cafile=certifi.where())
    
    archetype_list = []
    while not archetype_list:
        mtgsite.html.render(timeout=300)
        for link in mtgsite.html.links:
            if 'archetypes' in link:
                archetype_list.append(link) 
    mtgsite.close()

    for archetype in archetype_list:
        archetype_site = session.get(('https://www.mtgstocks.com' + archetype))
        deck = ''
        while not deck:
            archetype_site.html.render(timeout=300)
            for link in archetype_site.html.links:
                if 'decks' in link:
                    if not deck:
                        deck = link
                    elif link > deck: #Gets most recent version of deck
                        deck = link
        archetype_site.close()

        deck_site = session.get(('https://www.mtgstocks.com' + deck))
        pagetext=''
        attempt_count = 0
        while 'Mainboard' not in pagetext:
            attempt_count+=1
            print('\r'+'Attempting to fetch '+ deck +'. Try #'+str(attempt_count)   )
            deck_site.html.render(timeout=300)
            pagetext = deck_site.html.text
        deck_site.close()

        write_flag= False
        outdeck=''
        sideboard_count = -1
        words_to_skip = ['Creature','Instant','Sorcery','Enchantment','Land','Artifact','Planeswalker','Other']
        for line in pagetext.splitlines():
            if line in words_to_skip:
                continue
            if 'Mainboard (' in line:
                write_flag=True
                continue
            if 'Sideboard (' in line:
                sideboard_count = int(re.search('\d+',line).group())
                outdeck += 'sideboard\n'
                continue
            if write_flag == True:
                if sideboard_count > 0:    
                    sideboard_count -= int(re.search('\d+',line).group())
                outdeck += line+'\n'
                if sideboard_count == 0:
                    break
        
        out_name = pagetext.splitlines()[0][0:-12] + '.txt'
        f = open('decks/'+out_name, 'w')
        f.write(outdeck)
        f.close
        
    print('Finished fetching decks!')
    session.close()
    sys.exit(1)
        

if __name__ == '__main__':
    main()