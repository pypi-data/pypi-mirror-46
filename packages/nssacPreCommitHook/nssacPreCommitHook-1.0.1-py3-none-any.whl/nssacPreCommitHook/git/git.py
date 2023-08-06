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

import subprocess


def to_cli_args(*args, **kwargs):
    cmd = []
    for k, v in kwargs.items():
        k = k.replace('_', '-')
        short = len(k) == 1
        if short:
            cmd.append('-' + k)
            if v is not True:
                cmd.append(v)
        else:
            if v is True:
                cmd.append('--' + k)
            else:
                cmd.append('--{0}={1}'.format(k, v))

    cmd.extend(args)
    return cmd


class Git(object):
    def __init__(self, cmd=None, repo_path=None):
        self.repo_path = repo_path
        self.git = cmd if cmd else ['git']

    def __call__(self, subCommand, *args, **kwargs):
        cmd = self.git + [subCommand] + to_cli_args(*args, **kwargs)

        subprocess_kwargs = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE
        }

        if self.repo_path:
            subprocess_kwargs['cwd'] = self.repo_path

        pipes = subprocess.Popen(cmd, **subprocess_kwargs)
        out, err = pipes.communicate()
        return out.decode('utf-8'), err.decode('utf-8'), pipes.returncode

    def __str__(self):  # pragma: no cover
        return str(self.git)

    def __repr__(self):  # pragma: no cover
        return '<Git {}>'.format(str(self))
    
    def applyPatch(self, patch = None, *args, **kwargs):
        if not patch:
            return self.apply(args, **kwargs)
        
        cmd = self.git + ["apply"] + to_cli_args(*args, **kwargs)

        Patch = bytearray()
        Patch.extend(map(ord, patch))
        
        subprocess_kwargs = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'stdin': subprocess.PIPE
        }

        if self.repo_path:
            subprocess_kwargs['cwd'] = self.repo_path

        pipes = subprocess.Popen(cmd, **subprocess_kwargs)
        out, err = pipes.communicate(input = Patch)
        return out.decode('utf-8'), err.decode('utf-8'), pipes.returncode
        
