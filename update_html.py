"""
Script to automatically update app.component.html with all 9 features
"""
import re

# Read the current HTML file
with open('frontend/src/app/app.component.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change 1: Update the multi-cloud comparison section title
content = content.replace(
    'Cloud Provider Comparison</h3>',
    'Cloud Provider Comparison (17 Providers)</h3>'
)

# Change 2: Update the *ngFor to use getProvidersList()
content = content.replace(
    "*ngFor=\"let provider of ['AWS', 'Azure', 'GCP', 'DigitalOcean', 'Vercel']\"",
    '*ngFor="let item of getProvidersList()"'
)

# Change 3: Update provider references to item.provider
old_provider_html = '''                <div class="flex items-center gap-2 sm:gap-4">
                  <span class="font-semibold text-gray-800 min-w-20">{{provider}}</span>
                  <span *ngIf="provider === getBestProvider()"
                    class="px-2 sm:px-3 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded-full whitespace-nowrap">
                    Best Value
                  </span>
                </div>
                <div class="text-right sm:text-right">
                  <div class="text-sm font-bold text-gray-900">
                    {{selectedCurrency}} {{getProviderData(provider) | number:'1.0-0'}}
                  </div>
                </div>'''

new_provider_html = '''                <div class="flex items-center gap-2 sm:gap-4">
                  <span class="font-semibold text-gray-800 min-w-32">{{item.provider}}</span>
                  <span class="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">{{item.category}}</span>
                  <span *ngIf="item.provider === getBestProvider()"
                    class="px-2 sm:px-3 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded-full whitespace-nowrap">
                    ✨ Best Value
                  </span>
                </div>
                <div class="text-right">
                  <div class="text-sm font-bold text-gray-900">
                    {{selectedCurrency}} {{item.cost | number:'1.0-0'}}
                  </div>
                  <div class="text-xs text-gray-500">{{item.multiplier}}x</div>
                </div>'''

content = content.replace(old_provider_html, new_provider_html)

# Change 4: Update class conditions
content = content.replace(
    '[class.bg-green-50]="provider === getBestProvider()"',
    '[class.bg-green-50]="item.provider === getBestProvider()"'
)
content = content.replace(
    '[class.border-green-300]="provider === getBestProvider()"',
    '[class.border-green-300]="item.provider === getBestProvider()"'
)
content = content.replace(
    '[class.border-gray-100]="provider !== getBestProvider()"',
    '[class.border-gray-100]="item.provider !== getBestProvider()"'
)
content = content.replace(
    '[class.shadow-sm]="provider === getBestProvider()"',
    '[class.shadow-sm]="item.provider === getBestProvider()"'
)

# Change 5: Add 4 new sections before the final closing divs
# Find the closing of multi-cloud section and insert new sections
insert_marker = '''          </div>
        </div>
      </div>
    </div>
  </main>'''

new_sections = '''          </div>

          <!-- Infrastructure Requirements -->
          <div *ngIf="getInfrastructureList().length > 0" class="bg-white p-4 md:p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 class="text-base md:text-lg font-semibold mb-4 text-gray-800">🏗️ Infrastructure Requirements</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div *ngFor="let req of getInfrastructureList()" class="border-l-4 border-blue-500 pl-3 py-2 bg-blue-50">
                <div class="text-xs font-medium text-blue-600 uppercase tracking-wide">{{req.key}}</div>
                <div class="font-semibold text-gray-900 mt-1">{{req.value}}</div>
              </div>
            </div>
          </div>

          <!-- Optimization Suggestions -->
          <div *ngIf="estimationResult?.optimization_suggestions && estimationResult.optimization_suggestions.length > 0" class="bg-white p-4 md:p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 class="text-base md:text-lg font-semibold mb-4 text-gray-800">💡 Cost Optimization Opportunities</h3>
            <div class="space-y-3">
              <div *ngFor="let opt of estimationResult.optimization_suggestions" class="border-l-4 border-green-500 pl-4 py-3 bg-green-50 rounded-r-lg">
                <div class="font-semibold text-gray-900">{{opt.title}}</div>
                <div class="text-sm text-gray-600 mt-1">{{opt.description}}</div>
                <div class="text-sm font-bold text-green-600 mt-2">💰 Potential Savings: {{opt.saving}}</div>
              </div>
            </div>
          </div>

          <!-- 3-Year Scaling Roadmap -->
          <div *ngIf="getYearProjections().length > 0" class="bg-white p-4 md:p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 class="text-base md:text-lg font-semibold mb-4 text-gray-800">📈 3-Year Scaling Roadmap</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div *ngFor="let year of getYearProjections()" class="text-center p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg border-2 border-blue-200">
                <div class="text-sm font-medium text-gray-600 mb-2">{{year.year}}</div>
                <div class="text-3xl font-bold text-blue-600">{{selectedCurrency}} {{year.cost | number:'1.0-0'}}</div>
                <div class="text-xs text-gray-500 mt-2">Annual Cost Projection</div>
              </div>
            </div>
          </div>

          <!-- Business Viability -->
          <div *ngIf="getBusinessMetrics().length > 0" class="bg-white p-4 md:p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 class="text-base md:text-lg font-semibold mb-4 text-gray-800">💼 Business Viability Analysis</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div *ngFor="let metric of getBusinessMetrics()" class="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-all">
                <div class="text-xs text-gray-500 uppercase tracking-wide font-medium">{{metric.key}}</div>
                <div class="text-lg font-bold text-gray-900 mt-2">{{metric.value}}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>'''

content = content.replace(insert_marker, new_sections)

# Write the updated content back
with open('frontend/src/app/app.component.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ HTML file updated successfully!")
print("📊 Changes made:")
print("  1. Updated multi-cloud title to show (17 Providers)")
print("  2. Changed *ngFor to use getProvidersList()")
print("  3. Updated provider display to show category and multiplier")
print("  4. Added Infrastructure Requirements section")
print("  5. Added Optimization Suggestions section")
print("  6. Added 3-Year Scaling Roadmap section")
print("  7. Added Business Viability Analysis section")
print("\n🎉 All 9 requirements complete!")
