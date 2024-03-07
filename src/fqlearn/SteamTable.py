import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SteamTable:
    def __init__(self):
        """
        Initializes the SteamTable class by reading data from the CSV file and
        converting columns to numeric types.
        """
        self.table_data = pd.read_csv('src/data/tabla1-Saturation-Temperature.csv')

        # Convert columns to numeric types
        self.table_data['p'] = self.table_data['p'].str.replace(' ', '').astype(float)
        self.table_data['vV'] = self.table_data['vV'].str.replace(' ', '').astype(float)
        self.table_data['vL'] = self.table_data['vL'].str.replace(' ', '').astype(float)
        self.table_data['p'] = pd.to_numeric(self.table_data['p'], errors='coerce')
        self.table_data['vV'] = pd.to_numeric(self.table_data['vV'], errors='coerce')
        self.table_data['vL'] = pd.to_numeric(self.table_data['vL'], errors='coerce')

        # Create arrays
        self.t = np.array(self.table_data['t'])
        self.p = np.array(self.table_data['p'])
        self.vv = np.array(self.table_data['vV'])
        self.vl = np.array(self.table_data['vL'])
        self.dh = np.array(self.table_data['delta_h'])
        self.ds = np.array(self.table_data['delta_s'])

    def data(self):
        """
        Prints data in the table in chunks of 20 rows.
        """
        for i in range(0, len(self.table_data), 20):
            print(self.table_data.iloc[i:i+20])

    def point(self, t):
        """
        Prints the variables at a specific temperature.
        """
        indice_temperatura = np.where(self.table_data['t'] == t)[0]

        if len(indice_temperatura) > 0:
            # Si se encuentra la temperatura en la tabla, obtenemos el índice correspondiente
            indice_temperatura = indice_temperatura[0]

            # Obtener los valores de las variables
            p = self.table_data.loc[indice_temperatura, 'p']
            rhoL = self.table_data.loc[indice_temperatura, 'rhoL']
            rhoV = self.table_data.loc[indice_temperatura, 'rhoV']
            hL = self.table_data.loc[indice_temperatura, 'hL']
            hV = self.table_data.loc[indice_temperatura, 'hV']
            delta_h = self.table_data.loc[indice_temperatura, 'delta_h']
            sL = self.table_data.loc[indice_temperatura, 'sL']
            sV = self.table_data.loc[indice_temperatura, 'sV']
            delta_s = self.table_data.loc[indice_temperatura, 'delta_s']
            vL = self.table_data.loc[indice_temperatura, 'vL']
            vV = self.table_data.loc[indice_temperatura, 'vV']

            # Imprimir las variables
            print('Datos del punto requerido')
            print('Temperatura = {}[ºC]'.format(t))
            print('p = {}[MPa]'.format(p))
            print('rhoL = {}[kg/m^3]'.format(rhoL))
            print('rhoV = {}[kg/m^3]'.format(rhoV))
            print('hL = {}[KJ/kg]'.format(hL))
            print('hV = {}[KJ/kg]'.format(hV))
            print('delta_h = {}[KJ/kg]'.format(delta_h))
            print('sL = {}[KJ/(kg·K)]'.format(sL))
            print('sV = {}[KJ/(kg·K)]'.format(sV))
            print('delta_s = {}[KJ/(kg·K)]'.format(delta_s))
            print('vL = {}[cm^3/g]'.format(vL))
            print('vV = {}[cm^3/g]'.format(vV))
        else:
            print('No se encontró la temperatura {} en la tabla'.format(t))
            # Aquí se implementara una regresión para buscar el punto deseado

    def plot(self, variable):
        """
        Plots different diagrams based on the specified variable: PV, PT, or TV.
        """
        if variable == 'PV':
            # PV Diagram
            plt.plot(self.p, self.vv, label='Steam', color='blue')
            plt.plot(self.p, self.vl, '--', label='Liquid', color='green')
            plt.xlabel('Pressure (units)')
            plt.ylabel('Volume (units)')
            plt.title('PV Diagram')
            plt.legend(loc='upper right')
            plt.show()
        elif variable == 'PT':
            # PT Diagram
            plt.plot(self.p, self.t)
            plt.xlabel('Pressure (units)')
            plt.ylabel('Temperature (units)')
            plt.title('PT Diagram')
            plt.show()
        elif variable == 'TV':
            # TV Diagram
            plt.plot(self.t, self.vv, label='Steam', color='blue')
            plt.plot(self.t, self.vl, '--', label='Liquid', color='green')
            plt.xlabel('Temperature (units)')
            plt.ylabel('Volume (units)')
            plt.title('TV Diagram')
            plt.legend(loc='upper right')
            plt.show()
        else:
            print("Variable not recognized. Supported variables: PV, PT, TV")

    def plot3d(self):
        """
        Plots a 3D diagram based on pressure, temperature, and volume.
        """
        fig = plt.figure(dpi=200)
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.p, self.t, self.vv, label='Steam', color='blue')
        ax.scatter(self.p, self.t, self.vl, label='Liquid', color='green')
        ax.set_xlabel('Pressure (units)')
        ax.set_ylabel('Temperature (units)')
        ax.set_zlabel('Volume (units)')
        ax.set_title('3D Diagram')
        ax.legend()
        plt.show()
