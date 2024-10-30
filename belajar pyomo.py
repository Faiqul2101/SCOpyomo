# IMPORT PYOMO
from pyomo.environ  import ConcreteModel, Var, Objective, Constraint, NonNegativeReals
import pyomo.environ as pyo
from pyomo.opt import SolverFactory 
from pyomo import *



# MEMBUAT/MENDEFINISIKAN MODEL
'''model adalah tempat kita mendefinisikan seluruh elemen optimasi, termasuk variabel, fungsi objektif, dan kendala. 
    Ada 2 model: ConcreteModel --> yang paling umum digunakan, cocok untuk masalah dengan struktur yang telah ditentukan, di mana semua elemen sudah diketahui sebelum dijalankan.
                AbstractModel --> Lebih fleksibel
'''
model = ConcreteModel()



# MENDEFINISIKAN VARIABEL KEPUTUSAN
model.x1 = Var(domain=NonNegativeReals)
model.x2 = Var(domain=NonNegativeReals)

'''Var mendefinsikan bahwa ini adalah variabel, sedangkan domain menjelaskan batasan nilai yg diinginkan untuk variabel, kurang lebih ada:
NonNegativeReals: Variabel hanya bisa bernilai nol atau positif.
NonNegativeIntegers: Variabel hanya bisa bernilai nol atau positif dalam bentuk bilangan bulat.
Binary: Variabel hanya bisa bernilai 0 atau 1 (biasanya untuk keputusan ya/tidak).
Reals: Variabel dapat bernilai positif, negatif, atau nol (kontinu).
Integers: Variabel bisa berupa bilangan bulat positif atau negatif. 
'''
'''Dalam banyak kasus, kita perlu mendefinisikan beberapa variabel yang diindeks oleh satu atau lebih indeks. Misalnya, dalam masalah produksi dengan beberapa jenis produk,
kita bisa mendefinisikan satu variabel untuk setiap produk menggunakan indeks.
Hal ini bisa kita lakukan dengan menggunakan "Set", Misalkan kita punya 3 produk, dan kita ingin memutuskan berapa banyak unit setiap produk yang akan diproduksi.
CONTOH:'''

from pyomo import Set

model.I = Set(initialize=['produk_1', 'produk_2', 'produk_3'])

''''Kemudian, kita definisikan variabel x yang terindeks oleh produk. 
Artinya, kita memiliki variabel model.x['produk_1'], model.x['produk_2'], dan model.x['produk_3'] sebagai variabel terpisah namun tergabung dalam model yang sama.'''

model.x = Var(model.I, domain=NonNegativeReals)

'''Kadang kita perlu memberikan batasan nilai pada variabel tertentu, seperti batas bawah dan batas atas (bounds). Ini bisa diatur langsung dalam definisi variabel dengan parameter bounds.
Misalnya, jika jumlah produksi produk tertentu tidak boleh kurang dari 10 unit dan tidak lebih dari 50 unit, kita bisa mendefinisikan batasan seperti dibawah.
Dalam kasus ini, setiap model.x[i] hanya bisa bernilai antara 10 hingga 50.
'''
model.x = Var(model.I, domain=NonNegativeReals, bounds=(10, 50))

'''Namun, Jika batasan berbeda-beda untuk setiap produk, kita bisa mendefinisikan batasan sebagai fungsi yang bergantung pada indeks.'''

def produk_bounds(model, i):
    if i == 'produk_1':
        return (10, 50)
    elif i == 'produk_2':
        return (5, 30)
    else:
        return (0, 20)

'''Mendefinisikan variabel dengan batasan dinamis'''
model.x = Var(model.I, domain=NonNegativeReals, bounds=produk_bounds)



# MENDEFINISIKAN PARAMETER
'''Dalam banyak model, nilai batasan atau parameter yang terkait dengan variabel keputusan seringkali diambil dari data eksternal atau kondisi tertentu yang dapat berubah. 
Kita bisa menggunakan Param untuk menangani nilai ini dan mengintegrasikannya dengan variabel.
Contoh: Misalkan setiap produk memiliki batas produksi berdasarkan permintaan yang dapat berubah-ubah:
'''

from pyomo import Param

'''Menambahkan parameter permintaan'''
model.demand = Param(model.I, initialize={'produk_1': 40, 'produk_2': 30, 'produk_3': 20})

'''Batas atas variabel berdasarkan permintaan'''
def produk_bounds(model, i):
    return (0, model.demand[i])

'''Variabel dengan batas atas dari parameter permintaan'''
model.x = Var(model.I, domain=NonNegativeReals, bounds=produk_bounds)


# MENDEFINISIKAN FUNGSI TUJUAN
'''Di Pyomo, fungsi objektif didefinisikan menggunakan objek Objective. Berikut adalah sintaks dasar untuk mendefinisikan fungsi objektif:
model.obj = Objective(expr=ekspresi_objektif, sense=minimize/maximize)
'''
import pyomo as pyo
model.obj = Objective(expr=40 * model.x1 + 60 * model.x2, sense=pyo.maximize)

