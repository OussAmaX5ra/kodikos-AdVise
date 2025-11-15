import Image from 'next/image'
import Link from 'next/link'

export default function LandingNavbar() {
  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <Image
            src="/images/design-mode/logo.PNG.png"
            alt="Advise AI"
            width={40}
            height={40}
            className="rounded-lg"
          />
          <span className="font-bold text-xl text-black">Advise AI</span>
        </Link>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-8">
          <a href="#" className="text-gray-700 hover:text-gray-900 text-sm font-medium">Product</a>
          <a href="#" className="text-gray-700 hover:text-gray-900 text-sm font-medium">Pricing</a>
          <a href="#" className="text-gray-700 hover:text-gray-900 text-sm font-medium">Resources</a>
          <a href="#" className="text-gray-700 hover:text-gray-900 text-sm font-medium">Contact</a>
        </div>

        {/* Auth Buttons */}
        <div className="flex items-center gap-4">
          <Link href="/login" className="text-gray-700 hover:text-gray-900 text-sm font-medium">
            Login
          </Link>
          <Link href="/signup" className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-full text-sm font-medium transition">
            Sign Up
          </Link>
        </div>
      </div>
    </nav>
  )
}
