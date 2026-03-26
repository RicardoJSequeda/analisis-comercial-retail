# RetailBI — Guía de Implementación en Power BI
## Nivel Avanzado | Buenas Prácticas | Modelo Estrella

---

## PASO 1: Cargar los datos

### 1.1 Importar las 7 tablas CSV
`Inicio → Obtener datos → Texto/CSV`

Importar en este orden:
1. `dim_tiempo.csv`
2. `dim_categoria.csv`
3. `dim_producto.csv`
4. `dim_cliente.csv`
5. `dim_vendedor.csv`
6. `dim_region.csv`
7. `fact_ventas.csv`

### 1.2 Tipos de datos (Power Query — verificar antes de cerrar)

**dim_tiempo:**
| Campo | Tipo |
|-------|------|
| fecha_id | Número entero |
| fecha | Fecha |
| anio | Número entero |
| mes | Número entero |
| es_fin_semana | Verdadero/Falso |
| es_festivo | Verdadero/Falso |

**fact_ventas:**
| Campo | Tipo |
|-------|------|
| fecha_id | Número entero |
| cantidad | Número entero |
| precio_lista_cop | Número decimal |
| descuento_pct | Número decimal |
| ingreso_cop | Número decimal |
| costo_cop | Número decimal |
| margen_cop | Número decimal |
| margen_pct | Número decimal |

---

## PASO 2: Construir el Modelo de Datos

### 2.1 Crear relaciones en la vista Modelo

Ir a: `Vista → Modelo`

Crear estas relaciones arrastrando los campos:

```
fact_ventas[fecha_id]     → dim_tiempo[fecha_id]    (Muchos→1, Activa)
fact_ventas[producto_id]  → dim_producto[producto_id] (Muchos→1, Activa)
fact_ventas[cliente_id]   → dim_cliente[cliente_id]  (Muchos→1, Activa)
fact_ventas[vendedor_id]  → dim_vendedor[vendedor_id] (Muchos→1, Activa)
fact_ventas[region_id]    → dim_region[region_id]    (Muchos→1, Activa)
dim_producto[categoria_id]→ dim_categoria[categoria_id] (Muchos→1, Activa)
```

**Configuración de cada relación:**
- Cardinalidad: Varios a uno (*:1)
- Dirección del filtro cruzado: Único (de dimensión a hecho)
- Marcar como activa: ✅ Sí

### 2.2 Marcar dim_tiempo como tabla de fechas
Clic derecho sobre `dim_tiempo` → "Marcar como tabla de fechas" → seleccionar columna `fecha`

> Esto activa las funciones de inteligencia temporal (TOTALYTD, SAMEPERIODLASTYEAR, etc.)

### 2.3 Ocultar las columnas FK de fact_ventas
En la tabla `fact_ventas`, clic derecho sobre cada FK y seleccionar "Ocultar en la vista de informe":
- `fecha_id`, `producto_id`, `cliente_id`, `vendedor_id`, `region_id`

Los usuarios nunca deben ver las claves técnicas en los filtros.

---

## PASO 3: Tabla de Medidas

### 3.1 Crear tabla vacía para medidas
`Inicio → Nueva tabla`

```dax
_Medidas = ROW("placeholder", BLANK())
```

Nombrarla `_Medidas`. El guión bajo la mantiene al tope de la lista de campos.

### 3.2 Crear carpetas de medidas dentro de la tabla
Después de crear cada medida:
1. Seleccionarla en el panel de campos
2. En "Propiedades" (panel lateral) → "Carpeta para mostrar"
3. Asignar: `Revenue`, `Crecimiento`, `Clientes`, `Ranking`, `Metas`

---

## PASO 4: Implementar Medidas DAX

Copiar cada medida del archivo `medidas_dax.dax` usando:
`[_Medidas] → Nueva medida`

### Orden de implementación (respetar dependencias):
1. **Primero: Medidas base** (Revenue, Costo, Margen, Unidades, Transacciones, Ticket Promedio)
2. **Luego: Inteligencia temporal** (requiere las base)
3. **Luego: Ranking y ABC** (requieren las base)
4. **Al final: Metas y proyecciones** (requieren las anteriores)

### Formatos a aplicar (panel lateral → Formato):

| Medida | Formato |
|--------|---------|
| Revenue, Costo, Margen COP | `COP #,##0` |
| Ticket Promedio, Revenue por Cliente | `COP #,##0` |
| Margen %, YoY %, Market Share % | `0.0%` |
| # Transacciones, Clientes Activos | `#,##0` |
| Rank Producto, Rank Vendedor | `#,##0` |
| Cumplimiento Meta % | `0.0%` |

