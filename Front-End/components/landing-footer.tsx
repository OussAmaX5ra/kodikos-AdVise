import Image from 'next/image'

export default function LandingFooter() {
  return (
    <footer className="bg-white border-t border-gray-200 py-12 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-5 gap-8 mb-12">
          {/* Brand */}
          <div className="col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <Image
                src="/images/design-mode/logo.PNG.png"
                alt="Advise AI"
                width={40}
                height={40}
                className="rounded-lg"
              />
              <span className="font-bold text-black">Advise AI</span>
            </div>
            <p className="text-gray-600 text-sm mb-4">Download the app by clicking the link below:</p>
            <div className="flex gap-2">
              <button className="bg-black text-white px-3 py-2 rounded-lg text-xs font-medium hover:bg-gray-900 transition flex items-center gap-2">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M6 3h12a3 3 0 013 3v12a3 3 0 01-3 3H6a3 3 0 01-3-3V6a3 3 0 013-3z" />
                </svg>
                App Store
              </button>
              <button className="bg-black text-white px-3 py-2 rounded-lg text-xs font-medium hover:bg-gray-900 transition flex items-center gap-2">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M6 3h12a3 3 0 013 3v12a3 3 0 01-3 3H6a3 3 0 01-3-3V6a3 3 0 013-3z" />
                </svg>
                Play Store
              </button>
            </div>
          </div>

          {/* Pages */}
          <div>
            <h4 className="font-bold text-black mb-4">Pages</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-600 hover:text-gray-900 text-sm">Home it work</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-900 text-sm">Pricing</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-900 text-sm">Blog</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-900 text-sm">Demo</a></li>
            </ul>
          </div>

          {/* Service */}
          <div>
            <h4 className="font-bold text-black mb-4">Service</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-600 hover:text-gray-900 text-sm">Shopify</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-900 text-sm">WordPress</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-900 text-sm">UI/UX Design</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-bold text-black mb-4">Contact</h4>
            <ul className="space-y-3">
              <li className="flex items-start gap-2">
                <span className="text-gray-600 text-sm">(406) 555-0120</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-gray-600 text-sm">mariacoding123@gmail.com</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-gray-600 text-sm">2972 Westheimer Rd. Santa Ana, Illinois 85486</span>
              </li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h4 className="font-bold text-black mb-4">Social media</h4>
            <div className="flex gap-4">
              <a href="#" className="text-gray-600 hover:text-gray-900">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                </svg>
              </a>
              <a href="#" className="text-gray-600 hover:text-gray-900">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2s9 5 20 5a9.5 9.5 0 00-9-5.5c4.75 2.25 7-7 7-7a10.6 10.6 0 01-3-10z" />
                </svg>
              </a>
              <a href="#" className="text-gray-600 hover:text-gray-900">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z" />
                </svg>
              </a>
              <a href="#" className="text-gray-600 hover:text-gray-900">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <rect width="20" height="20" x="2" y="2" rx="5" ry="5" />
                  <path d="M16.5 7.5v9M12 10.5v6M7.5 12v4.5" stroke="white" strokeWidth="2" fill="none" />
                </svg>
              </a>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-gray-200 pt-8">
          <p className="text-gray-600 text-sm text-center">© 2025 Advise AI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
