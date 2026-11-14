/* ============================================================
   Veterinaria Plus — Frontend (web/app.js)
   Backend: http://127.0.0.1:8000/api
   ============================================================ */

/* La API vive en el mismo origen que este frontend. Al usar window.location.origin,
   desde cualquier computadora de la red local se apuntará automáticamente a la IP
   correcta del servidor (ej. http://192.168.1.50:8000/api). */
const API_BASE = window.location.origin + "/api";

/* ---------- Utilidades ---------- */
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

// Sanitización XSS: escapa HTML antes de insertar en el DOM
function esc(texto) {
  if (texto == null) return "";
  const div = document.createElement("div");
  div.textContent = String(texto);
  return div.innerHTML;
}

// Notificaciones (Notyf vía CDN)
const notyf = new Notyf({
  duration: 3000,
  position: { x: "right", y: "top" },
  ripple: false,
});
function toastOk(msg) { notyf.success(msg); }
function toastErr(msg) { notyf.error(msg); }

// Spinner util
function showSpinner(el) { el.style.display = "block"; }
function hideSpinner(el) { el.style.display = "none"; }

/* ---------- Tema claro/oscuro (persistente en localStorage) ---------- */
const THEME_KEY = "vet-theme";
const btnTheme = $("#btnTheme");
const moonIcon = btnTheme.querySelector(".fa-moon");
const sunIcon = document.createElement("i");
sunIcon.className = "fas fa-sun";

function getSavedTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved) return saved;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function setTheme(t) {
  document.documentElement.setAttribute("data-theme", t);
  localStorage.setItem(THEME_KEY, t);
  btnTheme.innerHTML = "";
  btnTheme.appendChild(t === "dark" ? sunIcon : moonIcon);
  btnTitle(t);
}
function btnTitle(t) { btnTheme.title = t === "dark" ? "Cambiar a modo claro" : "Cambiar a modo oscuro"; }

btnTheme.addEventListener("click", () => {
  const cur = document.documentElement.getAttribute("data-theme") || "light";
  setTheme(cur === "light" ? "dark" : "light");
});
setTheme(getSavedTheme());

/* ---------- Menú móvil (hamburguesa) ---------- */
const btnMenu = $("#btnMenu");
const mobileTabs = $("#mobileTabs");
const menuIcon = btnMenu.querySelector(".fa-bars");
const menuClose = document.createElement("i");
menuClose.className = "fas fa-times";

function toggleMenu() {
  const open = !mobileTabs.classList.contains("open");
  mobileTabs.classList.toggle("open");
  btnMenu.setAttribute("aria-expanded", open);
  btnMenu.innerHTML = "";
  btnMenu.appendChild(open ? menuClose : menuIcon);
  btnMenu.title = open ? "Cerrar menú" : "Menú";
}
btnMenu.addEventListener("click", toggleMenu);

// Cerrar menú al seleccionar una pestaña
$$(".tab-btn").forEach((b) => {
  b.addEventListener("click", () => {
    if (mobileTabs.classList.contains("open")) toggleMenu();
  });
});

/* ---------- Tabs ---------- */
const tabBtns = $$(".tab-btn");
const tabPanels = $$(".tab-panel");

function openTab(id) {
  const run = () => {
    tabBtns.forEach((b) => b.classList.toggle("active", b.dataset.tab === id));
    tabPanels.forEach((p) => p.classList.toggle("active", p.id === "tab-" + id));
    if (id === "vacunas") cargarVacunas();
  };
  if (document.startViewTransition) {
    try {
      document.startViewTransition(run);
    } catch (e) {
      run();
    }
  } else {
    run();
  }
}
tabBtns.forEach((b) => b.addEventListener("click", () => openTab(b.dataset.tab)));
openTab("catalog");

/* ---------- Registro de paciente (modal) ---------- */
const modal = $("#modalRegister");
const btnCloseModal = $("#btnCloseModal");
const formRegister = $("#formRegister");
const regInputs = {
  code: $("#regCode"),
  name: $("#regName"),
  age: $("#regAge"),
  species: $("#regSpecies"),
  breed: $("#regBreed"),
  owner: $("#regOwner"),
  phone: $("#regPhone"),
};
const regErrors = {
  code: $("#errRegCode"),
  name: $("#errRegName"),
  age: $("#errRegAge"),
  species: $("#errRegSpecies"),
  breed: $("#errRegBreed") || null,
  owner: $("#errRegOwner"),
  phone: $("#errRegPhone") || null,
};
let editandoCodigo = null;

function clearErrors() {
  Object.values(regErrors).forEach((e) => { if (e) e.textContent = ""; });
  Object.values(regInputs).forEach((i) => i.classList.remove("input-error"));
}
function markError(key, msg) {
  const input = regInputs[key];
  const err = regErrors[key];
  if (input) input.classList.add("input-error");
  if (err) err.textContent = msg;
}

// Abrir modal desde cualquier lugar (botón rápido opcional)
window.abrirRegistro = async function () {
  clearErrors();
  formRegister.reset();

  // Asignar código automático (máximo actual + 1, con 3 dígitos)
  try {
    const res = await fetch(`${API_BASE}/pacientes`);
    const data = await res.json();
    const pacientes = Array.isArray(data) ? data : data.pacientes || [];
    const maxCod = pacientes.reduce((max, p) => {
      const n = parseInt(p.codigo, 10) || 0;
      return n > max ? n : max;
    }, 0);
    regInputs.code.value = String(maxCod + 1).padStart(3, "0");
  } catch (e) {
    regInputs.code.value = "001";
  }

  setCreateMode();
  modal.style.display = "flex";
};

