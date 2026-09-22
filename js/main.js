/* =========================================================
   SHAKE FACTORY — cinematic scroll experience
   Layered SVG illustrations, animated with GSAP + Lenis.
   ========================================================= */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  gsap.registerPlugin(ScrollTrigger);

  // Guard every timeline on the page against a stalled first paint (a lot
  // of SVG gradients/filters decoding at once can block the main thread
  // for a beat). Without this, a long stall makes GSAP's ticker see a huge
  // time delta on its next tick and jump active timelines straight to
  // wherever "real time" says they should be — fast-forwarding the whole
  // hero intro to its end instead of playing it. Clamping any gap over
  // 500ms down to a small step keeps animations correct regardless.
  gsap.ticker.lagSmoothing(500, 33);

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
     HERO — opening cinematic sequence, in two beats:
     1. strawberries tumble through frame
     2. they settle back and the title/copy reveal

     Initial hidden states are applied immediately (synchronously, before
     the preloader even starts fading) so there's never a frame where the
     title/eyebrow flash fully visible underneath the preloader before
     snapping to hidden — only playHeroIntro() (run after the preloader
     fades) is timing-dependent; the hidden states themselves aren't.
     ========================================================= */
  var heroEls = {
    tumbleItems: gsap.utils.toArray("[data-tumble-item]"),
    titleLines: gsap.utils.toArray(".hero__title-line-inner"),
    eyebrow: document.querySelector("[data-hero-eyebrow]"),
    sub: document.querySelector("[data-hero-sub]"),
    scrollcue: document.querySelector("[data-hero-scrollcue]"),
    canvas3d: document.querySelector("[data-hero-3d]"),
    video: document.querySelector("[data-hero-video]"),
    scrim: document.querySelector("[data-hero-scrim]"),
  };

  (function setHeroInitialStates() {
    if (!document.querySelector("[data-hero-stage]")) return;
    var h = heroEls;

    if (reduceMotion) {
      gsap.set(h.tumbleItems, { opacity: 0 });
      gsap.set([h.eyebrow, h.sub, h.scrollcue], { opacity: 1, y: 0 });
      if (h.scrim) gsap.set(h.scrim, { opacity: 1 });
      return;
    }

    // each strawberry tumbles in from a random point above the frame
    h.tumbleItems.forEach(function (el) {
      el.dataset.fromX = gsap.utils.random(-120, 120);
      el.dataset.fromY = gsap.utils.random(-220, -100);
      el.dataset.fromRot = gsap.utils.random(-160, 160);
    });

    gsap.set(h.tumbleItems, {
      opacity: 0,
      scale: 0.5,
      x: function (i, el) { return parseFloat(el.dataset.fromX); },
      y: function (i, el) { return parseFloat(el.dataset.fromY); },
      rotate: function (i, el) { return parseFloat(el.dataset.fromRot); },
      filter: "blur(5px)",
    });
    gsap.set(h.eyebrow, { opacity: 0, y: 14, letterSpacing: "0.4em" });
    gsap.set(h.titleLines, { yPercent: 130, scale: 1.09, filter: "blur(14px)" });
    gsap.set(h.sub, { opacity: 0, y: 16, filter: "blur(4px)" });
    gsap.set(h.scrollcue, { opacity: 0 });
    if (h.canvas3d) gsap.set(h.canvas3d, { opacity: 0 });
    if (h.scrim) gsap.set(h.scrim, { opacity: 0 });
  })();

  function playHeroIntro() {
    if (!document.querySelector("[data-hero-stage]")) return;
    if (reduceMotion) return;

    var tumbleItems = heroEls.tumbleItems;
    var titleLines = heroEls.titleLines;
    var eyebrow = heroEls.eyebrow;
    var sub = heroEls.sub;
    var scrollcue = heroEls.scrollcue;
    var canvas3d = heroEls.canvas3d;
    var video = heroEls.video;
    var scrim = heroEls.scrim;

    // The eyebrow/title/sub/3D-bean reveal — the "Shake Factory" landing
    // moment. Shared by both paths below so it always looks the same
    // regardless of what triggered it.
    function revealCopy() {
      var tl = gsap.timeline({ defaults: { ease: "power3.out" } });
      if (canvas3d) tl.to(canvas3d, { opacity: 0.75, duration: 1.6, ease: "power1.out" }, 0);
      if (scrim) tl.to(scrim, { opacity: 1, duration: 1, ease: "power2.out" }, 0.05);
      tl.to(eyebrow, { opacity: 1, y: 0, letterSpacing: "0.14em", duration: 0.8, ease: "power2.out" }, 0.1)
        // the title pulls into focus — blur clears, a slight overshoot
        // scale settles to rest, each word rising out of its mask in turn
        .to(titleLines, {
          yPercent: 0,
          scale: 1,
          filter: "blur(0px)",
          duration: 1.1,
          stagger: 0.1,
          ease: "power4.out",
        }, 0.15)
        .to(sub, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.8 }, 0.25)
        .to(scrollcue, { opacity: 1, duration: 0.6 }, 0.6);
    }

    // Fallback for when there's no video (or it can't play): the original
    // tumble-then-reveal sequence.
    function playTumbleFallback() {
      gsap.timeline({ defaults: { ease: "power3.out" } })
        .to(tumbleItems, {
          opacity: 1,
          scale: 1,
          x: 0,
          y: 0,
          rotate: function () { return gsap.utils.random(-20, 20); },
          filter: "blur(0px)",
          duration: 1,
          stagger: { each: 0.07, from: "random" },
        }, 0.1)
        .to(tumbleItems, {
          y: "+=26",
          rotate: "+=14",
          duration: 1.1,
          ease: "sine.inOut",
          stagger: { each: 0.04, from: "random" },
        }, "-=0.3")
        .to(tumbleItems, {
          opacity: 0.14,
          scale: 0.8,
          y: "+=20",
          filter: "blur(2px)",
          duration: 0.6,
          stagger: { each: 0.02, from: "center" },
        }, "-=0.55")
        .add(revealCopy, "-=0.55");
    }

    if (video) {
      // The video is the intro now — it plays once, real footage the site
      // owner supplied, and "Shake Factory" lands right as it ends. The
      // tumbling strawberries stay hidden in this path (video already
      // shows real fruit flying into frame, no need to repeat that beat).
      var revealed = false;
      function reveal() {
        if (revealed) return;
        revealed = true;
        revealCopy();
      }
      video.addEventListener("ended", reveal);
      // never leave the title stuck hidden if the video can't play for
      // some reason (autoplay blocked, slow network, decode error, ...)
      video.addEventListener("error", reveal);
      setTimeout(reveal, 11000);
      var playPromise = video.play();
      if (playPromise && playPromise.catch) playPromise.catch(reveal);
    } else {
      playTumbleFallback();
    }

    /* Scroll-out: as the user leaves the hero, push the copy away with
       parallax + blur so it reads like a camera pull-back. */
    gsap.timeline({
      scrollTrigger: {
        trigger: ".hero",
        start: "top top",
        end: "bottom top",
        scrub: 0.6,
      },
    })
      .to(".hero__copy", { y: -80, opacity: 0, ease: "none" }, 0)
      .to(".hero__bg", { scale: 1.2, ease: "none" }, 0)
      .to(scrollcue, { opacity: 0, ease: "none" }, 0);
    if (canvas3d) {
      gsap.to(canvas3d, {
        opacity: 0, y: -40, ease: "none",
        scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: 0.6 },
      });
    }
    if (video) {
      gsap.to(video, {
        opacity: 0, ease: "none",
        scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: 0.6 },
      });
    }
    if (scrim) {
      gsap.to(scrim, {
        opacity: 0, ease: "none",
        scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: 0.6 },
      });
    }
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
    var splash = card.querySelector("[data-card-splash]");
    if (!img) return;

    if (reduceMotion) {
      gsap.fromTo(card, { opacity: 0, y: 60 }, {
        opacity: 1, y: 0, duration: 0.9, ease: "power3.out",
        scrollTrigger: { trigger: card, start: "top 88%", toggleActions: "play none none reverse" },
      });
      return;
    }

    // the card tips up into place with real perspective depth — like it's
    // being set down rather than just fading in — and a milk-splash burst
    // hits right as it lands, then clears
    var splashRotate = gsap.utils.random(-18, 18);
    var entrance = gsap.timeline({
      scrollTrigger: { trigger: card, start: "top 88%", toggleActions: "play none none reverse" },
    });
    entrance.fromTo(card,
      { opacity: 0, y: 70, rotateX: -22, scale: 0.94 },
      {
        opacity: 1, y: 0, rotateX: 0, scale: 1, duration: 0.9, ease: "power3.out",
        transformPerspective: 900, transformOrigin: "50% 100%",
      },
      0
    );
    if (splash) {
      entrance
        .fromTo(splash,
          { opacity: 0, scale: 0.35, rotate: splashRotate },
          { opacity: 0.9, scale: 1.15, rotate: splashRotate, duration: 0.45, ease: "power2.out" },
          0.12
        )
        .to(splash, { opacity: 0, scale: 1.4, duration: 0.55, ease: "power1.in" }, 0.5);
    }

    var bounds;
    card.addEventListener("pointerenter", function () {
      bounds = card.getBoundingClientRect();
      // the lift needs to happen here too, not just on pointermove — GSAP
      // writes the whole transform inline, which silently overrides the
      // CSS :hover translateY the instant the mouse moves, so without this
      // the card would only ever tilt and never actually lift off the page
      gsap.to(card, { y: -8, duration: 0.5, ease: "power3.out" });
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
        y: -8,
        rotateX: relY * -6,
        rotateY: relX * 6,
        duration: 0.6,
        ease: "power2.out",
        transformPerspective: 700,
      });
    });
    card.addEventListener("pointerleave", function () {
      gsap.to(img, { x: 0, y: 0, scale: 1, rotate: 0, duration: 0.8, ease: "power3.out" });
      gsap.to(card, { y: 0, rotateX: 0, rotateY: 0, duration: 0.8, ease: "power3.out" });
    });
  });

  /* =========================================================
     SHOWCASE — real product photographs fade/rise into view
     ========================================================= */
  gsap.fromTo(".showcase__card", { opacity: 0, y: 50 }, {
    opacity: 1, y: 0, duration: 0.9, stagger: 0.14, ease: "power3.out",
    scrollTrigger: { trigger: ".showcase__grid", start: "top 85%", toggleActions: "play none none reverse" },
  });
  gsap.fromTo(".showcase__head > *", { opacity: 0, y: 24 }, {
    opacity: 1, y: 0, duration: 0.7, stagger: 0.1, ease: "power3.out",
    scrollTrigger: { trigger: ".showcase", start: "top 75%", toggleActions: "play none none reverse" },
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
