/**
 * Client support for  SPARouter, see dash_spa\spa_components.py
 */


/**
 * Monitor changes in the SPA routers attributes. If
 * the tabindex attribute changes iterate over the
 * child elements showing the target and hiding the
 * rest.
 */

function spa_router_div(mutationsList, observer) {
  for (let mutation of mutationsList) {
    if ( mutation.attributeName == 'tabindex') {
      switch_div = mutation.target
      tabindex = switch_div.id + '::' + switch_div.getAttribute("tabindex")
      console.log('spa_router_div target:%s, tabindex=%s', switch_div.id, tabindex);
      for (const div of switch_div.children) {
        if (div.id === tabindex) {
          div.style["display"] = "block"
        }
        else {
          div.style["display"] = "none"
        }
      }
    }
  }
}

/**
 * An SPA router button has been clicked. Use the
 * buttons tabindex attribute to identify the the
 * associated router element and set its tabindex
 */

function spa_router_btn_onclick(e) {
  tabindex = e.currentTarget.getAttribute('tabIndex');
  target = tabindex.split('::');
  // console.log('spa_router_btn_onclick: target %s', target[0]);
  switch_div = document.getElementById(target[0]);
  switch_div.setAttribute("tabindex", target[1]);
}

/**
 * Called on page load. Set up a MutationObserver that will trigger
 * whenever React makes changes to the DOM. Look for the addition of
 * spa-router elements. For buttons add an onclick event handler and
 * for DIV add a MutationObserver that will monitor attribute changes
 * on the DIV 
 */

(function () {

  return 
  
  console.log('assets/js/spa-router.js is active')

  // https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver

  const spa_element_cb = function (mutationsList, observer) {
    for (let mutation of mutationsList) {
      if (mutation.type === 'childList' && mutation.addedNodes.length) {
        var switches = document.getElementsByClassName("spa-router");
        for (const s of switches) {
          if (s.tagName == 'BUTTON') {
            // console.log('Set on click event')
            s.addEventListener("click", spa_router_btn_onclick, false);
          }
          if (s.tagName == 'DIV') {
            // console.log('Set attribute observer on %s', s.id)
            const observer = new MutationObserver(spa_router_div);
            observer.observe(s, { attributes: true });
          }
        }
      }
    }
  };

  const observer = new MutationObserver(spa_element_cb);
  react_root = document.getElementById("react-entry-point");
  const config = { childList: true, subtree: true };
  observer.observe(react_root, config);


})()