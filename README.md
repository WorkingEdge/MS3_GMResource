<a href="https://ms3-gm-resources.herokuapp.com/" target="_blank">View the live project here</a>


# Contents <!-- omit in toc -->  
- [Scenario Outline](#scenario-outline)
- [User Experience](#user-experience)
  - [User Stories by User Type](#user-stories-by-user-type)
    - [First-time or Infrequent Vistor](#first-time-or-infrequent-vistor)
    - [Contributing or Frequent User](#contributing-or-frequent-user)
    - [MS3 Seeds Admin User](#ms3-seeds-admin-user)
    - [Site Owner](#site-owner)
- [Design](#design)
    - [Colour](#colour)
    - [Typography](#typography)
    - [Images](#images)
      - [Cards](#cards)
- [Features](#features)
- [Technolgies Used](#technolgies-used)
- [Testing](#testing)
- [Known Issues](#known-issues)
- [Deployment](#deployment)
- [Credits](#credits)
- [Notes](#notes)
- [Appendix](#appendix)

# Scenario Outline
This is the (fictional) scenario for which the site exists:

**MS3 Seeds** is a niche supplier of seeds, specialising in <a href="https://en.wikipedia.org/wiki/Green_manure" target="_blank">green manures</a>.
It has set up this site to do the following:
* Generate awareness for their company among the relevant community of growers
* Establish their name as being recognized as a thought leader in the area
* Establish their name as being a trustworthy and open source of unbiased information as well as quality seeds
* Generate customers by facilitating an easy through-flow from the information-sharing site to the store
* Build a community of growers who automatically think 'MS3 Seeds' when they think of green manure

# User Experience
There are 3 user types  currently envisaged for the site:
* Infrequent or first-time vistor who has not registered as a user
* Contributing users who may add posts or comment on other contributors' posts
* Admin user who represents MS3 seeds in the posts and comments and who also has the ability to add or update the specific products shown as available from MS3 Seeds

## User Stories by User Type
### First-time or Infrequent Vistor
* As a first-time visitor, the purpose and overall content of the site is clear and easy to navigate
* I want to easily browse the site for posts and/or products that I may be interested in
* I can search for a term and see results in user posts and separately, results in the 'MS3 Seeds' product information
* I can read all content but I cannot comment on posts
* The site feels informative, authorative, and welcoming
* I can contact MS3 seeds directly from the site without having to register as a user
* I can see additional contact info - phone, address, social media
* I can easily register to become a contributing user of the site
* As a grower, I can see valuable, relevant information, including:
    * Common and latin name
    * Growing season
    * N-fixing ability of a species
    * Seeding rate
    * Main benefits
    * Cost
    * Experiences of other growers/photos  

### Contributing or Frequent User
* I can easily see the latest posts that have been added to the site, allowing me to recognize immediately if new content has been added
* I can view posts by other users and comment on any posts that interest me or where I want to communicate with the poster
* For any post that interests me, I can easily navigate from the post directly to the relevant MS3 product or products that contain the species that is the topic of the post. This may be to get purchase information, or to consult the additional information provided by MS3 Seeds on that particular seed type
* I can easily log in and add a post
* I can add an image url for the species that is the topic of my post
* I can see and go to the source of any images in other user posts. *A future feature would allow direct upload of images as preferable to hot-linking*
* On my profile page, I can see all posts that I have previously submitted and can navigate directly to any of them
* I can choosse to update or delete any post that I have previously submitted
* I cannot easily delete a post by mistake as there is a confirmation required
* I feel like a valued member of the discussion community with a custom message from MS3 Seeds on my profile page
* If I have any website issues, I can use the contact form without being logged in to submit a support request
    
### MS3 Seeds Admin User
* I have all the post/comment functionality of a contributing user
* In case of an offending post, I have the option to delete that post, regardless of user - **not implemented yet**
* In addition to the post/comment functinoality of a contributing user, I also have the option to administer the products. That means, I can add details for a new product, update existing details for a product (add or remove a particular species from a seed mix, for example) or delete a product from the list.

### Site Owner
* The site presents a positive image for the brand
* The site facilitates the emergence of a discussion community around green manures with the brand name central to that discussion
* Sales Generation: When any user adds a post, they must enter the 'common name' of the plant species that is the topic of their post. This is automatically used as a search criteria against all seed mixes and a link is automatically inserted on the post to link readers to the corresponding product. 

# Design
The site revolves around meaningful content. As such, the design should not get in the way of clear communication. 
Furthermore, as organic growers or farmers, users are probably not 24/7 internet users - the interface should be clean and easy to follow and any forms easy and straighforward to fill out.

### Colour
In line with the site content, the main colours used are teal, gold, white.

### Typography 
** To be decided ** I 

### Images
Images are a central part of the site 'data'. As they convey information and are not simply a design element, they are used sparingly outside of the dedicated image spaces.
The main image for the jumbotron has an overlay to prevent easy identification of the species but allow the theme of the site to come through. To make it clear that the jumbotron image is 'design' and not 'content', the same image is used on different pages regardless of species.
To differentiate pages that arise from the MS3 Seeds shop, the overlay becomes white rather than the default dark.

#### Cards
Latest posts are displayed as (Bootstrap) cards with image tops. The image in the card should match the image provided by the user for that post. However, the *Image URL* field is not mandatory for a user post. Therefore, as there may be cards that do not have a specified image, a default image is used. This keeps the presentation of the latest posts correct. Only one default image is used and it is quite unspecific, indicating to the user (especially any frequent user) that it is a default image.

**Note:** The deafult/fallback image is used only for the cards - inside the post itself, no image appears unless it has been specified by the user.

# Features

# Technolgies Used

# Testing

# Known Issues 

# Deployment

# Credits

# Notes
* Turn off debug mode before submitting - in app.py
* Password for secret key created using randomkeygen
* Favicon from https://iconarchive.com/browse.html

# Appendix
Background:
Green manures and cover crops are an important part of land management for horticultural enterprises, particularly in an organic context. They have numerous benefits - for example, some green manures fix nitrogen from the air and reduce the need for the application of synthetic fertilizer. Others may be beneficial for pollinating insects or for soil conditioning.

There are many different species and species mixes that are considered green manures or cover crops and each one has a particular application and is suited for different conditions. For example, some are for winter growing, others for summer. Some summer green manures die back naturally with cold weather, others need to be stopped/killed before the next crop can be sown.