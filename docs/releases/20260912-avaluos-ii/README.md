# Publicación del 12-09-2026

Producto publicado: `b46381156ed259bbbdc2aea1e615ca3596174eb8`. [Pipeline #251](https://gitlab.com/tatanlabra/3cucharadas/-/pipelines/2843148339): build y Pages correctos.

`contract.json` y `TODO.md` distinguen publicación del blog, difusión externa y deuda real de auditoría. `remotes-ci.json` conserva los SHA observados antes del commit documental de estos recibos; ese commit posterior no cambia producto ni configuración y puede omitir reconstrucción CI.

La comparación pública usa el ZIP del job `16463031250`, cinco páginas y 49 archivos que esas páginas referencian. Incluye texto renderizado, referencias y SHA256, sin afirmar una auditoría exhaustiva de todos los enlaces, accesibilidad o rendimiento. `public-parity-negative.json` conserva el rechazo de una alteración del texto esperado, aplicada solamente en memoria; `public-parity-recovery.json` vuelve a PASS con el ZIP intacto.

Para repetirla: descargar el artefacto de ese job a `/tmp/3c-release-artifacts.zip` y ejecutar `python3 docs/releases/20260912-avaluos-ii/verify_public_parity.py /tmp/3c-public-check.json`. Un despliegue posterior puede invalidar legítimamente esta comparación histórica. La descarga usa la autenticación ya configurada en `glab`; no guardar credenciales en el recibo.

Los informes source-red/source-green son mediciones locales previas al commit, con sus SHA/digest originales; el pipeline remoto vuelve a ejecutar los checks sobre el commit publicado. Las pruebas añadidas rechazaron cuatro casos antes de implementar la corrección; después pasaron 9 pruebas/36 aserciones. La prueba DEV.to aislada pasó 2 pruebas/32 aserciones tras incorporar su dependencia real.

No se enviaron ni programaron piezas sociales: LinkedIn y X solicitan inicio de sesión. La autorización de envío ya existe; falta acceso efectivo a las cuentas. Nushell EN Medium permanece vencido en la auditoría diaria, y AC-Q6 conserva sus tres regresiones relativas de LCP. No se relajaron plazos ni reglas de fallo para presentar esos pendientes como éxito.
