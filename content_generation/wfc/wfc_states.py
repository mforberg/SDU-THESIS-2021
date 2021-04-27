from variables.wfc_variables import State, Pattern
import xml.etree.ElementTree as ET


class WfcStates:

    def create_2x2_states(self):

        states = {}

        mytree = ET.parse('wfc/configs/wfc_states.xml')
        myroot = mytree.getroot()

        # Find All States # TODO: I don't know if I need this :)
        x = myroot.findall('states')
        for z in x:
            test = z.findall('state')
            for p in test:
                print(p.get('name'))

        # Find All Neighbors to a State
        neighbors = myroot.findall('neighbors')
        for element in neighbors:
            parent_list = element.findall('parent')
            for parent in parent_list:
                key = parent.get('name')
                values = []
                legal_neighbors = parent.findall('neighbor')
                for ln in legal_neighbors:
                    values.append(ln.get('name'))
                states[key] = values
        print(states)
        return states
