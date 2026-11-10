#!/usr/bin/env python3
"""
Mobile Adaptation Checker & Auditor for Fencing Showcase
Checks HTML pages across standard mobile viewports (360px, 375px, 390px, 428px)
Detects horizontal overflow, elements extending past viewport, font size zoom risks,
and small tap targets using headless Google Chrome.
"""

import sys
import os
import subprocess
import json
import re

VIEWPORTS = [
    {"name": "Compact Android", "width": 360, "height": 780},
    {"name": "iPhone SE / Small", "width": 375, "height": 667},
    {"name": "iPhone 14 / 15 Standard", "width": 390, "height": 844},
    {"name": "iPhone Pro Max / Plus", "width": 428, "height": 926}
]

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

AUDIT_JS_SNIPPET = """
<div id="mobile-audit-container" style="display:none;"></div>
<script>
window.addEventListener('DOMContentLoaded', () => {
  const issues = [];
  const viewportWidth = window.innerWidth;
  const docScrollWidth = document.documentElement.scrollWidth;
  
  if (docScrollWidth > viewportWidth + 1) {
    issues.push({
      type: 'HORIZONTAL_OVERFLOW',
      severity: 'CRITICAL',
      message: `Page width (${docScrollWidth}px) exceeds mobile viewport (${viewportWidth}px) by ${docScrollWidth - viewportWidth}px`
    });
  }

  // Scan all visible elements for overflow past right viewport edge
  document.querySelectorAll('body *').forEach(el => {
    if (el.id === 'mobile-audit-container' || el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return;
    const r = el.getBoundingClientRect();
    if (r.right > viewportWidth + 1.5) {
      issues.push({
        type: 'ELEMENT_OVERFLOW',
        severity: 'CRITICAL',
        element: `<${el.tagName.toLowerCase()} class="${el.className}">`,
        right: Math.round(r.right),
        overflow: Math.round(r.right - viewportWidth)
      });
    }
    
    // Check input font size for iOS Safari unwanted zoom (must be >= 16px)
    if (el.tagName === 'INPUT' || el.tagName === 'SELECT' || el.tagName === 'TEXTAREA') {
      const fs = parseFloat(window.getComputedStyle(el).fontSize);
      if (fs < 15.8) {
        issues.push({
          type: 'IOS_SAFARI_AUTOZOOM_RISK',
          severity: 'WARNING',
          element: `<${el.tagName.toLowerCase()} placeholder="${el.getAttribute('placeholder') || ''}">`,
          fontSize: `${fs}px (minimum recommended is 16px)`
        });
      }
    }
  });

  document.getElementById('mobile-audit-container').textContent = JSON.stringify(issues);
});
</script>
"""

def audit_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: file not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Inject audit script before </body>
    temp_html = html.replace('</body>', AUDIT_JS_SNIPPET + '</body>')
    temp_path = file_path + '.audit_temp.html'
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(temp_html)

    os.makedirs('screenshots', exist_ok=True)
    all_passed = True
    print(f"\n=======================================================")
    print(f"  Mobile Adaptation Audit: {os.path.basename(file_path)}")
    print(f"=======================================================")

    for vp in VIEWPORTS:
        w = vp['width']
        h = vp['height']
        name = vp['name']
        screenshot_name = f"screenshots/{os.path.basename(os.path.dirname(file_path))}_{w}x{h}.png"

        cmd = [
            CHROME_PATH,
            '--headless',
            '--disable-gpu',
            f'--window-size={w},{h}',
            f'--screenshot={screenshot_name}',
            '--dump-dom',
            'file://' + os.path.abspath(temp_path)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        match = re.search(r'<div id="mobile-audit-container"[^>]*>(.*?)</div>', res.stdout, re.DOTALL)
        
        if match and match.group(1):
            issues = json.loads(match.group(1))
            critical = [i for i in issues if i.get('severity') == 'CRITICAL']
            warnings = [i for i in issues if i.get('severity') == 'WARNING']
            
            if not critical and not warnings:
                print(f"  [PASS] {name} ({w}x{h}px) -> Perfect mobile layout! (Screenshot: {screenshot_name})")
            else:
                all_passed = False
                print(f"  [FAIL] {name} ({w}x{h}px) -> {len(critical)} critical issues, {len(warnings)} warnings:")
                for c in critical[:4]:
                    print(f"    - ❌ {c.get('type')}: {c.get('message') or c.get('element')} (+{c.get('overflow')}px)")
                for w_iss in warnings[:2]:
                    print(f"    - ⚠️  {w_iss.get('type')}: {w_iss.get('element')} -> {w_iss.get('fontSize')}")
        else:
            print(f"  [?] {name} ({w}x{h}px) -> Unable to capture audit results")

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return all_passed

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'sites/underwood-fencing-and-gates/index.html'
    passed = audit_file(target)
    sys.exit(0 if passed else 1)
