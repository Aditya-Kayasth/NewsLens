"use client";
import React, { useState } from "react";
import { Sidebar, SidebarBody, SidebarLink } from "../components/ui/slidebar";
import {
  IconArrowLeft,
  IconBrandTabler,
  IconSettings,
  IconUserBolt,
} from "@tabler/icons-react";
import Link from "next/link";
import { motion } from "framer-motion";
import Image from "next/image";
import { cn } from "@/lib/utils";

export function SidebarDemo() {
  const links = [
    {
      label: "Dashboard",
      href: "#",
      icon: (
        <IconBrandTabler className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
    {
      label: "Profile",
      href: "#",
      icon: (
        <IconUserBolt className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
    {
      label: "Settings",
      href: "#",
      icon: (
        <IconSettings className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
    {
      label: "Logout",
      href: "#",
      icon: (
        <IconArrowLeft className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
  ];
  const [open, setOpen] = useState(false);
  return (
    <div className="flex w-full h-screen bg-transparent">
      <Sidebar open={open} setOpen={setOpen}>
        <SidebarBody className="justify-between gap-10 fixed">
          <div className="flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
            {open ? <Logo /> : <LogoIcon />}
            <div className="mt-8 flex flex-col gap-2">
              {links.map((link, idx) => (
                <SidebarLink key={idx} link={link} />
              ))}
            </div>
          </div>
          <div>
            <SidebarLink
              link={{
                label: "Samay Raina",
                href: "#",
                icon: (
                  <Image
                    src="https://assets.aceternity.com/manu.png"
                    className="h-7 w-7 flex-shrink-0 rounded-full"
                    width={50}
                    height={50}
                    alt="Avatar"
                  />
                ),
              }}
            />
          </div>
        </SidebarBody>
      </Sidebar>
      <BlogContent />
    </div>
  );
}

export const Logo = () => {
  return (
    <Link href="#" className="font-normal flex space-x-2 items-center text-sm text-black py-1 relative z-20">
      <div className="h-5 w-6 bg-black dark:bg-white rounded-br-lg rounded-tr-sm rounded-tl-lg rounded-bl-sm flex-shrink-0" />
      <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="font-medium text-black dark:text-white whitespace-pre">
        InsightPlus
      </motion.span>
    </Link>
  );
};

export const LogoIcon = () => {
  return (
    <Link href="#" className="font-normal flex space-x-2 items-center text-sm text-black py-1 relative z-20">
      <div className="h-5 w-6 bg-black dark:bg-white rounded-br-lg rounded-tr-sm rounded-tl-lg rounded-bl-sm flex-shrink-0" />
    </Link>
  );
};

const BlogContent = () => {
  return (
    <div className="flex flex-col flex-1 p-6 text-white ml-20">
      <button onClick={() => window.history.back()} className="mb-4 bg-gray-700 px-4 py-1 rounded-md shadow-lg transform transition duration-300 hover:scale-105 border border-gray-500 w-24 mx-auto">Back</button>
      <h1 className="text-4xl font-bold">Samay Raina joined Pakistan Got Latent?</h1>
      <p className="text-sm text-gray-400">Date: {new Date().toDateString()} | Time: {new Date().toLocaleTimeString()}</p>
      <div className="mt-4">
        <p className="text-lg leading-relaxed">
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Consequuntur ipsa omnis ratione tenetur nulla. Laborum, et itaque nisi ullam minima ab incidunt nobis ex nesciunt eos aliquam iure quam explicabo!
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Vel minus quo expedita sed fugit, quas amet quam ipsam id blanditiis fugiat dolor autem incidunt nesciunt, adipisci maiores delectus ipsum. Accusantium.
          Quos, aut officia pariatur fuga illum repudiandae animi quidem eveniet omnis cum maiores voluptates error reiciendis vel excepturi sapiente dolorem sed quis alias quaerat? Magnam laboriosam ad fugiat a quod.
          Sapiente aspernatur delectus nam soluta maxime, totam officia sequi repellendus voluptatem hic voluptatum debitis porro excepturi fugiat sint, cum a cupiditate molestias quaerat facilis ullam minus. Consectetur asperiores qui est!
          Natus quae esse autem porro, sapiente quasi nulla odio! Mollitia placeat repellendus tempore neque assumenda repudiandae illum excepturi perferendis, aliquid, sint expedita, impedit iste? Eos officia molestiae sapiente sunt ea.
          Omnis, corrupti, necessitatibus officia eos nostrum totam assumenda asperiores temporibus hic earum commodi incidunt corporis nisi voluptatem dolor optio culpa sequi quisquam dignissimos ad praesentium? Excepturi adipisci cum reprehenderit mollitia?
          Cupiditate inventore dolorum iusto quam accusamus in unde laboriosam velit rem. Maxime quasi, laudantium, aut culpa nihil, molestias beatae quaerat repellat natus repudiandae soluta ex magnam similique dolores quos aliquid!
        </p>
      </div>
      <div className="mt-6 flex gap-2 justify-end text-sm">
        <button className="bg-green-500 px-2 py-1 rounded-md shadow-lg transform transition duration-300 hover:scale-105 opacity-80 hover:opacity-100">👍</button>
        <button className="bg-red-500 px-2 py-1 rounded-md shadow-lg transform transition duration-300 hover:scale-105 opacity-80 hover:opacity-100">👎</button>
      </div>
      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-2">Comments</h2>
        <textarea className="w-full p-2 rounded-md bg-transparent text-white resize-none border border-gray-600" rows="4" placeholder="Write a comment..."></textarea>
        <button className="mt-2 bg-blue-600 px-4 py-2 rounded-md shadow-lg transform transition duration-300 hover:scale-105">Submit</button>
        <div className="mt-4">
          <p className="mb-2 text-gray-300"><strong>User1:</strong> This is a great blog!</p>
          <p className="text-gray-300"><strong>User2:</strong> Very informative, thanks for sharing.</p>
        </div>
      </div>
    </div>
  );
};

