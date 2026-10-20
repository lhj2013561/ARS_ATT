/*
 * 설문 공통 스크립트
 * - 미응답 문항 표시(한국어 안내)와 첫 미응답 문항으로 이동
 * - 동의하지 않음 선택 시 안내 문구 표시
 * - 버튼 연속 클릭으로 인한 중복 제출 방지
 * 서버에서도 같은 검증을 하므로, 이 스크립트가 동작하지 않아도 잘못된 응답은 저장되지 않습니다.
 */
(function () {
  'use strict';

  // 하이픈·공백·점을 제외한 숫자 기준: 010-XXXX-XXXX 또는 011/016/017/018/019-XXX(X)-XXXX
  var PHONE_RE = /^(?:010\d{8}|01[16789]\d{7,8})$/;

  var form;
  var checks = [];
  var summary;

  function $all(root, selector) {
    return Array.prototype.slice.call(root.querySelectorAll(selector));
  }

  function phoneDigits(value) {
    return value.replace(/[\s.\-]/g, '');
  }

  // 반환값: 오류 메시지(문자열) 또는 null
  function problemOf(item) {
    var kind = item.getAttribute('data-sv-check');
    if (kind === 'choice') {
      return item.querySelector('input[type=radio]:checked') ? null : item.getAttribute('data-msg-required');
    }
    var input = item.querySelector('input');
    var value = input ? input.value.trim() : '';
    if (kind === 'integer') {
      if (value === '') return item.getAttribute('data-msg-required');
      var min = Number(item.getAttribute('data-min'));
      var max = Number(item.getAttribute('data-max'));
      var ok = /^\d+$/.test(value) && Number(value) >= min && Number(value) <= max;
      return ok ? null : item.getAttribute('data-msg-invalid');
    }
    if (kind === 'phone') {
      return value === '' || PHONE_RE.test(phoneDigits(value)) ? null : item.getAttribute('data-msg-invalid');
    }
    return null;
  }

  function render(item, message) {
    var error = item.querySelector('.sv-error');
    item.classList.toggle('is-invalid', Boolean(message));
    $all(item, 'input').forEach(function (input) {
      if (message) input.setAttribute('aria-invalid', 'true');
      else input.removeAttribute('aria-invalid');
    });
    if (error) {
      if (message) error.textContent = message;
      error.hidden = !message;
    }
  }

  function updateSummary() {
    if (!summary) return;
    var stillInvalid = checks.some(function (item) {
      return item.classList.contains('is-invalid');
    });
    if (!stillInvalid) summary.hidden = true;
  }

  function updateDeclineNote(item) {
    var note = item.querySelector('[data-sv-decline-note]');
    if (!note) return;
    var checked = item.querySelector('input[type=radio]:checked');
    note.hidden = !(checked && checked.value === item.getAttribute('data-sv-decline'));
  }

  function focusItem(item) {
    item.scrollIntoView({ behavior: 'smooth', block: 'center' });
    var target = item.querySelector('input:checked') || item.querySelector('input');
    if (target) {
      try {
        target.focus({ preventScroll: true });
      } catch (e) {
        target.focus();
      }
    }
  }

  function buttons() {
    return $all(form, 'button');
  }

  function lock() {
    form.setAttribute('data-sv-submitting', '1');
    buttons().forEach(function (button) {
      button.disabled = true;
      var busy = button.getAttribute('data-busy-label');
      if (busy) {
        button.setAttribute('data-idle-label', button.textContent);
        button.textContent = busy;
      }
    });
  }

  function unlock() {
    form.removeAttribute('data-sv-submitting');
    buttons().forEach(function (button) {
      button.disabled = false;
      var idle = button.getAttribute('data-idle-label');
      if (idle) button.textContent = idle;
    });
  }

  // capture 단계에서 먼저 검사해, 실패하면 oTree의 기본 제출 처리(버튼 비활성화)까지 막습니다.
  function onSubmit(event) {
    if (event.target !== form) return;
    if (form.getAttribute('data-sv-submitting') === '1') {
      event.preventDefault();
      event.stopPropagation();
      return;
    }
    var invalid = checks.filter(function (item) {
      var message = problemOf(item);
      render(item, message);
      return Boolean(message);
    });
    if (invalid.length) {
      event.preventDefault();
      event.stopPropagation();
      if (summary) summary.hidden = false;
      focusItem(invalid[0]);
      return;
    }
    lock();
  }

  function init() {
    form = document.getElementById('form');
    if (!form) return;
    // 브라우저 기본 검증 팝업 대신 문항별 한국어 안내를 사용합니다.
    form.noValidate = true;
    checks = $all(form, '[data-sv-check]');
    summary = form.querySelector('[data-sv-summary]');

    checks.forEach(function (item) {
      var recheck = function () {
        updateDeclineNote(item);
        if (item.classList.contains('is-invalid')) {
          render(item, problemOf(item));
          updateSummary();
        }
      };
      item.addEventListener('change', recheck);
      item.addEventListener('input', recheck);
      updateDeclineNote(item);
    });

    var phone = form.querySelector('.sv-phone-input');
    if (phone) {
      phone.addEventListener('blur', function () {
        var digits = phoneDigits(phone.value);
        if (PHONE_RE.test(digits)) {
          phone.value = digits.length === 11
            ? digits.slice(0, 3) + '-' + digits.slice(3, 7) + '-' + digits.slice(7)
            : digits.slice(0, 3) + '-' + digits.slice(3, 6) + '-' + digits.slice(6);
        }
      });
    }

    document.addEventListener('submit', onSubmit, true);

    // 뒤로 가기 캐시로 페이지가 다시 보일 때 잠긴 버튼을 풀어 줍니다.
    window.addEventListener('pageshow', function (event) {
      if (event.persisted) unlock();
    });

    // 서버 검증에서 오류가 난 경우 첫 오류 문항으로 이동합니다.
    var firstInvalid = form.querySelector('[data-sv-check].is-invalid');
    if (firstInvalid) focusItem(firstInvalid);
  }

  document.addEventListener('DOMContentLoaded', init);
})();
