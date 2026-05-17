document.addEventListener('DOMContentLoaded', function () {
  const re = /^([0-5][0-9]):([0-5][0-9])$/;

  function validateInput(input) {
    const errorEl = input.closest('.split-row')?.querySelector('.duration-error');
    const val = (input.value || '').trim();
    if (!val) {
      if (errorEl) errorEl.textContent = '';
      input.setAttribute('aria-invalid', 'false');
      return true;
    }
    const ok = re.test(val);
    if (errorEl) errorEl.textContent = ok ? '' : 'Enter duration as mm:ss (00–59 minutes and seconds).';
    input.setAttribute('aria-invalid', ok ? 'false' : 'true');
    return ok;
  }

  document.querySelectorAll('input.duration-mmss').forEach(input => {
    input.setAttribute('pattern', '[0-5][0-9]:[0-5][0-9]');
    input.setAttribute('inputmode', 'numeric');
    input.addEventListener('blur', () => validateInput(input));
    input.addEventListener('input', () => validateInput(input));
  });

  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function (e) {
      const inputs = Array.from(form.querySelectorAll('input.duration-mmss'));
      const allOk = inputs.every(validateInput);
      if (!allOk) {
        e.preventDefault();
        const firstInvalid = inputs.find(i => i.getAttribute('aria-invalid') === 'true');
        if (firstInvalid) firstInvalid.focus();
      }
    });
  });
});