---

## PASO 5: Estructura del Dashboard (4 páginas)

### PÁGINA 1: Executive Overview
**Audiencia:** Gerencia general, dirección comercial

**Elementos:**
```
┌─────────────────────────────────────────────────────────────┐
│  FILTROS: Slicer Año | Slicer Trimestre | Slicer Región     │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ 💰 Revenue   │ 📦 Units     │ 💰 Margen %  │ 📈 YoY %      │
│ [Card KPI]   │ [Card KPI]   │ [Card KPI]   │ [Card KPI]    │
├──────────────┴──────────────┴──────────────┴────────────────┤
│  Revenue mensual + línea año anterior                       │
│  [Gráfico de líneas — dim_tiempo[mes] | Revenue, Rev AA]    │
├──────────────────────────────┬──────────────────────────────┤
│  Revenue por División        │  Revenue por Canal Venta     │
│  [Gráfico de barras apiladas]│  [Gráfico de rosca]          │
└──────────────────────────────┴──────────────────────────────┘
```

**Configuraciones clave:**
- Cards: activar "Valores de referencia" → Revenue Año Anterior
- Líneas: eje X = `dim_tiempo[mes_nombre]`, ordenar por `dim_tiempo[mes]`
- Rosca: máximo 5 categorías, resto en "Otros"

---

### PÁGINA 2: Análisis de Productos
**Audiencia:** Gerencia de producto, compras, categoría

**Elementos:**
```
┌─────────────────────────────────────────────────────────────┐
│  FILTROS: División | Categoría | Marca | Rango Precio       │
├────────────────────────────────────┬────────────────────────┤
│  Revenue por Categoría             │  Clasificación ABC     │
│  [Barras horizontales + %]         │  [Treemap con colores] │
├────────────────────────────────────┼────────────────────────┤
│  Top 10 Productos                  │  Margen % vs Revenue   │
│  [Tabla con Rank, Revenue, Margen] │  [Scatter plot]        │
└────────────────────────────────────┴────────────────────────┘
```

**Configuraciones clave:**
- Tabla Top 10: agregar `[🏆 Rank Producto Revenue]`, filtrar Rank ≤ 10
- Scatter: eje X = `[💰 Revenue]`, eje Y = `[💰 Margen Bruto %]`, tamaño = `[📦 Unidades Vendidas]`
- Treemap: usar color condicional basado en `[🏆 Clasificación ABC]`

---

### PÁGINA 3: Rendimiento de Vendedores
**Audiencia:** Gerencia comercial, supervisores de ventas

**Elementos:**
```
┌─────────────────────────────────────────────────────────────┐
│  FILTROS: Equipo | Zona | Período                           │
├──────────────────────────────────────────────────────────────┤
│  Ranking Vendedores                                         │
│  [Tabla con: Rank | Nombre | Revenue | Meta | Cumplimiento] │
│  → Formato condicional en Cumplimiento (semáforo Verde/Amarillo/Rojo)│
├──────────────────────┬──────────────────────────────────────┤
│  Revenue por Equipo  │  Tendencia YoY por Vendedor          │
│  [Barras agrupadas]  │  [Gráfico de cascada]               │
├──────────────────────┴──────────────────────────────────────┤
│  Dispersión: Revenue real vs Meta mensual                   │
│  [Scatter + línea de 100% cumplimiento]                    │
└─────────────────────────────────────────────────────────────┘
```

**Configuraciones clave:**
- Tabla: columna Cumplimiento → Formato condicional por valor de `[🎯 Color Cumplimiento]`
- Cascada: Año anterior como base, diferencia como variación
- Scatter: línea de referencia manual en Y=X (100% cumplimiento)

---

### PÁGINA 4: Clientes & Regiones
**Audiencia:** Gerencia de marketing, expansión territorial

**Elementos:**
```
┌─────────────────────────────────────────────────────────────┐
│  FILTROS: Segmento | Canal | Zona                           │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ 👥 Clientes  │ 💰 Rev/Cli   │ 📈 Nuevos    │ ⚠️ En Riesgo  │
│ [Card KPI]   │ [Card KPI]   │ [Card KPI]   │ [Card KPI]    │
├──────────────┴──────────────┴──────────────┴────────────────┤
│  Mapa de Colombia con Revenue por Ciudad                    │
│  [Mapa de formas o mapa de burbujas]                        │
│  → Color = Market Share %, Tamaño = Revenue                 │
├──────────────────────────────┬──────────────────────────────┤
│  Revenue por Segmento        │  Frecuencia de Compra        │
│  + % participación           │  por Canal                   │
│  [Barras + etiquetas %]      │  [Barras horizontales]       │
└──────────────────────────────┴──────────────────────────────┘
```