// Modo creación / edición del modal
function setCreateMode() {
  editandoCodigo = null;
  $("#btnRegSubmit").innerHTML = '<i class="fas fa-save"></i> Guardar Paciente';
  regInputs.code.disabled = false;
  regInputs.name.disabled = false;
  regInputs.age.disabled = false;
  regInputs.species.disabled = false;
  regInputs.breed.disabled = false;
  regInputs.owner.disabled = false;
  regInputs.phone.disabled = false;
}

function setEditMode(codigo) {
  editandoCodigo = codigo;
  $("#btnRegSubmit").innerHTML = '<i class="fas fa-save"></i> Actualizar Paciente';
  regInputs.code.disabled = true;
  regInputs.name.disabled = true;
  regInputs.age.disabled = false;
  regInputs.species.disabled = true;
  regInputs.breed.disabled = true;
  regInputs.owner.disabled = false;
  regInputs.phone.disabled = false;
}

// Eliminar paciente
async function eliminarPaciente(codigo) {
  const confirmado = await Swal.fire({
    title: "¿Eliminar paciente?",
    text: `¿Está seguro de que desea eliminar al paciente con código #${codigo}?`,
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#B42318",
    cancelButtonColor: "#5C665D",
    confirmButtonText: "Sí, eliminar",
    cancelButtonText: "Cancelar",
  });
  if (!confirmado.isConfirmed) return;

  try {
    const res = await fetch(`${API_BASE}/pacientes/${codigo}`, { method: "DELETE" });
    if (!res.ok) throw new Error("No se pudo eliminar");
    toastOk("Paciente eliminado correctamente.");
    cargarCatalogo();
  } catch (err) {
    toastErr("Error al eliminar el paciente.");
  }
}

// Editar paciente (carga los datos en el modal)
async function editarPaciente(codigo) {
  try {
    const res = await fetch(`${API_BASE}/pacientes/${codigo}`);
    if (!res.ok) throw new Error("No se pudo cargar el paciente");
    const p = await res.json();

    regInputs.code.value = p.codigo;
    regInputs.name.value = p.nombre;
    regInputs.age.value = p.edad;
    regInputs.species.value = p.especie;
    regInputs.breed.value = p.raza || "";
    regInputs.owner.value = p.duenio;
    regInputs.phone.value = p.telefono || "";

    clearErrors();
    setEditMode(codigo);
    modal.style.display = "flex";
  } catch (err) {
    toastErr("Error al cargar los datos del paciente.");
  }
}
btnCloseModal.addEventListener("click", () => { modal.style.display = "none"; });
modal.querySelector(".modal__overlay").addEventListener("click", () => { modal.style.display = "none"; });

