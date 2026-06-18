/* PowerStacks Assistant (Pax) floating chat widget for the docs site.
 * Injects a floating button that opens Pax in a slide-up iframe panel.
 * Styling lives in stylesheets/pax-widget.css.
 */
(function () {
  // Pax backend URL. Swap to https://assistant.powerstacks.com once the custom domain is live.
  var PAX_URL = "https://pax-assistant-prod-pwst-f7cyh9hedegkd3e4.eastus2-01.azurewebsites.net";

  var CHAT_ICON =
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>';
  var CLOSE_ICON =
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>';

  function mount() {
    // Mounted once and appended to <body>, so it survives Material instant navigation.
    if (document.getElementById("ps-assistant-root")) return;

    var root = document.createElement("div");
    root.id = "ps-assistant-root";
    root.setAttribute("aria-label", "PowerStacks Assistant");
    root.innerHTML =
      '<button id="ps-assistant-toggle" aria-label="Open PowerStacks Assistant" title="PowerStacks Assistant">' +
      '<span id="ps-icon-chat">' + CHAT_ICON + "</span>" +
      '<span id="ps-icon-close" style="display:none">' + CLOSE_ICON + "</span>" +
      "</button>" +
      '<div id="ps-assistant-panel" aria-hidden="true">' +
      '<div id="ps-assistant-header">' +
      '<div id="ps-assistant-title">' + CHAT_ICON + "<span>PowerStacks Assistant</span></div>" +
      '<button id="ps-assistant-close" aria-label="Close PowerStacks Assistant">' + CLOSE_ICON + "</button>" +
      "</div>" +
      '<div id="ps-assistant-body">' +
      '<iframe id="ps-assistant-iframe" src="' + PAX_URL + '" title="PowerStacks Assistant" allow="clipboard-write" loading="lazy"></iframe>' +
      "</div></div>";
    document.body.appendChild(root);

    var toggle = root.querySelector("#ps-assistant-toggle");
    var panel = root.querySelector("#ps-assistant-panel");
    var closeBtn = root.querySelector("#ps-assistant-close");
    var iconChat = root.querySelector("#ps-icon-chat");
    var iconClose = root.querySelector("#ps-icon-close");
    var isOpen = false;

    function open() {
      isOpen = true;
      panel.classList.add("ps-open");
      panel.setAttribute("aria-hidden", "false");
      iconChat.style.display = "none";
      iconClose.style.display = "inline";
    }
    function close() {
      isOpen = false;
      panel.classList.remove("ps-open");
      panel.setAttribute("aria-hidden", "true");
      iconChat.style.display = "inline";
      iconClose.style.display = "none";
    }

    toggle.addEventListener("click", function () {
      isOpen ? close() : open();
    });
    closeBtn.addEventListener("click", close);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && isOpen) close();
    });
  }

  // Material exposes document$ (fires on first load and every instant navigation). Use it when
  // present; otherwise fall back to a plain DOM-ready mount.
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(mount);
  } else if (document.readyState !== "loading") {
    mount();
  } else {
    document.addEventListener("DOMContentLoaded", mount);
  }
})();
