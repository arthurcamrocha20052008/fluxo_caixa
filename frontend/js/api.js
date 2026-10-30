/*
 * FLUXO DE CAIXA
 * Comunicação com a API FastAPI.
 */

function traduzirMensagemErroApi(mensagemBruta, statusHttp = 400) {
    const msg = String(mensagemBruta || "").trim();
    if (!msg) {
        return `Erro HTTP ${statusHttp}.`;
    }

    const textolimpo = msg.replace(/^Value error,\s*/i, "").trim();
    const lower = textoLimpoMinusculo(textolimpo);

    if (
        lower.includes("not a valid email") ||
        lower.includes("email address") ||
        lower.includes("part after the @-sign") ||
        lower.includes("an email address must have an @-sign")
    ) {
        return "Informe um endereço de e-mail válido (ex.: nome@dominio.com).";
    }
    if (lower.includes("field required") || lower === "missing") {
        return "Preencha todos os campos obrigatórios antes de continuar.";
    }
    if (lower.includes("string should have at least")) {
        return "Um dos campos informados possui menos caracteres do que o mínimo exigido.";
    }
    if (lower.includes("string should have at most")) {
        return "Um dos campos informados excedeu o limite máximo de caracteres.";
    }
    if (lower.includes("input should be a valid")) {
        return "Verifique o formato dos dados preenchidos e tente novamente.";
    }
    if (lower.includes("json decode error") || lower.includes("invalid json")) {
        return "Os dados enviados estão em formato inválido.";
    }

    return textoLimpoFinal(textolimpo);
}

function textoLimpoMinusculo(texto) {
    return String(texto || "").toLowerCase();
}

function textoLimpoFinal(texto) {
    return String(texto || "").trim();
}
const RENDER_API_URL = "https://fluxo-caixa-cuq1.onrender.com";

function obterUrlBaseApi() {
    if (window.__API_URL__) {
        return window.__API_URL__.replace(/\/+$/, "");
    }
    const urlPersistida = localStorage.getItem("fluxo_caixa_api_url");
    if (urlPersistida) {
        return urlPersistida.trim().replace(/\/+$/, "");
    }
    // Quando executado em HTTPS (Vercel / Produção), conecta ao backend no Render
    if (window.location.protocol === "https:") {
        return RENDER_API_URL;
    }
    // Ambiente de desenvolvimento local em HTTP
    return "http://127.0.0.1:8000";
}

const API_BASE_URL = obterUrlBaseApi();

const api = {
    getToken() {
        return sessionStorage.getItem("fluxo_caixa_token");
    },

    setToken(token) {
        sessionStorage.setItem("fluxo_caixa_token", token);
    },

    clearToken() {
        sessionStorage.removeItem("fluxo_caixa_token");
        sessionStorage.removeItem("fluxo_caixa_nome_usuario");
    },

    async request(path, options = {}) {
        const headers = new Headers(options.headers || {});
        const body = options.body;

        if (
            body !== undefined &&
            body !== null &&
            !(body instanceof FormData) &&
            !(body instanceof URLSearchParams) &&
            !headers.has("Content-Type")
        ) {
            headers.set("Content-Type", "application/json");
        }

        const token = this.getToken();
        if (token) {
            headers.set("Authorization", `Bearer ${token}`);
        }

        let response;
        try {
            response = await fetch(`${API_BASE_URL}${path}`, {
                ...options,
                headers
            });
        } catch (erro) {
            console.error("Erro na comunicação com a API:", erro);
            if (window.location.protocol === "https:" && API_BASE_URL.startsWith("http://")) {
                throw new Error(
                    "Bloqueio de conteúdo misto (HTTPS para HTTP). Para conectar à API a partir da Vercel, configure a URL segura da API: localStorage.setItem('fluxo_caixa_api_url', 'https://sua-api.com')"
                );
            }
            throw new Error(
                "Não foi possível conectar à API. Se o servidor estiver iniciando no Render (plano gratuito), aguarde cerca de 30 segundos e tente novamente."
            );
        }

        if (response.status === 401 && token) {
            this.clearToken();
            throw new Error(
                "Sessão expirada ou não autorizada. Faça login novamente."
            );
        }

        if (response.status === 401) {
            let message = "E-mail ou senha inválidos.";
            try {
                const data = await response.json();
                if (typeof data.detail === "string") {
                    message = data.detail;
                }
            } catch {
                // Mantém a mensagem de autenticação padrão.
            }
            throw new Error(message);
        }

        if (!response.ok) {
            let message = `Erro HTTP ${response.status}.`;
            try {
                const data = await response.json();
                if (typeof data.detail === "string") {
                    message = traduzirMensagemErroApi(data.detail, response.status);
                } else if (Array.isArray(data.detail)) {
                    const partes = data.detail
                        .map((error) =>
                            traduzirMensagemErroApi(error?.msg || "", response.status)
                        )
                        .filter(Boolean);
                    message = [...new Set(partes)].join(" ") || message;
                }
            } catch {
                // Mantém a mensagem HTTP quando a resposta não contém JSON.
            }
            throw new Error(message);
        }

        if (response.status === 204) {
            return null;
        }

        try {
            return await response.json();
        } catch (erro) {
            console.error("Erro na comunicação com a API:", erro);
            if (window.location.protocol === "https:" && API_BASE_URL.startsWith("http://")) {
                throw new Error(
                    "Bloqueio de conteúdo misto (HTTPS para HTTP). Para conectar à API a partir da Vercel, configure a URL segura da API: localStorage.setItem('fluxo_caixa_api_url', 'https://sua-api.com')"
                );
            }
            throw new Error("A API retornou uma resposta inválida.");
        }
    },

    get(path) {
        return this.request(path);
    },

    post(path, data) {
        return this.request(path, {
            method: "POST",
            body: JSON.stringify(data)
        });
    },

    postForm(path, data) {
        return this.request(path, {
            method: "POST",
            body: new URLSearchParams(data)
        });
    },

    put(path, data) {
        return this.request(path, {
            method: "PUT",
            body: JSON.stringify(data)
        });
    },

    delete(path, data) {
        const options = {
            method: "DELETE"
        };
        if (data !== undefined) {
            options.body = JSON.stringify(data);
        }
        return this.request(path, options);
    }
};