formRegister.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearErrors();
  const codigoRaw = regInputs.code.value.trim();
  const nombre = regInputs.name.value.trim();
  const especie = regInputs.species.value.trim();
  const raza = regInputs.breed.value.trim();
  const duenio = regInputs.owner.value.trim();
  const telefono = regInputs.phone.value.trim();
  const edad = parseInt(regInputs.age.value, 10);

  let valido = true;
  const codigoNum = parseInt(codigoRaw, 10);
  if (!/^\d+$/.test(codigoRaw) || codigoNum <= 0) {
    markError("code", "El código debe ser un entero positivo."); valido = false;
  }
  if (!nombre) { markError("name", "El nombre del paciente es obligatorio."); valido = false; }
  if (!regInputs.age.value || isNaN(edad) || edad < 0) {
    markError("age", "La edad debe ser un número mayor o igual a 0."); valido = false;
  }
  if (!especie) { markError("species", "Seleccione una especie."); valido = false; }
  if (!duenio) { markError("owner", "El dueño es obligatorio."); valido = false; }
  if (!valido) return;

  const btn = $("#btnRegSubmit");
  const txtOrig = btn.innerHTML;
  btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Guardando...';
  btn.disabled = true;

  try {
    let res;
    if (editandoCodigo) {
      res = await fetch(`${API_BASE}/pacientes/${editandoCodigo}?nueva_edad=${edad}&nuevo_duenio=${encodeURIComponent(duenio)}&telefono=${encodeURIComponent(telefono)}&nuevo_nombre=${encodeURIComponent(nombre)}&nueva_especie=${encodeURIComponent(especie)}&nueva_raza=${encodeURIComponent(raza || "")}`, {
        method: "PUT",
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw data.error || data.msg || "Error al actualizar";
      toastOk("Paciente actualizado correctamente.");
    } else {
      res = await fetch(`${API_BASE}/pacientes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          codigo: codigoRaw,
          nombre,
          especie,
          raza,
          edad,
          duenio,
          telefono,
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw data.error || data.msg || "Error al registrar";
      toastOk("Paciente registrado correctamente.");
    }
    modal.style.display = "none";
    formRegister.reset();
    setCreateMode();
    cargarCatalogo();
  } catch (err) {
    toastErr(String(err.message || err));
  } finally {
    btn.innerHTML = txtOrig;
    btn.disabled = false;
  }
});

/* ---------- Catálogo ---------- */
async function cargarCatalogo() {
  const skeleton = $("#catalogSkeleton");
  const wrap = $("#catalogTableWrap");
  const empty = $("#catalogEmpty");
  const body = $("#catalogBody");
  const count = $("#catalogCount");

  skeleton.style.display = "block";
  wrap.style.display = "none";
  empty.style.display = "none";

  try {
    const res = await fetch(`${API_BASE}/pacientes`);
    if (!res.ok) throw new Error("No se pudo cargar el catálogo");
    const data = await res.json();
    const pacientes = Array.isArray(data) ? data : data.pacientes || [];

    body.innerHTML = "";
    pacientes.forEach((p) => {
      const tr = document.createElement("tr");
      tr.className = "table-row-clickable";
      tr.setAttribute("view-transition-name", "paciente-" + p.codigo);
      tr.dataset.codigo = p.codigo;
      tr.innerHTML = `
        <td><strong>#${esc(p.codigo)}</strong></td>
        <td>${esc(p.nombre)}</td>
        <td>${esc(p.especie)}</td>
        <td>${esc(p.raza || "—")}</td>
        <td>${esc(p.duenio)}</td>
        <td>${esc(p.telefono || "—")}</td>
        <td><span class="badge badge-success">Activo</span></td>
        <td>
          <span class="tooltip-group" style="anchor-name: --edit-${p.codigo};">
            <button class="btn btn-outline btn-sm" type="button" onclick="editarPaciente('${p.codigo}')" aria-label="Editar paciente">
              <i class="fas fa-pen" aria-hidden="true"></i>
            </button>
            <span class="tooltip" style="position-anchor: --edit-${p.codigo};">Editar paciente</span>
          </span>
          <span class="tooltip-group" style="anchor-name: --del-${p.codigo};">
            <button class="btn btn-outline btn-sm btn-danger" type="button" onclick="eliminarPaciente('${p.codigo}')" aria-label="Eliminar paciente">
              <i class="fas fa-trash" aria-hidden="true"></i>
            </button>
            <span class="tooltip" style="position-anchor: --del-${p.codigo};">Eliminar paciente</span>
          </span>
        </td>
      `;
      tr.addEventListener("click", (e) => {
        if (e.target.tagName === "BUTTON" || e.target.closest("button")) return;
        abrirPanelDetalle(p.codigo);
      });
      body.appendChild(tr);
    });

    count.textContent = pacientes.length;
    skeleton.style.display = "none";
    if (pacientes.length) {
      wrap.style.display = "block";
    } else {
      empty.style.display = "block";
    }
  } catch (err) {
    skeleton.style.display = "none";
    empty.style.display = "block";
    empty.querySelector("p").textContent = "Error cargando el catálogo: " + esc(err.message);
    toastErr("Error cargando el catálogo.");
  }
}

/* ---------- Panel de detalle de paciente ---------- */
const panelPaciente = $("#panelPaciente");
const panelBackdrop = $("#panelBackdrop");
const btnClosePanel = $("#btnClosePanel");
const btnEditarDesdePanel = $("#btnEditarDesdePanel");
const btnEliminarDesdePanel = $("#btnEliminarDesdePanel");
let codigoAbierto = null;

async function abrirPanelDetalle(codigo) {
  try {
    const res = await fetch(`${API_BASE}/pacientes/${codigo}`);
    if (!res.ok) throw new Error("No se pudo cargar el paciente");
    const p = await res.json();

    $("#detCode").textContent = "#" + esc(p.codigo);
    $("#detNombre").textContent = esc(p.nombre);
    $("#detEspecie").textContent = esc(p.especie);
    $("#detRaza").textContent = esc(p.raza || "—");
    $("#detEdad").textContent = esc(p.edad);
    $("#detDuenio").textContent = esc(p.duenio);
    $("#detTelefono").textContent = esc(p.telefono || "—");

    btnEditarDesdePanel.onclick = () => { editarPaciente(codigo); cerrarPanelDetalle(); };
    btnEliminarDesdePanel.onclick = () => { eliminarPaciente(codigo); cerrarPanelDetalle(); };

    codigoAbierto = codigo;
    panelPaciente.classList.add("open");
  } catch (err) {
    toastErr("Error al cargar el detalle del paciente.");
  }
}

function cerrarPanelDetalle() {
  panelPaciente.classList.remove("open");
  codigoAbierto = null;
}

btnClosePanel.addEventListener("click", cerrarPanelDetalle);
panelBackdrop.addEventListener("click", cerrarPanelDetalle);

/* ---------- Vacunas y Controles Pendientes ---------- */
const vacunasSkeleton = $("#vacunasSkeleton");
const vacunasList = $("#vacunasList");
const vacunasEmpty = $("#vacunasEmpty");
const vacunasError = $("#vacunasError");
const vacunasGrid = $("#vacunasList .vacunas-grid");
const turnosPendientesGrid = $("#turnosPendientesGrid");

async function cargarVacunas() {
  vacunasSkeleton.style.display = "block";
  vacunasList.style.display = "none";
  vacunasEmpty.style.display = "none";
  vacunasError.style.display = "none";
  vacunasGrid.innerHTML = "";

  try {
    const res = await fetch(`${API_BASE}/vacunas/pendientes`);
    if (!res.ok) throw new Error("No se pudieron cargar las vacunas");
    const data = await res.json();
    const vacunas = Array.isArray(data) ? data : data.vacunas || [];
    renderVacunas(vacunas);
    renderTurnosPendientes();
  } catch (err) {
    vacunasSkeleton.style.display = "none";
    vacunasEmpty.style.display = "block";
    vacunasEmpty.querySelector("h3").textContent = "No se pudieron cargar las vacunas.";
    vacunasEmpty.querySelector("p").textContent = esc(err.message);
    toastErr("Error cargando vacunas pendientes.");
    renderTurnosPendientes();
  }
}

function renderVacunas(vacunas) {
  vacunasSkeleton.style.display = "none";
  if (!vacunas.length) {
    vacunasEmpty.style.display = "block";
    return;
  }
  vacunasList.style.display = "block";
  vacunasGrid.innerHTML = "";
  vacunas.forEach((v) => {
    const estado = v.estado || "pendiente";
    const dias = v.diasRestantes != null ? v.diasRestantes : "";
    const card = document.createElement("div");
    card.className = "vacuna-card";
    card.setAttribute("view-transition-name", "vacuna-" + (v.codigo || v.id));
    card.innerHTML = `
      <div class="vacuna-card__header">
        <div class="vacuna-card__icon"><i class="fas ${v.icono || "fa-syringe"}" aria-hidden="true"></i></div>
        <span class="vacuna-badge vacuna-badge--${estado}">${esc(estado)}</span>
      </div>
      <h4 class="vacuna-card__mascota">#${esc(v.codigo)} ${esc(v.nombre)}</h4>
      <p class="vacuna-card__tipo">${esc(v.tipo || "Control general")}</p>
      <div class="vacuna-card__meta">
        <i class="fas fa-calendar" aria-hidden="true"></i>
        <span>${esc(v.fecha || "—")}</span>
        ${dias ? `<span class="vacuna-card__dias">${dias} día${dias !== 1 ? "s" : ""} restantes</span>` : ""}
      </div>
      <button class="btn btn-outline btn-sm vacuna-atender-btn" type="button" onclick="marcarVacunaComoAtendida('${esc(v.codigo)}')" aria-label="Marcar como atendido">
        <i class="fas fa-check" aria-hidden="true"></i> Atender
      </button>
    `;
    vacunasGrid.appendChild(card);
  });
}

/* ---------- Marcar vacuna/control como atendido ---------- */
function marcarVacunaComoAtendida(codigo) {
  const card = vacunasGrid.querySelector(`[view-transition-name="vacuna-${codigo}"]`);
  if (!card) return;

  // Cambiar badge a "Atendido"
  const badge = card.querySelector(".vacuna-badge");
  if (badge) {
    badge.textContent = "Atendido";
    badge.className = "vacuna-badge vacuna-badge--atendido";
  }

  // Aplicar estilo de atendida (desvanecida)
  card.classList.add("vacuna-card--atendida");

  // Cambiar texto del botón y deshabilitarlo
  const btn = card.querySelector(".vacuna-atender-btn");
  if (btn) {
    btn.textContent = "Atendido";
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-check" aria-hidden="true"></i> Atendido';
  }

  // Remover la card después de un breve delay para que se vea el cambio
  setTimeout(() => {
    card.style.opacity = "0";
    card.style.transform = "scale(0.95)";
    setTimeout(() => {
      card.remove();
      // Si ya no quedan vacunas ni turnos, mostrar empty state
      const vacunasList = $("#vacunasList");
      const turnosPendientesList = $("#turnosPendientesList");
      const turnosPendientesGrid = $("#turnosPendientesGrid");
      const tieneVacunas = vacunasList.style.display === "block" && vacunasGrid.children.length > 0;
      const tieneTurnos = turnosPendientesGrid.children.length > 0;
      if (!tieneVacunas && !tieneTurnos) {
        $("#vacunasEmpty").style.display = "block";
        vacunasList.style.display = "none";
        $("#turnosPendientesList").style.display = "none";
      }
    }, 300);
  }, 800);
}

/* ---------- Renderizar turnos pendientes en sección de vacunas ---------- */
function renderTurnosPendientes() {
  const vacunasList = $("#vacunasList");
  const turnosPendientesList = $("#turnosPendientesList");

  // Si no hay vacunas ni turnos, mostrar empty state
  const tieneVacunas = vacunasList.style.display === "block";
  const tieneTurnos = turnosPendientes.length > 0;

  if (!tieneVacunas && !tieneTurnos) {
    turnosPendientesList.style.display = "none";
    $("#vacunasEmpty").style.display = "block";
    return;
  }

  // Si hay algo que mostrar, ocultar empty state
  $("#vacunasEmpty").style.display = "none";

  // Mostrar lista de vacunas si las hay
  if (tieneVacunas) {
    vacunasList.style.display = "block";
  }

  // Renderizar turnos pendientes
  if (tieneTurnos) {
    turnosPendientesList.style.display = "block";
    turnosPendientesGrid.innerHTML = "";
    turnosPendientes.forEach((t) => {
      const card = document.createElement("div");
      card.className = "vacuna-card";
      card.innerHTML = `
        <div class="vacuna-card__header">
          <div class="vacuna-card__icon"><i class="fas fa-calendar-check" aria-hidden="true"></i></div>
          <span class="vacuna-badge vacuna-badge--pendiente">Turno</span>
        </div>
        <h4 class="vacuna-card__mascota">#${esc(t.codigo)} ${esc(t.mascota)}</h4>
        <p class="vacuna-card__tipo">${esc(t.motivo)}</p>
        <div class="vacuna-card__meta">
          <i class="fas fa-user-tie" aria-hidden="true"></i>
          <span>${esc(t.duenio)}</span>
        </div>
        <div class="vacuna-card__meta">
          <i class="fas fa-calendar" aria-hidden="true"></i>
          <span>${esc(t.fecha)} · ${esc(t.horario)}</span>
        </div>
        <div class="vacuna-card__meta">
          <i class="fas fa-user-md" aria-hidden="true"></i>
          <span>${esc(t.veterinario)}</span>
        </div>
        ${t.observaciones ? `
          <div class="vacuna-card__meta" style="font-size:0.8rem; color:var(--fg-muted);">
            <i class="fas fa-notes" aria-hidden="true"></i>
            <span>${esc(t.observaciones)}</span>
          </div>
        ` : ""}
      `;
      turnosPendientesGrid.appendChild(card);
    });
  } else {
    turnosPendientesList.style.display = "none";
  }
}

/* ---------- Búsqueda general (nombre / dueño) ---------- */
function setupGeneralSearch(inputId, btnId, criterio, resultId, errorId, benchmarkPrefix) {
  const input = $(inputId);
  const btn = $(btnId);
  const result = $(resultId);
  const error = $(errorId);
  const benchContainer = benchmarkPrefix ? $(benchmarkPrefix.toLowerCase() + "Benchmark") : null;
  let timer = null;

  function ocultarBenchmark() {
    if (benchContainer) benchContainer.style.display = "none";
  }

  function ejecutar() {
    const valor = input.value.trim();
    result.style.display = "none";
    error.style.display = "none";
    ocultarBenchmark();
    if (!valor) return;

    btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i>';
    btn.disabled = true;

    fetch(`${API_BASE}/buscar/general?criterio=${encodeURIComponent(criterio)}&valor=${encodeURIComponent(valor)}`)
      .then((res) => res.json().catch(() => ({})))
      .then((data) => {
        btn.innerHTML = '<i class="fas fa-search"></i> Buscar';
        btn.disabled = false;
        const items = Array.isArray(data) ? data : data.resultados || [];
        renderResultList(result, items, criterio);
        if (!items.length) {
          error.textContent = `No se encontraron ${criterio} con "${esc(valor)}".`;
          error.style.display = "block";
        } else if (benchmarkPrefix && items[0].codigo) {
          mostrarBenchmarkComparativa(benchmarkPrefix, items[0].codigo);
        }
      })
      .catch((err) => {
        btn.innerHTML = '<i class="fas fa-search"></i> Buscar';
        btn.disabled = false;
        error.textContent = "Error en la consulta: " + esc(err.message);
        error.style.display = "block";
        ocultarBenchmark();
      });
  }

  btn.addEventListener("click", ejecutar);
  input.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(ejecutar, 350);
  });
  input.addEventListener("keypress", (e) => { if (e.key === "Enter") ejecutar(); });
}

function renderResultList(el, items, criterio) {
  el.innerHTML = "";
  items.forEach((p) => {
    const item = document.createElement("div");
    item.className = "result-item";
    item.innerHTML = `
      <div class="result-item__info">
        <strong>#${esc(p.codigo)} — ${esc(p.nombre)}</strong>
        <span>${esc(p.especie || "")} · ${esc(p.raza || "")} · Dueño: ${esc(p.duenio || "")}</span>
      </div>
      <div class="result-item__badge">Tel: ${esc(p.telefono || "—")}</div>
    `;
    el.appendChild(item);
  });
  el.style.display = "block";
}

/* ---------- Comparativa integrada: Lista vs BST para nombre/dueño ---------- */
function mostrarBenchmarkComparativa(prefix, codigo) {
  const contenedor = $(prefix.toLowerCase() + "Benchmark");
  if (!contenedor) return;
  contenedor.style.display = "none";

  fetch(`${API_BASE}/comparar?codigo=${encodeURIComponent(String(codigo).padStart(3, "0"))}`)
    .then((res) => res.json().catch(() => ({})))
    .then((cmp) => {
      if (!cmp || cmp.error) return;
      const nLista = cmp.busqueda_lista?.comparaciones ?? 0;
      const nBst = cmp.busqueda_bst?.comparaciones ?? 0;
      const ahorro = cmp.ahorro_comparaciones ?? 0;

      $("#bench" + prefix + "Lista").textContent = nLista;
      $("#bench" + prefix + "Bst").textContent = nBst;

      if (nBst < nLista) {
        $("#bench" + prefix + "Verdict").textContent = "Árbol BST";
        $("#bench" + prefix + "Verdict").className = "bench-value verdict-text ganador-bst";
        const pct = nLista > 0 ? Math.round((ahorro / nLista) * 100) : 0;
        $("#bench" + prefix + "Ahorro").textContent = `BST usó ${ahorro} comparación(es) menos (${pct}% menos).`;
      } else if (nLista < nBst) {
        $("#bench" + prefix + "Verdict").textContent = "Lista lineal";
        $("#bench" + prefix + "Verdict").className = "bench-value verdict-text ganador-lista";
        $("#bench" + prefix + "Ahorro").textContent = `Lista usó ${nLista - nBst} comparación(es) menos.`;
      } else {
        $("#bench" + prefix + "Verdict").textContent = "Empate";
        $("#bench" + prefix + "Verdict").className = "bench-value verdict-text ganador-empate";
        $("#bench" + prefix + "Ahorro").textContent = "Ambos usaron la misma cantidad de comparaciones.";
      }
      contenedor.style.display = "block";
    })
    .catch(() => {
      contenedor.style.display = "none";
    });
}

setupGeneralSearch("#nameInput", "#btnSearchName", "nombre", "#nameResult", "#nameError", "Name");
setupGeneralSearch("#ownerInput", "#btnSearchOwner", "duenio", "#ownerResult", "#ownerError", "Owner");

/* ---------- Búsqueda por Código (entero) ---------- */
const codeInput = $("#codeInput");
const btnSearchCode = $("#btnSearchCode");
const codeResult = $("#codeResult");
const codeError = $("#codeError");
const codeBenchmark = $("#codeBenchmark");

function buscarPorCodigo() {
  const valor = codeInput.value.trim();
  codeResult.style.display = "none";
  codeError.style.display = "none";

  if (!/^\d+$/.test(valor) || parseInt(valor, 10) <= 0) {
    codeError.textContent = "Ingrese un código entero positivo válido.";
    codeError.style.display = "block";
    return;
  }

  btnSearchCode.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i>';
  btnSearchCode.disabled = true;

  fetch(`${API_BASE}/buscar/general?criterio=codigo&valor=${encodeURIComponent(valor)}`)
    .then((res) => res.json().catch(() => ({})))
    .then((data) => {
      btnSearchCode.innerHTML = '<i class="fas fa-search"></i> Buscar';
      btnSearchCode.disabled = false;
      const items = Array.isArray(data) ? data : data.resultados || [];
      if (!items.length) {
        codeError.textContent = `No existe paciente con código #${esc(valor)}.`;
        codeError.style.display = "block";
        return;
      }
      const p = items[0];
      $("#codeResultCode").textContent = p.codigo;
      $("#codeResultName").textContent = p.nombre;
      $("#codeResultSpecies").textContent = p.especie;
      $("#codeResultBreed").textContent = p.raza || "—";
      $("#codeResultOwner").textContent = p.duenio;
      $("#codeResultPhone").textContent = p.telefono || "—";
      codeResult.style.display = "block";
      codeBenchmark.style.display = "none";

      // Comparativa integrada: Lista vs BST para este código, al momento de buscar
      fetch(`${API_BASE}/comparar?codigo=${encodeURIComponent(valor.padStart(3, "0"))}`)
        .then((res) => res.json().catch(() => ({})))
        .then((cmp) => {
          if (!cmp || cmp.error) return;
          const nLista = cmp.busqueda_lista?.comparaciones ?? 0;
          const nBst = cmp.busqueda_bst?.comparaciones ?? 0;
          const ahorro = cmp.ahorro_comparaciones ?? 0;

          $("#benchCodeLista").textContent = nLista;
          $("#benchCodeBst").textContent = nBst;

          if (nBst < nLista) {
            $("#benchCodeVerdict").textContent = "Árbol BST";
            $("#benchCodeVerdict").className = "bench-value verdict-text ganador-bst";
            const pct = nLista > 0 ? Math.round((ahorro / nLista) * 100) : 0;
            $("#benchCodeAhorro").textContent = `BST usó ${ahorro} comparación(es) menos (${pct}% menos).`;
          } else if (nLista < nBst) {
            $("#benchCodeVerdict").textContent = "Lista lineal";
            $("#benchCodeVerdict").className = "bench-value verdict-text ganador-lista";
            $("#benchCodeAhorro").textContent = `Lista usó ${nLista - nBst} comparación(es) menos.`;
          } else {
            $("#benchCodeVerdict").textContent = "Empate";
            $("#benchCodeVerdict").className = "bench-value verdict-text ganador-empate";
            $("#benchCodeAhorro").textContent = "Ambos usaron la misma cantidad de comparaciones.";
          }
          codeBenchmark.style.display = "block";
        })
        .catch(() => {
          codeBenchmark.style.display = "none";
        });
    })
    .catch((err) => {
      btnSearchCode.innerHTML = '<i class="fas fa-search"></i> Buscar';
      btnSearchCode.disabled = false;
      codeError.textContent = "Error en la consulta: " + esc(err.message);
      codeError.style.display = "block";
      codeBenchmark.style.display = "none";
    });
}
btnSearchCode.addEventListener("click", buscarPorCodigo);
codeInput.addEventListener("keypress", (e) => { if (e.key === "Enter") buscarPorCodigo(); });

/* ============================================================
   Módulo: Sacar Turno (Nueva cita veterinaria)
   POST a /api/turnos con fallback a localStorage
   ============================================================ */

const TURNO_API = `${API_BASE}/turnos`;
const TURNO_STORAGE_KEY = "vet_turnos";

// Turnos pendientes solicitados (se muestran en la sección de Vacunas y Controles)
let turnosPendientes = [];

const turno = {
  form: $("#formTurno"),
  confirm: $("#turnoConfirm"),
  inputs: {
    duenio: $("#tDuenio"),
    telefono: $("#tTelefono"),
    mascota: $("#tMascota"),
    especie: $("#tEspecie"),
    motivo: $("#tMotivo"),
    fecha: $("#tFecha"),
    horario: $("#tHorario"),
    veterinario: $("#tVeterinario"),
    observaciones: $("#tObservaciones"),
  },
  errors: {
    duenio: $("#errT_Duenio"),
    telefono: $("#errT_Telefono"),
    mascota: $("#errT_Mascota"),
    especie: $("#errT_Especie"),
    motivo: $("#errT_Motivo"),
    fecha: $("#errT_Fecha"),
    horario: $("#errT_Horario"),
    veterinario: $("#errT_Veterinario"),
    observaciones: $("#errT_Observaciones"),
  },
  btnSubmit: $("#btnTurnoSubmit"),
  btnLimpiar: $("#btnTurnoLimpiar"),
  btnCerrarConfirm: $("#btnTurnoCerrar"),
  btnNuevoConfirm: $("#btnTurnoNuevo"),
  disponibilidad: $("#turnoDisponibilidad"),
  resumen: {
    mascota: $("#resMascota"),
    duenio: $("#resDuenio"),
    telefono: $("#resTelefono"),
    especie: $("#resEspecie"),
    motivo: $("#resMotivo"),
    fecha: $("#resFecha"),
    horario: $("#resHorario"),
    veterinario: $("#resVeterinario"),
    observaciones: $("#resObs"),
  },
};

const VETERINARIOS = [
  "Dra. Ana Martínez — Medicina general",
  "Dr. Carlos Ruiz — Cirugía",
  "Dra. Sofía López — Vacunación",
  "Dr. Miguel Torres — Emergencias",
  "Dra. Elena Gómez — Controles",
];

/* ---------- Utilidades de validación ---------- */
function limpiarErroresTurno() {
  Object.values(turno.errors).forEach((e) => { if (e) e.textContent = ""; });
  Object.values(turno.inputs).forEach((i) => { if (i) i.classList.remove("input-error"); });
}

function marcarErrorTurno(campo, msg) {
  const input = turno.inputs[campo];
  const err = turno.errors[campo];
  if (input) input.classList.add("input-error");
  if (err) err.textContent = msg;
}

function validoTelefono(valor) {
  if (!valor) return false;
  const digitos = valor.replace(/\D/g, "");
  return digitos.length >= 7 && digitos.length <= 15;
}

function fechaNoEsFinDeSemana(fechaStr) {
  const d = new Date(fechaStr + "T00:00:00");
  const dia = d.getDay();
  return dia !== 0 && dia !== 6;
}

function fechaNoEsPasada(fechaStr) {
  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);
  const d = new Date(fechaStr + "T00:00:00");
  return d >= hoy;
}

