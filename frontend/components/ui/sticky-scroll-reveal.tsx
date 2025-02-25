"use client";
import React, { useEffect, useRef, useState } from "react";
import { useMotionValueEvent, useScroll } from "framer-motion";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

export const StickyScroll = ({
  content,
  contentClassName,
}: {
  content: {
    title: string;
    description: string;
    content?: React.ReactNode | any;
  }[];
  contentClassName?: string;
}) => {
  const [activeCard, setActiveCard] = useState(0);
  const ref = useRef<any>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });
  const cardLength = content.length;

  useMotionValueEvent(scrollYProgress, "change", (latest) => {
    const cardsBreakpoints = content.map((_, index) => index / cardLength);
    const closestBreakpointIndex = cardsBreakpoints.reduce(
      (acc, breakpoint, index) => {
        const distance = Math.abs(latest - breakpoint);
        if (distance < Math.abs(latest - cardsBreakpoints[acc])) {
          return index;
        }
        return acc;
      },
      0
    );
    setActiveCard(closestBreakpointIndex);
  });

  useEffect(() => {
    if (typeof window !== "undefined" && typeof document !== "undefined") {
      const globalStyles = document.createElement("style");
      globalStyles.innerHTML = `
        .no-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .no-scrollbar {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
      `;
      document.head.appendChild(globalStyles);
    }
  }, []);

  return (
    <motion.div
      className="h-[30rem] overflow-y-auto no-scrollbar flex justify-center relative space-x-10 rounded-md p-10 w-full bg-transparent"
      ref={ref}
    >
      <div className="relative flex items-start px-4 w-full">
        <div className="max-w-2xl w-full">
          {content.map((item, index) => (
            <div key={item.title + index} className="my-20">
              <h2 className="text-2xl font-bold text-slate-100">
                {item.title}
              </h2>
              <p className="text-lg text-slate-300 max-w-sm mt-10">
                {item.description}
              </p>
            </div>
          ))}
          <div className="h-40" />
        </div>
      </div>
      <div
        className={cn(
          "hidden lg:block h-[20rem] w-[75rem] rounded-md sticky top-10 overflow-hidden",
          contentClassName
        )}
      >
        {content[activeCard]?.content ?? null}
      </div>
    </motion.div>
  );
};
