# BEGIN: Copyright 
# Copyright (C) 2019 Rector and Visitors of the University of Virginia 
# All rights reserved 
# END: Copyright 

# BEGIN: License 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
#   http://www.apache.org/licenses/LICENSE-2.0 
# END: License 

import os
import re
import tempfile
from datetime import datetime
from shutil import copyfile
# from nssacPreCommitHook.git import Git, Status

class Header:
    def __init__(self, _git, _copyright, _license = None):
        
        self.copyrights = _copyright
        
        for c in self.copyrights:
            if not "startYear" in c:
                c["startYear"] = 0
            else:
                c["startYear"] = int(c["startYear"])
                
        self.git = _git
        self.copyrights = sorted(self.copyrights, key = lambda i: i["startYear"], reverse = True)
        self.license = _license
        self.commentStart = ""
        self.commentEnd = ""
        self.output = None
        
    def updateHeader(self, inFile, commentStart, commentEnd = "", prolog = [], mode = "now"):
        self.commentStart = commentStart
        self.commentEnd = commentEnd
        skipExistingLicense = False
        skipExistingCopyright = False

        TmpFile = tempfile.mktemp()
                
        copyfile(inFile, TmpFile)
          
        self.output = open(inFile, "w")
        Input = open(TmpFile, "r")
        
        self.skipProlog(Input, prolog)
        
        if self.copyrights:
            if mode == "now":
                CurrentYear = datetime.now().year
            else:
                Out, Err, Code = self.git("log", "-1", "--date=short", "--pretty=format:\"%ad\"", inFile)
                
                Result = Out.splitlines()
            
                if not Result:
                    CurrentYear = datetime.now().year
                else:
                    CurrentYear = int(Result[0].strip('"')[0:4])
                    
            Out, Err, Code = self.git("log", "--reverse", "--date=short", "--pretty=format:\"%ad\"", inFile)
            
            Result = Out.splitlines()
            
            if not Result:
                FirstYear = CurrentYear
            else:
                FirstYear = int(Result[0].strip('"')[0:4])
        
            self.writeCopyright(FirstYear, CurrentYear)
            skipExistingCopyright = True
            
        if self.license:
            self.writeLicense()
            skipExistingLicense = True
            
        if skipExistingLicense and skipExistingCopyright:
            SectionStart = re.compile("{:s} BEGIN: (License|Copyright) *{:s}".format(self.commentStart, self.commentEnd))
            SectionEnd = re.compile("{:s} END: (License|Copyright) *{:s}".format(self.commentStart, self.commentEnd))
        elif skipExistingLicense:
            SectionStart = re.compile("{:s} BEGIN: License *{:s}".format(self.commentStart, self.commentEnd))
            SectionEnd = re.compile("{:s} END: License *{:s}".format(self.commentStart, self.commentEnd))
        elif skipExistingCopyright:
            SectionStart = re.compile("{:s} BEGIN: Copyright *{:s}".format(self.commentStart, self.commentEnd))
            SectionEnd = re.compile("{:s} END: Copyright *{:s}".format(self.commentStart, self.commentEnd))
        else:
            self.write(Input.read())
            return
        
        EmptyLine = re.compile('^\\s*$')
        Skip = False
        SkipEmpty = True
        
        for Line in Input:
            if Skip:
                if SectionEnd.search(Line):
                    Skip = False
                    SkipEmpty = True
                continue
            
            if SkipEmpty:
                if EmptyLine.search(Line):
                    continue
                else:
                    SkipEmpty = False
            
            if SectionStart.search(Line):
                Skip = True
                continue
            
            self.write(Line)
            
        Input.close()
        self.output.close()
        
        os.remove(TmpFile)
        
    def skipProlog(self, file, prolog):
        if not prolog: return
        
        LinesToWrite = 0
        
        for p in prolog:
            MaxLines = p["maxLines"] if "maxLines" in p else 0
            Unlimited = (MaxLines == 0)
            PrologEnd = re.compile(p["end"])
            Finished = False
            LinesToWrite = 0
                  
            for Line in file:
                if not Unlimited and MaxLines <= 0:
                    break
                
                LinesToWrite += 1
                MaxLines -= 1
                
                if PrologEnd.search(Line):
                    Finished = True
                    break
                
            file.seek(0)
        
            if Finished:
                break
        
        if Finished:
            
            AppendLine = False
            while LinesToWrite > 0:
                AppendLine = True
                LinesToWrite -= 1
                self.output.write(file.readline())
                
            if AppendLine:
                self.output.write("\n")
                
    def writeCopyright(self, firstYear, lastYear):
        self.writeComment("BEGIN: Copyright")
        
        for c in self.copyrights:
            
            if lastYear > c["startYear"]:
                FirstYear = max([firstYear, c["startYear"]])
                
                if FirstYear == lastYear:
                    Range = "{:d}".format(FirstYear)
                else:
                    Range = "{:d} - {:d}".format(FirstYear, lastYear)
                    
                for t in c["text"]:
                    self.writeComment(t.format(Range))
                
                if firstYear >= c["startYear"]:
                    break
                
                lastYear = c["startYear"] - 1
                self.write("\n")
                
                
        self.writeComment("END: Copyright")
        self.write("\n")
        
    def writeLicense(self):
        self.writeComment("BEGIN: License")
        
        for t in self.license:
            self.writeComment(t)
                
        self.writeComment("END: License")
        self.write("\n")
        
    def write(self, line):
        self.output.write(line)
        
    def writeComment(self, line):
        self.output.write("{:s} {:s} {:s}\n".format(self.commentStart, line, self.commentEnd))
        