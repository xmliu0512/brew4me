from configparser import NoOptionError
from fileinput import close
from operator import truediv
import struct
import sys 
import statistics
import os
import csv
from telnetlib import NOOPT

class deck:
    
    def __init__(self,deck_dir,deck_file):
        self.name = deck_file[:-4]
        self.mainboard = []
        self.has_sideboard = False
        self.sideboard = []
        self.set_deck_from_dir (deck_dir+deck_file)

    def get_mainboard (self):
        return self.mainboard

    def set_deck_from_dir  (self,deck_dir):
        f = open(deck_dir, 'r')
        count = 0
        result = []
        while True:
            count += 1
            line = f.readline()
            if not line:
                break
            cur= line.split()
            if (cur[0] == "sideboard"):
                self.has_sideboard = True
                continue
            if (int(cur[0])):
                if (self.has_sideboard == True):
                    self.sideboard.append([ cur[0], " ".join(cur[1:]) ])
                else:
                    self.mainboard.append([cur[0]," ".join(cur[1:])])
            else:
                if (self.has_sideboard == True):
                    self.sideboard.append([cur[0]," ".join(cur[1:])])
                else:
                    self.mainboard.append([1," ".join(cur)])
        
        f.close()
        return result

    def get_sideboard (self,file_dir):
        f = open(file_dir)

        f.close()

class collection:
    cards = []

    def __init__(self,collection_dir):
        self.get_collection(collection_dir)
        self.cards = self.cards [1:]
        self.remove_duplicates()
        
    def remove_duplicates (self):
        count = 0
        while (count < (len(self.cards)-1) ):
            try:
                if self.cards[count][1] == self.cards[count+1][1] :
                    self.cards[count][0] = str( 
                        int(self.cards[count][0]) +
                        int(self.cards[count+1][0])
                        )
                    self.cards.pop(count+1)
                else:
                    count += 1  
            except:
                count += 1 
            
    def get_collection (self,file_dir):
        with open(file_dir, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    self.cards.append([row[0],row[2]])
                except:
                    continue

def compare_deck_to_collection (collection,deck):
    result = []
    for i in deck.mainboard:
        result.append(["0"]+i)
        for j in collection.cards:
            if i[1] == j[1]:
                result[-1][0] = j[0]
    return result


      
def main():

    file_dir = os.path.dirname(os.path.realpath(__file__))
    print (file_dir)
    deck_dir = file_dir + "\\decks\\"
    collection_dir = file_dir + "\\collection\\"
    deck_file_list = os.listdir(deck_dir)
    collection_file = os.listdir(collection_dir)

    my_collection = collection (collection_dir+collection_file[0])
    deck_list = []
    for deck_file in deck_file_list:
        temp_deck = deck(deck_dir,deck_file)
        deck_list.append(temp_deck)
    results = []
    for i in deck_list:
        results.append([i.name,compare_deck_to_collection(my_collection,i)])
    for i in results :
        have_cards = 0
        total_cards = 0
        for j in i[1] :

            if (j[2] == "Plains"
                or j[2] == "Island"
                or j[2] == "Swamp"
                or j[2] == "Mountain"
                or j[2] == "Forest"
            ):
                pass
            else:
                total_cards += float(j[1])
                if j[0] >= j[1] :
                    have_cards += float(j[1])
                else:
                    have_cards += float(j[0])
        i.append(have_cards/total_cards)   
    results = sorted(results, key=lambda x: x[-1])
    for i in results :     
        print ("\n================================\n")
        print ("Deck: "+i[0]+"\nCompletion rate (Not counting basic lands): " +str(i[-1]*100)+"%\n")
        for j in i[1]:
            print(j[0]+" | "+j[1]+" | "+j[2])
    input("Press Enter to exit")
    sys.exit(1)
        

if __name__ == '__main__':
    main()