**Para el mapa de Colombia:**
1. Visualización → Mapa (o Mapa de formas)
2. Ubicación: `dim_region[ciudad]` o `dim_region[departamento]`
3. Tamaño de burbuja: `[💰 Revenue]`
4. Color: `[🏆 Market Share Región %]`
5. Agregar `dim_region[pais]` como campo de desambiguación

---

## PASO 6: Interactividad Avanzada

### 6.1 Slicers sincronizados
`Vista → Sincronizar segmentaciones`
- Los slicers de Año, Mes y Región deben estar disponibles en todas las páginas
- Activar "Sincronizar" y "Visible" para cada página

### 6.2 Drill-through de productos a detalle
1. En la página de Productos → clic derecho en encabezado de página → "Página de obtención de detalles"
2. Agregar `dim_producto[producto_id]` como campo de detalles
3. Crear tabla de transacciones de ese producto específico

### 6.3 Botones de navegación entre páginas
`Insertar → Botones → Flecha`
- Configurar Acción → Tipo: Navegación de páginas
- Crear un panel de navegación consistente en todas las páginas

### 6.4 Marcadores para vistas alternas
`Ver → Marcadores`
- Crear marcador "Vista ejecutiva" (sin filtros)
- Crear marcador "Vista operativa" (con filtros de vendedor/región)
- Agregar botones en cada página que activen cada marcador

### 6.5 Información sobre herramientas personalizada
`Insertar → Nueva página de información sobre herramientas`
- Crear mini-página con YoY, MTD, Ticket promedio
- Asignar a los gráficos de revenue como tooltip personalizado

---

## PASO 7: Formateo y Estilo Profesional

### 7.1 Tema corporativo
`Vista → Temas → Personalizar tema actual`

Colores recomendados (paleta profesional):
```json
{
  "name": "RetailBI",
  "dataColors": [
    "#1F4E8C", "#2E75B6", "#5BA3D9",
    "#27AE60", "#E67E22", "#C0392B",
    "#8E44AD", "#17A589", "#2C3E50"
  ],
  "background": "#FFFFFF",
  "foreground": "#252423",
  "tableAccent": "#1F4E8C"
}
```

### 7.2 Configuración de Canvas
`Formato → Tamaño de página`: 1920 × 1080 (Full HD)

### 7.3 Buenas prácticas de diseño
- Alinear todos los elementos con la grilla (activar con `Vista → Mostrar cuadrícula`)
- Margen exterior: 16px en todos los bordes
- Espacio entre visualizaciones: 8px
- Tarjetas KPI: misma altura, alineadas horizontalmente
- Título de página: 18px, negrita, color primario `#1F4E8C`
- Subtítulos de gráficas: 12px, color `#555555`

---

## PASO 8: Publicación y Buenas Prácticas

### 8.1 Antes de publicar
- [ ] Verificar que no hay errores en medidas DAX (revisar panel de errores)
- [ ] Confirmar relaciones activas en vista de modelo
- [ ] Revisar que dim_tiempo está marcada como tabla de fechas
- [ ] Probar todos los slicers en modo "Ver"
- [ ] Verificar rendimiento: `Optimizador de rendimiento → Analizar`

### 8.2 Documentar el modelo
- [ ] Descripción de cada medida en el panel de propiedades
- [ ] Carpetas organizadas en [_Medidas]
- [ ] Tabla de columnas FK ocultas al usuario

### 8.3 Publicar al servicio de Power BI
`Inicio → Publicar → Seleccionar área de trabajo`

---

## CHECKLIST DE BUENAS PRÁCTICAS APLICADAS

| Práctica | Implementada |
|----------|:------------:|
| Modelo estrella (sin copo de nieve) | ✅ |
| Tabla de fechas marcada | ✅ |
| FK ocultas al usuario | ✅ |
| Tabla de medidas separada | ✅ |
| Prefijos en medidas por categoría | ✅ |
| DIVIDE() en lugar de "/" | ✅ |
| VAR + RETURN en medidas complejas | ✅ |
| Formato aplicado a cada medida | ✅ |
| Filtros cruzados unidireccionales | ✅ |
| Columnas calculadas solo cuando necesario | ✅ |
| Slicers sincronizados entre páginas | ✅ |
| Drill-through configurado | ✅ |
| Tema corporativo consistente | ✅ |
| Nombres en español y descriptivos | ✅ |
