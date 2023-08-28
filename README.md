# Retro Replay eCommerce web platform

![Am I responsive mockup](docs/images/mockup.png)

[Click here to view the deployed site!](https://pp5-retro-replay-f8ca18b6956c.herokuapp.com/)

<details>
  <summary>Click to reveal QR code for easy mobile access!</summary>
  <img src="docs/images/pp5-qr_code.png" alt="QR code link to deployed site">
</details>

The table of contents can be accessed at any time by selecting the menu icon at
the top left of the screen, next to 'README.md'.

Links can be opened in a new tab with a right click, middle click or Ctrl + click.

Getting the most out of this web app requires a verified account. If you would
like to use all features of the site without using a personal email address,
[temp-mail](https://temp-mail.org/) can provide you with a disposable email address.

## Introduction

Retro Replay is a web-based e-commerce platform, powered by Django and Stripe.
It operates on a B2C model, where customers can pay by card for one, or multiple
items in the store. Items are added to their basket, followed by a secure
checkout page. The user is provided with an order confirmation email and they
may view past orders on their profile page.

Additionally, role-based CRUD functions are implemented to benefit the customer.
Customers may store, modify and delete saved addresses on their profile and
nominate one as their default address to speed up their next checkout. There are
lines of support available to customers, facilitated by the FAQ/Contact section.
The administrator can easily create, update and delete FAQ entries entirely from
the front end.

This application expands on my previous [full stack application](https://github.com/jts272/pp4-safe-hands-guitar-tech)
with a complete SEO and marketing campaign, utilizing Facebook and Mailchimp.

## Agile methodologies

An agile methodology was employed from start to finish in this project. For a
detailed breakdown on the implementation, please consult the
[agile methodologies breakdown](https://github.com/jts272/pp4-safe-hands-guitar-tech#agile-methodologies)
outlined in my previous full-stack production. There you will find a thorough
explanation of each component, how to read the visualizations and how they benefit
the development process.

Here are the links to the agile resources for this project. GitHub project boards
are best viewed in 'Board' layout, with the 'Labels' field enabled.

- [Issues](https://github.com/jts272/pp5-retro-replay/issues?q=is%3Aissue+is%3Aclosed)
- [Milestones](https://github.com/jts272/pp5-retro-replay/milestones?state=closed)
- [Projects](https://github.com/jts272/pp5-retro-replay/projects?query=is%3Aopen)

---

## Five stages of UX design

### 1. Strategy

- Business model
- Competition check

### 2. Scope

- MVP features
- Admin CRUD
- Specific eCommerce implementation

### 3. Structure

- Information architecture
- Interaction design
- Navigation

### 4. Skeleton

- UI
- Navigation story
- Mobile-first

<details>
  <summary>Wireframe</summary>
  <img src="" alt="">
</details>

### 5. Surface

#### Colour

![Colour palette]

- Colour justification

#### Typography

- Font justification

[Pricedown]

#### Imagery

- Own images
- Customers interested in condition

#### Text content

- [igdb.com]
- Model text

#### Responsive design

- Mobile first
- Progressive enhancement to bigger screens

---

## Features

- Include screenshots of everything

### Navbar

- Fully responsive
- Search bar

### Home page

- Introduction
- New arrivals

### Footer

- Newsletter
- Social CTAs

### Pagination of console > item type

- e.g. Console > Region > Games list > game detail

### Product detail page

- Add to basket

### Basket

- Remove products
- Keep shopping

### Checkout

- Confirm address
- Payment integration

### Profile

- Address
- Order history

### FAQ/Contact page

- HTML detail/summary
- Contact

### Error pages

- 404
- 403
- 500

### Favicon

- Where it was made and why

### Feedback system

- Django messages
- Toasts
- Login/registration status

### Admin CRUD functions

- Add, update and deletion of products

---

## Web marketing campaign

- FB Business page
- Reciprocal links
- Newsletter
- eCommerce business model in-depth

## SEO implementation

- Step-up from previous considerations
- robots.txt
- sitemap.xml
- meta tags
- rel attrs on external links
- URL design

---

## Data modelling

- PostgreSQL on ElephantSQL
- How to read the graph
- Note on custom models, with images for each

### Header for each model

### Complete schema

---

## Testing

- Intro on nature of testing carried out
- Mention what was automated and what was manual/integration

### Python testing

#### Automated test for each app

#### Coverage

### JavaScript testing

- Table

### Stripe/webhook testing

- Local vs deployed

### UX/User story testing

- Link to project iterations; mention index card presentation

### UI testing

- Mobile-first design
- Each component that was tested for responsiveness throughout development

---

## Validation

- Accessibility and SEO considerations

### HTML validation

Tool: [Nu Html Checker](https://validator.w3.org/nu/)

### CSS validation

Tool: [Jigsaw CSS Validation Service](https://jigsaw.w3.org/css-validator/)

### JavaScript validation

Tool: [JSHint](https://jshint.com/)

- Local = eslint, prettier

### Python validation

https://pep8ci.herokuapp.com/

- Local = ruff, pylance, black

### WAVE accessibility validation

Tool: [WAVE](https://wave.webaim.org/)

### Lighthouse reports

---

## Bugs

- Link to milestones

## Version control

- Conventional commits
- No commented-out code
- Filename conventions
- Settings (pyproject, formatters)

## Deployment

- See PP4 steps where appropriate
- [Boutique Ado guide](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2021_T1/courseware/eb05f06e62c64ac89823cc956fcd8191/40cc2543c48643fda09351da6fa90579/)
- [AWS guide](https://codeinstitute.s3.amazonaws.com/fullstack/AWS%20changes%20sheet.pdf)

### Breakdown by service provider

- Environment
- SECRET KEYS

- GitHub
- Heroku
- ElephantSQL
- Stripe
- AWS

### Cloning

- See PP4 if same

### Forking

- See PP4 if same

---

## Acknowledgements

- Code credit given in comments and docstrings
- Any tutorials if required
- Shoutouts to CI tutors, mentors, students past and present
- Any repos that served as inspiration
- Summary of year's learning
