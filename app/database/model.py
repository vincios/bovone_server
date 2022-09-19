from sqlalchemy import Integer, Column, DateTime, Float, Float, Boolean

from . import Base


class Record(Base):
    __tablename__ = "record"
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, index=True)
    partial_meter_worked = Column(Float)  # Contametri Parziale (m)
    total_meter_worked = Column(Float) # Contametri Totale (m)
    conveyor_run = Column(Boolean)  # 1=traino in movimento 0=traino fermo
    conveyor_potentiometer_actual_read_points = Column(Float)  # Punti ingegneristici letti dal potenziometro della velocità
    conveyor_actual_value_in_mtmin = Column(Float)  # Velocità attuale in mt/min.
    glass_presence_in_machine = Column(Boolean)  # 1=presenza vetro in macchina 0=macchina vuota
    active_alarms_presence = Column(Boolean)  # 1=allarmi presenti 0=nessun allarme Ufficio Tecnico Elettrico Pag. 2
    thickness_potentiometer_points_read = Column(Float)  # Punti ingegneristici letti dal potenziometro dello spessore
    thickness_actual_value_in_mm = Column(Float)  # Valore attuale dello spessore in mm
    thickness_visualized_in_hmi = Column(Float)  # Spessore visualizzato su pannello operatore
    thickness_final_positioning_quote = Column(Float)  # Quota di posizionamento finale asse spessore
    remain_potentiometer_points_read = Column(Float)  # Punti ingegneristici letti dal potenziometro del tallone
    remain_actual_value_in_mm = Column(Float)  # Valore attuale del tallone in mm
    remain_visualized_in_hmi = Column(Float)  # Valore del tallone visualizzato a pannello
    remain_final_positioning_quote = Column(Float)  # Quota di posizionamento finale asse tallone
    angle_potentiometer_points_read = Column(Float)  # Punti ingegneristici letti dall’inclinometro dell’asse angolo
    angle_actual_value_in_mm = Column(Float)  # Valore attuale asse angolo in mm
    angle_visualized_in_hmi = Column(Float)  # Valore asse angolo visualizzato a pannello
    angle_final_positioning_quote = Column(Float)  # Quota di posizionamento finale asse angolo
    status_alarm_presence = Column(Integer)  # 1=allarmi presenti 0=macchina ok
    status_wheel_1_2 = Column(Integer)  # 0=mole ferme 1=mole in movimento 2=avaria
    status_wheel_3_4_5 = Column(Integer)  # 0=mole ferme 1=mole in movimento 2=avaria
    status_wheel_6_7 = Column(Integer)  # 0=mole_ferme_1=mole_in_movimento_2=avaria
    status_wheel_8_9 = Column(Integer)  # 0=mole ferme 1=mole in movimento 2=avaria
    status_wheel_10_11 = Column(Integer)  # 0=mole ferme 1=mole in movimento 2=avaria
    status_cooling_pump = Column(Integer)  # 0=pompa acqua raffreddamento ferma 1=pompa acqua raffreddamento accesa 2=pompa in avaria
    status_mixer_cerium = Column(Integer)  # 0=mixer cerio fermo 1=mixer cerio in movimento2=mixer cerio in avaria
    status_pump_cerium = Column(Integer)  # 0=pompa_cerio_ferma_1=pompa_cerio_accesa_2=pompa_cerio_in_avaria
    status_thickness_Axis = Column(Integer)  # 0=asse spessore fermo 1=asse spessore in movimento 2=asse spessore in avaria
    status_removal_axis = Column(Integer)  # (Optional) 0=asse asportazione automatica ferma 1=asse asportazione automatica in movimento 2=asse asportazione in avaria
    status_inclusion_exclusion_wheel_6 = Column(Integer)  # (Optional) 0=mola 6 esclusa 1=mola 6 inclusa
    status_brushes_motor_companion = Column(Integer)  # (Optional) 0=spazzole Companion ferme 1=spazzole Companion in movimento 2=avaria spazzole Companion
    status_fan_companion = Column(Integer)  # (Optional) 0=ventola Companion ferme 1=ventola Companion in movimento 2=avaria ventola Companion
    status_ev_h_2_o_companion = Column(Integer)  # (Optional) 1=EV H2O Companion Aperta 0=EV H2O Companion Chiusa
    status_image_visualized_on_hmi_angle_axis_quote = Column(Integer)  # Variabile utilizzata per il cambio della grafica a pannello asse angolo
    status_image_visualized_on_hmi_angle_axis = Column(Integer)  # Variabile utilizzata per il cambio della grafica a pannello asse angolo
