#! /usr/bin/python3

import subprocess as sp
import json,re,os
#parsed in each class is where the final data will lie
class getLspci:
    def __init__(self,command_file='commands.json'):
        self.path=os.path.dirname(os.path.realpath(__file__))
        self.path=os.path.join(self.path,'etc')
        self.cmd_file =os.path.join(self.path,command_file)

        with open(self.cmd_file,'r') as cmd:
            self.cmds=json.load(cmd)
        self.cmds=self.cmds['pci']
        data=self.execute()        
        self.parsed=self.parse(data)
        #print(data)

    def execute(self):
        proc=sp.Popen(self.cmds,stdout=sp.PIPE,stderr=sp.PIPE)
        data,err=proc.communicate(timeout=30)
        return data.decode(),err

    def parse(self,data):
        regex_nnmm=lspci_regex_nnmm(data[0])
        return {'nnmm':regex_nnmm.parsed}

class lspci_regex_nnmm:
    label_regex=r'[\w+\ \.\,\:\+\&\]\-\/\[\]\(\)]+'
    #label_regex=r'[\w+\ \.\,\:\+\&\-]+'
    code_regex=r'[0-9a-fA-F]{4}'
    busid_regex=r'[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9a-fA-F]'
    item_regex=[
        r'(?P<pci_device_bus_id>('+busid_regex+r'))\ "(?P<pci_device_class_name>'+label_regex+r') \[(?P<pci_device_class>'+code_regex+r')\]"' \
        +r'\ "(?P<pci_vendor_name>'+label_regex+r')\ \[(?P<pci_vendor_id>'+code_regex+r')\]"\ "(?P<pci_device_name>'+label_regex+r')' \
    + r'\ .*\"((?P<pci_subvendor_name>'+label_regex+r')\ \[(?P<pci_subvendor_id>'+code_regex+r')\])*"\ "((?P<pci_subdevice_name>'+label_regex+r')\ \[(?P<pci_subdevice_id>'+code_regex+r')\])*'
    ]
    item_separator=''
    required_fields=[
        'pci_device_bus_id',
        'pci_device_class_name',
        'pci_device_string'
    ]
    def __init__(self,data):
        self.data=data
        self.parsed=self.parser()
 
    def parser(self):
        rec=[]
        for pattern in self.item_regex:
            try:
                matches=[m.groupdict() for m in re.finditer(pattern,self.data)]
                rec=matches
            except Exception as e:
                print(pattern)
                print(e)
                return
        return rec
            

if __name__ == "__main__":
    lspci=getLspci("./commands.json")
    for i in lspci.parsed['nnmm']:
        print(i)
