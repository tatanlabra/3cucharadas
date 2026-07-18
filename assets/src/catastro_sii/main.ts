import "./styles.scss";

function begin(): void {
  const container = document.getElementById("map");
  if (!container) return;
  const start = () => {
    import("./app")
      .then(({ CatastroMapApplication }) => CatastroMapApplication.start())
      .then((application) => application.mount())
      .catch(() => {
        const status = document.getElementById("map-status");
        if (status) status.textContent = "La vista agregada sigue disponible; no fue posible iniciar el mapa vectorial.";
      });
  };
  if (!("IntersectionObserver" in window)) {
    start();
    return;
  }
  const observer = new IntersectionObserver((entries) => {
    if (!entries.some((entry) => entry.isIntersecting)) return;
    observer.disconnect();
    start();
  }, { rootMargin: "320px" });
  observer.observe(container);
}

begin();
