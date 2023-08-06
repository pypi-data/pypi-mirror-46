#! /usr/bin/python3

import subprocess as sp
import json,re,os
#parsed in each class is where the final data will lie
class getCpu:
    def __init__(self,command_file='commands.json'):
        self.path=os.path.dirname(os.path.realpath(__file__))
        self.path=os.path.join(self.path,'etc')
        self.cmd_file =os.path.join(self.path,command_file)

        with open(self.cmd_file,'r') as cmd:
            self.cmds=json.load(cmd)
        self.cmds=self.cmds['cpu']
        data=self.execute()        
        self.parsed=self.parse(data)
        #print(data)

    def execute(self):
        proc=sp.Popen(self.cmds,stdout=sp.PIPE,stderr=sp.PIPE)
        data,err=proc.communicate(timeout=30)
        return data,err

    def parse(self,data):
        regex=cpu_regex(data[0])
        return regex.parsed

class cpu_regex:
    #if parsed is None something mostlike did went wrong with the match, that or no processor was detected, which is odd since you are reading this code on a unit that requires a processor, less its paper, in which case, you are running a theoretical....
    parsed=None
    template=b'(%s([ \t])*:|(%s):) *(?P<%s>.*)'
    item_sep='\n'
    item_regex=[
        template % ( b'processor', b'processor',b'processor'),
        template % ( b'vendor_id', b'vendor_id', b'vendor_id'),
        template % ( b'cpu\ family',b'cpu\ family',b'cpu_family'),
        template % ( b'model',b'model',b'model'),
        template % ( b'model\ name',b'model\ name',b'model_name',),
        template % ( b'stepping',b'stepping',b'stepping',),
        template % ( b'microcode',b'microcode',b'microcode',),
        template % ( b'cpu MHz',b'cpu MHz',b'cpu_MHz',),
        template % ( b'cache size',b'cache size',b'cache_size',),
        template % ( b'fpu',b'fpu',b'fpu',),
        template % ( b'fpu_exception',b'fpu_exception',b'fpu_exception',),
        template % ( b'cpuid level',b'cpuid level',b'cpuid_level',),
        template % ( b'wp',b'wp',b'wp',),
        template % ( b'flags',b'flags',b'flags',),
        template % ( b'bogomips',b'bogomips',b'bogomips',),
        template % ( b'clflush size',b'clflush size',b'clflush_size',),
        template % ( b'cache_alignment',b'cache_alignment',b'cache_alignment',),
        template % ( b'address sizes',b'address sizes',b'address_sizes',),
        template % ( b'power management',b'power management',b'power_management',)
    ]
    def __init__(self,data):
        self.data=data
        self.parsed=self.parser()

    def combine_dicts(self,recs):
        if not recs:
            return None
        if len(recs) == 1:
            return recs.pop()
        tmp={}
        for rec in recs:
            for key in rec.keys():
                if key in tmp.keys():
                    tmp[key].append(rec[key])
                else:
                    tmp[key] = [rec[key]]
        return tmp

    def parser(self):
        rec={}
        for pattern in self.item_regex:
            matches=[m.groupdict() for m in re.finditer(pattern,self.data)]
            mdicts=self.combine_dicts(matches)
            if mdicts:
                rec.update(mdicts)
        return rec
            

if __name__ == "__main__":
    cpu=getCpu("./commands.json")
    print(cpu.parsed)
