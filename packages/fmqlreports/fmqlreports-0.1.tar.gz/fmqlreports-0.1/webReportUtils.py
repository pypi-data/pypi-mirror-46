#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter

import numpy
import math

from fmqlutils.cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator

"""
Site
"""
SITE_DIR_TEMPL = "/data/vista/{}/ReportSite/" 

TOP_MD_TEMPL = """---
layout: default
title: {}
---

# {}

"""

def dtdd(dt, dd):
    return "{}\n:    {}\n\n".format(dt, dd)

# ###################### Ensure/ Split Data Utils #########################

"""
Works off subReportInfo types. Specifically, per type, what is the form and scope?
- form == RAW: meaning need in /data
- form == TYPE 
  - scope == SO: need typeSO
  - scope == ALL: need type
- form == TYPEENHANCE: ignore here as means used to enhance a type (from raw) potentially somewhere else. ie/ incorporated into another typeSO or type
"""
def ensureRequiredData(stationNumber, subReportName):
    
    subReportInfos = json.load(open("subReportInfo.json"))
    subReportInfoByName = dict((info["title"], info) for info in subReportInfos)
    
    if subReportName not in subReportInfoByName:
        raise Exception("{} sub report not defined in 'subReportInfo.json'".format(subReportName))
        
    missing = {}
    for typeInfo in subReportInfoByName[subReportName]["types"]:
        form = typeInfo["form"]
        typId = re.sub(r'\.', '_', typeInfo["id"])
        if form == "TYPEENHANCE":
            continue # on another system
        if form == "TYPE":
            scope = typeInfo["scope"]    
            if scope == "SO":
                dataLocn = DATAREDUCTIONS_TYPESO_TEMPL.format(stationNumber)
                if not os.path.isfile(dataLocn + "{}SOReduction.json".format(typId)):
                    if "typesso" not in missing:
                        missing["typesso"] = []
                    missing["typesso"].append(typId)
            else:
                dataLocn = DATAREDUCTIONS_TYPE_TEMPL.format(stationNumber)
                if not os.path.isfile(dataLocn + "{}Reduction.json".format(typId)):
                    if "types" not in missing:
                        missing["types"] = []
                    missing["types"].append(typId)     
            continue
        if form == "RAW":
            dataLocn = DATALOCN_TEMPL.format(stationNumber)
            if not os.path.isfile(dataLocn + "{}-0.zip".format(typId)):
                if "data" not in missing:
                    missing["data"] = []
                missing["data"].append(typId)   
            continue
        raise Exception("Invalid/Unexpected 'form' in subReportInfo".format(form))                  

    if len(missing):
        raise Exception("Can't proceed to produce __{}__ - missing data for {} needed first - {}".format(subReportName, stationNumber, json.dumps(missing, indent=4)))
        
"""
Expect 1 ALL (returned first) and many sub's all of one property

It looks LIKE could add up Captures for JPG, ...
"""
def splitTypeDatas(stationNo, typ, useSO=True, expectSubTypeProperty=""):
    if useSO:
        typeDatas = json.load(open(DATAREDUCTIONS_TYPESO_TEMPL.format(stationNo) + "{}SOReduction.json".format(typ)))
    else:
        typeDatas = json.load(open(DATAREDUCTIONS_TYPE_TEMPL.format(stationNo) + "{}Reduction.json".format(typ)))
    if isinstance(typeDatas, dict): # old and dictionary only of ALL
        return typeDatas, []
    allTypeDatas = [typeData for typeData in typeDatas if "_subTypeId" not in typeData]
    if len(allTypeDatas):
        if len(allTypeDatas) != 1:
            raise Exception("Expect one and only one ALL type data in a type data list")
    allTypeData = allTypeDatas[0]
    subTypeDatas = [typeData for typeData in typeDatas if "_subTypeId" in typeData]
    if len(subTypeDatas):
        subTypeProp = subTypeDatas[0]["_subTypeId"].split(":")[0]
        if expectSubTypeProperty and subTypeProp != expectSubTypeProperty:
            raise Exception("Expect sub type prop \"{}\" and many splits but got \"{}\"".format(expectSubTypeProperty, subTypeProp))
    elif expectSubTypeProperty:
        raise Exception("No sub type datas but expect {} as sub type property".format(expectSubTypeProperty))
    return allTypeData, subTypeDatas

# ############################### Stat Utils #########################

"""
Shows off key stats with a little (obvious) stats observations

https://docs.scipy.org/doc/numpy/user/

TODO: more on numpy (ie/ go through it as go through books)
"""
def reportKeyStats(kstats):
    print "Count Values: {}".format(kstats["count"])
    mn = kstats["mean"]
    print "Mean: {}".format(mn)
    M = kstats["median"]
    print "Median (M): {}".format(M)
    if M > mn:
        print "\t... M bigger than Mean so data skews left"
    elif M < mn:
        print "\t... M smaller than Mean so data skews right"
    print "Standard Deviation (s): {}".format(kstats["std"])
    print "\treflect skew of min {} and max {}".format(kstats["min"], kstats["max"])
    print "IQR: {}".format(kstats["iqr"])                                                   
    print "\tbetween 1st ({}) and 3rd ({}) quartiles".format(kstats["quartileOne"], kstats["quartileThree"])
    if "olt" in kstats:
        print "Outliers below", kstats["olt"]
    print "Outliers above", kstats["oht"]
    print
    
