#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict
from datetime import datetime
import numpy

from fmqlutils.cacher.cacherUtils import FilteredResultIterator, SCHEMA_LOCN_TEMPL 
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

from ..webReportUtils import SITE_DIR_TEMPL, TOP_MD_TEMPL, ensureRequiredData, keyStats, roundFloat

"""
Overview of Data available in system AND what data is used for the subreports AND
national vs local data.

TODO:
- TYPES_USED_BY_SUBREPORT as part of stand alone and 'as data so far supports' reports
- national vs local 
- deprecated vs (REM: use that in Images ... want to know along with EMPTY)
- details on singletons as many are key configs like kernel sys params
- BRING IN CLIN vs ... (P Slice) ...
- consider per day/month graph for key types: ORDERS, DOCs, IMAGEs etc
"""
def webReportData(stationNo):

    def expectedTypeCounts(stationNo):
        try:
            selectTypes = json.load(open(SCHEMA_LOCN_TEMPL.format(stationNo) + "SELECT_TYPES.json"))
        except:
            raise Exception("Can't load SELECT_TYPE.json from {}".format(SCHEMA_LOCN_TEMPL.format(stationNo)))
        expectedCountByType = {}
        ranks = set()
        cnts = []
        for result in selectTypes["results"]:
            if "parent" in result:
                continue
            typ = re.sub(r'\.', '_', result["number"])
            if "count" not in result:
                cnt = 0
            elif re.search(r'\-', result["count"]):
                cnt = -1
            else:
                cnt = int(result["count"]) 
                cnts.append(cnt)
            if cnt not in ranks:
                ranks.add(cnt)
            expectedCountByType[typ] = {"label": result["name"], "count": cnt}
        ranks = sorted(list(ranks), reverse=True)
        percentileThress = []
        for ptile in range(90, 0, -10):
            thres = numpy.percentile(cnts, ptile)
            percentileThress.append((int(thres), ptile))
        for typ in expectedCountByType:
            if expectedCountByType[typ]["count"] == -1:
                continue
            expectedCountByType[typ]["rank"] = ranks.index(expectedCountByType[typ]["count"]) + 1
            if expectedCountByType[typ]["count"] == 0:
                continue
            for percThres in percentileThress:
                if expectedCountByType[typ]["count"] >= percThres[0]:
                    expectedCountByType[typ]["sizePercentile"] = percThres[1]
                    break
        return expectedCountByType
    typeInfoById = expectedTypeCounts(stationNo)

    title = "{} Data Types and Sizes".format(stationNo)
    mu = TOP_MD_TEMPL.format("Data Types and Sizes", title)
    
    mu += webReportSummary(stationNo, typeInfoById) + "\n\n"
    mu += webReportLocalNationalData(stationNo, typeInfoById) + "\n\n"

    # IMPORTANT: need to replace with types just from here or if types so far passed in then types as caller invokes
    # TYPES_USED_BY_SUBREPORT = json.load(open("subReportInfo.json")) # allows for new place for this
    # mu += webReportSubReportDataUsed(stationNo, typeInfoById, TYPES_USED_BY_SUBREPORT) + "\n\n"
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    if not os.path.isdir(userSiteDir):
        raise Exception("Expect User Site to already exist with its basic contents")
    open(userSiteDir + "dataTypes.md", "w").write(mu)

"""
Number, empty, sizes

TODO: last entry stuff to see if retired
"""
def webReportSummary(stationNo, typeInfoById):
        
    noEmptyTypes = sum(1 for typId in typeInfoById if typeInfoById[typId]["count"] == 0)
    # untrack is -1
    noUntrackedTypes = sum(1 for typId in typeInfoById if typeInfoById[typId]["count"] == -1)
    noRecords = sum(typeInfoById[typId]["count"] for typId in typeInfoById)
    
    cnts = [typeInfoById[typId]["count"] for typId in typeInfoById if typeInfoById[typId]["count"] > 1]
    singletonCnts = sum(1 for typId in typeInfoById if typeInfoById[typId]["count"] == 1)
    kstats = keyStats(cnts)
    median = roundFloat(kstats["median"])
    recordCntBiggest = sorted(cnts, reverse=True)[0]
    
    mu = "The system reports <span class='yellowIt'>{:,}</span> types of data (\"File Types\"), <span class='yellowIt'>{}</span> of which are singletons (have only one record), <span class='yellowIt'>{}</span> are empty and <span class='yellowIt'>{:,}</span> are untracked. The system has a total of <span class='yellowIt'>{:,}</span> records. While the biggest type has <span class='yellowIt'>{:,}</span> records, the median number of records for types with more than one record is a lowly <span class='yellowIt'>{:,}</span>.\n\n".format(len(typeInfoById), reportAbsAndPercent(singletonCnts, len(typeInfoById)), reportAbsAndPercent(noEmptyTypes, len(typeInfoById)), noUntrackedTypes, noRecords, recordCntBiggest, median)
    
    mu += "The top 15 types are a mixture of patient record and system log and configuration data ...\n\n"
    
    tbl = MarkdownTable(["Rank", "Type", "Records", "Share"], includeNo=False)
    for i, typId in enumerate(sorted(typeInfoById, key=lambda x: typeInfoById[x]["count"], reverse=True), 1):
        fid = re.sub(r'\_', '.', typId)
        cntMU = typeInfoById[typId]["count"] if typeInfoById[typId]["count"] != -1 else "UNTRACKED"
        percMU = reportPercent(typeInfoById[typId]["count"], noRecords) if typeInfoById[typId]["count"] > 0 else ""
        tbl.addRow([typeInfoById[typId]["rank"], "__{}__ ({})".format(typeInfoById[typId]["label"], fid), cntMU, percMU])
        if i == 15:
            break
    mu += tbl.md() + "\n\n"
    
    return mu
    
"""
National vs Local

... see nationalVsLocal .py old file in there
"""
def webReportLocalNationalData(stationNo, typeInfoById):
    return ""

"""
Drives off subReportInfo and its manifest of the types required by each subreport
"""
def webReportSubReportDataUsed(stationNo, typeInfoById, subReportInfo):
                
    # Reorganize
    labelByTypId = {}
    subReportsByTypId = defaultdict(list)
    for metaInfo in subReportInfo:
        title = metaInfo["title"]
        for typInfo in metaInfo["types"]:
            labelByTypId[typInfo["id"]] = typInfo["label"]
            subReportsByTypId[typInfo["id"]].append((title, typInfo["scope"]))
    
    mu = "## Data Types used for this Report\n\n"
    mu += "<span class='yellowIt'>{:,}</span> types of data are used in the following sections of this report ...\n\n".format(len(labelByTypId))
    
    tbl = MarkdownTable(["Rank", "Type", "Records", "Section"], includeNo=False)
    for typId in sorted(labelByTypId, key=lambda x: typeInfoById[re.sub(r'\.', '_', x)]["rank"]):
        typeInfo = typeInfoById[re.sub(r'\.', '_', typId)]
        tbl.addRow([typeInfo["rank"], "__{}__ ({})".format(labelByTypId[typId], typId), typeInfo["count"], ", ".join(["__{}__ ({})".format(sr[0], sr[1]) for sr in subReportsByTypId[typId]])]) 
    mu += tbl.md() + "\n\n"
    
    mu += "where _ALL_ means all of the records of a type are used while _SO_ means only those records created during the period for which sign on logs exist are examined.\n\n"
    
    mu += "As the report expands more types of data will be examined.\n\n"
    
    return mu

# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]

    webReportData(stationNo)
                 
if __name__ == "__main__":
    main()
