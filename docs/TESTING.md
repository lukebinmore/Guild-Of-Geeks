# [**Go Back**](../README.md)

# **Table Of Contents**
- [**Go Back**](#go-back)
- [**Table Of Contents**](#table-of-contents)
- [**Testing**](#testing)
  - [**During Development**](#during-development)
  - [**Automated Testing**](#automated-testing)
  - [**Manual Testing**](#manual-testing)

# **Testing**

## **During Development**

For bugs found and fixed during the development of this project, please [Click Here.](https://github.com/search?q=repo%3Alukebinmore%2FGuild-Of-Geeks+%22Bug+Fix+-+%22&type=commits)

## **Automated Testing**

Before finalizing the product, a number of tests were carried out to ensure the site functioned as expected.
These include:

- [Flake8 Linting](https://flake8.pycqa.org/en/latest/) - To ensure that the python code meets industry standards.
  - All python files follow Flake8 industry standards.
- [PEP8 Online Validator](http://pep8online.com/) - To ensure that the python code meets industry standards.
  - forum/views.py
    - W503 Warnings - Due to line break before terminary oporator - Not fixed due to then causing an issue with line length.
  - All other pages return no errors.
- Unit Testing - To ensure that all code behaves as expected.
  - All tests passed as expected.
- [Beautify JavaScript Validator](https://beautifytools.com/javascript-validator.php) - To ensure that all JavaScript code meets industry standards and functions correctly.
  - All essential tests passed.
  - Some errors due to the use of jQuery and external libraries.
- [JigSaw CSS Validator](https://jigsaw.w3.org/css-validator/) - To ensure that the css code meets industry standards.
  - static/style.css
    - No major errors.
    - Warnings due to use of CSS Variables.
    - Warnings due to setting border-color and background-color the same for buttons.
      - Left due to being required to override bootstrap defaults.
  - static/theme-dark.css
    - No errors found.
  - static/theme-light.css
    - No errors found.
- [W3C HTML Validator](https://validator.w3.org/#validate_by_input) - To ensure that the html code meets industry standards, and does not contain errors.
  - Due to use of django template tags, pages could not be tested directly from repo. Instead, computed source was grabbed from chrome devtools and checked in the validator. This resulted in the computed code being compiled of multiple templates. Results below show errors found across all pages.
    - HTMX tag errors - Attribute tags used by HTMX library.
    - Select2 element errors - Select2 places list of options inside span, causing errors.
    - Select2 element options - Select2 does not add content to options, using the value tag instead, causing label error.
    - Select2 searchbox role - Select2 applies unnessessary role=searchbox element.
    - FontAweomse Style error - Fontawesome applies style element as child of body.
    - FontAwesome aniamtion error - Fontawesome applies variable to animation-delay and transform, which is not detected as a correct value.
    - Profile edit button - h2 detected as empty due to use of link and icon only.
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/) - To ensure that no runtime errors occur when loading or displaying content. Additionally to provide metrics on performance, accessibility E.T.C.
  - Issue found with script.js - Bootstrap Alert function causing TypeError.
  - Performance
    - Desktop - 100%
    - Mobile - 98%
  - Accessibility
    - Desktop - 98%
    - Mobile - 97%
  - Best Practice - Low score caused by bootstrap error.
    - Desktop - 89%
    - mobile - 88%
  - SEO
    - Desktop - 94%
    - Mobile - 92%

## **Manual Testing**

Manual testing of the code and site was carried out during the development of this project. Due to the large number of features/aspects to test, below is a summary of the manual tests completed both during and after project finalization.

- Page Loading / Layout
  - All pages have been tested on different screen sizes for coherent design.
  - All pages have been tested on the following browsers for compatibiluty:
    - Firefox
    - Chrome
    - Edge
    - Safari
    - Opera
  - All pages have been tested using Chrome devtools simulated devices.
  - All pages have been tested on different networks to ensure connectvitiy to CDNS.
- Color Scheme
  - All pages have been checked for coherent color scheme.
  - All pages have been checked for implementation of themes.
- Search / Filters
  - Search feature has been tested on all pages.
  - Filter feature has been tested on all relevent pages.
  - Filtering existing searchs has been tested.
  - Clearing of filters by completing new search has been tested.
- Forms / Inputs - The below forms and inputs have been checked for incorrect values:
  - Search
  - Filters
  - Post details
  - Profile details
  - Login details
  - Signup details
  - Password change details
  - Delete account details
  - Delete post details
  - Delete comment details
  - Contact us details
- User specific info / options.
  - All user specific sections or alterations have been tested.
  - All non-user specific sections or alterations have been tested.
- Buttons / Links.
  - All user interaction buttons have been tested.
  - All page redirections have been tested.
- Manually re-directing pages via URL.
  - All urls have been tested for correct action.
  - All pages requiring authentication have been tested.