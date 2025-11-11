# FAQ Bot Landing Page

A modern, conversion-focused landing page for the FAQ Bot open-source document Q&A system.

## 🎯 Overview

This landing page showcases the FAQ Bot project with:
- **11 Sections**: Hero, Problem, How It Works, Features, Demo, Pricing, Tech Stack, FAQ, CTA, Footer
- **Modern Design**: Clean, professional UI with gradient accents and smooth animations
- **Fully Responsive**: Mobile-first design that works on all devices
- **Interactive Elements**: Cost calculator, FAQ accordion, copy-to-clipboard, scroll animations
- **Performance Optimized**: Fast loading, smooth animations, accessibility focused

## 📁 Files

```
landing/
├── index.html          # Main HTML structure
├── styles.css          # Complete stylesheet with design system
├── script.js           # JavaScript for interactions and animations
└── README.md          # This file
```

## 🚀 Quick Start

### Option 1: Open Locally

Simply open `index.html` in your web browser:

```bash
cd landing
open index.html  # macOS
# or
start index.html  # Windows
# or
xdg-open index.html  # Linux
```

### Option 2: Local Server

For better performance and testing, use a local server:

**Using Python:**
```bash
cd landing
python3 -m http.server 8000
# Open http://localhost:8000 in your browser
```

**Using Node.js (http-server):**
```bash
npm install -g http-server
cd landing
http-server -p 8000
# Open http://localhost:8000 in your browser
```

**Using PHP:**
```bash
cd landing
php -S localhost:8000
# Open http://localhost:8000 in your browser
```

## 🌐 Deployment

### Deploy to Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
cd landing
vercel
```

3. Follow the prompts to deploy

### Deploy to Netlify

1. Install Netlify CLI:
```bash
npm install -g netlify-cli
```

2. Deploy:
```bash
cd landing
netlify deploy
```

3. For production:
```bash
netlify deploy --prod
```

### Deploy to GitHub Pages

1. Create a new branch:
```bash
git checkout -b gh-pages
```

2. Copy landing files to root:
```bash
cp landing/* .
git add index.html styles.css script.js
git commit -m "Deploy landing page"
git push origin gh-pages
```

3. Enable GitHub Pages in repository settings:
   - Go to Settings → Pages
   - Source: gh-pages branch
   - Save

### Deploy to Cloudflare Pages

1. Go to [Cloudflare Pages](https://pages.cloudflare.com/)
2. Connect your GitHub repository
3. Set build settings:
   - Build command: (leave empty)
   - Build output directory: `/landing`
4. Deploy

## ✏️ Customization

### Update Content

Edit `index.html` to change:
- Text content
- Links to GitHub repository
- Contact email
- Social media links

### Change Colors

Edit CSS variables in `styles.css`:

```css
:root {
    --primary: #4F46E5;        /* Main brand color */
    --primary-hover: #4338CA;  /* Hover state */
    /* ... other colors */
}
```

### Modify Animations

Edit animation timings in `script.js`:

```javascript
// Hero chat animation loop
setTimeout(animateChatMockup, 5000); // Change 5000 to desired milliseconds

// Toast notification duration
setTimeout(() => {
    toast.classList.remove('show');
}, 2000); // Change 2000 to desired milliseconds
```

### Add Images

Replace placeholder SVGs with actual images:

1. Add images to `landing/images/` directory
2. Update HTML:
```html
<!-- Replace SVG with: -->
<img src="images/screenshot-1.png" alt="Description">
```

3. Optimize images:
   - Use WebP format for better compression
   - Resize to appropriate dimensions
   - Use lazy loading: `<img loading="lazy" src="...">`

## 📊 Analytics

To add Google Analytics:

1. Get your Google Analytics tracking ID
2. Add to `<head>` in `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

Replace `GA_MEASUREMENT_ID` with your actual ID.

## 🎨 Design System

### Colors

- **Primary**: #4F46E5 (Indigo) - Main brand color
- **Success**: #10B981 (Green) - Success states
- **Warning**: #F59E0B (Amber) - Warnings
- **Error**: #EF4444 (Red) - Errors

### Typography

- **Font**: Inter (Google Fonts)
- **Sizes**: 12px to 48px (defined as CSS variables)
- **Weights**: 400, 500, 600, 700

### Spacing

Based on 8px unit system (4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 80px)

### Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1023px
- **Desktop**: ≥ 1024px

## ✅ Features

### Interactive Elements

- ✅ Sticky navigation with scroll effect
- ✅ Mobile hamburger menu
- ✅ Smooth scroll to sections
- ✅ Hero chat animation with loop
- ✅ Scroll-triggered fade-in animations
- ✅ FAQ accordion (one item open at a time)
- ✅ Cost calculator with real-time updates
- ✅ Copy-to-clipboard for code snippet
- ✅ Toast notifications
- ✅ Hover effects on cards and buttons
- ✅ Keyboard navigation support

### Performance

- Fast loading (< 3s)
- Throttled scroll events
- Intersection Observer for animations
- No external dependencies (except Google Fonts)

### Accessibility

- Semantic HTML5
- ARIA labels where needed
- Keyboard navigation support
- Focus indicators
- Alt text for images
- Color contrast ratio > 4.5:1

## 🔧 Browser Support

- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)
- Mobile Safari (iOS 14+)
- Chrome Mobile (Android 10+)

## 📝 TODO

Future enhancements:

- [ ] Add demo video
- [ ] Replace screenshot placeholders with actual images
- [ ] Add logo/favicon
- [ ] Create OG image (1200x630)
- [ ] Create Twitter card image (1200x600)
- [ ] Add dark mode toggle
- [ ] Add blog section
- [ ] Implement A/B testing
- [ ] Add chat widget for support

## 📄 License

MIT License - Same as FAQ Bot project

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple devices/browsers
5. Submit a pull request

## 📧 Contact

Questions or feedback? Contact a.molchansky@gmail.com

---

**Built with ❤️ for the open-source community**
