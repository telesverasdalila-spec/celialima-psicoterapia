"use client";

/**
 * Wrappers client para animações da home.
 *
 * Em Next.js 16 (App Router + Turbopack), não é possível usar `<motion.div>`
 * diretamente dentro de um Server Component — o runtime queixa-se:
 *   "Attempted to call createMotionComponent() from the server..."
 *
 * A solução canônica é encapsular o uso de motion em componentes client
 * individuais. Estes wrappers cobrem os 3 padrões que a home usa:
 *
 *   1. <HeroStagger>  — container do hero com fade-in escalonado dos filhos
 *   2. <HeroItem>     — item individual do stagger (kicker, título, etc.)
 *   3. <FadeIn>       — fade-up genérico disparado no scroll (whileInView)
 *
 * Todos respeitam `prefers-reduced-motion` automaticamente (framer-motion).
 */

import { motion } from "framer-motion";
import type { CSSProperties, ReactNode } from "react";

const EASE = [0.22, 1, 0.36, 1] as const;

const staggerParent = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.12, delayChildren: 0.15 },
  },
};

const staggerChild = {
  hidden: { opacity: 0, y: 18 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.65, ease: EASE },
  },
};

const fadeUpVariant = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: EASE },
  },
};

export function HeroStagger({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <motion.div
      className={className}
      initial="hidden"
      animate="visible"
      variants={staggerParent}
    >
      {children}
    </motion.div>
  );
}

export function HeroItem({
  children,
  className,
  style,
}: {
  children: ReactNode;
  className?: string;
  style?: CSSProperties;
}) {
  return (
    <motion.div
      className={className}
      style={style}
      variants={staggerChild}
    >
      {children}
    </motion.div>
  );
}

export function FadeIn({
  children,
  className,
  style,
  delay = 0,
}: {
  children: ReactNode;
  className?: string;
  style?: CSSProperties;
  delay?: number;
}) {
  return (
    <motion.div
      className={className}
      style={style}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-100px" }}
      transition={{ delay }}
      variants={fadeUpVariant}
    >
      {children}
    </motion.div>
  );
}
