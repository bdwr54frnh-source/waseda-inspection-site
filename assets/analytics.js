/* GA4 Web — プロパティ G-WXF127P26H（tandemair / elementarycode HP と共通） */
(function (w, d, measurementId) {
  w.dataLayer = w.dataLayer || [];
  w.gtag = function gtag() {
    w.dataLayer.push(arguments);
  };
  var s = d.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
  d.head.appendChild(s);
  w.gtag('js', new Date());
  w.gtag('config', measurementId, { anonymize_ip: true, send_page_view: true });
})(window, document, 'G-WXF127P26H');
