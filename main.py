import subprocess
from time import sleep



# the class Network stores 
class Network:
    
    # creating a network
    def __init__(self, nw):
        # creates a class
        # @nw : string - the name of the network
        self.Network_name = nw  
        self.base_stations = []
        
    def print(self):
        # prints all the interface information we need
        print(self.Network_name)
        print("-----------------------")
        for item in self.base_stations:
            print(f"BSS:{item[0]} , RSSI:{item[1]}, Freq:{item[2]}, Rank:{item[3]}")
        
    # adding a Basestation to a Network
    def add_Ap(self,ap_line):
        # adds a basestation
        # @ap_line : string - adds a accesspoint 
        self.base_stations.append(ap_line)
        
    def get_base_Station(self):
        # returns the list of basestations
        return self.base_stations

####################################################################

class Save_obj:
    # the object to save the responses 
    def __init__(self, bssid):
        self.bssid = bssid
        self.information = {}
    def add_information(self,key, information):
        self.information[key] =information
    def get_information(self,key):
        return self.information[key]
####################################################################
def scan_for_networks(wlan_interface):
    # scanns for networks
    # @wlan_interface : string - the wlan interface we use to scan
    
    # creating all the variables we need
    all_networks = {}
    
    #scanning 
    subprocess.run(["iwctl","station", wlan_interface, "scan"])
    #waiting some time for the scan to get all of the APs
    #sleep(2)

    #getting all of the basestations
    return_value = subprocess.run(["iwctl","debug" , wlan_interface, "get-networks"],stdout= subprocess.PIPE ,text=True, )

    # preparing the list for seperation
    cleared_list= return_value.stdout.split("\n")
    #removing the first half
    #of unneded information with the header
    del cleared_list[0:4]
    
    # parsing the input
    current_network = ""
    for line in cleared_list:
        # filters the input 
        filtered_list = [x for x in line.split(" ") if not (x == '' or x =='\x1b[0m') ]
        if(len(filtered_list) ==1):
            # if we have another 
            current_network = filtered_list[0]
            all_networks[current_network] = (Network(current_network)) 
        #add all of the basstations
        if(len(filtered_list) == 5):

            all_networks[current_network].add_Ap(filtered_list)
    return all_networks


def scan_basestation(wlan_interface, base_station_id, waittime):
    # scans for a specific basestation
    # @wlan_interface : string - the wlan interface to use
    # @ base_station_id : string - the base_station to scan
    # @ waittime : int - the time for sleep while waiting betwen connecting
    
    # setting all of the options so that it stays connected to the 
    subprocess.run(["iwctl", "debug", wlan_interface,"autoconnect", "off"])
    # actually connects to the basestation
    subprocess.run(["iwctl", "debug", wlan_interface,"connect" ,base_station_id])
    
    #waiting some time for the dhcp to connect 
    sleep(waittime)
    
    #getting all of the information we needed  
    station_scan_result=subprocess.run(["iwctl", "station", wlan_interface, "show"], stdout=subprocess.PIPE, text=True)
    #deleting the unneded startstuff
    information_str =station_scan_result.stdout.split("\n")
    del information_str[0:4]
    # parsing the output into an object and into a dict
    for line in information_str:
        filtered_list = [x for x in line.split(" ") if not (x == '' or x.startswith('\x1b[0m'))]
        #skips empty lists
        if(filtered_list == []):
            continue
        print(filtered_list)
    #disconnecting from access point
    subprocess.run(["iwctl", "station", wlan_interface, "disconnect"])
    # returning the settings
    subprocess.run(["iwctl", "debug", wlan_interface,"autoconnect", "on"])


    
def main():
    print("Network Scanner")
    interface_name=input("Interface_name:")
    scan_results= scan_for_networks(interface_name)
    for key in scan_results.keys():
        scan_results[key].print()
        
    network_to_scan= input("Name of Network To Scan:")
    for bss in (scan_results["Gaesteresidenz"].get_base_Station()):
        print(bss[0])
        scan_basestation(interface_name, bss[0] ,30)
main()
