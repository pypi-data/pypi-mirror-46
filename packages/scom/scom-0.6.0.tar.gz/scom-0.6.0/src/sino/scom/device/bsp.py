# -*- coding: utf-8 -*-
#

import logging
from ..defines import *
from ..device.scomdevice import ScomDevice

logging.getLogger(__name__).setLevel(logging.INFO)  # DEBUG, INFO, WARNING, ERROR, CRITICAL


class Bsp(ScomDevice):
    """Provides access to a Battery Status Processor (BSP).
    """

    DEVICE_START_ADDRESS = 601
    DEVICE_MAX_ADDRESS = 615

    scom = None
    log = logging.getLogger(__name__)

    paramInfoTable = {
        'voltageOfTheSystem': {'name': 'voltageOfTheSystem', 'number': 6057,
                               'propertyFormat': 'enum', 'default': 0x01,
                               'studerName': 'Voltage of the system'},
        'nominalCapacity': {'name': 'nominalCapacity', 'number': 6001,
                            'propertyFormat': 'float', 'default': 110,
                            'studerName': 'Nominal capacity'},
        'nominalDischargeDuration': {'name': 'nominalDischargeDuration', 'number': 6002,
                                     'propertyFormat': 'float', 'default': 20,
                                     'studerName': 'Nominal discharge duration (C-rating)'},
        'nominalShuntCurrent': {'name': 'nominalShuntCurrent', 'number': 6017,
                                'propertyFormat': 'float', 'default': 500,
                                'studerName': 'Nominal shunt current'},
        'nominalShuntVoltage': {'name': 'nominalShuntVoltage', 'number': 6018,
                                'propertyFormat': 'float', 'default': 50,
                                'studerName': 'Nominal shunt voltage'},
    }

    userInfoTable = {
        'batteryVoltage': {'name': 'batteryVoltage', 'number': 7000,
                           'propertyFormat': 'float', 'default': 0.0,
                           'studerName': 'Battery voltage'},
        'batteryCurrent': {'name': 'batteryCurrent', 'number': 7001,
                           'propertyFormat': 'float', 'default': 0.0,
                           'studerName': 'Battery current'},
        'soc': {'name': 'soc', 'number': 7002,
                'propertyFormat': 'float', 'default': 0.0,
                'studerName': 'State of Charge'},
        'power': {'name': 'power', 'number': 7003,
                  'propertyFormat': 'float', 'default': 0.0,
                  'studerName': 'Power'},
        'remainingAutonomy': {'name': 'remainingAutonomy', 'number': 7004,
                              'propertyFormat': 'float', 'default': 0.0,
                              'studerName': 'Remaining autonomy'},
        'softVersionMsb': {'name': 'softVersionMsb', 'number': 7037,
                           'propertyFormat': 'float', 'default': 0.0,
                           'studerName': 'ID SOFT msb'},
        'softVersionLsb': {'name': 'softVersionLsb', 'number': 7038,
                           'propertyFormat': 'float', 'default': 0.0,
                           'studerName': 'ID SOFT lsb'},
    }

    systemVoltageToStringTable = {0: u'Invalid',
                                  1: u'Automatic',
                                  2: u'12V',
                                  4: u'24V',
                                  8: u'48V'}

    def __init__(self, device_address, **kwargs):
        """
        :param device_address The device number on the SCOM interface. Own address of the device.
        :type device_address int
        """
        super(Bsp, self).__init__(device_address, **kwargs)          # Call base class constructor
        self._add_instance(self.SD_XTENDER)                          # Add this instance to the instance counter

        # Give paramInfoTable to ScomDevice base class
        super(Bsp, self)._set_param_info_table(self.paramInfoTable)

    @classmethod
    def class_initialize(cls, scom):
        """Tells devices with which SCOM interface to communicate."""
        cls.scom = scom

    @classmethod
    def _get_scom(cls):
        """Implementation of ScomDevice interface.
        """
        return cls.scom

    @property
    def device_type(self):
        """Implementation of ScomDevice interface.
        """
        return self.SD_BSP

    @property
    def software_version(self):
        """Implementation of ScomDevice interface.
        """
        return self.getSoftwareVersion()

    def getSoftwareVersion(self):
        idSoftMsb = self._read_user_info_ex(self.userInfoTable['softVersionMsb'])
        idSoftLsb = self._read_user_info_ex(self.userInfoTable['softVersionLsb'])

        if idSoftMsb and idSoftLsb:
            idSoftMajorVersion = int(idSoftMsb) >> 8
            idSoftMinorVersion = int(idSoftLsb) >> 8
            idSoftRevision = int(idSoftLsb) & 0xFF

            return {'major': idSoftMajorVersion, 'minor': idSoftMinorVersion, 'patch': idSoftRevision}
        return {'major': 0, 'minor': 0, 'patch': 0}

    def getBatteryVoltage(self):
        """Reads and returns the actual battery voltage [V]."""
        return self._read_user_info_ex(self.userInfoTable['batteryVoltage'])

    def getBatteryCurrent(self):
        """Reads and returns the actual battery current [A]."""
        return self._read_user_info_ex(self.userInfoTable['batteryCurrent'])

    def getSoc(self):
        """Reads and returns the actual state of charge [%]."""
        return self._read_user_info_ex(self.userInfoTable['soc'])

    def getPower(self):
        """Reads and returns the actual power [W]."""
        return self._read_user_info_ex(self.userInfoTable['power'])

    def getRemainingAutonomity(self):
        """Reads and returns the remaining autonomity in minutes."""
        return self._read_user_info_ex(self.userInfoTable['remainingAutonomy'])

    def getVoltageOfTheSystem(self):
        return self._read_parameter_info('voltageOfTheSystem')

    def getNominalCapacity(self):
        return self._read_parameter_info('nominalCapacity')

    def setNominalCapacity(self, value):
        """Sets the nominal battery capacity.

        Caution:
        Should be used with care. Calling this method too often
        will damage the Flash of the device!
        """
        return self._write_parameter_info('nominalCapacity', value, property_id=PROPERTY_VALUE_QSP)

    def getNominalDischargeDuration(self):
        return self._read_parameter_info('nominalDischargeDuration')

    def setNominalDischargeDuration(self, value):
        """Sets the nominal discharge duration.

        Caution:
        Should be used with care. Calling this method too often
        will damage the Flash of the device!
        """
        return self._write_parameter_info('nominalDischargeDuration', value, property_id=PROPERTY_VALUE_QSP)

    def getNominalShuntCurrent(self):
        return self._read_parameter_info('nominalShuntCurrent')

    def getNominalShuntVoltage(self):
        return self._read_parameter_info('nominalShuntVoltage')

    def _test(self):
        #self.setNominalCapacity(900)
        #self.setNominalDischargeDuration(10)

        value = self.software_version
        value = self.getBatteryVoltage()
        value = self.getBatteryCurrent()
        value = self.getSoc()
        value = self.getPower()
        value = self.getRemainingAutonomity()
        value = self.getVoltageOfTheSystem()
        value = self.getNominalCapacity()
        value = self.getNominalDischargeDuration()
        value = self.getNominalShuntCurrent()
        value = self.getNominalShuntVoltage()
        value = value
