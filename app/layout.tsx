import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Election Intelligence Platform',
  description: 'Enterprise Election Intelligence Platform & Control Center for managing elections, candidates, constituencies, polling, real-time analytics, and AI-assisted governance.',
  openGraph: {
    title: 'Election Intelligence Platform',
    description: 'Enterprise Election Intelligence Platform & Control Center for managing elections, candidates, constituencies, polling, real-time analytics, and AI-assisted governance.',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Election Intelligence Platform',
    description: 'Enterprise Election Intelligence Platform & Control Center for managing elections, candidates, constituencies, polling, real-time analytics, and AI-assisted governance.',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                try {
                  var storedTheme = localStorage.getItem('election_theme') || localStorage.getItem('theme');
                  if (storedTheme === 'light') {
                    document.documentElement.classList.remove('dark');
                  } else {
                    document.documentElement.classList.add('dark');
                  }
                } catch(e) {}

                try {
                  var _origFetch = window.fetch;
                  Object.defineProperty(window, 'fetch', {
                    get: function() { return _origFetch; },
                    set: function(fn) { _origFetch = fn; },
                    configurable: true,
                    enumerable: true
                  });
                  if (typeof Window !== 'undefined' && Window.prototype) {
                    var desc = Object.getOwnPropertyDescriptor(Window.prototype, 'fetch');
                    if (desc && !desc.set) {
                      Object.defineProperty(Window.prototype, 'fetch', {
                        get: function() { return _origFetch; },
                        set: function(fn) { _origFetch = fn; },
                        configurable: true,
                        enumerable: true
                      });
                    }
                  }
                } catch(e) {}
              })();
            `,
          }}
        />
      </head>
      <body className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 selection:bg-indigo-500/30 transition-colors duration-150" suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
