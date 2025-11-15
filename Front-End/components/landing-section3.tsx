export default function LandingSection3() {
  return (
    <section className="bg-blue-50 py-20 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-black mb-4">Simple, Transparent Pricing</h2>
          <p className="text-gray-600 text-lg">Choose the plan that fits your business needs</p>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {/* Starter Card */}
          <div className="bg-gray-900 text-white p-8 rounded-2xl">
            <h3 className="text-2xl font-bold mb-2">Starter</h3>
            <p className="text-gray-400 text-sm mb-8">Perfect for small businesses getting started</p>
            
            <div className="mb-8">
              <span className="text-5xl font-bold">8000DA</span>
              <span className="text-gray-400 ml-2">/month</span>
            </div>

            <ul className="space-y-4 mb-8">
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span>
                <span>Up to 3 Ad Accounts</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span>
                <span>Daily Optimization</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span>
                <span>Email Support</span>
              </li>
            </ul>

            <button className="w-full bg-gray-700 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold transition">
              Get Started
            </button>
          </div>

          {/* Professional Card (Featured) */}
          <div className="bg-blue-600 text-white p-8 rounded-2xl relative md:-translate-y-4">
            <div className="absolute top-0 right-4 bg-yellow-400 text-black px-4 py-1 rounded-full text-xs font-bold">
              MOST POPULAR
            </div>
            
            <h3 className="text-2xl font-bold mb-2 mt-4">Professional</h3>
            <p className="text-blue-200 text-sm mb-8">For growing businesses with multiple campaigns</p>
            
            <div className="mb-8">
              <span className="text-5xl font-bold">15000DA</span>
              <span className="text-blue-200 ml-2">/month</span>
            </div>

            <ul className="space-y-4 mb-8">
              <li className="flex items-center gap-3">
                <span className="text-green-300">✓</span>
                <span>Up to 10 Ad Accounts</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-300">✓</span>
                <span>Real-time Optimization</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-300">✓</span>
                <span>Priority Support</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-300">✓</span>
                <span>Advanced Analytics</span>
              </li>
            </ul>

            <button className="w-full bg-white text-blue-600 hover:bg-blue-50 py-3 rounded-lg font-semibold transition">
              Start Free Trial
            </button>
          </div>

          {/* Enterprise Card */}
          <div className="bg-gray-900 text-white p-8 rounded-2xl">
            <h3 className="text-2xl font-bold mb-2">Enterprise</h3>
            <p className="text-gray-400 text-sm mb-8">For large businesses with custom needs</p>
            
            <div className="mb-8">
              <span className="text-5xl font-bold">Custom</span>
            </div>

            <ul className="space-y-4 mb-8">
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span>
                <span>Unlimited Ad Accounts</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span>
                <span>Real-time Optimization</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span>
                <span>24/7 Dedicated Support</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span>
                <span>Custom Integrations</span>
              </li>
            </ul>

            <button className="w-full bg-gray-700 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold transition">
              Contact Sales
            </button>
          </div>
        </div>

        {/* Footer Text */}
        <div className="text-center space-y-2">
          <p className="text-gray-600">
            Need something different? <a href="#" className="text-blue-600 hover:underline font-medium">Contact our sales team</a> for custom solutions.
          </p>
          <p className="text-gray-600 text-sm">All plans come with a 14-day free trial. No credit card required.</p>
        </div>
      </div>
    </section>
  )
}
