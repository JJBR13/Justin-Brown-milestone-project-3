# Testing 

Testing was done site-wide, all tests undertaken are shown below: 

## Contents 

- [Functional Testing](#functional-testing)
- [Wave](#wave)
- [Validator Testing](#validator-testing)
  + [HTML](#html)
  + [CSS](#CSS)
  + [JavaScript](#javascript)
  + [PEP8](#pep8-online)
- [Lighthouse](#lighthouse)
  + [Desktop Results](#desktop-results)
  + [Mobile Results](#mobile-results)
- [Colour Contrast](#colour-contrast)
- [Browser Compatibility](#browser-compatibility)
- [Responsivity](#responsivity)
- [Issues/ Bugs Found & Resolved](#issues-bugs-found--resolved)

## Functional Testing 

## Wave

[WAVE link](https://wave.webaim.org/)

- This Chrome extension was used throughout the build of the site as well as final testing, this was to minimize bugs at the end of the project in final testing. 

![Wave Screenshot](documents/test/wave.png)

## Validator Testing

### HTML

[W3C HTML Validator link](https://validator.w3.org/)

- All .html files were validated through this checker, highlighting issues such as: 
  - Redundant tags 
  - Missing tags 
  - "POST" method in div tags, not for tags

- This was brilliant, to find these issues, however, due to the use of Jinji templating and url_for for href links, these tests were never completely clear. 

### CSS

[W3C CSS Validator link](https://jigsaw.w3.org/css-validator/#validate_by_input+with_options)
![CSS Validator Results](documents/test/css.png)

- This test returned no issues. 

## JavaScript

[JSHint](https://jshint.com/)

- Both files were Tested, they highlighted minimal issues and pulled errors with the Materialize script.

## PEP8 Online

[PEP8](http://ww7.pep8online.com/)

- This validation tested python code, in the app.py and... 

## Lighthouse 

[Lighthouse](https://developer.chrome.com/docs/lighthouse/)

### Desktop Results

### Mobile Results

## Colour Contrast 

[A11y Color link](https://color.a11y.com/)
![A11y Color Contrast Validator Results](documents/test/a11y.png)

## Browser Compatibility 

- This site was tested on Chrome, Microsoft Edge, and Firefox on desktop.

- The website was tested in Chrome on mobile and tablet. 

- All tested devices were consistent across browsers.

## Browser Compatibility 

- This site was tested on Chrome, Microsoft Edge, and Firefox on desktop.

- The website was tested in Chrome on mobile and tablet. 

- All tested devices were consistent across browsers.

## Responsivity

- Escape Gaming Reviews, is made easily accessible on all devices with help from the Materialize framework. Test through Google Developer Tools, on devices: 
    - iPhone SE
    - iPhone XR
    - Pixel 5
    - Samsung S8+
    - iPad Mini
    - iPad Air 

- The site was also tested for full responsive functionality manually on the below devices: 
    - Razor Blade 15 
    - Galaxy Fold Z3
    - ASUS ZenScreen 

## Issues/ Bugs Found & Resolved
