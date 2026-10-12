(() => {
  const menuButton = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav-links");
  if (menuButton && nav) {
    menuButton.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("open");
      menuButton.setAttribute("aria-expanded", String(isOpen));
    });
    nav.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {
      nav.classList.remove("open");
      menuButton.setAttribute("aria-expanded", "false");
    }));
  }

  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealItems.forEach(item => observer.observe(item));
  } else {
    revealItems.forEach(item => item.classList.add("is-visible"));
  }

  const form = document.getElementById("contact-form");
  const result = document.getElementById("form-result");
  if (form && result) {
    form.addEventListener("submit", async event => {
      event.preventDefault();
      const button = form.querySelector('button[type="submit"]');
      const label = button.querySelector("span");
      const oldLabel = label.textContent;
      result.textContent = "";
      result.classList.remove("error");
      button.disabled = true;
      label.textContent = "Отправляем…";
      try {
        const response = await fetch(form.action, {
          method: "POST",
          body: new FormData(form),
          headers: { "Accept": "application/json" }
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) throw new Error(payload.message || "Не удалось отправить заявку.");
        result.textContent = payload.message;
        form.reset();
      } catch (error) {
        result.textContent = error.message || "Ошибка соединения. Попробуйте ещё раз.";
        result.classList.add("error");
      } finally {
        button.disabled = false;
        label.textContent = oldLabel;
      }
    });
  }

  document.querySelectorAll('[data-product="StudCRM"]').forEach(link => {
    link.addEventListener("click", () => {
      const message = document.getElementById("message");
      if (message && !message.value) message.value = "Хочу узнать подробнее о StudCRM.";
    });
  });
})();
