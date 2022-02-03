import logging
class Settings():



    def get_property_pair(self,property_line:str):

            index_of_equal =property_line.index("=")
            index_of_hash=2
            try:
                index_of_hash = property_line.index("#")
            except:
                index_of_hash=len(property_line)
            property_value = property_line[index_of_equal + 1:index_of_hash]
            property_name=property_line[:index_of_equal]
            return (property_name,property_value)

    def check_binary(self,property_value,property_name):
        property_value=str(property_value)
        property_value=property_value.strip()

        if (property_value == "1" or property_value == "0"):
            if (property_value == '1'):
                return True
            else:
                return False
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s może być 0 lub 1" % (property_name))

    def check_float(self,property_value,property_name,min,max,no_max):
        property_value=float(str(property_value))
        min=float(str(min))
        max = float(str(max))
        if(no_max):
            if (property_value > min):
                return float(str(property_value))
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s musi być większe od %f" % (property_name,min))
        else:

            if (property_value > min and property_value<max):
                return float(str(property_value))
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s musi być pomiędzy %f i %f " % (property_name,min,max))

    def check_int(self,property_value,property_name,min,max,no_max):
        property_value=int(str(property_value))
        if(no_max):

            if (property_value > min):
                return int(str(property_value))
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s ma nieprawidłową wartość"%(property_name))
        else:

            if (property_value > min and property_value<max):
                return int(str(property_value))
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s ma nieprawidłową wartość"%(property_name) )

    def get_properties(self,file_with_properties):
        logging.basicConfig(level=logging.NOTSET)

        setting_dict={}
        for record in file_with_properties.readlines():
            if(len(record)!=0):
                property_name,property_value=self.get_property_pair(record)
                self.check_property(property_name,property_value)

        self.map_size = self.tier1_distance_from_intruder * 1.3


        # self.back_distance = 2 * self.intuder_size
        # self.minimal_hand_move_time = 0.05
        # self.folder_to_save_visualization = "./visualsation"
        # self.vis_counter=0
        # self.minimal_points=0
        #
        # self.dimension = int((self.map_size - (-self.map_size)) / self.map_resolution)
        # self.simple_resolution=2
        # self.simple_map_size = self.tier1_distance_from_intruder * 1.3
        # self.simple_dimension = int((self.map_size - (-self.map_size)) / self.simple_resolution)
        self.dodge_radius=self.uav_size*4
        self.save_distance=self.dodge_radius*2
        self.minimal_hand_range=self.intuder_size*1.3
        self.intruder_time_of_reaction=1.0
        self.minimal_travel_time=0.2
        logging.info("properties correct")
        return setting_dict

    def check_property(self,property_name,property_value):

        if(property_name=="uav_number"):
            property_value=int(str(property_value))

            if(property_value>0 and property_value<=2):
                self.uav_number=property_value
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s może być tylko 1 lub 2"%(property_name))

        elif (property_name=="hands_number"):
            property_value = int(str(property_value))
            if (property_value >= 0 and property_value <= 2):
                self.hands_number=property_value
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s może być 0,1,2 "%(property_name))
        elif (property_name=="visualization"):
            self.visualisation=self.check_int(property_value, property_name, -1, 3, False)
        elif (property_name=="T"):
            self.T=self.check_float(property_value,property_name,0,1,True)
        elif (property_name=="beat_the_score"):
            self.beat_the_score=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="intruder_max_energy"):
            self.intruder_max_energy=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="mode"):
            property_value=property_value.strip()
            if (property_value=="RW-RA"):
                self.mode=property_value
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s może przyjmować wartości: RW-RA"%(property_name))

        elif (property_name=="prob_of_attack"):

            self.prob_of_attack=self.check_float(property_value,property_name,0,1.1,False)
        elif (property_name=="prob_of_return_to_T2"):

            self.prob_of_return_to_T2=self.check_float(property_value,property_name,0,1,False)

        elif (property_name=="arrive_deterministic"):

            self.arrive_deterministic=self.check_binary(property_value,property_name)
        elif (property_name=="lambda1"):

            self.lambda1=self.check_float(property_value,property_name,0,1,True)
        elif (property_name=="tier1_distance_from_intruder"):

            self.tier1_distance_from_intruder=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="v_of_uav"):

            self.v_of_uav=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="wiat_time"):

            self.wiat_time=self.check_float(property_value,property_name,0,1,True)
        elif (property_name=="intuder_size"):

            self.intuder_size=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="uav_size"):

            self.uav_size=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="hand_size"):

            self.hand_size=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="velocity_hand"):

            self.velocity_hand=self.check_float(property_value,property_name,0,1,True)
        elif (property_name=="visualzation_update_interval"):

            self.visualzation_update_interval=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="r_of_LR"):

            self.r_of_LR=self.check_float(property_value,property_name,0,1,True)
            # if self.r_of_LR<self.intuder_size+self.uav_size:
            #     raise Exception("r_of_LR musi być większe niż intuder_size i uav_size")


        elif (property_name=="minimal_hand_move_time"):

            self.minimal_hand_move_time=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="map_resolution"):

            self.map_resolution=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="search_angle"):

            self.search_angle=self.check_float(property_value,property_name,20,360,False)

        elif (property_name=="seed"):

            self.seed=self.check_int(property_value,property_name,0,223,True)

        else:
            raise Exception("Błąd pliku konfiguracyjnego, nieznana nazwa właściwości:" +property_name)
