'use strict';

/**
 * @param Horseman phantomInstance
 * @param string url
 */
module.exports = function (phantomInstance, url, loadPhantomInstance) {

  if (!url || typeof url !== 'string') {
    throw 'You must specify a url to gather links';
  }

  console.log('Getting links from: ', url);

  phantomInstance
    .open(url)

    // Optionally, determine the status of the response
    .status()
    .then(function (statusCode) {
      console.log('HTTP status code: ', statusCode);
      if (Number(statusCode) >= 400) {
        throw 'Page failed with status: ' + statusCode;
      }
    })

    // Interact with the page. This code is run in the browser.
    .evaluate(function () {
      $ = window.$ || window.jQuery;

      // Return a single result object with properties for
      // whatever intelligence you want to derive from the page
      var result = {
        links: []
      };

      if ($) {
        $('a').each(function (i, el) {
          var href = $(el).attr('href');
          if (href) {
            if (!href.match(/^(#|javascript|mailto)/) && href.match(/about_crc/) && result.links.indexOf(href) === -1) {
              result.links.push(href);
            }
          }
        });
      }
      // jQuery should be present, but if it's not, then collect the links using pure javascript
      else {
        var links = document.getElementsByTagName('a');
        for (var i = 0; i < links.length; i++) {
          var href = links[i].href;
          if (href) {
            if (!href.match(/^(#|javascript|mailto)/) && result.links.indexOf(href) === -1) {
              result.links.push(href);
            }
          }
        }
      }

      return result;
    })
    .then(function (result) {
      console.log('Success! Here are the derived links: \n', result.links);

      result.links.forEach( function( link ){
        var horseman = new loadPhantomInstance();
        horseman
          .open('http://www.colonscreen.gov.hk' + link)
          .evaluate(function () {
            $ = window.$ || window.jQuery;

            // Return a single result object with properties for
            // whatever intelligence you want to derive from the page
            var result = {
              title: "",
              content: []
            };

            if ($) {
              result.title = $('h1.title').text().trim();
              $('div.region-content p,div.region-content li').each(function (i, el) {
                result.content.push($(el).text().trim());
              });
            }

            return result;
          })
          .then(function (result) {
            console.log('Success! The title is: \n', result.title);
            var linkParts = link.split('/');
            var fileName = linkParts[linkParts.length - 1].replace(".html", ".json");

            var fs = require('fs');
            fs.writeFile('json_output/' + fileName, JSON.stringify(result), function(err) {
              if(err) {
                return console.log(err);
              }
              console.log("The file was saved!");
            });
          })
          .finally(function(){
            return horseman.close();
          });
      });
    })

    .catch(function (err) {
      console.log('Error getting links: ', err);
    })

    // Always close the Horseman instance, or you might end up with orphaned phantom processes
    .close();
};