/* ---------- Disponibilidad de horarios ---------- */
async function cargarDisponibilidad() {
  const fecha = turno.inputs.fecha.value.trim();
  const vet = turno.inputs.veterinario.value.trim();
  const contenedor = turno.disponibilidad;
  if (!contenedor) return;

  contenedor.style.display = "none";
  contenedor.className = "turno-disponibilidad";

  if (!fecha) return;

  // Validación de fin de semana / fecha pasada (UX temprana)
  if (!fechaNoEsPasada(fecha)) {
    contenedor.style.display = "block";
    contenedor.textContent = "La fecha no puede ser anterior a hoy.";
    contenedor.className = "turno-disponibilidad--warn";
    return;
  }
  if (!fechaNoEsFinDeSemana(fecha)) {
    contenedor.style.display = "block";
    contenedor.innerHTML = '<i class="fas fa-calendar-times" aria-hidden="true"></i> La clínica no atiende fines de semana.';
    contenedor.className = "turno-disponibilidad--warn";
    return;
  }

  // Intento de integración con backend (fallback a datos locales si falla)
  try {
    const url = vet
      ? `${TURNO_API}/disponibilidad?fecha=${encodeURIComponent(fecha)}&veterinario=${encodeURIComponent(vet)}`
      : `${TURNO_API}/disponibilidad?fecha=${encodeURIComponent(fecha)}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Sin disponibilidad");
    const data = await res.json().catch(() => ({}));
    const slots = Array.isArray(data) ? data : data.slots || [];
    renderDisponibilidad(slots.length > 0 ? slots : [], true);
  } catch (err) {
    // Fallback: disponibilidad simulada (sin backend de turnos aún)
    const horarios = {
      Mañana: ["09:00", "10:00", "11:00"],
      Tarde: ["14:00", "15:00", "16:00", "17:00"],
      Noche: ["18:00", "19:00", "20:00"],
    };
    const horarioSel = turno.inputs.horario.value || "Mañana";
    const slots = horarios[horarioSel] || [];
    renderDisponibilidad(slots, false);
  }
}

function renderDisponibilidad(slots, desdeApi) {
  const contenedor = turno.disponibilidad;
  if (!slots || slots.length === 0) {
    contenedor.style.display = "block";
    contenedor.innerHTML = '<i class="fas fa-times-circle" aria-hidden="true"></i> Sin horarios disponibles para esa fecha.';
    contenedor.className = "turno-disponibilidad--warn";
    return;
  }
  contenedor.style.display = "block";
  contenedor.innerHTML = `<i class="fas fa-check-circle" aria-hidden="true"></i> Horarios disponibles${desdeApi ? "" : " (estimados)"}: ${slots.join(" · ")}`;
  contenedor.className = "turno-disponibilidad--ok";
}

/* ---------- Envío del formulario ---------- */
async function guardarTurno(datos) {
  const btn = turno.btnSubmit;
  const txtOrig = btn.innerHTML;
  btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Procesando...';
  btn.disabled = true;

  let exito = false;
  let mensaje = "";

  try {
    const res = await fetch(TURNO_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw data.error || data.msg || "Error al solicitar el turno";
    exito = true;
    mensaje = data.mensaje || "Turno solicitado correctamente.";
  } catch (err) {
    // Fallback: almacenamiento local si el backend no responde
    try {
      const previos = JSON.parse(localStorage.getItem(TURNO_STORAGE_KEY) || "[]");
      previos.push({ ...datos, fechaSolicitud: new Date().toISOString(), estado: "pendiente_local" });
      localStorage.setItem(TURNO_STORAGE_KEY, JSON.stringify(previos));
      exito = true;
      mensaje = "Turno registrado localmente (el servidor no respondió). Se confirmará cuando se restablezca el servicio.";
    } catch (e) {
      exito = false;
      mensaje = String(err.message || err);
    }
  } finally {
    btn.innerHTML = txtOrig;
    btn.disabled = false;
  }

  return { exito, mensaje };
}

function mostrarConfirmacionTurno(datos) {
  turno.confirm.style.display = "block";
  turno.form.style.display = "none";

  const fechaLegible = datos.fecha
    ? new Date(datos.fecha + "T00:00:00").toLocaleDateString("es-AR", {
        weekday: "long", year: "numeric", month: "long", day: "numeric",
      })
    : "—";

  turno.resumen.mascota.textContent = esc(datos.mascota);
  turno.resumen.duenio.textContent = esc(datos.duenio);
  turno.resumen.telefono.textContent = esc(datos.telefono);
  turno.resumen.especie.textContent = esc(datos.especie);
  turno.resumen.motivo.textContent = esc(datos.motivo);
  turno.resumen.fecha.textContent = fechaLegible;
  turno.resumen.horario.textContent = esc(datos.horario);
  turno.resumen.veterinario.textContent = esc(datos.veterinario) || "— Asignado por la clínica —";
  turno.resumen.observaciones.textContent = esc(datos.observaciones) || "—";

  // Registrar turno en la lista de pendientes para mostrar en Vacunas y Controles
  turnosPendientes.unshift({
    codigo: datos.codigo || "—",
    mascota: datos.mascota,
    duenio: datos.duenio,
    telefono: datos.telefono,
    especie: datos.especie,
    motivo: datos.motivo,
    fecha: datos.fecha,
    horario: datos.horario,
    veterinario: datos.veterinario || "—",
    observaciones: datos.observaciones || "",
    estado: "pendiente",
    fechaSolicitud: new Date().toISOString(),
  });
  renderTurnosPendientes();
}

function limpiarFormularioTurno() {
  limpiarErroresTurno();
  turno.form.reset();
  turno.disponibilidad.style.display = "none";
  // Resetear fecha mínima por si acaso
  if (turno.inputs.fecha) turno.inputs.fecha.value = "";
}

async function handleSubmitTurno(e) {
  e.preventDefault();
  limpiarErroresTurno();

  const valores = {
    duenio: turno.inputs.duenio.value.trim(),
    telefono: turno.inputs.telefono.value.trim(),
    mascota: turno.inputs.mascota.value.trim(),
    especie: turno.inputs.especie.value.trim(),
    motivo: turno.inputs.motivo.value.trim(),
    fecha: turno.inputs.fecha.value.trim(),
    horario: turno.inputs.horario.value.trim(),
    veterinario: turno.inputs.veterinario.value.trim(),
    observaciones: turno.inputs.observaciones.value.trim(),
  };

  let valido = true;

  if (!valores.duenio) { marcarErrorTurno("duenio", "El nombre del dueño es obligatorio."); valido = false; }
  if (!valores.telefono) { marcarErrorTurno("telefono", "El teléfono es obligatorio."); valido = false; }
  else if (!validoTelefono(valores.telefono)) { marcarErrorTurno("telefono", "Ingrese un teléfono válido (7 a 15 dígitos)."); valido = false; }
  if (!valores.mascota) { marcarErrorTurno("mascota", "El nombre de la mascota es obligatorio."); valido = false; }
  if (!valores.especie) { marcarErrorTurno("especie", "Seleccione el tipo de animal."); valido = false; }
  if (!valores.motivo) { marcarErrorTurno("motivo", "Seleccione el motivo de la consulta."); valido = false; }
  if (!valores.fecha) { marcarErrorTurno("fecha", "Seleccione una fecha."); valido = false; }
  else if (!fechaNoEsPasada(valores.fecha)) { marcarErrorTurno("fecha", "La fecha no puede ser anterior a hoy."); valido = false; }
  else if (!fechaNoEsFinDeSemana(valores.fecha)) { marcarErrorTurno("fecha", "La clínica no atiende los fines de semana."); valido = false; }
  if (!valores.horario) { marcarErrorTurno("horario", "Seleccione un horario."); valido = false; }

  if (!valido) {
    toastErr("Completa los campos obligatorios y corrige los errores.");
    return;
  }

  const { exito, mensaje } = await guardarTurno(valores);

  if (exito) {
    toastOk(mensaje);
    mostrarConfirmacionTurno(valores);
  } else {
    toastErr(mensaje || "No se pudo solicitar el turno. Intente nuevamente.");
  }
}

/* ---------- Inicialización del módulo ---------- */
function initTurno() {
  if (!turno.form) return;

  // Fecha mínima = hoy (date picker no permite pasadas)
  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);
  turno.inputs.fecha.min = hoy.toISOString().split("T")[0];

  // Recalcular disponibilidad al cambiar fecha / veterinario / horario
  turno.inputs.fecha.addEventListener("change", cargarDisponibilidad);
  turno.inputs.veterinario.addEventListener("change", cargarDisponibilidad);
  turno.inputs.horario.addEventListener("change", cargarDisponibilidad);

  // Validación en tiempo real del teléfono
  turno.inputs.telefono.addEventListener("input", () => {
    const v = turno.inputs.telefono.value.trim();
    if (v && !validoTelefono(v)) {
      turno.inputs.telefono.classList.add("input-error");
      turno.errors.telefono.textContent = "Formato de teléfono inválido.";
    } else {
      turno.inputs.telefono.classList.remove("input-error");
      turno.errors.telefono.textContent = "";
    }
  });

  turno.btnLimpiar.addEventListener("click", () => {
    limpiarFormularioTurno();
    turno.confirm.style.display = "none";
    turno.form.style.display = "block";
  });

  turno.btnCerrarConfirm.addEventListener("click", () => {
    turno.confirm.style.display = "none";
    turno.form.style.display = "block";
    limpiarFormularioTurno();
  });

  turno.btnNuevoConfirm.addEventListener("click", () => {
    turno.confirm.style.display = "none";
    turno.form.style.display = "block";
    limpiarFormularioTurno();
  });

  turno.form.addEventListener("submit", handleSubmitTurno);
}

/* ---------- Inicialización global ---------- */
cargarCatalogo();
initTurno();
