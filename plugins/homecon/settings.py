#!/usr/bin/python3
################################################################################
#    Copyright 2016 Brecht Baeten
#    This file is part of HomeCon.
#
#    HomeCon is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    HomeCon is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with HomeCon.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

import os
import logging
import lib.orb

from dateutil.tz import gettz

logger = logging.getLogger('')


class Settings(object):
    def __init__(self,smarthome,database):
        """
        """
        self._sh = smarthome
        self._db = database

        self.ws_commands = {
            'setting': self._ws_setting,
        }

        # add homecon settings from the database
        self._add_settings_from_database_to_smarthome()

        # add homecon default settings if they are not added yet
        self.add_lat()
        self.add_lon()
        self.add_elev()
        self.add_tz()


    def add_lat(self):
        """
        add the lattitude setting to the database and smarthome
        """
        success = self._db.settings_POST(setting='lat',value=50.894914)
        if success:
            self._update_lat_in_smarthome(50.894914)
            return True
        return False

    def add_lon(self):
        """
        add the longitude setting to the database and smarthome
        """
        success = self._db.settings_POST(setting='lon',value=4.341551)
        if success:
            self._update_lon_in_smarthome(4.341551)
            return True
        return False

    def add_elev(self):
        """
        add the longitude setting to the database and smarthome
        """
        success = self._db.settings_POST(setting='elev',value=13)
        if success:
            self._update_elev_in_smarthome(13)
            return True
        return False

    def add_tz(self):
        """
        add the longitude setting to the database and smarthome
        """
        success = self._db.settings_POST(setting='tz',value='Europe/Brussels')
        if success:
            self._update_tz_in_smarthome('Europe/Brussels')
            return True
        return False


    def update_lat(self,value):
        # update the database

        success = self._db.settings_PUT(setting='lat',value=value)
        if success:
            # update the smarthome
            success = self._update_lat_in_smarthome(value)
            return success

        return False

    def update_lon(self,value):
        # update the database
        success = self._db.settings_PUT(setting='lat',value=value)
        if success:
            # update the smarthome
            success = self._update_lon_in_smarthome(value)
            return success

        return False

    def update_elev(self,value):
        # update the database
        success = self._db.settings_PUT(setting='elev',value=value)
        if success:
            # update the smarthome
            success = self._update_elev_in_smarthome(value)
            return success

        return False

    def update_tz(self,value):
        # update the database
        success = self._db.settings_PUT(setting='tz',value=value)
        if success:
            # update the smarthome
            success = self._update_tz_in_smarthome(value)
            return success

        return False



    def _update_lat_in_smarthome(self,value):
        # update the setting in smarthome
        self._sh._lat = value
        
        # reset sun and moon
        if hasattr(self._sh, '_lon') and hasattr(self._sh, '_lat') and hasattr(self._sh, '_elev'):
            self._sh.sun = lib.orb.Orb('sun', self._sh._lon, self._sh._lat, self._sh._elev)
            self._sh.moon = lib.orb.Orb('moon', self._sh._lon, self._sh._lat, self._sh._elev)
            return True
        return False

    def _update_lon_in_smarthome(self,value):
        # update the setting in smarthome
        self._sh._lon = value

        # reset sun and moon
        if hasattr(self._sh, '_lon') and hasattr(self._sh, '_lat') and hasattr(self._sh, '_elev'):
            self._sh.sun = lib.orb.Orb('sun', self._sh._lon, self._sh._lat, self._sh._elev)
            self._sh.moon = lib.orb.Orb('moon', self._sh._lon, self._sh._lat, self._sh._elev)
            return True
        return False

    def _update_elev_in_smarthome(self,value):
        # update the setting in smarthome
        self._sh._elev = value

        # reset sun and moon
        if hasattr(self._sh, '_lon') and hasattr(self._sh, '_lat') and hasattr(self._sh, '_elev'):
            self._sh.sun = lib.orb.Orb('sun', self._sh._lon, self._sh._lat, self._sh._elev)
            self._sh.moon = lib.orb.Orb('moon', self._sh._lon, self._sh._lat, self._sh._elev)
            return True
        return False

    def _update_tz_in_smarthome(self,value):

        success = False

        # update the setting in smarthome

        tzinfo = gettz(value)
        if not tzinfo == None:
            self._sh._tzinfo = tzinfo
            self._sh.tz = value
            os.environ['TZ'] = self._sh.tz
            success = True
        else:
            logger.warning("Problem parsing timezone: {}. Using UTC.".format(value))
        

        return success



    def _add_settings_from_database_to_smarthome(self):
        """
        """
        settings = self._db.settings_GET()
        for setting in settings:
            if setting['setting'] == 'lat':
                self._update_lat_in_smarthome(float(setting['value']))
            elif setting['setting'] == 'lon':
                self._update_lon_in_smarthome(float(setting['value']))
            elif setting['setting'] == 'elev':
                self._update_elev_in_smarthome(float(setting['value']))
            elif setting['setting'] == 'tz':
                self._update_tz_in_smarthome(setting['value'])




    ############################################################################
    # websocket commands
    ############################################################################

    def _ws_setting(self,client,data,tokenpayload):

        success = False

        if tokenpayload and tokenpayload['permission']>=5 and 'path' in data:
            if 'val' in data:
                # delete
                if data['val'] == None:
                    pass

                # put 
                elif data['path'] == 'lat':
                    try:
                        val = float(data['val'])
                        success = self.update_lat(val)
                    except:
                        pass
                    result = self._sh._lat

                elif data['path'] == 'lon':
                    try:
                        val = float(data['val'])
                        success = self.update_lon(val)
                    except:
                        pass
                    result = self._sh._lon

                elif data['path'] == 'elev':
                    try:
                        val = float(data['val'])
                        success = self.update_elev(val)
                    except:
                        pass
                    result = self._sh._elev

                elif data['path'] == 'tz':
                    success = self.update_tz(data['val'])
                    result = self._sh.tz

            else:
                # get
                if data['path'] == 'lat':
                    result = self._sh._lat
                    success = True
                elif data['path'] == 'lon':
                    result = self._sh._lon
                    success = True
                elif data['path'] == 'elev':
                    result = self._sh._elev
                    success = True
                elif data['path'] == 'tz':
                    result = self._sh.tz
                    success = True
                logger.warning(result)

        if success:
            logger.info("User {} on client {} updated setting {} to {}".format(tokenpayload['userid'],client.addr,data['path'],result))
            return {'cmd':'setting', 'path':data['path'],'val':result}
        else:
            logger.debug("User {} on client {} tried to update a setting {}".format(tokenpayload['userid'],client.addr,data))
            return {'cmd':'setting', 'path':data['path'],'val':result}


