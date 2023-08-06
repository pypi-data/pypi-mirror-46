#!python

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

import argparse
import os
from nssacPreCommitHook.git.git import Git
from nssacPreCommitHook.preCommitHook import PreCommitHook

parser = argparse.ArgumentParser(description="nssacPreCommitHook: A pre commit hook used to maintain license and copyright information in source files.")

parser.add_argument("-r", "--repository", required = True, nargs = 1, help = "The path to the git repository")
parser.add_argument("-c", "--config", nargs = 1, help = "The config file specifying the license and copyright applied (default: [REPOSITORY]/.nssac.json)")
parser.add_argument("--init", action='store_true', help = "Apply license and copyright to all files in the repository.")

arguments = parser.parse_args()

arguments.repository[0] = os.path.abspath(arguments.repository[0])

if not arguments.config:
    arguments.config = [] 
    arguments.config.append(os.path.join(arguments.repository[0], ".nssac.json"))

arguments.config[0] = os.path.abspath(arguments.config[0])

preCommitHook = PreCommitHook(arguments.config[0], Git(repo_path=arguments.repository[0]))

if not arguments.init:
    preCommitHook.run()
else:
    preCommitHook.initRepo()