"""
Key stats for distribution of values

min, max
Quartile: 1, 2 (Median), 3 for data-spread
... "five-number summary" ideal for data w/ outliers and a 'box-and-whisker' plot 
... Quartiles divide a rank-ordered data set into four equal parts at 25, 50, 75
percentiles
IQR
... "midspread" - best at spread if outliers
olt < (Q1-1.5*IQR)
oht > Q3+1.5*IQR
... for key outliers: < are lows, > are highs. Only present if > max, < min
mean
std
... for symm distributions with no outliers where five numbers don't kick in

TODO: consider <span class='yellowIt'>{:.2f}%</span> and numpy.around or
roundFloat (see below)

oht: 1.5 == "inner fences"
major outliers: Q3 + 3*IQR == "outer fences" ... need name for this.

Note: this is 'Univariate method' (See: https://www.kdnuggets.com/2017/01/3-methods-deal-outliers.html / 'Minkowski error' etc)

https://en.wikipedia.org/wiki/Outlier (Tukey's fences)
- above: Q3 + K(Q3-Q1) where K is 1.5 and K = 3 is "far out"
- below: Q1 - K(Q1-Q3)
ie/ K times Quartile. Fences for box plots.
"""
def keyStats(values):
    quartileOne = numpy.percentile(values, 25)
    median = numpy.percentile(values, 50)
    quartileThree = numpy.percentile(values, 75)
    # get variance in middle 50% of data
    # numpy.subtract(*numpy.percentile(values, [75, 25]))
    iqr = quartileThree - quartileOne # interquartile range    
    oht = quartileThree + (1.5 * iqr) # Outlier High above this
    cntValsGTOHT = sum(1 for val in values if val > oht) 
    ohto = quartileThree + (3 * iqr) # idea of "outer fence": TODO: get name
    cntValsGTOHTO = sum(1 for val in values if val > ohto) 
    stats = {"total": sum(val for val in values), "count": len(values), "min": numpy.min(values), "quartileOne": quartileOne, "median": median, "quartileThree": quartileThree, "max": numpy.max(values), "iqr": iqr, "oht": oht, "ohto": ohto, "mean": numpy.mean(values), "std": numpy.std(values)}
    olt = quartileOne - (1.5 * iqr) # Outlier Low below this
    if int(olt) > 0: # only olt if > 0 ie/ negative ie/ all acceptable
        stats["olt"] = olt
    """
    Own: should show outliers? only go into outliers if big ie/ if pretty smooth 
    """
    stats["hasOutliers"] = True if stats["max"] - stats["oht"] > stats["median"] else False
    if cntValsGTOHT:
        stats["gtoht"] = cntValsGTOHT
    if cntValsGTOHTO:
        stats["gtohto"] = cntValsGTOHTO
    return stats
    
"""
Use typically for byValueCount off typer or a Counter

    "a": 1
    "b": 2
    "c": 1
    
-----> [a, b, b, c]

and can pass into kstats if forceInt

Note: forceInt is for the measured values which may be integers but
are in string form.
"""
def flattenFrequencyDistribution(freqDistrib, forceInt=True):
    freqDistribFlat = []
    for entry in freqDistrib:
        f = [int(entry) if forceInt else entry for i in range(int(freqDistrib[entry]))]
        freqDistribFlat.extend(f)
    return freqDistribFlat
    
"""
New Stats to expand:

- (basic) and relative (percent/ration) frequency distribution ie/ cnt occurrences
        from collections import Counter
        Counter([...]) ... 
  ... put relatives into a stacked bar chart
  ... conditional => a number of freq distribs, one each per condition (ex/ for PDFs, WSs)
- bar (or a pie) to histogram: when # of distict values too big then go to histogram
- null hypothesis/expected frequencies: variables unrelated (type of image and WS?)
  - https://www.spss-tutorials.com/chi-square-independence-test/
"""

"""
- cumulative frequencies add as go (https://www.spss-tutorials.com/frequency-distribution-what-is-it/) ... no good for nominals ("French" or "PDF") but for good/better/best ...
  ie age of patients  ... https://www.wyzant.com/resources/lessons/math/statistics_and_probability/averages/cumulative_frequency_percentiles_and_quartiles
  ... A cumulative frequency graph, also known as an Ogive
  ... good site for stuff.
  ... cumulative freq can be used to gen quartiles
"""        

"""
Clustering, numpy has it (ntlk uses it - but mainly see intelligent web book)
... k ... and clumping 'users' or ... based on similarity/distance.
"""

"""
after excel, try matplotlib, networkx 
"""
    
# ############################ Simple Report Utils #################

def roundFloat(no):
    no = no.round(2)
    if no.is_integer():
        return int(no)
    return no
    
# ############################ Plot Utils ##########################

"""
Crude Example of Graph

import matplotlib.pyplot as plt

See: https://python-graph-gallery.com/120-line-chart-with-matplotlib/ and
https://matplotlib.org/gallery/index.html

    plot([2007, 2008, 2009, 2010], [1, 2, 3, 4])

"""
def plot(xs, ys):

    import matplotlib.pyplot as plt
    plt.plot(xs, ys, "ro")
    plt.xlabel("Time")
    plt.ylabel("Ibs")
    plt.show()
