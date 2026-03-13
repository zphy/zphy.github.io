(function () {
  "use strict";

  var AUTO_ADVANCE_MS = 5000;

  function textOf(el) {
    return (el && el.textContent ? el.textContent : "").replace(/\s+/g, " ").trim();
  }

  function makeEl(tag, className, text) {
    var el = document.createElement(tag);
    if (className) {
      el.className = className;
    }
    if (typeof text === "string") {
      el.textContent = text;
    }
    return el;
  }

  function safeSlides(raw) {
    if (!Array.isArray(raw)) {
      return [];
    }
    return raw.filter(function (s) {
      return s && typeof s.image === "string" && typeof s.title === "string";
    });
  }

  function toCssSize(value) {
    if (typeof value === "number" && isFinite(value) && value > 0) {
      return value + "px";
    }
    if (typeof value === "string") {
      var trimmed = value.trim();
      if (trimmed) {
        return trimmed;
      }
    }
    return "";
  }

  function insertCarouselAfterFeaturedHeading(slides) {
    var root = document.getElementById("layout-content");
    if (!root) {
      return;
    }

    var headings = root.querySelectorAll("h2");
    var target = null;
    for (var i = 0; i < headings.length; i++) {
      if (textOf(headings[i]).toLowerCase().indexOf("featured work") !== -1) {
        target = headings[i];
        break;
      }
    }
    if (!target) {
      return;
    }

    var host = makeEl("div", "featured-work");
    var anchor = target;
    var next = target.nextElementSibling;
    if (next && next.tagName === "P") {
      anchor = next;
    }
    anchor.insertAdjacentElement("afterend", host);

    if (slides.length === 0) {
      host.appendChild(makeEl("div", "featured-work-empty", "No slides configured. Edit data/featured-work-slides.js."));
      return;
    }

    var frame = makeEl("div", "featured-work-frame");
    var dots = makeEl("div", "featured-work-dots");
    var controls = makeEl("div", "featured-work-controls");
    host.appendChild(frame);
    host.appendChild(dots);
    frame.appendChild(controls);

    var prevBtn = makeEl("button", "featured-work-btn", "<");
    var nextBtn = makeEl("button", "featured-work-btn", ">");
    prevBtn.setAttribute("aria-label", "Previous slide");
    nextBtn.setAttribute("aria-label", "Next slide");
    controls.appendChild(prevBtn);
    controls.appendChild(nextBtn);

    var slideEls = [];
    var dotEls = [];
    var index = 0;
    var timer = null;

    slides.forEach(function (slide) {
      var slideEl = makeEl("div", "featured-work-slide");
      var img = makeEl("img", "featured-work-image");
      img.src = slide.image;
      img.alt = slide.title;
      var displayWidth = toCssSize(slide.displayWidth);
      var displayMaxHeight = toCssSize(slide.displayMaxHeight);
      if (displayWidth) {
        img.style.maxWidth = displayWidth;
      }
      if (displayMaxHeight) {
        img.style.maxHeight = displayMaxHeight;
      }
      slideEl.appendChild(img);

      var caption = makeEl("div", "featured-work-caption");
      caption.appendChild(makeEl("p", "featured-work-title", slide.title));

      var paper = makeEl("p", "featured-work-paper");
      if (slide.paperUrl) {
        var link = makeEl("a", "", slide.paperTitle || "Paper");
        link.href = slide.paperUrl;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        paper.appendChild(link);
      } else {
        paper.textContent = slide.paperTitle || "";
      }
      caption.appendChild(paper);

      if (slide.note) {
        caption.appendChild(makeEl("p", "featured-work-note", slide.note));
      }

      slideEl.appendChild(caption);
      frame.appendChild(slideEl);
      slideEls.push(slideEl);

      var dot = makeEl("button", "featured-work-dot");
      dot.setAttribute("aria-label", "Slide");
      dots.appendChild(dot);
      dotEls.push(dot);
    });

    function show(nextIndex) {
      if (nextIndex < 0) {
        nextIndex = slideEls.length - 1;
      }
      if (nextIndex >= slideEls.length) {
        nextIndex = 0;
      }
      index = nextIndex;
      for (var i = 0; i < slideEls.length; i++) {
        slideEls[i].classList.toggle("active", i === index);
        dotEls[i].classList.toggle("active", i === index);
      }
    }

    function stopAuto() {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
    }

    function startAuto() {
      stopAuto();
      timer = setInterval(function () {
        show(index + 1);
      }, AUTO_ADVANCE_MS);
    }

    prevBtn.addEventListener("click", function () {
      show(index - 1);
      startAuto();
    });
    nextBtn.addEventListener("click", function () {
      show(index + 1);
      startAuto();
    });

    dotEls.forEach(function (dot, i) {
      dot.addEventListener("click", function () {
        show(i);
        startAuto();
      });
    });

    host.addEventListener("mouseenter", stopAuto);
    host.addEventListener("mouseleave", startAuto);

    show(0);
    startAuto();
  }

  document.addEventListener("DOMContentLoaded", function () {
    insertCarouselAfterFeaturedHeading(safeSlides(window.FEATURED_WORK_SLIDES));
  });
})();
