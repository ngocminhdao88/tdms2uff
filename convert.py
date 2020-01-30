import os
import pyuff

class convert:
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

    def __init__(self,path):
        self.path = path
        #self.name = os.path.split(path)[1]
    
    def check (self):
        if os.path.exists(self.path[:-5] + ".uff") == 1:
            print("Datei schon vorhanden!")
        else:
            pass
    
    def delete (self):
        try:
            os.remove(self.path[:-5] + ".uff")
        except:
            print(self.path)
        
    
    def uff_convert (self):
        for i in range(len(channels)):
            uff_data = {
                'id1': channels[i][0],
                'ordinate_spec_data_type':channels[i][1],
                'ordinate_axis_lab': channels[i][2],'ordinate_axis_units_lab': channels[i][2],
                'data':data,'x':data,
                'type':uff_type,'binary':binary,'func_type':func_type,'rsp_node': response_node,'rsp_dir': response_direction,'ref_dir': reference_direction,'ref_node': reference_node,'ord_data_type': ord_data_type,'rsp_ent_name':name,'ref_ent_name':name,'abscissa_spacing':abscissa_spacing,'abscissa_spec_data_type':abscissa_spec_data_type,'abscissa_axis_lab': abscissa_axis_lab,'abscissa_axis_units_lab': abscissa_axis_units_lab,'orddenom_spec_data_type':orddenom_spec_data_type
            }
            uffwrite = pyuff.UFF(self.path[:-5]+".uff")
            uffwrite._write_set(uff_data,'add')
