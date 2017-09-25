from api_emulator.redfish.EventService_api import EventServiceAPI, CreateEventService
from api_emulator.redfish.Chassis_api import ChassisCollectionAPI, ChassisAPI, CreateChassis
from api_emulator.redfish.ComputerSystem_api import ComputerSystemCollectionAPI, ComputerSystemAPI, CreateComputerSystem
from api_emulator.redfish.Manager_api import ManagerCollectionAPI, ManagerAPI, CreateManager
from api_emulator.redfish.pcie_switch_api import PCIeSwitchesAPI, PCIeSwitchAPI
from api_emulator.redfish.eg_resource_api import EgResourceCollectionAPI, EgResourceAPI, CreateEgResource
from api_emulator.redfish.power_api import CreatePower
from api_emulator.redfish.thermal_api import CreateThermal
from api_emulator.redfish.ComputerSystem.ResetAction_api import ResetAction_API
from api_emulator.redfish.ComputerSystem.ResetActionInfo_api import ResetActionInfo_API
from api_emulator.redfish.processor import CreateProcessor
from api_emulator.redfish.memory import CreateMemory
from api_emulator.redfish.simplestorage import CreateSimpleStorage
from api_emulator.redfish.ethernetinterface import CreateEthernetInterface

import g
import random

from api_emulator.redfish.ResourceBlock_api import CreateResourceBlock
from api_emulator.redfish.ResourceBlock_processor import Create_ResourceBlock_Processor


def populate(num):
    # populate with some example infrastructure
    for i in xrange(num):
        chassis = 'Chassis-{0}'.format(i + 1)
        compSys = 'System-{0}'.format(i + 1)
        bmc = 'BMC-{0}'.format(i + 1)
        # create chassi
        CreateChassis(resource_class_kwargs={
            'rb': g.rest_base, 'linkSystem': compSys, 'linkMgr': bmc}).put(chassis)
        # create chassi subordinate sustems
        CreatePower(resource_class_kwargs={'rb': g.rest_base, 'ch_id': chassis}).put(chassis)
        CreateThermal(resource_class_kwargs={'rb': g.rest_base, 'ch_id': chassis}).put(chassis)
        # create ComputerSystem
        CreateComputerSystem(resource_class_kwargs={
            'rb': g.rest_base, 'linkChassis': chassis, 'linkMgr': bmc}).put(compSys)
        # subordinates, note that .put does not need to be called here
        ResetAction_API(resource_class_kwargs={'rb': g.rest_base, 'sys_id': compSys})
        ResetActionInfo_API(resource_class_kwargs={'rb': g.rest_base, 'sys_id': compSys})
        CreateProcessor(rb=g.rest_base, suffix='System', processor_id='CPU0', suffix_id=compSys, chassis_id=chassis)
        CreateProcessor(rb=g.rest_base, suffix='System', processor_id='CPU1', suffix_id=compSys, chassis_id=chassis)
        CreateMemory(rb=g.rest_base, suffix='System', memory_id='DRAM1', suffix_id=compSys, chassis_id=chassis)
        CreateMemory(rb=g.rest_base, suffix='System', memory_id='NVRAM1', suffix_id=compSys, chassis_id=chassis,
                     capacitymb=65536, devicetype='DDR4', type='NVDIMM_N', operatingmodes='PMEM')
        CreateSimpleStorage(rb=g.rest_base, suffix='System', suffix_id=compSys, storage_id='controller-1', drives=2,
                            capacitygb=512, chassis_id=chassis)
        CreateSimpleStorage(rb=g.rest_base, suffix='System', suffix_id=compSys, storage_id='controller-2', drives=2,
                            capacitygb=512, chassis_id=chassis)
        CreateEthernetInterface(rb=g.rest_base, suffix='System', suffix_id=compSys, nic_id='NIC-1',
                            speedmbps=40000, vlan_id=4095, chassis_id=chassis)
        CreateEthernetInterface(rb=g.rest_base, suffix='System', suffix_id=compSys, nic_id='NIC-2',
                            speedmbps=40000, vlan_id=4095, chassis_id=chassis)
        # create manager
        CreateManager(resource_class_kwargs={
            'rb': g.rest_base, 'linkSystem': compSys, 'linkChassis': chassis, 'linkInChassis': chassis}).put(bmc)


        # create ResourceBlock
        RB = 'RB-{0}'.format(i + 1)
        config = CreateResourceBlock(resource_class_kwargs={'rb': g.rest_base, 'linkSystem': "CS_%d"%i, 'linkChassis': "Chassis-%d"%i, 'linkZone': "ResourceZone-%d"%i})
        config.put(RB)
        # create ResourceBlock Processor
        Create_ResourceBlock_Processor(rb=g.rest_base, suffix='CompositionService/ResourceBlocks', processor_id='CPU-%d'%(i+1), suffix_id=RB, chassis_id=chassis)
        config.post(g.rest_base, RB, "Processors", 'CPU-%d'%(i+1))
        # Create ResourceBlock Processor
        Create_ResourceBlock_Processor(rb=g.rest_base, suffix='CompositionService/ResourceBlocks', processor_id='CPU-%d'%(i+2), suffix_id=RB, chassis_id=chassis)
        config.post(g.rest_base, RB, "Processors", 'CPU-%d'%(i+2))