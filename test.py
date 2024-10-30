# Mengimpor pustaka Pyomo
from pyomo.environ import ConcreteModel, Var, Objective, Constraint, SolverFactory, NonNegativeReals, summation

# Membuat model
model = ConcreteModel()

# Mendefinisikan set produk
model.I = ['A', 'B']

# Parameter keuntungan per unit
model.profit = {'A': 3, 'B': 4}

# Parameter kebutuhan sumber daya
model.time_required = {'A': 1, 'B': 2}  # Jam
model.material_required = {'A': 2, 'B': 1}  # Unit bahan baku

# Kapasitas sumber daya
model.max_time = 100  # Total jam
model.max_material = 60  # Total unit bahan baku

# Variabel keputusan: jumlah produk yang akan diproduksi
model.x = Var(model.I, domain=NonNegativeReals)

# Fungsi objektif: memaksimalkan total keuntungan
model.obj = Objective(expr=sum(model.profit[i] * model.x[i] for i in model.I), sense='maximize')

# Batasan waktu produksi
model.time_constraint = Constraint(expr=sum(model.time_required[i] * model.x[i] for i in model.I) <= model.max_time)

# Batasan bahan baku
model.material_constraint = Constraint(expr=sum(model.material_required[i] * model.x[i] for i in model.I) <= model.max_material)

# Menjalankan solver
solver = SolverFactory('ipopt')  # Pastikan Solver terinstal
result = solver.solve(model, tee=True)

# Menampilkan hasil
print("Hasil Solusi:")
for i in model.I:
    print(f"Produksi produk {i}: {model.x[i].value:.2f}")

print(f"Total keuntungan: {model.obj():.2f}")
