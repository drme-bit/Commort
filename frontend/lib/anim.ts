import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

const EASE = "power2.out";

export function revealIn(el: HTMLElement, opts: { delay?: number; y?: number } = {}) {
  gsap.set(el, { autoAlpha: 0, y: opts.y ?? 16 });
  ScrollTrigger.create({
    trigger: el,
    start: "top 88%",
    once: true,
    onEnter: () =>
      gsap.to(el, { autoAlpha: 1, y: 0, duration: 0.7, ease: EASE, delay: opts.delay ?? 0 }),
  });
}

export function staggerIn(els: HTMLElement[], opts: { delay?: number } = {}) {
  gsap.set(els, { autoAlpha: 0, y: 20 });
  ScrollTrigger.batch(els, {
    start: "top 88%",
    once: true,
    onEnter: (batch) =>
      gsap.to(batch, {
        autoAlpha: 1,
        y: 0,
        duration: 0.5,
        ease: EASE,
        stagger: 0.05,
        delay: opts.delay ?? 0,
      }),
  });
}