function aplicarTemaPreferido(tema) {
    const temaFinal = tema === "dark" ? "dark" : "light";
    const paginaSempreEscura = Boolean(
        document.body &&
            (document.body.classList.contains("login-page") ||
                document.body.classList.contains("landing-page"))
    );

    if (paginaSempreEscura) {
        document.documentElement.setAttribute("data-theme", "dark");
        document.body.classList.add("dark-theme");
        document.body.classList.remove("light-theme");
        return;
    }

    document.documentElement.setAttribute("data-theme", temaFinal);
    if (document.body) {
        document.body.classList.toggle("dark-theme", temaFinal === "dark");
        document.body.classList.toggle("light-theme", temaFinal !== "dark");
    }
    localStorage.setItem("fluxo_caixa_tema", temaFinal);
}

function inicializarTemaSalvo() {
    const temaSalvo = localStorage.getItem("fluxo_caixa_tema") || "light";
    aplicarTemaPreferido(temaSalvo);
}

inicializarTemaSalvo();
document.addEventListener("DOMContentLoaded", inicializarTemaSalvo);

// ====================================================================
// HOOK GLOBAL DE SCROLL LOCK E FECHAMENTO AO CLICAR FORA (CLICK OUTSIDE)
// ====================================================================
if (typeof HTMLDialogElement !== "undefined" && !HTMLDialogElement.prototype.__scrollLockHooked) {
    HTMLDialogElement.prototype.__scrollLockHooked = true;
    
    function vincularFechamentoCliqueFora(dialog) {
        if (!dialog || dialog.__clickOutsideAttached) return;
        dialog.__clickOutsideAttached = true;
        dialog.addEventListener("click", (event) => {
            if (event.target !== dialog) return;
            const rect = dialog.getBoundingClientRect();
            const clicouFora = (
                event.clientX < rect.left ||
                event.clientX > rect.right ||
                event.clientY < rect.top ||
                event.clientY > rect.bottom
            );
            if (clicouFora && typeof dialog.close === "function") {
                dialog.close();
            }
        });
    }

    const showModalOriginal = HTMLDialogElement.prototype.showModal;
    HTMLDialogElement.prototype.showModal = function(...args) {
        document.body.classList.add("modal-open");
        document.documentElement.classList.add("modal-open");
        vincularFechamentoCliqueFora(this);
        return showModalOriginal.apply(this, args);
    };

    const closeOriginal = HTMLDialogElement.prototype.close;
    HTMLDialogElement.prototype.close = function(...args) {
        const res = closeOriginal.apply(this, args);
        setTimeout(() => {
            const abertos = document.querySelectorAll("dialog[open]");
            if (abertos.length === 0) {
                document.body.classList.remove("modal-open");
                document.documentElement.classList.remove("modal-open");
            }
        }, 0);
        return res;
    };

    window.addEventListener("DOMContentLoaded", () => {
        document.querySelectorAll("dialog").forEach((dlg) => {
            vincularFechamentoCliqueFora(dlg);
            const removerScroll = () => {
                setTimeout(() => {
                    const abertos = document.querySelectorAll("dialog[open]");
                    if (abertos.length === 0) {
                        document.body.classList.remove("modal-open");
                        document.documentElement.classList.remove("modal-open");
                    }
                }, 0);
            };
            dlg.addEventListener("cancel", removerScroll);
            dlg.addEventListener("close", removerScroll);
        });
    });
}

