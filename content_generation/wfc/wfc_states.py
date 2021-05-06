from models.wfc_models import State, Pattern
import xml.etree.ElementTree as ET


class WfcStates:

    def create_3x3_states(self):

        weights = {}
        states = {}

        mytree = ET.parse('wfc/configs/wfc_states.xml')
        myroot = mytree.getroot()

        # Find All States # TODO: I don't know if I need this :)
        x = myroot.findall('states')
        for z in x:
            test = z.findall('state')
            for p in test:
                try:
                    weights[p.get('name')] = int(p.get('weight'))
                except ValueError:
                    print("Could not parse weight to int")


        # Find All Neighbors to a State
        neighbors = myroot.findall('neighbors')
        for element in neighbors:
            parent_list = element.findall('parent')
            for parent in parent_list:
                key = parent.get('name')
                # values = []
                # legal_neighbors = parent.findall('neighbor')
                # for ln in legal_neighbors:
                #     values.append(ln.get('name'))
                # states[key] = values
                values = {}
                legal_neighbors = parent.findall('neighbor')
                for ln in legal_neighbors:
                    values[ln.get('name')] = [char for char in ln.get('legal')]

                states[key] = values
        return weights, states
