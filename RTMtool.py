import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import os
from typing import Dict, Any

class MoriaConfigEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Moria Server Config Editor")
        self.config_file = 'MoriaServerConfig.ini'
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create tabs
        self.basic_tab = ttk.Frame(self.notebook)
        self.difficulty_tab = ttk.Frame(self.notebook)
        self.network_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.basic_tab, text='Basic')
        self.notebook.add(self.difficulty_tab, text='Difficulty')
        self.notebook.add(self.network_tab, text='Network')
        
        # Initialize variables with correct section names
        self.vars: Dict[str, Dict[str, tk.StringVar]] = {
            'Main': {
                'OptionalPassword': tk.StringVar()
            },
            'World': {
                'Name': tk.StringVar()
            },
            'World.Create': {
                'Type': tk.StringVar(value='campaign'),
                'Seed': tk.StringVar(value='random'),
                'Difficulty.Preset': tk.StringVar(value='normal')
            },
            'World.Create.Difficulty.Custom': {
                'CombatDifficulty': tk.StringVar(value='default'),
                'EnemyAggression': tk.StringVar(value='default'),
                'SurvivalDifficulty': tk.StringVar(value='default'),
                'MiningDrops': tk.StringVar(value='default'),
                'WorldDrops': tk.StringVar(value='default'),
                'HordeFrequency': tk.StringVar(value='default'),
                'SiegeFrequency': tk.StringVar(value='default'),
                'PatrolFrequency': tk.StringVar(value='default')
            },
            'Console': {
                'Enabled': tk.StringVar(value='true')
            },
            'Performance': {
                'ServerFPS': tk.StringVar(value='60')
            },
            'Host': {
                'ListenAddress': tk.StringVar(),
                'ListenPort': tk.StringVar(value='7777'),
                'AdvertiseAddress': tk.StringVar(value='auto'),
                'AdvertisePort': tk.StringVar(value='-1'),
                'InitialConnectionRetryTime': tk.StringVar(value='60'),
                'AfterDisconnectionRetryTime': tk.StringVar(value='600')
            }
        }
        
        self.create_ui()
        self.load_config()
        
        # Save button
        ttk.Button(self.root, text="Save Configuration", 
                  command=self.save_config).pack(pady=10)

    def create_ui(self):
        self.create_basic_tab()
        self.create_difficulty_tab()
        self.create_network_tab()
        
    def create_basic_tab(self):
        basic_frame = ttk.LabelFrame(self.basic_tab, text="Basic Settings")
        basic_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(basic_frame, text="Optional Password:").pack(side='left', padx=5)
        ttk.Entry(basic_frame, textvariable=self.vars['Main']['OptionalPassword']).pack(side='left', padx=5)
        
        world_frame = ttk.LabelFrame(self.basic_tab, text="World Settings")
        world_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(world_frame, text="World Name:").pack(side='left', padx=5)
        ttk.Entry(world_frame, textvariable=self.vars['World']['Name']).pack(side='left', padx=5)
        
        world_create_frame = ttk.LabelFrame(self.basic_tab, text="World Create Settings")
        world_create_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(world_create_frame, text="World Type:").pack(side='left', padx=5)
        world_type_combo = ttk.Combobox(world_create_frame, textvariable=self.vars['World.Create']['Type'], values=['campaign', 'sandbox'])
        world_type_combo.pack(side='left', padx=5)
        
        ttk.Label(world_create_frame, text="World Seed:").pack(side='left', padx=5)
        ttk.Entry(world_create_frame, textvariable=self.vars['World.Create']['Seed']).pack(side='left', padx=5)
        
        console_frame = ttk.LabelFrame(self.basic_tab, text="Console Settings")
        console_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(console_frame, text="Console Enabled:").pack(side='left', padx=5)
        console_enabled_combo = ttk.Combobox(console_frame, textvariable=self.vars['Console']['Enabled'], values=['true', 'false'])
        console_enabled_combo.pack(side='left', padx=5)
        
        performance_frame = ttk.LabelFrame(self.basic_tab, text="Performance Settings")
        performance_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(performance_frame, text="Server FPS:").pack(side='left', padx=5)
        ttk.Entry(performance_frame, textvariable=self.vars['Performance']['ServerFPS']).pack(side='left', padx=5)
        
    def create_difficulty_tab(self):
        # Difficulty preset
        preset_frame = ttk.LabelFrame(self.difficulty_tab, text="Difficulty Preset")
        preset_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(preset_frame, text="Preset:").pack(side='left', padx=5)
        preset_combo = ttk.Combobox(preset_frame, 
                                  textvariable=self.vars['World.Create']['Difficulty.Preset'],
                                  values=['story', 'solo', 'normal', 'hard', 'custom'])
        preset_combo.pack(side='left', padx=5)
        preset_combo.bind('<<ComboboxSelected>>', self.toggle_custom_difficulty)
        
        # Custom difficulty options
        self.custom_frame = ttk.LabelFrame(self.difficulty_tab, text="Custom Difficulty")
        self.custom_frame.pack(fill='x', padx=5, pady=5)
        
        row = 0
        for setting, var in self.vars['World.Create.Difficulty.Custom'].items():
            ttk.Label(self.custom_frame, text=setting).grid(row=row, column=0, padx=5, pady=2)
            combo = ttk.Combobox(self.custom_frame, textvariable=var,
                               values=['verylow', 'low', 'default', 'high', 'veryhigh'],
                               state='disabled')
            combo.grid(row=row, column=1, padx=5, pady=2)
            row += 1
            
    def create_network_tab(self):
        network_frame = ttk.LabelFrame(self.network_tab, text="Network Settings")
        network_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(network_frame, text="Listen Address:").grid(row=0, column=0, padx=5, pady=2, sticky='w')
        ttk.Entry(network_frame, textvariable=self.vars['Host']['ListenAddress']).grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        
        ttk.Label(network_frame, text="Listen Port:").grid(row=1, column=0, padx=5, pady=2, sticky='w')
        ttk.Entry(network_frame, textvariable=self.vars['Host']['ListenPort']).grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        
        ttk.Label(network_frame, text="Advertise Address:").grid(row=2, column=0, padx=5, pady=2, sticky='w')
        ttk.Entry(network_frame, textvariable=self.vars['Host']['AdvertiseAddress']).grid(row=2, column=1, padx=5, pady=2, sticky='ew')
        
        ttk.Label(network_frame, text="Advertise Port:").grid(row=3, column=0, padx=5, pady=2, sticky='w')
        ttk.Entry(network_frame, textvariable=self.vars['Host']['AdvertisePort']).grid(row=3, column=1, padx=5, pady=2, sticky='ew')
        
        ttk.Label(network_frame, text="Initial Connection Retry Time:").grid(row=4, column=0, padx=5, pady=2, sticky='w')
        ttk.Entry(network_frame, textvariable=self.vars['Host']['InitialConnectionRetryTime']).grid(row=4, column=1, padx=5, pady=2, sticky='ew')
        
        ttk.Label(network_frame, text="After Disconnection Retry Time:").grid(row=5, column=0, padx=5, pady=2, sticky='w')
        ttk.Entry(network_frame, textvariable=self.vars['Host']['AfterDisconnectionRetryTime']).grid(row=5, column=1, padx=5, pady=2, sticky='ew')
        
        network_frame.columnconfigure(1, weight=1)

    def toggle_custom_difficulty(self, event=None):
        state = 'normal' if self.vars['World.Create']['Difficulty.Preset'].get() == 'custom' else 'disabled'
        for child in self.custom_frame.winfo_children():
            if isinstance(child, ttk.Combobox):
                child.configure(state=state)

    def load_config(self):
        if not os.path.exists(self.config_file):
            return
            
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        # Load basic settings
        if 'Main' in config:
            self.vars['Main']['OptionalPassword'].set(config['Main'].get('OptionalPassword', ''))
        if 'World' in config:
            self.vars['World']['Name'].set(config['World'].get('Name', ''))
        
        # Load difficulty settings
        if 'World.Create' in config:
            self.vars['World.Create']['Type'].set(config['World.Create'].get('Type', 'campaign'))
            self.vars['World.Create']['Seed'].set(config['World.Create'].get('Seed', 'random'))
            self.vars['World.Create']['Difficulty.Preset'].set(
                config['World.Create'].get('Difficulty.Preset', 'normal'))
            
            # Load custom difficulty settings
            for setting in self.vars['World.Create.Difficulty.Custom']:
                value = config['World.Create'].get(f'Difficulty.Custom.{setting}', 'default')
                self.vars['World.Create.Difficulty.Custom'][setting].set(value)
        
        # Load console settings
        if 'Console' in config:
            self.vars['Console']['Enabled'].set(config['Console'].get('Enabled', 'true'))
        
        # Load performance settings
        if 'Performance' in config:
            self.vars['Performance']['ServerFPS'].set(config['Performance'].get('ServerFPS', '60'))
            
        # Load host settings
        if 'Host' in config:
            self.vars['Host']['ListenAddress'].set(config['Host'].get('ListenAddress', ''))
            self.vars['Host']['ListenPort'].set(config['Host'].get('ListenPort', '7777'))
            self.vars['Host']['AdvertiseAddress'].set(config['Host'].get('AdvertiseAddress', 'auto'))
            self.vars['Host']['AdvertisePort'].set(config['Host'].get('AdvertisePort', '-1'))
            self.vars['Host']['InitialConnectionRetryTime'].set(config['Host'].get('InitialConnectionRetryTime', '60'))
            self.vars['Host']['AfterDisconnectionRetryTime'].set(config['Host'].get('AfterDisconnectionRetryTime', '600'))
        
        self.toggle_custom_difficulty()

    def save_config(self):
        try:
            with open(self.config_file, 'r') as f:
                lines = f.readlines()
            
            # Update values while preserving comments
            for i, line in enumerate(lines):
                if '=' in line:
                    key = line.split('=')[0].strip()
                    
                    # Handle basic settings
                    if key == 'OptionalPassword' and 'Main' in self.vars:
                        value = self.vars['Main']['OptionalPassword'].get()
                        lines[i] = f"{key}={value}\n"
                    elif key == 'Name' and 'World' in self.vars:
                        value = self.vars['World']['Name'].get()
                        lines[i] = f"{key}={value}\n"
                    
                    # Handle world create settings
                    elif key == 'Type' and 'World.Create' in self.vars:
                        value = self.vars['World.Create']['Type'].get()
                        lines[i] = f"{key}={value}\n"
                    elif key == 'Seed' and 'World.Create' in self.vars:
                        value = self.vars['World.Create']['Seed'].get()
                        lines[i] = f"{key}={value}\n"
                    
                    # Handle custom difficulty settings
                    elif key.startswith('Difficulty.Custom.'):
                        setting = key.split('.')[-1]
                        if setting in self.vars['World.Create.Difficulty.Custom']:
                            value = self.vars['World.Create.Difficulty.Custom'][setting].get()
                            lines[i] = f"{key}={value}\n"
                    
                    # Handle difficulty preset
                    elif key == 'Difficulty.Preset' and 'World.Create' in self.vars:
                        value = self.vars['World.Create']['Difficulty.Preset'].get()
                        lines[i] = f"{key}={value}\n"
                    
                    # Handle console settings
                    elif key == 'Enabled' and 'Console' in self.vars:
                        value = self.vars['Console']['Enabled'].get()
                        lines[i] = f"{key}={value}\n"
                    
                    # Handle performance settings
                    elif key == 'ServerFPS' and 'Performance' in self.vars:
                        value = self.vars['Performance']['ServerFPS'].get()
                        lines[i] = f"{key}={value}\n"
                    
                    # Handle host settings
                    elif key == 'ListenAddress' and 'Host' in self.vars:
                        value = self.vars['Host']['ListenAddress'].get()
                        lines[i] = f"{key}={value}\n"
                    elif key == 'ListenPort' and 'Host' in self.vars:
                        value = self.vars['Host']['ListenPort'].get()
                        lines[i] = f"{key}={value}\n"
                    elif key == 'AdvertiseAddress' and 'Host' in self.vars:
                        value = self.vars['Host']['AdvertiseAddress'].get()
                        lines[i] = f"{key}={value}\n"
                    elif key == 'AdvertisePort' and 'Host' in self.vars:
                        value = self.vars['Host']['AdvertisePort'].get()
                        lines[i] = f"{key}={value}\n"
                    elif key == 'InitialConnectionRetryTime' and 'Host' in self.vars:
                        value = self.vars['Host']['InitialConnectionRetryTime'].get()
                        lines[i] = f"{key}={value}\n"
                    elif key == 'AfterDisconnectionRetryTime' and 'Host' in self.vars:
                        value = self.vars['Host']['AfterDisconnectionRetryTime'].get()
                        lines[i] = f"{key}={value}\n"
            
            with open(self.config_file, 'w') as f:
                f.writelines(lines)
            
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving config: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MoriaConfigEditor()
    app.run()