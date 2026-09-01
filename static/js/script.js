document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Toggle
  const mobileToggle = document.getElementById('mobileToggle');
  const navMenu = document.getElementById('navMenu');
  
  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('open');
      const isOpen = navMenu.classList.contains('open');
      mobileToggle.setAttribute('aria-expanded', isOpen);
    });

    // Close mobile menu when clicking outside or link
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
      });
    });
  }

  // 2. Sticky Navbar scroll shadow
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 20) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }

  // 3. Accurate Countdown Timer to 21 September 2026 23:59:59 IST
  const countdownDays = document.getElementById('countDays');
  const countdownHours = document.getElementById('countHours');
  const countdownMins = document.getElementById('countMins');
  const countdownSecs = document.getElementById('countSecs');
  const countdownStatus = document.getElementById('countdownStatus');

  if (countdownDays && countdownHours && countdownMins && countdownSecs) {
    // Deadline: 21 September 2026, 23:59:59 IST
    const deadline = new Date('2026-09-21T23:59:59+05:30').getTime();

    function updateCountdown() {
      const now = new Date().getTime();
      const difference = deadline - now;

      if (difference <= 0) {
        if (countdownStatus) {
          countdownStatus.innerText = 'Registration deadline has passed.';
        }
        countdownDays.innerText = '00';
        countdownHours.innerText = '00';
        countdownMins.innerText = '00';
        countdownSecs.innerText = '00';
        return;
      }

      const days = Math.floor(difference / (1000 * 60 * 60 * 24));
      const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((difference % (1000 * 60)) / 1000);

      countdownDays.innerText = String(days).padStart(2, '0');
      countdownHours.innerText = String(hours).padStart(2, '0');
      countdownMins.innerText = String(minutes).padStart(2, '0');
      countdownSecs.innerText = String(seconds).padStart(2, '0');
    }

    updateCountdown();
    setInterval(updateCountdown, 1000);
  }

  // 4. FAQ Accordion Interaction
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');

    if (questionBtn && answer) {
      questionBtn.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        
        // Close others
        faqItems.forEach(other => {
          if (other !== item) {
            other.classList.remove('active');
            const otherAns = other.querySelector('.faq-answer');
            if (otherAns) otherAns.style.maxHeight = null;
          }
        });

        // Toggle current
        if (!isActive) {
          item.classList.add('active');
          answer.style.maxHeight = answer.scrollHeight + 'px';
        } else {
          item.classList.remove('active');
          answer.style.maxHeight = null;
        }
      });
    }
  });

  // 5. Client-side Form Validation & Prevention
  const registerForm = document.getElementById('donorRegistrationForm');
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      const mobileInput = document.getElementById('mobile');
      const ageInput = document.getElementById('age');
      const collegeIdInput = document.getElementById('college_id');
      const emailInput = document.getElementById('email');

      // Phone validation (10 digits)
      if (mobileInput) {
        const phoneVal = mobileInput.value.trim();
        const phoneRegex = /^[6-9]\d{9}$/;
        if (!phoneRegex.test(phoneVal)) {
          alert('Please enter a valid 10-digit Indian mobile number starting with 6, 7, 8, or 9.');
          mobileInput.focus();
          e.preventDefault();
          return false;
        }
      }

      // Age validation (17 to 65)
      if (ageInput) {
        const ageVal = parseInt(ageInput.value, 10);
        if (isNaN(ageVal) || ageVal < 17 || ageVal > 70) {
          alert('Please enter a valid donor age between 17 and 70.');
          ageInput.focus();
          e.preventDefault();
          return false;
        }
      }

      // College ID validation
      if (collegeIdInput && !collegeIdInput.value.trim()) {
        alert('Please enter your College Roll No or Employee ID.');
        collegeIdInput.focus();
        e.preventDefault();
        return false;
      }

      // Show submitting state on button
      const submitBtn = registerForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.innerHTML = '<span>Processing Registration...</span>';
        submitBtn.disabled = true;
      }
      return true;
    });
  }

  // 6. Flash Alert Dismiss
  document.querySelectorAll('.flash-close').forEach(btn => {
    btn.addEventListener('click', () => {
      const alert = btn.closest('.flash-alert');
      if (alert) alert.remove();
    });
  });
});
