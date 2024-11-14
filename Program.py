# IMPORT PYOMO
from pyomo.environ  import ConcreteModel, Var, Objective, Constraint, NonNegativeReals, Set, Param
import pyomo.environ as pyo
from pyomo.opt import SolverFactory 
from pyomo import *

# Definisikan Model
model = ConcreteModel()

'''Stakeholder'''
# Definisikan Set Stakeholder
model.I = Set(initialize=['Manufaktur 1', 'Manufaktur 2'])
model.J = Set(initialize=['Distributor 1', 'Distributor 2'])
model.K = Set(initialize=['Konsumen 1', 'Konsumen 2', 'Konsumen 3', 'Konsumen 4'])
model.L = Set(initialize=['Pengumpulan 1', 'Pengumpulan 2'])
model.M = Set(initialize=['Pembuangan 1', 'Pembuangan 2'])
model.S = Set(initialize=['Sekunder 1', 'Sekunder 2', 'Sekunder 3', 'Sekunder 4'])

# Definisikan Parameter Jarak Masing-Masing Stakeholder
# Jarak antara Manufaktur dan Distributor (I dan J)
model.distance_IJ = Param(model.I, model.J, initialize={
    ('Manufaktur 1', 'Distributor 1'): 150,
    ('Manufaktur 1', 'Distributor 2'): 400,
    ('Manufaktur 2', 'Distributor 1'): 200,
    ('Manufaktur 2', 'Distributor 2'): 500
}, mutable=True)

# Jarak antara Distributor dan Konsumen (J dan K)
model.distance_JK = Param(model.J, model.K, initialize={
    ('Distributor 1', 'Konsumen 1'): 100,
    ('Distributor 1', 'Konsumen 2'): 150,
    ('Distributor 1', 'Konsumen 3'): 250,
    ('Distributor 1', 'Konsumen 4'): 350,
    ('Distributor 2', 'Konsumen 1'): 350,
    ('Distributor 2', 'Konsumen 2'): 200,
    ('Distributor 2', 'Konsumen 3'): 125,
    ('Distributor 2', 'Konsumen 4'): 175
}, mutable=True)

# Jarak antara Konsumen dan Pengumpulan (K dan L)
model.distance_KL = Param(model.K, model.L, initialize={
    ('Konsumen 1', 'Pengumpulan 1'): 90,
    ('Konsumen 1', 'Pengumpulan 2'): 95,
    ('Konsumen 2', 'Pengumpulan 1'): 92,
    ('Konsumen 2', 'Pengumpulan 2'): 91,
    ('Konsumen 3', 'Pengumpulan 1'): 90,
    ('Konsumen 3', 'Pengumpulan 2'): 93,
    ('Konsumen 4', 'Pengumpulan 1'): 92,
    ('Konsumen 4', 'Pengumpulan 2'): 91
}, mutable=True)

# Jarak antara Pengumpulan dan Manufaktur (L dan I)
model.distance_LI = Param(model.L, model.I, initialize={
    ('Pengumpulan 1', 'Manufaktur 1'): 200,
    ('Pengumpulan 1', 'Manufaktur 2'): 400,
    ('Pengumpulan 2', 'Manufaktur 1'): 250,
    ('Pengumpulan 2', 'Manufaktur 2'): 650
}, mutable=True)

# Jarak antara Pengumpulan dan Pembuangan (L dan M)
model.distance_LM = Param(model.L, model.M, initialize={
    ('Pengumpulan 1', 'Pembuangan 1'): 350,
    ('Pengumpulan 1', 'Pembuangan 2'): 500,
    ('Pengumpulan 2', 'Pembuangan 1'): 250,
    ('Pengumpulan 2', 'Pembuangan 2'): 750
}, mutable=True)

# Jarak antara Manufaktur dan Sekunder (I dan N)
model.distance_IS = Param(model.I, model.S, initialize={
    ('Manufaktur 1', 'Sekunder 1'): 110,
    ('Manufaktur 1', 'Sekunder 2'): 115,
    ('Manufaktur 1', 'Sekunder 3'): 120,
    ('Manufaktur 1', 'Sekunder 4'): 125,
    ('Manufaktur 2', 'Sekunder 1'): 110,
    ('Manufaktur 2', 'Sekunder 2'): 115,
    ('Manufaktur 2', 'Sekunder 3'): 120,
    ('Manufaktur 2', 'Sekunder 4'): 125
}, mutable=True)

# Jarak antara Sekunder dan Konsumen (N dan L)
model.distance_SL = Param(model.S, model.L, initialize={
    ('Sekunder 1', 'Pengumpulan 1'): 150,
    ('Sekunder 1', 'Pengumpulan 2'): 160,
    ('Sekunder 2', 'Pengumpulan 1'): 200,
    ('Sekunder 2', 'Pengumpulan 2'): 155,
    ('Sekunder 3', 'Pengumpulan 1'): 150,
    ('Sekunder 3', 'Pengumpulan 2'): 152,
    ('Sekunder 4', 'Pengumpulan 1'): 190,
    ('Sekunder 4', 'Pengumpulan 2'): 175
}, mutable=True)

# Definisikan Set Kendaraan
model.V = Set(initialize=["Truck", "Trailer"])

