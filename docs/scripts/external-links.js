// Open external links in a new browser tab so customers don't lose their place
// in the docs when clicking through to Microsoft Learn, GitHub, the Azure
// portal, etc. Same-origin links keep their default behavior.
(function () {
  function markExternal() {
    var sameOrigin = window.location.origin;
    document.querySelectorAll('a[href^="http"]').forEach(function (link) {
      try {
        if (new URL(link.href).origin === sameOrigin) return;
      } catch (e) {
        return;
      }
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    });
  }

  // mkdocs-material instant nav exposes document$ for page-change events.
  // Fall back to DOMContentLoaded for non-instant configs.
  if (typeof document$ !== 'undefined' && typeof document$.subscribe === 'function') {
    document$.subscribe(markExternal);
  } else if (document.readyState !== 'loading') {
    markExternal();
  } else {
    document.addEventListener('DOMContentLoaded', markExternal);
  }
})();