// ====================================================================
// FUNÇÕES UTILITÁRIAS DE VALIDAÇÃO COMPARTILHADAS (CPF, TELEFONE, EMAIL, SENHA)
// ====================================================================

const MAPA_DOMINIOS_EMAIL_SUGERIDOS = {
    "gamil.com": "gmail.com",
    "gnail.com": "gmail.com",
    "gmial.com": "gmail.com",
    "gmai.com": "gmail.com",
    "gmail.con": "gmail.com",
    "gmail.cmo": "gmail.com",
    "gmail.cm": "gmail.com",
    "hotmial.com": "hotmail.com",
    "hotmal.com": "hotmail.com",
    "hotmail.con": "hotmail.com",
    "outlok.com": "outlook.com",
    "outllok.com": "outlook.com",
    "outlook.con": "outlook.com",
    "yaho.com": "yahoo.com",
    "yahooo.com": "yahoo.com",
    "yahoo.con": "yahoo.com"
};

function formatarMascaraCpf(valor) {
    const digitos = String(valor || "").replace(/\D/g, "").slice(0, 11);
    if (!digitos) return "";
    if (digitos.length <= 3) return digitos;
    if (digitos.length <= 6) return `${digitos.slice(0, 3)}.${digitos.slice(3)}`;
    if (digitos.length <= 9) return `${digitos.slice(0, 3)}.${digitos.slice(3, 6)}.${digitos.slice(6)}`;
    return `${digitos.slice(0, 3)}.${digitos.slice(3, 6)}.${digitos.slice(6, 9)}-${digitos.slice(9)}`;
}

function validarCpfMatematico(cpf) {
    const bruto = String(cpf || "").trim();
    if (!bruto) {
        return { valido: false, incompleto: true, mensagem: "Informe o CPF do titular." };
    }
    if (/[^0-9.\-\s]/.test(bruto)) {
        return { valido: false, incompleto: false, mensagem: "O CPF deve conter apenas números." };
    }
    const digitos = bruto.replace(/\D/g, "");
    if (digitos.length !== 11) {
        return {
            valido: false,
            incompleto: digitos.length < 11,
            mensagem: "CPF inválido. Verifique os números digitados."
        };
    }
    if (/^(\d)\1{10}$/.test(digitos)) {
        return {
            valido: false,
            incompleto: false,
            mensagem: "CPF inválido. Verifique os números digitados."
        };
    }
    let soma1 = 0;
    for (let i = 0; i < 9; i += 1) {
        soma1 += Number(digitos[i]) * (10 - i);
    }
    let resto1 = (soma1 * 10) % 11;
    if (resto1 === 10) resto1 = 0;

    let soma2 = 0;
    for (let i = 0; i < 10; i += 1) {
        soma2 += Number(digitos[i]) * (11 - i);
    }
    let resto2 = (soma2 * 10) % 11;
    if (resto2 === 10) resto2 = 0;

    if (resto1 !== Number(digitos[9]) || resto2 !== Number(digitos[10])) {
        return {
            valido: false,
            incompleto: false,
            mensagem: "CPF inválido. Verifique os números digitados."
        };
    }
    return {
        valido: true,
        incompleto: false,
        digitos,
        mensagem: "CPF válido verificado."
    };
}