'''Jika kita ingin menggunakan parameter dalam fungsi objektif, kita bisa mendefinisikan Param seperti yang telah kita bahas sebelumnya. 
Misalnya, biaya per unit dapat didefinisikan sebagai parameter:
'''
'''Mendefinisikan parameter biaya per unit'''
model.cost1 = Param(initialize=40)
model.cost2 = Param(initialize=60)

'''Fungsi objektif dengan parameter'''
model.obj = Objective(expr=model.cost1 * model.x1 + model.cost2 * model.x2, sense=pyo.minimize)

'''Jika kita memiliki banyak produk, kita dapat mendefinisikan variabel terindeks dan menggunakan fungsi objektif berbasis indeks.

'''
model.I = ['produk_1', 'produk_2']

model.cost = Param(model.I, initialize={'produk_1': 40, 'produk_2': 60})

model.x = Var(model.I, domain=NonNegativeReals)

from pyomo import summation

model.obj = Objective(expr=summation(model.cost, model.x), sense=pyo.minimize)

'''Jika menggunakan Set:.

'''

model.I = Set(initialize=['produk_1', 'produk_2', 'produk_3'])
model.cost = Param(model.I, initialize={'produk_1': 40, 'produk_2': 60, 'produk_3': 50})
model.x = Var(model.I, domain=NonNegativeReals)
model.obj = Objective(expr=sum(model.cost[i] * model.x[i] for i in model.I), sense=pyo.minimize)

''''Contoh untuk Transportasi:'''
'''Set untuk produk dan lokasi'''
model.Y = Set(initialize=['produk_1', 'produk_2'])
model.J = Set(initialize=['lokasi_1', 'lokasi_2'])

'''Mendefinisikan parameter biaya transportasi'''
model.transport_cost = Param(model.Y, model.Z, initialize={
    ('produk_1', 'lokasi_1'): 5,
    ('produk_1', 'lokasi_2'): 10,
    ('produk_2', 'lokasi_1'): 8,
    ('produk_2', 'lokasi_2'): 7,
})

'''Variabel keputusan: jumlah produk yang dikirim dari produk ke lokasi'''
model.shipment = Var(model.I, model.J, domain=NonNegativeReals)

'''Fungsi objektif: meminimalkan total biaya transportasi'''
model.obj = Objective(expr=sum(model.transport_cost[i, j] * model.shipment[i, j] for i in model.I for j in model.J), sense=pyo.minimize)






# MENDEFINISIKAN FUNGSI BATASAN
'''Fungsi batasan di Pyomo didefinisikan menggunakan objek Constraint. Berikut adalah sintaks dasar untuk mendefinisikan batasan:
model.batasan = Constraint(rule=aturan_batasan)'''



'''COntoh dengan set'''
from pyomo import ConcreteModel, Var, NonNegativeReals

model = ConcreteModel()

model.I = Set(initialize=['produk_1', 'produk_2'])

model.x = Var(model.I, domain=NonNegativeReals)

'''Contoh batasan kapasitas Produksi, Jika semua produk sama batasannya
'''
def total_production_constraint(model):
    return sum(model.x[i] for i in model.I) <= 100

model.total_production = Constraint(rule=total_production_constraint)

'''Contoh batasan kapasitas Produksi, Jika semua produk berbeda batasannya, menggunakan Param
'''
model.capacity = Param(model.I, initialize={'produk_1': 60, 'produk_2': 50})

def individual_capacity_constraint(model, i):
    return model.x[i] <= model.capacity[i]

model.individual_capacity = Constraint(model.I, rule=individual_capacity_constraint)

'''Untuk Set Multi Indeks
Jika kita memiliki banyak produk dan lokasi, 
kita bisa menggunakan set multi-indeks untuk mendefinisikan batasan yang lebih kompleks. Misalkan kita ingin membatasi jumlah pengiriman dari setiap produk ke setiap lokasi.'''

model.J = Set(initialize=['lokasi_1', 'lokasi_2'])

'''Variabel keputusan: jumlah pengiriman dari produk ke lokasi'''
model.shipment = Var(model.I, model.J, domain=NonNegativeReals)

'''Batasan: total pengiriman dari setiap produk ke semua lokasi harus memenuhi permintaan'''
model.demand = Param(model.J, initialize={'lokasi_1': 30, 'lokasi_2': 40})

def demand_constraint(model, j):
    return sum(model.shipment[i, j] for i in model.I) >= model.demand[j]

model.demand_constraints = Constraint(model.J, rule=demand_constraint)



# SOLVE
solver = SolverFactory('glpk')  # Menggunakan GLPK sebagai solver
result = solver.solve(model, tee=True)  # tee=True untuk menampilkan log solver

# Menampilkan hasil
print("Hasil Solusi:")
for i in model.I:
    for j in model.J:
        print(f"Pengiriman {i} ke {j}: {model.shipment[i, j].value}")
print("Total biaya transportasi:", model.obj())
