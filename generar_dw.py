"""
RetailBI — Generador de Data Warehouse
=======================================
Genera las 6 tablas del modelo estrella en formato CSV.
Ejecutar una sola vez: python generar_dw.py

Tablas generadas:
  dim_tiempo.csv      — 730 fechas (2 años)
  dim_producto.csv    — 200 productos
  dim_cliente.csv     — 500 clientes
  dim_vendedor.csv    — 30 vendedores
  dim_region.csv      — 20 regiones
  dim_categoria.csv   — 12 categorías
  fact_ventas.csv     — 80,000 transacciones
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random, os

np.random.seed(42)
random.seed(42)

OUT = "data"
os.makedirs(OUT, exist_ok=True)

# ════════════════════════════════════════════════════════════
# DIM_TIEMPO
# ════════════════════════════════════════════════════════════
FECHA_INI = datetime(2023, 1, 1)
FECHA_FIN = datetime(2024, 12, 31)

FESTIVOS_CO = {
    "01-01","01-06","03-25","04-17","04-18","05-01",
    "05-29","06-19","06-26","07-04","07-20","08-07",
    "08-18","10-13","11-03","11-17","12-08","12-25"
}

def temporada(mes):
    if mes in [12, 1]:      return "Navidad"
    elif mes in [6, 7]:     return "Mitad_año"
    elif mes == 5:           return "Madres"
    elif mes in [10, 11]:   return "Halloween_BF"
    else:                    return "Normal"

dias = []
d = FECHA_INI
while d <= FECHA_FIN:
    mm_dd = d.strftime("%m-%d")
    dias.append({
        "fecha_id":        int(d.strftime("%Y%m%d")),
        "fecha":           d.date(),
        "anio":            d.year,
        "trimestre":       (d.month - 1) // 3 + 1,
        "mes":             d.month,
        "mes_nombre":      d.strftime("%B"),
        "semana_anio":     int(d.strftime("%V")),
        "dia_mes":         d.day,
        "dia_semana_num":  d.weekday(),
        "dia_semana":      d.strftime("%A"),
        "es_fin_semana":   d.weekday() >= 5,
        "es_festivo":      mm_dd in FESTIVOS_CO,
        "temporada":       temporada(d.month),
        "anio_mes":        d.strftime("%Y-%m"),
    })
    d += timedelta(days=1)

dim_tiempo = pd.DataFrame(dias)
dim_tiempo.to_csv(f"{OUT}/dim_tiempo.csv", index=False)
print(f"✅ dim_tiempo:   {len(dim_tiempo):>6,} filas")

# ════════════════════════════════════════════════════════════
# DIM_CATEGORIA
# ════════════════════════════════════════════════════════════
categorias = [
    ("CAT01","Tecnología","Electrónicos",0.22,"Todo el año"),
    ("CAT02","Audio & Video","Electrónicos",0.18,"Todo el año"),
    ("CAT03","Computadores","Electrónicos",0.20,"Todo el año"),
    ("CAT04","Ropa Hombre","Moda",0.55,"Temporadas"),
    ("CAT05","Ropa Mujer","Moda",0.60,"Temporadas"),
    ("CAT06","Calzado","Moda",0.50,"Temporadas"),
    ("CAT07","Hogar & Deco","Hogar",0.45,"Todo el año"),
    ("CAT08","Cocina","Hogar",0.40,"Navidad"),
    ("CAT09","Deportes","Deporte",0.35,"Todo el año"),
    ("CAT10","Juguetes","Infantil",0.48,"Navidad"),
    ("CAT11","Libros","Cultura",0.30,"Todo el año"),
    ("CAT12","Belleza","Salud",0.52,"Todo el año"),
]
dim_categoria = pd.DataFrame(categorias,
    columns=["categoria_id","nombre","division","margen_objetivo","temporalidad"])
dim_categoria.to_csv(f"{OUT}/dim_categoria.csv", index=False)
print(f"✅ dim_categoria:{len(dim_categoria):>6,} filas")

# ════════════════════════════════════════════════════════════
# DIM_PRODUCTO
# ════════════════════════════════════════════════════════════
MARCAS = {
    "Tecnología":  ["Samsung","Apple","Xiaomi","LG","Sony"],
    "Audio & Video":["Sony","JBL","Bose","Samsung","Philips"],
    "Computadores":["HP","Dell","Lenovo","Asus","Apple"],
    "Ropa Hombre": ["Chevignon","Americanino","Tennis","Arturo Calle","Zara"],
    "Ropa Mujer":  ["Zara","H&M","Studio F","Mango","Guess"],
    "Calzado":     ["Nike","Adidas","Converse","Vélez","Aldo"],
    "Hogar & Deco":["IKEA","HomeCenter","Easy","Falabella","Krea"],
    "Cocina":      ["Imusa","Oster","Hamilton","Tramontina","WMF"],
    "Deportes":    ["Nike","Adidas","Under Armour","Puma","Reebok"],
    "Juguetes":    ["LEGO","Mattel","Hasbro","Fisher-Price","Funko"],
    "Libros":      ["Planeta","Norma","Penguin","Alfaguara","Oveja Negra"],
    "Belleza":     ["L'Oréal","Avon","Yanbal","Natura","Nivea"],
}

prods = []
for i, (cid, cat, div, margen, temp) in enumerate(categorias, 1):
    marcas_cat = MARCAS[cat]
    n = 17 if cat in ["Tecnología","Ropa Mujer","Ropa Hombre"] else 16
    for j in range(1, n + 1 if i <= 2 else n):
        pid = f"PRD{i:02d}{j:03d}"
        marca = random.choice(marcas_cat)
        costo = round(np.random.lognormal(11.5, 0.8))
        precio = round(costo / (1 - margen - random.uniform(-0.05, 0.05)))
        prods.append({
            "producto_id":   pid,
            "nombre":        f"{marca} {cat} {j:03d}",
            "sku":           f"SKU-{pid}",
            "categoria_id":  cid,
            "categoria":     cat,
            "division":      div,
            "marca":         marca,
            "costo_cop":     costo,
            "precio_lista_cop": precio,
            "margen_bruto":  round((precio - costo) / precio, 4),
            "activo":        random.choices([True, False], weights=[0.92, 0.08])[0],
        })

dim_producto = pd.DataFrame(prods[:200])
dim_producto.to_csv(f"{OUT}/dim_producto.csv", index=False)
print(f"✅ dim_producto: {len(dim_producto):>6,} filas")

# ════════════════════════════════════════════════════════════
# DIM_REGION
# ════════════════════════════════════════════════════════════
regiones = [
    ("REG01","Bogotá","Cundinamarca","Centro","Colombia",8_400_000),
    ("REG02","Medellín","Antioquia","Andina","Colombia",2_700_000),
    ("REG03","Cali","Valle del Cauca","Pacífica","Colombia",2_300_000),
    ("REG04","Barranquilla","Atlántico","Caribe","Colombia",1_300_000),
    ("REG05","Cartagena","Bolívar","Caribe","Colombia",1_000_000),
    ("REG06","Bucaramanga","Santander","Andina","Colombia",590_000),
    ("REG07","Pereira","Risaralda","Andina","Colombia",480_000),
    ("REG08","Manizales","Caldas","Andina","Colombia",430_000),
    ("REG09","Santa Marta","Magdalena","Caribe","Colombia",560_000),
    ("REG10","Cúcuta","Norte de Santander","Andina","Colombia",730_000),
    ("REG11","Ibagué","Tolima","Andina","Colombia",570_000),
    ("REG12","Villavicencio","Meta","Orinoquía","Colombia",510_000),
    ("REG13","Armenia","Quindío","Andina","Colombia",320_000),
    ("REG14","Neiva","Huila","Andina","Colombia",360_000),
    ("REG15","Montería","Córdoba","Caribe","Colombia",450_000),
    ("REG16","Pasto","Nariño","Pacífica","Colombia",440_000),
    ("REG17","Popayán","Cauca","Pacífica","Colombia",320_000),
    ("REG18","Tunja","Boyacá","Andina","Colombia",210_000),
    ("REG19","Sincelejo","Sucre","Caribe","Colombia",300_000),
    ("REG20","Valledupar","Cesar","Caribe","Colombia",520_000),
]
dim_region = pd.DataFrame(regiones,
    columns=["region_id","ciudad","departamento","zona","pais","poblacion"])
dim_region.to_csv(f"{OUT}/dim_region.csv", index=False)
print(f"✅ dim_region:   {len(dim_region):>6,} filas")

# ════════════════════════════════════════════════════════════
# DIM_VENDEDOR
# ════════════════════════════════════════════════════════════
NOMBRES = ["Carlos","Andrés","Juliana","María","Diego","Laura","Felipe","Ana","Jorge","Valentina",
           "Sebastián","Camila","Nicolás","Isabella","David","Daniela","Santiago","Alejandra",
           "Mateo","Paula","Tomás","Manuela","Juan","Sara","Esteban","Catalina","Alejandro",
           "Natalia","Ricardo","Sofía"]
APELLIDOS = ["García","Rodríguez","Martínez","López","González","Pérez","Sánchez","Ramírez",
             "Torres","Flores","Rivera","Gómez","Díaz","Reyes","Morales","Cruz","Ortiz","Vargas",
             "Ramos","Castro","Herrera","Medina","Jiménez","Ruiz","Álvarez","Moreno","Suárez",
             "Mendoza","Vega","Aguilar"]
EQUIPOS = ["Equipo Norte","Equipo Sur","Equipo Centro","Equipo Digital","Equipo Empresarial"]

vendedores = []
for i in range(1, 31):
    nombre = f"{NOMBRES[i-1]} {APELLIDOS[i-1]}"
    zona_base = dim_region.sample(1).iloc[0]
    meta = round(random.uniform(15_000_000, 80_000_000), -6)
    fi = FECHA_INI - timedelta(days=random.randint(30, 1800))
    vendedores.append({
        "vendedor_id":      f"VND{i:03d}",
        "nombre":           nombre,
        "email":            f"{nombre.split()[0].lower()}.{nombre.split()[1].lower()}@retailbi.co",
        "equipo":           random.choice(EQUIPOS),
        "zona":             zona_base["zona"],
        "region_base":      zona_base["region_id"],
        "meta_mensual_cop": meta,
        "fecha_ingreso":    fi.date(),
        "activo":           True,
    })

dim_vendedor = pd.DataFrame(vendedores)
dim_vendedor.to_csv(f"{OUT}/dim_vendedor.csv", index=False)
print(f"✅ dim_vendedor: {len(dim_vendedor):>6,} filas")

# ════════════════════════════════════════════════════════════
# DIM_CLIENTE
# ════════════════════════════════════════════════════════════
SEGMENTOS = ["Premium","Regular","Ocasional","Corporativo","Online"]
CANALES   = ["Tienda física","E-commerce","Teléfono","App móvil","WhatsApp Business"]

clientes = []
for i in range(1, 501):
    nom = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"
    reg = dim_region.sample(1).iloc[0]
    seg = np.random.choice(SEGMENTOS, p=[0.10,0.40,0.25,0.15,0.10])
    fr  = FECHA_INI - timedelta(days=random.randint(1, 1095))
    clientes.append({
        "cliente_id":      f"CLI{i:04d}",
        "nombre":          nom,
        "segmento":        seg,
        "canal_principal": random.choice(CANALES),
        "region_id":       reg["region_id"],
        "ciudad":          reg["ciudad"],
        "zona":            reg["zona"],
        "fecha_registro":  fr.date(),
        "activo":          random.choices([True, False], weights=[0.88, 0.12])[0],
    })

dim_cliente = pd.DataFrame(clientes)
dim_cliente.to_csv(f"{OUT}/dim_cliente.csv", index=False)
print(f"✅ dim_cliente:  {len(dim_cliente):>6,} filas")

# ════════════════════════════════════════════════════════════
# FACT_VENTAS  — 80,000 registros
# ════════════════════════════════════════════════════════════
fechas_ids = dim_tiempo["fecha_id"].values
fechas_dt  = pd.to_datetime(dim_tiempo["fecha"].values)
meses_dt   = dim_tiempo["mes"].values
temporadas = dim_tiempo["temporada"].values
festivos   = dim_tiempo["es_festivo"].values

prod_ids   = dim_producto["producto_id"].values
costos     = dim_producto["costo_cop"].values
precios    = dim_producto["precio_lista_cop"].values
cat_ids    = dim_producto["categoria_id"].values
cats       = dim_producto["categoria"].values

cli_ids    = dim_cliente["cliente_id"].values
vnd_ids    = dim_vendedor["vendedor_id"].values
reg_ids    = dim_region["region_id"].values

N = 80_000
idx_prod = np.random.choice(len(prod_ids), size=N, p=None)
idx_cli  = np.random.choice(len(cli_ids),  size=N)
idx_vnd  = np.random.choice(len(vnd_ids),  size=N)
idx_reg  = np.random.choice(len(reg_ids),  size=N,
               p=np.array([8400,2700,2300,1300,1000,590,480,430,560,730,
                            570,510,320,360,450,440,320,210,300,520], dtype=float) /
                 np.array([8400,2700,2300,1300,1000,590,480,430,560,730,
                            570,510,320,360,450,440,320,210,300,520], dtype=float).sum())

# Fechas ponderadas: más en festivos y temporadas altas
pesos_fecha = np.ones(len(fechas_ids))
pesos_fecha[temporadas == "Navidad"]     *= 2.5
pesos_fecha[temporadas == "Mitad_año"]  *= 1.5
pesos_fecha[temporadas == "Madres"]     *= 1.8
pesos_fecha[temporadas == "Halloween_BF"] *= 2.0
pesos_fecha[festivos == True]            *= 1.6
pesos_fecha = pesos_fecha / pesos_fecha.sum()

idx_fecha = np.random.choice(len(fechas_ids), size=N, p=pesos_fecha)

filas = []
for i in range(N):
    ip = idx_prod[i]
    precio_base = float(precios[ip])
    costo_unit  = float(costos[ip])

    # Descuento dinámico
    temp = temporadas[idx_fecha[i]]
    if temp == "Navidad":         desc_pct = round(random.uniform(0.10, 0.30), 2)
    elif temp in ["Madres","Halloween_BF"]: desc_pct = round(random.uniform(0.05, 0.20), 2)
    elif festivos[idx_fecha[i]]:  desc_pct = round(random.uniform(0.05, 0.15), 2)
    else:                          desc_pct = round(random.uniform(0.00, 0.10), 2)

    cantidad   = int(np.random.choice([1,2,3,4,5], p=[0.55,0.25,0.12,0.05,0.03]))
    precio_unt = round(precio_base * (1 - desc_pct))
    ingreso    = precio_unt * cantidad
    costo_tot  = costo_unit * cantidad
    margen     = ingreso - costo_tot
    margen_pct = round(margen / ingreso, 4) if ingreso else 0

    canal = np.random.choice(["Tienda","E-commerce","App","Teléfono"],
                              p=[0.45,0.30,0.15,0.10])
    metodo = np.random.choice(["Efectivo","Tarjeta déb.","Tarjeta créd.","PSE","Nequi"],
                               p=[0.20,0.25,0.30,0.15,0.10])

    filas.append({
        "venta_id":         f"V{i+1:07d}",
        "fecha_id":         int(fechas_ids[idx_fecha[i]]),
        "producto_id":      prod_ids[ip],
        "cliente_id":       cli_ids[idx_cli[i]],
        "vendedor_id":      vnd_ids[idx_vnd[i]],
        "region_id":        reg_ids[idx_reg[i]],
        "cantidad":         cantidad,
        "precio_lista_cop": precio_base,
        "descuento_pct":    desc_pct,
        "precio_venta_cop": precio_unt,
        "ingreso_cop":      ingreso,
        "costo_cop":        costo_tot,
        "margen_cop":       margen,
        "margen_pct":       margen_pct,
        "canal_venta":      canal,
        "metodo_pago":      metodo,
    })

fact_ventas = pd.DataFrame(filas)
fact_ventas.to_csv(f"{OUT}/fact_ventas.csv", index=False)
print(f"✅ fact_ventas:  {len(fact_ventas):>6,} filas")

print(f"\n📁 Archivos en ./{OUT}/")
print(f"   Revenue total generado: COP {fact_ventas['ingreso_cop'].sum():,.0f}")
print(f"   Margen promedio:        {fact_ventas['margen_pct'].mean()*100:.1f}%")
print(f"   Ticket promedio:        COP {fact_ventas['ingreso_cop'].mean():,.0f}")
