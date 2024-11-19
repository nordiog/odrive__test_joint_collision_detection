import odrive
from odrive.enums import *
import json
import time

def load_config(file_path):
    """Carica i parametri dal file di configurazione."""
    with open(file_path, 'r') as f:
        return json.load(f)

def configure_axis(axis, config):
    """Configura un singolo asse della scheda ODrive."""
    motor_cfg = config['motor_config']
    controller_cfg = config['controller_config']
    
    # Configurazione del motore
    axis.motor.config.current_lim = motor_cfg['max_current']
    axis.motor.config.pole_pairs = motor_cfg['pole_pairs']
    axis.motor.config.torque_constant = motor_cfg['torque_constant']

    # Configurazione del controller
    axis.controller.config.control_mode = controller_cfg['control_mode']
    axis.controller.config.pos_gain = controller_cfg['pos_gain']
    axis.controller.config.vel_gain = controller_cfg['vel_gain']
    axis.controller.config.vel_integrator_gain = controller_cfg['vel_integrator_gain']

    print(f"Asse configurato con successo: {axis}")

def configure_odrive(odrv, config):
    """Applica i parametri di configurazione a entrambe le assi della scheda ODrive."""
    axes_config = config['axes']
    for axis_num, axis_cfg in axes_config.items():
        print(f"Configurazione asse {axis_num}...")
        axis = getattr(odrv, f'axis{axis_num}')
        configure_axis(axis, axis_cfg)

def main():
    # Carica il file di configurazione
    config = load_config("config.json")

    print("Inizializzazione connessione ODrive...")
    odrv = odrive.find_any()  # Trova la scheda ODrive

    if odrv:
        print("ODrive trovato!")
        
        # Configura gli assi
        configure_odrive(odrv, config)

        print("Salvataggio dei parametri nella scheda...")
        odrv.save_configuration()
        print("Configurazione salvata con successo.")
    else:
        print("Errore: Impossibile trovare una scheda ODrive.")

if __name__ == "__main__":
    main()