function vincularValidacaoCpfTempoReal(inputCpf, elementoFeedback = null, elementoErro = null) {
    if (!inputCpf) return;
    const erroEl = elementoErro || inputCpf.closest(".form-field, label")?.querySelector("small.field-error");
    const ocultarErro = () => {
        if (erroEl) {
            erroEl.textContent = "";
            erroEl.hidden = true;
        }
    };
    const exibirErro = (mensagem) => {
        if (erroEl) {
            erroEl.textContent = mensagem || "CPF inválido. Verifique os números digitados.";
            erroEl.hidden = false;
        }
    };
    const atualizarEstado = (exibirIncompleto = false) => {
        inputCpf.value = formatarMascaraCpf(inputCpf.value);
        const digitos = inputCpf.value.replace(/\D/g, "");
        if (!digitos) {
            inputCpf.classList.remove("input-valid", "input-invalid");
            inputCpf.removeAttribute("aria-invalid");
            ocultarErro();
            if (elementoFeedback) {
                elementoFeedback.hidden = false;
                elementoFeedback.textContent = "Criptografado em repouso (Fernet AES + HMAC-SHA256).";
                elementoFeedback.className = "field-help";
            }
            return;
        }
        const resultado = validarCpfMatematico(inputCpf.value);
        if (resultado.valido) {
            inputCpf.classList.add("input-valid");
            inputCpf.classList.remove("input-invalid");
            inputCpf.setAttribute("aria-invalid", "false");
            ocultarErro();
            if (elementoFeedback) {
                elementoFeedback.hidden = false;
                elementoFeedback.textContent = "✓ CPF matematicamente válido.";
                elementoFeedback.className = "field-feedback is-valid";
            }
        } else if (!resultado.incompleto || exibirIncompleto) {
            inputCpf.classList.add("input-invalid");
            inputCpf.classList.remove("input-valid");
            inputCpf.setAttribute("aria-invalid", "true");
            exibirErro(resultado.mensagem);
            if (elementoFeedback) {
                if (erroEl) {
                    elementoFeedback.hidden = true;
                } else {
                    elementoFeedback.hidden = false;
                    elementoFeedback.textContent = resultado.mensagem;
                    elementoFeedback.className = "field-feedback is-invalid";
                }
            }
        } else {
            inputCpf.classList.remove("input-valid", "input-invalid");
            inputCpf.removeAttribute("aria-invalid");
            ocultarErro();
            if (elementoFeedback) {
                elementoFeedback.hidden = false;
                elementoFeedback.textContent = `Digite os 11 números (${digitos.length}/11).`;
                elementoFeedback.className = "field-help";
            }
        }
    };
    inputCpf.addEventListener("input", () => atualizarEstado(false));
    inputCpf.addEventListener("blur", () => atualizarEstado(true));
}

function formatarMascaraTelefone(valor) {
    const bruto = String(valor || "");
    const temMais55 = /^\s*\+55/.test(bruto);
    const temMaisInternacional = /^\s*\+/.test(bruto) && !temMais55;
    if (temMaisInternacional) {
        return bruto.replace(/[^\d+ ()-]/g, "").slice(0, 22);
    }
    let digitos = bruto.replace(/\D/g, "");
    if (temMais55 && digitos.startsWith("55")) {
        digitos = digitos.slice(2);
    }
    digitos = digitos.slice(0, 11);
    if (!digitos) return temMais55 ? "+55 " : "";
    let formatado = "";
    if (digitos.length <= 2) {
        formatado = `(${digitos}`;
    } else if (digitos.length <= 6) {
        formatado = `(${digitos.slice(0, 2)}) ${digitos.slice(2)}`;
    } else if (digitos.length <= 10) {
        formatado = `(${digitos.slice(0, 2)}) ${digitos.slice(2, 6)}-${digitos.slice(6)}`;
    } else {
        formatado = `(${digitos.slice(0, 2)}) ${digitos.slice(2, 7)}-${digitos.slice(7, 11)}`;
    }
    return temMais55 ? `+55 ${formatado}` : formatado;
}

