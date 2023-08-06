#! /usr/bin/python3

import subprocess as sp
import json,re,string,os
#parsed in each class is where the final data will lie
class getDmidecode:
    def __init__(self,command_file='commands.json'):
        self.path=os.path.dirname(os.path.realpath(__file__))
        self.path=os.path.join(self.path,'etc')
        self.cmd_file =os.path.join(self.path,command_file)
        if os.environ['USER'] == 'root':
            with open(self.cmd_file,'r') as cmd:
                self.cmds=json.load(cmd)
            self.cmds=self.cmds['dmidecode']
            data=self.execute()        
            self.parsed=self.parse(data)
            #print(data)
        else:
            self.parsed={}
            print('Error! You do not have permission to do this!')

    def execute(self):
        proc=sp.Popen(self.cmds,stdout=sp.PIPE,stderr=sp.PIPE)
        data,err=proc.communicate(timeout=30)
        return data.decode(),err

    def parse(self,data):
        regex=dmidecode_regex(data[0])
        return regex.parsed

    def exportToFile(self,fname):
        try:
            with open(fname,'w') as ofile:
                json.dump(self.parsed,ofile)
            return True
        except Exception as e:
            print(e)
            return False    

class dmidecode_regex: 
    item_regex=[
        # BIOS Info
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBIOS\ Information\n(.)*Vendor:\ (?P<bios_vendor_name>.*)\n',0,'bios_info'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBIOS\ Information\n(.)*\n\tVersion:\ (?P<bios_version>.*)\n',0,'bios_info'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBIOS\ Information\n(.)*\n(.)*\n\tRelease\ Date:\ (?P<bios_release_date>.*)\n',0,'bios_info'],
        # System Info
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Information\n\tManufacturer:\ (?P<system_manufacturer>.*)\n',0,'system_info'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Information\n(.)*\n\tProduct\ Name:\ (?P<system_product_name>.*)\n',0,'system_info'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Information\n(.)*\n(.)*\n(.)*\n\tSerial\ Number:\ (?P<system_serial_number>.*)\n',0],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Information\n(.)*\n(.)*\n(.)*\n(.)*\n\tUUID:\ (?P<system_uuid>.*)\n',0,'system_info'], 
        #port information
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPort\ Connector\ Information\n\tInternal\ Reference\ Designator:\ (?P<int_ref_des>.*)\n',0,'port_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPort\ Connector\ Information\n(.)*\n\tInternal\ Connector\ Type:\ (?P<int_con_type>.*)\n',0,'port_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPort\ Connector\ Information\n(.)*\n(.)*\n\tExternal\ Reference\ Designator:\ (?P<ext_ref_des>.*)\n',0,'port_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPort\ Connector\ Information\n(.)*\n(.)*\n(.)*\n\tExternal\ Connector\ Type:\ (?P<ext_con_type>.*)\n',0,'port_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPort\ Connector\ Information\n(.)*\n(.)*\n(.)*\n(.)*\n\tPort Type:\ (?P<port_type>.*)\n',0,'port_information'],
        #baseboard information
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBase\ Board\ Information\n\tManufacturer:\ (?P<baseboard_manufacturer>.*)\n',0,'baseboard_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBase\ Board\ Information\n(.)*\n\tProduct\ Name:\ (?P<product_name>.*)\n',0,'baseboard_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBase\ Board\ Information\n(.)*\n(.)*\n\tVersion:\ (?P<version>.*)\n',0,'baseboard_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBase\ Board\ Information\n(.)*\n(.)*\n(.)*\n\tSerial\ Number:\ (?P<serial_number>.*)\n',0,'baseboard_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBase\ Board\ Information\n(.)*\n(.)*\n(.)*\n(.)*\n\tAsset\ Tag:\ (?P<asset_tag>.*)\n',0,'baseboard_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBase\ Board\ Information.*?Features:\n(?P<features>.*)\tLocation\ In\ Chassis' ,re.DOTALL,'baseboard_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBase\ Board\ Information.*?Location\ In Chassis:\ (?P<location_in_chassis>[\w\ ]*)\n\tChassis\ Handle:',re.DOTALL,'baseboard_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBase\ Board\ Information.*?Chassis Handle:\ (?P<chassis_handle>\S*)\n\tType:',re.DOTALL,'baseboard_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBase\ Board\ Information.*?Type:\ (?P<type>[\w\ ]*)\n\tContained\ Object\ Handles:',re.DOTALL,'baseboard_information'],
        #Chassis information
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nChassis\ Information\n\tManufacturer:\ (?P<manufacturer>.*)\n',0,'chassis_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nChassis\ Information\n(.)*\n\tType:\ (?P<chassis_type>.*)\n',0,'chassis_information'],      
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nChassis\ Information\n(.)*\n(.)*\n(.)*\tLock:\ (?P<lock>.*)\n',0,'chassis_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nChassis\ Information\n(.)*\n(.)*\n(.)*\n(.)*\tVersion:\ (?P<version>.*)\n',0,'chassis_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nChassis\ Information\n(.)*\n(.)*\n(.)*\n(.)*\n(.)*\tSerial\ Number:\ (?P<serial_number>.*)\n',0,'chassis_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nChassis\ Information\n(.)*\n(.)*\n(.)*\n(.)*\n(.)*\n(.)*\tAsset\ Tag:\ (?P<asset_tag>.*)\n',0,'chassis_information'], 
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nChassis\ Information\n(.)*\n(.)*\n(.)*\n(.)*\n(.)*\n(.)*\n(.)*\tBoot-up\ State:\ (?P<boot_up_state>.*)\n',0,'chassis_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nChassis\ Information.*?\tPower\ Supply\ State:\ (?P<power_supply_state>.*)\n\tThermal\ State:',re.DOTALL,'chassis_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nChassis\ Information.*?\tThermal\ State:\ (?P<thermal_state>.*)\n\tSecurity\ Status:',re.DOTALL,'chassis_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nChassis\ Information.*?\tSecurity\ Status:\ (?P<security_status>.*)\n\tOEM\ Information:',re.DOTALL,'chassis_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nChassis\ Information.*?\tNumber\ Of\ Power\ Cords:\ (?P<number_of_power_cords>.*)\n\tContained\ Elements:',re.DOTALL,'chassis_information'],
        #system slot information
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Slot\ Information.*?\tDesignation:\ (?P<designation>[^\n]*)\n\tType:',re.DOTALL,'system_slot_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Slot\ Information.*?\tType:\ (?P<type>[^\n]*)\n\tCurrent\ Usage:',re.DOTALL,'system_slot_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Slot\ Information.*?\tCurrent\ Usage:\ (?P<current_usage>[^\n]*)\n\tLength:',re.DOTALL,'system_slot_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Slot\ Information.*?\tLength:\ (?P<length>[^\n]*)\n\tID:',re.DOTALL,'system_slot_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Slot\ Information.*?\tID:\ (?P<id>[^\n]*)\n\tCharacteristics:',re.DOTALL,'system_slot_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Slot\ Information.*?\tCharacteristics:\n(?P<characteristics>.*?)\n\tBus\ Address:',re.DOTALL,'system_slot_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Slot\ Information.*?\tBus\ Address:\ (?P<bus_address>[^\n]*?)\n',re.DOTALL,'system_slot_information'],
        #onboard device information
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nOn\ Board\ Device\ Information.*?\tType:\ (?P<type>[^!\n]*)\n',re.DOTALL,'onboard_device_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nOn\ Board\ Device\ Information.*?\tStatus:\ (?P<status>[^[\n]*)\n',re.DOTALL,'onboard_device_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nOn\ Board\ Device\ Information.*?\tDescription:\ (?P<description>[^\n]*)\n',re.DOTALL,'onboard_device_information'],
        #RAM information
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPhysical\ Memory\ Array\n.*?Location:\ (?P<location>[^\n]*)\n',re.DOTALL,'RAM_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPhysical\ Memory\ Array\n.*?Use:\ (?P<use>[^\n]*)\n',re.DOTALL,'RAM_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPhysical\ Memory\ Array\n.*?Error\ Correction\ Type:\ (?P<error_correction_type>[^\n]*)\n',re.DOTALL,'RAM_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPhysical\ Memory\ Array\n.*?Maximum\ Capacity:\ (?P<max_cap>[^\n]*)\n',re.DOTALL,'RAM_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPhysical\ Memory\ Array\n.*?Error\ Information\ Handle:\ (?P<error_information_handle>[^\n]*)\n',re.DOTALL,'RAM_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPhysical\ Memory\ Array\n.*?Number\ Of\ Devices:\ (?P<number_of_devices>[^\n]*)\n',re.DOTALL,'RAM_information'],
        #memory array mapped address
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Array\ Mapped\ Address\n.*?Starting\ Address:\ (?P<starting_address>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Array\ Mapped\ Address\n.*?Ending\ Address:\ (?P<ending_address>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Array\ Mapped\ Address\n.*?Range\ Size:\ (?P<range_size>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Array\ Mapped\ Address\n.*?Physical\ Array\ Handle:\ (?P<physical_array_handle>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Array\ Mapped\ Address\n.*?Partition\ Width:\ (?P<partition_width>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Array\ Handle:\ (?P<array_handle>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Error\ Information\ Handle:\ (?P<error_information_handle>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Total\ Width:\ (?P<total_width>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Data\ Width:\ (?P<data_width>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Size:\ (?P<size>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Form\ Factor:\ (?P<form_factor>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Set:\ (?P<set>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Locator:\ (?P<locator>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Bank\ Locator:\ (?P<bank_locator>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Type:\ (?P<type>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Type\ Detail:\ (P?<type_detail>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Speed:\ (?P<speed>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Manufacturer:\ (?P<manufacturer>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Serial\ Number:\ (?P<serial_number>[^\n*])\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Asset\ Tag:\ (<?Passet_tag>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Part\ Number:\ (?P<part_number>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Rank:\ (?P<rank>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Configured\ Memory\ Speed:\ (?P<configured_mem_speed>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Minimum\ Voltage:\ (?P<minimum_voltage>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Maximum\ Voltage:\ (?P<maximum_voltage>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\n.*?Configured\ Voltage:\ (?P<configured_voltage>[^\n]*)\n',re.DOTALL,'memory_mapped_array_address'],
        # Processor Info
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n\tSocket\ Designation:\ (?P<socket_designation>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Type:\ (?P<type>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Family:\ (?P<family>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Manufacturer:\ (?P<manufacturer>[^\n]*)\n',re.DOTALL,'processor_information'],
    [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?ID:\ (?P<id>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Signature:\ (?P<signature>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Flags:\n(?P<flags>.*?)\n\tVersion:',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Version:\ (?P<version>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Voltage:\ (?P<voltage>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?External\ Clock:\ (?P<external_clock>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Max\ Speed:\ (?P<max_speed>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Current\ Speed:\ (?P<current_speed>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Status:\ (?P<status>[^\n]*)\n',re.DOTALL,'processor_information'],
         [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Upgrade:\ (?P<upgrade>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?L1\ Cache\ Handle:\ (?P<l1_cache_handle>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?L2\ Cache\ Handle:\ (?P<l2_cache_handle>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?L3\ Cache\ Handle:\ (?P<l3_cache_handle>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Serial\ Number:\ (?P<serial_number>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Asset\ Tag:\ (?P<asset_tag>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Part\ Number:\ (?P<part_number>[^[\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Core\ Count:\ (?P<core_count>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Core\ Enabled:\ (?P<core_enabled>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Thread\ Count:\ (?P<thread_count>[^\n]*)\n',re.DOTALL,'processor_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nProcessor\ Information\n.*?Characteristics:\n(?P<characteristics>.*?)\n\n',re.DOTALL,'processor_information'],
        #bios lang info
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBIOS\ Language\ Information\n.*?Language\ Description\ Format:\ (?P<language_description_fmt>[^\n]*)\n',re.DOTALL,'bios_language_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBIOS\ Language\ Information\n.*?Installable\ Languages:\ (?P<number_of_installable_lang>[^\n]*)\n(?P<installable_lang>.*?)Currently\ Installed\ Language:',re.DOTALL,'bios_language_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nBIOS\ Language\ Information\n.*?Currently\ Installed\ Language:\ (?P<currently_installed_lang>[^\n]*)\n',re.DOTALL,'bios_language_information'],
    #memory device mapped address
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\ Mapped\ Address.*?Starting\ Address:\ (?P<starting_address>[^\n]*)\n',re.DOTALL,'memory_device_mapped_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\ Mapped\ Address.*?Ending\ Address:\ (?P<ending_address>[^\n]*)\n',re.DOTALL,'memory_device_mapped_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\ Mapped\ Address.*?Range\ Size:\ (?P<range_size>[^\n]*)\n',re.DOTALL,'memory_device_mapped_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\ Mapped\ Address.*?Physical\ Device\ Handle:\ (?P<physical_device_handle>[^\n]*)\n',re.DOTALL,'memory_device_mapped_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\ Mapped\ Address.*?Memory\ Array\ Mapped\ Address\ Handle:\ (?P<memory_array_mapped_address_handle>[^\n]*)\n',re.DOTALL,'memory_device_mapped_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\ Mapped\ Address.*?Partition\ Row\ Position:\ (?P<partition_row_position>[^\n]*)\n',re.DOTALL,'memory_device_mapped_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\ Mapped\ Address.*?Interleave\ Position:\ (?P<interleave_position>[^\n]*)\n',re.DOTALL,'memory_device_mapped_address'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nMemory\ Device\ Mapped\ Address.*?Interleaved\ Data\ Depth:\ (?P<interleaved_data_depth>[^\n]*)\n',re.DOTALL,'memory_device_mapped_address'],
        #portable battery
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPortable\ Battery\n.*?Location:\ (?P<location>[^\n]*)\n',re.DOTALL,'portable_battery'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPortable\ Battery\n.*?Manufacturer:\ (?P<manufacturer>[^\n]*)\n',re.DOTALL,'portable_battery'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPortable\ Battery\n.*?Serial\ Number:\ (?P<serial_number>[^\n]*)\n',re.DOTALL,'portable_battery'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPortable\ Battery\n.*?Name:\ (?P<name>[^\n]*)\n',re.DOTALL],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPortable\ Battery\n.*?Chemistry:\ (?P<chemistry>[^\n]*)\n',re.DOTALL,'portable_battery'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPortable\ Battery\n.*?Design\ Capacity:\ (?P<design_capacity>[^\n]*)\n',re.DOTALL,'portable_battery'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPortable\ Battery\n.*?Design\ Voltage:\ (?P<design_voltage>[^\n]*)\n',re.DOTALL,'portable_battery'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPortable\ Battery\n.*?SBDS\ Version:\ (?P<sbds_version>[^\n]*)\n',re.DOTALL,'portable_battery'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPortable\ Battery\n.*?Maximum\ Error:\ (?P<maximum_error>[^\n]*)\n',re.DOTALL,'portable_battery'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPortable\ Battery\n.*?SBDS\ Manufacture\ Date:\ (?P<sbds_manufacture_date>[^\n]*)\n',re.DOTALL,'portable_battery'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nPortable\ Battery\n.*?OEM-specific\ Information:\ (?P<oem_specific_information>[^\n]*)\n',re.DOTALL,'portable_battery'],
        #system boot info
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nSystem\ Boot\ Information\n.*?Status:\ (?P<status>[^\n]*)\n',re.DOTALL,'system_boot_information'],
        #onboard device
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nOnboard\ Device\n.*?Reference\ Designation: (?P<reference_designation>[^\n]*)\n',re.DOTALL,'onboard_device'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nOnboard\ Device\n.*?Type: (?P<type>[^\n]*)\n',re.DOTALL,'onboard_device'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nOnboard\ Device\n.*?Status:\ (?P<status>[^\n]*)\n',re.DOTALL,'onboard_device'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nOnboard\ Device\n.*?Type\ Instance:\ (?P<type_instance>[^\n]*)\n',re.DOTALL,'onboard_device'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nOnboard\ Device\n.*?Bus\ Address:\ (?P<bus_address>[^\n]*)\n',re.DOTALL,'onboard_device'],
        #cache information
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?Socket\ Designation:\ (?P<socket_designation>[^\n]*)\n',re.DOTALL,'cache_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?Configuration:\ (?P<configuration>[^\n]*)\n',re.DOTALL,'cache_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?Operational\ Mode:\ (?P<operational_mode>[^\n]*)\n',re.DOTALL,'cache_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?Location:\ (?P<location>[^\n]*)\n',re.DOTALL,'cache_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?Installed\ Size:\ (?P<installed_size>[^\n]*)\n',re.DOTALL,'cache_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?Maximum\ Size:\ (?P<maximum_size>[^\n]*)\n',re.DOTALL,'cache_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?Supported\ SRAM\ Types:\n(?P<supported_sram_types>.*?)\tInstalled\ SRAM\ Type',re.DOTALL,'cache_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?Installed\ SRAM\ Type:\ (?P<installed_sram_type>[^\n]*)\n',re.DOTALL,'cache_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?Speed:\ (?P<speed>[^\n]*)\n',re.DOTALL,'cache_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?Error\ Correction\ Type:\ (?P<error_correction_type>[^\n]*)\n',re.DOTALL,'cache_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?System\ Type:\ (?P<system_type>[^\n]*)\n',re.DOTALL,'cache_information'],
        [r'Handle\ (?P<handle>[^\n\ ,]*),\ DMI\ type\ (?P<dmi_type>[^\n]*)\nCache\ Information\n.*?Associativity:\ (?P<associativity>[^\n]*)\n',re.DOTALL,'cache_information'],
    ]
    def __init__(self,data):
        self.data=data
        self.parsed=self.parser()
 
    def parser(self):
        rec=[]
        tmp={}
        for pattern in self.item_regex:
            
            try:
                if type(pattern) != type(list()):
                    matches=[{str(m.start()):m.groupdict()} for m in re.finditer(pattern,self.data)]

                    rec.extend(matches)
                    #print(pattern,[m.groups() for m in re.finditer(pattern,self.data)])                        
                    for i in matches:
                        for k in i.keys():
                            if k in tmp:
                                for kk in i[k].keys():
                                    tmp[k][kk]=i[k][kk].replace('\t','')
                            else:
                                tmp[k]={}
                                for kk in i[k].keys():
                                    tmp[k][kk]=i[k][kk].replace('\t','')
                else:
                    #primary supported method of regex list
                    if len(pattern) > 2:
                        matches=[{'{}_{}'.format(str(m.start()),pattern[2]):m.groupdict()} for m in re.finditer(pattern[0],self.data,pattern[1])]
                        rec.extend(matches)
                        #print(pattern,[m.groups() for m in re.finditer(pattern[0],self.data,pattern[1])])                        
                    else:
                        matches=[{str(m.start()):m.groupdict()} for m in re.finditer(pattern[0],self.data)]
                        rec.extend(matches)
                        #print(pattern,[m.groups() for m in re.finditer(pattern[0],self.data)])                        
                    for i in matches:
                        for k in i.keys():
                            if k in tmp:
                                for kk in i[k].keys():
                                    tmp[k][kk]=i[k][kk].replace('\t','')
                            else:
                                tmp[k]={}
                                for kk in i[k].keys():
                                    tmp[k][kk]=i[k][kk].replace('\t','')
            except Exception as e:
                print(pattern)
                print(e)
                return    
        return tmp

if __name__ == "__main__":
    dmidecode=getDmidecode("commands.json")
    
    for i in dmidecode.parsed.keys():
        print(dmidecode.parsed[i])
    print(dmidecode.parsed.keys())
    dmidecode.exportToFile('dmidecode.json')
