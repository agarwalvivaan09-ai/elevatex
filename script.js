// LOAD NAVBAR
fetch("navbar.html")
  .then(res => res.text())
  .then(data => {
    document.getElementById("navbar").innerHTML = data;

    const toggle = document.getElementById("menuToggle");
    const menu = document.getElementById("mobileMenu");
    const overlay = document.getElementById("overlay");
    const closeBtn = document.getElementById("closeMenu");

    // OPEN
    toggle.addEventListener("click", () => {
      menu.classList.add("open");
      overlay.classList.add("active");
    });

    // CLOSE
    function closeMenu() {
      menu.classList.remove("open");
      overlay.classList.remove("active");
    }

    closeBtn.addEventListener("click", closeMenu);
    overlay.addEventListener("click", closeMenu);
  });
  document.addEventListener("DOMContentLoaded", () => {

  /* ===== METRICS ===== */
  const metrics = document.querySelectorAll('.metric');

  const animateCounter = (el) => {
    const target = +el.dataset.target;
    const duration = 1200;

    const step = (timestamp, startTime) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);

      el.innerText = Math.floor(progress * target);

      if (progress < 1) {
        requestAnimationFrame((t) => step(t, startTime));
      } else {
        el.innerText = target;
      }
    };

    requestAnimationFrame(step);
  };

  const metricObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");

        const counters = entry.target.querySelectorAll(".counter");
        counters.forEach(counter => animateCounter(counter));

        metricObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  metrics.forEach(metric => metricObserver.observe(metric));



const timeline = document.querySelector(".timeline");
const progress = document.querySelector(".timeline-progress");
const items = document.querySelectorAll(".timeline-item");

window.addEventListener("scroll", () => {
  const rect = timeline.getBoundingClientRect();
  const windowHeight = window.innerHeight;

  const totalHeight = timeline.offsetHeight;

  const start = windowHeight * 0.2;
const scrolled = Math.min(
  Math.max(windowHeight - rect.top - start, 0),
  totalHeight
);

  progress.style.height = scrolled + "px";

  items.forEach(item => {
    const itemRect = item.getBoundingClientRect();

    if (itemRect.top < windowHeight * 0.75) {
      item.classList.add("active");
      item.classList.add("show");
    }
  });
});
const blogCards = document.querySelectorAll(".blog-card");

const blogObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show");
    }
  });
}, { threshold: 0.2 });

blogCards.forEach(card => blogObserver.observe(card));

});