# Definisikan Parameter Kapasitas Kendaraan
model.vehicle_capacity= Param(model.V, initialize={
    'Truck': 11, 
    'Traier': 25
    })

# Definiskan Cost Transportasi per 1 Unit
# Definisikan ongkos per kendaraan untuk rute tertentu dari Pengumpulan ke Manufaktur
# Jika Distance Matter
# model.cost_VLI = Param(model.V, model.L, model.I, initialize={
#     ('Truck', 'Pengumpulan 1', 'Manufaktur 1'): 500,
#     ('Truck', 'Pengumpulan 1', 'Manufaktur 2'): 800,
#     ('Truck', 'Pengumpulan 2', 'Manufaktur 1'): 600,
#     ('Truck', 'Pengumpulan 2', 'Manufaktur 2'): 1000,
#     ('Trailer', 'Pengumpulan 1', 'Manufaktur 1'): 700,
#     ('Trailer', 'Pengumpulan 1', 'Manufaktur 2'): 1200,
#     ('Trailer', 'Pengumpulan 2', 'Manufaktur 1'): 900,
#     ('Trailer', 'Pengumpulan 2', 'Manufaktur 2'): 1500
# }, mutable=True)

# Jika Distance Doesnt Matter
model.vehicle_cost= Param(model.V, initialize={
    'Truck': 5, 
    'Traier': 10
    })

# Definisikan Parameter COST (MANUFAKTUR)
# 1. PCi
model.PCi = Param(model.I, initialize={
    'Manufaktur 1' : 12.5,
    'Manufaktur 2' : 19.5,
})

# 2. CRe
model.CRe = Param(model.I, initialize={
    'Manufaktur 1' : 8,
    'Manufaktur 2' : 13,
})

# 3.Beta
model.Beta = Param(model.I, initialize={
    'Manufaktur 1' : 0.1,
    'Manufaktur 2' : 0.3,
})

# 4. Pngi
model.Pngi = Param(model.I, initialize={
    'Manufaktur 1' : 50,
    'Manufaktur 2' : 55,
})

# 5. Q
model.q = Param(model.I, initialize={
    'Manufaktur 1' : 0.3,
    'Manufaktur 2' : 0.5,
})

# 6. B
model.b = Param(model.I, initialize={
    'Manufaktur 1' : 0.1,
    'Manufaktur 2' : 0.3,
})

# 7. DD
model.dd = Param(model.I, initialize={
    'Manufaktur 1' : 0.3,
    'Manufaktur 2' : 0.5,
})

# Definisikan Parameter COST (PASAR SEKUNDER)
# 1. Csr
model.Csr = Param(model.S, initialize={
    'Sekunder 1' : 30,
    'Sekunder 2' : 35,
    'Sekunder 3' : 45,
    'Sekunder 4' : 50
})

# Definisikan Parameter COST (DISTRIBUTOR)
# 1. Coj
model.Coj = Param(model.J, initialize={
    'Distributor 1' : 5,
    'Distributor 2' : 8,
})

# Definisikan Parameter COST (PENGUMPULAN)
# 1. Ccl
model.Ccl = Param(model.L, initialize={
    'Pengumpulan 1' : 13,
    'Pengumpulan 2' : 17,
})

# 2. Fcl
model.Fcl = Param(model.L, initialize={
    'Pengumpulan 1' : 20*20,
    'Pengumpulan 2' : 20*25,
})

# Definisikan Parameter COST (PEMBUANGAN)
# 1. Cdl
model.Cdl = Param(model.M, initialize={
    'Pembuangan 1' : 10,
    'Pembuangan 2' : 13,
})

# 2. Fbm
model.Fbm = Param(model.M, initialize={
    'Pembuangan 1' : 10*30,
    'Pembuangan 2' : 10*35,
})

'''CAPACITY'''
# CAPACITY
# 1. Manufaktur Reguler (Cppi)
model.Cppi = Param(model.I, initialize={
    'Manufaktur 1' : 235,
    'Manufaktur 2' :250,
})

# 2. Manufaktur Remanufaktur (Cri)
model.Cri = Param(model.I, initialize={
    'Manufaktur 1' : 88,
    'Manufaktur 2' :92,
})

# 3. Distributor (Cpdj)
model.Cpdj = Param(model.J, initialize={
    'Distributor 1' : 350,
    'Distributor 2' :275,
})

# 4. Pengumpulan (Cccl)
model.Cccl = Param(model.L, initialize={
    'Distributor 1' : 70,
    'Distributor 2' :95,
})

# 4. Pembuangan (Ccdm)
model.Ccdm = Param(model.M, initialize={
    'Pembuangan 1' : 80,
    'Pembuangan 2' : 100,
})

'''Demand'''
# DEMAND
# 1. Konsumen (Dk)
model.Dk = Param(model.K, initialize={
    'Konsumen 1' : 100,
    'Konsumen 2' : 110,
    'Konsumen 3' : 120,
    'Konsumen 4' : 130
})

# Pasar Sekunder (Ds)
model.Ds = Param(model.S, initialize={
    'Sekunder 1' : 25,
    'Sekunder 2' : 35,
    'Sekunder 3' : 45,
    'Sekunder 4' : 50
})

