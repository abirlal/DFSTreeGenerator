#!/usr/bin/python2.7 -u

############################################################
#
# Summary: Parser of flat tree structure output into a DFS Search Tree
# Author : Abirlal Biswas
# Date Created: 22.02.2018
# Last Modified: 22.02.2018
#
###########################################################

import os
import sys
import subprocess
import re

class DFSTree:
    ''' '''
    def __init__(self, isFile, txtLines='', filePath=''):
        self.fileName = filePath
        self.dataTree = []
        self.lastWorkingNode = 0
        self.lastWorkingLevel = -1
        self.lastAncestor = -1
        self.ancestors = []
        if isFile:
            if os.path.isfile(self.fileName):
                txtFile = open( self.fileName, 'r+' )
	        txtFileLines = txtFile.readlines()
	        self.readLines(txtFileLines)
            else:
	        print "No file found: " + self.fileName
        else:
            self.readLines(txtLines)
            
	
    def getTree(self):
	return self.dataTree
	
    def readLines(self, txtLines):
	for line in txtLines:
            line = line.strip('\n')
            lineVals = []
	    if ':' in line:
	        lineVals = line.split(":", 1)
                nodeName =  lineVals[0].strip()
                nodeVal = lineVals[1].strip()
                if len(nodeVal) > 0:
		    self.addNode( self.countLevel(line), True, nodeName, nodeVal )
                else:
                    self.addNode(self.countLevel(line), False, nodeName, nodeVal)
	    else:
	        pass
			
    def countLevel(self, lineString):
        nodeLevel = re.search('[^ ]', lineString).start()
	if nodeLevel == 0:
	    return nodeLevel
	else:
	    return nodeLevel/2
			
    def addNode(self, nodeLevel, isLeaf, nodeName, nodeVal):
        dList = {}
        #print (("\n Fetched Data : lastWorkingLevel: %d| Nodelevel : %d=> %s:%s ") % (self.lastWorkingLevel, nodeLevel, nodeName,nodeVal))
        if self.lastWorkingLevel < nodeLevel:
            self.lastAncestor = self.lastWorkingNode
            if self.lastAncestor > 0:
                self.ancestors.append(self.lastAncestor)
        elif self.lastWorkingLevel > nodeLevel:
            popCount = self.lastWorkingLevel - nodeLevel
            for i in range(0, popCount):
                self.ancestors.pop()
        else:
            pass
        self.lastWorkingNode += 1
        dList.update({"node":self.lastWorkingNode})
        dList.update({"isLeaf":isLeaf})
        dList.update({"label":nodeName})
        if isLeaf:
            dList.update({"value":nodeVal})
        self.lastWorkingLevel = nodeLevel
	dList.update({"ancestors":[]})
        for a in self.ancestors:
            dList["ancestors"].append(a)
        #print ("AFTER INSERT (List view)=> lastAncestor => %d | lastRootNode =>%d :" % (self.lastAncestor, self.lastWorkingLevel ))
        #print dList 
        self.dataTree.append(dList)

    def findNodesByLevel(self, nodeLevel):
        nodeLists = []
        for i, e in enumerate(self.dataTree):
            if len(e["ancestors"]) == nodeLevel:
                nodeLists.append(e['label'])
	return nodeLists

    def findLeafValByLevel(self, nodeLevel, mode = ''): # Mode 1=>list, 2=> associative array i.e. dictionary
        nodeLists = []
        for i, e in enumerate(self.dataTree):
            if len(e["ancestors"]) == nodeLevel:
                if mode == 'list':
                    if  e["isLeaf"]:
                         nodeLists.append(e["value"])
                else:
                    ndict = {}
                    if  e["isLeaf"]:
                        ndict.update({e['label']: e["value"]})
                        nodeLists.append(ndict)
	return nodeLists

    def findLeafByLevelAndLabel(self, nodeLevel, label): 
        nodeLists = []
        for i, e in enumerate(self.dataTree):
            if len(e["ancestors"]) == nodeLevel:
                if e['label'] == label:
                    if e["isLeaf"]:
                        nodeLists.append(e["value"])
	return nodeLists

    def findValByPath(self, pathList):
        k = 0
        maxLenth = len(pathList)
        ancestors = []
        lastNode = 0
        lastNodeLabel = ''
        lastNodeVal = None
        for i, e in enumerate(self.dataTree):
            if k == maxLenth:
                    break
            if e["label"] == pathList[k]:
                lastNode = e["node"]
                lastNodeLabel =  e["label"]
                if e["isLeaf"]:
                    lastNodeVal =  e["value"] 
                else:
                #ancestors.append(e["node"])
                    pass
                k += 1
        #print ancestors
        return lastNode, lastNodeLabel, lastNodeVal
   

