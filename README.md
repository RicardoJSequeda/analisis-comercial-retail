# 📊 RetailBI — Dashboard de Análisis Comercial

Dashboard de Business Intelligence avanzado para una cadena retail colombiana.
Modelo estrella con 80,000 transacciones, medidas DAX de inteligencia temporal, ranking, segmentación ABC y análisis de clientes.

---

## 🎯 Objetivo del Proyecto

Construir un sistema de análisis comercial completo que permita a la gerencia responder preguntas clave de negocio:

- ¿Cómo evoluciona el revenue frente al año anterior?
- ¿Qué productos generan el 80% del margen (análisis ABC)?
- ¿Qué vendedores están por debajo de su meta y cuánto les falta?
- ¿Dónde están los clientes en riesgo de abandono?
- ¿Qué regiones tienen mayor potencial sin explotar?

---

## 🏗️ Arquitectura del Modelo

```
Modelo estrella — 1 tabla de hechos + 6 dimensiones

dim_tiempo ────────────┐
dim_producto ──────────┤
dim_cliente ───────────┼──→ fact_ventas (80,000 registros)
dim_vendedor ──────────┤
dim_region ────────────┤
dim_categoria ─────────┘
```

### Tablas del Data Warehouse

| Tabla | Filas | Descripción |
|-------|------:|-------------|
| `fact_ventas` | 80,000 | Transacciones con ingreso, costo, margen, descuento |
| `dim_tiempo` | 731 | Fechas 2023–2024 con festivos, temporadas, semanas |
| `dim_producto` | 185 | Productos con SKU, marca, categoría, precio y costo |
| `dim_cliente` | 500 | Clientes segmentados por canal y zona |
| `dim_vendedor` | 30 | Vendedores con equipo, zona y meta mensual |
| `dim_region` | 20 | 20 ciudades colombianas con departamento y zona |
| `dim_categoria` | 12 | Categorías con margen objetivo y temporalidad |

---

## 🛠️ Stack Tecnológico

| Herramienta | Uso |
|-------------|-----|
| Python 3.10+ | Generación del Data Warehouse |
| pandas / numpy | Modelado y simulación de datos |
| Power BI Desktop | Visualización y dashboard |
| DAX | Medidas de análisis avanzado |
| Power Query | Transformación y carga de datos |

---

## 📐 Medidas DAX Implementadas (40+)

### Por categoría:

**Revenue y márgenes**
- `[💰 Revenue]`, `[💰 Margen Bruto COP]`, `[💰 Margen Bruto %]`
- `[💰 Ticket Promedio]`, `[💰 Precio Promedio / Unidad]`
- `[💰 Descuento Promedio %]`, `[💰 Revenue / Día]`

**Inteligencia temporal**
- `[📈 Revenue YTD]`, `[📈 Revenue MTD]`, `[📈 Revenue QTD]`
- `[📈 Revenue Año Anterior]`, `[📈 YoY Revenue %]`, `[📈 MoM Revenue %]`
- `[📈 Revenue MA3]` — media móvil 3 meses
- `[📈 Revenue Rolling 12M]`, `[📈 Revenue Acumulado]`

**Ranking y portafolio**
- `[🏆 Rank Producto Revenue]`, `[🏆 Clasificación ABC]`
- `[🏆 Market Share %]`, `[🏆 Contribución Margen %]`
- `[💰 Revenue / SKU Activo]`

**Clientes**
- `[👥 Clientes Activos]`, `[👥 Clientes Nuevos]`, `[👥 Clientes en Riesgo]`
- `[👥 Revenue por Cliente]`, `[👥 Frecuencia Compra]`
- `[👥 Revenue Segmento Premium %]`

**Metas y semáforos**
- `[🎯 Cumplimiento Meta %]`, `[🎯 Color Cumplimiento]`
- `[🎯 Revenue Proyectado Mes]`, `[📈 Icono Tendencia YoY]`

---

## 📊 Páginas del Dashboard

### 1. Executive Overview
KPIs globales + evolución mensual de revenue vs año anterior + mix por división y canal.

### 2. Análisis de Productos
Clasificación ABC automática, scatter margen vs revenue, top 10 productos con ranking dinámico.

### 3. Rendimiento de Vendedores
Tabla de cumplimiento de metas con semáforo condicional, dispersión real vs meta, tendencia YoY por vendedor.

### 4. Clientes & Regiones
Mapa de Colombia por ciudad, segmentación de clientes, alerta de clientes en riesgo, frecuencia de compra por canal.

---

## ✅ Buenas Prácticas Aplicadas

- **Modelo estrella limpio** — sin relaciones circulares ni copo de nieve
- **Tabla de fechas marcada** — activa inteligencia temporal completa en DAX
- **Tabla [_Medidas] separada** — medidas aisladas de tablas de datos
- **Prefijos por categoría** — `💰 📈 📦 🏆 👥 🎯` para localización rápida
- **DIVIDE()** en todas las divisiones — nunca "/" (evita errores de división por cero)
- **VAR + RETURN** en medidas complejas — legibilidad y rendimiento
- **FK ocultas al usuario** — experiencia de análisis limpia
- **Formato explícito** en cada medida — unidades claras en las visualizaciones
- **Filtros cruzados unidireccionales** — evita ambigüedades en el modelo
- **Slicers sincronizados** entre páginas — contexto consistente al navegar
- **Drill-through** configurado — de resumen a detalle de transacciones
- **Tema corporativo** personalizado — paleta profesional consistente

---

## 🚀 Cómo Usar el Proyecto

```bash
# 1. Clonar el repositorio
git clone https://github.com/ricardosequeda/retailbi-dashboard
cd retailbi-dashboard

# 2. Instalar dependencias Python
pip install pandas numpy

# 3. Generar el Data Warehouse
python generar_dw.py
# Genera 7 archivos CSV en la carpeta ./data/

# 4. Abrir Power BI Desktop
# 5. Seguir la guía paso a paso en guia_power_bi.md
# 6. Importar las medidas DAX desde medidas_dax.dax
```

### Requisitos
- Python 3.10+
- Power BI Desktop (gratuito) — [descargar](https://powerbi.microsoft.com/desktop)

---

## 📁 Estructura del Proyecto

```
retailbi-dashboard/
│
├── generar_dw.py          # Generador del Data Warehouse (Python)
├── medidas_dax.dax        # 40+ medidas DAX comentadas y organizadas
├── guia_power_bi.md       # Guía paso a paso de implementación
├── README.md
│
└── data/                  # Generado al ejecutar generar_dw.py
    ├── dim_tiempo.csv
    ├── dim_categoria.csv
    ├── dim_producto.csv
    ├── dim_cliente.csv
    ├── dim_vendedor.csv
    ├── dim_region.csv
    └── fact_ventas.csv
```

---

## 👤 Autor

**Ricardo Javier Sequeda Goez**
Data Analyst | Business Intelligence | Python & SQL
📧 Ricardojgoez@gmail.com | [LinkedIn](https://linkedin.com/in/ricardosequeda)

---

*Data Warehouse sintético generado con distribuciones estadísticas realistas: temporadas de alta demanda (Navidad, Día de la Madre, Black Friday), pricing dinámico, segmentación de clientes y distribución de ciudades proporcional a la población colombiana.*