function validarTelefoneBrasileiro(valor, { obrigatorio = false } = {}) {
    const bruto = String(valor || "").trim();
    if (!bruto) {
        return {
            valido: !obrigatorio,
            incompleto: true,
            e164: "",
            mensagem: obrigatorio
                ? "Informe um telefone válido com DDD para receber o código por SMS ou WhatsApp."
                : ""
        };
    }
    if (/[^0-9+().\-\s]/.test(bruto)) {
        return {
            valido: false,
            incompleto: false,
            e164: "",
            mensagem: "O telefone contém caracteres inválidos."
        };
    }
    const digitosTotais = bruto.replace(/\D/g, "");
    if (bruto.startsWith("+") && !bruto.startsWith("+55")) {
        if (digitosTotais.length >= 10 && digitosTotais.length <= 15) {
            return {
                valido: true,
                incompleto: false,
                e164: `+${digitosTotais}`,
                mensagem: "Telefone internacional válido."
            };
        }
        return {
            valido: false,
            incompleto: digitosTotais.length < 10,
            e164: "",
            mensagem: "Informe um telefone válido com código do país (10 a 15 dígitos)."
        };
    }
    let nacional = digitosTotais;
    if ((bruto.startsWith("+55") || nacional.length === 12 || nacional.length === 13) && nacional.startsWith("55")) {
        nacional = nacional.slice(2);
    }
    if (nacional.length < 10) {
        return {
            valido: false,
            incompleto: true,
            e164: "",
            mensagem: "Informe o DDD (11 a 99) seguido do telefone com 8 ou 9 dígitos."
        };
    }
    if (nacional.length > 11) {
        return {
            valido: false,
            incompleto: false,
            e164: "",
            mensagem: "Telefone inválido. Use o formato (DD) 9XXXX-XXXX."
        };
    }
    const ddd = Number(nacional.slice(0, 2));
    if (!Number.isInteger(ddd) || ddd < 11 || ddd > 99) {
        return {
            valido: false,
            incompleto: false,
            e164: "",
            mensagem: "DDD inválido. Informe um DDD brasileiro válido entre 11 e 99."
        };
    }
    if (nacional.length === 11 && nacional[2] !== "9") {
        return {
            valido: false,
            incompleto: false,
            e164: "",
            mensagem: "Celulares com 11 dígitos devem começar com 9 após o DDD."
        };
    }
    return {
        valido: true,
        incompleto: false,
        e164: `+55${nacional}`,
        nacional,
        mensagem: "Telefone válido."
    };
}

function vincularValidacaoTelefoneTempoReal(inputTelefone, elementoErro = null, isObrigatorioFn = () => false) {
    if (!inputTelefone) return null;
    const erroEl = elementoErro || inputTelefone.closest(".form-field, label")?.querySelector("small.field-error");
    const atualizarEstado = (exibirIncompleto = false) => {
        inputTelefone.value = formatarMascaraTelefone(inputTelefone.value);
        const obrigatorio = Boolean(typeof isObrigatorioFn === "function" ? isObrigatorioFn() : isObrigatorioFn);
        const digitos = inputTelefone.value.replace(/\D/g, "");
        if (!digitos) {
            if (obrigatorio && exibirIncompleto) {
                inputTelefone.classList.add("input-invalid");
                inputTelefone.classList.remove("input-valid");
                inputTelefone.setAttribute("aria-invalid", "true");
                if (erroEl) {
                    erroEl.textContent = "Informe seu telefone com DDD para receber o código via SMS ou WhatsApp.";
                    erroEl.hidden = false;
                }
            } else {
                inputTelefone.classList.remove("input-valid", "input-invalid");
                inputTelefone.removeAttribute("aria-invalid");
                if (erroEl) {
                    erroEl.textContent = "";
                    erroEl.hidden = true;
                }
            }
            return;
        }
        const res = validarTelefoneBrasileiro(inputTelefone.value, { obrigatorio });
        if (res.valido) {
            inputTelefone.classList.add("input-valid");
            inputTelefone.classList.remove("input-invalid");
            inputTelefone.setAttribute("aria-invalid", "false");
            if (erroEl) {
                erroEl.textContent = "";
                erroEl.hidden = true;
            }
        } else if (!res.incompleto || exibirIncompleto) {
            inputTelefone.classList.add("input-invalid");
            inputTelefone.classList.remove("input-valid");
            inputTelefone.setAttribute("aria-invalid", "true");
            if (erroEl) {
                erroEl.textContent = res.mensagem;
                erroEl.hidden = false;
            }
        } else {
            inputTelefone.classList.remove("input-valid", "input-invalid");
            inputTelefone.removeAttribute("aria-invalid");
            if (erroEl) {
                erroEl.textContent = "";
                erroEl.hidden = true;
            }
        }
    };
    inputTelefone.addEventListener("input", () => atualizarEstado(false));
    inputTelefone.addEventListener("blur", () => atualizarEstado(true));
    return { revalidar: atualizarEstado };
}

