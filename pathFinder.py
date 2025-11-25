# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 12:44:48 2025

@author: CHJ2LIZ
"""

import json
import math
import pathlib
import tkinter as tk

from PIL import Image, ImageDraw
from tkinter import filedialog


class jsonObject:
    def __init__(self, properties, stitches, colors):
        self.properties = properties
        self.stitches = stitches
        self.colors = colors


class properties:
    def __init__(self, width, height):
        self.height = height
        self.width = width


class stitchObj:
    def __init__(self, x, y, code, cluster):
        self.x = x
        self.y = y
        self.code = code
        self.cluster = cluster


class coordObj:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def parseJson(jsonFile):
    with open(jsonFile) as f:
        d = json.load(f)
    print('Loaded: ', jsonFile)
    return d


def fileToStitches(objStr, width, height):
    s2return = []
    stitches = objStr['stitches'].split(',')
    lastID = 0
    for stitch in stitches:
        currID = int(stitch.split('-')[0])
        currCode = stitch.split('-')[1]
        while(lastID <= currID):
            x = lastID % width
            y = math.floor(lastID / width)
            s2return.append(stitchObj(x, y, currCode, 0))
            lastID += 1

    return s2return


def getNeighbors(x, y, code):
    # print("Point: ", x, y, code)
    foundStitches = []
    newStitches = []
    color2paint = code

    if(color2paint == 'stitched' or color2paint == '0'):
        return foundStitches

    newStitches.append(coordObj(x, y))
    foundStitches.append(coordObj(x, y))

    while(len(newStitches) > 0):
        stitch2Test = newStitches[len(newStitches) - 1]
        newStitches.pop()
        edges = []
        if(stitch2Test.y > 0):
            edges.append(coordObj(stitch2Test.x, stitch2Test.y - 1))
        if(stitch2Test.y < (height - 1)):
            edges.append(coordObj(stitch2Test.x, stitch2Test.y + 1))
        if(stitch2Test.x > 0):
            edges.append(coordObj(stitch2Test.x - 1, stitch2Test.y))
        if(stitch2Test.x < (width - 1)):
            edges.append(coordObj(stitch2Test.x + 1, stitch2Test.y))

        for edge in edges:
            if(getStitchColor(edge) == color2paint):
                if(not isCoordAlreadyThere(edge, foundStitches)):
                    newStitches.append(edge)
                    foundStitches.append(edge)
    return foundStitches


def getStitchColor(stitchCoord):
    return(stitchesList[stitchCoord.x + stitchCoord.y * width].code)


def isCoordAlreadyThere(stitchCoord, list2Test):
    ret = False
    for stitch in list2Test:
        if(stitch.x == stitchCoord.x and stitch.y == stitchCoord.y):
            ret = True
    return ret


def getColorsFromStitchList():
    colors = []
    for stitch in stitchesList:
        if(stitch.code not in colors and
           stitch.code != "empty" and
           stitch.code != "stitched"):
            colors.append(stitch.code)
    return colors


def getLastCluster():
    lastCluster = 0
    for stitch in stitchesList:
        if(stitch.cluster > lastCluster):
            lastCluster = stitch.cluster
    return lastCluster


def getClusterList():
    lastCluster = getLastCluster()
    clusterList = [[0, "0"] for _ in range(lastCluster + 1)]
    for stitch in stitchesList:
        # print(clusterList[stitch.cluster])
        clusterList[stitch.cluster][0] = clusterList[stitch.cluster][0] + 1
        clusterList[stitch.cluster][1] = stitch.code
    return clusterList


def getClusterNumberListForColor(color):
    clusterNumbers = []
    for stitch in stitchesList:
        if(stitch.code == color and stitch.cluster not in clusterNumbers):
            clusterNumbers.append(stitch.cluster)
    return clusterNumbers


def getDistBetweenClusters(c1, c2, sList):
    retVal = [0, [0, 0], [0, 0]]
    # Compare all point in c1 to all points in c2 and keep minimum
    dist = float('inf')
    for s1 in sList:
        if(s1.cluster == c1):
            for s2 in sList:
                if(s2.cluster == c2):
                    newDist = math.sqrt(
                        (s1.x - s2.x) ** 2 + (s1.y - s2.y) ** 2)
                    if(newDist < dist):
                        dist = newDist
                        retVal = [c1, c2, dist, [s1.x, s1.y], [s2.x, s2.y]]
    return retVal


def removeCodeFromList(code):
    for stitch in stitchesList:
        if(stitch.code == code):
            stitchesList.remove(stitch)


def extractCodeFromList(code):
    retList = []
    for stitch in stitchesList:
        if(stitch.code == code):
            retList.append(stitch)
    return retList


def getClosestClusterToCenter(code):
    closestCluster = 0
    closestDistance = float('inf')
    for s in stitchesList:
        if(s.code == code):
            dist2Center = math.sqrt(
                (s.x - width/2) ** 2 + (s.y - height/2) ** 2)
            if(dist2Center < closestDistance):
                closestDistance = dist2Center
                closestCluster = s.cluster
    # print(closestCluster, closestDistance)
    return closestCluster


def getLargerCluster(code):
    largerCluster = 0
    largerClusterCount = 0
    sList = extractCodeFromList(code)
    cList = getClusterNumberListForColor(code)
    for c in cList:
        sCount = 0
        for s in sList:
            if(s.cluster == c):
                sCount += 1
        if(sCount > largerClusterCount):
            largerClusterCount = sCount
            largerCluster = c
    print(f"Code: {code}, Larger cluster: {largerCluster}")


def main():
    root = tk.Tk()
    root.withdraw()
    global stitchesList, width, height
    jsonFile = parseJson(pathlib.Path(filedialog.askopenfilename()))

    width = int(jsonFile['properties']['width'])
    height = int(jsonFile['properties']['height'])
    stitchesList = fileToStitches(jsonFile, width, height)

    TH = 20
    # Set output image properties
    SIZE = 10
    imageW = width * SIZE
    imageH = height * SIZE

    # Go through all stitches, find neighbors and assign clusters
    clusterCounter = 0
    for stitch in stitchesList:
        if(stitch.cluster != 0 or stitch.code == 'stitched' or stitch.code == 'empty'):
            continue
        clusterCounter += 1
        neighbors = getNeighbors(stitch.x, stitch.y, stitch.code)
        for neighbor in neighbors:
            stitchesList[neighbor.x + neighbor.y *
                         width].cluster = clusterCounter

    clusterList = getClusterList()
    sortedClusterList = sorted(clusterList, key=lambda x: x[0], reverse=True)
    print("CLUSTER PRIORITY")
    for elem in sortedClusterList[0:19]:
        print(elem[1], " - ", elem[0])

    usageIndexList = []
    for color in getColorsFromStitchList():
        print("COLOR: ", color)
        colorClusters = getClusterNumberListForColor(color)
        colorList = extractCodeFromList(color)
        # Initial cluseter the first for now
        # print(colorClusters)
        clusterSequence = []
        # nextCluster = colorClusters[0]
        nextCluster = getClosestClusterToCenter(color)
        getLargerCluster(color)
        while(len(colorClusters) > 0):
            # colorClusters.remove(nextCluster)
            # print("colorClusters", colorClusters)
            # print("clusterSequence")
            # for seq in clusterSequence:
            #     print(seq)
            dist2Next = [nextCluster, 0, float('inf'), [-1, -1], [-1, -1]]
            for cluster in colorClusters:
                dist2Cluster = getDistBetweenClusters(
                    nextCluster, cluster, colorList)
                if(dist2Cluster[2] < dist2Next[2]):
                    dist2Next = dist2Cluster
                    closestCluster = cluster
                    # print(dist2Next)

            # If the distance is greater than TH, then we look for
            # a pair of consecutive clusters in the clusterSequence
            # whose summed distance to the next cluster is less than
            # the single distance to the previous one
            # (that doesn't sound right but whatever)
            # If there is a better option, then the clusterSequence
            # is split to put the next in the middle of the pair
            # If not then we proceed to append the next one and move on
            # No way I'll understand that later

            if(dist2Next[2] <= TH):
                clusterSequence.append(dist2Next)
                nextCluster = closestCluster
                colorClusters.remove(nextCluster)
            else:
                # Go through the clusterSequence and find the summed
                # distance to each pair
                # print("Found gap")
                newMinSum = dist2Next[2]
                betterOptionFlag = 0
                for cI, clusterS in enumerate(clusterSequence):
                    # print("clusterS, closestCluster", clusterS, closestCluster)
                    dist0 = getDistBetweenClusters(
                        clusterS[0], closestCluster, colorList)
                    dist1 = getDistBetweenClusters(
                        closestCluster, clusterS[1], colorList)
                    # print("dist0, dist1", dist0, dist1)
                    if(dist0[2] + dist1[2] < newMinSum):
                        # print("Better option found", dist0, dist1)
                        newSeq0 = dist0
                        newSeq1 = dist1
                        newMinSum = dist0[2] + dist1[2]
                        betterOptionFlag = 1
                        betterOptionIndex = cI

                if(betterOptionFlag):
                    # Look for the index where to split
                    # print("Better option: ", newSeq0, newSeq1, nextCluster)
                    newClusterSequence = []
                    # print("BEFORE")
                    for seq in clusterSequence[0:betterOptionIndex]:
                        # print(seq)
                        newClusterSequence.append(seq)
                    newClusterSequence.append(newSeq0)
                    newClusterSequence.append(newSeq1)
                    # print("AFTER")
                    for seq in clusterSequence[betterOptionIndex+1:(len(clusterSequence))]:
                        # print("seq2", seq)
                        newClusterSequence.append(seq)
                    clusterSequence = newClusterSequence
                    colorClusters.remove(closestCluster)

                    # clusterSequence = \
                    #     clusterSequence[0:betterOptionIndex] + \
                    #     [newSeq0] + [newSeq1] + \
                    #     clusterSequence[betterOptionIndex+1:-1]
                    # for seq in clusterSequence:
                    #     print(seq)
                else:
                    clusterSequence.append(dist2Next)
                    nextCluster = closestCluster
                    colorClusters.remove(nextCluster)
                betterOptionFlag = 0
            # print("colorClusters", colorClusters)
            # print("clusterSequence")
            # for seq in clusterSequence:
            #     print(seq)

        # print(color)
        # if(color == '310'):
        #     for seq in clusterSequence:
        #         print(seq)
        # Now that the cluster sequence is ready, draw the color image
        out = Image.new(mode="RGB", size=(imageW, imageH))
        rect = ImageDraw.Draw(out)
        rect.rectangle([(0, 0), (imageW, imageH)], fill="white")

        totalDistance = 0
        for i, step in enumerate(clusterSequence):
            totalDistance += step[2]
            # Draw squares of second cluster
            for stitch in colorList:
                if(stitch.cluster == step[1]):
                    shape = [(stitch.x * SIZE, stitch.y * SIZE),
                             ((stitch.x + 1) * SIZE, (stitch.y + 1) * SIZE)]
                    rect.rectangle(shape, fill="black")
                if(stitch.cluster == step[0] and i == 0):
                    shape = [(stitch.x * SIZE, stitch.y * SIZE),
                             ((stitch.x + 1) * SIZE, (stitch.y + 1) * SIZE)]
                    rect.rectangle(shape, fill="black")
            # If first draw both, for all others draw only second cluster
            # Draw lines
            shape = [(step[3][0] * SIZE, step[3][1] * SIZE),
                     (step[4][0] * SIZE, step[4][1] * SIZE)]
            if(step[2] <= TH):
                if(i < 2):
                    lineColor = "limegreen"
                elif(i % 2 == 0):
                    lineColor = "blue"
                else:
                    lineColor = "cyan"
                rect.line(shape, fill=lineColor, width=3)
            else:
                rect.line(shape, fill="red", width=3)
        # Draw middle lines
        shape = [(width * SIZE / 2, 0), (width * SIZE / 2, height * SIZE)]
        rect.line(shape, fill="gray", width=2)
        shape = [(0, height * SIZE / 2), (width * SIZE, height * SIZE / 2)]
        rect.line(shape, fill="gray", width=2)
        out = out.save(f"out/{color}.png", "PNG")
        # Calculate usage index
        totalStitches = len(colorList)
        totalDistance += totalStitches * 5.25
        usageIndex = totalDistance / (totalStitches * 5.25)
        # print(f"Usage index: {usageIndex:.3f}")
        usageIndexList.append([color, usageIndex, totalStitches])

    sortedIndexList = sorted(usageIndexList, key=lambda x: x[1])
    for indexElem in sortedIndexList:
        print(indexElem)
    # print(sortedClusterList)
    # print(sortedClusterList[0])
    # print(sortedClusterList[1])

    # print(getClusterNumberListForColor('820'))
    # print(getDistBetweenClusters(1, 3))
    # print(getDistBetweenClusters(1, 5))
    root.destroy()
    return 0


if __name__ == '__main__':
    main()
