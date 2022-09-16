import logging
import typing

from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Modes
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point
from Events.Game.move.algos.GameObjects.data_lists.tools.points_cell import PointsCell


class Settings():

    def __init__(self):
        self.list_to_print=[]

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

            if (property_value >= min and property_value<max):
                return int(str(property_value))
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s ma nieprawidłową wartość"%(property_name) )

    def get_properties(self,file_with_properties,file_with_rewards,file_with_boxes,file_with_invisible):
        logging.basicConfig(level=logging.NOTSET)

        setting_dict={}
        self.is_directory=False
        for record in file_with_properties.readlines():
            if(len(record)!=0):
                if record[0]=="#":
                    continue

                property_name,property_value=self.get_property_pair(record)
                self.list_to_print.append({"name":property_name,"value":property_value})
                self.check_property(property_name,property_value)


        # if self.is_multirun and self.mode==Modes.LEARNING:
        #     raise Exception("Błąd pliku konfiguracyjnego. Tryb multirun działa tylko w trybie eksplotacji")
        self.map_size_y=520
        self.map_size_x=1040


        self.list_of_cell_points:typing.List[PointsCell]=self.get_list_of_points(file_with_rewards)
        self.lif_of_invisible=self.get_boxes_invisible(file_with_invisible)
        self.get_boxes(file_with_boxes)



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
        self.save_distance=self.dodge_radius*2 #minimal distance form secound uav
        self.minimal_hand_range=self.intuder_size*1.3
        self.tier1_distance_from_intruder=400
        self.uav_wait_time=3.0
        self.uav_number=2
        self.fake_targets_number=1






        self.minimal_travel_time=0.2


        self.is_hand_deviation=True
        self.safe_margin=self.jump_ratio*self.velocity_hand*4 # minimal distance from each hand to start attack

        self.naive_algo_curiosity_ratio=0.0


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
        elif (property_name=="operation_mode_cases"):
            property_value = property_value.strip()

            if (property_value in ["10", "11","12","13"]):
                self.mode_debug=property_value
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s może przyjmować wartości: 10, 11, 12, 13"%(property_name))
        elif (property_name=="operation_mode"):
            property_value = property_value.strip()

            if (property_value in ["00", "11"]):
                self.mode_debug=property_value
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s może przyjmować wartości: 10, 11, 12, 13"%(property_name))

            if property_value=="00":
                self.learning=True
                self.mode="learning"
            else:
                self.learning=False
                self.mode="exploitation"


        elif (property_name=="visualization"):
            self.visualisation=self.check_int(property_value, property_name, 0, 3, False)
        elif (property_name=="uav_energy_energy_cost_attack"):
            self.uav_energy_energy_cost_attack=self.check_float(property_value, property_name, 0, 3, True)
        elif (property_name=="uav_energy_energy_cost_tier1"):
            self.uav_energy_energy_cost_tier1=self.check_float(property_value, property_name, 0, 3, True)

        elif (property_name=="uav_energy_energy_cost_tier2"):
            self.uav_energy_energy_cost_tier2=self.check_float(property_value, property_name, 0, 3, True)
        elif (property_name=="uav_energy"):
            self.uav_energy=self.check_float(property_value, property_name, 1, 3, True)
        elif (property_name=="intruder_energy"):
            self.intruder_energy_cost_jump=self.check_float(property_value, property_name, 1, 3, True)
        elif (property_name=="intruder_energy_cost_jump"):
            self.intruder_energy_cost_jump=self.check_float(property_value, property_name, 0, 3, True)
        elif (property_name=="intruder_energy_cost_chasing"):
            self.intruder_energy_cost_chasing=self.check_float(property_value, property_name, 0, 3, True)
        elif (property_name=="searching_max_range"):
            self.searching_max_range=self.check_float(property_value, property_name, 0, 3, True)
        elif (property_name=="intruder_energy_cost_of_reaction"):
            self.intruder_energy_cost_of_reaction=self.check_float(property_value, property_name, 0, 3, True)
        elif (property_name=="energy_simulation_end_condition"):
            self.energy_simulation_end_condition=self.check_binary(property_value, property_name)
        elif (property_name=="drone_energy_destroy_condition"):
            self.drone_energy_destroy_condition=self.check_binary(property_value, property_name)
        elif (property_name=="safe_distance_ratio"):
            self.safe_distance_ratio=self.check_float(property_value, property_name,0.1,0,True)
        elif (property_name=="show_safe_space"):
            self.show_safe_space=self.check_binary(property_value, property_name)
        elif (property_name=="fake_targets_number"):
            self.fake_targets_number=self.check_int(property_value, property_name,1,0,True)
        elif (property_name=="number_of_points_to_win"):
            self.number_of_points_to_win=self.check_int(property_value, property_name,1,0,True)
        elif (property_name=="load_memory"):
            self.load_memory=self.check_binary(property_value,property_name)
        elif (property_name=="zone_width"):
            self.zone_width=self.check_int(property_value, property_name, 1, 3, True)
        elif(property_name=="is_multirun"):
            self.is_multirun=self.check_binary(property_value,property_name)
        elif (property_name=="number_of_runs"):
            self.number_of_runs=self.check_int(property_value,property_name,1,0,True)

        elif (property_name=="annealing_range"):
            self.annealing_step=self.check_float(property_value,property_name,0.1,0,True)

        elif (property_name=="epsilon"):
            self.epslion=self.check_float(property_value,property_name,0.001,0,True)

        elif(property_name=="temperature"):
            self.temperature=self.check_float(property_value,property_name,1,0,True)
        elif(property_name=="iterations_for_learning"):

            self.iterations_for_learning=self.check_int(property_value,property_name,1,0,True)
        elif(property_name=="temperature_reduction"):
            self.temperature_reduction=self.check_float(property_value,property_name,0,1,False)
        elif(property_name=="prob_of_fake_attack"):
            self.prob_of_fake_attack=self.check_float(property_value,property_name,0,1,False)
        elif(property_name=="annealing_number_of_iterations"):
            self.annealing_number_of_iterations=self.check_int(property_value,property_name,1,0,True)
        elif (property_name=="naive algo list limit"):
            self.naive_algo_list_limit=self.check_int(property_value,property_name,1,0,True)
        elif (property_name=="hand_max_deviation"):
            self.hand_max_deviation=self.check_int(property_value, property_name, 0, 1, True)
        elif (property_name=="T"):
            self.T=self.check_float(property_value,property_name,0,1,True)
        elif (property_name=="target_directory"):
            property_value=property_value.replace("\n","")
            self.target_directory=property_value
        elif (property_name=="visualisation_speed"):
            self.visualisation_speed=self.check_int(property_value,property_name,0,1,True)
        elif (property_name=="jump_ratio"):
            self.jump_ratio=self.check_float(property_value,property_name,0,1,True)
        elif (property_name=="time_to_wait_after_jump"):
            self.time_to_wait_after_jump=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="itertions_without_progress_to_stop"):
            self.itertions_without_progress_to_stop=self.check_int(property_value,property_name,0,1,True)
        elif (property_name=="temeprature_to_stop"):
            self.temeprature_to_stop=self.check_float(property_value,property_name,0,1,True)
        elif (property_name=="beat_the_score"):
            self.beat_the_score=self.check_float(property_value,property_name,0,1,True)
        elif (property_name=="is_anneling_step_active"):
            self.is_anneling_step_active=self.check_binary(property_value,property_name)

        elif (property_name=="intruder_max_energy"):
            self.intruder_max_energy=self.check_float(property_value,property_name,0,1,True)
        elif (property_name=="not_accept_tresh"):
            self.not_accept_tresh=self.check_int(property_value,property_name,-0.1,1,True)

        elif (property_name=="delay_between_attacks"):
            self.delay_between_attacks=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="learning"):
            self.learning=self.check_binary(property_value,property_name)
        elif(property_name=="exploitation"):
            exploitation=self.check_binary(property_value,property_name)
            if exploitation==self.learning:
                raise Exception("Błąd pliku konfiguracyjnego. parametry exploitation i learning nie mogą mieć tej samej wartości")
            if exploitation:
                self.mode="exploitation"
            else:
                self.mode="learning"
        elif (property_name=="debug"):
            self.debug=self.check_binary(property_value,property_name)
        elif (property_name=="mode"):
            property_value=property_value.strip()
            if (property_value in ["learning", "exploitation"]):
                self.mode=property_value
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s może przyjmować wartości: learning, exploitation"%(property_name))
        elif (property_name=="learning_algo_type"):
            property_value=property_value.strip()
            if (property_value in ["RS", "SA"]):
                self.learning_algo_type=property_value
                self.is_sa_b=False
            elif property_value=="SA-B":
                self.learning_algo_type="SA"
                self.is_sa_b=True
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s może przyjmować wartości: RS, SA"%(property_name))
        elif (property_name=="exploitation_type"):
            property_value=property_value.strip()
            if (property_value in ["wheel_roulette", "epsilon-LA", "best", "random"]):
                self.exploitation_type=property_value
            else:
                raise Exception("Błąd pliku konfiguracyjnego. %s może przyjmować wartości: wheel_roulette, eplsion-LA, best, random"%(property_name))
        elif (property_name=="tier2_mode"):

            self.tier2_mode=self.check_binary(property_value,property_name)

        elif (property_name=="prob_of_attack"):

            self.prob_of_attack=self.check_float(property_value,property_name,0,1.1,False)
        elif (property_name=="prob_of_return_to_T2"):

            self.prob_of_return_to_T2=self.check_float(property_value,property_name,0,1,False)

        elif (property_name=="v_of_uav"):

            self.v_of_uav=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="wait_time"):

            self.wiat_time=self.check_float(property_value,property_name,0,1,True)
        elif (property_name=="intuder_size"):

            self.intuder_size=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="uav_size"):

            self.uav_size=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="hand_size"):

            self.hand_size=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="velocity_hand"):

            self.velocity_hand=self.check_float(property_value,property_name,0,1,True)
        elif (property_name=="visualization_update_interval"):

            self.visualzation_update_interval=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="l_lr"):

            self.l_lr=self.check_int(property_value,property_name,1,1,True)
        elif (property_name=="is_directory"):

            self.is_directory=self.check_binary(property_value,property_name)

        elif (property_name=="r_of_LR"):

            self.r_of_LR=self.check_float(property_value,property_name,0,1,True)
            # if self.r_of_LR<self.intuder_size+self.uav_size:
            #     raise Exception("r_of_LR musi być większe niż intuder_size i uav_size")


        elif (property_name=="minimal_hand_move_time"):

            self.minimal_hand_move_time=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="intruder_time_of_reaction"):

            self.intruder_time_of_reaction=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="map_resolution"):

            self.map_resolution=self.check_float(property_value,property_name,0,1,True)

        elif (property_name=="seed"):

            self.seed=self.check_int(property_value,property_name,0,223,True)

        elif (property_name=="seed_clock"):

            self.seed_clock=self.check_binary(property_value,property_name)
        elif (property_name=="reward_threshold"):
            try:
                self.reward_threshold=self.check_float(property_value,property_name,0,1,True)
            except Exception as e:
                if float(property_value)==0.0:
                    self.reward_threshold=0
                else:
                    raise e

        elif (property_name=="blind_angle"):

            self.blind_angle=self.check_int(property_value,property_name,0,223,True)

        else:
            raise Exception("Błąd pliku konfiguracyjnego, nieznana nazwa właściwości:" +property_name)

    def get_list_of_points(self, file_with_rewards):
        list_of_cell_points:typing.List[PointsCell]=[]
        for record in file_with_rewards.readlines():
            if record[0]=="#":
                continue
            fields_list=record.split(" ")
            fields_list=list(filter("".__ne__,fields_list))
            for i,field in enumerate(fields_list):
                fields_list[i]=field.strip("\n")
            list_of_cell_points.append(PointsCell(int(fields_list[0]),int(fields_list[1]),int(fields_list[2]),float(fields_list[3])))
        return list_of_cell_points

    def get_boxes(self,file_with_boxes):
        record=file_with_boxes.readlines()
        field_list=record[0].split(" ")
        self.left_box=Point(float(field_list[0]),float(field_list[1]))
        field_list=record[1].split(" ")
        self.right_box=Point(float(field_list[0]),float(field_list[1]))

    def get_boxes_invisible(self,file_with_invisible):
        list_of_invisible:typing.List[PointsCell]=[]
        for record in file_with_invisible.readlines():

            fields_list=record.split(" ")
            list_of_invisible.append(PointsCell(int(fields_list[0]),int(fields_list[1]),int(fields_list[2]),0))
        return list_of_invisible

    def add_settings_to_csv(self,file):
        file.write("actual seed,%s\n"%(str(self.acutal_seed)))
        for record in self.list_to_print:

            file.write("%s,%s\n"%(record["name"],str(record["value"])))

    def add_settings_to_data_file(self,file):
        file.write("#actual seed=%s\n"%(str(self.acutal_seed)))
        for record in self.list_to_print:

            file.write("#%s=%s\n"%(record["name"],str(record["value"])))