function mascararEmailCliente(email) {
    const limpo = String(email || "").trim().toLowerCase();
    if (!limpo.includes("@")) return limpo || "—";
    const [local, dominio] = limpo.split("@");
    const prefixo = local.length <= 2 ? local.slice(0, 1) || "*" : local.slice(0, 2);
    return `${prefixo}***@${dominio}`;
}

function mascararTelefoneCliente(telefone) {
    const digitos = String(telefone || "").replace(/\D/g, "");
    let nac = digitos;
    if ((nac.length === 12 || nac.length === 13) && nac.startsWith("55")) {
        nac = nac.slice(2);
    }
    if (nac.length === 11) {
        return `(${nac.slice(0, 2)}) ${nac[2]}****-${nac.slice(-4)}`;
    }
    if (nac.length === 10) {
        return `(${nac.slice(0, 2)}) ****-${nac.slice(-4)}`;
    }
    return telefone || "(**) *****-****";
}

function detectarErroDominioEmail(email) {
    const valor = String(email || "").trim().toLowerCase();
    if (!valor.includes("@")) return null;
    const partes = valor.split("@");
    if (partes.length !== 2 || !partes[0] || !partes[1]) return null;
    const [usuario, dominio] = partes;
    const dominioSugerido = MAPA_DOMINIOS_EMAIL_SUGERIDOS[dominio];
    if (!dominioSugerido) return null;
    const sugestaoEmail = `${usuario}@${dominioSugerido}`;
    return {
        dominioDigitado: dominio,
        dominioSugerido,
        sugestaoEmail,
        mensagem: `Domínio '@${dominio}' parece incorreto. Você quis dizer ${sugestaoEmail}?`
    };
}

function validarEmailFormato(email) {
    const valor = String(email || "").trim();
    if (!valor || valor.length > 254 || /\s/.test(valor)) {
        return false;
    }
    const regexEmail = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    if (!regexEmail.test(valor)) {
        return false;
    }
    const partes = valor.split("@");
    if (partes.length !== 2) return false;
    const [usuario, dominio] = partes;
    if (
        usuario.startsWith(".") ||
        usuario.endsWith(".") ||
        usuario.includes("..") ||
        dominio.startsWith(".") ||
        dominio.startsWith("-") ||
        dominio.endsWith("-") ||
        dominio.includes("..")
    ) {
        return false;
    }
    if (detectarErroDominioEmail(valor)) {
        return false;
    }
    return true;
}

function vincularValidacaoEmailTempoReal(inputEmail, elementoErro = null) {
    if (!inputEmail) return;
    const erroEl = elementoErro || inputEmail.closest(".form-field, label")?.querySelector("small.field-error");
    let jaDesfocou = false;

    const limparEstado = () => {
        inputEmail.classList.remove("input-valid", "input-invalid");
        inputEmail.removeAttribute("aria-invalid");
        if (erroEl) {
            erroEl.textContent = "";
            erroEl.hidden = true;
        }
    };
    const marcarValido = () => {
        inputEmail.classList.add("input-valid");
        inputEmail.classList.remove("input-invalid");
        inputEmail.setAttribute("aria-invalid", "false");
        if (erroEl) {
            erroEl.textContent = "";
            erroEl.hidden = true;
        }
    };
    const renderizarSugestaoDominio = (erroDominio) => {
        inputEmail.classList.add("input-invalid");
        inputEmail.classList.remove("input-valid");
        inputEmail.setAttribute("aria-invalid", "true");
        if (!erroEl) return;
        erroEl.replaceChildren();
        const spanTexto = document.createElement("span");
        spanTexto.textContent = `${erroDominio.mensagem} `;
        const btnCorrigir = document.createElement("button");
        btnCorrigir.type = "button";
        btnCorrigir.className = "email-typo-fix-btn";
        btnCorrigir.textContent = `Usar @${erroDominio.dominioSugerido}`;
        btnCorrigir.addEventListener("click", () => {
            inputEmail.value = erroDominio.sugestaoEmail;
            marcarValido();
            inputEmail.focus();
        });
        erroEl.append(spanTexto, btnCorrigir);
        erroEl.hidden = false;
    };
    const marcarInvalido = (valorAtual = "") => {
        const erroDominio = detectarErroDominioEmail(valorAtual);
        if (erroDominio) {
            renderizarSugestaoDominio(erroDominio);
            return;
        }
        inputEmail.classList.add("input-invalid");
        inputEmail.classList.remove("input-valid");
        inputEmail.setAttribute("aria-invalid", "true");
        if (erroEl) {
            erroEl.textContent = "Informe um endereço de e-mail válido (ex.: nome@dominio.com).";
            erroEl.hidden = false;
        }
    };
    inputEmail.addEventListener("input", () => {
        const valor = inputEmail.value.trim();
        if (!valor) {
            limparEstado();
            return;
        }
        const erroDominio = detectarErroDominioEmail(valor);
        if (erroDominio) {
            renderizarSugestaoDominio(erroDominio);
            return;
        }
        if (validarEmailFormato(valor)) {
            marcarValido();
            return;
        }
        if (jaDesfocou || inputEmail.classList.contains("input-invalid")) {
            marcarInvalido(valor);
        } else {
            inputEmail.classList.remove("input-valid");
        }
    });
    inputEmail.addEventListener("blur", () => {
        const valor = inputEmail.value.trim();
        if (!valor) {
            limparEstado();
            return;
        }
        jaDesfocou = true;
        if (validarEmailFormato(valor)) {
            marcarValido();
        } else {
            marcarInvalido(valor);
        }
    });
}

