from python_terraform import *
from terraformvspherevm.terrascriptvspherevm import TerrascriptVSphereVM
from os import environ, pathsep, linesep
from os.path import exists, join, normpath
import socket


class TerraformVM:
    def __init__(self):
        find_file = self.__search_file('terraform',environ['PATH'])
        if not find_file:
            raise Exception

        self.terraform = Terraform()
        self.tfstateFile = 'terraform.tfstate'
        self.tfstate = None
        try:
            fd = open(self.tfstateFile, 'r')
            self.tfstate = json.load(fd)
            fd.close()
        except FileNotFoundError:
            pass

        self.VmResources = {}


    def __search_file(self, filename, search_path):
        logger = logging.getLogger()
        file_found = 0
        paths = str.split(search_path, pathsep)
        for path in paths:
            if exists(join(path, filename)):
                file_found = 1
                break
        if file_found:
            logger.info("{} found at {}".format(filename, normpath(join(path, filename))))
            return True
        else:
            logger.error("{} not found".format(filename))
            return None


    def addVirtualMachine(self, properties):
        logger = logging.getLogger()
        if properties['nic'] is not None:
            if (len(properties['nic']) != len(properties['ip'])):
                logger.critical("The number of --ip must be equal to --nic")
                raise Exception

            if (len(properties['nic']) != len(properties['cidr'])):
                logger.critical("The number of --cidr must be equal to --nic")
                raise Exception

            for addr in properties['ip']:
                try:
                    socket.inet_aton(addr)
                    # legal
                except socket.error:
                    logger.critical("{} is not a valid IP address".format(addr))
                    raise Exception

        vm = TerrascriptVSphereVM(
            properties['name'],
            properties['guestid'],
            properties['cpu'],
            properties['ram'],
            properties['folder'])
        
        vm.setProvider(
            properties['esxhost'],
            properties['esxuser'],
            properties['esxiPassword'])
        
        vm.setDatacenter(properties['datacenter'])
        vm.setDatastore(properties['datastore'])
        vm.setResourcePool(properties['pool'])
        vm.setTemplate(properties['template'])
        vm.setTimezone(properties['timezone'])
        vm.setDomain(properties['domain'])
        vm.setGateway(properties['gateway'])
        for dns in properties['dns']:
            vm.addDns(dns)
        
        if properties['disk'] is not None:
            for idx, size in enumerate(properties['disk']):
                vm.addDisk(size)

        if properties['nic'] is not None:
            for idx, nic in enumerate(properties['nic']):
                vm.addNetworkInterface(nic, properties['ip'][idx], properties['cidr'][idx])

        self.VmResources[properties['name']] = {
            "script": "{}.tf.json".format(properties['name']),
            "properties": properties,
            "terrascript": vm }


    def createTerraformConfigurationFiles(self, name):
        logger = logging.getLogger()
        logger.info("Create Terraform script '{}'".format(self.VmResources[name]['script']))
        self.VmResources[name]['terrascript'].saveConfiguration(self.VmResources[name]['script'])


    def cleanTerraformConfigurationFiles(self, name):
        logger = logging.getLogger()
        logger.info("Clean terraform configuration file {}".format(self.VmResources[name]['script']))
        os.unlink(self.VmResources[name]['script'])

    
    def isVmExistsInStateFile(self, name):
        if self.tfstate:
            try:
                for module in self.tfstate['modules']:
                    if module['resources']['vsphere_virtual_machine.vm']['primary']['attributes']['name'] == name:
                        return True
            except KeyError:
                pass
        return False
    

    def tfInit(self):
        logger = logging.getLogger()
        logger.info("Init Terraform")
        return_code, stdout, stderr = self.terraform.init(
            input=False,
            no_color=IsFlagged)


    def createPlan(self, name):
        logger = logging.getLogger()
        planFile = "{}.plan".format(name)
        logger.info("Create Terraform plan '{}'".format(planFile))
        return_code, stdout, stderr = self.terraform.plan(
            out=planFile,
            input=False,
            no_color=IsFlagged)
        
        logger.debug(stdout)

        if return_code == 0:
            logger.warning("Nothing to create. Exit")
            exit(0)
    
        if return_code != 2:
            logger.error("Return Code: {}".format(return_code))
            logger.error(stderr)
            raise Exception
        
        self.VmResources[name]['planfile'] = planFile
    
    
    def deletePlan(self, name):
        logger = logging.getLogger()
        logger.debug("Remove file ''".format(self.VmResources[name]['planfile']))
        os.unlink(self.VmResources[name]['planfile'])
        del self.VmResources[name]['planfile']


    def applyPlan(self, name):
        logger = logging.getLogger()
        planFile = self.VmResources[name]['planfile']
        logger.info("Apply terraform plan '{}'".format(planFile))
        return_code, stdout, stderr = self.terraform.apply(
            planFile,
            input=False,
            no_color=IsFlagged)
        
        logger.debug(stdout)

        if return_code != 0:
            logger.error("Return Code: {}".format(return_code))
            logger.error(stderr)
            raise Exception
        logger.info("Virtual Machine created")


    def destroyResource(self, name):
        logger = logging.getLogger()
        logger.info("Destroy terraform Resource")
        return_code, stdout, stderr = self.terraform.destroy(
            input=False)
        logger.debug(stdout)

        if return_code != 0:
            logger.error("Return Code: {}".format(return_code))
            logger.error(stderr)
            raise Exception


    def importResource(self, name):
        logger = logging.getLogger
        logger.info("Import Ressource from vSphere")
        vmProperties = self.VmResources[name]['properties']
        self.terraform.import_cmd(
            "vsphere_virtual_machine.vm",
            "/{}/vm/{}/{}".format(
                vmProperties['datacenter'],
                vmProperties['folder'],
                vmProperties['name']))

  
    def createVM(self, name):
        self.createTerraformConfigurationFiles(name)
        self.tfInit()
        self.createPlan(name)
        self.applyPlan(name)
        self.deletePlan(name)
        self.cleanTerraformConfigurationFiles(name)


    def destroyVM(self,name):
        self.createTerraformConfigurationFiles(name)
        self.tfInit()
        if not self.isVmExistsInStateFile(name):
            self.importResource(name)
        self.destroyResource(name)
        self.cleanTerraformConfigurationFiles(name)