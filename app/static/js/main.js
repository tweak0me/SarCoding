const form = document.getElementById("contactForm");
const message = document.getElementById("formMessage");
const submit = form.querySelector("button");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "";
  message.className = "form-message";
  submit.disabled = true;
  submit.textContent = "Отправляем...";

  try {
    const response = await fetch("/api/contact", {
      method: "POST",
      body: new FormData(form)
    });
    const data = await response.json();

    if (!response.ok || !data.ok) {
      throw new Error(data.message || "Ошибка отправки");
    }

    message.textContent = data.message;
    message.className = "form-message success";
    form.reset();
  } catch (error) {
    message.textContent = error.message || "Что-то пошло не так.";
    message.className = "form-message error";
  } finally {
    submit.disabled = false;
    submit.textContent = "Отправить заявку →";
  }
});
