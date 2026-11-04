/*
 * FLUXO DE CAIXA
 * Cadastro simplificado (Arquitetura Zero-CPF): Nome, E-mail, Telefone (DDD 11-99)
 * e Senha Forte, com Google OAuth 2.0 e verificação 2FA/OTP via E-mail ou SMS.
 */

function inicializarBotoesVerSenha(root = document) {
    const botoes = root.querySelectorAll("[data-toggle-password]");
    botoes.forEach((botao) => {
        botao.addEventListener("click", () => {
            const targetId = botao.getAttribute("data-toggle-password");
            const input = document.getElementById(targetId);
            if (!input) return;

            const mostrar = input.type === "password";
            input.type = mostrar ? "text" : "password";
            botao.classList.toggle("is-visible", mostrar);
            botao.setAttribute("aria-pressed", String(mostrar));
            botao.setAttribute(
                "aria-label",
                mostrar ? "Ocultar senha" : "Mostrar senha"
            );
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    inicializarBotoesVerSenha();

    if (api.getToken()) {
        window.location.replace("index.html");
        return;
    }

    if (typeof inicializarBotaoGoogleOAuth === "function") {
        inicializarBotaoGoogleOAuth({
            buttonSelector: "#google-oauth-btn",
            gsiContainerSelector: "#google-gsi-button",
            messageSelector: "#register-message"
        });
    }

    const form = document.querySelector("#register-form");
    if (!form) return;

    const nameInput = document.querySelector("#register-name");
    const emailInput = document.querySelector("#register-email");
    const emailError = document.querySelector("#email-error");
    const phoneInput = document.querySelector("#register-phone");
    const phoneError = document.querySelector("#phone-error");
    const phoneOptionalTag = document.querySelector("#register-phone-optional");
    const channelRadios = document.querySelectorAll('input[name="canal_verificacao"]');
    const submitLabel = document.querySelector("#register-submit-label");
    const passwordInput = document.querySelector("#register-password");
    const passwordChecklist = document.querySelector("#register-password-checklist");
    const confirmationInput = document.querySelector("#register-password-confirm");
    const confirmFeedback = document.querySelector("#password-confirm-feedback");
    const passwordConfirmError = document.querySelector("#password-confirm-error");
    const acceptTermsCheckbox = document.querySelector("#accept-terms");
    const acceptPrivacyCheckbox = document.querySelector("#accept-privacy");
    const message = document.querySelector("#register-message");
    const submitButton = form.querySelector('[type="submit"]');

    // Modal Multi-Canal de Verificação OTP (6 dígitos)
    const verifyDialog = document.querySelector("#verify-email-dialog");
    const verifyForm = document.querySelector("#verify-email-form");
    const verifyTitle = document.querySelector("#verify-email-title");
    const verifyEmailDisplay = document.querySelector("#verify-email-display");
    const verifyContingencyBanner = document.querySelector("#verify-contingency-banner");
    const verifyContingencyCode = document.querySelector("#verify-contingency-code");
    const verifyFillContingencyBtn = document.querySelector("#verify-fill-contingency-btn");
    const verifyOtpInput = document.querySelector("#verify-otp-input");
    const verifyInlinePhoneBox = document.querySelector("#verify-inline-phone-box");
    const verifyInlinePhoneInput = document.querySelector("#verify-inline-phone");
    const verifyInlinePhoneError = document.querySelector("#verify-inline-phone-error");
    const verifyInlinePhoneSend = document.querySelector("#verify-inline-phone-send");
    const verifyMessage = document.querySelector("#verify-email-message");
    const verifySubmitBtn = document.querySelector("#verify-email-submit");
    const resendBtn = document.querySelector("#resend-verification-btn");
    const switchChannelBtn = document.querySelector("#switch-verification-channel-btn");
    const verifyCloseBtn = document.querySelector("#verify-email-close");

    let emailPendenteVerificacao = "";
    let telefonePendenteVerificacao = "";
    let canalAtualVerificacao = "email";
    let timerReenvioId = null;
    let segundosRestantesReenvio = 0;

    function obterCanalSelecionadoFormulario() {
        const selecionado = document.querySelector('input[name="canal_verificacao"]:checked');
        return selecionado ? selecionado.value : "email";
    }

    function ehCanalTelefone(canal) {
        return canal === "telefone" || canal === "sms" || canal === "whatsapp";
    }

    let controleTelefone = null;
    if (typeof vincularValidacaoTelefoneTempoReal === "function") {
        controleTelefone = vincularValidacaoTelefoneTempoReal(
            phoneInput,
            phoneError,
            () => true
        );
        if (verifyInlinePhoneInput) {
            vincularValidacaoTelefoneTempoReal(
                verifyInlinePhoneInput,
                verifyInlinePhoneError,
                () => true
            );
        }
    }

    function atualizarInterfaceSeletorCanal() {
        const canal = obterCanalSelecionadoFormulario();
        const porTelefone = ehCanalTelefone(canal);

        channelRadios.forEach((radio) => {
            const card = radio.closest(".channel-option-card");
            if (card) {
                card.classList.toggle("is-selected", radio.checked);
            }
        });

        if (phoneOptionalTag) {
            phoneOptionalTag.textContent = porTelefone
                ? "(receberá o SMS)"
                : "(com DDD)";
            phoneOptionalTag.classList.toggle("is-required", porTelefone);
        }
        if (submitLabel) {
            submitLabel.textContent = porTelefone
                ? "Criar conta e enviar SMS"
                : "Criar conta e enviar código por E-mail";
        }
        if (controleTelefone) {
            controleTelefone.revalidar(false);
        }
    }

    channelRadios.forEach((radio) => {
        radio.addEventListener("change", atualizarInterfaceSeletorCanal);
    });
    atualizarInterfaceSeletorCanal();

    if (typeof vincularValidacaoEmailTempoReal === "function") {
        vincularValidacaoEmailTempoReal(emailInput, emailError);
    }

    if (typeof vincularChecklistSenha === "function") {
        vincularChecklistSenha({
            inputSenha: passwordInput,
            containerChecklist: passwordChecklist,
            inputConfirmacao: confirmationInput,
            feedbackConfirmacao: confirmFeedback,
            erroConfirmacao: passwordConfirmError
        });
    }

    if (verifyOtpInput) {
        verifyOtpInput.addEventListener("input", () => {
            verifyOtpInput.value = verifyOtpInput.value.replace(/\D/g, "").slice(0, 6);
        });
    }

    function iniciarContadorReenvio(segundos = 60) {
        if (timerReenvioId) {
            clearInterval(timerReenvioId);
            timerReenvioId = null;
        }
        segundosRestantesReenvio = segundos;

        const atualizarBotao = () => {
            if (!resendBtn) return;
            if (segundosRestantesReenvio > 0) {
                resendBtn.disabled = true;
                resendBtn.textContent = `Reenviar (${segundosRestantesReenvio}s)`;
            } else {
                resendBtn.disabled = false;
                resendBtn.textContent = "Reenviar código";
                if (timerReenvioId) {
                    clearInterval(timerReenvioId);
                    timerReenvioId = null;
                }
            }
        };

        atualizarBotao();
        timerReenvioId = setInterval(() => {
            segundosRestantesReenvio -= 1;
            atualizarBotao();
        }, 1000);
    }

    function atualizarEstadoVisualModalOtp({
        canal = "email",
        destinoMascarado = "",
        modoContingencia = false,
        codigoDemonstracao = ""
    }) {
        canalAtualVerificacao = ehCanalTelefone(canal) ? "telefone" : "email";
        const porTel = canalAtualVerificacao === "telefone";

        if (verifyTitle) {
            verifyTitle.textContent = porTel
                ? "Valide o código enviado por SMS"
                : "Valide o código enviado por E-mail";
        }

        const destinoExibido =
            destinoMascarado ||
            (porTel
                ? typeof mascararTelefoneCliente === "function"
                    ? mascararTelefoneCliente(telefonePendenteVerificacao)
                    : telefonePendenteVerificacao
                : typeof mascararEmailCliente === "function"
                ? mascararEmailCliente(emailPendenteVerificacao)
                : emailPendenteVerificacao);

        if (verifyEmailDisplay) {
            verifyEmailDisplay.textContent = destinoExibido;
        }

        if (switchChannelBtn) {
            switchChannelBtn.textContent = porTel
                ? "Prefere E-mail? Enviar token para minha caixa de entrada"
                : "Prefere SMS? Enviar token para o meu Telefone";
        }

        if (verifyContingencyBanner && verifyContingencyCode) {
            if (modoContingencia && codigoDemonstracao) {
                verifyContingencyCode.textContent = codigoDemonstracao;
                verifyContingencyBanner.hidden = false;
            } else {
                verifyContingencyCode.textContent = "";
                verifyContingencyBanner.hidden = true;
            }
        }
    }

    verifyFillContingencyBtn?.addEventListener("click", () => {
        if (verifyOtpInput && verifyContingencyCode?.textContent) {
            verifyOtpInput.value = verifyContingencyCode.textContent.trim();
            verifyOtpInput.focus();
        }
    });

    function abrirModalVerificacaoOtp(respostaCadastro, emailCadastrado, telefoneCadastrado, canalEscolhido) {
        emailPendenteVerificacao = emailCadastrado;
        telefonePendenteVerificacao = telefoneCadastrado || "";

        if (!verifyDialog) {
            window.location.assign("login.html?cadastro=sucesso");
            return;
        }

        if (verifyOtpInput) verifyOtpInput.value = "";
        if (verifyInlinePhoneBox) verifyInlinePhoneBox.hidden = true;

        atualizarEstadoVisualModalOtp({
            canal: respostaCadastro?.canal_verificacao || canalEscolhido || "email",
            destinoMascarado: respostaCadastro?.destino_mascarado || "",
            modoContingencia: Boolean(respostaCadastro?.modo_contingencia),
            codigoDemonstracao: respostaCadastro?.codigo_demonstracao || ""
        });

        if (verifyMessage) {
            verifyMessage.textContent =
                canalAtualVerificacao === "telefone"
                    ? "Conta criada! Digite o token de 6 dígitos enviado por SMS."
                    : "Conta criada! Digite o token de 6 dígitos enviado para o seu e-mail.";
            verifyMessage.className = "form-message info";
        }

        iniciarContadorReenvio(60);

        if (typeof verifyDialog.showModal === "function") {
            verifyDialog.showModal();
        } else {
            verifyDialog.setAttribute("open", "open");
        }
        verifyOtpInput?.focus();
    }

    verifyCloseBtn?.addEventListener("click", () => {
        if (timerReenvioId) {
            clearInterval(timerReenvioId);
            timerReenvioId = null;
        }
        if (verifyDialog && typeof verifyDialog.close === "function") {
            verifyDialog.close();
        }
        window.location.assign("login.html?cadastro=sucesso");
    });

    async function dispararReenvioOuTrocaCanal(novoCanal, telefoneInformado = "") {
        if (!emailPendenteVerificacao || !verifyMessage) return;

        const payload = {
            email: emailPendenteVerificacao,
            canal_verificacao: novoCanal
        };
        if (telefoneInformado) {
            payload.telefone = telefoneInformado;
        }

        if (resendBtn) resendBtn.disabled = true;
        if (switchChannelBtn) switchChannelBtn.disabled = true;
        verifyMessage.textContent =
            novoCanal === "telefone"
                ? "Enviando novo token de 6 dígitos por SMS..."
                : "Enviando novo token de 6 dígitos por E-mail...";
        verifyMessage.className = "form-message info";

        try {
            const resp = await api.post("/usuarios/enviar-codigo", payload);
            if (telefoneInformado) {
                telefonePendenteVerificacao = telefoneInformado;
            }
            if (verifyInlinePhoneBox) verifyInlinePhoneBox.hidden = true;

            atualizarEstadoVisualModalOtp({
                canal: resp?.canal_utilizado || novoCanal,
                destinoMascarado: resp?.destino_mascarado || "",
                modoContingencia: Boolean(resp?.modo_contingencia),
                codigoDemonstracao: resp?.codigo_demonstracao || ""
            });

            verifyMessage.textContent =
                resp?.mensagem || "Novo código enviado com sucesso!";
            verifyMessage.className = "form-message info";
            iniciarContadorReenvio(60);
            verifyOtpInput?.focus();
        } catch (erro) {
            verifyMessage.textContent = erro.message;
            verifyMessage.className = "form-message error";
            if (segundosRestantesReenvio <= 0 && resendBtn) {
                resendBtn.disabled = false;
            }
        } finally {
            if (switchChannelBtn) switchChannelBtn.disabled = false;
        }
    }

    resendBtn?.addEventListener("click", async () => {
        if (segundosRestantesReenvio > 0) return;
        await dispararReenvioOuTrocaCanal(canalAtualVerificacao);
    });

    switchChannelBtn?.addEventListener("click", async () => {
        const proximoCanal = canalAtualVerificacao === "email" ? "telefone" : "email";
        if (proximoCanal === "telefone" && !telefonePendenteVerificacao) {
            if (verifyInlinePhoneBox) {
                verifyInlinePhoneBox.hidden = false;
                verifyInlinePhoneInput?.focus();
            }
            if (verifyMessage) {
                verifyMessage.textContent =
                    "Informe seu celular com DDD acima para receber o código por SMS.";
                verifyMessage.className = "form-message info";
            }
            return;
        }
        await dispararReenvioOuTrocaCanal(proximoCanal, telefonePendenteVerificacao);
    });

    verifyInlinePhoneSend?.addEventListener("click", async () => {
        if (!verifyInlinePhoneInput) return;
        const telDigitado = verifyInlinePhoneInput.value.trim();
        const validacaoTel =
            typeof validarTelefoneBrasileiro === "function"
                ? validarTelefoneBrasileiro(telDigitado, { obrigatorio: true })
                : { valido: telDigitado.replace(/\D/g, "").length >= 10, mensagem: "Telefone inválido." };

        if (!validacaoTel.valido) {
            verifyInlinePhoneInput.classList.add("input-invalid");
            if (verifyInlinePhoneError) {
                verifyInlinePhoneError.textContent = validacaoTel.mensagem;
                verifyInlinePhoneError.hidden = false;
            }
            verifyInlinePhoneInput.focus();
            return;
        }
        await dispararReenvioOuTrocaCanal("telefone", telDigitado);
    });

    verifyForm?.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!verifyOtpInput || !verifyMessage) return;

        const codigo = verifyOtpInput.value.trim();
        if (!/^\d{6}$/.test(codigo)) {
            verifyMessage.textContent = "Digite os 6 dígitos numéricos do token recebido.";
            verifyMessage.className = "form-message error";
            verifyOtpInput.focus();
            return;
        }

        if (verifySubmitBtn) {
            verifySubmitBtn.disabled = true;
            verifySubmitBtn.classList.add("is-loading");
        }
        verifyMessage.textContent = "Validando código e preparando seu painel...";
        verifyMessage.className = "form-message info";

        try {
            const dados = await api.post("/usuarios/verificar-email", {
                email: emailPendenteVerificacao,
                codigo_otp: codigo
            });

            if (timerReenvioId) {
                clearInterval(timerReenvioId);
                timerReenvioId = null;
            }

            if (dados && typeof dados.access_token === "string" && dados.access_token) {
                api.setToken(dados.access_token);
                window.location.assign("index.html");
                return;
            }

            window.location.assign("login.html?verificado=sucesso");
        } catch (erro) {
            verifyMessage.textContent = erro.message;
            verifyMessage.className = "form-message error";
        } finally {
            if (verifySubmitBtn) {
                verifySubmitBtn.disabled = false;
                verifySubmitBtn.classList.remove("is-loading");
            }
        }
    });

    if (
        !nameInput ||
        !emailInput ||
        !phoneInput ||
        !passwordInput ||
        !confirmationInput ||
        !message
    ) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        message.textContent = "";
        message.className = "form-message";

        const nome = nameInput.value.trim();
        if (nome.length < 3) {
            message.textContent = "Informe seu nome completo (mínimo de 3 caracteres).";
            message.classList.add("error");
            nameInput.focus();
            return;
        }

        // 1. Validação estrita de formato e domínio de e-mail
        const email = emailInput.value.trim();
        const erroDominio =
            typeof detectarErroDominioEmail === "function"
                ? detectarErroDominioEmail(email)
                : null;
        const emailValido = typeof validarEmailFormato === "function"
            ? validarEmailFormato(email)
            : Boolean(email && emailInput.checkValidity());

        if (!emailValido || erroDominio) {
            const msgEmail = erroDominio
                ? erroDominio.mensagem
                : "Informe um endereço de e-mail válido (ex.: voce@dominio.com).";
            emailInput.classList.add("input-invalid");
            emailInput.classList.remove("input-valid");
            emailInput.setAttribute("aria-invalid", "true");
            if (emailError && !erroDominio) {
                emailError.textContent = msgEmail;
                emailError.hidden = false;
            }
            message.textContent = msgEmail;
            message.classList.add("error");
            emailInput.focus();
            return;
        }

        // 2. Validação do telefone com DDD (11 a 99)
        const canalEscolhido = obterCanalSelecionadoFormulario();
        const telObrigatorio = true;
        const telefoneTexto = phoneInput.value.trim();

        const validacaoTel =
            typeof validarTelefoneBrasileiro === "function"
                ? validarTelefoneBrasileiro(telefoneTexto, { obrigatorio: telObrigatorio })
                : {
                      valido: telefoneTexto.replace(/\D/g, "").length >= 10,
                      mensagem: "Informe um telefone válido com DDD."
                  };

        if (!validacaoTel.valido) {
            const msgTel =
                validacaoTel.mensagem ||
                "Informe seu telefone válido com DDD (11 a 99).";
            phoneInput.classList.add("input-invalid");
            phoneInput.classList.remove("input-valid");
            phoneInput.setAttribute("aria-invalid", "true");
            if (phoneError) {
                phoneError.textContent = msgTel;
                phoneError.hidden = false;
            }
            message.textContent = msgTel;
            message.classList.add("error");
            phoneInput.focus();
            return;
        }

        // 3. Validação dos 5 requisitos de senha forte
        if (typeof obterMensagemErroSenha === "function") {
            const erroSenha = obterMensagemErroSenha(passwordInput.value);
            if (erroSenha) {
                message.textContent = erroSenha;
                message.classList.add("error");
                passwordInput.focus();
                return;
            }
        }

        if (passwordInput.value !== confirmationInput.value) {
            const msgConfirmacao = "As senhas digitadas não coincidem.";
            confirmationInput.classList.add("input-invalid");
            confirmationInput.classList.remove("input-valid");
            confirmationInput.setAttribute("aria-invalid", "true");
            if (passwordConfirmError) {
                passwordConfirmError.textContent = msgConfirmacao;
                passwordConfirmError.hidden = false;
            }
            message.textContent = msgConfirmacao;
            message.classList.add("error");
            confirmationInput.focus();
            return;
        }

        // 4. Consentimento transparente LGPD
        const aceitouTermos = Boolean(acceptTermsCheckbox?.checked);
        const aceitouPrivacidade = Boolean(acceptPrivacyCheckbox?.checked);
        if (!aceitouTermos || !aceitouPrivacidade) {
            message.textContent =
                "Confirme a leitura dos Termos de Uso e da Política de Privacidade (LGPD) para continuar.";
            message.classList.add("error");
            (!aceitouTermos ? acceptTermsCheckbox : acceptPrivacyCheckbox)?.focus();
            return;
        }

        const porSms = ehCanalTelefone(canalEscolhido);

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.classList.add("is-loading");
        }
        message.textContent = porSms
            ? "Criando sua conta e enviando token de 6 dígitos por SMS..."
            : "Criando sua conta e enviando token de 6 dígitos por E-mail...";
        message.classList.add("info");

        try {
            const respostaCadastro = await api.post("/usuarios/", {
                nome_completo: nome,
                email,
                telefone: telefoneTexto,
                senha: passwordInput.value,
                canal_verificacao: canalEscolhido,
                aceite_termos: true,
                aceite_privacidade: true
            });

            message.textContent = porSms
                ? "Conta criada! Digite o código de 6 dígitos enviado por SMS."
                : "Conta criada! Digite o código de 6 dígitos enviado para o seu e-mail.";
            message.className = "form-message info";
            abrirModalVerificacaoOtp(
                respostaCadastro,
                email,
                telefoneTexto,
                canalEscolhido
            );
        } catch (error) {
            const msgErro = error?.message || "Não foi possível concluir o cadastro.";
            const msgLower = msgErro.toLowerCase();
            if (msgLower.includes("telefone") || msgLower.includes("ddd") || msgLower.includes("sms")) {
                phoneInput.classList.add("input-invalid");
                phoneInput.classList.remove("input-valid");
                if (phoneError) {
                    phoneError.textContent = msgErro;
                    phoneError.hidden = false;
                }
            } else if (msgLower.includes("e-mail") || msgLower.includes("email") || msgLower.includes("domínio")) {
                emailInput.classList.add("input-invalid");
                emailInput.classList.remove("input-valid");
                if (emailError) {
                    emailError.textContent = msgErro;
                    emailError.hidden = false;
                }
            }
            message.textContent = msgErro;
            message.className = "form-message error";
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.classList.remove("is-loading");
            }
        }
    });
});
