#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
from enum import Enum, unique
import json
import pprint
import datetime
import time

import ExperimentsLogReader.scan as s

@unique
class LogTypes(Enum):
    DBBC = 1
    SDR = 2

os.environ['TZ'] = 'UTC'
time.tzset()

class ExperimentLogReader(object):
    __slots__ = ('logFile', 'outputPath', 'output', 'logLines')

    def __init__(self, logFile, outputPath):
        self.logFile = logFile
        self.outputPath = outputPath
        self.output = dict()

        with open(self.logFile, 'rb') as contents:
            self.logLines = contents.readlines()

        def tesLogLine(line):
            try :
                line.decode("utf-8")
            except:
                return ("")
            else:
                return line.decode("utf-8")

        self.logLines = [tesLogLine(l) for l in self.logLines]

    def writeOutput(self):
        self.output_data = open(self.outputPath + "log.dat", "w")
        self.output_data.write(json.dumps(self.output, indent=1))
        self.output_data.close()
        print("created", self.outputPath + "log.dat")

    def getLogs(self):
        return self.output

    def printLogs(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.output)

class SDRlogReader(ExperimentLogReader):
    def __init__(self, logFile, outputPath):
        super().__init__(logFile, outputPath)
        self.parseHeader()
        self.parseBody()
        self.writeOutput()

    def getHeader(self):
        header = [h for h in self.logLines if h.startswith("#")]
        return header

    def getBody(self):
        body = [b for b in self.logLines if "#" not in b]
        return body

    def parseHeader(self):
        self.output["header"] = dict()
        for line in self.getHeader():
            key = line.split(":")[0][1:len(line.split(":")[0])]
            value = line.split(":")[1].strip()
            if " " in value:
                value = value.split()
            self.output["header"][key] = value

    def parseBody(self):
        for line in self.getBody():
            if not "rxc" in line and not "wx" in line:
                key = line.split(" ")[1].strip() + line.split(" ")[2].strip()
                date = line.split(" ")[0].strip()
                AzEl = [line.split(" ")[3].strip(), line.split(" ")[4].strip()]
                self.output[key] = dict()
                self.output[key]["date"] = date
                self.output[key]["AzEl"] = AzEl

