/**
 * Hero background — a real WebGL 3D field of coffee beans and pistachios
 * (procedurally-modelled, no external 3D assets) drifting behind the hero
 * copy/product shot. Purely atmospheric: transparent background, blurred
 * and dimmed so the burgundy hero gradient and foreground photos still
 * read as the main event.
 *
 * Loaded as a plain <script type="module">, independent of main.js's GSAP
 * timelines — if WebGL isn't available, or the visitor asked for reduced
 * motion, it degrades to nothing (or one static frame) and the hero looks
 * exactly like it did before this file existed.
 */
import * as THREE from "./vendor/three.module.min.js";

(function () {
  var hero = document.querySelector(".hero");
  var canvas = document.querySelector("[data-hero-3d]");
  if (!hero || !canvas) return;

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var isNarrow = window.matchMedia("(max-width: 760px)").matches;

  var renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, powerPreference: "low-power" });
  } catch (e) {
    return; // no WebGL — leave the hero as a plain CSS scene
  }
  if (!renderer.getContext()) return;

  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
  camera.position.set(0, 0, 15);

  scene.add(new THREE.AmbientLight(0x6b4a33, 0.7));
  var key = new THREE.DirectionalLight(0xffe9c7, 1.1);
  key.position.set(5, 6, 8);
  scene.add(key);
  var rim = new THREE.DirectionalLight(0xff8fae, 0.45);
  rim.position.set(-6, -3, -4);
  scene.add(rim);
  var glow = new THREE.PointLight(0xffb347, 1.5, 34, 2);
  scene.add(glow);

  /* one shared sphere geometry, reused (scaled per-mesh) for every bean
     body / pistachio shell / pistachio nut — keeps the object count light */
  var sphereGeo = new THREE.SphereGeometry(1, 20, 16);

  /* ---- procedural coffee bean: an ellipsoid + a pressed-in crease ---- */
  var beanBodyMat = new THREE.MeshPhysicalMaterial({
    color: 0x3b2113, roughness: 0.38, clearcoat: 0.7, clearcoatRoughness: 0.25,
  });
  var creaseGeo = new THREE.CapsuleGeometry(0.07, 1.1, 4, 8);
  var creaseMat = new THREE.MeshStandardMaterial({ color: 0x140a06, roughness: 0.65 });

  function makeBean() {
    var g = new THREE.Group();
    var body = new THREE.Mesh(sphereGeo, beanBodyMat);
    body.scale.set(1, 0.66, 0.46);
    g.add(body);
    [1, -1].forEach(function (side) {
      var crease = new THREE.Mesh(creaseGeo, creaseMat);
      crease.rotation.z = Math.PI / 2;
      crease.position.set(0, 0, side * 0.465);
      crease.scale.set(1, 1, 0.55);
      g.add(crease);
    });
    return g;
  }

  /* ---- procedural pistachio: a tan shell with the green nut visibly
     poking out of one open end, rather than a fully-enclosed sphere ---- */
  var shellMat = new THREE.MeshPhysicalMaterial({ color: 0xd9c69c, roughness: 0.55, clearcoat: 0.15 });
  var nutMat = new THREE.MeshStandardMaterial({ color: 0x9dc26a, roughness: 0.6, emissive: 0x2a3a12, emissiveIntensity: 0.25 });

  function makePistachio() {
    var g = new THREE.Group();
    var shell = new THREE.Mesh(sphereGeo, shellMat);
    shell.scale.set(0.95, 0.72, 0.6);
    shell.position.x = -0.08;
    g.add(shell);
    var nut = new THREE.Mesh(sphereGeo, nutMat);
    nut.scale.set(0.6, 0.42, 0.38);
    nut.position.set(0.62, 0.03, 0.06); // pokes out past the shell's open end
    g.add(nut);
    return g;
  }

  var group = new THREE.Group();
  scene.add(group);

  var rand = function (a, b) { return a + Math.random() * (b - a); };
  var items = [];
  var beanCount = isNarrow ? 7 : 14;
  var pistaCount = isNarrow ? 4 : 8;

  function scatter(mesh) {
    mesh.position.set(rand(-9, 9), rand(-5.5, 5.5), rand(-7, 2));
    mesh.rotation.set(rand(0, Math.PI * 2), rand(0, Math.PI * 2), rand(0, Math.PI * 2));
    group.add(mesh);
    items.push({ mesh: mesh, spin: rand(0.4, 1.3), bob: rand(0.3, 0.9), phase: rand(0, 10) });
  }
  for (var i = 0; i < beanCount; i++) {
    var bean = makeBean();
    bean.scale.setScalar(rand(0.7, 1.3));
    scatter(bean);
  }
  for (var j = 0; j < pistaCount; j++) {
    var p = makePistachio();
    p.scale.setScalar(rand(0.6, 1.1));
    scatter(p);
  }

  /* ---- sizing ---- */
  function resize() {
    var w = hero.clientWidth, h = hero.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  resize();
  window.addEventListener("resize", resize);

  /* ---- gentle pointer parallax (desktop only, real motion allowed) ---- */
  var pointer = { x: 0, y: 0 };
  if (!reduceMotion && !isNarrow) {
    hero.addEventListener("pointermove", function (e) {
      var r = hero.getBoundingClientRect();
      pointer.x = (e.clientX - r.left) / r.width - 0.5;
      pointer.y = (e.clientY - r.top) / r.height - 0.5;
    });
  }

  /* ---- pause rendering while the hero is off-screen ---- */
  var visible = true;
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
    }, { threshold: 0 }).observe(hero);
  }

  var t = 0;
  var running = true;

  function renderFrame() {
    for (var k = 0; k < items.length; k++) {
      var it = items[k];
      it.mesh.rotation.x += it.spin * 0.0022;
      it.mesh.rotation.y += it.spin * 0.0032;
      it.mesh.position.y += Math.sin(t + it.phase) * 0.0016 * it.bob;
    }
    group.rotation.y = Math.sin(t * 0.06) * 0.15 + pointer.x * 0.25;
    group.rotation.x = pointer.y * 0.12;
    glow.position.set(Math.sin(t * 0.4) * 6, Math.cos(t * 0.3) * 4, 4);
    renderer.render(scene, camera);
  }

  if (reduceMotion) {
    renderFrame(); // one static frame, no loop, no parallax
    running = false;
  } else {
    (function animate() {
      if (!running) return;
      requestAnimationFrame(animate);
      if (!visible) return;
      t += 0.016;
      renderFrame();
    })();
  }
})();
