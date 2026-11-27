(() => {
  const sections = [...document.querySelectorAll('[data-eden-style]')];
  const style = document.querySelector('#eden-style');
  const room = document.querySelector('#eden-room');
  const title = document.querySelector('#eden-title');
  const comparison = document.querySelector('#eden-comparison');
  const controls = document.querySelector('#eden-controls');
  const hide = (element, hidden) => {
    element.hidden = hidden;
    element.style.display = hidden ? 'none' : '';
  };
  function render() {
    const hash = location.hash.slice(1);
    const roomOption = [...room.options].find(option => option.value && option.value === hash);
    const selected = sections.find(section => section.id === hash) || sections[1];
    room.value = roomOption ? hash : '';
    style.value = roomOption ? '' : selected.id;
    comparison.replaceChildren();
    for (const section of sections) {
      hide(section, Boolean(roomOption) || section !== selected);
      if (roomOption) {
        const key = hash.slice(5);
        const card = section.querySelector('[data-eden-room="' + key + '"]').cloneNode(true);
        card.querySelector('h3').textContent = section.getAttribute('aria-label');
        comparison.append(card);
      }
    }
    title.textContent = roomOption ? roomOption.text : '';
    hide(title, !roomOption);
    hide(comparison, !roomOption);
  }
  for (const select of [style, room]) {
    select.addEventListener('change', () => {
      if (select.value) {
        history.pushState(null, '', '#' + select.value);
      }
      render();
    });
  }
  window.addEventListener('hashchange', render);
  window.addEventListener('popstate', render);
  hide(controls, false);
  render();
})();
