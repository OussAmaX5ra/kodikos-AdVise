export default function LandingSection1() {
  return (
    <section className="bg-white py-16 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <h1 className="text-5xl md:text-6xl font-bold text-black leading-tight">
              Take Control of Your Social Media Ads
            </h1>
            <p className="text-gray-600 text-lg">
              Scale your e-commerce brand smartly with clear insights, optimized campaigns all guide by your AI Advisor
            </p>
            
            <div className="flex gap-4">
              <button 
                onClick={() => window.location.href = '/dashboard'}
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-semibold transition cursor-pointer">
                Try For Free
              </button>
              <button className="bg-black hover:bg-gray-900 text-white px-8 py-3 rounded-full font-semibold transition">
                Watch Demo
              </button>
            </div>
            
            {/* Stats Image */}
            <div className="pt-8">
              <img
                src="/images/design-mode/oMrf0Q3.png"
                alt="Analytics Dashboard"
                className="rounded-lg shadow-md w-full max-w-md"
              />
            </div>
          </div>

          {/* Middle Image */}
          <div className="flex justify-center">
            <img
              src="/images/design-mode/5t1j2mC.png"
              alt="Social Media Ads Control"
              className="max-w-full h-auto"
              style={{ width: '350px', height: '200px', objectFit: 'contain' }}
            />
          </div>

          {/* Right Content */}
          <div className="space-y-6">
            {/* AI Assistant Image */}
            <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl p-6 flex justify-center items-center h-64">
              <img
                src="/images/design-mode/KT6zWGf.png"
                alt="AI Assistant"
                className="rounded-xl shadow-lg max-w-full h-auto"
              />
            </div>

            {/* AI Advisor Text */}
            <div className="space-y-3">
              <h3 className="text-2xl font-bold text-gray-900">AI Advisor</h3>
              <p className="text-gray-600 text-base leading-relaxed">
                Meet your AI Assistant that guides you to smarter decisions
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