function avaliarForcaSenha(senha) {
    const valor = String(senha || "");
    const criterios = {
        tamanho: valor.length >= 8,
        maiuscula: /[A-Z]/.test(valor),
        minuscula: /[a-z]/.test(valor),
        numero: /\d/.test(valor),
        especial: /[!@#$%^&*(),.?":{}|<>_\-\[\]\\\/+=~`';]/.test(valor)
    };
    const atendidos = Object.values(criterios).filter(Boolean).length;
    const valida = atendidos === 5;
    return { ...criterios, atendidos, valida };
}

function obterMensagemErroSenha(senha) {
    const status = avaliarForcaSenha(senha);
    if (!status.tamanho) return "A senha deve possuir no mínimo 8 caracteres.";
    if (!status.maiuscula) return "A senha deve possuir pelo menos uma letra maiúscula (A-Z).";
    if (!status.minuscula) return "A senha deve possuir pelo menos uma letra minúscula (a-z).";
    if (!status.numero) return "A senha deve possuir pelo menos um número (0-9).";
    if (!status.especial) return "A senha deve possuir pelo menos um caractere especial.";
    return "";
}

function vincularChecklistSenha({
    inputSenha,
    containerChecklist,
    inputConfirmacao = null,
    feedbackConfirmacao = null,
    erroConfirmacao = null
}) {
    if (!inputSenha || !containerChecklist) return;

    if (!containerChecklist.querySelector('[data-req="tamanho"]')) {
        containerChecklist.classList.add("password-checklist");
        containerChecklist.innerHTML = `
            <div class="password-checklist-header">
                <span>Requisitos de segurança da senha</span>
                <strong data-password-status>0/5 requisitos</strong>
            </div>
            <div class="password-strength-track" aria-hidden="true">
                <div class="password-strength-bar level-weak" style="width: 0%"></div>
            </div>
            <ul class="password-req-list">
                <li class="password-req" data-req="tamanho"><span class="password-req-dot" aria-hidden="true"></span><span>Mínimo de 8 caracteres</span></li>
                <li class="password-req" data-req="maiuscula"><span class="password-req-dot" aria-hidden="true"></span><span>Pelo menos uma letra maiúscula (A-Z)</span></li>
                <li class="password-req" data-req="minuscula"><span class="password-req-dot" aria-hidden="true"></span><span>Pelo menos uma letra minúscula (a-z)</span></li>
                <li class="password-req" data-req="numero"><span class="password-req-dot" aria-hidden="true"></span><span>Pelo menos um número (0-9)</span></li>
                <li class="password-req" data-req="especial"><span class="password-req-dot" aria-hidden="true"></span><span>Pelo menos um caractere especial (!@#$%^&*(),.?":{}|<>_-)</span></li>
            </ul>
        `;
    }

    const barra = containerChecklist.querySelector(".password-strength-bar");
    const rotuloStatus = containerChecklist.querySelector("[data-password-status]");
    const erroConfEl = erroConfirmacao || inputConfirmacao?.closest(".form-field, label")?.querySelector("small.field-error");

    const atualizarConfirmacao = () => {
        if (!inputConfirmacao) return;
        const s1 = inputSenha.value;
        const s2 = inputConfirmacao.value;
        if (!s2) {
            inputConfirmacao.classList.remove("input-valid", "input-invalid");
            inputConfirmacao.removeAttribute("aria-invalid");
            if (erroConfEl) {
                erroConfEl.textContent = "";
                erroConfEl.hidden = true;
            }
            if (feedbackConfirmacao) {
                feedbackConfirmacao.hidden = false;
                feedbackConfirmacao.textContent = "";
                feedbackConfirmacao.className = "field-help";
            }
            return;
        }
        if (s1 && s1 === s2) {
            inputConfirmacao.classList.add("input-valid");
            inputConfirmacao.classList.remove("input-invalid");
            inputConfirmacao.setAttribute("aria-invalid", "false");
            if (erroConfEl) {
                erroConfEl.textContent = "";
                erroConfEl.hidden = true;
            }
            if (feedbackConfirmacao) {
                feedbackConfirmacao.hidden = false;
                feedbackConfirmacao.textContent = "✓ As senhas conferem.";
                feedbackConfirmacao.className = "field-feedback is-valid";
            }
        } else {
            inputConfirmacao.classList.add("input-invalid");
            inputConfirmacao.classList.remove("input-valid");
            inputConfirmacao.setAttribute("aria-invalid", "true");
            if (erroConfEl) {
                erroConfEl.textContent = "As senhas digitadas não coincidem.";
                erroConfEl.hidden = false;
                if (feedbackConfirmacao) feedbackConfirmacao.hidden = true;
            } else if (feedbackConfirmacao) {
                feedbackConfirmacao.hidden = false;
                feedbackConfirmacao.textContent = "As senhas digitadas não coincidem.";
                feedbackConfirmacao.className = "field-feedback is-invalid";
            }
        }
    };

    const atualizar = () => {
        const res = avaliarForcaSenha(inputSenha.value);
        ["tamanho", "maiuscula", "minuscula", "numero", "especial"].forEach((chave) => {
            const item = containerChecklist.querySelector(`[data-req="${chave}"]`);
            if (!item) return;
            const cumprido = Boolean(res[chave]);
            item.classList.toggle("is-met", cumprido);
            const ponto = item.querySelector(".password-req-dot");
            if (ponto) {
                ponto.textContent = cumprido ? "✓" : "";
            }
        });

        if (barra) {
            const pct = (res.atendidos / 5) * 100;
            barra.style.width = `${pct}%`;
            barra.classList.remove("level-weak", "level-medium", "level-strong");
            if (res.atendidos === 5) {
                barra.classList.add("level-strong");
            } else if (res.atendidos >= 3) {
                barra.classList.add("level-medium");
            } else {
                barra.classList.add("level-weak");
            }
        }

        if (rotuloStatus) {
            if (!inputSenha.value) {
                rotuloStatus.textContent = "0/5 requisitos";
            } else if (res.valida) {
                rotuloStatus.textContent = "Senha forte aprovada (5/5)";
            } else {
                rotuloStatus.textContent = `${res.atendidos}/5 requisitos atendidos`;
            }
        }

        atualizarConfirmacao();
    };

    inputSenha.addEventListener("input", atualizar);
    if (inputConfirmacao) {
        inputConfirmacao.addEventListener("input", atualizarConfirmacao);
    }
    atualizar();
}

// Exportação explícita de todas as funções no escopo global (window)
if (typeof window !== "undefined") {
    window.MAPA_DOMINIOS_EMAIL_SUGERIDOS = MAPA_DOMINIOS_EMAIL_SUGERIDOS;
    window.formatarMascaraCpf = formatarMascaraCpf;
    window.validarCpfMatematico = validarCpfMatematico;
    window.vincularValidacaoCpfTempoReal = vincularValidacaoCpfTempoReal;
    window.formatarMascaraTelefone = formatarMascaraTelefone;
    window.validarTelefoneBrasileiro = validarTelefoneBrasileiro;
    window.vincularValidacaoTelefoneTempoReal = vincularValidacaoTelefoneTempoReal;
    window.mascararEmailCliente = mascararEmailCliente;
    window.mascararTelefoneCliente = mascararTelefoneCliente;
    window.detectarErroDominioEmail = detectarErroDominioEmail;
    window.validarEmailFormato = validarEmailFormato;
    window.vincularValidacaoEmailTempoReal = vincularValidacaoEmailTempoReal;
    window.avaliarForcaSenha = avaliarForcaSenha;
    window.obterMensagemErroSenha = obterMensagemErroSenha;
    window.vincularChecklistSenha = vincularChecklistSenha;
}
