// Sahayak Content Script - STABLE + SMART VALIDATION VERSION
(function() {
  'use strict';

  const API_URL = 'http://localhost:5000';
  const IS_IFRAME = window !== window.top;

  if (IS_IFRAME) {
    runIframeMode();
  } else {
    runParentMode();
  }

  // ============================================================
  // IFRAME MODE — runs inside the form iframe
  // Finds fields, validates them, sends data to parent
  // ============================================================
  // ── Universal Fuzzy Normalizer (top-level: accessible by iframe + parent) ──
  // ── Universal Fuzzy Normalizer ──────────────────────────────────────
  // Used everywhere: form labels, OCR data, chat text, voice input
  function fuzzyLabel(label) {
    let l = (label || '').toLowerCase().trim();

    // ── Phone / Mobile (all variants) ────────────────────────────────
    l = l.replace(/\bph\.?\s*no\.?\b/g,            'phone number');
    l = l.replace(/\bph\.?\s*num(ber)?\b/g,         'phone number');
    l = l.replace(/\bphn\.?\b/g,                     'phone number');
    l = l.replace(/\bph[ao]ne?\b/g,                   'phone');
    l = l.replace(/\bphon[eo]\b/g,                    'phone');
    l = l.replace(/\bmob\.?\s*no\.?\b/g,           'mobile number');
    l = l.replace(/\bmob\.?\s*num(ber)?\b/g,        'mobile number');
    l = l.replace(/\bm[ou]b[iy]l[ae]?\b/g,           'mobile');
    l = l.replace(/\bcontact\s*(no\.?|num(ber)?)?\b/g, 'mobile number');
    l = l.replace(/\bcell\s*(no\.?|num(ber)?)?\b/g,'mobile number');
    l = l.replace(/\bwhatsapp\s*(no\.?|num(ber)?)?\b/g,'mobile number');
    l = l.replace(/\btel\.?\s*(no\.?|num(ber)?)?\b/g, 'phone number');
    l = l.replace(/\bteleph[ao]ne?\b/g,               'phone');

    // ── Aadhaar variants ─────────────────────────────────────────────
    l = l.replace(/\baadh?[aeu]{1,2}r\b/g,  'aadhaar');
    l = l.replace(/\badh[aeu]{1,2}r\b/g,    'aadhaar');
    l = l.replace(/\baadhar\b/g,             'aadhaar');
    l = l.replace(/\badhar\b/g,              'aadhaar');
    l = l.replace(/\baadh\b/g,               'aadhaar');
    l = l.replace(/\buid[ai]?\s*(no\.?|card|num(ber)?)?\b/g, 'aadhaar number');

    // ── PAN variants ─────────────────────────────────────────────────
    l = l.replace(/\bperman[ae]nt\s*acc[ao]unt\s*(num(ber)?)?\b/g, 'pan number');
    l = l.replace(/\bpan\s*c[ae]rd\b/g,    'pan card');
    l = l.replace(/\bpan\s*(no\.?|num(ber)?)\b/g, 'pan number');

    // ── IFSC variants ────────────────────────────────────────────────
    l = l.replace(/\bif[sc]{2}\b/g,          'ifsc');
    l = l.replace(/\bifcs\b/g,               'ifsc');
    l = l.replace(/\bisfc\b/g,               'ifsc');
    l = l.replace(/\bifsc\s*c[ao]de\b/g,    'ifsc code');
    l = l.replace(/\bbank\s*c[ao]de\b/g,    'ifsc code');
    l = l.replace(/\brtgs\s*c[ao]de\b/g,    'ifsc code');

    // ── Account Number variants ───────────────────────────────────────
    l = l.replace(/\bacc[ao]unt\b/g,         'account');
    l = l.replace(/\bacct?\.?\b/g,           'account');
    l = l.replace(/\bacc\.?\s*(no\.?|num(ber)?)\b/g, 'account number');
    l = l.replace(/\bbank\s*acc(ount)?\b/g, 'account');

    // ── Email variants ────────────────────────────────────────────────
    l = l.replace(/\be[-\s]?m[ae][iy]l\b/g, 'email');
    l = l.replace(/\bemeil\b/g,              'email');
    l = l.replace(/\bemail\s*[iy]d\b/g,    'email');
    l = l.replace(/\bemail\s*addr[ae]s{1,2}\b/g, 'email');

    // ── DOB variants ─────────────────────────────────────────────────
    l = l.replace(/\bdate\s*of\s*br[iy]th\b/g,     'date of birth');
    l = l.replace(/\bdate\s*of\s*birt?h?\b/g,      'date of birth');
    l = l.replace(/\bd\.?o\.?b\.?\b/g,            'date of birth');
    l = l.replace(/\bbirth\s*d[ae]te\b/g,           'date of birth');
    l = l.replace(/\bbirthd[ae]y\b/g,                'date of birth');
    l = l.replace(/\bjanm\s*(tithi|date)?\b/g,      'date of birth');

    // ── Name variants ─────────────────────────────────────────────────
    l = l.replace(/\bf[au]ll\s*n[ae]m[ae]\b/g,      'full name');
    l = l.replace(/\bappl?ic[ae]nt\s*n[ae]m[ae]\b/g,'applicant name');
    l = l.replace(/\bfather[\s']*s?\s*n[ae]m[ae]\b/g,"father's name");
    l = l.replace(/\bpita\s*(ka\s*)?n[ae]am?\b/g,  "father's name");
    l = l.replace(/\bmother[\s']*s?\s*n[ae]m[ae]\b/g,"mother's name");
    l = l.replace(/\bmata\s*(ka\s*)?n[ae]am?\b/g,  "mother's name");
    l = l.replace(/\bn[ae]am?\b/g,                   'name');

    // ── Address variants ──────────────────────────────────────────────
    l = l.replace(/\bperm[ae]n[ae]nt\s*addr[ae]s{1,2}\b/g, 'permanent address');
    l = l.replace(/\bpres[ae]nt\s*addr[ae]s{1,2}\b/g,      'present address');
    l = l.replace(/\baddr[ae]s{1,2}\b/g,  'address');
    l = l.replace(/\bpata\b/g,            'address');

    // ── Pincode variants ──────────────────────────────────────────────
    l = l.replace(/\bpin\s*c[ao]de\b/g,     'pin code');
    l = l.replace(/\bpinc[ao]de\b/g,         'pin code');
    l = l.replace(/\bpost[ae]l\s*(c[ao]de)?\b/g, 'pin code');
    l = l.replace(/\bzip\s*(c[ao]de)?\b/g,  'pin code');

    // ── Other ─────────────────────────────────────────────────────────
    l = l.replace(/\bs[ae]x\b/g,              'gender');
    l = l.replace(/\blingen\b/g,              'gender');
    l = l.replace(/\bc[ae]t[ae]g[ao]ry\b/g,  'category');
    l = l.replace(/\bjati\b/g,                'caste');
    l = l.replace(/\b[ae]nn?u[ae]l\s*[iy]nc[ao]me\b/g, 'annual income');
    l = l.replace(/\binc[ao]me\b/g,           'income');
    l = l.replace(/\bb[ae]nk\s*n[ae]m[ae]\b/g, 'bank name');
    l = l.replace(/\bblood\s*gr[ao]up\b/g,  'blood group');
    l = l.replace(/\bblood\s*typ[ae]\b/g,   'blood group');
    l = l.replace(/\bjila\b/g,               'district');

    return l;
  }


  function runIframeMode() {
    let updateTimer = null;

    const IS_GOOGLE_FORMS = /docs\.google\.com\/forms/i.test(window.location.href) ||
                            /docs\.google\.com\/forms/i.test(document.referrer);

    function getAllInputs() {
      if (IS_GOOGLE_FORMS) return getAllInputsGoogleForms();
      const nodes = document.querySelectorAll(
        'input:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([type="image"]):not([type="reset"]), select, textarea'
      );
      return Array.from(nodes).filter(el => {
        const s = window.getComputedStyle(el);
        return s.display !== 'none' && s.visibility !== 'hidden' && el.offsetParent !== null;
      });
    }

    function isFieldFilled(input) {
      if (IS_GOOGLE_FORMS) return isFieldFilledGF(input);
      const v = (input.value || '').trim();
      if (!v) return false;
      return !/^(select\s*(an?\s*)?option[:\s]*|--\s*select\s*--|choose\s*(an?\s*)?option|please\s*select)$/i.test(v);
    }

    // ── SMART VALIDATION ─────────────────────────────────────
    // Detects form type from URL/title and (for Google Forms) body text
    function getFormType() {
      const url = (window.location.href + ' ' + document.title).toLowerCase();
      if (url.includes('pension') || url.includes('old age') || url.includes('vridha'))   return 'pension';
      if (url.includes('scholarship') || url.includes('chatravritti'))                    return 'scholarship';
      if (url.includes('ration') || url.includes('ration card'))                          return 'ration';
      if (url.includes('driving') || url.includes('licence') || url.includes('license'))  return 'driving_license';
      if (url.includes('birth') || url.includes('janm'))                                  return 'birth_certificate';
      if (url.includes('income') || url.includes('aay'))                                  return 'income_certificate';
      if (url.includes('caste') || url.includes('jati'))                                  return 'caste_certificate';
      if (url.includes('domicile') || url.includes('niwas') || url.includes('residence')) return 'domicile';
      if (url.includes('aadhar') || url.includes('aadhaar'))                              return 'aadhaar';
      // For Google Forms, URL has no form-type keywords — scan visible body text instead
      if (IS_GOOGLE_FORMS) return detectGoogleFormType();
      return 'general';
    }

    // Rules per form type: required field keywords and their specific validations
    const FORM_RULES = {
      pension: {
        label: 'Old Age Pension',
        requiredFields: ['age', 'name', 'address', 'bank', 'aadhar'],
        ageMin: 60,
        ageMax: null,
        incomeMax: 100000,
        needsAadhaar: true,
        needsBankDetails: true,
        tips: [
          'Age must be 60 or above for pension eligibility',
          'Annual income should be below ₹1,00,000',
          'Aadhaar card is mandatory',
          'Bank account details required for DBT'
        ]
      },
      scholarship: {
        label: 'Scholarship',
        requiredFields: ['name', 'age', 'school', 'marks', 'income'],
        ageMin: 5,
        ageMax: 30,
        incomeMax: 250000,
        needsAadhaar: true,
        tips: [
          'Annual family income must be below ₹2,50,000',
          'Valid school/college enrollment certificate required',
          'Aadhaar card is mandatory',
          'Previous year marksheet required'
        ]
      },
      ration: {
        label: 'Ration Card',
        requiredFields: ['name', 'address', 'family', 'income'],
        incomeMax: 120000,
        needsAadhaar: true,
        tips: [
          'All family member details required',
          'Aadhaar linking is mandatory for all members',
          'Address proof required',
          'Income certificate required'
        ]
      },
      driving_license: {
        label: 'Driving License',
        requiredFields: ['name', 'age', 'address', 'blood'],
        ageMin: 18,
        ageMax: null,
        tips: [
          'Age must be 18 or above',
          'Valid address proof required',
          'Medical certificate may be required',
          'Learner\'s license required before permanent license'
        ]
      },
      birth_certificate: {
        label: 'Birth Certificate',
        requiredFields: ['name', 'date', 'hospital', 'parent'],
        tips: [
          'Hospital/place of birth details required',
          'Parent\'s Aadhaar required',
          'Application should be within 21 days of birth for free registration'
        ]
      },
      income_certificate: {
        label: 'Income Certificate',
        requiredFields: ['name', 'address', 'income', 'occupation'],
        needsAadhaar: true,
        tips: [
          'Aadhaar card is mandatory',
          'Self-declaration of income required',
          'Valid address proof required',
          'Occupation details required'
        ]
      },
      caste_certificate: {
        label: 'Caste Certificate',
        requiredFields: ['name', 'caste', 'address', 'parent'],
        needsAadhaar: true,
        tips: [
          'Aadhaar card is mandatory',
          'Father/Mother\'s caste certificate may be required',
          'Address proof required',
          'School certificate as proof of caste'
        ]
      },
      domicile: {
        label: 'Domicile/Residence Certificate',
        requiredFields: ['name', 'address', 'duration'],
        needsAadhaar: true,
        tips: [
          'Minimum 15 years of residence proof required',
          'Aadhaar card is mandatory',
          'Utility bills as address proof'
        ]
      },
      aadhaar: {
        label: 'Aadhaar Card',
        requiredFields: ['name', 'dob', 'address', 'mobile'],
        tips: [
          'Original documents required for verification',
          'Mobile number mandatory for OTP',
          'Address proof must match current address'
        ]
      },
      general: {
        label: 'General Form',
        requiredFields: [],
        tips: []
      }
    };

    // ── GOOGLE FORMS LABEL EXTRACTION ───────────────────────
    // Google Forms renders labels in nearby <div> / <span> elements,
    // NOT as input[name], input[placeholder], or aria-label.
    // This function walks up the DOM to find the closest visible question text.
    function getNearbyLabel(input) {
      // 1. Standard attributes first (aria-label is most reliable)
      const ariaLabel = input.getAttribute('aria-label') || '';
      if (ariaLabel.trim()) return ariaLabel.toLowerCase();

      const ariaLabelledBy = input.getAttribute('aria-labelledby') || '';
      if (ariaLabelledBy) {
        const labelEl = document.getElementById(ariaLabelledBy);
        if (labelEl && labelEl.textContent.trim()) return labelEl.textContent.toLowerCase();
      }

      const direct = (input.name || input.id || input.placeholder || '').toLowerCase();
      if (direct) return direct;

      // 2. Walk up the DOM tree (up to 12 levels) looking for a label-like element
      let el = input.parentElement;
      for (let i = 0; i < 12 && el; i++) {
        // Explicit <label> linked by for=""
        if (input.id) {
          const linked = document.querySelector(`label[for="${CSS.escape(input.id)}"]`);
          if (linked) return linked.textContent.toLowerCase();
        }

        // Google Forms (2024-2025): question text lives in specific elements.
        // Multiple selector patterns because Google changes class names frequently.
        const gFormSelectors = [
          '[role="heading"]',
          // New Google Forms class patterns
          '[class*="freebirdFormviewerComponentsQuestionBaseHeader"]',
          '[class*="freebirdFormviewerViewItemsItemItemTitle"]',
          '[class*="exportLabel"]',
          '[class*="questionTitle"]',
          // Older patterns kept as fallback
          '.freebirdFormviewerComponentsQuestionBaseTitle',
          '.freebirdFormviewerViewItemsItemItemTitle',
        ];
        for (const sel of gFormSelectors) {
          const heading = el.querySelector(sel);
          if (heading && heading.textContent.trim()) {
            return heading.textContent.toLowerCase();
          }
        }

        // Fallback: any <label> inside this ancestor
        const lbl = el.querySelector('label');
        if (lbl && lbl.textContent.trim()) return lbl.textContent.toLowerCase();

        // Check preceding sibling text nodes / spans that look like labels
        const prev = el.previousElementSibling;
        if (prev && prev.textContent.trim() &&
            (prev.tagName === 'LABEL' || /label|question|title|heading/i.test(prev.className + ' ' + (prev.getAttribute('role') || '')))) {
          return prev.textContent.toLowerCase();
        }

        el = el.parentElement;
      }

      // 3. Last resort: walk up until we find ANY meaningful text near the input
      el = input.parentElement;
      for (let i = 0; i < 6 && el; i++) {
        const text = (el.textContent || '').trim().toLowerCase();
        // Only use short text blocks that look like labels (not entire form sections)
        if (text && text.length < 120 && text.length > 2) {
          return text;
        }
        el = el.parentElement;
      }

      return '';
    }

    // ── GOOGLE FORMS INPUT DISCOVERY ────────────────────────
    // Google Forms uses <input> for short answers BUT <div contenteditable="true">
    // or <textarea> for paragraph questions. We must collect all of these.
    function getAllInputsGoogleForms() {
      const standard = Array.from(document.querySelectorAll(
        'input:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([type="image"]):not([type="reset"]), select, textarea'
      ));
      // Google Forms short-answer: <div role="listitem"> > <div contenteditable="true">
      const contentEditable = Array.from(document.querySelectorAll('[contenteditable="true"]'));
      const all = [...standard, ...contentEditable];
      return all.filter(el => {
        const s = window.getComputedStyle(el);
        return s.display !== 'none' && s.visibility !== 'hidden' && el.offsetParent !== null;
      });
    }

    // ── GOOGLE FORMS TYPE DETECTION ─────────────────────────
    // Google Form URLs don't include form-type keywords.
    // Instead, we scan the visible question text to infer the form context.
    function detectGoogleFormType() {
      const allText = document.body.innerText.toLowerCase();
      if (allText.includes('pension') || allText.includes('वृद्धा') || allText.includes('old age')) return 'pension';
      if (allText.includes('scholarship') || allText.includes('छात्रवृत्ति')) return 'scholarship';
      if (allText.includes('ration card') || allText.includes('राशन')) return 'ration';
      if (allText.includes('driving') || allText.includes('licence') || allText.includes('license')) return 'driving_license';
      if (allText.includes('birth certificate') || allText.includes('जन्म प्रमाण')) return 'birth_certificate';
      if (allText.includes('income certificate') || allText.includes('आय प्रमाण')) return 'income_certificate';
      if (allText.includes('caste certificate') || allText.includes('जाति प्रमाण')) return 'caste_certificate';
      if (allText.includes('domicile') || allText.includes('निवास प्रमाण')) return 'domicile';
      if (allText.includes('aadhaar') || allText.includes('aadhar') || allText.includes('आधार')) return 'aadhaar';
      return 'general';
    }

    // ── VALUE ACCESSOR (handles both input and contenteditable) ─
    function getInputValue(input) {
      if (input.isContentEditable || input.contentEditable === 'true') {
        return input.innerText || '';
      }
      return input.value || '';
    }

    function isFieldFilledGF(input) {
      const v = getInputValue(input).trim();
      if (!v) return false;
      return !/^(select\s*(an?\s*)?option[:\s]*|--\s*select\s*--|choose\s*(an?\s*)?option|please\s*select)$/i.test(v);
    }

    function validateAllFields(inputs, formType) {
      const errors = [];
      const warnings = [];
      const rules = FORM_RULES[formType] || FORM_RULES.general;

      // Extract values from all filled fields
      // IMPORTANT: use getNearbyLabel() so Google Forms question text is detected
      const fieldValues = {};
      inputs.forEach(input => {
        if (!isFieldFilled(input)) return;
        const label = getNearbyLabel(input);   // ← rich label from DOM
        const type  = (input.type || '').toLowerCase();
        const value = IS_GOOGLE_FORMS ? getInputValue(input).trim() : input.value.trim();

        // ── Classify field by label + type ───────────────────
        // IMPORTANT: use EXPLICIT keywords only. Never use generic "number" alone
        // because "Account Number", "IFSC", "Aadhaar Number" all contain "number".

        // Fields that MUST NOT be mis-classified as phone
        const normLabel = fuzzyLabel(label);
        const isAccountNumber = normLabel.includes('account') || normLabel.includes('खाता');
        const isIFSC    = normLabel.includes('ifsc') || normLabel.includes('आईएफएससी');
        const isAadhaar = normLabel.includes('aadhaar') || normLabel.includes('uid number') || normLabel.includes('आधार');
        const isPAN     = (normLabel.includes('pan card') || normLabel.includes('pan no') || normLabel.includes('pan number') || normLabel.includes(' pan '))
                          && !normLabel.includes('panchayat');
        const isPincode = normLabel.includes('pin code') || normLabel.includes('pincode')
                          || normLabel.includes('postal code') || normLabel.includes('zip code')
                          || normLabel.includes('पिन कोड')
                          // bare "pin" only if NOT aadhaar/account context
                          || (label === 'pin' || label.endsWith(' pin'));

        // Phone: use normLabel so ph.no / mob.no / phn etc. all match
        const isPhone   = type === 'tel'
                          || normLabel.includes('phone')
                          || normLabel.includes('mobile')
                          || normLabel.includes('फ़ोन')
                          || normLabel.includes('फोन')
                          || normLabel.includes('मोबाइल');

        // Email
        const isEmail   = type === 'email'
                          || normLabel.includes('email')
                          || normLabel.includes('ईमेल');

        const isDate    = type === 'date'
                          || normLabel.includes('date of birth')
                          || normLabel.includes('birth date')
                          || normLabel.includes('dob')
                          || normLabel.includes('जन्म तिथि')
                          || normLabel.includes('जन्म');
        const isAge     = normLabel.includes('age') || normLabel.includes('उम्र') || normLabel.includes('आयु');
        const isIncome  = normLabel.includes('income') || normLabel.includes('आय');

        // ── Store cross-field values ──────────────────────────
        if (isAge)     fieldValues.age    = parseInt(value);
        if (isIncome)  fieldValues.income = parseInt(value.replace(/[^0-9]/g, ''));
        if (isEmail)   fieldValues.email  = value;
        if (isAadhaar) fieldValues.aadhaar = value;
        if (isPhone)   fieldValues.phone  = value;

        // ── Per-field format validations ──────────────────────

        // Email
        if (isEmail) {
          if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value)) {
            errors.push({ field: 'Email', message: 'Invalid email format (e.g. name@gmail.com)' });
          }
        }

        // Phone / Mobile — only if NOT an account/aadhaar/ifsc field
        if (isPhone && !isAccountNumber && !isAadhaar && !isIFSC) {
          const digits = value.replace(/[^0-9]/g, '');
          if (!/^[6-9]\d{9}$/.test(digits)) {
            errors.push({
              field: 'Mobile Number',
              message: `"${value}" is not a valid Indian mobile number. Must be 10 digits starting with 6, 7, 8, or 9.`
            });
          }
        }

        // Aadhaar — must be exactly 12 digits
        if (isAadhaar) {
          const clean = value.replace(/[\s-]/g, '');
          if (!/^\d{12}$/.test(clean)) {
            errors.push({ field: 'Aadhaar Number', message: `"${value}" is not a valid Aadhaar. Must be 12 digits in format: 2345 6789 0123 (you entered ${clean.length} digit(s))` });
          }
        }

        // Bank Account Number — must be 9 to 18 digits only
        if (isAccountNumber && !isAadhaar && !isIFSC) {
          const digits = value.replace(/[\s-]/g, '');
          if (!/^\d{9,18}$/.test(digits)) {
            errors.push({ field: 'Account Number', message: 'Bank account number must be 9–18 digits (numbers only)' });
          }
        }

        // IFSC Code — must be 11 chars: 4 letters, 0, 6 alphanumeric
        if (isIFSC) {
          if (!/^[A-Z]{4}0[A-Z0-9]{6}$/i.test(value.trim())) {
            errors.push({ field: 'IFSC Code', message: 'IFSC must be 11 characters (e.g. SBIN0001234)' });
          }
        }

        // PAN
        if (isPAN) {
          if (!/^[A-Z]{5}\d{4}[A-Z]$/.test(value.toUpperCase())) {
            errors.push({ field: 'PAN', message: 'PAN format: ABCDE1234F (5 letters, 4 digits, 1 letter)' });
          }
        }

        // Pincode — exactly 6 digits
        if (isPincode && !isAccountNumber && !isAadhaar) {
          if (!/^\d{6}$/.test(value.replace(/\s/g, ''))) {
            errors.push({ field: 'Pincode', message: 'Pincode must be exactly 6 digits' });
          }
        }

        // Date of birth — must not be in the future
        if (isDate && value) {
          // Parse various date formats: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD
          let dob = null;
          const v = value.trim();
          // Try DD/MM/YYYY or D/M/YYYY
          const dmyMatch = v.match(/^(\d{1,2})[\/-](\d{1,2})[\/-](\d{2,4})$/);
          if (dmyMatch) {
            let [_, d, m, y] = dmyMatch;
            if (y.length === 2) y = '19' + y;
            dob = new Date(parseInt(y), parseInt(m) - 1, parseInt(d));
          } else {
            dob = new Date(v);
          }
          if (dob && !isNaN(dob)) {
            if (dob > new Date()) {
              errors.push({ field: 'Date of Birth', message: 'Date of birth cannot be in the future' });
            } else {
              const today = new Date();
              let age = today.getFullYear() - dob.getFullYear();
              const m = today.getMonth() - dob.getMonth();
              if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) age--;
              fieldValues.age = age;
              infos.push({ field: 'Date of Birth', message: `Age calculated: ${age} years old` });
            }
          }
        }
      });

      // ── Cross-field / form-type rules ─────────────────────

      // AGE RULES
      if (fieldValues.age !== undefined) {
        const age = fieldValues.age;
        if (rules.ageMin && age < rules.ageMin) {
          errors.push({
            field: 'Age',
            message: `Age must be at least ${rules.ageMin} years for ${rules.label}`
          });
        }
        if (rules.ageMax && age > rules.ageMax) {
          errors.push({
            field: 'Age',
            message: `Age must be ${rules.ageMax} years or below for ${rules.label}`
          });
        }
        if (age < 0 || age > 120) {
          errors.push({ field: 'Age', message: 'Please enter a valid age (0–120)' });
        }
      }

      // INCOME RULES
      if (fieldValues.income !== undefined && rules.incomeMax) {
        if (fieldValues.income > rules.incomeMax) {
          warnings.push({
            field: 'Income',
            message: `Income above ₹${rules.incomeMax.toLocaleString('en-IN')} may make you ineligible for ${rules.label}`
          });
        }
      }

      // AADHAAR REQUIRED
      if (rules.needsAadhaar && !fieldValues.aadhaar) {
        warnings.push({
          field: 'Aadhaar',
          message: `Aadhaar number is mandatory for ${rules.label}`
        });
      }

      // BANK DETAILS REQUIRED (pension/DBT schemes)
      if (rules.needsBankDetails) {
        const inputs_lower = inputs.map(i => getNearbyLabel(i)).join(' ');
        const hasBankField = inputs_lower.includes('bank') || inputs_lower.includes('account') || inputs_lower.includes('ifsc');
        if (!hasBankField) {
          warnings.push({
            field: 'Bank Details',
            message: `Bank account details are required for ${rules.label} (direct benefit transfer)`
          });
        }
      }

      return { errors, warnings };
    }

    function sendFieldDataToParent() {
      const inputs = getAllInputs();
      const total = inputs.length;
      const filled = inputs.filter(isFieldFilled).length;
      const formType = getFormType();
      const { errors, warnings } = validateAllFields(inputs, formType);

      window.parent.postMessage({
        type: 'SAHAYAK_FIELD_DATA',
        total,
        filled,
        errors,
        warnings,
        formType,
        formLabel: (FORM_RULES[formType] || FORM_RULES.general).label,
        tips: (FORM_RULES[formType] || FORM_RULES.general).tips || []
      }, '*');
    }

    function scheduleUpdate() {
      clearTimeout(updateTimer);
      updateTimer = setTimeout(sendFieldDataToParent, 300);
    }

    function attachListeners() {
      getAllInputs().forEach(input => {
        if (!input._sahayakWatched) {
          input._sahayakWatched = true;
          input.addEventListener('input', scheduleUpdate);
          input.addEventListener('change', scheduleUpdate);
          // contenteditable divs (Google Forms) fire 'input' but not 'change'
          if (input.isContentEditable || input.contentEditable === 'true') {
            input.addEventListener('blur', scheduleUpdate);
          }
        }
      });
    }

    const observer = new MutationObserver(() => {
      attachListeners();
      scheduleUpdate();
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // Initial send after page loads
    setTimeout(() => {
      attachListeners();
      sendFieldDataToParent();
    }, 1500);

    // Heartbeat every 4 seconds — keeps parent in sync when user is idle
    setInterval(sendFieldDataToParent, 4000);
  }


  // ============================================================
  // PARENT MODE — runs on the main page, shows the UI panel
  // ============================================================
  function runParentMode() {
    let assistantWidget = null;
    let formData = {
      errors: [],
      warnings: [],
      tips: [],
      formType: 'general',
      formLabel: 'General Form',
      acceptanceScore: 0,
      filledFieldsCount: 0,
      totalFieldsCount: 0
    };

    let recognition = null;
    let isListening = false;
    let currentLanguage = 'en-US';
    let conversationHistory = [];
    let formInputs = [];
    let updateTimer = null;

    // ── STABLE iframe state tracking ────────────────────────
    // FIX: We never reset to 0. Once iframe data arrives, we trust it.
    // The stale guard only kicks in after 30 seconds of complete silence
    // (not 5s which caused the flicker).
    let iframeActive = false;
    let lastIframeTime = 0;

    window.addEventListener('message', (event) => {
      if (event.data && event.data.type === 'SAHAYAK_FIELD_DATA') {
        iframeActive = true;
        lastIframeTime = Date.now();

        // Only update if data is MEANINGFUL (has actual fields)
        // This prevents a 0-field heartbeat from wiping real data
        const incomingTotal = event.data.total || 0;
        const currentTotal = formData.totalFieldsCount;

        if (incomingTotal > 0 || currentTotal === 0) {
          formData.totalFieldsCount = incomingTotal;
          formData.filledFieldsCount = event.data.filled || 0;
          formData.errors = event.data.errors || [];
          formData.warnings = event.data.warnings || [];
          formData.formType = event.data.formType || 'general';
          formData.formLabel = event.data.formLabel || 'General Form';
          formData.tips = event.data.tips || [];
          calculateAcceptanceScore();
          if (assistantWidget) updateAssistantUI();
        }
      }
    });

    // Stale guard: only fall back after 30 seconds of silence
    setInterval(() => {
      if (iframeActive && Date.now() - lastIframeTime > 30000) {
        console.log('[Sahayak] iframe silent >30s, switching to page scan');
        iframeActive = false;
        watchPageFields();
      }
    }, 10000);

    function init() {
      checkBackendConnection();
      injectAssistantButton();

      setTimeout(() => {
        if (!iframeActive) watchPageFields();
        initializeVoiceRecognition();
        loadConversationHistory();
      }, 3000);
    }

    async function checkBackendConnection() {
      try {
        await fetch(`${API_URL}/api/health`);
      } catch (e) { /* silent */ }
    }

    // ── BUTTON ───────────────────────────────────────────────
    function injectAssistantButton() {
      if (document.getElementById('sahayak-button')) return;
      const button = document.createElement('div');
      button.id = 'sahayak-button';
      button.innerHTML = `
        <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
          <circle cx="20" cy="20" r="18" fill="#4F46E5" stroke="white" stroke-width="2"/>
          <path d="M15 16C15 15.4477 15.4477 15 16 15H24C24.5523 15 25 15.4477 25 16V18C25 18.5523 24.5523 19 24 19H16C15.4477 19 15 18.5523 15 18V16Z" fill="white"/>
          <circle cx="17" cy="24" r="1.5" fill="white"/>
          <circle cx="23" cy="24" r="1.5" fill="white"/>
          <path d="M17 27C17 27 18.5 28.5 20 28.5C21.5 28.5 23 27 23 27" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <div class="pulse-ring"></div>
      `;
      button.title = 'Sahayak AI Assistant';
      button.addEventListener('click', toggleAssistant);
      document.body.appendChild(button);
    }

    function toggleAssistant() {
      if (assistantWidget) {
        assistantWidget.remove();
        assistantWidget = null;
      } else {
        showAssistant();
      }
    }

    function showAssistant() {
      const panel = document.createElement('div');
      panel.id = 'sahayak-panel';
      panel.innerHTML = `
        <div class="sahayak-header">
          <div class="sahayak-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" fill="#4F46E5"/>
              <path d="M9 10C9 9.44772 9.44772 9 10 9H14C14.5523 9 15 9.44772 15 10V11C15 11.5523 14.5523 12 14 12H10C9.44772 12 9 11.5523 9 11V10Z" fill="white"/>
              <circle cx="10.5" cy="14.5" r="1" fill="white"/>
              <circle cx="13.5" cy="14.5" r="1" fill="white"/>
            </svg>
            <span>Sahayak AI</span>
          </div>
          <div class="header-controls">
            <select id="language-selector" class="language-select">
              <option value="en-US">English</option>
              <option value="hi-IN">&#2361;&#2367;&#2344;&#2381;&#2342;&#2368;</option>
            </select>
            <button class="close-btn" id="sahayak-close">&#215;</button>
          </div>
        </div>
        <div class="sahayak-body">
          <div id="form-type-badge" class="form-type-badge" style="display:none;"></div>
          <div class="acceptance-gauge">
            <svg viewBox="0 0 200 120" class="gauge-svg">
              <defs>
                <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" style="stop-color:#EF4444;stop-opacity:1"/>
                  <stop offset="50%" style="stop-color:#F59E0B;stop-opacity:1"/>
                  <stop offset="100%" style="stop-color:#10B981;stop-opacity:1"/>
                </linearGradient>
              </defs>
              <path d="M 20 100 A 80 80 0 0 1 180 100" stroke="#E5E7EB" stroke-width="20" fill="none"/>
              <path id="gauge-fill" d="M 20 100 A 80 80 0 0 1 180 100" stroke="url(#gaugeGradient)" stroke-width="20" fill="none" stroke-dasharray="251.2" stroke-dashoffset="251.2"/>
              <!-- Needle as a group rotated around pivot point (100,100) -->
              <g id="gauge-needle-group" transform="rotate(-90, 100, 100)">
                <line x1="100" y1="100" x2="100" y2="28" stroke="#1F2937" stroke-width="3" stroke-linecap="round"/>
                <circle cx="100" cy="100" r="5" fill="#1F2937"/>
                <circle cx="100" cy="100" r="3" fill="white"/>
              </g>
            </svg>
            <div class="gauge-value">
              <div class="score" id="acceptance-score">0%</div>
              <div class="score-label">Acceptance Score</div>
            </div>
          </div>
          <div class="recommendation" id="recommendation">
            <div class="loading-state">
              <div class="spinner"></div>
              <p>Analyzing form...</p>
            </div>
          </div>
          <!-- ══ DOCUMENT UPLOAD & AUTO-FILL SECTION ══ -->
          <div class="doc-upload-section" id="doc-upload-section">
            <div class="doc-upload-header">
              <span class="doc-upload-icon">📂</span>
              <div>
                <div class="doc-upload-title">Upload Documents to Auto-Fill</div>
                <div class="doc-upload-subtitle">Aadhaar, PAN, Marksheet, Passbook, etc.</div>
              </div>
            </div>

            <label class="doc-drop-zone" id="doc-drop-zone" for="doc-file-input">
              <input type="file" id="doc-file-input" multiple accept=".pdf,.jpg,.jpeg,.png,.gif,.bmp,.webp,.doc,.docx,.txt" style="display:none;" />
              <div class="drop-zone-icon">⬆️</div>
              <div class="drop-zone-text">Drop files here or <span class="drop-zone-link">click to browse</span></div>
              <div class="drop-zone-hint">PDF · Image · Word · Multiple files supported</div>
            </label>

            <div id="doc-file-list" class="doc-file-list" style="display:none;"></div>

            <button class="doc-extract-btn" id="doc-extract-btn" style="display:none;">
              <span id="doc-extract-btn-text">✨ Extract & Auto-Fill Form</span>
            </button>

            <div class="doc-progress" id="doc-progress" style="display:none;">
              <div class="doc-progress-bar"><div class="doc-progress-fill" id="doc-progress-fill"></div></div>
              <div class="doc-progress-text" id="doc-progress-text">Reading documents with AI...</div>
            </div>

            <div class="doc-result" id="doc-result" style="display:none;"></div>
          </div>
          <!-- ══════════════════════════════════════════ -->

          <div class="issues-section" id="issues-section" style="display:none;">
            <h3>&#9888;&#65039; Issues Found</h3>
            <div id="issues-list"></div>
          </div>
          <div class="suggestions-section" id="suggestions-section" style="display:none;">
            <h3>&#128161; Suggestions</h3>
            <div id="suggestions-list"></div>
          </div>
          <div class="tips-section" id="tips-section" style="display:none;">
            <h3>&#128203; Form Requirements</h3>
            <div id="tips-list"></div>
          </div>
          <div class="chat-section">
            <div class="chat-messages" id="chat-messages">
              <div class="message bot-message">
                <div class="message-avatar">S</div>
                <div class="message-content">Hi! I'm Sahayak AI. I can check your form and guide you on government schemes!</div>
              </div>
            </div>
            <!-- Voice language selector -->
            <div class="voice-lang-bar">
              <span class="voice-lang-label">🎙️ Voice Language:</span>
              <button class="voice-lang-btn active" id="vlang-en" data-lang="en-IN">🇬🇧 English</button>
              <button class="voice-lang-btn" id="vlang-hi" data-lang="hi-IN">🇮🇳 Hindi</button>
            </div>

            <!-- TTS playback controls — shown while bot is speaking -->
            <div id="tts-controls" class="tts-controls" style="display:none;">
              <span class="tts-status" id="tts-status">🔊 Speaking...</span>
              <button id="tts-pause-btn" class="tts-btn" title="Pause / Resume">⏸ Pause</button>
              <button id="tts-stop-btn" class="tts-btn tts-stop" title="Stop reading">⏹ Stop</button>
            </div>

            <!-- Live transcript while speaking -->
            <div id="voice-transcript" class="voice-transcript" style="display:none;">
              <div class="transcript-text" id="transcript-text">Listening...</div>
            </div>

            <div class="chat-input-container">
              <button id="voice-btn" class="voice-btn" title="Click to speak">
                <svg id="mic-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1-9c0-.55.45-1 1-1s1 .45 1 1v6c0 .55-.45 1-1 1s-1-.45-1-1V5zm6 6c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
                <div class="mic-ripple" id="mic-ripple" style="display:none;"></div>
              </button>
              <input type="text" id="chat-input" placeholder="Type or click 🎙️ to speak..." />
              <button id="chat-send">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M2.003 5.884L18.832 10.5l-16.83 4.616L3.28 11l-1.277-5.116zm1.944 4.584l-.625-2.512L14.678 10.5 3.322 13.044l.625-2.512z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      `;

      document.body.appendChild(panel);
      assistantWidget = panel;

      document.getElementById('sahayak-close').addEventListener('click', toggleAssistant);
      document.getElementById('chat-send').addEventListener('click', sendMessage);
      document.getElementById('chat-input').addEventListener('keypress', e => {
        if (e.key === 'Enter') sendMessage();
      });
      document.getElementById('voice-btn').addEventListener('click', toggleVoice);

      // TTS pause / stop buttons
      document.getElementById('tts-pause-btn').addEventListener('click', toggleTTSPause);
      document.getElementById('tts-stop-btn').addEventListener('click', stopTTS);

      // Voice language buttons
      document.getElementById('vlang-en').addEventListener('click', () => {
        setVoiceLanguage('en-IN');
      });
      document.getElementById('vlang-hi').addEventListener('click', () => {
        setVoiceLanguage('hi-IN');
      });

      // Main language selector still works
      document.getElementById('language-selector').addEventListener('change', e => {
        currentLanguage = e.target.value;
        if (recognition) recognition.lang = currentLanguage;
      });

      restoreConversationHistory();
      initDocUpload();
      setTimeout(() => {
        calculateAcceptanceScore();
        updateAssistantUI();
      }, 400);
    }

    // ── PAGE-LEVEL FIELD DETECTION (fallback, no iframe) ─────
    const IS_GOOGLE_FORMS_PAGE = /docs\.google\.com\/forms/i.test(window.location.href);

    function getAllPageInputs() {
      const nodes = document.querySelectorAll(
        'input:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([type="image"]):not([type="reset"]), select, textarea'
      );
      const standard = Array.from(nodes);
      // Google Forms: also collect contenteditable divs
      const contentEditable = IS_GOOGLE_FORMS_PAGE
        ? Array.from(document.querySelectorAll('[contenteditable="true"]'))
        : [];
      return [...standard, ...contentEditable].filter(el => {
        const s = window.getComputedStyle(el);
        return s.display !== 'none' && s.visibility !== 'hidden' && el.offsetParent !== null;
      });
    }

    function getPageInputValue(input) {
      if (input.isContentEditable || input.contentEditable === 'true') {
        return input.innerText || '';
      }
      return input.value || '';
    }

    function isFieldFilled(input) {
      const v = getPageInputValue(input).trim();
      if (!v) return false;
      return !/^(select\s*(an?\s*)?option[:\s]*|--\s*select\s*--|choose\s*(an?\s*)?option|please\s*select)$/i.test(v);
    }

    function watchPageFields() {
      if (iframeActive) return;
      formInputs = getAllPageInputs();
      formData.totalFieldsCount = formInputs.length;
      formInputs.forEach(input => {
        if (!input._sahayakWatched) {
          input._sahayakWatched = true;
          input.addEventListener('input', schedulePageUpdate);
          input.addEventListener('change', schedulePageUpdate);
          if (input.isContentEditable || input.contentEditable === 'true') {
            input.addEventListener('blur', schedulePageUpdate);
          }
        }
      });
      schedulePageUpdate();
    }

    // ── LABEL DETECTION (parent mode, mirrors iframe getNearbyLabel) ──
    function getPageFieldLabel(input) {
      const ariaLabel = input.getAttribute('aria-label') || '';
      if (ariaLabel.trim()) return ariaLabel.toLowerCase();

      const ariaLabelledBy = input.getAttribute('aria-labelledby') || '';
      if (ariaLabelledBy) {
        const labelEl = document.getElementById(ariaLabelledBy);
        if (labelEl && labelEl.textContent.trim()) return labelEl.textContent.toLowerCase();
      }

      const direct = (input.name || input.id || input.placeholder || '').toLowerCase();
      if (direct) return direct;

      let el = input.parentElement;
      for (let i = 0; i < 12 && el; i++) {
        if (input.id) {
          try {
            const linked = document.querySelector(`label[for="${CSS.escape(input.id)}"]`);
            if (linked) return linked.textContent.toLowerCase();
          } catch(e) {}
        }
        const gFormSelectors = [
          '[role="heading"]',
          '[class*="freebirdFormviewerComponentsQuestionBaseHeader"]',
          '[class*="freebirdFormviewerViewItemsItemItemTitle"]',
          '[class*="exportLabel"]',
          '[class*="questionTitle"]',
          '.freebirdFormviewerComponentsQuestionBaseTitle',
          '.freebirdFormviewerViewItemsItemItemTitle',
        ];
        for (const sel of gFormSelectors) {
          const heading = el.querySelector(sel);
          if (heading && heading.textContent.trim()) return heading.textContent.toLowerCase();
        }
        const lbl = el.querySelector('label');
        if (lbl && lbl.textContent.trim()) return lbl.textContent.toLowerCase();
        const prev = el.previousElementSibling;
        if (prev && prev.textContent.trim() &&
            (prev.tagName === 'LABEL' || /label|question|title|heading/i.test(prev.className + ' ' + (prev.getAttribute('role') || '')))) {
          return prev.textContent.toLowerCase();
        }
        el = el.parentElement;
      }

      // Last resort for Google Forms: use surrounding text
      if (IS_GOOGLE_FORMS_PAGE) {
        el = input.parentElement;
        for (let i = 0; i < 6 && el; i++) {
          const text = (el.textContent || '').trim().toLowerCase();
          if (text && text.length < 120 && text.length > 2) return text;
          el = el.parentElement;
        }
      }

      return '';
    }

    // ── PAGE-MODE VALIDATION (same rules as iframe validateAllFields) ──
    function validatePageFields(inputs) {
      const errors = [];
      const warnings = [];

      inputs.forEach(input => {
        if (!isFieldFilled(input)) return;
        const label = getPageFieldLabel(input);
        const type  = (input.type || '').toLowerCase();
        const value = getPageInputValue(input).trim();

        // ── Classify field by label + type ───────────────────
        // Fields that MUST NOT be mis-classified as phone
        const normLabel = fuzzyLabel(label);
        const isAccountNumber = normLabel.includes('account') || normLabel.includes('खाता');
        const isIFSC    = normLabel.includes('ifsc') || normLabel.includes('आईएफएससी');
        const isAadhaar = normLabel.includes('aadhaar') || normLabel.includes('uid number') || normLabel.includes('आधार');
        const isPAN     = (normLabel.includes('pan card') || normLabel.includes('pan no') || normLabel.includes('pan number') || normLabel.includes(' pan '))
                          && !normLabel.includes('panchayat');
        const isPincode = normLabel.includes('pin code') || normLabel.includes('pincode')
                          || normLabel.includes('postal code') || normLabel.includes('zip code')
                          || normLabel.includes('पिन कोड')
                          || (label === 'pin' || label.endsWith(' pin'));

        // Phone: normLabel handles all variants (ph no, mob no, phn, etc.)
        const isPhone   = type === 'tel'
                          || normLabel.includes('phone')
                          || normLabel.includes('mobile')
                          || normLabel.includes('फ़ोन')
                          || normLabel.includes('फोन')
                          || normLabel.includes('मोबाइल');

        const isEmail   = type === 'email'
                          || normLabel.includes('email')
                          || normLabel.includes('ईमेल');
        const isDate    = type === 'date'
                          || normLabel.includes('date of birth')
                          || normLabel.includes('birth date')
                          || normLabel.includes('dob')
                          || normLabel.includes('जन्म तिथि')
                          || normLabel.includes('जन्म');

        if (isEmail) {
          if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value)) {
            errors.push({ field: 'Email', message: `"${value}" is not a valid email. Must include domain like @gmail.com` });
          }
        }
        if (isPhone && !isAccountNumber && !isAadhaar && !isIFSC) {
          const digits = value.replace(/[^0-9]/g, '');
          if (!/^[6-9]\d{9}$/.test(digits)) {
            errors.push({ field: 'Mobile Number', message: `"${value}" is not valid. Must be 10 digits starting with 6, 7, 8, or 9` });
          }
        }
        if (isAadhaar) {
          if (!/^\d{12}$/.test(value.replace(/[\s-]/g, ''))) {
            errors.push({ field: 'Aadhaar Number', message: `"${value}" is not a valid Aadhaar. Must be 12 digits in format: 2345 6789 0123 (you entered ${clean.length} digit(s))` });
          }
        }
        if (isAccountNumber && !isAadhaar && !isIFSC) {
          const digits = value.replace(/[\s-]/g, '');
          if (!/^\d{9,18}$/.test(digits)) {
            errors.push({ field: 'Account Number', message: 'Bank account number must be 9–18 digits (numbers only)' });
          }
        }
        if (isIFSC) {
          if (!/^[A-Z]{4}0[A-Z0-9]{6}$/i.test(value.trim())) {
            errors.push({ field: 'IFSC Code', message: 'IFSC must be 11 characters (e.g. SBIN0001234)' });
          }
        }
        if (isPAN) {
          if (!/^[A-Z]{5}\d{4}[A-Z]$/.test(value.toUpperCase())) {
            errors.push({ field: 'PAN', message: 'PAN format: ABCDE1234F (5 letters, 4 digits, 1 letter)' });
          }
        }
        if (isPincode && !isAccountNumber && !isAadhaar) {
          if (!/^\d{6}$/.test(value.replace(/\s/g, ''))) {
            errors.push({ field: 'Pincode', message: 'Pincode must be exactly 6 digits' });
          }
        }
        if (isDate && value) {
          if (new Date(value) > new Date()) {
            errors.push({ field: 'Date of Birth', message: 'Date of birth cannot be in the future' });
          }
        }
      });

      return { errors, warnings };
    }

    function schedulePageUpdate() {
      if (iframeActive) return;
      clearTimeout(updateTimer);
      updateTimer = setTimeout(() => {
        if (iframeActive) return;
        formInputs = getAllPageInputs();
        formData.totalFieldsCount = formInputs.length;
        formData.filledFieldsCount = formInputs.filter(isFieldFilled).length;
        // ← Run real validation instead of wiping errors
        const { errors, warnings } = validatePageFields(formInputs);
        formData.errors = errors;
        formData.warnings = warnings;
        calculateAcceptanceScore();
        if (assistantWidget) updateAssistantUI();
      }, 300);
    }

    // ── VOICE ─────────────────────────────────────────────────
    let voiceLanguage = 'en-IN'; // Default voice language

    function setVoiceLanguage(lang) {
      voiceLanguage = lang;
      currentLanguage = lang; // Keep in sync so UI selector reflects voice language
      if (recognition) recognition.lang = lang;

      // Update active button styling
      document.querySelectorAll('.voice-lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
      });

      // Sync the header language selector dropdown
      const selector = document.getElementById('language-selector');
      if (selector) selector.value = lang;

      // Show confirmation
      const label = lang === 'hi-IN' ? 'हिंदी में बोलें 🎙️' : 'Speak in English 🎙️';
      const inp = document.getElementById('chat-input');
      if (inp) inp.placeholder = label;
    }

    function initializeVoiceRecognition() {
      const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
      if (!SpeechRecognition) {
        console.warn('Speech Recognition not supported');
        return;
      }

      recognition = new SpeechRecognition();
      recognition.continuous = false;       // Single utterance
      recognition.interimResults = true;    // Show live transcript while speaking
      recognition.maxAlternatives = 1;
      recognition.lang = voiceLanguage;

      // Called repeatedly while user is speaking — shows live transcript
      recognition.onresult = (e) => {
        let interimText = '';
        let finalText = '';

        for (let i = e.resultIndex; i < e.results.length; i++) {
          const transcript = e.results[i][0].transcript;
          if (e.results[i].isFinal) {
            finalText += transcript;
          } else {
            interimText += transcript;
          }
        }

        // Show live transcript
        const transcriptDiv = document.getElementById('transcript-text');
        if (transcriptDiv) {
          transcriptDiv.textContent = finalText || interimText || 'Listening...';
          transcriptDiv.style.opacity = finalText ? '1' : '0.6';
        }

        // When final result comes in — put in input and send
        if (finalText) {
          const inp = document.getElementById('chat-input');
          if (inp) inp.value = finalText;

          // Brief pause so user can see what was heard, then send
          setTimeout(() => {
            stopListening();
            sendMessage();
          }, 600);
        }
      };

      recognition.onerror = (e) => {
        console.warn('Voice error:', e.error);
        stopListening();
        const messages = {
          'no-speech':        'No speech detected. Try again.',
          'audio-capture':    'Microphone not found. Check permissions.',
          'not-allowed':      'Microphone permission denied. Allow mic in browser settings.',
          'network':          'Network error during voice recognition.',
          'aborted':          'Voice input cancelled.'
        };
        const msg = messages[e.error] || 'Voice error: ' + e.error;
        addChatMessage('⚠️ ' + msg, 'bot');
      };

      recognition.onend = () => {
        stopListening();
      };
    }

    function startListening() {
      if (!recognition) {
        addChatMessage('⚠️ Voice not supported in this browser. Please use Chrome.', 'bot');
        return;
      }
      isListening = true;
      recognition.lang = voiceLanguage;

      try {
        recognition.start();
      } catch(e) {
        // Already started — stop and restart
        recognition.stop();
        setTimeout(() => { recognition.start(); }, 200);
      }

      // Show UI feedback
      const btn = document.getElementById('voice-btn');
      const ripple = document.getElementById('mic-ripple');
      const transcriptBox = document.getElementById('voice-transcript');
      const transcriptText = document.getElementById('transcript-text');
      const inp = document.getElementById('chat-input');

      if (btn) btn.classList.add('listening');
      if (ripple) ripple.style.display = 'block';
      if (transcriptBox) transcriptBox.style.display = 'flex';
      if (transcriptText) transcriptText.textContent = voiceLanguage === 'hi-IN' ? 'सुन रहा हूँ...' : 'Listening...';
      if (inp) inp.placeholder = voiceLanguage === 'hi-IN' ? 'बोलिए...' : 'Speak now...';
      if (inp) inp.value = '';
    }

    function stopListening() {
      isListening = false;
      try { if (recognition) recognition.stop(); } catch(e) {}

      // Hide UI feedback
      const btn = document.getElementById('voice-btn');
      const ripple = document.getElementById('mic-ripple');
      const transcriptBox = document.getElementById('voice-transcript');
      const inp = document.getElementById('chat-input');

      if (btn) btn.classList.remove('listening');
      if (ripple) ripple.style.display = 'none';
      if (transcriptBox) setTimeout(() => { transcriptBox.style.display = 'none'; }, 800);

      const placeholder = voiceLanguage === 'hi-IN' ? 'हिंदी में बोलें 🎙️' : 'Type or click 🎙️ to speak...';
      if (inp && !inp.value) inp.placeholder = placeholder;
    }

    function toggleVoice() {
      if (isListening) {
        stopListening();
      } else {
        startListening();
      }
    }

    function updateVoiceButton() {
      // Kept for compatibility — actual update handled in start/stopListening
    }

    // ── SMART CHAT RESPONSES ──────────────────────────────────
    // Full conversation memory — stores all messages for context
    let chatMessages = [];

    async function sendMessage() {
      const input = document.getElementById('chat-input');
      const rawMessage = input.value.trim();
      if (!rawMessage) return;

      // Normalize spelling in user message (fuzzy understand ph no, adhar, etc.)
      const fuzzy = window._sahayakFuzzy || (s => s);
      const message = fuzzy(rawMessage);

      // Show original message to user but send normalized to AI
      addChatMessage(rawMessage, 'user');
      input.value = '';

      // Add normalized version to memory for better AI understanding
      chatMessages.push({ role: 'user', content: message });

      // Show typing indicator
      const typingId = showTyping();

      try {
        // Call YOUR Python backend (localhost:5000) which uses Gemini
        const response = await fetch(`${API_URL}/api/ai-chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: message,
            context: {
              formType: formData.formType,
              formLabel: formData.formLabel,
              errors: formData.errors,
              warnings: formData.warnings,
              filled: formData.filledFieldsCount,
              total: formData.totalFieldsCount,
              language: voiceLanguage || currentLanguage,
              systemPrompt: buildSystemPrompt()
            },
            // Send full conversation history for memory
            history: chatMessages.slice(0, -1)  // All except the current message
          })
        });

        removeTyping(typingId);

        if (response.ok) {
          const data = await response.json();
          if (data.success && data.response) {
            chatMessages.push({ role: 'assistant', content: data.response });
            addChatMessage(data.response, 'bot');
            return;
          }
        }
      } catch (e) {
        removeTyping(typingId);
        console.warn('Backend unavailable:', e.message);
      }

      // Local fallback if backend is not running
      const fallback = generateSmartResponse(message);
      chatMessages.push({ role: 'assistant', content: fallback });
      addChatMessage(fallback, 'bot');
    }

    function buildSystemPrompt() {
      // Use voiceLanguage so that if user spoke in Hindi, AI responds in Hindi
      const lang = voiceLanguage === 'hi-IN' || currentLanguage === 'hi-IN'
        ? 'Hindi (Devanagari script)'
        : 'English';
      const formInfo = formData.formType !== 'general'
        ? `The user is currently filling a "${formData.formLabel}" form.`
        : 'The user is on a general web page.';
      const fieldStatus = formData.totalFieldsCount > 0
        ? `Form status: ${formData.filledFieldsCount}/${formData.totalFieldsCount} fields filled.`
        : '';
      const errorInfo = formData.errors.length > 0
        ? `Current errors in form: ${formData.errors.map(e => e.field + ': ' + e.message).join('; ')}`
        : 'No form errors currently.';
      const warnInfo = formData.warnings.length > 0
        ? `Current warnings: ${formData.warnings.map(w => w.field + ': ' + w.message).join('; ')}`
        : '';
      const tipsInfo = formData.tips && formData.tips.length > 0
        ? `Requirements for this form: ${formData.tips.join('; ')}`
        : '';

      return `You are Sahayak AI, a helpful assistant built into a Chrome extension that helps Indian citizens fill government forms and apply for government schemes and certificates.

CURRENT FORM CONTEXT:
${formInfo}
${fieldStatus}
${errorInfo}
${warnInfo}
${tipsInfo}

YOUR CAPABILITIES:
- Help users understand eligibility criteria for government schemes (pension, scholarship, ration card, etc.)
- Guide users on required documents for any certificate or application
- Explain form fields and what information is needed
- Provide direct links to official government portals when asked
- Answer questions about Aadhaar, PAN, income certificates, caste certificates, domicile, etc.
- Remember the full conversation context and refer back to earlier messages

OFFICIAL GOVERNMENT LINKS (provide these when relevant):
- Aadhaar: https://uidai.gov.in
- PAN Card: https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html
- Passport: https://passportindia.gov.in
- Driving License: https://parivahan.gov.in
- Ration Card: https://nfsa.gov.in
- Old Age Pension: https://nsap.nic.in
- PM Scholarship: https://scholarships.gov.in
- Income/Caste/Domicile certificates: https://serviceonline.gov.in
- DigiLocker (for all documents): https://digilocker.gov.in
- Common Services Centre: https://csc.gov.in

RULES:
- CRITICAL: You MUST respond ONLY in ${lang}. Do NOT mix languages. Do NOT include any ${lang === 'Hindi (Devanagari script)' ? 'English words or sentences' : 'Hindi words or sentences'} in your response.
- Be concise but complete — use numbered lists when listing multiple items
- When the user asks for a link or website, ALWAYS provide the direct URL
- When you see form errors in the context above, proactively mention them
- Keep responses short (3-5 sentences max) unless listing documents or steps
- If asked something outside government forms/schemes, politely redirect`;
    }

    function showTyping() {
      const container = document.getElementById('chat-messages');
      if (!container) return null;
      const id = 'typing-' + Date.now();
      const div = document.createElement('div');
      div.className = 'message bot-message';
      div.id = id;
      div.innerHTML = '<div class="message-avatar">S</div><div class="message-content typing-dots"><span></span><span></span><span></span></div>';
      container.appendChild(div);
      container.scrollTop = container.scrollHeight;
      return id;
    }

    function removeTyping(id) {
      if (id) {
        const el = document.getElementById(id);
        if (el) el.remove();
      }
    }

    function generateSmartResponse(message) {
      const msg = message.toLowerCase();
      const hi = voiceLanguage === 'hi-IN' || currentLanguage === 'hi-IN';
      const formType = formData.formType;

      // Score query
      if (msg.includes('score') || msg.includes('kitna')) {
        return hi
          ? `Aapka score ${formData.acceptanceScore}% hai. ${formData.filledFieldsCount}/${formData.totalFieldsCount} fields bhare hain.`
          : `Your score is ${formData.acceptanceScore}%. ${formData.filledFieldsCount}/${formData.totalFieldsCount} fields filled.`;
      }

      // Eligibility check
      if (msg.includes('eligible') || msg.includes('yogya') || msg.includes('qualify')) {
        const score = formData.acceptanceScore;
        const errors = formData.errors.length;
        if (score >= 80 && errors === 0) {
          return hi
            ? 'Aap eligible lagte hain! Sab fields sahi bhare hain.'
            : `You appear eligible for ${formData.formLabel}. All fields look correct!`;
        } else if (errors > 0) {
          return hi
            ? `${errors} galtiyan hain jo eligibility rok sakti hain. Unhe theek karein.`
            : `You have ${errors} issue(s) that may affect eligibility. Please fix them first.`;
        }
        return hi
          ? 'Abhi tak poori jaankari nahi mili. Sab fields bharo.'
          : 'Not enough information yet. Please fill all the fields.';
      }

      // Pension specific
      if (msg.includes('pension') || (formType === 'pension' && msg.includes('age'))) {
        return hi
          ? 'Pension ke liye: Umra 60 saal ya usse zyada, income 1 lakh se kam, Aadhaar zaroori hai, bank account chahiye DBT ke liye.'
          : 'For pension: Age 60+, income below ₹1,00,000/year, Aadhaar mandatory, bank account needed for DBT transfer.';
      }

      // Aadhaar requirement
      if (msg.includes('aadhar') || msg.includes('aadhaar')) {
        return hi
          ? 'Aadhaar 12-digit unique number hai. Zyaadatar sarkaari forms ke liye zaroori hai. Format: XXXX XXXX XXXX'
          : 'Aadhaar is a 12-digit unique identity number. Required for most government forms. Format: XXXX XXXX XXXX';
      }

      // Certificate specific
      if (msg.includes('certificate') || msg.includes('praman patra')) {
        const tips = formData.tips;
        if (tips && tips.length > 0) {
          return (hi ? 'Is form ke liye zaroori documents:\n' : `Documents needed for ${formData.formLabel}:\n`) +
            tips.map((t, i) => `${i + 1}. ${t}`).join('\n');
        }
        return hi
          ? 'Certificate ke liye: Aadhaar card, address proof, aur concerned authority ka form chahiye.'
          : 'For a certificate: Aadhaar card, address proof, and the relevant authority\'s form are needed.';
      }

      // Documents query
      if (msg.includes('document') || msg.includes('dastavez') || msg.includes('required') || msg.includes('what do i need')) {
        const tips = formData.tips;
        if (tips && tips.length > 0) {
          return (hi ? 'Zaroori documents:\n' : 'Required documents:\n') +
            tips.map((t, i) => `${i + 1}. ${t}`).join('\n');
        }
        return hi
          ? 'Aadhaar, address proof, aur income proof zyaadatar forms ke liye chahiye.'
          : 'Aadhaar, address proof, and income proof are needed for most government forms.';
      }

      // Errors query
      if (msg.includes('error') || msg.includes('problem') || msg.includes('galti')) {
        if (formData.errors.length === 0) {
          return hi ? 'Koi error nahi mili!' : 'No errors found! Form looks good.';
        }
        return (hi ? 'Yeh galtiyan hain:\n' : 'These errors were found:\n') +
          formData.errors.map((e, i) => `${i + 1}. ${e.field}: ${e.message}`).join('\n');
      }

      // Help
      if (msg.includes('help') || msg.includes('madad')) {
        return hi
          ? 'Main in cheezon mein madad kar sakta hoon:\n1. "eligible hoon?" - eligibility check\n2. "documents kya chahiye?" - required documents\n3. "score?" - acceptance score\n4. "errors?" - form ki galtiyan'
          : 'I can help with:\n1. "am I eligible?" - check eligibility\n2. "what documents needed?" - required documents\n3. "score?" - check your score\n4. "errors?" - see form issues';
      }

      return hi
        ? `${formData.formLabel} ke baare mein poochhein. Type "help" for commands.`
        : `Ask me about ${formData.formLabel}. Type "help" for commands.`;
    }

    function addChatMessage(text, sender) {
      const container = document.getElementById('chat-messages');
      if (!container) return;
      const div = document.createElement('div');
      div.className = `message ${sender}-message`;

      // Format text: convert URLs to clickable links, newlines to <br>, bold **text**
      let htmlText = text
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') // Escape HTML
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')  // **bold**
        .replace(/\*(\S.*?)\*/g, '<em>$1</em>')              // *italic*
        .replace(/(https?:\/\/[^\s<>"]+)/g,
          '<a href="$1" target="_blank" rel="noopener" class="chat-link">$1</a>'); // clickable URLs

      div.innerHTML = `
        ${sender === 'bot' ? '<div class="message-avatar">S</div>' : ''}
        <div class="message-content">${htmlText}</div>
      `;
      container.appendChild(div);
      container.scrollTop = container.scrollHeight;
      if (sender === 'bot') speakText(text);
    }

    // ── TTS STATE ─────────────────────────────────────────────
    let ttsPaused = false;

    function speakText(text) {
      if (!('speechSynthesis' in window)) return;

      // Cancel any ongoing speech first
      speechSynthesis.cancel();
      ttsPaused = false;

      // Clean text: strip HTML tags, trim whitespace
      let cleanText = text.replace(/<[^>]*>/g, '').trim();
      if (!cleanText) return;

      // Fix numbered list reading:
      // Without this, "Birth Certificate\n2. SSLC" is read as "Birth Certificate 2 SSLC"
      // We ensure each list item ends with a pause before the next number starts.
      cleanText = cleanText
        .replace(/([a-zA-Z\u0900-\u097F])\s*\n\s*(\d+[\.\)])/g, '$1. $2')  // "text\n2." → "text. 2."
        .replace(/\n\s*(\d+[\.\)])/g, '. $1')                                // remaining "\n2." → ". 2."
        .replace(/\n/g, '. ');                                                // any other newlines → pause

      const u = new SpeechSynthesisUtterance(cleanText);
      u.lang = voiceLanguage;   // Always match voice input language
      u.rate = 0.9;

      // Show TTS controls
      const controls = document.getElementById('tts-controls');
      const statusEl = document.getElementById('tts-status');
      const pauseBtn = document.getElementById('tts-pause-btn');
      if (controls) controls.style.display = 'flex';
      if (statusEl) statusEl.textContent = '🔊 Speaking...';
      if (pauseBtn) pauseBtn.textContent = '⏸ Pause';

      u.onend = () => {
        ttsPaused = false;
        if (controls) controls.style.display = 'none';
      };
      u.onerror = () => {
        ttsPaused = false;
        if (controls) controls.style.display = 'none';
      };

      speechSynthesis.speak(u);
    }

    function toggleTTSPause() {
      if (!('speechSynthesis' in window)) return;
      const pauseBtn = document.getElementById('tts-pause-btn');
      const statusEl = document.getElementById('tts-status');
      if (speechSynthesis.speaking && !speechSynthesis.paused) {
        speechSynthesis.pause();
        ttsPaused = true;
        if (pauseBtn) pauseBtn.textContent = '▶ Resume';
        if (statusEl) statusEl.textContent = '⏸ Paused';
      } else if (speechSynthesis.paused) {
        speechSynthesis.resume();
        ttsPaused = false;
        if (pauseBtn) pauseBtn.textContent = '⏸ Pause';
        if (statusEl) statusEl.textContent = '🔊 Speaking...';
      }
    }

    function stopTTS() {
      if (!('speechSynthesis' in window)) return;
      speechSynthesis.cancel();
      ttsPaused = false;
      const controls = document.getElementById('tts-controls');
      if (controls) controls.style.display = 'none';
    }

    // ── SCORE ─────────────────────────────────────────────────
    function calculateAcceptanceScore() {
      const total = formData.totalFieldsCount || 1;
      const filled = formData.filledFieldsCount;
      const errors = formData.errors.length;
      const warnings = formData.warnings.length;
      let score = (filled / total) * 100;
      score = score - (errors * 15) - (warnings * 5);
      formData.acceptanceScore = Math.round(Math.max(0, Math.min(100, score)));
    }

    // ── UI UPDATE ─────────────────────────────────────────────
    function updateAssistantUI() {
      updateGauge(formData.acceptanceScore);

      const score = formData.acceptanceScore;
      const filled = formData.filledFieldsCount;
      const total = formData.totalFieldsCount;
      const errors = formData.errors.length;
      const warnings = formData.warnings.length;

      // Form type badge
      const badge = document.getElementById('form-type-badge');
      if (badge) {
        if (formData.formType !== 'general' && total > 0) {
          badge.style.display = 'block';
          badge.textContent = '📋 Detected: ' + formData.formLabel;
        } else {
          badge.style.display = 'none';
        }
      }

      // Score & recommendation
      const scoreEl = document.getElementById('acceptance-score');
      if (scoreEl) scoreEl.textContent = score + '%';

      const recDiv = document.getElementById('recommendation');
      if (recDiv) {
        if (total === 0) {
          recDiv.innerHTML = `<div class="rec-icon">&#128269;</div><div class="rec-text"><div class="rec-title">No form detected</div><div class="rec-desc">Navigate to a government form to start.</div></div>`;
        } else if (score >= 80 && errors === 0) {
          recDiv.innerHTML = `<div class="rec-icon success">&#10003;</div><div class="rec-text"><div class="rec-title">Ready to Submit</div><div class="rec-desc">${filled}/${total} fields filled. Form looks good!</div></div>`;
        } else if (score >= 50 || (filled > 0 && errors === 0)) {
          recDiv.innerHTML = `<div class="rec-icon warning">&#9888;</div><div class="rec-text"><div class="rec-title">Review Before Submitting</div><div class="rec-desc">${filled}/${total} fields filled.${errors > 0 ? ' ' + errors + ' error(s) found.' : ''}</div></div>`;
        } else {
          recDiv.innerHTML = `<div class="rec-icon error">&#10005;</div><div class="rec-text"><div class="rec-title">Don't Submit Yet</div><div class="rec-desc">${filled}/${total} fields filled. Please complete the form.</div></div>`;
        }
      }

      // Errors
      const issuesSection = document.getElementById('issues-section');
      const issuesList = document.getElementById('issues-list');
      if (issuesSection && issuesList) {
        const hasIssues = errors > 0 || (formData.infos && formData.infos.length > 0);
        issuesSection.style.display = hasIssues ? 'block' : 'none';
        if (hasIssues) {
          issuesList.innerHTML = '';
          formData.errors.forEach(e => {
            const d = document.createElement('div');
            d.className = 'issue-item error-item';
            d.innerHTML = `<span class="issue-icon">&#10060;</span><span class="issue-text"><strong>${e.field}:</strong> ${e.message}</span>`;
            issuesList.appendChild(d);
          });
          // Info messages (e.g. age calculated from DOB)
          (formData.infos || []).forEach(e => {
            const d = document.createElement('div');
            d.className = 'issue-item';
            d.style.cssText = 'border-left: 3px solid #3b82f6; background: #eff6ff; padding: 8px 10px; border-radius: 6px; margin-bottom: 6px; display:flex; gap:8px; align-items:flex-start;';
            d.innerHTML = `<span style="color:#3b82f6;font-size:14px;">ℹ️</span><span class="issue-text"><strong>${e.field}:</strong> ${e.message}</span>`;
            issuesList.appendChild(d);
          });
        }
      }

      // Warnings
      const suggestionsSection = document.getElementById('suggestions-section');
      const suggestionsList = document.getElementById('suggestions-list');
      if (suggestionsSection && suggestionsList) {
        suggestionsSection.style.display = warnings > 0 ? 'block' : 'none';
        if (warnings > 0) {
          suggestionsList.innerHTML = '';
          formData.warnings.forEach(w => {
            const d = document.createElement('div');
            d.className = 'issue-item warning-item';
            d.innerHTML = `<span class="issue-icon">&#9888;&#65039;</span><span class="issue-text"><strong>${w.field}:</strong> ${w.message}</span>`;
            suggestionsList.appendChild(d);
          });
        }
      }

      // Tips / Form Requirements
      const tipsSection = document.getElementById('tips-section');
      const tipsList = document.getElementById('tips-list');
      if (tipsSection && tipsList && formData.tips && formData.tips.length > 0) {
        tipsSection.style.display = 'block';
        tipsList.innerHTML = '';
        formData.tips.forEach(tip => {
          const d = document.createElement('div');
          d.className = 'issue-item tip-item';
          d.innerHTML = `<span class="issue-icon">&#128204;</span><span class="issue-text">${tip}</span>`;
          tipsList.appendChild(d);
        });
      } else if (tipsSection) {
        tipsSection.style.display = 'none';
      }
    }

    let currentNeedleAngle = -90;
    let needleAnimFrame = null;

    function updateGauge(score) {
      const needleGroup = document.getElementById('gauge-needle-group');
      const fill = document.getElementById('gauge-fill');
      if (!needleGroup || !fill) return;

      // Animate the fill arc via CSS transition
      fill.style.strokeDashoffset = 251.2 - (score / 100) * 251.2;

      // Animate needle smoothly with requestAnimationFrame
      const targetAngle = -90 + (score / 100) * 180;
      if (needleAnimFrame) cancelAnimationFrame(needleAnimFrame);

      const startAngle = currentNeedleAngle;
      const startTime = performance.now();
      const duration = 700; // ms

      function easeOutBack(t) {
        const c1 = 1.70158, c3 = c1 + 1;
        return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
      }

      function animate(now) {
        const elapsed = now - startTime;
        const t = Math.min(elapsed / duration, 1);
        const easedT = easeOutBack(t);
        const angle = startAngle + (targetAngle - startAngle) * easedT;
        needleGroup.setAttribute('transform', `rotate(${angle}, 100, 100)`);
        currentNeedleAngle = angle;
        if (t < 1) needleAnimFrame = requestAnimationFrame(animate);
        else currentNeedleAngle = targetAngle;
      }

      needleAnimFrame = requestAnimationFrame(animate);
    }

    // ── CONVERSATION ──────────────────────────────────────────
    function loadConversationHistory() {
      const tabId = sessionStorage.getItem('sahayak_tab');
      if (tabId) {
        const saved = localStorage.getItem(`sahayak_chat_${tabId}`);
        if (saved) { try { conversationHistory = JSON.parse(saved); } catch(e) { conversationHistory = []; } }
      }
    }

    function restoreConversationHistory() {
      conversationHistory.forEach(entry => { if (entry.query) addChatMessage(entry.query, 'user'); });
    }

    // ══════════════════════════════════════════════════════════
    // DOCUMENT UPLOAD & AI AUTO-FILL
    // ══════════════════════════════════════════════════════════
    function initDocUpload() {
      const dropZone  = document.getElementById('doc-drop-zone');
      const fileInput = document.getElementById('doc-file-input');
      const fileList  = document.getElementById('doc-file-list');
      const extractBtn= document.getElementById('doc-extract-btn');
      const progress  = document.getElementById('doc-progress');
      const progressFill = document.getElementById('doc-progress-fill');
      const progressText = document.getElementById('doc-progress-text');
      const resultBox = document.getElementById('doc-result');
      if (!dropZone || !fileInput) return;

      let selectedFiles = [];

      // ── Drag & Drop ──────────────────────────────────────────
      dropZone.addEventListener('dragover', e => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
      });
      dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
      dropZone.addEventListener('drop', e => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        addFiles(Array.from(e.dataTransfer.files));
      });

      fileInput.addEventListener('change', () => {
        addFiles(Array.from(fileInput.files));
        fileInput.value = '';
      });

      extractBtn.addEventListener('click', runSmartOCR);

      function addFiles(newFiles) {
        newFiles.forEach(f => {
          if (!selectedFiles.find(x => x.name === f.name && x.size === f.size)) {
            selectedFiles.push(f);
          }
        });
        renderFileList();
      }

      function removeFile(idx) {
        selectedFiles.splice(idx, 1);
        renderFileList();
      }

      function getFileIcon(name) {
        const ext = name.split('.').pop().toLowerCase();
        if (['jpg','jpeg','png','gif','bmp','webp'].includes(ext)) return '🖼️';
        if (ext === 'pdf') return '📄';
        if (['doc','docx'].includes(ext)) return '📝';
        return '📎';
      }

      function renderFileList() {
        if (selectedFiles.length === 0) {
          fileList.style.display = 'none';
          extractBtn.style.display = 'none';
          resultBox.style.display = 'none';
          return;
        }
        fileList.style.display = 'flex';
        extractBtn.style.display = 'block';
        fileList.innerHTML = selectedFiles.map((f, i) => `
          <div class="doc-file-chip">
            <span>${getFileIcon(f.name)}</span>
            <span class="doc-file-name">${f.name.length > 22 ? f.name.slice(0,20)+'…' : f.name}</span>
            <button class="doc-file-remove" data-idx="${i}" title="Remove">✕</button>
          </div>
        `).join('');
        fileList.querySelectorAll('.doc-file-remove').forEach(btn => {
          btn.addEventListener('click', () => removeFile(parseInt(btn.dataset.idx)));
        });
      }

      // ── OCR → Auto-Fill ─────────────────────────────────────
      async function runSmartOCR() {
        if (!selectedFiles.length) return;

        extractBtn.disabled = true;
        document.getElementById('doc-extract-btn-text').textContent = '⏳ Processing...';
        progress.style.display = 'block';
        resultBox.style.display = 'none';
        animateProgress(0, 30, 800, 'Reading files...');

        try {
          const formData = new FormData();
          selectedFiles.forEach(f => formData.append('files[]', f));

          animateProgress(30, 65, 1200, 'AI is analyzing documents...');

          const res = await fetch(`${API_URL}/api/smart-ocr`, {
            method: 'POST',
            body: formData
          });

          animateProgress(65, 85, 600, 'Matching fields in form...');

          if (!res.ok) throw new Error(`Server error: ${res.status}`);
          const data = await res.json();
          if (!data.success) throw new Error(data.error || 'Extraction failed');

          animateProgress(85, 100, 400, 'Filling form fields...');

          const filled = autoFillForm(data.extracted_data);
          await sleep(500);

          progress.style.display = 'none';
          showResult(data, filled);

          // Recalculate score after filling
          setTimeout(() => {
            calculateAcceptanceScore();
            updateAssistantUI();
          }, 600);

        } catch (err) {
          progress.style.display = 'none';
          resultBox.style.display = 'block';
          resultBox.innerHTML = `<div class="doc-result-error">❌ ${err.message}<br><small>Make sure the backend server is running.</small></div>`;
        } finally {
          extractBtn.disabled = false;
          document.getElementById('doc-extract-btn-text').textContent = '✨ Extract & Auto-Fill Form';
        }
      }

      function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

      function animateProgress(from, to, duration, label) {
        progressText.textContent = label;
        const start = performance.now();
        function step(now) {
          const t = Math.min((now - start) / duration, 1);
          const v = from + (to - from) * t;
          progressFill.style.width = v + '%';
          if (t < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      }

      // ── Smart field mapping ──────────────────────────────────
      // Maps extracted data keys → patterns that match form field labels
      const FIELD_MAP = [
        // ── ORDER MATTERS: more specific patterns first ──
        { key: 'father_name',    patterns: ["father's name","father name",'father','pita','पिता'] },
        { key: 'mother_name',    patterns: ["mother's name","mother name",'mother','mata','माता'] },
        { key: 'account_number', patterns: ['account number','account no','acc no','bank account number','खाता संख्या'] },
        { key: 'ifsc',           patterns: ['ifsc code','ifsc','bank code','rtgs code'] },
        { key: 'bank_name',      patterns: ['bank name','name of bank','बैंक का नाम'] },
        { key: 'branch_name',    patterns: ['branch name','branch','शाखा'] },
        { key: 'aadhar',         patterns: ['aadhaar number','aadhar number','adhaar number','adhaar no','aadhaar no','aadhar no','uid number','aadhaar','aadhar','adhaar','आधार संख्या','आधार नंबर','आधार'] },
        { key: 'pan',            patterns: ['pan number','pan no','pan card number','permanent account number','पैन नंबर'] },
        { key: 'dob',            patterns: ['date of birth','birth date','dob','d.o.b','जन्म तिथि','जन्म दिनांक'] },
        { key: 'age',            patterns: ['age','aayu','आयु','उम्र'] },
        { key: 'gender',         patterns: ['gender','sex','लिंग'] },
        { key: 'email',          patterns: ['email address','email id','e-mail','email','ईमेल'] },
        { key: 'mobile',         patterns: ['mobile number','phone number','mobile no','contact number','mob no','मोबाइल नंबर','फोन नंबर'] },
        { key: 'address',        patterns: ['permanent address','present address','residential address','full address','address','पता'] },
        { key: 'pincode',        patterns: ['pin code','pincode','zip code','postal code','पिन कोड'] },
        { key: 'district',       patterns: ['district','zila','जिला'] },
        { key: 'state',          patterns: ['state','rajya','राज्य','प्रदेश'] },
        { key: 'city',           patterns: ['city','town','shahar','शहर'] },
        { key: 'voter_id',       patterns: ['voter id','voter card','epic no','election card','मतदाता'] },
        { key: 'driving_license',patterns: ['driving licence','driving license','dl no','licence no'] },
        { key: 'marks_10th',     patterns: ['10th marks','10th percentage','class 10 marks','ssc marks','matriculation marks','10th %'] },
        { key: 'marks_12th',     patterns: ['12th marks','12th percentage','class 12 marks','hsc marks','intermediate marks','12th %'] },
        { key: 'income',         patterns: ['annual income','monthly income','income','आय','वार्षिक आय'] },
        { key: 'occupation',     patterns: ['occupation','profession','job type','व्यवसाय'] },
        { key: 'caste',          patterns: ['caste category','caste','category','जाति','श्रेणी'] },
        { key: 'religion',       patterns: ['religion','dharm','धर्म'] },
        { key: 'blood_group',    patterns: ['blood group','blood type','रक्त समूह'] },
        { key: 'nationality',    patterns: ['nationality','rashtriyata','राष्ट्रीयता'] },
        // ── name LAST so it doesn't match father/mother name fields ──
        { key: 'name',           patterns: ['full name','applicant name','candidate name','beneficiary name','student name','your name','naam','पूरा नाम','नाम','name'] },
      ];

      function autoFillForm(data) {
        const IS_GF = /docs\.google\.com\/forms/i.test(window.location.href);
        let filledCount = 0;

        // ── GOOGLE FORMS: Question-block approach ────────────────────────
        // Walk each question block, find its title, then find its input
        if (IS_GF) {
          // Each question is wrapped in a div[role="listitem"] or similar container
          const questionBlocks = Array.from(document.querySelectorAll(
            '[role="listitem"], .freebirdFormviewerViewItemsItemItem, .m2'
          ));

          // Process ALL question blocks regardless of filledCount
          // Process ALL question blocks regardless of filledCount
          questionBlocks.forEach(block => {
            // Get question title from the block
            const titleEl = block.querySelector(
              '[role="heading"], .freebirdFormviewerComponentsQuestionBaseTitle, ' +
              '.freebirdFormviewerViewItemsItemItemTitle, .z12JJ, .M7eMe, ' +
              '[class*="questionTitle"], [class*="exportLabel"]'
            );
            if (!titleEl) return;
            // Clean label: remove asterisks, "required", extra whitespace, then fuzzy-normalize
            const label = fuzzyLabel(titleEl.textContent
              .trim()
              .replace(/[*★✱]/g, '')
              .replace(/\bRequired\b/gi, '')
              .replace(/\s+/g, ' ')
              .trim());
            if (!label || label.length < 2) return;

            console.log('[Sahayak OCR] GF question block label:', label);

            // Find the fillable input inside this block
            const fillable = block.querySelector(
              'input:not([type="hidden"]):not([type="submit"]):not([type="file"]), ' +
              'textarea, [contenteditable="true"]'
            );
            if (!fillable) return;

            // Skip already filled
            const currentVal = fillable.isContentEditable
              ? (fillable.innerText || '').trim()
              : (fillable.value || '').trim();
            if (currentVal) return;

            // Match label to data
            for (const mapping of FIELD_MAP) {
              const value = data[mapping.key];
              if (!value) continue;
              // Prevent 'name' key from filling father/mother name fields
              if (mapping.key === 'name' && /father|mother|pita|mata/i.test(label)) continue;
              const matched = mapping.patterns.some(p => {
                const pl = p.toLowerCase();
                if (label === pl) return true;
                const re = new RegExp('(^|[\\s\\-/(])' + pl.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '([\\s\\-/)*:]|$)', 'i');
                return re.test(label);
              });
              if (!matched) continue;

              fillGFField(fillable, String(value));
              filledCount++;
              break;
            }
          });

          // If block approach found fields, return
          if (filledCount > 0) return filledCount;
        }

        // ── FALLBACK: Standard input approach ────────────────────────────
        const standard = Array.from(document.querySelectorAll(
          'input:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([type="reset"]):not([type="file"]), select, textarea'
        ));
        const contentEditable = IS_GF
          ? Array.from(document.querySelectorAll('[contenteditable="true"]'))
          : [];
        const inputs = [...standard, ...contentEditable].filter(el => {
          const s = window.getComputedStyle(el);
          return s.display !== 'none' && s.visibility !== 'hidden' && el.offsetParent !== null;
        });

        inputs.forEach(input => {
          const rawLabel = getGoogleFormsLabel(input);
          if (rawLabel) console.log('[Sahayak OCR] Field label detected:', rawLabel);
          if (!rawLabel) return;
          const label = fuzzyLabel(rawLabel.toLowerCase().trim());

          for (const mapping of FIELD_MAP) {
            const value = data[mapping.key];
            if (!value) continue;

            // Skip 'name' key if label belongs to father/mother
            if (mapping.key === 'name' && /father|mother|pita|mata/i.test(label)) continue;

            // Check if any pattern matches the label
            const matched = mapping.patterns.some(p => {
              const pl = p.toLowerCase();
              if (label === pl) return true;
              // Pattern must appear as a whole phrase (not substring of a word)
              const re = new RegExp('(^|[\\s\\-/(])' + pl.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '([\\s\\-/)*:]|$)', 'i');
              return re.test(label);
            });
            if (!matched) continue;

            const currentVal = (input.isContentEditable || input.contentEditable === 'true')
              ? (input.innerText || '').trim()
              : (input.value || '').trim();
            if (currentVal) continue;

            const fillValue = String(value);

            if (input.tagName === 'SELECT') {
              const opt = Array.from(input.options).find(o =>
                o.text.toLowerCase().includes(fillValue.toLowerCase()) ||
                o.value.toLowerCase().includes(fillValue.toLowerCase())
              );
              if (opt) {
                input.value = opt.value;
                input.dispatchEvent(new Event('change', {bubbles: true}));
                flashField(input);
                filledCount++;
              }
            } else if (input.isContentEditable || input.contentEditable === 'true') {
              // Google Forms contenteditable fill
              input.focus();
              document.execCommand('selectAll', false, null);
              document.execCommand('insertText', false, fillValue);
              if (!input.innerText || input.innerText.trim() !== fillValue) {
                input.innerText = fillValue;
                input.dispatchEvent(new Event('input', {bubbles: true}));
                input.dispatchEvent(new KeyboardEvent('keydown', {bubbles: true}));
                input.dispatchEvent(new KeyboardEvent('keyup', {bubbles: true}));
              }
              flashField(input);
              filledCount++;
            } else {
              // Regular input
              const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
              if (nativeSetter && input.tagName === 'INPUT') {
                nativeSetter.set.call(input, fillValue);
              } else {
                input.value = fillValue;
              }
              input.dispatchEvent(new Event('input', {bubbles: true}));
              input.dispatchEvent(new Event('change', {bubbles: true}));
              flashField(input);
              filledCount++;
            }
            break; // one mapping per field
          }
        });

        return filledCount;
      }

      function fillGFField(el, value) {
        if (el.isContentEditable || el.contentEditable === 'true') {
          el.focus();
          document.execCommand('selectAll', false, null);
          document.execCommand('insertText', false, value);
          if ((el.innerText || '').trim() !== value) {
            el.innerText = value;
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new KeyboardEvent('keydown', {bubbles: true}));
            el.dispatchEvent(new KeyboardEvent('keyup', {bubbles: true}));
          }
        } else if (el.tagName === 'SELECT') {
          const opt = Array.from(el.options).find(o =>
            o.text.toLowerCase().includes(value.toLowerCase()) ||
            o.value.toLowerCase().includes(value.toLowerCase())
          );
          if (opt) { el.value = opt.value; el.dispatchEvent(new Event('change', {bubbles: true})); }
        } else {
          const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
          if (nativeSetter && el.tagName === 'INPUT') {
            nativeSetter.set.call(el, value);
          } else {
            el.value = value;
          }
          el.dispatchEvent(new Event('input', {bubbles: true}));
          el.dispatchEvent(new Event('change', {bubbles: true}));
        }
        flashField(el);
      }

      function getGoogleFormsLabel(input) {
        // 1. aria-label (most reliable)
        const aria = (input.getAttribute('aria-label') || '').trim();
        if (aria) return aria;

        // 1b. Check the wrapping div's aria-label (Google Forms wraps inputs in labeled divs)
        let parent = input.parentElement;
        for (let i = 0; i < 5 && parent; i++) {
          const parentAria = (parent.getAttribute('aria-label') || '').trim();
          if (parentAria && parentAria.length > 1) return parentAria;
          parent = parent.parentElement;
        }

        // 2. aria-labelledby
        const ariaId = input.getAttribute('aria-labelledby');
        if (ariaId) {
          const ids = ariaId.split(' ');
          const text = ids.map(id => {
            const el = document.getElementById(id);
            return el ? el.textContent.trim() : '';
          }).filter(Boolean).join(' ');
          if (text) return text;
        }

        // 3. name / placeholder (skip Google Forms entry.XXXXX ids)
        const placeholder = (input.placeholder || '').trim();
        if (placeholder) return placeholder;
        const nameAttr = (input.name || '').trim();
        if (nameAttr && !/^entry\.\d+/.test(nameAttr)) return nameAttr;

        // 4. Google Forms specific — question text is in parent containers
        // Walk up DOM looking for heading/title elements
        const GF_SELECTORS = [
          '[role="heading"]',
          '[class*="freebirdFormviewerComponentsQuestionBaseTitle"]',
          '[class*="freebirdFormviewerViewItemsItemItemTitle"]',
          '[class*="exportLabel"]',
          '[class*="M7eMe"]',   // common GF class
          '[class*="z12JJ"]',   // another GF class
          'label',
        ];

        let el = input.parentElement;
        for (let i = 0; i < 20 && el; i++) {
          // Check aria-label on container divs
          const elAria = (el.getAttribute('aria-label') || '').trim();
          if (elAria && elAria.length > 1) return elAria;

          for (const sel of GF_SELECTORS) {
            try {
              const heading = el.querySelector(sel);
              if (heading) {
                // Make sure heading doesn't contain the input itself
                if (!heading.contains(input)) {
                  const txt = heading.textContent.trim().replace(/\s+/g, ' ');
                  if (txt.length > 1 && txt !== input.placeholder) return txt;
                }
              }
            } catch(e) {}
          }
          // Also check if this element IS a label/heading
          if (['LABEL','H1','H2','H3','H4'].includes(el.tagName)) {
            const txt = el.textContent.trim();
            if (txt.length > 1) return txt;
          }
          // Check jsname attribute — Google Forms uses data-params with question text
          const jsname = el.getAttribute('jsname') || '';
          if (jsname) {
            // Look for sibling heading before this element
            const prev = el.previousElementSibling;
            if (prev) {
              const txt = prev.textContent.trim().replace(/\s+/g, ' ');
              if (txt.length > 1 && txt.length < 100) return txt;
            }
          }
          el = el.parentElement;
        }

        // 5. Fallback: id attribute
        if (input.id && !/^entry/.test(input.id)) return input.id;

        return '';
      }

            function flashField(input) {
        const orig = input.style.transition;
        const origBg = input.style.backgroundColor;
        const origBorder = input.style.border;
        input.style.transition = 'background 0.3s, border 0.3s';
        input.style.backgroundColor = '#D1FAE5';
        input.style.border = '2px solid #10B981';
        setTimeout(() => {
          input.style.backgroundColor = origBg;
          input.style.border = origBorder;
          input.style.transition = orig;
        }, 1800);
      }

      function showResult(data, filled) {
        const docTypes = (data.doc_types || []).join(', ') || 'documents';
        const confidence = Math.round((data.confidence || 0.7) * 100);
        const fieldsFound = data.fields_found || 0;

        resultBox.style.display = 'block';
        resultBox.innerHTML = `
          <div class="doc-result-success">
            <div class="doc-result-header">
              <span class="doc-result-icon">✅</span>
              <div>
                <div class="doc-result-title">${filled} field${filled !== 1 ? 's' : ''} auto-filled!</div>
                <div class="doc-result-sub">${fieldsFound} data points extracted · ${confidence}% confidence</div>
              </div>
            </div>
            ${docTypes ? `<div class="doc-result-types">📋 Detected: ${docTypes}</div>` : ''}
            <div class="doc-result-preview">
              ${Object.entries(data.extracted_data || {}).slice(0, 6).map(([k, v]) =>
                `<span class="doc-result-pill"><b>${k.replace(/_/g,' ')}:</b> ${String(v).slice(0,20)}</span>`
              ).join('')}
            </div>
          </div>
        `;
      }
    }
    // ══════════════════════════════════════════════════════════

    // ── START ─────────────────────────────────────────────────
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }
  }

})();