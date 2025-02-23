import Link from "next/link"

export default function MainNav() {
  return (
    <nav className="flex items-center gap-6 mt-4">
      <Link href="#" className="text-[#0EA6E9] border-b-2 border-[#0EA6E9] py-2">
        Home
      </Link>
    </nav>
  )
}
