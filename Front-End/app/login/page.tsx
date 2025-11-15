'use client'

import { useState } from 'react'
import Image from 'next/image'
import { Eye, EyeOff } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Login submitted:', { email, password, rememberMe })
    // Redirect to dashboard after login
    router.push('/dashboard')
  }

  const handleGoogleLogin = () => {
    console.log('Google login clicked')
    router.push('/dashboard')
  }

  const handleAppleLogin = () => {
    console.log('Apple login clicked')
    router.push('/dashboard')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md">
        {/* Logo */}
        <div className="flex justify-center mb-8">
          <Image
            src="/images/design-mode/logo.PNG.png"
            alt="Advise AI Logo"
            width={64}
            height={64}
            priority
          />
        </div>

        {/* Title and Subtitle */}
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-2">Sign In</h1>
        <p className="text-center text-gray-600 text-sm mb-8">
          You can sign into your account using your email or username
        </p>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Email Input */}
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-2">
              Email or User Name
            </label>
            <input
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email or user name"
              className="w-full px-4 py-3 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Password Input */}
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-2">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>

          {/* Remember Me and Forgot Password */}
          <div className="flex items-center justify-between pt-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="w-4 h-4 rounded border-gray-300"
              />
              <span className="text-sm text-gray-700">Remember Me</span>
            </label>
            <a href="#" className="text-sm text-red-600 hover:text-red-700 font-medium">
              Forgot Password?
            </a>
          </div>

          {/* Sign In Button */}
          <button
            type="submit"
            className="w-full bg-blue-600 text-white font-semibold py-3 rounded-full hover:bg-blue-700 transition-colors mt-6"
          >
            Sign In
          </button>
        </form>

        {/* Sign Up Link */}
        <p className="text-center text-gray-600 text-sm mt-6">
          Don't have an account?{' '}
          <a href="/signup" className="text-blue-600 hover:text-blue-700 font-medium">
            Sign up
          </a>
        </p>

        {/* Divider */}
        <div className="flex items-center gap-3 my-6">
          <div className="flex-1 border-t border-gray-300"></div>
          <span className="text-gray-500 text-sm">Or</span>
          <div className="flex-1 border-t border-gray-300"></div>
        </div>

        {/* Social Login Buttons */}
        <div className="grid grid-cols-2 gap-4">
          <button 
            onClick={handleGoogleLogin}
            className="flex items-center justify-center gap-2 px-4 py-3 border border-gray-300 rounded-full hover:bg-gray-50 transition-colors"
          >
            <Image src="/google-logo.png" alt="Google" width={20} height={20} />
            <span className="text-sm font-medium text-gray-900">Google</span>
          </button>
          <button 
            onClick={handleAppleLogin}
            className="flex items-center justify-center gap-2 px-4 py-3 border border-gray-300 rounded-full hover:bg-gray-50 transition-colors"
          >
            <Image src="/apple-logo-minimalist.png" alt="Apple" width={20} height={20} />
            <span className="text-sm font-medium text-gray-900">Apple</span>
          </button>
        </div>
      </div>
    </div>
  )
}
