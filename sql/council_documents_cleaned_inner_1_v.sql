SELECT substr(action_date, 7, 10) AS action_year, 
action_date, replace(
               replace(
                 replace(
                   replace(
                     replace(
                       replace(
                         replace(
                           replace(
                             replace(
                               replace(
                                 replace(
                                   replace(title, 'Voices Neighborhood Council', 'Voices of 90037 Neighborhood Council'),
              'Community Impact Statement from', ''),
              'Community Impact Statement submitted by ', ''),
              ' Community Council', ''),
              ' Neighborhood Council', ''),
              ' (e)', ''),
              'Bel-Air Beverly', 'Bel Air-Beverly'),
              'Community Impact Statement submitted by', ''),
               'Neighbhood Council', ''),
               ' ofs', ''),
               '- 2nd Submission', ''),
               'Neightborhood Council', '') AS council, file_name
FROM council_document 
WHERE title LIKE 'Community Impact Statement from%' or title LIKE 'Community Impact Statement submitted by%'