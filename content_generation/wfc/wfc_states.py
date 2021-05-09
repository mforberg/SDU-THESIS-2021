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

    def create_simple_3x3_states(self):

        weights = {}
        states = {}
        required = {}
        requires = {}

        mytree = ET.parse('wfc/configs/wfc_simple_states.xml')
        myroot = mytree.getroot()

        # Find All States # TODO: I don't know if I need this :)
        x = myroot.findall('states')
        for z in x:
            test = z.findall('state')
            for p in test:
                try:
                    weights[p.get('name')] = int(p.get('weight'))
                    requires[p.get('name')] = [char for char in p.get('requires')]
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
                    required[ln.get('name')] = ln.get('required')

                states[key] = values
        return weights, states, requires

    def create_simplest_3x3_states(self):

        weights = {}
        states = {}
        required = {}
        requires = {}

        mytree = ET.parse('wfc/configs/wfc_simplest_states.xml')
        myroot = mytree.getroot()

        # Find All States # TODO: I don't know if I need this :)
        x = myroot.findall('states')
        for z in x:
            test = z.findall('state')
            for p in test:
                try:
                    weights[p.get('name')] = int(p.get('weight'))
                    requires[p.get('name')] = [char for char in p.get('requires')]
                except ValueError:
                    print("Could not parse weight to int")


        # Find All Neighbors to a State
        neighbors = myroot.findall('neighbors')
        for element in neighbors:
            parent_list = element.findall('parent')
            for parent in parent_list:
                key = parent.get('name')

                values = {}
                legal_neighbors = parent.findall('neighbor')
                for ln in legal_neighbors:
                    values[ln.get('name')] = [char for char in ln.get('legal')]
                    required[ln.get('name')] = ln.get('required')

                states[key] = values
        return weights, states, requires
