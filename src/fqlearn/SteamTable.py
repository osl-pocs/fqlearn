import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SteamTable:
    def __init__(self):
        self.table_data = pd.read_csv('src/data/tabla1-Saturation-Temperature.csv')

        # Convertir columnas a tipos numéricos
        self.table_data['p'] = self.table_data['p'].str.replace(' ', '').astype(float)
        self.table_data['vV'] = self.table_data['vV'].str.replace(' ', '').astype(float)
        self.table_data['vL'] = self.table_data['vL'].str.replace(' ', '').astype(float)
        self.table_data['p'] = pd.to_numeric(self.table_data['p'], errors='coerce')
        self.table_data['vV'] = pd.to_numeric(self.table_data['vV'], errors='coerce')
        self.table_data['vL'] = pd.to_numeric(self.table_data['vL'], errors='coerce')

        # Crear arrays
        self.t = np.array(self.table_data['t'])
        self.p = np.array(self.table_data['p'])
        self.vv = np.array(self.table_data['vV'])
        self.vl = np.array(self.table_data['vL'])
        self.dh = np.array(self.table_data['delta_h'])
        self.ds = np.array(self.table_data['delta_s'])

    def data(self):
        for i in range(0, len(self.table_data), 20):
            print(self.table_data.iloc[i:i+20])

    def plot(self, variable):
        #plt.style.use('seaborn-darkgrid')  # Estilo consistente

        if variable == 'PV':
            plt.plot(self.p, self.vv, label='Steam', color='blue')
            plt.plot(self.p, self.vl, '--', label='Liquid', color='green')
            plt.xlabel('Pressure (units)')
            plt.ylabel('Volume (units)')
            plt.title('PV Diagram')
            plt.legend(loc='upper right')  
            plt.show()
        elif variable == 'PT':
            plt.plot(self.p, self.t)
            plt.xlabel('Pressure (units)')
            plt.ylabel('Temperature (units)')
            plt.title('PT Diagram')
            plt.show()
        elif variable == 'TV':
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


class State:
    def __init__(self, p=None, T=None):
        """
        Inicializa la clase State con la presión (p) y temperatura (T) especificadas.
        """

    def __call__(self, x=None):
        """
        Permite llamar a la instancia de la clase State con un valor opcional x.
        """