/* =========================================================
   SHAKE FACTORY — cinematic scroll experience
   Real photographic layers, animated with GSAP + Lenis.
   ========================================================= */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  gsap.registerPlugin(ScrollTrigger);

  /* ---------------- Lenis smooth scroll ---------------- */
  var lenis = null;
  if (!reduceMotion && window.Lenis) {
    lenis = new Lenis({
      duration: 1.15,
      easing: function (t) { return 1 - Math.pow(1 - t, 3); },
      smoothWheel: true,
    });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
  }

  /* ---------------- Preloader ---------------- */
  var preloader = document.getElementById("preloader");
  var introStarted = false;
  function runPreloaderOut() {
    if (introStarted) return;
    introStarted = true;
    var bar = preloader.querySelector(".preloader__bar span");
    gsap.to(bar, {
      width: "100%",
      duration: 0.5,
      ease: "power2.out",
      onComplete: function () {
        gsap.to(preloader, {
          opacity: 0,
          duration: 0.5,
          ease: "power2.inOut",
          onComplete: function () {
            preloader.style.display = "none";
            playHeroIntro();
          },
        });
      },
    });
  }
  // The document may already be fully loaded by the time this script runs
  // (it's at the end of <body>), so 'load' can fire before we ever attach
  // a listener for it — check readyState directly instead of assuming.
  if (document.readyState === "complete") {
    runPreloaderOut();
  } else {
    window.addEventListener("load", runPreloaderOut);
  }
  // Safety net in case something (a slow font, a stalled request) blocks
  // 'load' entirely.
  setTimeout(runPreloaderOut, 1800);

  /* ---------------- Nav scroll state ---------------- */
  var nav = document.querySelector("[data-nav]");
  ScrollTrigger.create({
    start: 60,
    end: 99999,
    onUpdate: function (self) {
      nav.classList.toggle("is-scrolled", self.scroll() > 60);
    },
  });

  /* ---------------- Footer year ---------------- */
  var yearEl = document.querySelector("[data-year]");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* =========================================================
     HERO — opening cinematic sequence
     Real ingredient photographs fly in, converge, then reveal
     the real milkshake product photograph + title.
     ========================================================= */
  function playHeroIntro() {
    var stage = document.querySelector("[data-hero-stage]");
    if (!stage) return;

    var items = gsap.utils.toArray("[data-hero-item]");
    var shake = document.querySelector("[data-hero-shake]");
    var shadow = document.querySelector("[data-hero-shake-shadow]");
    var titleLines = gsap.utils.toArray(".hero__title-line");
    var eyebrow = document.querySelector("[data-hero-eyebrow]");
    var sub = document.querySelector("[data-hero-sub]");
    var scrollcue = document.querySelector("[data-hero-scrollcue]");

    if (reduceMotion) {
      gsap.set(items, { opacity: 1 });
      gsap.set(shake, { opacity: 1, scale: 1, y: 0 });
      gsap.set(shadow, { opacity: 1 });
      gsap.set([eyebrow, sub, scrollcue], { opacity: 1, y: 0 });
      return;
    }

    // randomize entry direction per item for a natural, non-mechanical feel
    items.forEach(function (el) {
      var fromX = gsap.utils.random(-160, 160);
      var fromY = gsap.utils.random(-120, -40);
      el.dataset.fromX = fromX;
      el.dataset.fromY = fromY;
    });

    gsap.set(items, {
      opacity: 0,
      scale: 0.4,
      rotate: function () { return gsap.utils.random(-45, 45); },
      x: function (i, el) { return parseFloat(el.dataset.fromX); },
      y: function (i, el) { return parseFloat(el.dataset.fromY); },
      filter: "blur(6px)",
    });
    gsap.set(shake, { opacity: 0, scale: 0.7, y: 50 });
    gsap.set(shadow, { opacity: 0, scaleX: 0.6 });
    gsap.set(eyebrow, { opacity: 0, y: 14 });
    gsap.set(titleLines, { yPercent: 130 });
    gsap.set(sub, { opacity: 0, y: 16 });
    gsap.set(scrollcue, { opacity: 0 });

    var tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    tl.to(items, {
      opacity: 1,
      scale: 1,
      rotate: 0,
      x: 0,
      y: 0,
      filter: "blur(0px)",
      duration: 1.1,
      stagger: { each: 0.09, from: "random" },
    }, 0.15)
      .to(items, {
        y: "-=18",
        duration: 1.6,
        ease: "sine.inOut",
        stagger: { each: 0.05, from: "random" },
      }, "-=0.4")
      .to(shadow, { opacity: 1, scaleX: 1, duration: 0.5 }, "-=1.2")
      .to(shake, { opacity: 1, scale: 1, y: 0, duration: 1, ease: "power3.out" }, "-=1.1")
      .to(items, { opacity: 0.16, scale: 0.85, filter: "blur(2px)", duration: 0.8 }, "-=0.7")
      .to(eyebrow, { opacity: 1, y: 0, duration: 0.6 }, "-=0.5")
      .to(titleLines, { yPercent: 0, duration: 0.9, stagger: 0.08, ease: "power4.out" }, "-=0.45")
      .to(sub, { opacity: 1, y: 0, duration: 0.7 }, "-=0.5")
      .to(scrollcue, { opacity: 1, duration: 0.6 }, "-=0.3");

    /* Scroll-out: as the user leaves the hero, push the whole stage
       away with parallax + blur so it reads like a camera pull-back. */
    gsap.timeline({
      scrollTrigger: {
        trigger: ".hero",
        start: "top top",
        end: "bottom top",
        scrub: 0.6,
      },
    })
      .to(shake, { scale: 1.25, y: -60, opacity: 0, filter: "blur(6px)", ease: "none" }, 0)
      .to(items, {
        y: function (i) { return -140 - i * 20; },
        opacity: 0,
        ease: "none",
      }, 0)
      .to(".hero__copy", { y: -80, opacity: 0, ease: "none" }, 0)
      .to(".hero__bg", { scale: 1.2, ease: "none" }, 0)
      .to(scrollcue, { opacity: 0, ease: "none" }, 0);
  }

  /* =========================================================
     INGREDIENTS — pinned parallax depth scene
     Real ingredient cutouts move at different speeds to fake depth.
     ========================================================= */
  var ingredientsPin = document.querySelector("[data-ingredients-pin]");
  if (ingredientsPin && !reduceMotion) {
    var layers = gsap.utils.toArray(".depth-layer");

    ScrollTrigger.create({
      trigger: ".ingredients",
      start: "top top",
      end: "bottom bottom",
      pin: ingredientsPin,
      pinSpacing: false,
    });

    var scene = gsap.timeline({
      scrollTrigger: {
        trigger: ".ingredients",
        start: "top top",
        end: "bottom bottom",
        scrub: 0.7,
      },
    });

    layers.forEach(function (layer) {
      var depth = parseFloat(layer.dataset.depth) || 0.5;
      var dir = layer.classList.contains("depth-layer--back") ? -1 : 1;
      scene.to(layer, {
        y: -300 * depth * dir,
        x: 60 * depth * (layer.classList.contains("depth-layer--front") ? -1 : 1),
        rotate: 6 * depth * dir,
        ease: "none",
      }, 0);
    });

    scene.fromTo(".ingredients__copy", { opacity: 0, y: 40 }, {
      opacity: 1, y: 0, ease: "none",
    }, 0.15)
      .to(".ingredients__copy", { opacity: 0, y: -40, ease: "none" }, 0.75);

    gsap.utils.toArray(".depth-img").forEach(function (img, i) {
      gsap.fromTo(img, { opacity: 0, scale: 0.7 }, {
        opacity: 1,
        scale: 1,
        duration: 1,
        ease: "power3.out",
        scrollTrigger: {
          trigger: ".ingredients",
          start: "top 70%",
          toggleActions: "play none none reverse",
        },
        delay: i * 0.04,
      });
    });
  } else if (ingredientsPin) {
    gsap.set(".depth-img, .ingredients__copy", { opacity: 1 });
  }

  /* =========================================================
     SIGNATURE — real milkshake photograph reveal
     ========================================================= */
  var sigImg = document.querySelector("[data-signature-img]");
  if (sigImg) {
    if (reduceMotion) {
      gsap.set(sigImg, { opacity: 1, scale: 1, rotateY: 0, y: 0 });
      gsap.set(".floater", { opacity: 1 });
    } else {
      gsap.timeline({
        scrollTrigger: {
          trigger: ".signature",
          start: "top 75%",
          toggleActions: "play none none reverse",
        },
      })
        .to(sigImg, {
          opacity: 1, scale: 1, rotateY: 0, y: 0,
          duration: 1.3, ease: "power3.out",
        })
        .to(".floater", {
          opacity: 1, duration: 0.8, stagger: 0.12, ease: "power2.out",
        }, "-=0.8");

      // idle float + subtle 3D drift, tied to scroll position
      gsap.to(sigImg, {
        rotateY: 6,
        y: -10,
        ease: "none",
        scrollTrigger: {
          trigger: ".signature",
          start: "top bottom",
          end: "bottom top",
          scrub: 1,
        },
      });
    }
  }

  /* =========================================================
     COLLECTION — product card hover parallax (real photographs
     shift opposite to the cursor, like studio product photography).
     ========================================================= */
  gsap.utils.toArray(".shake-card").forEach(function (card) {
    var img = card.querySelector("[data-tilt-img]");
    if (!img) return;

    gsap.fromTo(card, { opacity: 0, y: 60 }, {
      opacity: 1, y: 0, duration: 0.9, ease: "power3.out",
      scrollTrigger: { trigger: card, start: "top 88%", toggleActions: "play none none reverse" },
    });

    if (reduceMotion) return;

    var bounds;
    card.addEventListener("pointerenter", function () {
      bounds = card.getBoundingClientRect();
    });
    card.addEventListener("pointermove", function (e) {
      if (!bounds) bounds = card.getBoundingClientRect();
      var relX = (e.clientX - bounds.left) / bounds.width - 0.5;
      var relY = (e.clientY - bounds.top) / bounds.height - 0.5;
      gsap.to(img, {
        x: relX * -22,
        y: relY * -16,
        scale: 1.08,
        rotate: relX * -2,
        duration: 0.6,
        ease: "power2.out",
      });
      gsap.to(card, {
        rotateX: relY * -6,
        rotateY: relX * 6,
        duration: 0.6,
        ease: "power2.out",
        transformPerspective: 700,
      });
    });
    card.addEventListener("pointerleave", function () {
      gsap.to(img, { x: 0, y: 0, scale: 1, rotate: 0, duration: 0.8, ease: "power3.out" });
      gsap.to(card, { rotateX: 0, rotateY: 0, duration: 0.8, ease: "power3.out" });
    });
  });

  /* =========================================================
     CRAFT — ingredient portraits fade/rise into view
     ========================================================= */
  gsap.fromTo(".craft__item", { opacity: 0, y: 40 }, {
    opacity: 1, y: 0, duration: 0.8, stagger: 0.12, ease: "power3.out",
    scrollTrigger: { trigger: ".craft__grid", start: "top 85%", toggleActions: "play none none reverse" },
  });
  gsap.fromTo(".craft__inner > *:not(.craft__grid)", { opacity: 0, y: 30 }, {
    opacity: 1, y: 0, duration: 0.8, stagger: 0.1, ease: "power3.out",
    scrollTrigger: { trigger: ".craft", start: "top 70%", toggleActions: "play none none reverse" },
  });

  /* ---------------- Mobile nav (basic toggle) ---------------- */
  var burger = document.querySelector("[data-burger]");
  if (burger) {
    burger.addEventListener("click", function () {
      var links = document.querySelector(".site-nav__links");
      var open = nav.classList.toggle("nav-open");
      if (open) {
        links.style.cssText = "display:flex;flex-direction:column;position:fixed;top:64px;left:0;right:0;background:var(--paper);padding:1.5rem;gap:1.2rem;box-shadow:0 12px 24px rgba(0,0,0,.12)";
      } else {
        links.style.cssText = "";
      }
    });
  }
})();