class DBBClogReader(ExperimentLogReader):
    def __init__(self, logFile, outputPath, coordinates=None, sourceName=None):
        __slots__ = ('coordinates', 'scan_names', 'sources', 'dates', "timeStarts", "timeStops", "DurationsMin", "RAs", "DECs", "Epochs", "Systemtemperatures", "FreqBBC1s", "FreqBBC1s", "FreqBBC2s", "FreqStart", "FreqStop", "loas", "locs", "scanNameString", "sourceName_list", "clocks", "scanList", "headerLines", "fs_frequency_list", "elevation_list", "scanLines", "Location", "sourceName", "date_list", "single")

        super().__init__(logFile, outputPath)
        self.coordinates = coordinates
        self.scan_names = list()
        self.sources = list()
        self.dates = ""
        self.timeStarts = list()
        self.timeStops = list()
        self.DurationsMin = list()
        self.DurationsSec = list()
        self.RAs = list()
        self.DECs = list()
        self.Epochs = list()
        self.Systemtemperatures = list()
        self.FreqBBC1s = list()
        self.FreqBBC2s = list()
        self.FreqStart = list()
        self.FreqStop = list()
        self.loas = list()
        self.locs = list()
        self.scanNameString = list()
        self.sourceName_list = list()
        self.clocks = list()
        self.scanList = list()
        self.headerLines = list()
        self.fs_frequency_list = list()
        self.elevation_list = list()
        self.scanLines = dict()
        self.Location = ""
        self.sourceName = sourceName
        self.date_list = list()

        if len(self.coordinates) != 0:
            self.single = True
        else:
            self.single = False

        append = False
        key = 0
        previousScan = 0

        for line in self.logLines:
            if type(line) == None:
                pass
            else:
                if "location" in line:
                    self.Location = line.split(";")[1].split(",")[1].strip()

                elif "scan_name=no" in line:
                    append = True

                    if ";" not in line:
                        self.scan_name = line.split(":")[3].split(",")[0].split("=")[1][2:].lstrip("0")
                        key = int(self.scan_name)

                        if self.scan_name in self.scan_names:
                            raise Exception("Two scans with same name " + self.scan_name)

                        self.scan_names.append(self.scan_name)
                        self.scanLines[key] = list()

                        if previousScan != 0 and previousScan + 1 != key:
                            print("Skipped scan ", previousScan + 1)

                        previousScan = key

                    elif ";" in line:
                        self.scan_name = line.split(";")[1].split("=")[1].split(",")[0][2:].lstrip("0")
                        key = self.scan_name

                        if self.scan_name in self.scan_names:
                            raise Exception("Two scans with same name " + self.scan_name)

                        self.scan_names.append(self.scan_name)
                        self.scanLines[key] = list()

                # Testing if line is not in header and it is not empty
                if len(line) != 0 and append:
                    self.scanLines[key].append(line)

                # Testing if line is  in header and it is not empty
                elif len(line) != 0 and append == False:
                    self.headerLines.append(line)

        header = s.Scan(self.headerLines)
        header.getParametrs()
        self.header_date, self.header_source, self.header_sourceName, self.header_epoch, self.header_ra, self.header_dec, self.header_timeStart, self.header_timeStop, self.header_SystemtemperaturesForScan, self.header_freqBBC1, self.header_freqBBC2, self.header_loa, self.header_loc, self.header_clock, self.header_fs_frequency, self.header_elevation = header.returnParametrs()

        for scan in self.scanLines:
            scanData = s.Scan(self.scanLines[scan])
            self.scanList.append(scanData)
            scanData.setScanNumber(scan)
            scanData.getParametrs()
            self.date, source, sourceName, epoch, ra, dec, timeStart, timeStop, SystemtemperaturesForScan, freqBBC1, freqBBC2, loa, loc, clock, fs_frequency, elevation = scanData.returnParametrs()

            if self.single:
                source = self.sourceName + "," + self.coordinates[0] + "," + self.coordinates[1]
                sourceName = self.sourceName
                ra = list()
                dec = list()
                Ra = self.coordinates[0]
                Dec = self.coordinates[1]
                print(Dec)
                epoch = self.coordinates[2]

                ra.append(Ra[0:2])
                ra.append(Ra[2:4])
                ra.append(Ra[4:len(Ra)])

                if Dec[0] == "-":
                    dec.append(Dec[0:3])
                    dec.append(Dec[3:5])
                    dec.append(Dec[5:len(Dec)])
                else:
                    dec.append(Dec[0:2])
                    dec.append(Dec[2:4])
                    dec.append(Dec[4:len(Dec)])

                freqBBC2 = self.header_freqBBC2
                loc = self.header_loc
                loa = self.header_loa

            self.date_list.append(self.date)
            self.fs_frequency_list.append(fs_frequency)
            self.sources.append(source)
            self.sourceName_list.append(sourceName)
            self.Epochs.append(epoch)
            self.RAs.append(ra)
            self.DECs.append(dec)
            self.timeStarts.append(timeStart)
            self.timeStops.append(timeStop)
            self.Systemtemperatures.append(SystemtemperaturesForScan)
            self.FreqBBC1s.append(freqBBC1)
            self.FreqBBC2s.append(freqBBC2)
            self.loas.append(loa)
            self.locs.append(loc)
            self.clocks.append(clock)
            self.elevation_list.append(elevation)

        if self.single:
            tmp_fs_frequency = list()
            tmp_fs_frequency.append(self.header_fs_frequency)
            tmp_fs_frequency.extend(self.fs_frequency_list)
            self.fs_frequency_list = tmp_fs_frequency

            tmpSystemperatures = list()
            tmpSystemperatures.append(self.header_SystemtemperaturesForScan)
            tmpSystemperatures.extend(self.Systemtemperatures)

            self.Systemtemperatures = tmpSystemperatures

        for y in range(0, len(self.scan_names)):
            try:
                DurMin = datetime.datetime.strptime(self.timeStops[y], "%H:%M:%S") - datetime.datetime.strptime(self.timeStarts[y], "%H:%M:%S")
                self.DurationsMin.append(DurMin.seconds)
                self.DurationsSec.append(DurMin.seconds / 60)
            except:
                self.DurationsMin.append(0)
                self.DurationsSec.append(0)
                continue

        for f in range(0, len(self.scan_names)):
            self.FreqStart.append(float(self.FreqBBC1s[f]) + float(self.loas[f]))
            self.FreqStop.append(float(self.FreqBBC2s[f]) + float(self.locs[f]))
        self.__createLogs()
        self.writeOutput()

    def __createLogs(self):
        message = ""
        if any(scan.getmanualyChangedSystemTemU1() or scan.getmanualyChangedSystemTemU9() or scan.getmanualyChangedBBC1() or scan.getmanualyChangedBBC2() for scan in self.scanList):
            message = message + "Manual Changes !!!" + "\n"

            print("Yes changes ")

            for scan in self.scanList:
                if scan.getmanualyChangedSystemTemU1():
                    message = message + "For scan Number " + str(
                        scan.getScanNumber()) + " Manually Changed System Temperature U1" + "\n"

                if scan.getmanualyChangedSystemTemU9():
                    message = message + "For scan Number " + str(
                        scan.getScanNumber()) + " Manually Changed System Temperature U9" + "\n"

                if scan.getmanualyChangedBBC1():
                    message = message + "For scan Number " + str(scan.getScanNumber()) + " Manually Changed BBC1" + "\n"

                if scan.getmanualyChangedBBC2():
                    message = message + "For scan Number " + str(scan.getScanNumber()) + " Manually Changed BBC2" + "\n"

        self.output["header"] = {"location":self.Location,"Systemtemperature":self.header_SystemtemperaturesForScan, "Ra":self.header_ra , "Dec":self.header_dec, "dates":self.date_list[0], "startTime":self.header_timeStart, "LO":float(self.header_loa), "BBC":self.header_freqBBC1, "FreqStart": float(self.header_freqBBC1) + float(self.header_loa), "sourceName":self.header_source, "source":self.header_sourceName, "stopTime": self.header_timeStop, "clockOffset": self.header_clock, "fs_frequencyfs":"0.0", "message":message}

        for i in range(0, len(self.scan_names)):
            #print(self.Systemtemperatures[i])
            self.output[self.scan_names[i]] = {"Systemtemperature": self.Systemtemperatures[i], "Ra": self.RAs[i],
                                            "Dec": self.DECs[i], "dates": self.date_list[i],
                                            "startTime": self.timeStarts[i], "FreqStart": self.FreqStart[i],
                                            "sourceName": self.sourceName_list[i], "stopTime": self.timeStops[i],
                                            "clockOffset": str(self.clocks[i]),
                                            "fs_frequencyfs": self.fs_frequency_list[i],
                                            "elevation": self.elevation_list[i]}

    def getAllScansNumbers(self):
        return self.scan_names

    def getScansForSource(self, sourceName):
        indices_source = [i for i, x in enumerate(self.sourceName) if x == sourceName]
        scanNamesForSource = list()

        for j in range(0, len(indices_source)):
            scanNamesForSource.append(self.scan_names[indices_source[j]])
            return scanNamesForSource

    def getAllfs_frequencys(self):
        return self.fs_frequency_list

    def getFirstScanStartTime(self):
        return self.timeStarts[0]

class LogReaderFactory:
    def getLogReader(type, logFile, outputPath, coordinates=None, sourceName=None):
        if type == LogTypes.SDR:
            return SDRlogReader(logFile, outputPath)
        else:
            return DBBClogReader(logFile, outputPath, coordinates, sourceName)

