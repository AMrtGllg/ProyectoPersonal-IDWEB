const formulario = document.getElementById("formularioContacto");
const campos = {
    nombre: document.getElementById("nombre"),
    email: document.getElementById("email"),
    asunto: document.getElementById("asunto"),
    mensaje: document.getElementById("mensaje")
};

const errores = {
    nombre: document.getElementById("errorNombre"),
    email: document.getElementById("errorEmail"),
    asunto: document.getElementById("errorAsunto"),
    mensaje: document.getElementById("errorMensaje")
};

const mensajeConfirmacion = document.getElementById("mensajeConfirmacion");


campos.mensaje.addEventListener("input", () => {
    document.getElementById("contadorActual").textContent = campos.mensaje.value.length;
});

const validaciones = {
    nombre: (valor) => {
        return valor.trim().length >= 3;
    },
    email: (valor) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(valor);
    },
    asunto: (valor) => {
        return valor.trim().length >= 5;
    },
    mensaje: (valor) => {
        return valor.trim().length >= 10 && valor.trim().length <= 500;
    }
};


function validarCampo(nombreCampo) {
    const campo = campos[nombreCampo];
    const esValido = validaciones[nombreCampo](campo.value);

    if (esValido) {
        campo.classList.remove("invalido");
        errores[nombreCampo].style.display = "none";
    } else {
        campo.classList.add("invalido");
        errores[nombreCampo].style.display = "block";
    }

    return esValido;
}

Object.keys(campos).forEach(nombreCampo => {
    campos[nombreCampo].addEventListener("blur", () => {
        validarCampo(nombreCampo);
    });


    campos[nombreCampo].addEventListener("input", () => {
        if (campos[nombreCampo].classList.contains("invalido")) {
            validarCampo(nombreCampo);
        }
    });
});


function mostrarMensaje(texto, tipo) {
    mensajeConfirmacion.innerHTML = texto;
    mensajeConfirmacion.className = `mensaje ${tipo}`;

    if (tipo === 'exito') {
        setTimeout(() => {
            mensajeConfirmacion.className = "mensaje";
        }, 4000);
    }
}

formulario.addEventListener("submit", (e) => {
    e.preventDefault();


    let formularioValido = true;
    Object.keys(campos).forEach(nombreCampo => {
        if (!validarCampo(nombreCampo)) {
            formularioValido = false;
        }
    });

    if (!formularioValido) {
        mostrarMensaje("Completa todos los campos correctamente porfav", "error");
        return;
    }

    const datosFormulario = {
        nombre: campos.nombre.value.trim(),
        email: campos.email.value.trim(),
        asunto: campos.asunto.value.trim(),
        mensaje: campos.mensaje.value.trim(),
        fecha: new Date().toLocaleString('es-PE')
    };

    fetch('/enviar-contacto', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(datosFormulario)
})
  .then(r => {
    if (!r.ok) throw new Error('Error en el servidor');
    return r.json();
  })
  .then(d => {
    console.log(d);
    mostrarMensaje("Mensaje enviado con éxito! me pondré en contacto algún día.", "exito");
    formulario.reset();
    document.getElementById("contadorActual").textContent = "0";
    Object.values(campos).forEach(campo => campo.classList.remove("invalido"));
  })
  .catch(err => {
    console.error(err);
    mostrarMensaje("Ocurrió un error al enviar el mensaje. Intenta de nuevo.", "error");
  });


    formulario.reset();
    document.getElementById("contadorActual").textContent = '0';
    Object.values(campos).forEach(campo => campo.classList.remove("invalido"));

    console.log("Datos guardados:", datosFormulario);
});

console.log("Formulario de contacto cargado");
