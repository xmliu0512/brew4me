import sys 
import requests_html
import re

def main():
    session = requests_html.HTMLSession()
    print('What kind of decks would you like to download?\n'
          '1 - Legacy\n'
          '2 - Vintage\n'
          '3 - Modern\n'
          '4 - Pioneer\n' 
          '5 - Standard\n'
          '6 - Pauper\n'
          'Please enter the number of the format you wish to download.')
    format = input()
    format_to_num = {'1':1,'2':2,'3':3,'4':15,'5':4,'6':7}
    format_to_str = {'1':'Legacy','2':'Vintage','3':'Modern','4':'Pioneer','5':'Standard','6':'Pauper'}
    print('Downloading '+ format_to_str[format] +' decks...')
    mtgsite = session.get('https://www.mtgstocks.com/formats/' + str(format_to_num[format])) #, context=ssl.create_default_context(cafile=certifi.where())
    
    archetype_list = []               
    while not archetype_list:
        mtgsite.html.render(timeout=300)
        for link in mtgsite.html.links:
            if 'archetypes' in link:
                archetype_list.append(link) 
    mtgsite.close()
    print('Found ' + str (len(archetype_list))+' Decks!')

    progress_count = 0
    for archetype in archetype_list:
        progress_count += 1
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
            print('\r'+'Attempting to fetch deck # '+str(progress_count)+'/'+ str(len(archetype_list)) +'. Try #'+str(attempt_count) , end = ''  )
            deck_site.html.render(timeout=300)
            pagetext = deck_site.html.text
        deck_site.close()

        write_flag= False
        outdeck=''
        deck_count = -1
        words_to_skip = ['Creature','Instant','Sorcery','Enchantment','Land','Artifact','Planeswalker','Other']
        for line in pagetext.splitlines():
            
            if 'Mainboard (' in line:
                write_flag=True
                deck_count = int(re.search('\d+',line).group())
                continue
            if 'Sideboard (' in line:
                write_flag=True
                deck_count = int(re.search('\d+',line).group())
                outdeck += 'sideboard\n'
                continue
            if write_flag == True:
                if line in words_to_skip:
                    continue
                if deck_count > 0:    
                    deck_count -= int(re.search('\d+',line).group())
                outdeck += line+'\n'
                if deck_count == 0:
                    write_flag = False
        
        out_name = pagetext.splitlines()[0][0:-12] + '.txt'
        f = open('decks/'+out_name, 'w')
        f.write(outdeck)
        f.close
        
    print('\nFinished fetching decks!')
    session.close()
    sys.exit(1)
        

if __name__ == '__main__':
    main()