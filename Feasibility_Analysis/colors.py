# -*- coding: utf-8, -*-
"""
Created on Mon Mar  3, 08:58:32, 2025

@author: Alanis Zeoli

Objective: Create a dictionnary containing the most used colors
"""

def normalize_color(rgb):
    return tuple(value/255 for value in rgb)

def main():
    main = {
        # Blue
        'lightblue': normalize_color((196, 233, 238)),
        'blue': normalize_color((114, 203, 215)),
        'teal': normalize_color((46, 150, 164)),
        'darkblue': normalize_color((34, 112, 123)),
        'ruddyblue': normalize_color((121,173,220)),
    
        # Green
        'green': normalize_color((166, 183, 39)),
        'darkgreen': normalize_color((125, 137, 29)),
        'verydarkgreen': normalize_color((83, 92, 19)),
        'lightgreen': normalize_color((204, 219, 87)),
        'verylightgreen': normalize_color((224, 233, 155)),
    
        # Red
        'darkred': normalize_color((128, 10, 18)),
        'red': normalize_color((200, 80, 80)),
        'lightred': normalize_color((255, 127, 127)),
        'verylightred': normalize_color((255, 200, 200)),
    
        # Orange
        'orange': normalize_color((245, 158, 0)),
        'oranger': normalize_color((242, 139, 24)),
        'darkbrown': normalize_color((123, 79, 0)),
        'coral': normalize_color((244, 134, 104)),
        'lightcoral': normalize_color((221, 115, 115)),
        'melon': normalize_color((244, 166, 152)),
        'lightorange': normalize_color((245, 166, 91)),
    
        'lightsalmon': normalize_color((247, 185, 129)),
        'orangesalmon': normalize_color((244, 155, 74)),
        'darkorange': normalize_color((236, 120, 14)),
        'verydarkorange': normalize_color((215, 105, 15)),
    
        # Yellow
        'yellow': normalize_color((254, 195, 6)),
    
        # Pink
        'fushia': normalize_color((232, 74, 145)),
        'lightfushia': normalize_color((237, 115, 170)),
        'pink': normalize_color((244, 166, 201)),
        'lightpink': normalize_color((247, 182, 210)),
        'darkpink': normalize_color((141, 17, 73)),
        'verydarkpink': normalize_color((91, 11, 47)),
        'amaranth': normalize_color((182, 23, 94)),
    
        # Purple
        'purple': normalize_color((195, 139, 213)),
    
        # Grey
        'lightgreyblue': normalize_color((192, 206, 214)),
        'greyblue': normalize_color((69, 91, 105)),
        'grey': normalize_color((0.7, 0.7, 0.7)),
        'darkgrey': normalize_color((0.3, 0.3, 0.3)),
        'black': normalize_color((0, 0, 0))
    }

    # ULiege color palette
    ULg = {
        'red': normalize_color((230, 39, 54)),
        'orange': normalize_color((238, 129, 62)),
        'ocre': normalize_color((247, 172, 18)),
        'yellow': normalize_color((254, 209, 22)),
        'lightgreen': normalize_color((186, 205, 116)),
        'green': normalize_color((127, 182, 28)),
        'grassgreen': normalize_color((43, 152, 45)),
        'darkgreen': normalize_color((5, 130, 52)),
        'blue': normalize_color((34, 185, 214)),
        'darkblue': normalize_color((16, 94, 168)),
        'lightteal': normalize_color((97, 166, 173)),
        'teal': normalize_color((10, 112, 124)),
        'lightpurple': normalize_color((139, 166, 209)),
        'purple': normalize_color((88, 88, 160)),
        'lila': normalize_color((165, 89, 154)),
        'darklila': normalize_color((84, 36, 120))
    }

    # Climate zones
    climate = {
        'Singapore': main['black'],
        'Abu_Dhabi': main['grey'],
        'Guayaquil': normalize_color((189, 103, 171)),
        'Sao_Paulo': normalize_color((240, 62, 62)),
        'Buenos_Aires': normalize_color((239, 122, 57)),
        'Los_Angeles': normalize_color((248, 165, 124)),
        'Brussels': normalize_color((241, 238, 101)),
        'Vancouver': normalize_color((255, 230, 153)),
        'Copenhaguen': normalize_color((129, 198, 90)),
        'Montreal': normalize_color((92, 114, 196))
    }

    # Basic Excel colors
    excel = {
        'grey': normalize_color((183, 183, 183)),
        'darkblue': normalize_color((38, 68, 120)),
        'blue': normalize_color((105, 142, 208)),
        'lightblue': normalize_color((124, 175, 221)),
        'yellow': normalize_color((255, 205, 51)),
        'orange': normalize_color((233, 113, 50)),
        'red': normalize_color((255, 0, 0))
    }
    
    colors = {
        'main': main,
        'ULg': ULg,
        'climate': climate,
        'excel': excel
        }
    
    return colors