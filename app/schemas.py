import datetime
import os
from typing import Union
from pydantic import BaseModel, BaseSettings

RECORD_HEADERS = [
    "date_hour_day",
    "date_hour_month",
    "date_hour_year",
    "date_hour_hour",
    "date_hour_minute",
    "date_hour_second",
    "date_hour_weekday",
    "partial_meter_worked",
    "total_meter_worked",
    "conveyor_run",
    "conveyor_potentiometer_actual_read_points",
    "conveyor_actual_value_in_mtmin",
    "glass_presence_in_machine",
    "active_alarms_presence",
    "thickness_potentiometer_points_read",
    "thickness_actual_value_in_mm",
    "thickness_visualized_in_hmi",
    "thickness_final_positioning_quote",
    "remain_potentiometer_points_read",
    "remain_actual_value_in_mm",
    "remain_visualized_in_hmi",
    "remain_final_positioning_quote",
    "angle_potentiometer_points_read",
    "angle_actual_value_in_mm",
    "angle_visualized_in_hmi",
    "angle_final_positioning_quote",
    "status_alarm_presence",
    "status_wheel_1_2",
    "status_wheel_3_4_5",
    "status_wheel_6_7",
    "status_wheel_8_9",
    "status_wheel_10_11",
    "status_cooling_pump",
    "status_mixer_cerium",
    "status_pump_cerium",
    "status_thickness_Axis",
    "status_removal_axis",
    "status_inclusion_exclusion_wheel_6",
    "status_brushes_motor_companion",
    "status_fan_companion",
    "status_ev_h_2_o_companion",
    "status_image_visualized_on_hmi_angle_axis_quote",
    "status_image_visualized_on_hmi_angle_axis",
]


class RecordSchema(BaseModel):
    """
    Representation of a record of the bovone statistics csv file
    """
    @classmethod
    def from_csv_line(cls, line):
        line_dict = dict(zip(RECORD_HEADERS, line))
        record_time = datetime.datetime(year=int(line_dict['date_hour_year']), month=int(line_dict['date_hour_month']),
                                        day=int(line_dict['date_hour_day']), hour=int(line_dict['date_hour_hour']),
                                        minute=int(line_dict['date_hour_minute']), second=int(line_dict['date_hour_second']))
        line_dict['time'] = record_time
        return cls.parse_obj(line_dict)

    class Config:
        orm_mode = True

    time: datetime.datetime
    partial_meter_worked: Union[int, float]  # Contametri Parziale (m)
    total_meter_worked: Union[int, float]  # Contametri Totale (m)
    conveyor_run: bool  # 1=traino in movimento 0=traino fermo
    conveyor_potentiometer_actual_read_points: Union[int, float]  # Punti ingegneristici letti dal potenziometro della velocità
    conveyor_actual_value_in_mtmin: Union[int, float]  # Velocità attuale in mt/min.
    glass_presence_in_machine: bool  # 1=presenza vetro in macchina 0=macchina vuota
    active_alarms_presence: bool  # 1=allarmi presenti 0=nessun allarme Ufficio Tecnico Elettrico Pag. 2
    thickness_potentiometer_points_read: Union[int, float]  # Punti ingegneristici letti dal potenziometro dello spessore
    thickness_actual_value_in_mm: Union[int, float]  # Valore attuale dello spessore in mm
    thickness_visualized_in_hmi: Union[int, float]  # Spessore visualizzato su pannello operatore
    thickness_final_positioning_quote: Union[int, float]  # Quota di posizionamento finale asse spessore
    remain_potentiometer_points_read: Union[int, float]  # Punti ingegneristici letti dal potenziometro del tallone
    remain_actual_value_in_mm: Union[int, float]  # Valore attuale del tallone in mm
    remain_visualized_in_hmi: Union[int, float]  # Valore del talloniiiiiiiiiiiue visualizzato a pannello
    remain_final_positioning_quote: Union[int, float]  # Quota di posizionamento finale asse tallone
    angle_potentiometer_points_read: Union[int, float]  # Punti ingegneristici letti dall’inclinometro dell’asse angolo
    angle_actual_value_in_mm: Union[int, float]  # Valore attuale asse angolo in mm
    angle_visualized_in_hmi: Union[int, float]  # Valore asse angolo visualizzato a pannello
    angle_final_positioning_quote: Union[int, float]  # Quota di posizionamento finale asse angolo
    status_alarm_presence: int  # 1=allarmi presenti 0=macchina ok
    status_wheel_1_2: int  # 0=mole ferme 1=mole in movimento 2=avaria
    status_wheel_3_4_5: int  # 0=mole ferme 1=mole in movimento 2=avaria
    status_wheel_6_7: int  # 0=mole_ferme_1=mole_in_movimento_2=avaria
    status_wheel_8_9: int  # 0=mole ferme 1=mole in movimento 2=avaria
    status_wheel_10_11: int  # 0=mole ferme 1=mole in movimento 2=avaria
    status_cooling_pump: int  # 0=pompa acqua raffreddamento ferma 1=pompa acqua raffreddamento accesa 2=pompa in avaria
    status_mixer_cerium: int  # 0=mixer cerio fermo 1=mixer cerio in movimento2=mixer cerio in avaria
    status_pump_cerium: int  # 0=pompa_cerio_ferma_1=pompa_cerio_accesa_2=pompa_cerio_in_avaria
    status_thickness_Axis: int  # 0=asse spessore fermo 1=asse spessore in movimento 2=asse spessore in avaria
    status_removal_axis: int  # (Optional) 0=asse asportazione automatica ferma 1=asse asportazione automatica in movimento 2=asse asportazione in avaria
    status_inclusion_exclusion_wheel_6: int  # (Optional) 0=mola 6 esclusa 1=mola 6 inclusa
    status_brushes_motor_companion: int  # (Optional) 0=spazzole Companion ferme 1=spazzole Companion in movimento 2=avaria spazzole Companion
    status_fan_companion: int  # (Optional) 0=ventola Companion ferme 1=ventola Companion in movimento 2=avaria ventola Companion
    status_ev_h_2_o_companion: int  # (Optional) 1=EV H2O Companion Aperta 0=EV H2O Companion Chiusa
    status_image_visualized_on_hmi_angle_axis_quote: int = 0  # Variabile utilizzata per il cambio della grafica a pannello asse angolo
    status_image_visualized_on_hmi_angle_axis: int = 0 # Variabile utilizzata per il cambio della grafica a pannello asse angolo


class DBRecordSchema(RecordSchema):
    id: int

    class Config:
        orm_mode = True
