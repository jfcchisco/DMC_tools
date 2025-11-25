# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 12:59:51 2023

@author: CHJ2LIZ
"""

import json
import numpy as np
import csv


def parseJson(jsonFile):
    with open(jsonFile) as f:
        d = json.load(f)
    print('Loaded:', jsonFile)
    return d


def getDMCData(letter, codes):
    for code in codes:
        if code['code'] == letter:
            return code
    return None


def getCodeFromLetter(letter, textCodes):
    for textCode in textCodes:
        if(letter == textCode['letter']):
            return textCode['code']
    print(letter)
    return None


def obj_dict(obj):
    return obj.__dict__


def main():
    dmcCodes = parseJson('dmc_codes.json')

    stitches = []
    textCodes = [
        {"letter": "0", "code": "943", "char": "\u0030"},
        {"letter": "1", "code": "552", "char": "\u0031"},
        {"letter": "2", "code": "310", "char": "\u0032"},
        {"letter": "3", "code": "803", "char": "\u0033"},
        {"letter": "4", "code": "334", "char": "\u0034"},
        {"letter": "5", "code": "3863", "char": "\u0035"},
        {"letter": "6", "code": "353", "char": "\u0036"},
        {"letter": "7", "code": "826", "char": "\u0037"},
        {"letter": "8", "code": "3752", "char": "\u0038"},
        {"letter": "9", "code": "3072", "char": "\u0039"},
        {"letter": "A", "code": "791", "char": "\u0041"},
        {"letter": "B", "code": "3799", "char": "\u0042"},
        {"letter": "C", "code": "369", "char": "\u0043"},
        {"letter": "D", "code": "517", "char": "\u0044"},
        {"letter": "E", "code": "800", "char": "\u0045"},
        {"letter": "F", "code": "3787", "char": "\u0046"},
        {"letter": "G", "code": "794", "char": "\u0047"},
        {"letter": "H", "code": "3078", "char": "\u0048"},
        {"letter": "I", "code": "966", "char": "\u0049"},
        {"letter": "J", "code": "954", "char": "\u004A"},
        {"letter": "K", "code": "3765", "char": "\u004B"},
        {"letter": "L", "code": "155", "char": "\u004C"},
        {"letter": "M", "code": "3825", "char": "\u004D"},
        {"letter": "N", "code": "317", "char": "\u004E"},
        {"letter": "O", "code": "453", "char": "\u004F"},
        {"letter": "P", "code": "3371", "char": "\u0050"},
        {"letter": "Q", "code": "612", "char": "\u0051"},
        {"letter": "R", "code": "519", "char": "\u0052"},
        {"letter": "S", "code": "939", "char": "\u0053"},
        {"letter": "T", "code": "3042", "char": "\u0054"},
        {"letter": "U", "code": "924", "char": "\u0055"},
        {"letter": "V", "code": "160", "char": "\u0056"},
        {"letter": "W", "code": "931", "char": "\u0057"},
        {"letter": "X", "code": "553", "char": "\u0058"},
        {"letter": "Y", "code": "564", "char": "\u0059"},
        {"letter": "Z", "code": "161", "char": "\u005A"},
        {"letter": "a", "code": "932", "char": "\u0061"},
        {"letter": "b", "code": "311", "char": "\u0062"},
        {"letter": "c", "code": "208", "char": "\u0063"},
        {"letter": "d", "code": "327", "char": "\u0064"},
        {"letter": "e", "code": "772", "char": "\u0065"},
        {"letter": "f", "code": "500", "char": "\u0066"},
        {"letter": "g", "code": "209", "char": "\u0067"},
        {"letter": "h", "code": "840", "char": "\u0068"},
        {"letter": "i", "code": "921", "char": "\u0069"},
        {"letter": "j", "code": "955", "char": "\u006A"},
        {"letter": "k", "code": "3750", "char": "\u006B"},
        {"letter": "l", "code": "3023", "char": "\u006C"},
        {"letter": "m", "code": "3808", "char": "\u006D"},
        {"letter": "n", "code": "948", "char": "\u006E"},
        {"letter": "o", "code": "3024", "char": "\u006F"},
        {"letter": "p", "code": "640", "char": "\u0070"},
        {"letter": "q", "code": "413", "char": "\u0071"},
        {"letter": "r", "code": "3746", "char": "\u0072"},
        {"letter": "s", "code": "3779", "char": "\u0073"},
        {"letter": "t", "code": "825", "char": "\u0074"},
        {"letter": "u", "code": "3760", "char": "\u0075"},
        {"letter": "v", "code": "3847", "char": "\u0076"},
        {"letter": "w", "code": "158", "char": "\u0077"},
        {"letter": "x", "code": "3790", "char": "\u0078"},
        {"letter": "y", "code": "597", "char": "\u0079"},
        {"letter": "z", "code": "169", "char": "\u007A"},
        {"letter": "#", "code": "434", "char": "\u007B"},
        {"letter": "$", "code": "958", "char": "\u007C"},
        {"letter": "%", "code": "779", "char": "\u007D"},
        {"letter": "&", "code": "823", "char": "\u007E"},
        {"letter": "'", "code": "3846", "char": "\u0021"},
        {"letter": "(", "code": "3713", "char": "\u0022"},
        {"letter": ")", "code": "3727", "char": "\u0023"},
        {"letter": "*", "code": "3031", "char": "\u0024"},
        {"letter": "+", "code": "3864", "char": "\u0025"},
        {"letter": ",", "code": "913", "char": "\u0026"},
        {"letter": "-", "code": "809", "char": "\u0027"},
        {"letter": ".", "code": "959", "char": "\u0028"},
        {"letter": "/", "code": "820", "char": "\u0029"},
        {"letter": "¡", "code": "159", "char": "\u002A"},
        {"letter": "¢", "code": "333", "char": "\u002B"},
        {"letter": "£", "code": "436", "char": "\u002C"},
        {"letter": "¤", "code": "501", "char": "\u002D"},
        {"letter": "¥", "code": "598", "char": "\u002E"},
        {"letter": "¦", "code": "3766", "char": "\u002F"},
        {"letter": "§", "code": "613", "char": "\u003A"},
        {"letter": "α", "code": "793", "char": "\u003B"},
        {"letter": "β", "code": "799", "char": "\u003C"},
        {"letter": "γ", "code": "807", "char": "\u003D"},
        {"letter": "δ", "code": "828", "char": "\u003E"},
        {"letter": "ε", "code": "964", "char": "\u003F"},
        {"letter": "ζ", "code": "3768", "char": "\u00A1"},
        {"letter": "η", "code": "3810", "char": "\u00A2"},
        {"letter": "θ", "code": "3812", "char": "\u00A3"},
        {"letter": "ú", "code": "3814", "char": "\u00A4"},
        {"letter": "ó", "code": "3816", "char": "\u00A5"},
        {"letter": ":", "code": "3835", "char": "\u00A6"},
        {"letter": "á", "code": "3842", "char": "\u00A7"},
        {"letter": "é", "code": "3844", "char": "\u00A8"},
        {"letter": "í", "code": "3851", "char": "\u00A9"},
        {"letter": "@", "code": "3861", "char": "\u0040"},
    ]

    # with open('stitches.txt', 'r') as f:
    #    lines = [line.rstrip() for line in f]

    #with open('C:/Users/chj2liz/Documents/Python/dino.csv') as f:
    #    reader = csv.reader(f)
    #    data = list(reader)

    with open('C:/Users/chj2liz/Documents/Python/AutoDMC/northern/pdfText.txt', 'r', encoding="utf8") as file:
    # Read each line in the file
        y = 0
        for line in file:
            # Print each line
            # print(line.strip())
            x = 0
            for char in line.strip():
                print(char)
                stitches.append(
                    {
                        "X": x, "Y": y,
                        "dmcCode": getCodeFromLetter(char, textCodes)
                    }
                )
                x += 1
            y += 1

    json_string = json.dumps(stitches, default=obj_dict)
    with open('out2.json', 'w') as jsonFile:
        jsonFile.write(json_string)

    colors = []
    
    # Adding STITCHED
    colors.append(
    {
        "dmcCode": "stitched",
        "dmcName": "STITCHED",
        "R": 0,
        "G": 255,
        "B": 0,
        "symbol": "\u00D7",
    }
    )
    
    
    for color in textCodes:
        dmcData = getDMCData(color['code'], dmcCodes)
        colors.append(
            {
                "dmcCode": dmcData['code'],
                "dmcName": dmcData['name'],
                "R": dmcData['R'],
                "G": dmcData['G'],
                "B": dmcData['B'],
                "symbol": color['char']
            }
            )
    
    json_string = json.dumps(colors, default=obj_dict)
    with open('colors.json', 'w') as jsonFile:
        jsonFile.write(json_string)

  

# =============================================================================
#     print(data[0][0])
#     for line in data:
#         x = 0
#         for char in data[y][0].split(';'):
#             if(char != '.'):
#                 #charData = getDMCData(
#                 #    getCodeFromLetter(char, textCodes),
#                 #    dmcCodes)
#                 stitches.append(
#                     {
#                         "X": x, "Y": y,
#                         "dmcCode": getCodeFromLetter(char, textCodes)
#                     }
#                 )
#             else:
#                 stitches.append(
#                     {
#                         "X": x, "Y": y,
#                         "dmcCode": "empty",
#                     }
#                 )
#             x += 1
# 
#         y += 1
# =============================================================================
    # y = 0
    # for line in lines:
    #     x = 0
    #     for char in line:
    #         if(char != '.'):
    #             charData = getDMCData(
    #                 getCodeFromLetter(char, textCodes),
    #                 dmcCodes)
    #             stitches.append(
    #                 {
    #                     "X": x, "Y": y,
    #                     "dmcCode": charData['code'],
    #                     "dmcName": charData['name'],
    #                     "R": charData['R'],
    #                     "G": charData['G'],
    #                     "B": charData['B'],
    #                     "symbol": char
    #                 }
    #             )
    #         else:
    #             stitches.append(
    #                 {
    #                     "X": x, "Y": y,
    #                     "dmcCode": "0",
    #                     "dmcName": "EMPTY",
    #                     "R": 255,
    #                     "G": 255,
    #                     "B": 255,
    #                     "symbol": ""
    #                 }
    #             )
    #         x += 1

    #     y += 1

    


if __name__ == '__main__':
    main()
