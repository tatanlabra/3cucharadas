# Units de usuario de 3cucharadas

Se instalan por **enlace simbólico**, no por copia, que es la convención de
`activos/memoria-personal/systemd/user/`: así una edición versionada surte efecto
tras un `daemon-reload` y no hay dos verdades divergiendo en silencio.

```
ln -sf "$PWD/systemd/user/difusion-cadencia.service" ~/.config/systemd/user/
ln -sf "$PWD/systemd/user/difusion-cadencia.timer"   ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now difusion-cadencia.timer
```

Estado al 2026-10-04: el timer está desactivado por decisión de la persona usuaria,
que sigue la difusión a mano. Las units siguen enlazadas y verificadas; la última
línea de arriba lo reactiva.

## `difusion-cadencia`

Corre a diario `verify_distribution_done.rb --ventana 30` y avisa por
`user-unit-alert@` cuando un canal declarado vence sin artefacto.

Existe porque el gate ya estaba escrito y **nadie lo corría**: salía 1 cuando
alguien se acordaba, y nadie se acordaba. Es el mismo patrón que dejó el
anti-drift del RAG cuatro días en rojo sin que nada avisara.

La bandera `--ventana 30` no indulta el atraso: lo baja de fatal a visible. El
aviso diario habla solo de lo que aún se puede hacer a tiempo, y el resumen
imprime igual cuántos atrasos históricos hay. En GitLab,
`distribution_audit` corre después de Pages en la schedule diaria solo si esta fija
`AUDITORIA_DIFUSION_DIARIA=1` (opcional desde el 2026-10-04; ver `.gitlab-ci.yml`).
Cuando corre, una deuda de difusión vuelve rojo el pipeline sin impedir que el
sitio ya validado quede servido.

**Falsado el 2026-09-05.** Con un drop-in que fijaba `DISTRIBUCION_HOY=2026-09-08`
el service salió 1, y `user-unit-alert@difusion-cadencia.service` arrancó y
terminó bien —nombre sin el `.service` duplicado, porque el `OnFailure` usa `%N`
y no `%n`—. Restaurado, vuelve a `Result=success`.
