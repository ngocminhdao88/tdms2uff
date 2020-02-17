import pyuff
import os
from nptdms import TdmsFile
from tdmsobj import TdmsObj

response_node          = 0
response_direction     = 0
reference_node         = 0 
reference_direction    = 0
name                   = 'name'
uff_type               = 58
binary                 = 1
func_type              = 1
ord_data_type          = 2
abscissa_spacing       = 1
abscissa_spec_data_type= 17
abscissa_axis_lab      = 'Time'
abscissa_axis_units_lab= 's'
orddenom_spec_data_type= 0

class Convert:
    """
    This class convert a tdms object to uff58 file
    """
    def __init__(self,tdmsObj):
        self._tdmsObj = tdmsObj

    def convert_tdms (self):
        tdms_file = TdmsFile(self._tdmsObj.path())
        """
        for group in tdms_file.groups():
            for i,tdms_channel in enumerate(tdms_file.group_channels(group)):

                # Access dictionary of properties:
                properties = tdms_channel.properties
                #print(properties)
                try:
                    unit_name = properties['NI_UnitDescription']
                    #print(unit_name)
                    channel_name = properties['NI_ChannelName']
                except:
                    unit_name = 'unknown'
                    channel_name = 'unknown'
                    #print ('unknown')
                    #pass

                # Access numpy array of data for channel:
                data = tdms_channel.data

                try:
                    time = tdms_channel.time_track()
                    #print(time)
                except:
                    #print('no time')
                    time = []
                    pass

                # do stuff with data and properties...
                uff_data = {
                    #'id1': channel_name,
                    'id1': chnName,
                    #'ordinate_spec_data_type':channels[i][1],
                    'ordinate_spec_data_type':chnType,
                    #'ordinate_axis_lab': unit_name,'ordinate_axis_units_lab': channels[i][2],
                    'ordinate_axis_lab': chnUnitDesc,'ordinate_axis_units_lab': chnUnit,
                    'data':data,'x':time,
                    'type':uff_type,'binary':binary,'func_type':func_type,'rsp_node': response_node,'rsp_dir': response_direction,'ref_dir': reference_direction,'ref_node': reference_node,'ord_data_type': ord_data_type,'rsp_ent_name':name,'ref_ent_name':name,'abscissa_spacing':abscissa_spacing,'abscissa_spec_data_type':abscissa_spec_data_type,'abscissa_axis_lab': abscissa_axis_lab,'abscissa_axis_units_lab': abscissa_axis_units_lab,'orddenom_spec_data_type':orddenom_spec_data_type
                    }
                uffwrite = pyuff.UFF(self.path[:-5]+".uff")
                uffwrite._write_set(uff_data,'add')
                #print('added '+channel_name)
        """
        #for i,tdms_channel in enumerate(tdms_file.group_channels(group)):
        group = tdms_file.groups()[0] #There is only one data group in TdmsFile
        for tdms_channel in self._tdmsObj.channels():

            """
            # Access dictionary of properties:
            properties = tdms_channel.properties
            #print(properties)
            try:
                unit_name = properties['NI_UnitDescription']
                #print(unit_name)
                channel_name = properties['NI_ChannelName']
            except:
                unit_name = 'unknown'
                channel_name = 'unknown'
                #print ('unknown')
                #pass

            # Access numpy array of data for channel:
            """
            #data = tdms_channel.data
            data = tdms_file.object(group, tdms_channel[0]).data

            try:
                #time = tdms_channel.time_track()
                time = tdms_file.object(group, tdms_channel[0]).time_track()
                #print(time)
            except:
                #print('no time')
                time = []
                pass

            # do stuff with data and properties...
            uff_data = {
                #'id1': channel_name,
                'id1': tdms_channel[0],
                #'ordinate_spec_data_type':channels[i][1],
                'ordinate_spec_data_type':tdms_channel[1],
                #'ordinate_axis_lab': unit_name,'ordinate_axis_units_lab': channels[i][2],
                'ordinate_axis_lab': tdms_channel[3],'ordinate_axis_units_lab': tdms_channel[2],
                'data':data,'x':time,
                'type':uff_type,'binary':binary,'func_type':func_type,'rsp_node': response_node,'rsp_dir': response_direction,'ref_dir': reference_direction,'ref_node': reference_node,'ord_data_type': ord_data_type,'rsp_ent_name':name,'ref_ent_name':name,'abscissa_spacing':abscissa_spacing,'abscissa_spec_data_type':abscissa_spec_data_type,'abscissa_axis_lab': abscissa_axis_lab,'abscissa_axis_units_lab': abscissa_axis_units_lab,'orddenom_spec_data_type':orddenom_spec_data_type
                }
            #uffwrite = pyuff.UFF(self.path[:-5]+".uff")
            uffwrite = pyuff.UFF(self._tdmsObj.path()[:-5]+".uff")
            uffwrite._write_set(uff_data,'overwrite')
