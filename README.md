# Herramientas KW

Herramientas para los asesores de KW ON, KW Parque Leloir y KW City. Cada cambio que se sube a `main` se publica solo.

## Marca de agua — `index.html`

Agrega logo y corredor interviniente (KW ON, KW Leloir o KW City) a las fotos de propiedades. Las fotos se procesan en el dispositivo del asesor; no se suben a ningún servidor.

Link: https://soledadsenger-creator.github.io/marca-agua-kw/

## Calculadora de alquileres — `alquileres/`

Actualización de alquileres por ICL, IPC, CER o UVA con los índices oficiales. Muestra todos los períodos del contrato y exporta a WhatsApp, imagen, PDF y Excel; arma la carta de aviso al inquilino o al propietario y un archivo de calendario con las próximas actualizaciones; guarda cálculos en el dispositivo y arma un link para reabrir el mismo cálculo.

Link: https://soledadsenger-creator.github.io/marca-agua-kw/alquileres/

- Los índices se piden en vivo al BCRA (ICL variable 40, CER 30, UVA 31) y al INDEC vía datos.gob.ar (IPC nivel general, serie `148.3_INIVELNAL_DICI_M_26`).
- Si esas fuentes no responden, usa `alquileres/indices.json`, que la acción `Actualizar índices de la calculadora de alquileres` regenera todos los días con `alquileres/actualizar_indices.py`.
- Casa Propia, CAC, IS e IPIM no tienen fuente abierta: la página manda a ARquiler con los mismos datos.

## Simulador hipotecario UVA — `hipotecario/`

Cuota inicial, ingreso que pide el banco, cuánto le prestan con su ingreso y plata propia necesaria, con comparativo de bancos (Nación, Hipotecario, BBVA, Ciudad, Provincia, ICBC, Santander, Galicia, Macro). Exporta a WhatsApp, imagen, PDF y Excel (con cuadro de cuotas en UVA); guarda simulaciones y arma link.

Link: https://soledadsenger-creator.github.io/marca-agua-kw/hipotecario/

- Dólar mayorista (BCRA variable 5) y UVA (variable 31) en vivo; respaldo en `alquileres/indices.json`.
- Las condiciones de cada banco están en la constante `BANCOS` del `index.html` (relevadas el 05/10/2026). Cada asesor puede ajustarlas en su teléfono.
