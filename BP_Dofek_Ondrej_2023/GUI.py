from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QPushButton, QLabel, QSpinBox, QWidget
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys
from petnetsim import PetriNet, Place, Transition, new_context
import petnetsim.json_io
from petnetsim import PetriNet
from petnetsim.elements import *
from petnetsim.json_io import loads, dumps
import matplotlib.pyplot as plt
import numpy as np

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi('GUI.ui', self)
        self.steps_spin = self.findChild(QSpinBox, 'steps_spin')
        self.min_spin = self.findChild(QSpinBox, 'min_spin')
        self.max_spin = self.findChild(QSpinBox, 'max_spin')
        self.c12_spin = self.findChild(QSpinBox, 'c12_spin')
        self.c23_spin = self.findChild(QSpinBox, 'c23_spin')
        self.c14_spin = self.findChild(QSpinBox, 'c14_spin')
        self.c25_spin = self.findChild(QSpinBox, 'c25_spin')
        self.c36_spin = self.findChild(QSpinBox, 'c36_spin')
        self.c45_spin = self.findChild(QSpinBox, 'c45_spin')
        self.c56_spin = self.findChild(QSpinBox, 'c56_spin')
        self.c47_spin = self.findChild(QSpinBox, 'c47_spin')
        self.c58_spin = self.findChild(QSpinBox, 'c58_spin')
        self.c69_spin = self.findChild(QSpinBox, 'c69_spin')
        self.c78_spin = self.findChild(QSpinBox, 'c78_spin')
        self.c89_spin = self.findChild(QSpinBox, 'c89_spin')

        self.start_button = self.findChild(QPushButton, 'start_button')
        self.kriz1_combo = self.findChild(QComboBox, f'kriz1_combo')
        self.kriz1_label = self.findChild(QLabel, 'kriz1_label')
        self.kriz2_combo = self.findChild(QComboBox, 'kriz2_combo')
        self.kriz2_label = self.findChild(QLabel, 'kriz2_label')
        self.kriz3_combo = self.findChild(QComboBox, 'kriz3_combo')
        self.kriz3_label = self.findChild(QLabel, 'kriz3_label')
        self.kriz4_combo = self.findChild(QComboBox, 'kriz4_combo')
        self.kriz4_label = self.findChild(QLabel, 'kriz4_label')
        self.kriz5_combo = self.findChild(QComboBox, 'kriz5_combo')
        self.kriz5_label = self.findChild(QLabel, 'kriz5_label')
        self.kriz6_combo = self.findChild(QComboBox, 'kriz6_combo')
        self.kriz6_label = self.findChild(QLabel, 'kriz6_label')
        self.kriz7_combo = self.findChild(QComboBox, 'kriz7_combo')
        self.kriz7_label = self.findChild(QLabel, 'kriz7_label')
        self.kriz8_combo = self.findChild(QComboBox, 'kriz8_combo')
        self.kriz8_label = self.findChild(QLabel, 'kriz8_label')
        self.kriz9_combo = self.findChild(QComboBox, 'kriz9_combo')
        self.kriz9_label = self.findChild(QLabel, 'kriz9_label')
        self.label12 = self.findChild(QLabel, 'label12')
        self.label21 = self.findChild(QLabel, 'label21')
        self.label23 = self.findChild(QLabel, 'label23')
        self.label32 = self.findChild(QLabel, 'label32')
        self.label54 = self.findChild(QLabel, 'label54')
        self.label45 = self.findChild(QLabel, 'label45')
        self.label56 = self.findChild(QLabel, 'label56')
        self.label65 = self.findChild(QLabel, 'label65')
        self.label87 = self.findChild(QLabel, 'label87')
        self.label78 = self.findChild(QLabel, 'label78')
        self.label89 = self.findChild(QLabel, 'label89')
        self.label98 = self.findChild(QLabel, 'label98')
        self.label14 = self.findChild(QLabel, 'label14')
        self.label41 = self.findChild(QLabel, 'label41')
        self.label25 = self.findChild(QLabel, 'label25')
        self.label52 = self.findChild(QLabel, 'label52')
        self.label36 = self.findChild(QLabel, 'label36')
        self.label63 = self.findChild(QLabel, 'label63')
        self.label47 = self.findChild(QLabel, 'label47')
        self.label74 = self.findChild(QLabel, 'label74')
        self.label58 = self.findChild(QLabel, 'label58')
        self.label85 = self.findChild(QLabel, 'label85')
        self.label69 = self.findChild(QLabel, 'label69')
        self.label96 = self.findChild(QLabel, 'label96')
        self.auta12 = self.findChild(QLabel, 'auta12')
        self.auta21 = self.findChild(QLabel, 'auta21')
        self.auta23 = self.findChild(QLabel, 'auta23')
        self.auta32 = self.findChild(QLabel, 'auta32')
        self.auta14 = self.findChild(QLabel, 'auta14')
        self.auta41 = self.findChild(QLabel, 'auta41')
        self.auta25 = self.findChild(QLabel, 'auta25')
        self.auta52 = self.findChild(QLabel, 'auta52')
        self.auta36 = self.findChild(QLabel, 'auta36')
        self.auta63 = self.findChild(QLabel, 'auta63')
        self.auta45 = self.findChild(QLabel, 'auta45')
        self.auta54 = self.findChild(QLabel, 'auta54')
        self.auta56 = self.findChild(QLabel, 'auta56')
        self.auta65 = self.findChild(QLabel, 'auta65')
        self.auta74 = self.findChild(QLabel, 'auta74')
        self.auta47 = self.findChild(QLabel, 'auta47')
        self.auta85 = self.findChild(QLabel, 'auta85')
        self.auta58 = self.findChild(QLabel, 'auta58')
        self.auta69 = self.findChild(QLabel, 'auta69')
        self.auta96 = self.findChild(QLabel, 'auta96')
        self.auta78 = self.findChild(QLabel, 'auta78')
        self.auta87 = self.findChild(QLabel, 'auta87')
        self.auta98 = self.findChild(QLabel, 'auta98')
        self.auta89 = self.findChild(QLabel, 'auta89')

        self.MWindow = self.findChild(QWidget, 'centralwidget')





        self.start_button.clicked.connect(self.run)
        #self.kriz4_combo.changeEvent(self.obr)
        self.kriz1_combo.activated.connect(self.obr)
        self.kriz2_combo.activated.connect(self.obr)
        self.kriz3_combo.activated.connect(self.obr)
        self.kriz4_combo.activated.connect(self.obr)
        self.kriz5_combo.activated.connect(self.obr)
        self.kriz6_combo.activated.connect(self.obr)
        self.kriz7_combo.activated.connect(self.obr)
        self.kriz8_combo.activated.connect(self.obr)
        self.kriz9_combo.activated.connect(self.obr)
        #self.start_button.clicked.connect(self.r)
        #self.label.setStyleSheet("color: rgb(255, 255, 0)")
        self.show()


    def obr(self):
        for i in range(1,10):
            self.krizX_label = self.findChild(QLabel, f'kriz{i}_label')
            self.krizX_combo = self.findChild(QComboBox, f'kriz{i}_combo')
            #print(self.krizX_label.name)
            x = self.krizX_combo.currentText()
            #print(i)
            #print(x)
            pixmap = QPixmap(f'krizovatky/ikony/{x}.png')
            self.krizX_label.setPixmap(pixmap)

    def run(self):
        self.label12.setStyleSheet("color : white")
        max_steps = self.steps_spin.value()
        p_min =self.min_spin.value()
        p_max =self.max_spin.value()
        c12 = self.c12_spin.value()
        c23 = self.c23_spin.value()
        c14 = self.c14_spin.value()
        c25 = self.c25_spin.value()
        c36 = self.c36_spin.value()
        c45 = self.c45_spin.value()
        c56 = self.c56_spin.value()
        c47 = self.c47_spin.value()
        c58 = self.c58_spin.value()
        c69 = self.c69_spin.value()
        c78 = self.c78_spin.value()
        c89 = self.c89_spin.value()
        p12 = Place('p12', capacity=c12)
        p21 = Place('p21', capacity=c12)
        p23 = Place('p23', capacity=c23)
        p32 = Place('p32', capacity=c23)
        p14 = Place('p14', capacity=c14)
        p41 = Place('p41', capacity=c14)
        p25 = Place('p25', capacity=c25)
        p52 = Place('p52', capacity=c25)
        p63 = Place('p63', capacity=c36)
        p36 = Place('p36', capacity=c36)
        p54 = Place('p54', capacity=c45)
        p45 = Place('p45', capacity=c45)
        p65 = Place('p65', capacity=c56)
        p56 = Place('p56', capacity=c56)
        p96 = Place('p96', capacity=c69)
        p69 = Place('p69', capacity=c69)
        p85 = Place('p85', capacity=c58)
        p58 = Place('p58', capacity=c58)
        p47 = Place('p47', capacity=c47)
        p74 = Place('p74', capacity=c47)
        p87 = Place('p87', capacity=c78)
        p78 = Place('p78', capacity=c78)
        p89 = Place('p89', capacity=c89)
        p98 = Place('p98', capacity=c89)







        places = [p12, p21, p23, p32, p41, p14, p25, p52, p36, p63, p45, p54, p56, p65, p47, p74, p58, p85, p69, p96, p78, p87, p89, p98]
        transitions = [TransitionTimed('PZ1', t_min=p_min, t_max=p_max), TransitionTimed('PZ2', t_min=p_min, t_max=p_max), TransitionTimed('PZ3', t_min=p_min, t_max=p_max),
                       TransitionTimed('PS1', t_min=p_min, t_max=p_max), TransitionTimed('PS2', t_min=p_min, t_max=p_max), TransitionTimed('PS3', t_min=p_min, t_max=p_max),
                       TransitionTimed('PJ1', t_min=p_min, t_max=p_max), TransitionTimed('PJ2', t_min=p_min, t_max=p_max), TransitionTimed('PJ3', t_min=p_min, t_max=p_max),
                       TransitionTimed('PV1', t_min=p_min, t_max=p_max), TransitionTimed('PV2', t_min=p_min, t_max=p_max), TransitionTimed('PV3', t_min=p_min, t_max=p_max),
                       Transition('T12'), Transition('T21'), Transition('T23'), Transition('T32'),
                       Transition('T14'), Transition('T41'), Transition('T25'), Transition('T52'),Transition('T63'), Transition('T36'),
                       Transition('T45'), Transition('T54'), Transition('T56'), Transition('T65'),
                       Transition('T47'), Transition('T74'), Transition('T58'), Transition('T85'), Transition('T69'), Transition('T96'),
                       Transition('T78'), Transition('T87'), Transition('T89'), Transition('T98'),
                       Transition('TT12'), Transition('TT21'), Transition('TT23'), Transition('TT32'),
                       Transition('TT14'), Transition('TT41'), Transition('TT25'), Transition('TT52'), Transition('TT63'),
                       Transition('TT36'),
                       Transition('TT45'), Transition('TT54'), Transition('TT56'), Transition('TT65'),
                       Transition('TT47'), Transition('TT74'), Transition('TT58'), Transition('TT85'), Transition('TT69'),
                       Transition('TT96'),
                       Transition('VV1'), Transition('VV2'), Transition('VV3'), Transition('VS1'), Transition('VS2'), Transition('VS3'), Transition('VJ1'), Transition('VJ2'), Transition('VJ3'), Transition('VZ1'), Transition('VZ2'), Transition('VZ3'),
                       Transition('TT78'), Transition('TT87'), Transition('TT89'), Transition('TT98')   ]
        arcs = [Arc('T12', p12), Arc(p12, 'TT12'), Arc('T21', p21), Arc(p21, 'TT21'), Arc('T23', p23), Arc(p23, 'TT23'), Arc('T32', p32), Arc(p32, 'TT32'),
                Arc('T14', p14), Arc(p14, 'TT14'), Arc('T41', p41), Arc(p41, 'TT41'), Arc('T25', p25), Arc(p25, 'TT25'), Arc('T52', p52), Arc(p52, 'TT52'), Arc('T36', p36), Arc(p36, 'TT36'), Arc('T63', p63), Arc(p63, 'TT63'),
                Arc('T45', p45), Arc(p45, 'TT45'), Arc('T54', p54), Arc(p54, 'TT54'), Arc('T56', p56), Arc(p56, 'TT56'), Arc('T65', p65), Arc(p65, 'TT65'),
                Arc('T47', p47), Arc(p47, 'TT47'), Arc('T74', p74), Arc(p74, 'TT74'), Arc('T58', p58), Arc(p58, 'TT58'), Arc('T85', p85), Arc(p85, 'TT85'), Arc('T69', p69), Arc(p69, 'TT69'), Arc('T96', p96), Arc(p96, 'TT96'),
                Arc('T78', p78), Arc(p78, 'TT78'), Arc('T87', p87), Arc(p87, 'TT87'), Arc('T89', p89), Arc(p89, 'TT89'), Arc('T98', p98), Arc(p98, 'TT98'),]






        global kriz
        krizovatka = ['fghjk','kriz1', 'kriz2', 'kriz3', 'kriz4', 'kriz5', 'kriz6', 'kriz7', 'kriz8', 'kriz9']
        for i in range(1, 10):

            self.krizX_combo = self.findChild(QComboBox, f'kriz{i}_combo')

            x = self.krizX_combo.currentText()
            print(x)
            if x == ('X_prednost_zprava'):
                subnet_ctx = new_context()
                with open('krizovatky/X_krizovatka.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)
            elif x == ('X_hlavni_SJ'):
                subnet_ctx = new_context()
                with open('krizovatky/X_krizovatka_SJ_hlavni.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)
            elif x == ('X_hlavni_ZV'):
                subnet_ctx = new_context()
                with open('krizovatky/X_krizovatka_ZV_hlavni.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)
            elif x == ('X_hlavni_JZ'):
                subnet_ctx = new_context()
                with open('krizovatky/X_krizovatka_JZ_hlavni.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)
            elif x == ('X_hlavni_JV'):
                subnet_ctx = new_context()
                with open('krizovatky/X_krizovatka_JV_hlavni.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)
            elif x == ('X_hlavni_SV'):
                subnet_ctx = new_context()
                with open('krizovatky/X_krizovatka_SV_hlavni.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)
            elif x == ('X_hlavni_SZ'):
                subnet_ctx = new_context()
                with open('krizovatky/X_krizovatka_SZ_hlavni.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)
            elif x == ('X_semafor'):
                subnet_ctx = new_context()
                with open('krizovatky/X_krizovatka_semafor.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)
            elif x == ('X_semafor_2proud'):
                subnet_ctx = new_context()
                with open('krizovatky/X_krizovatka_semafor_2proud.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)
            elif x == ('X_semafor_2proud_SJ'):
                subnet_ctx = new_context()
                with open('krizovatky/X_krizovatka_semafor_2proud_SJ.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)
            elif x == ('X_semafor_2proud_ZV'):
                subnet_ctx = new_context()
                with open('krizovatky/X_krizovatka_semafor_2proud_ZV.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)
            else:
                subnet_ctx = new_context()
                with open('krizovatky/Silnice.json') as f:
                    sn_places, sn_transitions, sn_arcs, _ = petnetsim.json_io.load(f, subnet_ctx)
                    kriz = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)

            krizovatka[i] = kriz




#krizovtka1
        cislo = 1
        prefix = f'{cislo}_'
        krizovatka[cislo].clone(prefix, places, transitions, arcs)
        arcs.append(('PZ1', prefix + 'z'))
        arcs.append(('PS1', prefix + 's'))
        arcs.append(('TT41', prefix + 'j'))
        arcs.append(('TT21', prefix + 'v'))
        arcs.append((prefix + 'ov', 'T12'))
        arcs.append((prefix + 'oj', 'T14'))
        arcs.append((prefix + 'oz', 'VZ1'))
        arcs.append((prefix + 'os', 'VS1'))
# krizovtka2
        cislo = 2
        prefix = f'{cislo}_'
        krizovatka[cislo].clone(prefix, places, transitions, arcs)
        arcs.append(('TT12', prefix + 'z'))
        arcs.append(('PS2', prefix + 's'))
        arcs.append(('TT52', prefix + 'j'))
        arcs.append(('TT32', prefix + 'v'))
        arcs.append((prefix + 'oz', 'T21'))
        arcs.append((prefix + 'oj', 'T25'))
        arcs.append((prefix + 'ov', 'T23'))
        arcs.append((prefix + 'os', 'VS2'))

# krizovtka3
        cislo = 3
        prefix = f'{cislo}_'
        krizovatka[cislo].clone(prefix, places, transitions, arcs)
        arcs.append(('TT23', prefix + 'z'))
        arcs.append(('PS3', prefix + 's'))
        arcs.append(('TT63', prefix + 'j'))
        arcs.append(('PV1', prefix + 'v'))
        arcs.append((prefix + 'oz', 'T32'))
        arcs.append((prefix + 'oj', 'T36'))
        arcs.append((prefix + 'ov', 'VV1'))
        arcs.append((prefix + 'os', 'VS3'))
# krizovtka4
        cislo = 4
        prefix = f'{cislo}_'
        krizovatka[cislo].clone(prefix, places, transitions, arcs)
        arcs.append(('PZ2', prefix + 'z'))
        arcs.append(('TT14', prefix + 's'))
        arcs.append(('TT74', prefix + 'j'))
        arcs.append(('TT54', prefix + 'v'))
        arcs.append((prefix + 'os', 'T41'))
        arcs.append((prefix + 'oj', 'T47'))
        arcs.append((prefix + 'ov', 'T45'))
        arcs.append((prefix + 'oz', 'VZ2'))

# krizovtka5
        cislo = 5
        prefix = f'{cislo}_'
        krizovatka[cislo].clone(prefix, places, transitions, arcs)
        arcs.append(('TT45', prefix + 'z'))
        arcs.append(('TT25', prefix + 's'))
        arcs.append(('TT85', prefix + 'j'))
        arcs.append(('TT65', prefix + 'v'))
        arcs.append((prefix + 'ov', 'T56'))
        arcs.append((prefix + 'oj', 'T58'))
        arcs.append((prefix + 'os', 'T52'))
        arcs.append((prefix + 'oz', 'T54'))
# krizovtka6
        cislo = 6
        prefix = f'{cislo}_'
        krizovatka[cislo].clone(prefix, places, transitions, arcs)
        arcs.append(('TT56', prefix + 'z'))
        arcs.append(('TT36', prefix + 's'))
        arcs.append(('TT96', prefix + 'j'))
        arcs.append(('PV2', prefix + 'v'))
        arcs.append((prefix + 'os', 'T63'))
        arcs.append((prefix + 'oj', 'T69'))
        arcs.append((prefix + 'oz', 'T65'))
        arcs.append((prefix + 'ov', 'VV2'))
# krizovtka7
        cislo = 7
        prefix = f'{cislo}_'
        krizovatka[cislo].clone(prefix, places, transitions, arcs)
        arcs.append(('PZ3', prefix + 'z'))
        arcs.append(('TT47', prefix + 's'))
        arcs.append(('PJ1', prefix + 'j'))
        arcs.append(('TT87', prefix + 'v'))
        arcs.append((prefix + 'ov', 'T78'))
        arcs.append((prefix + 'os', 'T74'))
        arcs.append((prefix + 'oj', 'VJ1'))
        arcs.append((prefix + 'oz', 'VZ3'))
# krizovtka8
        cislo = 8
        prefix = f'{cislo}_'
        krizovatka[cislo].clone(prefix, places, transitions, arcs)
        arcs.append(('TT78', prefix + 'z'))
        arcs.append(('TT58', prefix + 's'))
        arcs.append(('PJ2', prefix + 'j'))
        arcs.append(('TT98', prefix + 'v'))
        arcs.append((prefix + 'os', 'T85'))
        arcs.append((prefix + 'ov', 'T89'))
        arcs.append((prefix + 'oz', 'T87'))
        arcs.append((prefix + 'oj', 'VJ2'))

# krizovtka9
        cislo = 9
        prefix = f'{cislo}_'
        krizovatka[cislo].clone(prefix, places, transitions, arcs)
        arcs.append(('TT89', prefix + 'z'))
        arcs.append(('TT69', prefix + 's'))
        arcs.append(('PJ3', prefix + 'j'))
        arcs.append(('PV3', prefix + 'v'))
        arcs.append((prefix + 'os', 'T96'))
        arcs.append((prefix + 'oz', 'T98'))
        arcs.append((prefix + 'ov', 'VV3'))
        arcs.append((prefix + 'oj', 'VJ3'))



        global petri_net
        petri_net = PetriNet(places, transitions, arcs)
        print('conflict groups:', petri_net.conflict_groups_str)

        print('------------------------------------')
        print(' run')

        petri_net.reset()




        print('--------------- step', petri_net.step_num, 't', petri_net.time)
        petri_net.print_places()

        while not petri_net.ended and petri_net.step_num < max_steps:
            petri_net.step()
            #print('--------------- step', petri_net.step_num, 't', petri_net.time)
            petri_net.print_places()

            #print(petri_net.time, p21.tokens, p41.tokens, p12.tokens, p32.tokens,p52.tokens,p23.tokens, p63.tokens, p14.tokens, p54.tokens, p74.tokens, p45.tokens, p25.tokens, p65.tokens, p85.tokens, p56.tokens,p36.tokens,p96.tokens, p47.tokens, p87.tokens, p78.tokens,p58.tokens,p98.tokens, p89.tokens, p69.tokens, sep=':')
            self.label12.setStyleSheet(f"background-color: rgb({(p12.tokens/c12)*255}, 0, 0)")
            self.label21.setStyleSheet(f"background-color: rgb({(p21.tokens / c12) * 255}, 0, 0)")
            self.label23.setStyleSheet(f"background-color: rgb({(p23.tokens / c23) * 255}, 0, 0)")
            self.label32.setStyleSheet(f"background-color: rgb({(p32.tokens / c23) * 255}, 0, 0)")
            self.label45.setStyleSheet(f"background-color: rgb({(p45.tokens / c45) * 255}, 0, 0)")
            self.label54.setStyleSheet(f"background-color: rgb({(p54.tokens / c45) * 255}, 0, 0)")
            self.label56.setStyleSheet(f"background-color: rgb({(p56.tokens / c56) * 255}, 0, 0)")
            self.label65.setStyleSheet(f"background-color: rgb({(p65.tokens / c56) * 255}, 0, 0)")
            self.label78.setStyleSheet(f"background-color: rgb({(p78.tokens / c78) * 255}, 0, 0)")
            self.label87.setStyleSheet(f"background-color: rgb({(p87.tokens / c78) * 255}, 0, 0)")
            self.label89.setStyleSheet(f"background-color: rgb({(p89.tokens / c89) * 255}, 0, 0)")
            self.label98.setStyleSheet(f"background-color: rgb({(p98.tokens / c89) * 255}, 0, 0)")
            self.label14.setStyleSheet(f"background-color: rgb({(p14.tokens / c14) * 255}, 0, 0)")
            self.label41.setStyleSheet(f"background-color: rgb({(p41.tokens / c14) * 255}, 0, 0)")
            self.label25.setStyleSheet(f"background-color: rgb({(p25.tokens / c25) * 255}, 0, 0)")
            self.label52.setStyleSheet(f"background-color: rgb({(p52.tokens / c25) * 255}, 0, 0)")
            self.label36.setStyleSheet(f"background-color: rgb({(p36.tokens / c36) * 255}, 0, 0)")
            self.label63.setStyleSheet(f"background-color: rgb({(p63.tokens / c36) * 255}, 0, 0)")
            self.label47.setStyleSheet(f"background-color: rgb({(p47.tokens / c47) * 255}, 0, 0)")
            self.label74.setStyleSheet(f"background-color: rgb({(p74.tokens / c47) * 255}, 0, 0)")
            self.label58.setStyleSheet(f"background-color: rgb({(p58.tokens / c58) * 255}, 0, 0)")
            self.label85.setStyleSheet(f"background-color: rgb({(p85.tokens / c58) * 255}, 0, 0)")
            self.label69.setStyleSheet(f"background-color: rgb({(p69.tokens / c69) * 255}, 0, 0)")
            self.label96.setStyleSheet(f"background-color: rgb({(p96.tokens / c69) * 255}, 0, 0)")
            self.auta12.setText(str(p12.tokens))
            self.auta21.setText(str(p21.tokens))
            self.auta23.setText(str(p23.tokens))
            self.auta32.setText(str(p32.tokens))
            self.auta14.setText(str(p14.tokens))
            self.auta41.setText(str(p41.tokens))
            self.auta25.setText(str(p25.tokens))
            self.auta52.setText(str(p52.tokens))
            self.auta36.setText(str(p36.tokens))
            self.auta63.setText(str(p63.tokens))
            self.auta45.setText(str(p45.tokens))
            self.auta54.setText(str(p54.tokens))
            self.auta56.setText(str(p56.tokens))
            self.auta65.setText(str(p65.tokens))
            self.auta47.setText(str(p47.tokens))
            self.auta74.setText(str(p74.tokens))
            self.auta58.setText(str(p58.tokens))
            self.auta85.setText(str(p85.tokens))
            self.auta69.setText(str(p69.tokens))
            self.auta96.setText(str(p96.tokens))
            self.auta78.setText(str(p78.tokens))
            self.auta87.setText(str(p87.tokens))
            self.auta89.setText(str(p89.tokens))
            self.auta98.setText(str(p98.tokens))
            a = p23.tokens








            #ui = UI()
            #ui.setupUi(MainWindow)
            self.MWindow.repaint()

            #self.pv2_num.setText(n)


            #print('++++', n)
            #self.show()






        if petri_net.ended:
            print('  breaking condition')
        else:
            print('  max steps reached')

        print('--- transitions stats -------------------------')
        #for t in places:
            #print(t.name, t.tokens, sep=': ')
        #print('--- transitions stats -------------------------')
        #for t in transitions:
            #print(t.name, t.fired_times, sep=': ')


app = QApplication(sys.argv)
IUWindow = UI()
app.exec_()